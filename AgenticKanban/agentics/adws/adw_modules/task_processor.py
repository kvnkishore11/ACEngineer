"""
Task Processor module for ADW workflows
Handles task lifecycle management and execution coordination
"""

import subprocess
import sys
import threading
import queue
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

from logger import WorkflowLogger, get_logger
from state_manager import StateManager, WorkflowStatus
from config_manager import ConfigManager
from file_ops import FileOperations


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class TaskExecution:
    """Task execution context"""
    adw_id: str
    stage: str
    pipeline_path: Path
    arguments: List[str]
    env_vars: Dict[str, str]
    timeout: int
    retry_count: int
    priority: TaskPriority = TaskPriority.MEDIUM
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    process: Optional[subprocess.Popen] = None


class TaskProcessor:
    """
    Processes tasks through pipeline stages with proper orchestration
    Handles execution, monitoring, and error recovery
    """

    def __init__(self, workspace_dir: Path = None):
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.logger = get_logger("task_processor")

        # Initialize components
        self.config_manager = ConfigManager(self.workspace_dir)
        self.state_manager = StateManager(self.workspace_dir / "agentics" / "agents")
        self.file_ops = FileOperations(self.workspace_dir)

        # Execution tracking
        self.active_executions: Dict[str, TaskExecution] = {}
        self.execution_queue = queue.PriorityQueue()
        self.shutdown_event = threading.Event()

        # Performance metrics
        self.metrics = {
            'tasks_processed': 0,
            'tasks_successful': 0,
            'tasks_failed': 0,
            'total_execution_time': 0,
            'average_execution_time': 0
        }

        # Load configuration
        self.config = self.config_manager.get_workflow_config()

    def process_task(self, task_data: Dict) -> bool:
        """
        Process a complete task through all stages

        Args:
            task_data: Task data dictionary

        Returns:
            True if task completed successfully, False otherwise
        """
        adw_id = task_data.get('adw_id')
        if not adw_id:
            self.logger.error("Task data missing adw_id")
            return False

        try:
            # Initialize state
            state = self.state_manager.initialize_state(task_data)
            workflow_logger = WorkflowLogger(adw_id, log_dir=Path(self.config.logs_dir))

            workflow_logger.info("Starting task processing")

            # Update status to executing
            self.state_manager.update_status(
                adw_id,
                WorkflowStatus.EXECUTING,
                "Processing task through stages"
            )

            # Execute each stage
            stages = state.stages
            total_stages = len(stages)
            start_time = datetime.now()

            for i, stage in enumerate(stages):
                if self.shutdown_event.is_set():
                    self.logger.info(f"Shutdown requested, stopping task {adw_id}")
                    break

                workflow_logger.log_stage_start(stage)

                # Update progress
                progress = (i / total_stages) * 100
                self.state_manager.update_stage(adw_id, stage, progress)
                self.state_manager.add_log(adw_id, "info", stage, f"Starting {stage} stage")

                # Execute stage
                success = self.execute_stage(adw_id, stage, workflow_logger)

                if success:
                    self.state_manager.complete_stage(adw_id, stage)
                    self.state_manager.add_log(adw_id, "success", stage, f"Completed {stage} stage successfully")
                    workflow_logger.log_stage_complete(stage)
                else:
                    error_msg = f"Stage {stage} failed"
                    self.state_manager.fail_stage(adw_id, stage, error_msg)
                    self.state_manager.add_log(adw_id, "error", stage, error_msg)
                    workflow_logger.log_stage_error(stage, error_msg)

                    if not self.config.pipeline_continue_on_failure:
                        workflow_logger.error("Stopping execution due to stage failure")
                        self.metrics['tasks_failed'] += 1
                        return False

            # Task completed
            execution_time = (datetime.now() - start_time).total_seconds()
            self.state_manager.update_status(
                adw_id,
                WorkflowStatus.COMPLETED,
                "Task execution completed successfully"
            )

            # Update metrics
            self.metrics['tasks_processed'] += 1
            self.metrics['tasks_successful'] += 1
            self.metrics['total_execution_time'] += execution_time
            self.metrics['average_execution_time'] = (
                self.metrics['total_execution_time'] / self.metrics['tasks_processed']
            )

            workflow_logger.info(f"Task completed successfully in {execution_time:.2f} seconds")
            return True

        except Exception as e:
            self.logger.error(f"Task processing failed for {adw_id}: {e}")
            self.state_manager.update_status(
                adw_id,
                WorkflowStatus.FAILED,
                f"Task processing error: {str(e)}",
                str(e)
            )
            self.metrics['tasks_failed'] += 1
            return False

    def execute_stage(self, adw_id: str, stage: str, workflow_logger: WorkflowLogger) -> bool:
        """
        Execute a specific stage of the workflow

        Args:
            adw_id: Task ID
            stage: Stage name to execute
            workflow_logger: Logger for this workflow

        Returns:
            True if stage executed successfully, False otherwise
        """
        try:
            # Get pipeline configuration
            pipeline_config = self.config_manager.get_pipeline_config(stage)
            if not pipeline_config:
                workflow_logger.warning(f"No pipeline configuration found for stage {stage}, using defaults")

            # Find pipeline script
            pipelines_dir = Path(self.config.pipelines_dir)
            if not pipelines_dir.is_absolute():
                pipelines_dir = self.workspace_dir / pipelines_dir

            pipeline_script = pipelines_dir / f"{stage}_pipeline.py"

            if not pipeline_script.exists():
                workflow_logger.warning(f"Pipeline script not found: {pipeline_script}")
                return self._execute_default_stage(adw_id, stage, workflow_logger)

            # Prepare execution context
            task_dir = self.state_manager.agents_dir / adw_id
            env_vars = self.config_manager.get_environment_variables(stage)

            # Build command arguments
            args = [
                sys.executable, str(pipeline_script),
                "--task-id", adw_id,
                "--task-dir", str(task_dir),
                "--stage", stage
            ]

            # Add pipeline-specific arguments
            if pipeline_config and pipeline_config.arguments:
                args.extend(pipeline_config.arguments)

            # Set timeout
            timeout = pipeline_config.timeout if pipeline_config else self.config.execution_timeout

            # Execute with retry logic
            max_retries = pipeline_config.retry_count if pipeline_config else self.config.max_retries

            for attempt in range(max_retries + 1):
                if attempt > 0:
                    workflow_logger.info(f"Retry attempt {attempt} for stage {stage}")
                    time.sleep(2 ** attempt)  # Exponential backoff

                success = self._execute_pipeline_script(
                    args, env_vars, timeout, workflow_logger, stage
                )

                if success:
                    return True

                if attempt < max_retries:
                    workflow_logger.warning(f"Stage {stage} failed, retrying...")

            workflow_logger.error(f"Stage {stage} failed after {max_retries + 1} attempts")
            return False

        except Exception as e:
            workflow_logger.error(f"Error executing stage {stage}: {e}")
            return False

    def _execute_pipeline_script(self, args: List[str], env_vars: Dict[str, str],
                                timeout: int, workflow_logger: WorkflowLogger,
                                stage: str) -> bool:
        """Execute pipeline script with proper monitoring"""
        try:
            workflow_logger.info(f"Executing pipeline: {' '.join(args)}")

            # Prepare environment
            execution_env = dict(env_vars)
            execution_env.update(env_vars)

            # Execute process
            process = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=execution_env,
                cwd=self.workspace_dir
            )

            # Log output
            if process.stdout:
                for line in process.stdout.strip().split('\n'):
                    if line.strip():
                        workflow_logger.info(f"Pipeline output: {line.strip()}")

            if process.stderr:
                for line in process.stderr.strip().split('\n'):
                    if line.strip():
                        workflow_logger.warning(f"Pipeline stderr: {line.strip()}")

            # Check return code
            success = process.returncode == 0
            if not success:
                workflow_logger.error(f"Pipeline exited with code {process.returncode}")

            return success

        except subprocess.TimeoutExpired:
            workflow_logger.error(f"Pipeline timed out after {timeout} seconds")
            return False
        except Exception as e:
            workflow_logger.error(f"Pipeline execution error: {e}")
            return False

    def _execute_default_stage(self, adw_id: str, stage: str,
                              workflow_logger: WorkflowLogger) -> bool:
        """Execute default stage behavior when no pipeline script is found"""
        try:
            workflow_logger.info(f"Executing default behavior for stage {stage}")

            # Simulate work
            time.sleep(2)

            # Create stage output
            task_dir = self.state_manager.agents_dir / adw_id
            output_file = task_dir / f"{stage}_output.json"

            output_data = {
                "stage": stage,
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "task_id": adw_id,
                "execution_type": "default",
                "message": f"Default {stage} stage execution completed"
            }

            success = self.file_ops.write_json_file(output_file, output_data)

            if success:
                workflow_logger.info(f"Default stage {stage} completed successfully")
            else:
                workflow_logger.error(f"Failed to write output for default stage {stage}")

            return success

        except Exception as e:
            workflow_logger.error(f"Default stage execution failed: {e}")
            return False

    def queue_task(self, task_data: Dict, priority: TaskPriority = TaskPriority.MEDIUM):
        """
        Queue task for processing

        Args:
            task_data: Task data dictionary
            priority: Task priority level
        """
        adw_id = task_data.get('adw_id')
        if not adw_id:
            self.logger.error("Cannot queue task without adw_id")
            return

        # Priority queue uses negative values for higher priority
        priority_value = -priority.value
        self.execution_queue.put((priority_value, datetime.now(), task_data))
        self.logger.info(f"Queued task {adw_id} with priority {priority.name}")

    def start_worker_threads(self, num_workers: int = 1):
        """
        Start worker threads for task processing

        Args:
            num_workers: Number of worker threads
        """
        for i in range(num_workers):
            worker_thread = threading.Thread(
                target=self._worker_loop,
                name=f"TaskWorker-{i}",
                daemon=True
            )
            worker_thread.start()
            self.logger.info(f"Started task worker thread {i}")

    def _worker_loop(self):
        """Worker thread main loop"""
        while not self.shutdown_event.is_set():
            try:
                # Get task from queue with timeout
                try:
                    priority, queued_at, task_data = self.execution_queue.get(timeout=1)
                except queue.Empty:
                    continue

                # Process task
                adw_id = task_data.get('adw_id', 'unknown')
                self.logger.info(f"Worker processing task: {adw_id}")

                success = self.process_task(task_data)

                if success:
                    self.logger.info(f"Task {adw_id} completed successfully")
                else:
                    self.logger.error(f"Task {adw_id} failed")

                # Mark task as done in queue
                self.execution_queue.task_done()

            except Exception as e:
                self.logger.error(f"Worker thread error: {e}")

    def get_metrics(self) -> Dict[str, Any]:
        """Get processing metrics"""
        return self.metrics.copy()

    def get_active_tasks(self) -> List[str]:
        """Get list of active task IDs"""
        return list(self.active_executions.keys())

    def stop_task(self, adw_id: str) -> bool:
        """
        Stop a running task

        Args:
            adw_id: Task ID to stop

        Returns:
            True if stopped successfully, False otherwise
        """
        try:
            if adw_id in self.active_executions:
                execution = self.active_executions[adw_id]
                if execution.process and execution.process.poll() is None:
                    execution.process.terminate()
                    self.logger.info(f"Terminated task {adw_id}")

            # Update state
            self.state_manager.update_status(
                adw_id,
                WorkflowStatus.CANCELLED,
                "Task execution cancelled by user"
            )

            return True

        except Exception as e:
            self.logger.error(f"Failed to stop task {adw_id}: {e}")
            return False

    def cleanup_completed_tasks(self, max_age_days: int = None) -> int:
        """
        Clean up old completed tasks

        Args:
            max_age_days: Override default cleanup age

        Returns:
            Number of tasks cleaned up
        """
        age_days = max_age_days or self.config.cleanup_age_days
        return self.state_manager.cleanup_completed_tasks(age_days)

    def shutdown(self):
        """Gracefully shutdown the task processor"""
        self.logger.info("Shutting down task processor...")
        self.shutdown_event.set()

        # Stop active processes
        for adw_id, execution in self.active_executions.items():
            if execution.process and execution.process.poll() is None:
                try:
                    execution.process.terminate()
                    self.logger.info(f"Terminated process for task {adw_id}")
                except:
                    pass

        self.logger.info("Task processor shutdown complete")
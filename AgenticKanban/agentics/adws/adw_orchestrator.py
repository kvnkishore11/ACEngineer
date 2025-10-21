#!/usr/bin/env python3
"""
Agentic Development Workflow (ADW) Orchestrator
Optimized for AgenticKanban direct integration with TAC-7 conventions

This orchestrator handles:
1. File-based trigger monitoring (for direct kanban integration)
2. Pipeline execution management
3. State tracking and reporting
4. Multi-stage workflow processing

Updated to use ADW primitive modules for better modularity and maintainability
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import threading
import queue
from dataclasses import dataclass, asdict
from enum import Enum

# Import ADW primitive modules
sys.path.append(str(Path(__file__).parent / "adw_modules"))
from logger import setup_logger, WorkflowLogger
from state_manager import StateManager, WorkflowStatus
from file_ops import FileOperations
from config_manager import ConfigManager
from task_processor import TaskProcessor, TaskPriority


# Use WorkflowStatus from state_manager module
# Legacy TaskStatus for compatibility
class TaskStatus(Enum):
    PENDING = "pending"
    INITIALIZING = "initializing"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TriggerSource(Enum):
    FILE_SYSTEM = "file_system"
    KANBAN_UI = "kanban_ui"
    API = "api"


@dataclass
class TaskData:
    adw_id: str
    title: str
    description: str
    type: str = "feature"
    priority: str = "medium"
    stages: List[str] = None
    created_at: str = None
    project_context: Dict = None
    execution_mode: str = "automatic"
    triggered_at: str = None
    kanban_integration: bool = True
    trigger_source: str = TriggerSource.KANBAN_UI.value
    ui_metadata: Dict = None
    workflow_status: str = "initialized"

    def __post_init__(self):
        if self.stages is None:
            self.stages = ["plan", "implement"]
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.project_context is None:
            self.project_context = {}


@dataclass
class ExecutionState:
    adw_id: str
    status: TaskStatus
    current_stage: str
    completed_stages: List[str]
    failed_stages: List[str]
    current_action: str
    progress: float
    logs: List[Dict]
    metrics: Dict
    started_at: str
    updated_at: str
    error_message: Optional[str] = None

    def to_dict(self):
        result = asdict(self)
        result['status'] = self.status.value
        return result


class ADWOrchestrator:
    def __init__(self, workspace_dir: Path = None):
        self.workspace_dir = workspace_dir or Path.cwd()
        self.agentics_dir = self.workspace_dir / "agentics"
        self.adws_dir = self.agentics_dir / "adws"
        self.agents_dir = self.agentics_dir / "agents"
        self.pipelines_dir = self.adws_dir / "pipelines"

        # Initialize ADW modules
        self.config_manager = ConfigManager(self.workspace_dir)
        self.config = self.config_manager.get_workflow_config()
        self.file_ops = FileOperations(self.workspace_dir)
        self.state_manager = StateManager(self.agents_dir)
        self.task_processor = TaskProcessor(self.workspace_dir)

        # Ensure directories exist
        self.file_ops.ensure_directory(self.agents_dir)
        self.file_ops.ensure_directory(self.pipelines_dir)
        self.file_ops.ensure_directory(self.adws_dir / "logs")

        # Setup logging using ADW logger
        self.logger = setup_logger(
            "adw_orchestrator",
            self.config.log_level,
            self.adws_dir / "logs",
            self.config.log_to_console
        )

        # Execution tracking (simplified with new modules)
        self.active_executions: Dict[str, str] = {}  # adw_id -> status
        self.execution_queue = queue.Queue()
        self.shutdown_event = threading.Event()

        # Start background workers
        self.start_workers()

    def setup_logging_legacy(self):
        """Legacy method - now handled by ADW modules"""
        pass

    def start_workers(self):
        """Start background worker threads"""
        # File system trigger monitor
        self.fs_monitor_thread = threading.Thread(
            target=self.monitor_file_triggers,
            daemon=True
        )
        self.fs_monitor_thread.start()

        # Start task processor workers
        self.task_processor.start_worker_threads(1)

        self.logger.info("ADW Orchestrator workers started")

    def monitor_file_triggers(self):
        """Monitor for file-based triggers from the Kanban UI"""
        processed_triggers = set()

        while not self.shutdown_event.is_set():
            try:
                # Scan for trigger files
                for trigger_file in self.adws_dir.glob("trigger_*.json"):
                    if trigger_file.name in processed_triggers:
                        continue

                    try:
                        with open(trigger_file, 'r') as f:
                            trigger_data = json.load(f)

                        self.logger.info(f"Processing file trigger: {trigger_file.name}")

                        # Load task data
                        task_file = Path(trigger_data.get('task_file', ''))
                        if not task_file.is_absolute():
                            task_file = self.adws_dir / task_file

                        if task_file.exists():
                            task_data_dict = self.file_ops.read_json_file(task_file)
                            if task_data_dict:
                                task_data = TaskData(**task_data_dict)
                                task_data.trigger_source = TriggerSource.KANBAN_UI.value

                                # Queue for execution
                                self.queue_task_execution(task_data)

                            # Mark as processed
                            processed_triggers.add(trigger_file.name)

                            # Optionally remove trigger file
                            try:
                                trigger_file.unlink()
                                self.logger.info(f"Removed processed trigger: {trigger_file.name}")
                            except OSError:
                                pass

                    except Exception as e:
                        self.logger.error(f"Error processing trigger {trigger_file}: {e}")

                time.sleep(2)  # Check every 2 seconds

            except Exception as e:
                self.logger.error(f"Error in file monitor: {e}")
                time.sleep(5)

    def queue_task_execution(self, task_data: TaskData):
        """Queue a task for execution using task processor"""
        # Convert TaskData to dict for task processor
        task_dict = asdict(task_data)

        # Determine priority based on task metadata
        priority = TaskPriority.MEDIUM
        if task_data.priority == "high":
            priority = TaskPriority.HIGH
        elif task_data.priority == "urgent":
            priority = TaskPriority.URGENT
        elif task_data.priority == "low":
            priority = TaskPriority.LOW

        self.task_processor.queue_task(task_dict, priority)
        self.logger.info(f"Queued task for execution: {task_data.adw_id}")

    def execution_worker_legacy(self):
        """Legacy worker - now handled by task processor"""
        pass

    def execute_task(self, task_data: TaskData):
        """Execute a task through the ADW pipeline using task processor"""
        try:
            # Convert TaskData to dict for task processor
            task_dict = asdict(task_data)

            # Track execution
            self.active_executions[task_data.adw_id] = "executing"
            self.logger.info(f"Starting execution for task: {task_data.adw_id}")

            # Use task processor for execution
            success = self.task_processor.process_task(task_dict)

            if success:
                self.active_executions[task_data.adw_id] = "completed"
                self.logger.info(f"Task execution completed: {task_data.adw_id}")
            else:
                self.active_executions[task_data.adw_id] = "failed"
                self.logger.error(f"Task execution failed: {task_data.adw_id}")

        except Exception as e:
            self.logger.error(f"Error executing task {task_data.adw_id}: {e}")
            self.active_executions[task_data.adw_id] = "failed"

    def execute_stage_legacy(self, task_data, stage, exec_state, task_dir):
        """Legacy method - now handled by task processor"""
        pass

    def save_execution_state_legacy(self, exec_state):
        """Legacy method - now handled by StateManager"""
        pass

    def process_api_trigger(self, task_data_dict: Dict) -> str:
        """Process an API-based trigger"""
        try:
            task_data = TaskData(**task_data_dict)
            task_data.trigger_source = TriggerSource.API.value

            self.logger.info(f"Processing API trigger: {task_data.adw_id}")

            # Queue for execution
            self.queue_task_execution(task_data)

            return task_data.adw_id

        except Exception as e:
            self.logger.error(f"Error processing API trigger: {e}")
            raise

    def get_execution_status(self, adw_id: str) -> Optional[Dict]:
        """Get current execution status for a task using state manager"""
        return self.state_manager.get_status_summary(adw_id)

    def list_active_executions(self) -> List[str]:
        """List all active execution IDs"""
        return self.state_manager.list_active_tasks()

    def shutdown(self):
        """Gracefully shutdown the orchestrator"""
        self.logger.info("Shutting down ADW Orchestrator...")
        self.shutdown_event.set()

        # Shutdown task processor
        self.task_processor.shutdown()

        # Wait for threads to finish
        if hasattr(self, 'fs_monitor_thread'):
            self.fs_monitor_thread.join(timeout=5)

        self.logger.info("ADW Orchestrator shutdown complete")


def main():
    """Main entry point for the orchestrator"""
    import argparse

    parser = argparse.ArgumentParser(description="ADW Orchestrator")
    parser.add_argument("--workspace", type=Path, help="Workspace directory")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("task_data", nargs="?", help="Task data JSON for single execution")

    args = parser.parse_args()

    # Initialize orchestrator
    orchestrator = ADWOrchestrator(workspace_dir=args.workspace)

    try:
        if args.task_data:
            # Single task execution mode
            task_data_dict = json.loads(args.task_data)
            task_data = TaskData(**task_data_dict)
            orchestrator.execute_task(task_data)
        elif args.daemon:
            # Daemon mode - keep running
            orchestrator.logger.info("Running in daemon mode...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                orchestrator.logger.info("Received interrupt signal")
        else:
            # Monitor mode - run until interrupted
            orchestrator.logger.info("Running in monitor mode...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                orchestrator.logger.info("Received interrupt signal")
    finally:
        orchestrator.shutdown()


if __name__ == "__main__":
    main()
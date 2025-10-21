import asyncio
import logging
import json
import subprocess
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from .database import AsyncSessionLocal, WorkflowTask
from .models import TaskStatus, WorkflowStage
from .websocket import notify_workflow_update

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskOrchestrator:
    """Background task orchestrator for executing ADW workflows"""

    def __init__(self):
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.task_queue = asyncio.Queue()
        self.is_running = False

    async def start(self):
        """Start the orchestrator and background worker"""
        if self.is_running:
            return

        self.is_running = True
        logger.info("Starting Task Orchestrator...")

        # Start background worker
        asyncio.create_task(self._worker())

        # Start task queue processor
        asyncio.create_task(self._process_queue())

    async def stop(self):
        """Stop the orchestrator and cancel running tasks"""
        self.is_running = False
        logger.info("Stopping Task Orchestrator...")

        # Cancel all running tasks
        for adw_id, task in self.running_tasks.items():
            task.cancel()
            logger.info(f"Cancelled task: {adw_id}")

        self.running_tasks.clear()

    async def submit_task(self, adw_id: str):
        """Submit a task for execution"""
        if adw_id in self.running_tasks:
            logger.warning(f"Task {adw_id} is already running")
            return

        await self.task_queue.put(adw_id)
        logger.info(f"Task {adw_id} submitted to queue")

    async def _worker(self):
        """Background worker that monitors for new pending tasks"""
        while self.is_running:
            try:
                async with AsyncSessionLocal() as db:
                    # Find pending tasks
                    result = await db.execute(
                        select(WorkflowTask).where(WorkflowTask.status == TaskStatus.PENDING.value)
                    )
                    pending_tasks = result.scalars().all()

                    for task in pending_tasks:
                        if task.adw_id not in self.running_tasks:
                            await self.submit_task(task.adw_id)

                # Wait before checking again
                await asyncio.sleep(5)

            except Exception as e:
                logger.error(f"Error in worker: {e}")
                await asyncio.sleep(10)

    async def _process_queue(self):
        """Process tasks from the queue"""
        while self.is_running:
            try:
                # Get task from queue
                adw_id = await self.task_queue.get()

                if adw_id not in self.running_tasks:
                    # Create and start task
                    task = asyncio.create_task(self._execute_workflow(adw_id))
                    self.running_tasks[adw_id] = task

                    # Clean up completed task
                    task.add_done_callback(
                        lambda t, aid=adw_id: self.running_tasks.pop(aid, None)
                    )

            except Exception as e:
                logger.error(f"Error processing queue: {e}")

    async def _execute_workflow(self, adw_id: str):
        """Execute a complete workflow for a task"""
        logger.info(f"Starting workflow execution for {adw_id}")

        async with AsyncSessionLocal() as db:
            try:
                # Get task details
                result = await db.execute(
                    select(WorkflowTask).where(WorkflowTask.adw_id == adw_id)
                )
                task = result.scalar_one_or_none()

                if not task:
                    logger.error(f"Task {adw_id} not found")
                    return

                # Update status to running
                await self._update_task_status(db, adw_id, TaskStatus.RUNNING)

                # Execute each stage
                for i, stage in enumerate(task.stages):
                    logger.info(f"Executing stage '{stage}' for task {adw_id}")

                    # Update current stage
                    await self._update_current_stage(db, adw_id, stage)

                    # Execute stage
                    stage_result = await self._execute_stage(adw_id, stage, task)

                    if not stage_result["success"]:
                        # Stage failed
                        await self._update_task_status(
                            db, adw_id, TaskStatus.FAILED,
                            error_message=stage_result.get("error", "Stage execution failed")
                        )
                        return

                    # Update progress
                    progress = int(((i + 1) / len(task.stages)) * 100)
                    await notify_workflow_update(adw_id, {
                        "type": "progress_update",
                        "data": {
                            "adw_id": adw_id,
                            "stage": stage,
                            "progress": progress,
                            "stage_result": stage_result
                        }
                    })

                # All stages completed successfully
                await self._update_task_status(
                    db, adw_id, TaskStatus.COMPLETED,
                    result={"completed_stages": task.stages, "success": True}
                )

                logger.info(f"Workflow {adw_id} completed successfully")

            except Exception as e:
                logger.error(f"Error executing workflow {adw_id}: {e}")
                await self._update_task_status(
                    db, adw_id, TaskStatus.FAILED,
                    error_message=f"Workflow execution error: {str(e)}"
                )

    async def _execute_stage(self, adw_id: str, stage: str, task: WorkflowTask) -> Dict[str, Any]:
        """Execute a specific workflow stage"""
        try:
            # Prepare stage execution
            stage_config = {
                "adw_id": adw_id,
                "stage": stage,
                "task_type": task.task_type,
                "title": task.title,
                "description": task.description,
                "timestamp": datetime.utcnow().isoformat()
            }

            # Determine execution method based on stage
            if stage == "plan":
                return await self._execute_plan_stage(stage_config)
            elif stage == "implement":
                return await self._execute_implement_stage(stage_config)
            elif stage == "test":
                return await self._execute_test_stage(stage_config)
            elif stage == "deploy":
                return await self._execute_deploy_stage(stage_config)
            else:
                return {
                    "success": False,
                    "error": f"Unknown stage: {stage}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Stage execution error: {str(e)}"
            }

    async def _execute_plan_stage(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute planning stage"""
        logger.info(f"Planning stage for {config['adw_id']}")

        # Simulate planning logic (replace with actual implementation)
        await asyncio.sleep(2)  # Simulate processing time

        return {
            "success": True,
            "stage": "plan",
            "result": {
                "plan_created": True,
                "estimated_time": "10 minutes",
                "files_to_modify": ["src/components/", "src/utils/"]
            }
        }

    async def _execute_implement_stage(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute implementation stage"""
        logger.info(f"Implementation stage for {config['adw_id']}")

        try:
            # Try to use existing ADW orchestrator as fallback
            adw_path = Path(__file__).parent.parent.parent / "agentics" / "adws" / "adw_orchestrator.py"

            if adw_path.exists():
                # Use the existing orchestrator
                result = await self._run_adw_orchestrator(config, adw_path)
                return result
            else:
                # Fallback implementation
                await asyncio.sleep(5)  # Simulate implementation time
                return {
                    "success": True,
                    "stage": "implement",
                    "result": {
                        "implementation_completed": True,
                        "files_modified": ["src/components/NewComponent.jsx"],
                        "lines_changed": 150
                    }
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Implementation failed: {str(e)}"
            }

    async def _execute_test_stage(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute testing stage"""
        logger.info(f"Testing stage for {config['adw_id']}")

        # Simulate testing logic
        await asyncio.sleep(3)

        return {
            "success": True,
            "stage": "test",
            "result": {
                "tests_run": 25,
                "tests_passed": 23,
                "tests_failed": 2,
                "coverage": "85%"
            }
        }

    async def _execute_deploy_stage(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deployment stage"""
        logger.info(f"Deployment stage for {config['adw_id']}")

        # Simulate deployment logic
        await asyncio.sleep(2)

        return {
            "success": True,
            "stage": "deploy",
            "result": {
                "deployment_successful": True,
                "build_time": "45 seconds",
                "deployment_url": "https://localhost:3000"
            }
        }

    async def _run_adw_orchestrator(self, config: Dict[str, Any], adw_path: Path) -> Dict[str, Any]:
        """Run the existing ADW orchestrator as a subprocess"""
        try:
            # Create temporary config file for the orchestrator
            temp_config = {
                "adw_id": config["adw_id"],
                "task_type": config["task_type"],
                "title": config["title"],
                "description": config["description"]
            }

            config_path = f"/tmp/adw_config_{config['adw_id']}.json"
            with open(config_path, "w") as f:
                json.dump(temp_config, f)

            # Run the orchestrator
            process = await asyncio.create_subprocess_exec(
                sys.executable, str(adw_path), "--config", config_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                return {
                    "success": True,
                    "stage": "implement",
                    "result": {
                        "adw_orchestrator_used": True,
                        "output": stdout.decode() if stdout else "",
                        "config_path": config_path
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"ADW orchestrator failed: {stderr.decode() if stderr else 'Unknown error'}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to run ADW orchestrator: {str(e)}"
            }

    async def _update_task_status(
        self,
        db: AsyncSession,
        adw_id: str,
        status: TaskStatus,
        error_message: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None
    ):
        """Update task status in database and notify WebSocket subscribers"""
        update_data = {
            "status": status.value,
            "updated_at": datetime.utcnow()
        }

        if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            update_data["completed_at"] = datetime.utcnow()

        if error_message:
            update_data["error_message"] = error_message

        if result:
            update_data["result"] = result

        await db.execute(
            update(WorkflowTask)
            .where(WorkflowTask.adw_id == adw_id)
            .values(**update_data)
        )
        await db.commit()

        # Notify WebSocket subscribers
        await notify_workflow_update(adw_id, {
            "type": "status_update",
            "data": {
                "adw_id": adw_id,
                "status": status.value,
                "error_message": error_message,
                "result": result
            }
        })

    async def _update_current_stage(self, db: AsyncSession, adw_id: str, stage: str):
        """Update current stage in database"""
        await db.execute(
            update(WorkflowTask)
            .where(WorkflowTask.adw_id == adw_id)
            .values(current_stage=stage, updated_at=datetime.utcnow())
        )
        await db.commit()

        # Notify WebSocket subscribers
        await notify_workflow_update(adw_id, {
            "type": "stage_update",
            "data": {
                "adw_id": adw_id,
                "current_stage": stage
            }
        })


# Global orchestrator instance
orchestrator = TaskOrchestrator()


async def start_orchestrator():
    """Start the global orchestrator"""
    await orchestrator.start()


async def stop_orchestrator():
    """Stop the global orchestrator"""
    await orchestrator.stop()


async def submit_task_for_execution(adw_id: str):
    """Submit a task to the orchestrator"""
    await orchestrator.submit_task(adw_id)
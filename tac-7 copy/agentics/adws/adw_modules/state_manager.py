"""
State Manager for ADW workflows
Handles reading, writing, and updating task state following TAC-7 conventions
"""

import json
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, asdict
from enum import Enum

from logger import get_logger


class WorkflowStatus(Enum):
    """Workflow status enumeration following TAC-7 conventions"""
    INITIALIZED = "initialized"
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class StateData:
    """Base state data structure following TAC-7 conventions"""
    adw_id: str
    title: str
    description: str
    type: str = "feature"
    priority: str = "medium"
    stages: List[str] = None
    workflow_status: str = WorkflowStatus.INITIALIZED.value
    current_stage: str = ""
    completed_stages: List[str] = None
    failed_stages: List[str] = None
    current_action: str = ""
    progress: float = 0.0
    created_at: str = None
    updated_at: str = None
    project_context: Dict = None
    execution_mode: str = "automatic"
    triggered_at: str = None
    kanban_integration: bool = True
    trigger_source: str = "kanban_ui"
    ui_metadata: Dict = None
    logs: List[Dict] = None
    metrics: Dict = None
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.stages is None:
            self.stages = ["plan", "implement"]
        if self.completed_stages is None:
            self.completed_stages = []
        if self.failed_stages is None:
            self.failed_stages = []
        if self.logs is None:
            self.logs = []
        if self.metrics is None:
            self.metrics = {}
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()


class StateManager:
    """
    Manages workflow state persistence and updates
    Thread-safe operations for concurrent access
    """

    def __init__(self, agents_dir: Path):
        self.agents_dir = Path(agents_dir)
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger("state_manager")
        self._locks = {}  # Per-task locks for thread safety

    def _get_lock(self, adw_id: str) -> threading.Lock:
        """Get or create lock for specific task"""
        if adw_id not in self._locks:
            self._locks[adw_id] = threading.Lock()
        return self._locks[adw_id]

    def _get_state_file(self, adw_id: str) -> Path:
        """Get path to state.json file for task"""
        task_dir = self.agents_dir / adw_id
        return task_dir / "state.json"

    def initialize_state(self, task_data: Dict) -> StateData:
        """
        Initialize state for new task following TAC-7 conventions

        Args:
            task_data: Raw task data from trigger

        Returns:
            StateData object
        """
        state = StateData(**task_data)
        state.workflow_status = WorkflowStatus.INITIALIZED.value
        state.updated_at = datetime.now().isoformat()

        self.save_state(state)
        return state

    def load_state(self, adw_id: str) -> Optional[StateData]:
        """
        Load state from state.json file

        Args:
            adw_id: Task ID

        Returns:
            StateData object or None if not found
        """
        state_file = self._get_state_file(adw_id)

        if not state_file.exists():
            return None

        try:
            with open(state_file, 'r') as f:
                data = json.load(f)

            return StateData(**data)

        except Exception as e:
            self.logger.error(f"Failed to load state for {adw_id}: {e}")
            return None

    def save_state(self, state: StateData) -> bool:
        """
        Save state to state.json file (thread-safe)

        Args:
            state: StateData object

        Returns:
            True if successful, False otherwise
        """
        lock = self._get_lock(state.adw_id)

        with lock:
            try:
                # Ensure task directory exists
                task_dir = self.agents_dir / state.adw_id
                task_dir.mkdir(parents=True, exist_ok=True)

                # Update timestamp
                state.updated_at = datetime.now().isoformat()

                # Write state file
                state_file = self._get_state_file(state.adw_id)
                state_data = asdict(state)

                with open(state_file, 'w') as f:
                    json.dump(state_data, f, indent=2)

                return True

            except Exception as e:
                self.logger.error(f"Failed to save state for {state.adw_id}: {e}")
                return False

    def update_status(self, adw_id: str, status: WorkflowStatus,
                     current_action: str = "", error_message: str = None) -> bool:
        """
        Update workflow status and action

        Args:
            adw_id: Task ID
            status: New workflow status
            current_action: Current action description
            error_message: Error message if failed

        Returns:
            True if successful, False otherwise
        """
        state = self.load_state(adw_id)
        if not state:
            return False

        state.workflow_status = status.value
        if current_action:
            state.current_action = current_action
        if error_message:
            state.error_message = error_message

        return self.save_state(state)

    def update_stage(self, adw_id: str, stage: str, progress: float = None) -> bool:
        """
        Update current stage and progress

        Args:
            adw_id: Task ID
            stage: Current stage name
            progress: Progress percentage (0-100)

        Returns:
            True if successful, False otherwise
        """
        state = self.load_state(adw_id)
        if not state:
            return False

        state.current_stage = stage
        state.workflow_status = WorkflowStatus.EXECUTING.value

        if progress is not None:
            state.progress = progress

        return self.save_state(state)

    def complete_stage(self, adw_id: str, stage: str) -> bool:
        """
        Mark stage as completed

        Args:
            adw_id: Task ID
            stage: Stage name to complete

        Returns:
            True if successful, False otherwise
        """
        state = self.load_state(adw_id)
        if not state:
            return False

        if stage not in state.completed_stages:
            state.completed_stages.append(stage)

        # Remove from failed stages if present
        if stage in state.failed_stages:
            state.failed_stages.remove(stage)

        # Update progress
        total_stages = len(state.stages)
        completed_count = len(state.completed_stages)
        state.progress = (completed_count / total_stages) * 100

        # Check if all stages completed
        if completed_count == total_stages:
            state.workflow_status = WorkflowStatus.COMPLETED.value
            state.current_stage = "completed"
            state.current_action = "Task execution completed"

        return self.save_state(state)

    def fail_stage(self, adw_id: str, stage: str, error_message: str) -> bool:
        """
        Mark stage as failed

        Args:
            adw_id: Task ID
            stage: Stage name that failed
            error_message: Error description

        Returns:
            True if successful, False otherwise
        """
        state = self.load_state(adw_id)
        if not state:
            return False

        if stage not in state.failed_stages:
            state.failed_stages.append(stage)

        # Remove from completed stages if present
        if stage in state.completed_stages:
            state.completed_stages.remove(stage)

        state.workflow_status = WorkflowStatus.FAILED.value
        state.error_message = error_message

        return self.save_state(state)

    def add_log(self, adw_id: str, level: str, stage: str, message: str) -> bool:
        """
        Add log entry to state

        Args:
            adw_id: Task ID
            level: Log level (info, warning, error, success)
            stage: Current stage
            message: Log message

        Returns:
            True if successful, False otherwise
        """
        state = self.load_state(adw_id)
        if not state:
            return False

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "stage": stage,
            "message": message
        }

        state.logs.append(log_entry)

        return self.save_state(state)

    def get_status_summary(self, adw_id: str) -> Optional[Dict]:
        """
        Get status summary for task

        Args:
            adw_id: Task ID

        Returns:
            Status summary dict or None
        """
        state = self.load_state(adw_id)
        if not state:
            return None

        return {
            "adw_id": state.adw_id,
            "workflow_status": state.workflow_status,
            "current_stage": state.current_stage,
            "current_action": state.current_action,
            "progress": state.progress,
            "completed_stages": state.completed_stages,
            "failed_stages": state.failed_stages,
            "error_message": state.error_message,
            "updated_at": state.updated_at
        }

    def list_active_tasks(self) -> List[str]:
        """
        List all active task IDs

        Returns:
            List of task IDs with state files
        """
        active_tasks = []

        for task_dir in self.agents_dir.iterdir():
            if task_dir.is_dir():
                state_file = task_dir / "state.json"
                if state_file.exists():
                    active_tasks.append(task_dir.name)

        return active_tasks

    def cleanup_completed_tasks(self, max_age_days: int = 7) -> int:
        """
        Clean up old completed tasks

        Args:
            max_age_days: Maximum age in days for completed tasks

        Returns:
            Number of tasks cleaned up
        """
        cleanup_count = 0
        cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 3600)

        for task_id in self.list_active_tasks():
            state = self.load_state(task_id)
            if not state:
                continue

            if (state.workflow_status == WorkflowStatus.COMPLETED.value and
                datetime.fromisoformat(state.updated_at.replace('Z', '+00:00')).timestamp() < cutoff_time):

                try:
                    task_dir = self.agents_dir / task_id
                    # Archive instead of delete for safety
                    import shutil
                    archive_dir = self.agents_dir.parent / "archived" / task_id
                    archive_dir.parent.mkdir(exist_ok=True)
                    shutil.move(str(task_dir), str(archive_dir))
                    cleanup_count += 1
                    self.logger.info(f"Archived completed task: {task_id}")
                except Exception as e:
                    self.logger.error(f"Failed to archive task {task_id}: {e}")

        return cleanup_count
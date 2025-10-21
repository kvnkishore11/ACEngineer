"""
TAC-7 Compatible ADW State Management
Persistent state with file persistence for isolated workflow execution
"""

import json
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any, List, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import subprocess

try:
    from pydantic import BaseModel, validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    # Fallback for systems without pydantic
    class BaseModel:
        pass

from logger import get_logger


class WorkflowPhase(Enum):
    """TAC-7 Workflow phases"""
    PLAN = "plan"
    BUILD = "build"
    TEST = "test"
    REVIEW = "review"
    DOCUMENT = "document"
    SHIP = "ship"


class WorkflowStatus(Enum):
    """TAC-7 Workflow status enumeration"""
    INITIALIZED = "initialized"
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


if PYDANTIC_AVAILABLE:
    class ADWStateData(BaseModel):
        """Pydantic model for ADW state validation (TAC-7 compatible)"""
        adw_id: str
        issue_number: Optional[int] = None
        branch_name: Optional[str] = None
        plan_file: Optional[str] = None
        worktree_path: Optional[str] = None
        backend_port: Optional[int] = None
        frontend_port: Optional[int] = None
        model_set: str = "default"

        # Workflow tracking
        workflow_status: str = WorkflowStatus.INITIALIZED.value
        current_phase: str = ""
        completed_phases: List[str] = field(default_factory=list)
        failed_phases: List[str] = field(default_factory=list)
        all_adws: List[str] = field(default_factory=list)

        # Task metadata
        title: str = ""
        description: str = ""
        type: str = "feature"
        priority: str = "medium"

        # Execution tracking
        current_action: str = ""
        progress: float = 0.0
        created_at: str = field(default_factory=lambda: datetime.now().isoformat())
        updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
        logs: List[Dict] = field(default_factory=list)
        metrics: Dict = field(default_factory=dict)
        error_message: Optional[str] = None

        @validator('backend_port')
        def validate_backend_port(cls, v):
            if v is not None and not (9100 <= v <= 9114):
                raise ValueError('Backend port must be between 9100-9114')
            return v

        @validator('frontend_port')
        def validate_frontend_port(cls, v):
            if v is not None and not (9200 <= v <= 9214):
                raise ValueError('Frontend port must be between 9200-9214')
            return v

        class Config:
            arbitrary_types_allowed = True
else:
    # Fallback dataclass when pydantic is not available
    @dataclass
    class ADWStateData:
        adw_id: str
        issue_number: Optional[int] = None
        branch_name: Optional[str] = None
        plan_file: Optional[str] = None
        worktree_path: Optional[str] = None
        backend_port: Optional[int] = None
        frontend_port: Optional[int] = None
        model_set: str = "default"
        workflow_status: str = WorkflowStatus.INITIALIZED.value
        current_phase: str = ""
        completed_phases: List[str] = field(default_factory=list)
        failed_phases: List[str] = field(default_factory=list)
        all_adws: List[str] = field(default_factory=list)
        title: str = ""
        description: str = ""
        type: str = "feature"
        priority: str = "medium"
        current_action: str = ""
        progress: float = 0.0
        created_at: str = field(default_factory=lambda: datetime.now().isoformat())
        updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
        logs: List[Dict] = field(default_factory=list)
        metrics: Dict = field(default_factory=dict)
        error_message: Optional[str] = None


class ADWState:
    """
    TAC-7 Compatible ADW State Management
    Storage: agents/{adw_id}/adw_state.json (following TAC-7 path convention)

    Core TAC-7 Features:
    - Persistent state with file persistence
    - Port allocation system (9100-9114 backend, 9200-9214 frontend)
    - Worktree isolation tracking
    - Workflow phase tracking
    - Validation using Pydantic when available
    """

    def __init__(self, workspace_dir: Path):
        self.workspace_dir = Path(workspace_dir)
        self.agents_dir = self.workspace_dir / "agentics" / "agents"
        self.trees_dir = self.workspace_dir / "trees"  # TAC-7 worktree location

        # Ensure directories exist
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.trees_dir.mkdir(parents=True, exist_ok=True)

        self.logger = get_logger("adw_state")
        self._locks = {}  # Per-task locks for thread safety

    def _get_lock(self, adw_id: str) -> threading.Lock:
        """Get or create lock for specific task"""
        if adw_id not in self._locks:
            self._locks[adw_id] = threading.Lock()
        return self._locks[adw_id]

    def _get_state_file(self, adw_id: str) -> Path:
        """Get path to adw_state.json file for task (TAC-7 convention)"""
        task_dir = self.agents_dir / adw_id
        return task_dir / "adw_state.json"

    def ensure_adw_id(self, task_data: Dict) -> str:
        """
        Ensure ADW ID exists, create if needed
        TAC-7 requirement for state initialization
        """
        adw_id = task_data.get('adw_id')
        if not adw_id:
            # Generate ADW ID if not provided
            title = task_data.get('title', 'task')
            timestamp = int(datetime.now().timestamp() * 1000)
            hash_suffix = abs(hash(title)) % 10000
            adw_id = f"adw_{timestamp}_{hash_suffix}"
            task_data['adw_id'] = adw_id

        return adw_id

    def allocate_ports(self, adw_id: str) -> tuple[int, int]:
        """
        TAC-7 Deterministic Port Allocation System
        Backend: 9100-9114, Frontend: 9200-9214
        """
        # Use hash of adw_id for deterministic port allocation
        hash_value = abs(hash(adw_id)) % 15
        backend_port = 9100 + hash_value
        frontend_port = 9200 + hash_value

        self.logger.info(f"Allocated ports for {adw_id}: backend={backend_port}, frontend={frontend_port}")
        return backend_port, frontend_port

    def generate_branch_name(self, adw_id: str, issue_number: Optional[int] = None,
                           task_type: str = "feature") -> str:
        """
        Generate standardized branch name following TAC-7 conventions
        Format: {type}-{issue_number}-{adw_id} or {type}-{adw_id}
        """
        # Clean up adw_id to remove prefix if present
        clean_adw_id = adw_id.replace("adw_", "") if adw_id.startswith("adw_") else adw_id

        if issue_number:
            branch_name = f"{task_type}-{issue_number}-{clean_adw_id}"
        else:
            branch_name = f"{task_type}-{clean_adw_id}"

        # Sanitize branch name
        branch_name = branch_name.lower().replace(" ", "-").replace("_", "-")
        return branch_name

    def get_worktree_path(self, adw_id: str) -> Path:
        """Get worktree path following TAC-7 convention: trees/{adw_id}/"""
        return self.trees_dir / adw_id

    def create_ports_env(self, adw_id: str, backend_port: int, frontend_port: int) -> bool:
        """
        Create .ports.env file for TAC-7 environment isolation
        """
        try:
            worktree_path = self.get_worktree_path(adw_id)
            if not worktree_path.exists():
                self.logger.warning(f"Worktree doesn't exist for {adw_id}, creating directory")
                worktree_path.mkdir(parents=True, exist_ok=True)

            ports_env_file = worktree_path / ".ports.env"
            env_content = f"""# TAC-7 Port Configuration for {adw_id}
BACKEND_PORT={backend_port}
FRONTEND_PORT={frontend_port}
VITE_BACKEND_URL=http://localhost:{backend_port}
ADW_ID={adw_id}
"""
            with open(ports_env_file, 'w') as f:
                f.write(env_content)

            self.logger.info(f"Created .ports.env for {adw_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create .ports.env for {adw_id}: {e}")
            return False

    def validate_worktree(self, adw_id: str) -> Dict[str, bool]:
        """
        TAC-7 Three-way Worktree Validation:
        1. State has worktree_path
        2. Directory exists on filesystem
        3. Git recognizes the worktree
        """
        state = self.load_state(adw_id)

        validation = {
            "state_has_path": False,
            "directory_exists": False,
            "git_recognizes": False,
            "valid": False
        }

        if not state:
            return validation

        # Check 1: State has worktree_path
        if state.worktree_path:
            validation["state_has_path"] = True
            worktree_path = Path(state.worktree_path)

            # Check 2: Directory exists
            if worktree_path.exists() and worktree_path.is_dir():
                validation["directory_exists"] = True

                # Check 3: Git recognizes worktree
                try:
                    result = subprocess.run(
                        ["git", "worktree", "list"],
                        capture_output=True,
                        text=True,
                        cwd=self.workspace_dir
                    )
                    if result.returncode == 0 and str(worktree_path) in result.stdout:
                        validation["git_recognizes"] = True
                except Exception as e:
                    self.logger.error(f"Git worktree validation failed: {e}")

        validation["valid"] = all([
            validation["state_has_path"],
            validation["directory_exists"],
            validation["git_recognizes"]
        ])

        return validation

    def initialize_state(self, task_data: Dict) -> ADWStateData:
        """
        Initialize TAC-7 compatible state for new task
        """
        adw_id = self.ensure_adw_id(task_data)

        # Allocate ports
        backend_port, frontend_port = self.allocate_ports(adw_id)

        # Generate branch name
        issue_number = task_data.get('issue_number')
        task_type = task_data.get('type', 'feature')
        branch_name = self.generate_branch_name(adw_id, issue_number, task_type)

        # Set worktree path
        worktree_path = str(self.get_worktree_path(adw_id))

        # Create state data
        state_data = {
            **task_data,
            'adw_id': adw_id,
            'branch_name': branch_name,
            'worktree_path': worktree_path,
            'backend_port': backend_port,
            'frontend_port': frontend_port,
            'workflow_status': WorkflowStatus.INITIALIZED.value,
        }

        if PYDANTIC_AVAILABLE:
            state = ADWStateData(**state_data)
        else:
            state = ADWStateData(**state_data)

        # Track this ADW in all_adws list
        existing_state = self.load_state(adw_id)
        if existing_state and adw_id not in existing_state.all_adws:
            state.all_adws = existing_state.all_adws + [adw_id]
        elif not existing_state:
            state.all_adws = [adw_id]

        self.save_state(state)

        # Create ports environment file
        self.create_ports_env(adw_id, backend_port, frontend_port)

        return state

    def load_state(self, adw_id: str) -> Optional[ADWStateData]:
        """Load state from adw_state.json file"""
        state_file = self._get_state_file(adw_id)

        if not state_file.exists():
            return None

        try:
            with open(state_file, 'r') as f:
                data = json.load(f)

            if PYDANTIC_AVAILABLE:
                return ADWStateData(**data)
            else:
                return ADWStateData(**data)

        except Exception as e:
            self.logger.error(f"Failed to load state for {adw_id}: {e}")
            return None

    def save_state(self, state: ADWStateData) -> bool:
        """Save state to adw_state.json file (thread-safe)"""
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

                if PYDANTIC_AVAILABLE:
                    state_data = state.dict()
                else:
                    state_data = asdict(state)

                with open(state_file, 'w') as f:
                    json.dump(state_data, f, indent=2)

                return True

            except Exception as e:
                self.logger.error(f"Failed to save state for {state.adw_id}: {e}")
                return False

    def update_phase(self, adw_id: str, phase: WorkflowPhase,
                    status: WorkflowStatus = WorkflowStatus.EXECUTING) -> bool:
        """Update current workflow phase"""
        state = self.load_state(adw_id)
        if not state:
            return False

        state.current_phase = phase.value
        state.workflow_status = status.value

        return self.save_state(state)

    def complete_phase(self, adw_id: str, phase: WorkflowPhase) -> bool:
        """Mark phase as completed"""
        state = self.load_state(adw_id)
        if not state:
            return False

        if phase.value not in state.completed_phases:
            state.completed_phases.append(phase.value)

        # Remove from failed phases if present
        if phase.value in state.failed_phases:
            state.failed_phases.remove(phase.value)

        return self.save_state(state)

    def fail_phase(self, adw_id: str, phase: WorkflowPhase, error_message: str) -> bool:
        """Mark phase as failed"""
        state = self.load_state(adw_id)
        if not state:
            return False

        if phase.value not in state.failed_phases:
            state.failed_phases.append(phase.value)

        state.workflow_status = WorkflowStatus.FAILED.value
        state.error_message = error_message

        return self.save_state(state)

    def get_all_adws(self) -> List[str]:
        """Get list of all ADW IDs that have been tracked"""
        all_adws = set()

        for task_dir in self.agents_dir.iterdir():
            if task_dir.is_dir():
                state = self.load_state(task_dir.name)
                if state:
                    all_adws.update(state.all_adws)

        return sorted(list(all_adws))

    def list_active_tasks(self) -> List[str]:
        """List all tasks with state files"""
        active_tasks = []

        for task_dir in self.agents_dir.iterdir():
            if task_dir.is_dir():
                state_file = task_dir / "adw_state.json"
                if state_file.exists():
                    active_tasks.append(task_dir.name)

        return active_tasks
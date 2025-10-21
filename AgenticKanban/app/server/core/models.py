from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TaskType(str, Enum):
    """Enumeration of supported task types"""
    FEATURE = "feature"
    BUG = "bug"
    ENHANCEMENT = "enhancement"
    REFACTOR = "refactor"
    DOCUMENTATION = "documentation"


class TaskStatus(str, Enum):
    """Enumeration of task status values"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStage(str, Enum):
    """Enumeration of workflow stages"""
    PLAN = "plan"
    IMPLEMENT = "implement"
    TEST = "test"
    DEPLOY = "deploy"


class WorkflowCreateRequest(BaseModel):
    """Request model for creating a new workflow task"""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    task_type: TaskType = Field(..., description="Type of task")
    stages: List[WorkflowStage] = Field(..., min_items=1, description="Workflow stages to execute")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication to the API",
                "task_type": "feature",
                "stages": ["plan", "implement", "test"]
            }
        }
    }


class WorkflowUpdateRequest(BaseModel):
    """Request model for updating a workflow task"""
    status: Optional[TaskStatus] = Field(None, description="New task status")
    current_stage: Optional[WorkflowStage] = Field(None, description="Current workflow stage")
    result: Optional[Dict[str, Any]] = Field(None, description="Task execution result")
    error_message: Optional[str] = Field(None, max_length=2000, description="Error message if task failed")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "running",
                "current_stage": "implement",
                "result": {"files_modified": ["src/auth.py", "src/models.py"]}
            }
        }
    }


class WorkflowResponse(BaseModel):
    """Response model for workflow task data"""
    id: int = Field(..., description="Database ID")
    adw_id: str = Field(..., description="Unique ADW identifier")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    task_type: TaskType = Field(..., description="Type of task")
    status: TaskStatus = Field(..., description="Current task status")
    stages: List[WorkflowStage] = Field(..., description="Workflow stages")
    current_stage: Optional[WorkflowStage] = Field(None, description="Current stage being executed")
    result: Optional[Dict[str, Any]] = Field(None, description="Task execution result")
    error_message: Optional[str] = Field(None, description="Error message if task failed")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Task completion timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "adw_id": "adw_feature_auth_1635789123",
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication to the API",
                "task_type": "feature",
                "status": "running",
                "stages": ["plan", "implement", "test"],
                "current_stage": "implement",
                "result": {"files_modified": ["src/auth.py"]},
                "error_message": None,
                "created_at": "2023-11-01T10:30:00Z",
                "updated_at": "2023-11-01T10:35:00Z",
                "completed_at": None
            }
        }
    }


class WorkflowListResponse(BaseModel):
    """Response model for listing workflow tasks"""
    tasks: List[WorkflowResponse] = Field(..., description="List of workflow tasks")
    total: int = Field(..., description="Total number of tasks")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Tasks per page")


class WebSocketMessage(BaseModel):
    """Model for WebSocket messages"""
    type: str = Field(..., description="Message type")
    adw_id: str = Field(..., description="Associated ADW ID")
    data: Dict[str, Any] = Field(..., description="Message payload")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "status_update",
                "adw_id": "adw_feature_auth_1635789123",
                "data": {
                    "status": "running",
                    "current_stage": "implement",
                    "progress": 45
                },
                "timestamp": "2023-11-01T10:35:00Z"
            }
        }
    }


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "Task not found",
                "details": {"adw_id": "adw_feature_auth_1635789123"},
                "timestamp": "2023-11-01T10:35:00Z"
            }
        }
    }
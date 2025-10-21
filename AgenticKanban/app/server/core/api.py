from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
import uuid
import time
from datetime import datetime

from .database import get_db, WorkflowTask
from .models import (
    WorkflowCreateRequest,
    WorkflowUpdateRequest,
    WorkflowResponse,
    WorkflowListResponse,
    ErrorResponse,
    TaskStatus
)
from .websocket import notify_workflow_update
from .orchestrator import submit_task_for_execution

router = APIRouter(tags=["workflows"])


def generate_adw_id(task_type: str) -> str:
    """Generate unique ADW ID for a task"""
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4())[:8]
    return f"adw_{task_type}_{timestamp}_{unique_id}"


@router.post("/workflows/create", response_model=WorkflowResponse, status_code=201)
async def create_workflow(
    request: WorkflowCreateRequest,
    db: AsyncSession = Depends(get_db)
) -> WorkflowResponse:
    """Create a new workflow task with immediate response"""
    try:
        # Generate unique ADW ID
        adw_id = generate_adw_id(request.task_type.value)

        # Create new workflow task
        task = WorkflowTask(
            adw_id=adw_id,
            title=request.title,
            description=request.description,
            task_type=request.task_type.value,
            status=TaskStatus.PENDING.value,
            stages=request.stages,
            current_stage=None,
            result=None,
            error_message=None
        )

        db.add(task)
        await db.commit()
        await db.refresh(task)

        # Create response
        response = WorkflowResponse(
            id=task.id,
            adw_id=task.adw_id,
            title=task.title,
            description=task.description,
            task_type=task.task_type,
            status=task.status,
            stages=task.stages,
            current_stage=task.current_stage,
            result=task.result,
            error_message=task.error_message,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )

        # Notify WebSocket subscribers
        await notify_workflow_update(adw_id, {
            "type": "task_created",
            "data": response.model_dump()
        })

        # Submit task to orchestrator for execution
        await submit_task_for_execution(adw_id)

        return response

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create workflow task: {str(e)}"
        )


@router.get("/workflows/{adw_id}", response_model=WorkflowResponse)
async def get_workflow(
    adw_id: str,
    db: AsyncSession = Depends(get_db)
) -> WorkflowResponse:
    """Get workflow task by ADW ID"""
    result = await db.execute(
        select(WorkflowTask).where(WorkflowTask.adw_id == adw_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Workflow task with ADW ID '{adw_id}' not found"
        )

    return WorkflowResponse(
        id=task.id,
        adw_id=task.adw_id,
        title=task.title,
        description=task.description,
        task_type=task.task_type,
        status=task.status,
        stages=task.stages,
        current_stage=task.current_stage,
        result=task.result,
        error_message=task.error_message,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at
    )


@router.put("/workflows/{adw_id}/status", response_model=WorkflowResponse)
async def update_workflow_status(
    adw_id: str,
    request: WorkflowUpdateRequest,
    db: AsyncSession = Depends(get_db)
) -> WorkflowResponse:
    """Update workflow task status and progress"""
    # Check if task exists
    result = await db.execute(
        select(WorkflowTask).where(WorkflowTask.adw_id == adw_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Workflow task with ADW ID '{adw_id}' not found"
        )

    # Prepare update data
    update_data = {"updated_at": datetime.utcnow()}

    if request.status is not None:
        update_data["status"] = request.status.value
        if request.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            update_data["completed_at"] = datetime.utcnow()

    if request.current_stage is not None:
        update_data["current_stage"] = request.current_stage.value

    if request.result is not None:
        update_data["result"] = request.result

    if request.error_message is not None:
        update_data["error_message"] = request.error_message

    # Update task
    await db.execute(
        update(WorkflowTask)
        .where(WorkflowTask.adw_id == adw_id)
        .values(**update_data)
    )
    await db.commit()

    # Fetch updated task
    result = await db.execute(
        select(WorkflowTask).where(WorkflowTask.adw_id == adw_id)
    )
    updated_task = result.scalar_one()

    response = WorkflowResponse(
        id=updated_task.id,
        adw_id=updated_task.adw_id,
        title=updated_task.title,
        description=updated_task.description,
        task_type=updated_task.task_type,
        status=updated_task.status,
        stages=updated_task.stages,
        current_stage=updated_task.current_stage,
        result=updated_task.result,
        error_message=updated_task.error_message,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at,
        completed_at=updated_task.completed_at
    )

    # Notify WebSocket subscribers
    await notify_workflow_update(adw_id, {
        "type": "status_update",
        "data": response.model_dump()
    })

    return response


@router.delete("/workflows/{adw_id}", status_code=204)
async def delete_workflow(
    adw_id: str,
    db: AsyncSession = Depends(get_db)
) -> None:
    """Cancel/delete a workflow task"""
    # Check if task exists
    result = await db.execute(
        select(WorkflowTask).where(WorkflowTask.adw_id == adw_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Workflow task with ADW ID '{adw_id}' not found"
        )

    # Update status to cancelled instead of deleting
    await db.execute(
        update(WorkflowTask)
        .where(WorkflowTask.adw_id == adw_id)
        .values(
            status=TaskStatus.CANCELLED.value,
            updated_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )
    )
    await db.commit()

    # Notify WebSocket subscribers
    await notify_workflow_update(adw_id, {
        "type": "task_cancelled",
        "data": {"adw_id": adw_id, "status": "cancelled"}
    })


@router.get("/workflows", response_model=WorkflowListResponse)
async def list_workflows(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    task_type: Optional[str] = Query(None, description="Filter by task type"),
    db: AsyncSession = Depends(get_db)
) -> WorkflowListResponse:
    """List workflow tasks with pagination and filtering"""
    # Build query
    query = select(WorkflowTask)

    if status:
        query = query.where(WorkflowTask.status == status)

    if task_type:
        query = query.where(WorkflowTask.task_type == task_type)

    # Get total count
    count_result = await db.execute(
        select(WorkflowTask).where(query.whereclause)
    )
    total = len(count_result.scalars().all())

    # Apply pagination
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page).order_by(WorkflowTask.created_at.desc())

    # Execute query
    result = await db.execute(query)
    tasks = result.scalars().all()

    # Convert to response models
    task_responses = [
        WorkflowResponse(
            id=task.id,
            adw_id=task.adw_id,
            title=task.title,
            description=task.description,
            task_type=task.task_type,
            status=task.status,
            stages=task.stages,
            current_stage=task.current_stage,
            result=task.result,
            error_message=task.error_message,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )
        for task in tasks
    ]

    return WorkflowListResponse(
        tasks=task_responses,
        total=total,
        page=page,
        per_page=per_page
    )
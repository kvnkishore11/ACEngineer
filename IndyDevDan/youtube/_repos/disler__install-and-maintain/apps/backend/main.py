"""Simple FastAPI backend for the Setup Hook demo."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Starter API", version="0.1.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = Path(__file__).parent / "starter.db"


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class Task(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: str


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Database connection context manager."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@app.get("/")
def root() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "message": "Starter API is running"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[dict]:
    """Get all tasks."""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [
            {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "completed": bool(row["completed"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> dict:
    """Get a single task by ID."""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "completed": bool(row["completed"]),
            "created_at": row["created_at"],
        }


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate) -> dict:
    """Create a new task."""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (task.title, task.description),
        )
        conn.commit()
        task_id = cursor.lastrowid
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "completed": bool(row["completed"]),
            "created_at": row["created_at"],
        }


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate) -> dict:
    """Update an existing task."""
    with get_db() as conn:
        # Check if task exists
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Task not found")

        # Build update query
        updates = []
        values = []
        if task.title is not None:
            updates.append("title = ?")
            values.append(task.title)
        if task.description is not None:
            updates.append("description = ?")
            values.append(task.description)
        if task.completed is not None:
            updates.append("completed = ?")
            values.append(int(task.completed))

        if updates:
            values.append(task_id)
            conn.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
                values,
            )
            conn.commit()

        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "completed": bool(row["completed"]),
            "created_at": row["created_at"],
        }


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    """Delete a task."""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Task not found")
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return {"message": "Task deleted"}

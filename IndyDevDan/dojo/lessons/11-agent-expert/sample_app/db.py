"""sample_app/db.py — the data layer the database expert owns. DO NOT EDIT.

House conventions (a database expert knows these cold):
1. EVERY query flows through _execute() — the single gateway. Never call
   conn.execute() directly; _execute is the one choke point for logging,
   retries, and future migrations.
2. SQL is always parameterized with ? placeholders — values are never
   interpolated into the SQL string.
3. The schema lives in schema.sql next to this file; connect() applies it.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "schema.sql"

_conn: sqlite3.Connection | None = None


def connect(path: str = ":memory:") -> sqlite3.Connection:
    """Open the database and apply schema.sql. Call this once, first."""
    global _conn
    _conn = sqlite3.connect(path)
    _conn.row_factory = sqlite3.Row
    _conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    return _conn


def _execute(sql: str, params: tuple = ()) -> sqlite3.Cursor:
    """The single gateway: every query in this data layer flows through here."""
    if _conn is None:
        raise RuntimeError("call connect() before querying")
    cur = _conn.execute(sql, params)  # parameterized, always
    _conn.commit()
    return cur


def insert_task(title: str, done: bool = False) -> int:
    """Add a task; returns its id."""
    cur = _execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, int(done)))
    return cur.lastrowid


def list_tasks(include_done: bool = True) -> list[dict]:
    """All tasks as dicts, optionally hiding completed ones."""
    if include_done:
        rows = _execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    else:
        rows = _execute("SELECT id, title, done FROM tasks WHERE done = ? ORDER BY id", (0,)).fetchall()
    return [dict(r) for r in rows]

"""Initialize the SQLite database with mock tables and data."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "starter.db"

def init_database() -> None:
    """Create tables and insert mock data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check if we already have data
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert mock data
        mock_tasks = [
            ("Setup Python backend", "Configure FastAPI with SQLite", 1),
            ("Create Vue frontend", "Scaffold Vite Vue-TS project", 1),
            ("Implement CRUD API", "Add endpoints for tasks", 0),
            ("Connect frontend to backend", "Use fetch to call API", 0),
            ("Test the application", "Verify everything works", 0),
        ]
        cursor.executemany(
            "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
            mock_tasks
        )
        print(f"Inserted {len(mock_tasks)} mock tasks")

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_database()

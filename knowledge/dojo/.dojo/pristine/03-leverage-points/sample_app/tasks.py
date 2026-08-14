#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""tasks — a tiny task-tracker CLI.

Usage:
  python3 tasks.py add "water the bonsai"
  python3 tasks.py list
  python3 tasks.py done 1

It works — and it is bad agentic code. Run it: silence. No stdout, no type hints.
A human can open tasks.json to see what happened; an agent watching stdout sees nothing.
Open the two leverage points (standard out, types) without changing behavior.
"""
import json
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not DB_PATH.exists():
        return []
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def save_tasks(tasks):
    DB_PATH.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(tasks, text):  # ____  # YOUR TURN: add type hints — (tasks: list[dict], text: str) -> dict
    task = {"id": len(tasks) + 1, "text": text, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    # ____  # YOUR TURN: print what happened (leverage point: stdout) — e.g. added #<id>: <text>
    return task


def list_tasks(tasks):  # ____  # YOUR TURN: add type hints — (tasks: list[dict]) -> None
    for task in tasks:
        # ____  # YOUR TURN: print each task (leverage point: stdout) — its id, a done/open marker, and its text
        pass


def complete_task(tasks, task_id):  # ____  # YOUR TURN: add type hints — (tasks: list[dict], task_id: int) -> dict | None
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            # ____  # YOUR TURN: print the confirmation (leverage point: stdout) — e.g. done #<id>: <text>
            return task
    return None


def main():
    args = sys.argv[1:]
    tasks = load_tasks()
    if args[:1] == ["add"] and len(args) > 1:
        add_task(tasks, " ".join(args[1:]))
    elif args[:1] == ["list"]:
        list_tasks(tasks)
    elif args[:1] == ["done"] and len(args) > 1:
        complete_task(tasks, int(args[1]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()

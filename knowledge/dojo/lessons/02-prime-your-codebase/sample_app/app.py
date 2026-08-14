"""TaskTrail CLI — entry point. Parses argv and routes commands to the JSON store in db.py."""
import json
import sys
from pathlib import Path

from db import load_tasks, save_tasks

CONFIG = json.loads((Path(__file__).parent / "config.json").read_text(encoding="utf-8"))


def main() -> None:
    args = sys.argv[1:]
    tasks = load_tasks()
    if args[:1] == ["add"] and len(args) > 1:
        text = " ".join(args[1:])
        tasks.append({"id": len(tasks) + 1, "text": text, "done": False})
        save_tasks(tasks)
        print(f"added #{len(tasks)}: {text}")
    elif args[:1] == ["list"]:
        for task in tasks:
            marker = "x" if task["done"] else " "
            print(f"#{task['id']} [{marker}] {task['text']}")
    elif args[:1] == ["done"] and len(args) > 1:
        for task in tasks:
            if task["id"] == int(args[1]):
                task["done"] = True
                save_tasks(tasks)
                print(f"done #{task['id']}: {task['text']}")
    else:
        print(f"{CONFIG['app_name']}: usage — add <text> | list | done <id>")


if __name__ == "__main__":
    main()

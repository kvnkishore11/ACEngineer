"""TaskTrail storage layer — tasks live in a JSON file (path comes from config.json)."""
import json
from pathlib import Path

_CONFIG = json.loads((Path(__file__).parent / "config.json").read_text(encoding="utf-8"))
DB_PATH = Path(__file__).parent / _CONFIG["db_path"]


def load_tasks() -> list[dict]:
    """Return every task, oldest first. A missing file means an empty tracker."""
    if not DB_PATH.exists():
        return []
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def save_tasks(tasks: list[dict]) -> None:
    """Write the full task list back to disk, pretty-printed for humans and agents."""
    DB_PATH.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

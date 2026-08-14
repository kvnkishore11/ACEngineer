#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-dotenv"]
# ///
"""
Claude Code SessionStart Hook: Load Environment Variables

Triggered by: Session start, resume, clear, or compact
Purpose: Load environment variables from .env file into CLAUDE_ENV_FILE
         so they persist across all bash commands in the session.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import dotenv_values

# Log file in the same directory as this script
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "session_start.log"


class Logger:
    """Simple logger that writes to both stderr and a log file (appends)."""

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_path, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"=== SessionStart Hook: {datetime.now().isoformat()} ===\n")
            f.write(f"{'='*60}\n")

    def log(self, message: str) -> None:
        """Print to stderr and append to log file."""
        print(message, file=sys.stderr)
        with open(self.log_path, "a") as f:
            f.write(message + "\n")


logger = Logger(LOG_FILE)


def main() -> None:
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    logger.log("")
    logger.log("HOOK INPUT (JSON received via stdin from Claude Code):")
    logger.log("-" * 60)
    logger.log(json.dumps(hook_input, indent=2) if hook_input else "{}")
    logger.log("")

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    env_file_path = os.environ.get("CLAUDE_ENV_FILE")
    source = hook_input.get("source", "unknown")
    session_id = hook_input.get("session_id", "unknown")

    logger.log("Claude Code SessionStart Hook: Loading Environment")
    logger.log("-" * 60)
    logger.log(f"Source: {source}")
    logger.log(f"Session ID: {session_id}")
    logger.log(f"Project directory: {project_dir}")
    logger.log(f"CLAUDE_ENV_FILE: {env_file_path or 'not set'}")
    logger.log(f"Log file: {LOG_FILE}")

    # Look for .env file in project root
    dotenv_path = Path(project_dir) / ".env"

    # Track what we loaded
    loaded_vars = []

    if env_file_path:
        # Load variables from .env if it exists
        if dotenv_path.exists():
            logger.log(f"\n>>> Loading variables from {dotenv_path}...")
            env_vars = dotenv_values(dotenv_path)
            with open(env_file_path, "a") as f:
                for key, value in env_vars.items():
                    if value is not None:
                        # Escape any single quotes in the value
                        escaped_value = value.replace("'", "'\"'\"'")
                        f.write(f"export {key}='{escaped_value}'\n")
                        loaded_vars.append(key)
                        logger.log(f"  Loaded: {key}")
        else:
            logger.log(f"\n>>> No .env file found at {dotenv_path}")

        # Always add a mock variable for demonstration
        logger.log("\n>>> Adding mock session variable...")
        with open(env_file_path, "a") as f:
            f.write("export MOCK_SESSION_VAR='hello_from_session_start'\n")
        loaded_vars.append("MOCK_SESSION_VAR")
        logger.log("  Added: MOCK_SESSION_VAR='hello_from_session_start'")
    else:
        logger.log("\n>>> CLAUDE_ENV_FILE not available - cannot persist variables")

    logger.log("\n" + "-" * 60)
    logger.log("SessionStart Complete!")
    logger.log("-" * 60)

    # Build output context
    context_parts = [f"SessionStart hook ran (source: {source})."]

    if loaded_vars:
        context_parts.append(f"Loaded environment variables: {', '.join(loaded_vars)}")
    else:
        context_parts.append(
            "No CLAUDE_ENV_FILE available - environment variables not persisted."
        )

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": " ".join(context_parts),
        }
    }

    logger.log("")
    logger.log("HOOK OUTPUT (JSON returned via stdout to Claude Code):")
    logger.log("-" * 60)
    logger.log(json.dumps(output, indent=2))

    # Log completion timestamp
    with open(LOG_FILE, "a") as f:
        f.write(f"\n=== SessionStart Hook Completed: {datetime.now().isoformat()} ===\n")

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()

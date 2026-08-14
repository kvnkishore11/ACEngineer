#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""PostToolUse hook: validate every JSON file the agent writes under data/.

The closed loop, wired into the harness: request → validate → resolve.
Claude Code pipes the PostToolUse payload to stdin after every tool call.

Exit 0 → work is valid, or not ours to judge: stay silent, let the agent roll.
Exit 2 → block: everything on stderr is fed BACK to the agent as feedback,
         and the agent resolves the problem itself.
"""

import json
import sys
from pathlib import Path

REQUIRED_KEYS = ("name", "version")


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # malformed hook input is our plumbing's fault — never punish the agent

    file_path = payload.get("tool_input", {}).get("file_path", "")

    path = Path(file_path)
    if path.suffix != ".json" or "data" not in path.parts:
        sys.exit(0)

    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(
            f"{file_path} is not valid JSON ({exc}). "
            "Rewrite the file so it parses cleanly.",
            file=sys.stderr,
        )
        sys.exit(2)

    missing = [key for key in REQUIRED_KEYS if key not in doc]
    if missing:
        print(
            f"{file_path} is missing required key(s): {', '.join(missing)}. "
            "Every config under data/ must define 'name' and 'version'. "
            "Add the missing key(s) and save the file again.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)  # valid — the loop closes clean


if __name__ == "__main__":
    main()

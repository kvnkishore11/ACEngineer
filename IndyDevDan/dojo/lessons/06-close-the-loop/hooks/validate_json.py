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

    # YOUR TURN: extract the edited file's path from the payload. PostToolUse
    # payloads nest it at tool_input -> file_path. Use .get() with defaults so
    # a missing key never crashes the hook.
    file_path = ____

    path = Path(file_path)
    # YOUR TURN: the applicability test. This hook only judges .json files that
    # live under a data/ directory — check the suffix and whether "data" is in
    # path.parts. Everything else is not our class of work: exit 0 silently.
    if ____:
        sys.exit(0)

    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(
            f"{file_path} is not valid JSON ({exc}). "
            "Rewrite the file so it parses cleanly.",
            file=sys.stderr,
        )
        # YOUR TURN: the blocking exit code. Exit 2 tells Claude Code to feed
        # stderr back to the agent — request → validate → resolve.
        sys.exit(____)

    # YOUR TURN: the validation. Collect every key from REQUIRED_KEYS that is
    # missing from doc — a list comprehension does it in one line.
    missing = ____
    if missing:
        print(
            f"{file_path} is missing required key(s): {', '.join(missing)}. "
            "Every config under data/ must define 'name' and 'version'. "
            "Add the missing key(s) and save the file again.",
            file=sys.stderr,
        )
        # YOUR TURN: same blocking exit code — the loop stays open until the
        # agent resolves the feedback.
        sys.exit(____)

    sys.exit(0)  # valid — the loop closes clean


if __name__ == "__main__":
    main()

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 06 close-the-loop.

Deterministic, offline, stdlib-only. Runs the learner's PostToolUse hook the
way Claude Code would — payload JSON on stdin — and asserts the exit-code
protocol. Never calls an LLM.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "06 close-the-loop"

HOOK = HERE / "hooks" / "validate_json.py"
SETTINGS = HERE / "settings.sample.json"
PAYLOAD_GOOD = HERE / "fixtures" / "payload_good.json"
PAYLOAD_BAD = HERE / "fixtures" / "payload_bad.json"

NOT_APPLICABLE_PAYLOAD = {
    "session_id": "5b9e6b0e-2f4c-4a1a-9c3e-7d2f8a41c9d0",
    "hook_event_name": "PostToolUse",
    "tool_name": "Write",
    "tool_input": {"file_path": "notes/handbook.md", "content": "# notes\n"},
    "tool_response": {"filePath": "notes/handbook.md", "success": True},
}


def scan_blanks() -> list[str]:
    hits = []
    for p in sorted(HERE.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(HERE)
        if "solution" in rel.parts or p.name in ("check.py", "README.md", "hints.md"):
            continue
        try:
            n = p.read_text(encoding="utf-8").count("____")
        except (UnicodeDecodeError, OSError):
            continue
        if n:
            hits.append(f"{rel}: {n} blank(s) left — fill every `____` (the YOUR TURN comments say what goes where)")
    return hits


def run_hook(stdin_text: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=HERE,  # fixture file_paths are lesson-relative
        timeout=15,
    )


def main() -> int:
    failures: list[str] = []

    blanks = scan_blanks()
    if blanks:
        report(blanks)
        return 1

    for f in (HOOK, SETTINGS, PAYLOAD_GOOD, PAYLOAD_BAD):
        if not f.exists():
            failures.append(f"{f.relative_to(HERE)} is missing — restore it (just reset 06)")
    if failures:
        report(failures)
        return 1

    # The hook stays a uv single-file script: PEP 723 header + uv shebang.
    hook_text = HOOK.read_text(encoding="utf-8")
    head = "\n".join(hook_text.splitlines()[:12])
    if "uv run --script" not in head:
        failures.append("hooks/validate_json.py lost its `#!/usr/bin/env -S uv run --script` shebang — keep it a uv single-file script")
    if "/// script" not in head:
        failures.append("hooks/validate_json.py lost its PEP 723 `# /// script` header — Dan's hooks always declare their deps inline (here: none)")

    # Closed loop test 1: valid work → exit 0, silent.
    proc = run_hook(PAYLOAD_GOOD.read_text(encoding="utf-8"))
    if proc.returncode != 0:
        failures.append(
            f"fed fixtures/payload_good.json, the hook exited {proc.returncode} (want 0) — "
            f"data/config_good.json has both required keys; valid work must pass silently. stderr: {proc.stderr.strip()[:200]!r}"
        )

    # Closed loop test 2: invalid work → exit 2 + actionable stderr.
    proc = run_hook(PAYLOAD_BAD.read_text(encoding="utf-8"))
    if proc.returncode != 2:
        failures.append(
            f"fed fixtures/payload_bad.json, the hook exited {proc.returncode} (want 2) — "
            "data/config_bad.json is missing 'version'; exit 2 is the code that blocks and feeds stderr back to the agent"
        )
    if not proc.stderr.strip():
        failures.append(
            "fed fixtures/payload_bad.json, the hook printed nothing to stderr — "
            "stderr IS the feedback the agent gets; name the file, the missing key, and the fix"
        )

    # Closed loop test 3: not our class of work → exit 0.
    proc = run_hook(json.dumps(NOT_APPLICABLE_PAYLOAD))
    if proc.returncode != 0:
        failures.append(
            f"fed a payload for notes/handbook.md (not a .json under data/), the hook exited {proc.returncode} (want 0) — "
            "the applicability test must let everything outside data/*.json pass untouched"
        )

    # Registration: the hook must be wired to the PostToolUse event.
    try:
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        hooks_cfg = settings.get("hooks", {})
        if "PostToolUse" not in hooks_cfg:
            failures.append(
                "settings.sample.json does not register the PostToolUse event — "
                f"the hooks key(s) found: {sorted(hooks_cfg)} — validators judge finished work, so they fire AFTER the tool call"
            )
        elif "validate_json.py" not in json.dumps(hooks_cfg["PostToolUse"]):
            failures.append("settings.sample.json PostToolUse entry never runs validate_json.py — point the command at the hook")
    except json.JSONDecodeError as exc:
        failures.append(f"settings.sample.json is not valid JSON ({exc}) — a broken settings file silently disables every hook")

    report(failures)
    return 1 if failures else 0


def report(failures: list[str]) -> None:
    if not failures:
        print(f"✅ PASS — {SLUG}")
        print("   your hook closes the loop: request → validate → resolve. Exit 2 does the teaching now.")
        return
    print(f"❌ FAIL — {SLUG}")
    for i, msg in enumerate(failures, 1):
        print(f"  {i}. {msg}")


if __name__ == "__main__":
    sys.exit(main())

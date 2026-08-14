#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""agent.py — a minimal custom agent harness. No SDK, no magic: the Core Four laid bare.

AH-3: "The system prompt is the most important element of your custom agents.
With zero exceptions." Below it: a tool registry (strip everything the agent
doesn't need) and a PreToolUse hook (governance). Overwrite the system prompt,
pick the tools — "this is not Claude Code anymore... you change the product."

Usage:  DOJO_MOCK=1 python3 agent.py
(mock mode replays fixtures/session.jsonl through the registry + hook — the
model is mocked, the governance is real)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE / "workspace"
FIXTURES = HERE / "fixtures" / "session.jsonl"
TRANSCRIPT = HERE / "transcript.jsonl"

# -- 1. The system prompt: the law for this agent ------------------------------
# YOUR TURN (first blank): the role line. The first line of the system prompt IS
# the agent. State it plainly: this is a read-only codebase QA agent — it answers
# questions about the files in workspace/ and never modifies anything.
# YOUR TURN (second blank): the output-format rule. Every answer must cite the
# workspace file paths it read, and the final line must start with "ANSWER:".
SYSTEM_PROMPT = """\
You are a read-only codebase QA agent. You answer questions about the files in
workspace/ and you never modify anything.

## Instructions
- Only inspect files inside workspace/. Never write, never execute.
- If a tool call is denied, say so and move on — do not retry it.

## Output format
- Cite every workspace file path you read, and end every response with a final
  line that starts with "ANSWER:".
"""

# -- 2. Tools: deterministic code the agent can call ---------------------------


def read_file(path: str) -> str:
    """Return the text of one file inside the workspace."""
    return (WORKSPACE / path).resolve().read_text(encoding="utf-8")


def list_files(path: str = ".") -> str:
    """List every file under a workspace directory."""
    root = (WORKSPACE / path).resolve()
    return "\n".join(
        sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
    )


def run_bash(cmd: str) -> str:
    """Run an arbitrary shell command. DANGEROUS — this agent must never hold it."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


# YOUR TURN: the registry — strip the tools. This is a QA agent: "This agent
# cannot write. It's a QA agent. Why would it need to write anything?" Register
# EXACTLY the two read-only tools (name → function). run_bash is defined above
# and it stays OUT: a tool your agent doesn't hold is a tool it can't misuse.
TOOLS: dict = {
    "read_file": read_file,
    "list_files": list_files,
}

# -- 3. The hook: governance before every tool call ----------------------------


def pre_tool_hook(tool: str, args: dict) -> bool:
    """PreToolUse gate. Return True to allow the call, False to deny it.

    Hooks are "essential for governance, for control, for permissions in all of
    your agents." The registry says WHICH tools exist; the hook says WHEN a call
    is acceptable.
    """
    if tool in ("read_file", "list_files"):
        target = (WORKSPACE / args.get("path", ".")).resolve()
        # YOUR TURN: block the escape. Deny any call whose resolved target lands
        # OUTSIDE the workspace/ directory — compare target against WORKSPACE
        # (Path.is_relative_to is your friend) and return False when it escapes.
        if not target.is_relative_to(WORKSPACE):
            return False
    return True


# -- 4. The agent loop ----------------------------------------------------------


def run_session() -> None:
    """Mock-driven loop: replay a scripted session through registry + hook.

    A real model would choose the tool calls; here fixtures/session.jsonl does.
    Everything else — registry lookup, hook gate, transcript — is exactly what a
    live agent loop runs.
    """
    if os.environ.get("DOJO_MOCK") != "1":
        sys.exit("live mode is not wired in this harness — run: DOJO_MOCK=1 python3 agent.py")
    TRANSCRIPT.unlink(missing_ok=True)
    calls = [
        json.loads(line)
        for line in FIXTURES.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for call in calls:
        tool, args = call["tool"], call.get("args", {})
        if tool not in TOOLS:
            record = {"tool": tool, "args": args, "status": "denied", "reason": "not in registry"}
        elif not pre_tool_hook(tool, args):
            record = {"tool": tool, "args": args, "status": "denied", "reason": "blocked by hook"}
        else:
            try:
                output = TOOLS[tool](**args)
                record = {"tool": tool, "args": args, "status": "ok", "output_chars": len(output)}
            except Exception as exc:  # a failing tool is a report, not a crash
                record = {"tool": tool, "args": args, "status": "error", "reason": str(exc)}
        suffix = "" if record["status"] == "ok" else f" ({record.get('reason')})"
        print(f"[agent] {tool} -> {record['status']}{suffix}")
        with TRANSCRIPT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    print(f"[agent] transcript: {TRANSCRIPT.name} ({len(calls)} tool calls)")


if __name__ == "__main__":
    run_session()

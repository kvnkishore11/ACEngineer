#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""check.py — closed-loop validator for 09 custom-agent. Deterministic, offline, stdlib-only."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LESSON = "09 custom-agent"
AGENT = HERE / "agent.py"
TRANSCRIPT = HERE / "transcript.jsonl"


def scan_blanks(problems: list[str]) -> None:
    if AGENT.exists():
        n = AGENT.read_text(encoding="utf-8").count("____")
        if n:
            problems.append(
                f"blanks remain — fill every ____ before the loop can close: agent.py ({n})"
            )


def check_structure(problems: list[str]) -> None:
    for rel in ("agent.py", "fixtures/session.jsonl", "workspace/notes.md", "workspace/app.py"):
        if not (HERE / rel).exists():
            problems.append(f"missing file: {rel} — restore it (just reset 09)")


def load_agent():
    spec = importlib.util.spec_from_file_location("dojo_agent_09", AGENT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_definitions(problems: list[str]) -> bool:
    try:
        mod = load_agent()
    except Exception as exc:
        problems.append(f"agent.py failed to import: {exc!r} — fix the file before the loop can close")
        return False

    sp = getattr(mod, "SYSTEM_PROMPT", "")
    if not isinstance(sp, str) or not sp.strip():
        problems.append("SYSTEM_PROMPT is missing or empty — the system prompt IS the agent")
    else:
        if not re.search(r"(?i)read[- ]?only", sp):
            problems.append(
                "SYSTEM_PROMPT never says the agent is read-only — the role line is the law; "
                "state it: a read-only codebase QA agent"
            )
        if not re.search(r"(?i)\bQA\b", sp):
            problems.append(
                "SYSTEM_PROMPT never names the role (QA) — say what this agent IS, not just what it avoids"
            )
        if not re.search(r"(?i)answer:", sp):
            problems.append(
                'SYSTEM_PROMPT has no output-format rule — require the final line to start with "ANSWER:"'
            )
        if not re.search(r"(?i)\bcit(e|es|ing|ation)\b", sp):
            problems.append(
                "SYSTEM_PROMPT never requires citing file paths — a QA answer without citations is a guess"
            )

    tools = getattr(mod, "TOOLS", None)
    if not isinstance(tools, dict):
        problems.append("TOOLS must be a dict mapping tool names to functions")
    else:
        if "run_bash" in tools:
            problems.append(
                "run_bash is registered in TOOLS — strip it. This agent cannot execute; "
                "a tool it doesn't hold is a tool it can't misuse"
            )
        expected = {"read_file", "list_files"}
        if set(tools) != expected:
            problems.append(
                f"TOOLS registers {sorted(tools)} — register exactly {sorted(expected)}"
            )
        elif not all(callable(fn) for fn in tools.values()):
            problems.append("every TOOLS value must be a callable (the tool function itself)")

    hook = getattr(mod, "pre_tool_hook", None)
    if not callable(hook):
        problems.append("pre_tool_hook is missing — the governance gate must exist")
    else:
        try:
            if hook("read_file", {"path": "notes.md"}) is not True:
                problems.append(
                    "pre_tool_hook denies a legitimate workspace read (notes.md) — "
                    "governance blocks escapes, not the agent's actual job"
                )
            if hook("read_file", {"path": "../check.py"}) is not False:
                problems.append(
                    "pre_tool_hook allows a path that resolves OUTSIDE workspace/ "
                    "(../check.py) — resolve the target and deny the escape"
                )
        except Exception as exc:
            problems.append(f"pre_tool_hook raised {exc!r} — the gate must return True/False, never crash")
    return True


def check_session(problems: list[str]) -> None:
    env = dict(os.environ)
    env["DOJO_MOCK"] = "1"
    proc = subprocess.run(
        [sys.executable, str(AGENT)],
        cwd=HERE, env=env, capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
        problems.append(
            f"DOJO_MOCK=1 python3 agent.py exited {proc.returncode} — last output: {' | '.join(tail)}"
        )
        return
    if not TRANSCRIPT.exists():
        problems.append("no transcript.jsonl written — the loop must log every tool call")
        return
    records = [
        json.loads(line)
        for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(records) != 4:
        problems.append(f"transcript has {len(records)} records — the scripted session makes 4 tool calls")
        return
    r_read, r_list, r_escape, r_bash = records
    if r_read.get("tool") != "read_file" or r_read.get("status") != "ok":
        problems.append(
            f"call 1 (read notes.md) recorded {r_read.get('status')!r} — the allowed read must succeed"
        )
    if r_list.get("tool") != "list_files" or r_list.get("status") != "ok":
        problems.append(
            f"call 2 (list workspace) recorded {r_list.get('status')!r} — the allowed listing must succeed"
        )
    if r_escape.get("status") != "denied" or "hook" not in str(r_escape.get("reason", "")):
        problems.append(
            f"call 3 (the ../../etc/passwd escape) recorded status={r_escape.get('status')!r} "
            f"reason={r_escape.get('reason')!r} — the hook must deny it (reason: blocked by hook)"
        )
    if r_bash.get("status") != "denied" or "registry" not in str(r_bash.get("reason", "")):
        problems.append(
            f"call 4 (run_bash) recorded status={r_bash.get('status')!r} "
            f"reason={r_bash.get('reason')!r} — run_bash must not be in the registry (reason: not in registry)"
        )


def main() -> None:
    problems: list[str] = []
    scan_blanks(problems)
    if not problems:
        check_structure(problems)
    if not problems:
        try:
            if check_definitions(problems):
                check_session(problems)
        finally:
            TRANSCRIPT.unlink(missing_ok=True)
    if problems:
        print(f"❌ FAIL — {LESSON}")
        for i, p in enumerate(problems, 1):
            print(f"  {i}. {p}")
        sys.exit(1)
    print(f"✅ PASS — {LESSON}")
    sys.exit(0)


if __name__ == "__main__":
    main()

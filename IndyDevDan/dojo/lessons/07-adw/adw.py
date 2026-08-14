#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""adw.py — an AFK Developer Workflow: deterministic code chaining agentic prompts.

plan → build → validate → (resolve once, re-validate) → report

TAC-4: an ADW is "a reusable agentic workflow that combines code, agentic prompts,
and agents to deliver results autonomously." The deterministic Python you are
standing in IS the workflow; the non-deterministic agents live behind run_agent().
"In the future these will just be known as scripts."

Usage:  DOJO_MOCK=1 python3 adw.py "add greeting"
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMPTS = HERE / "prompts"
MOCK_OUTPUTS = HERE / "mock_outputs"
LOG = HERE / "adw_log.jsonl"


def run_agent(prompt_path: Path, args: str = "") -> str:
    """One agent, one prompt, one purpose. Returns the agent's report text.

    DOJO_MOCK=1 short-circuits to canned output in mock_outputs/ — the dojo's
    checks never call an LLM. Live mode shells out to `claude -p` (see the
    README's Run It Live section).
    """
    if os.environ.get("DOJO_MOCK") == "1":
        out = (MOCK_OUTPUTS / f"{prompt_path.stem}.txt").read_text(encoding="utf-8")
    else:  # live mode — optional, never exercised by check.py
        prompt = prompt_path.read_text(encoding="utf-8") + (f"\n\n{args}" if args else "")
        proc = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True)
        out = proc.stdout
    print(f"[{prompt_path.stem}] {out.strip().splitlines()[0]}")
    return out


def parse_plan_path(plan_report: str) -> str:
    """The planner's report ends with 'PLAN_PATH: <path>' — stdout is a leverage point."""
    for line in plan_report.splitlines():
        if line.startswith("PLAN_PATH:"):
            return line.split(":", 1)[1].strip()
    return ""


def validate() -> bool:
    """Close the loop: the tests are the rule of law in this codebase."""
    # YOUR TURN: run the unit test suite as a subprocess —
    #   python3 -m unittest discover tests
    # The blank is the discover start directory (the tests live in tests/).
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "____"],
        cwd=HERE,
        capture_output=True,
        text=True,
    )
    tail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "no output"
    print(f"[validate] {tail}")
    # YOUR TURN: a validation gate is binary — return True only when the suite
    # passed (the subprocess exited with returncode 0).
    return ____


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('usage: DOJO_MOCK=1 python3 adw.py "<task>"')
    task = sys.argv[1]
    steps: list[str] = []

    # -- plan -----------------------------------------------------------------
    # YOUR TURN: the chain starts with the planner. Run the plan prompt with the
    # task as its argument. (Which file in prompts/ writes the plan?)
    plan_report = run_agent(PROMPTS / "____", task)
    steps.append("plan")

    # -- build (the HOP move) -------------------------------------------------
    # YOUR TURN: the higher-order-prompt move — the plan is the prompt. The plan
    # path was parsed from the planner's report below; pass it into the build
    # prompt as its argument. Prompts passed into prompts, like functions into
    # functions.
    plan_path = parse_plan_path(plan_report)
    run_agent(PROMPTS / "build.md", ____)
    steps.append("build")

    # -- validate ---------------------------------------------------------------
    ok = validate()
    steps.append("validate")

    # -- resolve gate -------------------------------------------------------------
    if not ok:
        # YOUR TURN: one shot at self-correction — run the resolve prompt exactly
        # once with the task, record the step honestly, then re-validate below.
        # No infinite loops: one resolve, one re-check, then report the truth.
        run_agent(PROMPTS / "____", task)
        steps.append("____")
        ok = validate()
        steps.append("validate")

    # -- report -----------------------------------------------------------------
    # YOUR TURN: every artifact reports what it did. Append exactly ONE line of
    # JSON to adw_log.jsonl with exactly these keys:
    #   {"task": <the task>, "steps": <the steps list>, "ok": <final validation>}
    # (json.dumps the dict, then add a newline.)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(____)

    print(f"[adw] task={task!r} ok={ok} steps={steps}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

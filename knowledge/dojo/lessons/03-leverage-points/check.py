#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 03 · leverage-points.

Deterministic, offline, stdlib-only. Runs the learner's CLI in a temp copy and
reads its stdout — exactly the way an agent would — then AST-parses signatures.
"""
from __future__ import annotations

import ast
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
NN, SLUG = "03", "leverage-points"
TASKS = HERE / "sample_app" / "tasks.py"
TYPED_FUNCS = ("add_task", "list_tasks", "complete_task")
TASK_TEXT = "water the bonsai"


def finish(fails: list[str]) -> None:
    if fails:
        print(f"❌ FAIL — {NN} {SLUG}")
        for i, msg in enumerate(fails, 1):
            print(f"  {i}. {msg}")
        sys.exit(1)
    print(f"✅ PASS — {NN} {SLUG}")
    sys.exit(0)


def main() -> None:
    fails: list[str] = []

    if not TASKS.exists():
        finish([f"sample_app/tasks.py is missing — restore the starter: python3 ../../dojo.py reset {NN}"])

    # Step zero: every ____ must be filled before the real checks run.
    src = TASKS.read_text(encoding="utf-8")
    count = src.count("____")
    if count:
        finish([
            f"fill every ____ first — sample_app/tasks.py: {count} blank(s) "
            "(3 stdout sites, 3 type-hint sites)"
        ])

    # Types are IDKs: AST-check the marked signatures.
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        finish([f"sample_app/tasks.py: syntax error at line {exc.lineno}: {exc.msg}"])

    funcs = {node.name: node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    for name in TYPED_FUNCS:
        fn = funcs.get(name)
        if fn is None:
            fails.append(
                f"tasks.py: function {name}() vanished — keep the original functions, "
                "just open the leverage points"
            )
            continue
        missing = [a.arg for a in fn.args.args if a.annotation is None]
        if missing:
            fails.append(
                f"tasks.py: {name}() parameters missing type hints: {', '.join(missing)} — "
                "types are IDKs; they tell the story of what flows in"
            )
        if fn.returns is None:
            fails.append(
                f"tasks.py: {name}() has no return type hint — annotate what flows out "
                "(-> dict, -> None, -> dict | None)"
            )

    # Stdout is a top leverage point: run the CLI in a temp copy and watch it.
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        shutil.copy2(TASKS, tmp / "tasks.py")

        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, "tasks.py", *args],
                cwd=tmp, capture_output=True, text=True, timeout=30,
            )

        r_add = run("add", TASK_TEXT)
        r_list = run("list")
        r_done = run("done", "1")

    for label, proc in (("add", r_add), ("list", r_list), ("done 1", r_done)):
        if proc.returncode != 0:
            detail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "non-zero exit"
            fails.append(f"tasks.py {label}: crashed — {detail}")

    def got(proc: subprocess.CompletedProcess[str]) -> str:
        return proc.stdout.strip()[:60] or "silence"

    if r_add.returncode == 0 and not (TASK_TEXT in r_add.stdout and re.search(r"add", r_add.stdout, re.I)):
        fails.append(
            "tasks.py add: stdout must confirm the action and name the task — "
            f"e.g. `added #1: {TASK_TEXT}` (got: {got(r_add)})"
        )
    if r_list.returncode == 0 and not (TASK_TEXT in r_list.stdout and "1" in r_list.stdout):
        fails.append(
            "tasks.py list: stdout must print every task with its id and text — "
            f"e.g. `#1 [open] {TASK_TEXT}` (got: {got(r_list)})"
        )
    if r_done.returncode == 0 and not (re.search(r"done", r_done.stdout, re.I) and "1" in r_done.stdout):
        fails.append(
            "tasks.py done 1: stdout must confirm the completion with the id — "
            f"e.g. `done #1: {TASK_TEXT}` (got: {got(r_done)})"
        )

    finish(fails)


if __name__ == "__main__":
    main()

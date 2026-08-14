#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""The Agentic Dojo runner — play, check, hint, diff, reset.

Usage:
  python3 dojo.py status            show every lesson and your progress
  python3 dojo.py next              show the first lesson you haven't passed
  python3 dojo.py check <NN|all>    run a lesson's closed-loop validator
  python3 dojo.py hint <NN> [k]     reveal hint k (default: the next one you haven't seen)
  python3 dojo.py diff <NN>         diff your files against the reference solution
  python3 dojo.py reset <NN>        restore a lesson's starter files (your edits are lost)

Everything is deterministic and offline. The checks never call an LLM —
they are the closed loop you are training yourself to always build.
"""
from __future__ import annotations

import difflib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LESSONS = ROOT / "lessons"
PROGRESS = ROOT / "progress.jsonl"
PRISTINE = ROOT / ".dojo" / "pristine"

GREEN, RED, YELLOW, DIM, BOLD, END = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[1m", "\033[0m"


def lessons() -> list[Path]:
    return sorted(p for p in LESSONS.iterdir() if p.is_dir() and re.match(r"^\d{2}-", p.name))


def find(nn: str) -> Path:
    nn = nn.zfill(2)
    hits = [p for p in lessons() if p.name.startswith(nn + "-")]
    if not hits:
        sys.exit(f"{RED}no lesson {nn!r} — run: python3 dojo.py status{END}")
    return hits[0]


def log_event(event: dict) -> None:
    event["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with PROGRESS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def history() -> list[dict]:
    if not PROGRESS.exists():
        return []
    return [json.loads(line) for line in PROGRESS.read_text(encoding="utf-8").splitlines() if line.strip()]


def last_result(name: str) -> dict | None:
    for event in reversed(history()):
        if event.get("lesson") == name and event.get("kind") == "check":
            return event
    return None


def hints_seen(name: str) -> int:
    return max((e.get("k", 0) for e in history() if e.get("lesson") == name and e.get("kind") == "hint"), default=0)


def blanks_left(lesson: Path) -> int:
    count = 0
    for p in lesson.rglob("*"):
        if p.is_file() and "solution" not in p.parts and p.name not in ("check.py", "hints.md", "README.md"):
            try:
                count += p.read_text(encoding="utf-8").count("____")
            except (UnicodeDecodeError, OSError):
                pass
    return count


def run_check(lesson: Path) -> bool:
    checker = lesson / "check.py"
    if not checker.exists():
        print(f"{RED}{lesson.name}: no check.py{END}")
        return False
    proc = subprocess.run([sys.executable, str(checker)], cwd=lesson, capture_output=True, text=True, timeout=120)
    out = (proc.stdout + proc.stderr).strip()
    print(out)
    passed = proc.returncode == 0
    log_event({"kind": "check", "lesson": lesson.name, "pass": passed})
    return passed


def cmd_status() -> None:
    print(f"\n{BOLD}The Agentic Dojo{END} {DIM}· fill the blanks · close the loop · climb{END}\n")
    for p in lessons():
        res = last_result(p.name)
        blanks = blanks_left(p)
        if res and res["pass"]:
            mark, note = f"{GREEN}✅ passed{END}", ""
        elif res:
            mark, note = f"{RED}❌ failing{END}", f"{DIM} · {blanks} blank(s) left{END}" if blanks else ""
        else:
            mark, note = f"{YELLOW}· not attempted{END}", f"{DIM} · {blanks} blank(s){END}" if blanks else ""
        print(f"  {p.name:<26} {mark}{note}")
    passed = sum(1 for p in lessons() if (r := last_result(p.name)) and r["pass"])
    print(f"\n  {BOLD}{passed}/{len(lessons())}{END} lessons passed", end="")
    nxt = _next()
    print(f" · next up: {BOLD}{nxt.name}{END}\n" if nxt else f" · {GREEN}the dojo is complete. go build your own layer.{END}\n")


def _next() -> Path | None:
    for p in lessons():
        res = last_result(p.name)
        if not (res and res["pass"]):
            return p
    return None


def cmd_next() -> None:
    nxt = _next()
    if not nxt:
        print(f"{GREEN}all lessons passed — the dojo is complete.{END}")
        return
    print(f"{BOLD}next up: {nxt.name}{END}\n")
    readme = nxt / "README.md"
    if readme.exists():
        print("\n".join(readme.read_text(encoding="utf-8").splitlines()[:8]))
        print(f"\n{DIM}full brief: {readme}{END}")


def cmd_check(target: str) -> None:
    targets = lessons() if target == "all" else [find(target)]
    results = [run_check(p) for p in targets]
    if len(targets) > 1:
        print(f"\n{BOLD}{sum(results)}/{len(results)} passing{END}")
    sys.exit(0 if all(results) else 1)


def cmd_hint(nn: str, k: str | None) -> None:
    lesson = find(nn)
    text = (lesson / "hints.md").read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)
    hints = ["## " + p for p in parts if p.strip() and p.lstrip().lower().startswith("hint")]
    idx = int(k) if k else min(hints_seen(lesson.name) + 1, len(hints))
    if not 1 <= idx <= len(hints):
        sys.exit(f"{RED}hints go 1..{len(hints)}{END}")
    print(f"{YELLOW}{hints[idx - 1].strip()}{END}\n{DIM}({idx}/{len(hints)} — hints cost you nothing but glory){END}")
    log_event({"kind": "hint", "lesson": lesson.name, "k": idx})


def cmd_diff(nn: str) -> None:
    lesson = find(nn)
    sol = lesson / "solution"
    shown = False
    for spath in sorted(p for p in sol.rglob("*") if p.is_file()):
        rel = spath.relative_to(sol)
        yours = lesson / rel
        a = yours.read_text(encoding="utf-8").splitlines(keepends=True) if yours.exists() else []
        b = spath.read_text(encoding="utf-8").splitlines(keepends=True)
        diff = list(difflib.unified_diff(a, b, fromfile=f"yours/{rel}", tofile=f"solution/{rel}"))
        if diff:
            shown = True
            for line in diff:
                color = GREEN if line.startswith("+") else RED if line.startswith("-") else DIM
                print(color + line.rstrip("\n") + END)
    if not shown:
        print(f"{GREEN}your files match the reference solution.{END}")


def cmd_reset(nn: str) -> None:
    lesson = find(nn)
    src = PRISTINE / lesson.name
    if not src.exists():
        sys.exit(f"{RED}no pristine snapshot for {lesson.name}{END}")
    for spath in src.rglob("*"):
        if spath.is_file():
            dest = lesson / spath.relative_to(src)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(spath, dest)
    log_event({"kind": "reset", "lesson": lesson.name})
    print(f"{YELLOW}{lesson.name} restored to its starter state.{END}")


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args else "status"
    if cmd == "status":
        cmd_status()
    elif cmd == "next":
        cmd_next()
    elif cmd == "check" and len(args) >= 2:
        cmd_check(args[1])
    elif cmd == "hint" and len(args) >= 2:
        cmd_hint(args[1], args[2] if len(args) > 2 else None)
    elif cmd == "diff" and len(args) >= 2:
        cmd_diff(args[1])
    elif cmd == "reset" and len(args) >= 2:
        cmd_reset(args[1])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()

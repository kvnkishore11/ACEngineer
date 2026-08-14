#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 10 o-agent. Deterministic, offline, stdlib only.

Drives the orchestrator through the full CRUD sequence against a real worker
process: create alpha -> command alpha -> status -> delete alpha. Every step
is bounded by timeouts and fleet/ is cleaned before and after, so reruns are
deterministic and nothing ever hangs.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LESSON = "10 o-agent"
OAGENT = HERE / "oagent.py"
FLEET = HERE / "fleet"


def scan_blanks() -> list[str]:
    """Step zero: no ____ may remain in the starter files."""
    problems = []
    for p in sorted(HERE.rglob("*")):
        if not p.is_file() or "solution" in p.parts or "__pycache__" in p.parts:
            continue
        if p.name in ("check.py", "hints.md", "README.md"):
            continue
        try:
            n = p.read_text(encoding="utf-8").count("____")
        except (UnicodeDecodeError, OSError):
            continue
        if n:
            problems.append(f"{p.relative_to(HERE)} still has {n} blank(s) — fill every ____ (see the YOUR TURN comments)")
    return problems


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def cleanup() -> None:
    """Kill any workers recorded in manifests, then remove fleet/."""
    if not FLEET.exists():
        return
    for manifest in FLEET.glob("*/manifest.json"):
        try:
            pid = json.loads(manifest.read_text(encoding="utf-8")).get("pid")
            if isinstance(pid, int):
                os.kill(pid, signal.SIGTERM)
        except (OSError, ValueError):
            pass
    shutil.rmtree(FLEET, ignore_errors=True)


def oagent(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(OAGENT), *args],
        cwd=HERE, capture_output=True, text=True, timeout=15,
        stdin=subprocess.DEVNULL,
    )


def tail_of(proc: subprocess.CompletedProcess) -> str:
    out = (proc.stderr or proc.stdout or "").strip()
    return out.splitlines()[-1] if out else "no output"


def validate() -> list[str]:
    fails: list[str] = []

    # 1. CREATE
    try:
        proc = oagent("create", "alpha", "summarize the fleet")
    except subprocess.TimeoutExpired:
        return ["oagent.py create hung — in create_agent, detach the worker's "
                "stdin/stdout/stderr with subprocess.DEVNULL or callers block on its pipes forever"]
    if proc.returncode != 0:
        return [f"`oagent.py create alpha <purpose>` exited {proc.returncode}: {tail_of(proc)}"]
    manifest_path = FLEET / "alpha" / "manifest.json"
    if not manifest_path.exists():
        return ["create_agent must write fleet/alpha/manifest.json — every agent must have a purpose (and a pid) on record"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except ValueError:
        return ["fleet/alpha/manifest.json is not valid JSON — write it with json.dumps"]
    for key in ("name", "purpose", "pid"):
        if key not in manifest:
            fails.append(f"manifest.json is missing the {key!r} key — the manifest is {{name, purpose, pid}}")
    if fails:
        return fails
    if not str(manifest["purpose"]).strip():
        fails.append("manifest purpose is empty — every agent must have a purpose")
    pid = manifest["pid"]
    if not isinstance(pid, int) or not pid_alive(pid):
        fails.append("manifest pid is not a live process — create_agent must subprocess.Popen worker.py and record proc.pid")
        return fails

    # 2. COMMAND — the status trail must gain events
    trail = FLEET / "alpha" / "status.jsonl"
    before = len(trail.read_text(encoding="utf-8").splitlines()) if trail.exists() else 0
    try:
        proc = oagent("command", "alpha", "do work")
    except subprocess.TimeoutExpired:
        return ["oagent.py command hung — command_agent should only write the inbox file and return"]
    if proc.returncode != 0:
        return [f"`oagent.py command alpha \"do work\"` exited {proc.returncode}: {tail_of(proc)}"]
    events: list[dict] = []
    deadline = time.time() + 5
    while time.time() < deadline:
        if trail.exists():
            try:
                events = [json.loads(l) for l in trail.read_text(encoding="utf-8").splitlines() if l.strip()]
            except ValueError:
                events = []
            if len(events) >= before + 2 and any("do work" in str(e.get("detail", "")) for e in events):
                break
        time.sleep(0.05)
    else:
        fails.append("after `command alpha \"do work\"`, fleet/alpha/status.jsonl never gained work events — "
                     "command_agent must write the text to fleet/alpha/inbox.txt (the worker polls it)")

    # 3. STATUS — one-line summary per agent (observability pillar)
    try:
        proc = oagent("status")
    except subprocess.TimeoutExpired:
        return ["oagent.py status hung — status only reads files, it should never wait"]
    if proc.returncode != 0:
        fails.append(f"`oagent.py status` exited {proc.returncode}: {tail_of(proc)}")
    elif not any(line.strip().startswith("alpha") for line in proc.stdout.splitlines()):
        fails.append("`oagent.py status` must print a one-line summary per agent — expected a line starting "
                     "with 'alpha' built from the LAST status.jsonl event (read the tail, not the full log)")

    # 4. DELETE — process gone, directory gone
    try:
        proc = oagent("delete", "alpha")
    except subprocess.TimeoutExpired:
        return ["oagent.py delete hung — poll pid_alive for ~2s max, then SIGTERM; deletable means deletable"]
    if proc.returncode != 0:
        fails.append(f"`oagent.py delete alpha` exited {proc.returncode}: {tail_of(proc)}")
        return fails
    deadline = time.time() + 3
    while time.time() < deadline and pid_alive(pid):
        time.sleep(0.05)
    if pid_alive(pid):
        fails.append("worker process is still alive after delete — write 'shutdown' to the inbox, wait, then os.kill SIGTERM")
    if (FLEET / "alpha").exists():
        fails.append("fleet/alpha still exists after delete — agents are deletable resources: shutil.rmtree the directory")
    return fails


def main() -> None:
    cleanup()  # deterministic reruns: start from an empty fleet
    fails = scan_blanks()
    if not fails:
        try:
            fails = validate()
        finally:
            cleanup()
    if fails:
        print(f"❌ FAIL — {LESSON}")
        for i, f in enumerate(fails, 1):
            print(f"  {i}. {f}")
        sys.exit(1)
    print(f"✅ PASS — {LESSON}")
    sys.exit(0)


if __name__ == "__main__":
    main()

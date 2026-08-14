#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""oagent.py — the Orchestrator Agent (O-Agent): one interface, many agents.

Usage:
  python3 oagent.py create <name> <purpose...>   spawn a worker + write its manifest
  python3 oagent.py command <name> <text...>     hand the agent work via its inbox
  python3 oagent.py status [name]                one-line summary per agent
  python3 oagent.py delete <name>                shut down, terminate, remove

The orchestrator never does the work itself — it creates, commands, observes,
and deletes. The fleet/ directory is the whole registry: each agent owns
fleet/<name>/ with a manifest.json, an inbox.txt, and a status.jsonl trail.
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

ROOT = Path(__file__).resolve().parent
FLEET = ROOT / "fleet"
WORKER = ROOT / "worker.py"


def fleet_dir(name: str) -> Path:
    return FLEET / name


def pid_alive(pid: int) -> bool:
    """True if a process with this pid is still running."""
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def create_agent(name: str, purpose: str) -> None:
    """CREATE — pillar two, the C in CRUD for your agents."""
    home = fleet_dir(name)
    home.mkdir(parents=True, exist_ok=True)
    # Spawn worker.py as a detached background process. DEVNULL on every
    # stream — if the worker inherits your pipes, everything upstream hangs.
    proc = subprocess.Popen(
        [sys.executable, str(WORKER), name],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Every agent must have a purpose. Register it in the manifest so the
    # fleet is inspectable at rest.
    (home / "manifest.json").write_text(
        json.dumps({"name": name, "purpose": purpose, "pid": proc.pid}, indent=2),
        encoding="utf-8",
    )
    print(f"created {name} (pid {proc.pid}) — purpose: {purpose}")


def command_agent(name: str, text: str) -> None:
    """COMMAND — the orchestrator writes prompts, the worker does the work."""
    home = fleet_dir(name)
    if not home.exists():
        sys.exit(f"no agent named {name!r} — create it first")
    # The whole command channel is one file. The worker polls it.
    (home / "inbox.txt").write_text(text, encoding="utf-8")
    print(f"commanded {name}: {text}")


def status(name: str | None = None) -> None:
    """STATUS — pillar three, observability. If you can't measure it, you can't scale it."""
    if not FLEET.exists() or not any(FLEET.iterdir()):
        print("fleet is empty")
        return
    names = [name] if name else sorted(p.name for p in FLEET.iterdir() if p.is_dir())
    for n in names:
        trail = fleet_dir(n) / "status.jsonl"
        if not trail.exists():
            print(f"{n}: no status trail yet")
            continue
        # Read the tail, not the full log — protect your own context window.
        last = json.loads(trail.read_text(encoding="utf-8").splitlines()[-1])
        print(f"{n}: {last['event']} — {last['detail']}")


def delete_agent(name: str) -> None:
    """DELETE — agents are deletable resources. Force focus, then let it go."""
    home = fleet_dir(name)
    if not home.exists():
        sys.exit(f"no agent named {name!r}")
    manifest = json.loads((home / "manifest.json").read_text(encoding="utf-8"))
    pid = manifest["pid"]
    # Ask nicely first: the shutdown command lets the worker log its exit.
    (home / "inbox.txt").write_text("shutdown", encoding="utf-8")
    deadline = time.time() + 2
    while time.time() < deadline and pid_alive(pid):
        time.sleep(0.05)
    if pid_alive(pid):  # still up? deletable means deletable.
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.1)
    # The best code is no code; you learn to delete.
    shutil.rmtree(home)
    print(f"deleted {name} — back to the data center")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd, rest = args[0], args[1:]
    if cmd == "create" and len(rest) >= 2:
        create_agent(rest[0], " ".join(rest[1:]))
    elif cmd == "command" and len(rest) >= 2:
        command_agent(rest[0], " ".join(rest[1:]))
    elif cmd == "status":
        status(rest[0] if rest else None)
    elif cmd == "delete" and len(rest) == 1:
        delete_agent(rest[0])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()

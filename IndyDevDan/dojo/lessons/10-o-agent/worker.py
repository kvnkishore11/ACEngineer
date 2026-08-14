#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""worker.py — a toy background agent. THIS FILE IS COMPLETE — read it, don't edit it.

Usage: python3 worker.py <name>

The worker is the thing your orchestrator manages. It:
  - polls fleet/<name>/inbox.txt for a command (the command channel),
  - "does work" (sleeps briefly, appends a line to fleet/<name>/result.txt —
    every agent should produce a concrete result),
  - appends every state change to fleet/<name>/status.jsonl (the observability
    trail the orchestrator reads),
  - exits on the command "shutdown" — and self-terminates after 30 seconds
    regardless, because no agent should live forever.

Adopt your agent's perspective: everything oagent.py does only makes sense
once you know how this loop reads its world.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POLL_SECONDS = 0.05
LIFETIME_SECONDS = 30  # a worker is a temporary resource, never a daemon


def log_status(name: str, event: str, detail: str = "") -> None:
    """Append one event to the agent's status trail. Observability is pillar three."""
    home = ROOT / "fleet" / name
    home.mkdir(parents=True, exist_ok=True)
    with (home / "status.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"agent": name, "event": event, "detail": detail, "ts": time.time()}) + "\n")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python3 worker.py <name>")
    name = sys.argv[1]
    home = ROOT / "fleet" / name
    inbox = home / "inbox.txt"
    log_status(name, "idle", "waiting for a command")

    deadline = time.time() + LIFETIME_SECONDS
    while time.time() < deadline:
        if inbox.exists():
            command = inbox.read_text(encoding="utf-8").strip()
            if command:
                inbox.write_text("", encoding="utf-8")  # consume the command
                if command == "shutdown":
                    log_status(name, "shutdown", "going home to the data center")
                    return
                log_status(name, "working", command)
                time.sleep(0.1)  # the "work"
                with (home / "result.txt").open("a", encoding="utf-8") as f:
                    f.write(f"did: {command}\n")
                log_status(name, "idle", f"finished: {command}")
        time.sleep(POLL_SECONDS)

    log_status(name, "shutdown", "lifetime expired — no agent lives forever")


if __name__ == "__main__":
    main()

# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27"]
# ///
"""Run the Pi coding agent benchmark for a specific hardware platform.

Thin wrapper around bench.py — pass --hw m4 or --hw m5.

Usage:
    uv run run_all.py --hw m4                # full run on M4 Max
    uv run run_all.py --hw m5 --smoke        # quick validation on M5 Max
    uv run run_all.py --hw m4 --reset        # wipe session then run
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent
SESSION = "pi-coding-agent-3way"


def main() -> int:
    ap = argparse.ArgumentParser(description="Run pi-coding-agent-3way benchmark")
    ap.add_argument("--hw", required=True, choices=["m4", "m5"],
                    help="Hardware tag (m4 or m5)")
    ap.add_argument("--smoke", action="store_true",
                    help="Quick validation: T1 only, first model only")
    ap.add_argument("--server", default=os.environ.get("LIVE_BENCH_SERVER", "http://127.0.0.1:8787"),
                    help="live-bench server URL (env: LIVE_BENCH_SERVER)")
    ap.add_argument("--reset", action="store_true",
                    help="Reset the session before running")
    args = ap.parse_args()

    if args.reset:
        print(f"Resetting session {SESSION}...", file=sys.stderr)
        subprocess.run(
            ["live-bench", "--server", args.server, "reset", SESSION, "--yes"],
            check=True,
        )

    cmd = ["uv", "run", str(BENCH_DIR / "bench.py"),
           "--hw", args.hw, "--server", args.server]
    if args.smoke:
        cmd.append("--smoke")

    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    sys.exit(main())

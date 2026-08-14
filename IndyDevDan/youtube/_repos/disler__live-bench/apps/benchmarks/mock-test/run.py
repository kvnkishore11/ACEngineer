# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Mock benchmark — emits fake data + metadata for quick UI testing.

No models needed. Runs in ~2 seconds. Emits 2 groups x 2 metrics with
prompt text and response text so you can test the metadata modal.

Usage:
    uv run apps/benchmarks/mock-test/run.py
    uv run apps/benchmarks/mock-test/run.py --server http://192.168.1.42:8787
"""

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time

SESSION = "mock-test"
CHART = "speed"

GROUPS = [
    {
        "key": "q1",
        "prompt": "Say hello in a creative way.",
        "responses": {
            "model_a": {
                "text": "Greetings, fellow traveler of the digital realm! May your bits be ever in order and your packets never lost in transit. Welcome to this magnificent day of computation!",
                "speed": 342.5,
            },
            "model_b": {
                "text": "Hey there! Imagine I'm a friendly robot waving at you with my shiny metallic arm. Beep boop, hello human! Ready to explore the wonders of technology together?",
                "speed": 487.2,
            },
        },
    },
    {
        "key": "q2",
        "prompt": "Write a Python function to reverse a string.",
        "responses": {
            "model_a": {
                "text": "def reverse_string(s: str) -> str:\n    \"\"\"Reverse a string using slicing.\"\"\"\n    return s[::-1]\n\n# Example\nprint(reverse_string('hello'))  # 'olleh'",
                "speed": 298.1,
            },
            "model_b": {
                "text": "def reverse_string(s: str) -> str:\n    \"\"\"Reverse a string character by character.\"\"\"\n    result = []\n    for char in s:\n        result.insert(0, char)\n    return ''.join(result)\n\n# Usage\nassert reverse_string('hello') == 'olleh'",
                "speed": 412.8,
            },
        },
    },
]


def sample_speed(base: float) -> float:
    """Return a slightly jittered speed so each mock run looks fresh."""
    return round(base * random.uniform(0.88, 1.12), 1)


def emit(group: str, metric: str, value: float, server: str) -> None:
    subprocess.run(
        ["live-bench", "--server", server, "emit", SESSION,
         "--chart", CHART, "--group", group,
         "--metric", metric, "--value", str(round(value, 1))],
        check=True,
    )


def meta(group: str, data: dict, server: str) -> None:
    subprocess.run(
        ["live-bench", "--server", server, "meta", SESSION,
         "--chart", CHART, "--group", group,
         "--json", json.dumps(data)],
        check=True,
    )


def complete(group: str, server: str) -> None:
    subprocess.run(
        ["live-bench", "--server", server, "complete", SESSION,
         "--chart", CHART, "--group", group],
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Mock benchmark — fake data for UI testing")
    ap.add_argument("--server", default=os.environ.get("LIVE_BENCH_SERVER", "http://127.0.0.1:8787"))
    ap.add_argument("--reset", action="store_true", help="Reset session first")
    args = ap.parse_args()

    if args.reset:
        subprocess.run(
            ["live-bench", "--server", args.server, "reset", SESSION, "--yes"],
            check=True,
        )

    host = args.server.split("//")[1].split(":")[0]
    frontend_port = os.environ.get("LB_FRONTEND_PORT", "5787")
    print(f"\n  Open: http://{host}:{frontend_port}/benchmark/{SESSION}", file=sys.stderr)
    print(f"  Starting in 8 seconds...", file=sys.stderr)
    time.sleep(8)

    print("Running mock benchmark...", file=sys.stderr)

    for g in GROUPS:
        print(f"\n  {g['key']}: {g['prompt'][:40]}...", file=sys.stderr)

        for metric_key, r in g["responses"].items():
            # Emit a randomized numeric value around the fixture baseline.
            value = sample_speed(r["speed"])
            emit(g["key"], metric_key, value, args.server)
            print(f"    {metric_key}: {value} tok/s", file=sys.stderr)

            # Emit metadata (prompt + this model's response)
            meta(g["key"], {
                "prompt": g["prompt"],
                "responses": {metric_key: r["text"]},
            }, args.server)

            time.sleep(1.5)  # delay so bar animations are visible

        # All metrics done for this group — mark complete
        complete(g["key"], args.server)
        print(f"  ✓ {g['key']} complete", file=sys.stderr)

    print("\nMock benchmark done!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

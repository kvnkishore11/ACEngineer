"""Synthetic data emitter for `just demo-stream`.

Usage::

    python -m live_bench_cli.dev.fake_stream <session_id>
    python -m live_bench_cli.dev.fake_stream <session_id> --server http://127.0.0.1:8787

Discovers the session's (group, metric) cells via ``GET /benchmarks/<id>``
and emits one random-walk point every 200 ms for 60 seconds per cell.
Then marks every group complete. Routes through ``LiveBenchClient`` so
this script exercises the same ingest path as the real CLI.
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time

from .. import client as client_module
from ..client import LiveBenchClient, LiveBenchError
from ..models import DataPoint, IngestRequest


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog="fake_stream")
    ap.add_argument("session_id", help="Target benchmark session id")
    ap.add_argument(
        "--server",
        default=os.environ.get("LIVE_BENCH_SERVER", "http://127.0.0.1:8787"),
        help="Backend base URL",
    )
    ap.add_argument(
        "--duration-s",
        type=float,
        default=60.0,
        help="How many seconds to run for before marking complete",
    )
    ap.add_argument(
        "--interval-s",
        type=float,
        default=0.2,
        help="Emit interval per cell",
    )
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    session_id = args.session_id

    with LiveBenchClient(args.server) as client:
        try:
            data = client.get_benchmark(session_id)
        except LiveBenchError as exc:
            print(f"fake_stream: failed to fetch benchmark: {exc}", file=sys.stderr)
            return 1

        config = data.get("config", {}) or {}
        groups = [g.get("key") for g in (config.get("groups") or []) if g.get("key")]
        metrics = [m.get("key") for m in (config.get("metrics") or []) if m.get("key")]
        if not groups or not metrics:
            print(
                "fake_stream: config has no groups/metrics to emit for",
                file=sys.stderr,
            )
            return 1

        # Per-cell random-walk state.
        baselines: dict[tuple[str, str], float] = {}
        for g in groups:
            for m in metrics:
                baselines[(g, m)] = random.uniform(50.0, 500.0)

        deadline = time.monotonic() + args.duration_s
        tick = 0
        print(
            f"fake_stream: emitting to {session_id} "
            f"({len(groups)} groups × {len(metrics)} metrics) "
            f"for {args.duration_s:.0f}s",
            file=sys.stderr,
        )

        while time.monotonic() < deadline:
            points: list[DataPoint] = []
            for g in groups:
                for m in metrics:
                    baseline = baselines[(g, m)]
                    # Random walk with clamping to keep it visible.
                    baseline = max(1.0, baseline + random.uniform(-baseline * 0.05, baseline * 0.05))
                    baselines[(g, m)] = baseline
                    points.append(
                        DataPoint(
                            group_key=g,
                            metric_key=m,
                            value=round(baseline, 3),
                            client_ts=client_module.now_ts(),
                        )
                    )
            req = IngestRequest(
                session_id=session_id,
                request_ts=client_module.now_ts(),
                points=points,
            )
            try:
                client.ingest(req)
            except LiveBenchError as exc:
                print(f"fake_stream: ingest error (continuing): {exc}", file=sys.stderr)
            tick += 1
            time.sleep(args.interval_s)

        # Mark all groups complete.
        complete_req = IngestRequest(
            session_id=session_id,
            request_ts=client_module.now_ts(),
            points=[],
            complete_groups=list(groups),
        )
        try:
            client.ingest(complete_req)
        except LiveBenchError as exc:
            print(f"fake_stream: complete error: {exc}", file=sys.stderr)
            return 1

        print(f"fake_stream: done ({tick} ticks)", file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

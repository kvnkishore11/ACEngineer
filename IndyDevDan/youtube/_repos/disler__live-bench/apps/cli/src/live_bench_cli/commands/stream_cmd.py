"""`live-bench stream <session_id>` — persistent stdin → batched POSTs.

The canonical usage is::

    python my_bench.py | live-bench stream gemma4-e4b-prefill-2026-04-07

The reader consumes stdin **line by line**, stamping each point's
``client_ts`` at read time (spec §15). Points are buffered and flushed
every ``--flush-ms`` milliseconds or when the buffer reaches
``--max-batch`` points, whichever comes first. Control lines of the form
``{"complete": "<group_key>"}`` are routed into ``complete_groups`` of
the next batch. One ``LiveBenchClient`` is held for the full lifetime of
the command.
"""

from __future__ import annotations

import json
import queue
import sys
import threading
import time
from typing import TextIO

import click
from rich.console import Console

from .. import client as client_module
from ..client import LiveBenchClient, LiveBenchError
from ..models import CompletionRef, DataPoint, IngestRequest
from .emit_cmd import _build_point_from_line


# Sentinel to signal EOF from the reader thread.
_EOF = object()


def _reader_thread(
    stream: TextIO,
    q: "queue.Queue[object]",
    default_chart: str = "default",
) -> None:
    """Read lines off ``stream`` and push (stamped_point_or_control, ts) tuples.

    The reader stamps ``client_ts`` the moment it pops a line so the time
    reflects user-produced order, not batching delay. Chart id is resolved at
    the same moment: a line's ``chart`` / ``chart_id`` field wins over the
    command-level ``--chart`` flag, which itself defaults to ``"default"``.
    """

    try:
        for raw in stream:
            line = raw.strip()
            if not line:
                continue
            # Stamp immediately for control lines / point lines alike so the
            # batch window cannot reorder them relative to the user's output.
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                q.put(("error", f"invalid JSON: {exc} — line={line!r}"))
                continue
            if isinstance(obj, dict) and "complete" in obj and "value" not in obj:
                # Resolve chart: line-level > --chart flag > "default".
                if "chart_id" in obj and obj["chart_id"]:
                    chart_id = str(obj["chart_id"])
                elif "chart" in obj and obj["chart"]:
                    chart_id = str(obj["chart"])
                else:
                    chart_id = default_chart
                ref = CompletionRef(
                    chart_id=chart_id,
                    group_key=str(obj["complete"]),
                )
                q.put(("complete", ref))
                continue
            try:
                point = _build_point_from_line(line, default_chart=default_chart)
            except Exception as exc:  # noqa: BLE001
                q.put(("error", str(exc)))
                continue
            q.put(("point", point))
    finally:
        q.put(_EOF)


def _flush(
    client: LiveBenchClient,
    session_id: str,
    buffer: list[DataPoint],
    complete_groups: list[CompletionRef],
    console: Console,
) -> tuple[int, int]:
    """Build + POST an ``IngestRequest``; return (points_sent, groups_completed).

    On transport error the failure is logged and counted, but the stream
    keeps running — one bad batch shouldn't nuke a 10-minute run.
    """

    if not buffer and not complete_groups:
        return 0, 0
    req = IngestRequest(
        session_id=session_id,
        request_ts=client_module.now_ts(),
        points=list(buffer),
        complete_groups=list(complete_groups),
    )
    try:
        client.ingest(req)
    except LiveBenchError as exc:
        console.print(f"[red]flush failed:[/red] {exc}")
        return 0, 0
    return len(buffer), len(complete_groups)


@click.command()
@click.argument("session_id")
@click.option("--flush-ms", type=int, default=50, show_default=True, help="Flush interval in ms.")
@click.option("--max-batch", type=int, default=100, show_default=True, help="Max points per batch.")
@click.option(
    "--chart",
    "chart",
    default="default",
    show_default=True,
    help="Default chart id for lines that omit their own (multi-chart benchmarks only).",
)
@click.pass_context
def stream(
    ctx: click.Context,
    session_id: str,
    flush_ms: int,
    max_batch: int,
    chart: str,
) -> None:
    """Read JSONL from stdin and POST batches to /ingest until EOF."""

    console = Console()
    server: str = ctx.obj["server"]

    q: "queue.Queue[object]" = queue.Queue()
    reader = threading.Thread(
        target=_reader_thread,
        args=(sys.stdin, q, chart),
        daemon=True,
    )
    reader.start()

    buffer: list[DataPoint] = []
    pending_complete: list[CompletionRef] = []
    total_points = 0
    total_completes = 0

    flush_interval = max(flush_ms, 0) / 1000.0
    next_flush = time.monotonic() + flush_interval

    with LiveBenchClient(server) as client:
        eof = False
        while not eof:
            timeout = max(0.0, next_flush - time.monotonic())
            try:
                item = q.get(timeout=timeout if timeout > 0 else 0.001)
            except queue.Empty:
                item = None

            if item is _EOF:
                eof = True
            elif item is not None:
                kind, payload = item  # type: ignore[misc]
                if kind == "point":
                    buffer.append(payload)  # type: ignore[arg-type]
                elif kind == "complete":
                    pending_complete.append(payload)  # type: ignore[arg-type]
                elif kind == "error":
                    console.print(f"[yellow]skip:[/yellow] {payload}")

            now = time.monotonic()
            should_flush_time = now >= next_flush
            should_flush_size = len(buffer) >= max_batch

            if should_flush_time or should_flush_size:
                sent_p, sent_c = _flush(
                    client, session_id, buffer, pending_complete, console
                )
                total_points += sent_p
                total_completes += sent_c
                buffer.clear()
                pending_complete.clear()
                next_flush = time.monotonic() + flush_interval

        # Final drain after EOF.
        while True:
            try:
                item = q.get_nowait()
            except queue.Empty:
                break
            if item is _EOF:
                continue
            kind, payload = item  # type: ignore[misc]
            if kind == "point":
                buffer.append(payload)  # type: ignore[arg-type]
            elif kind == "complete":
                pending_complete.append(payload)  # type: ignore[arg-type]
            elif kind == "error":
                console.print(f"[yellow]skip:[/yellow] {payload}")

        sent_p, sent_c = _flush(
            client, session_id, buffer, pending_complete, console
        )
        total_points += sent_p
        total_completes += sent_c

    console.print(
        f"[green]stream done[/green] {session_id} "
        f"points={total_points} complete_groups={total_completes}"
    )

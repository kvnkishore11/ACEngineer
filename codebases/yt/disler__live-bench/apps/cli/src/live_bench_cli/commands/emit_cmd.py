"""`live-bench emit` — single-shot or batch ingest.

Two mutually-exclusive modes:

* Single: ``--group/--metric/--value`` → one ``DataPoint``, ``client_ts``
  stamped immediately at command entry.
* Batch: ``--batch <file|->`` → JSONL stream where each line is read,
  ``client_ts`` stamped (or passed through if the line carries its own),
  and the **whole batch** posted as one ``IngestRequest``.

The "stamp at read time" invariant from spec §15 is critical: if we built
the points in a 20 ms batching window we'd risk reordering relative to the
runner's emit order. Stamping at read time guarantees that ``client_ts``
is monotonic with the order the user produced the data.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Iterable, TextIO

import click
from rich.console import Console

from .. import client as client_module
from ..client import LiveBenchClient, LiveBenchError
from ..models import DataPoint, IngestRequest


def _parse_client_ts(value: str) -> datetime:
    """Parse an ISO-8601 string into an aware UTC ``datetime``.

    Accepts ``Z`` and ``+00:00`` suffixes; naive inputs are assumed UTC.
    """

    s = value.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _build_point_from_line(raw: str, default_chart: str = "default") -> DataPoint:
    """Parse one JSONL line into a ``DataPoint``.

    Stamps ``client_ts = now_ts()`` immediately if the line does not carry
    its own. The stamping happens **at the moment this function is called**
    — i.e. when the line was just read off stdin/file — which is the whole
    point of the read-time invariant.

    ``chart_id`` resolution order:
    1. If the JSONL object carries ``chart_id`` (or legacy ``chart``), use it.
    2. Otherwise use ``default_chart`` (which comes from the ``--chart`` flag,
       itself defaulting to ``"default"``).
    """

    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise click.ClickException(f"batch line must be a JSON object, got: {raw!r}")
    if "client_ts" in obj and obj["client_ts"]:
        client_ts = _parse_client_ts(str(obj["client_ts"]))
    else:
        # CRITICAL: stamp now, before any further work or batching delay.
        client_ts = client_module.now_ts()

    # Resolve chart_id at read time, same invariant as client_ts.
    if "chart_id" in obj and obj["chart_id"]:
        chart_id = str(obj["chart_id"])
    elif "chart" in obj and obj["chart"]:
        chart_id = str(obj["chart"])
    else:
        chart_id = default_chart

    try:
        return DataPoint(
            chart_id=chart_id,
            group_key=obj["group"] if "group" in obj else obj["group_key"],
            metric_key=obj["metric"] if "metric" in obj else obj["metric_key"],
            value=float(obj["value"]),
            client_ts=client_ts,
        )
    except KeyError as exc:
        raise click.ClickException(
            f"batch line missing required field {exc.args[0]!r}: {raw!r}"
        ) from exc


def _iter_batch_points(
    stream: TextIO, default_chart: str = "default"
) -> Iterable[DataPoint]:
    """Yield one ``DataPoint`` per non-empty line, stamped at read time."""

    for raw in stream:
        line = raw.strip()
        if not line:
            continue
        yield _build_point_from_line(line, default_chart=default_chart)


@click.command()
@click.argument("session_id")
@click.option("--group", "group", default=None, help="Group key (single mode).")
@click.option("--metric", "metric", default=None, help="Metric key (single mode).")
@click.option("--value", "value", type=float, default=None, help="Value (single mode).")
@click.option(
    "--batch",
    "batch",
    default=None,
    help="Batch mode: path to a JSONL file, or '-' for stdin.",
)
@click.option(
    "--chart",
    "chart",
    default="default",
    show_default=True,
    help="Chart id inside the benchmark (multi-chart benchmarks only).",
)
@click.pass_context
def emit(
    ctx: click.Context,
    session_id: str,
    group: str | None,
    metric: str | None,
    value: float | None,
    batch: str | None,
    chart: str,
) -> None:
    """Emit one or many datapoints to a session."""

    console = Console()

    single_mode = any(v is not None for v in (group, metric, value))
    batch_mode = batch is not None

    if single_mode and batch_mode:
        raise click.UsageError(
            "--group/--metric/--value and --batch are mutually exclusive"
        )
    if not single_mode and not batch_mode:
        raise click.UsageError(
            "provide either --group/--metric/--value or --batch <file|->"
        )

    points: list[DataPoint] = []

    if single_mode:
        if group is None or metric is None or value is None:
            raise click.UsageError("single mode requires --group, --metric, and --value")
        # CRITICAL: stamp at command entry — before any I/O.
        client_ts = client_module.now_ts()
        points.append(
            DataPoint(
                chart_id=chart,
                group_key=group,
                metric_key=metric,
                value=float(value),
                client_ts=client_ts,
            )
        )
    else:
        assert batch is not None
        if batch == "-":
            points = list(_iter_batch_points(sys.stdin, default_chart=chart))
        else:
            with open(batch, "r", encoding="utf-8") as fp:
                points = list(_iter_batch_points(fp, default_chart=chart))

    req = IngestRequest(
        session_id=session_id,
        request_ts=client_module.now_ts(),
        points=points,
    )

    server: str = ctx.obj["server"]
    try:
        with LiveBenchClient(server) as client:
            resp = client.ingest(req)
    except LiveBenchError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise SystemExit(1)

    summary_parts = [f"accepted={resp.accepted}"]
    if resp.seq_from is not None and resp.seq_to is not None:
        summary_parts.append(f"seq={resp.seq_from}..{resp.seq_to}")
    console.print(f"[green]ok[/green] {session_id} {' '.join(summary_parts)}")

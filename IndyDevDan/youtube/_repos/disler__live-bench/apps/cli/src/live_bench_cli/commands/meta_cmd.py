"""`live-bench meta` — emit per-group metadata (prompt text, responses, etc.).

Sends arbitrary key-value metadata to a ``(chart_id, group_key)`` pair. The
backend merges new data into existing metadata for that pair, so responses
accumulate as backends complete.
"""

from __future__ import annotations

import json
import sys

import click
from rich.console import Console

from .. import client as client_module
from ..client import LiveBenchClient, LiveBenchError
from ..models import GroupMetadata, IngestRequest


@click.command()
@click.argument("session_id")
@click.option("--chart", "chart", default="default", show_default=True,
              help="Chart id inside the benchmark.")
@click.option("--group", "group", required=True,
              help="Group key (e.g., p1, p2).")
@click.option("--json", "json_data", required=True,
              help="JSON string or '-' for stdin.")
@click.pass_context
def meta(
    ctx: click.Context,
    session_id: str,
    chart: str,
    group: str,
    json_data: str,
) -> None:
    """Emit metadata for a (chart, group) pair."""

    console = Console()

    if json_data == "-":
        raw = sys.stdin.read()
    else:
        raw = json_data

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        console.print(f"[red]error:[/red] invalid JSON: {exc}")
        raise SystemExit(1)

    if not isinstance(data, dict):
        console.print("[red]error:[/red] JSON must be an object")
        raise SystemExit(1)

    req = IngestRequest(
        session_id=session_id,
        request_ts=client_module.now_ts(),
        metadata=[GroupMetadata(chart_id=chart, group_key=group, data=data)],
    )

    server: str = ctx.obj["server"]
    try:
        with LiveBenchClient(server) as client:
            client.ingest(req)
    except LiveBenchError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise SystemExit(1)

    console.print(f"[green]ok[/green] metadata {session_id} chart={chart} group={group}")

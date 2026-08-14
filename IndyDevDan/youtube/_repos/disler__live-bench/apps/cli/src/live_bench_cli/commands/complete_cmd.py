"""`live-bench complete <session_id> --group <g> ...` — mark groups complete."""

from __future__ import annotations

import click
from rich.console import Console

from .. import client as client_module
from ..client import LiveBenchClient, LiveBenchError
from ..models import CompletionRef, IngestRequest


@click.command()
@click.argument("session_id")
@click.option(
    "--group",
    "groups",
    multiple=True,
    required=True,
    help="Group key to mark complete (repeatable).",
)
@click.option(
    "--chart",
    "chart",
    default="default",
    show_default=True,
    help="Chart id that the groups belong to (multi-chart benchmarks only).",
)
@click.pass_context
def complete(
    ctx: click.Context,
    session_id: str,
    groups: tuple[str, ...],
    chart: str,
) -> None:
    """Mark one or more groups as complete for a session."""

    console = Console()
    refs = [CompletionRef(chart_id=chart, group_key=g) for g in groups]
    req = IngestRequest(
        session_id=session_id,
        request_ts=client_module.now_ts(),
        points=[],
        complete_groups=refs,
    )

    server: str = ctx.obj["server"]
    try:
        with LiveBenchClient(server) as client:
            resp = client.ingest(req)
    except LiveBenchError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise SystemExit(1)

    completed = ", ".join(resp.completed) if resp.completed else "(none)"
    console.print(f"[green]complete[/green] {session_id} groups={completed}")

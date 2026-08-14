"""`live-bench reset <session_id>` — wipe datapoints + datasets for a session."""

from __future__ import annotations

import click
from rich.console import Console

from ..client import LiveBenchClient, LiveBenchError


@click.command()
@click.argument("session_id")
@click.option("--yes", is_flag=True, help="Skip the confirmation prompt.")
@click.pass_context
def reset(ctx: click.Context, session_id: str, yes: bool) -> None:
    """Reset a benchmark session (wipes points + datasets)."""

    console = Console()
    if not yes:
        click.confirm(
            f"Reset session {session_id!r}? This deletes all datapoints and dataset status.",
            abort=True,
        )

    server: str = ctx.obj["server"]
    try:
        with LiveBenchClient(server) as client:
            data = client.reset(session_id)
    except LiveBenchError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise SystemExit(1)

    console.print(f"[green]reset[/green] {session_id} → {data}")

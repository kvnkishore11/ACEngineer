"""`live-bench ping` — verify connectivity to the backend.

Hits ``POST /ping`` which broadcasts a ping event to all active SSE
subscribers, confirming the full data path (CLI -> backend -> SSE -> frontend).
"""

from __future__ import annotations

import click
from rich.console import Console

from ..client import LiveBenchClient, LiveBenchError


@click.command()
@click.pass_context
def ping(ctx: click.Context) -> None:
    """Ping the backend and broadcast to all connected frontends."""

    console = Console()
    server: str = ctx.obj["server"]

    try:
        with LiveBenchClient(server) as client:
            r = client._client.post("/ping")
            if 200 <= r.status_code < 300:
                console.print(f"[green]pong[/green] {server}")
            else:
                console.print(f"[red]error[/red] {server} → {r.status_code}")
                raise SystemExit(1)
    except LiveBenchError as exc:
        console.print(f"[red]error[/red] {exc}")
        raise SystemExit(1)
    except Exception as exc:
        console.print(f"[red]error[/red] cannot reach {server} — {exc}")
        raise SystemExit(1)

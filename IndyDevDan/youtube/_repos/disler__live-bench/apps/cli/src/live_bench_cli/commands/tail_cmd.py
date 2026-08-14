"""`live-bench tail <session_id>` — dev-only SSE pretty-printer.

Opens ``GET /stream/{session_id}`` via the underlying ``httpx.Client``
and prints each ``event:`` block as it arrives. Runs until the user
hits Ctrl-C. Highlights ``client_ts`` and ``server_ts`` on every line
so you can eyeball clock skew.
"""

from __future__ import annotations

import json

import click
from rich.console import Console

from ..client import LiveBenchClient


@click.command()
@click.argument("session_id")
@click.pass_context
def tail(ctx: click.Context, session_id: str) -> None:
    """Attach to the SSE stream for a session and print events."""

    console = Console()
    server: str = ctx.obj["server"]

    with LiveBenchClient(server) as client:
        url = f"/stream/{session_id}"
        try:
            with client._client.stream("GET", url, timeout=None) as resp:
                if resp.status_code >= 400:
                    console.print(
                        f"[red]error:[/red] HTTP {resp.status_code} on GET {url}"
                    )
                    raise SystemExit(1)
                event_name: str | None = None
                event_id: str | None = None
                data_lines: list[str] = []
                for raw_line in resp.iter_lines():
                    line = raw_line if isinstance(raw_line, str) else raw_line.decode("utf-8", "replace")
                    if line == "":
                        # Dispatch event.
                        if event_name or data_lines:
                            data = "\n".join(data_lines)
                            _print_event(console, event_name, event_id, data)
                        event_name = None
                        event_id = None
                        data_lines = []
                        continue
                    if line.startswith(":"):
                        # SSE comment.
                        continue
                    if line.startswith("event:"):
                        event_name = line[len("event:"):].strip()
                    elif line.startswith("id:"):
                        event_id = line[len("id:"):].strip()
                    elif line.startswith("data:"):
                        data_lines.append(line[len("data:"):].lstrip())
        except KeyboardInterrupt:
            console.print("[dim]tail interrupted[/dim]")


def _print_event(
    console: Console,
    event: str | None,
    event_id: str | None,
    data: str,
) -> None:
    header = f"[bold cyan]{event or 'message'}[/bold cyan]"
    if event_id:
        header += f" [dim]id={event_id}[/dim]"

    client_ts = None
    server_ts = None
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError:
        parsed = None

    if isinstance(parsed, dict):
        if "point" in parsed and isinstance(parsed["point"], dict):
            client_ts = parsed["point"].get("client_ts")
            server_ts = parsed["point"].get("server_ts")
        else:
            client_ts = parsed.get("client_ts")
            server_ts = parsed.get("server_ts")

    stamp_bits: list[str] = []
    if client_ts:
        stamp_bits.append(f"[magenta]client_ts={client_ts}[/magenta]")
    if server_ts:
        stamp_bits.append(f"[yellow]server_ts={server_ts}[/yellow]")
    if stamp_bits:
        header += " " + " ".join(stamp_bits)

    console.print(header)
    console.print(data)

"""`live-bench list` — print the benchmarks table."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ..client import LiveBenchClient, LiveBenchError


@click.command("list")
@click.pass_context
def list_(ctx: click.Context) -> None:
    """List all benchmarks registered with the server."""

    server: str = ctx.obj["server"]
    console = Console()
    try:
        with LiveBenchClient(server) as client:
            data = client.list_benchmarks()
    except LiveBenchError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise SystemExit(1)

    benchmarks = data.get("benchmarks", [])

    table = Table(show_header=True, header_style="bold")
    table.add_column("session_id", style="cyan")
    table.add_column("title")
    table.add_column("subtitle")
    table.add_column("better")
    table.add_column("charts", justify="right")
    table.add_column("complete/total", justify="right")
    table.add_column("last_update")

    for b in benchmarks:
        completed = b.get("completed", 0)
        total = b.get("total", 0)
        # chart_count is a new field on BenchmarkSummary for multi-chart benchmarks.
        # Fall back to 1 for older backend responses that don't include it.
        chart_count = b.get("chart_count")
        if chart_count is None:
            chart_count = 1
        # better is nullable for multi-chart benchmarks — render an em-dash.
        better = b.get("better")
        if better is None or better == "":
            better_display = "—"
        else:
            better_display = str(better)
        table.add_row(
            str(b.get("session_id", "")),
            str(b.get("title", "")),
            str(b.get("subtitle", "") or ""),
            better_display,
            str(chart_count),
            f"{completed}/{total}",
            str(b.get("last_update", "") or "—"),
        )

    console.print(table)
    if not benchmarks:
        console.print(
            "[dim]No benchmarks registered — drop a YAML file in benchmarks/ and restart the server.[/dim]"
        )

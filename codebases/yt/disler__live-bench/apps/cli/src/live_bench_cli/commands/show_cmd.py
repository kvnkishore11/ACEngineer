"""`live-bench show <session_id>` — print config + latest matrix.

For single-chart benchmarks (one chart in ``config.all_charts``), renders
the legacy flat group/metric matrix. For multi-chart benchmarks, renders
one labeled section per chart with its own matrix and dataset status bar.
"""

from __future__ import annotations

import json as _json
from typing import Any

import click
from rich.console import Console
from rich.table import Table

from ..client import LiveBenchClient, LiveBenchError


_STATUS_COLORS = {
    "pending": "dim",
    "running": "yellow",
    "complete": "green",
}


def _better_label(better: Any) -> str:
    if better == "higher":
        return "Higher is better"
    if better == "lower":
        return "Lower is better"
    return ""


def _resolve_charts(config: dict) -> list[dict]:
    """Return the chart list, synthesising a default chart for legacy configs.

    Mirrors ``BenchmarkConfig.all_charts()`` from the Pydantic side: if the
    config has an explicit ``charts`` list, return it; otherwise synthesise a
    single ``default`` chart from the top-level legacy fields.
    """

    charts = config.get("charts")
    if isinstance(charts, list) and charts:
        return charts
    # Legacy single-chart synthesis.
    return [
        {
            "chart_id": "default",
            "title": None,
            "subtitle": None,
            "better": config.get("better"),
            "direction": config.get("direction", "BT"),
            "x": config.get("x"),
            "y": config.get("y"),
            "metrics": config.get("metrics", []) or [],
        }
    ]


def _render_chart_matrix(
    console: Console,
    chart: dict,
    groups: list[dict],
    latest: dict[tuple[str, str, str], dict],
    datasets_for_chart: list[dict],
) -> None:
    """Render one chart's matrix + dataset status bar.

    Uses the shared ``latest`` map keyed by ``(chart_id, group_key, metric_key)``.
    """

    chart_id = str(chart.get("chart_id", "default"))
    metrics = chart.get("metrics", []) or []

    if groups and metrics:
        matrix = Table(show_header=True, header_style="bold")
        matrix.add_column("group", style="cyan")
        for m in metrics:
            matrix.add_column(
                str(m.get("label") or m.get("key", "")), justify="right"
            )
        for g in groups:
            gk = g.get("key", "")
            row = [str(g.get("label") or gk)]
            for m in metrics:
                mk = m.get("key", "")
                cell = latest.get((chart_id, gk, mk))
                if cell is None:
                    row.append("—")
                else:
                    row.append(f"{cell.get('value')}")
            matrix.add_row(*row)
        console.print(matrix)

    # Per-chart dataset status line.
    total = len(datasets_for_chart)
    complete_count = sum(
        1 for d in datasets_for_chart if str(d.get("status", "")) == "complete"
    )
    console.print(f"[dim]Status: {complete_count}/{total} complete[/dim]")
    console.print()


@click.command()
@click.argument("session_id")
@click.option("--json", "as_json", is_flag=True, help="Print raw JSON instead of a pretty table.")
@click.pass_context
def show(ctx: click.Context, session_id: str, as_json: bool) -> None:
    """Show config + latest-per-cell values + per-group status for a session."""

    server: str = ctx.obj["server"]
    console = Console()
    try:
        with LiveBenchClient(server) as client:
            data = client.get_benchmark(session_id)
    except LiveBenchError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise SystemExit(1)

    if as_json:
        click.echo(_json.dumps(data, indent=2, sort_keys=True, default=str))
        return

    config = data.get("config", {}) or {}
    points = data.get("points", []) or []
    datasets = data.get("datasets", []) or []

    title = config.get("title", session_id)
    subtitle = config.get("subtitle") or ""

    console.print(f"[bold]{title}[/bold]")
    if subtitle:
        console.print(f"[dim]{subtitle}[/dim]")
    console.print()

    # Resolve charts — either the explicit multi-chart list or a synthesised
    # single-chart from the legacy top-level fields.
    charts = _resolve_charts(config)
    groups = config.get("groups", []) or []

    # Build latest map keyed by (chart_id, group_key, metric_key) from all points.
    # Each point carries chart_id (defaults to "default" for legacy points).
    latest: dict[tuple[str, str, str], dict] = {}
    for p in points:
        key = (
            str(p.get("chart_id", "default")),
            str(p.get("group_key", "")),
            str(p.get("metric_key", "")),
        )
        prev = latest.get(key)
        if prev is None or str(p.get("client_ts", "")) > str(prev.get("client_ts", "")):
            latest[key] = p

    # Group datasets by chart_id for per-chart status lines.
    datasets_by_chart: dict[str, list[dict]] = {}
    for d in datasets:
        cid = str(d.get("chart_id", "default"))
        datasets_by_chart.setdefault(cid, []).append(d)

    if len(charts) > 1:
        # Multi-chart: render one labeled section per chart.
        for chart in charts:
            chart_id = str(chart.get("chart_id", "default"))
            chart_title = chart.get("title") or chart_id
            better_label = _better_label(chart.get("better"))
            header = f"=== Chart: {chart_id}"
            if chart.get("title"):
                header += f" ({chart_title})"
            if better_label:
                header += f" — {better_label}"
            header += " ==="
            console.print(f"[bold]{header}[/bold]")
            _render_chart_matrix(
                console,
                chart,
                groups,
                latest,
                datasets_by_chart.get(chart_id, []),
            )

        # Flat dataset status table across all charts for detail.
        status_table = Table(show_header=True, header_style="bold")
        status_table.add_column("chart", style="magenta")
        status_table.add_column("group", style="cyan")
        status_table.add_column("status")
        status_table.add_column("started_at")
        status_table.add_column("completed_at")
        for d in datasets:
            status = str(d.get("status", "pending"))
            colour = _STATUS_COLORS.get(status, "white")
            status_table.add_row(
                str(d.get("chart_id", "default")),
                str(d.get("group_key", "")),
                f"[{colour}]{status}[/{colour}]",
                str(d.get("started_at") or "—"),
                str(d.get("completed_at") or "—"),
            )
        console.print(status_table)
        return

    # Single-chart path — keep the existing rendering shape.
    chart = charts[0]
    better_label = _better_label(chart.get("better") or config.get("better"))
    if better_label:
        console.print(f"[dim]{better_label}[/dim]")
        console.print()

    metrics = chart.get("metrics", []) or []
    chart_id = str(chart.get("chart_id", "default"))

    if groups and metrics:
        matrix = Table(show_header=True, header_style="bold")
        matrix.add_column("group", style="cyan")
        for m in metrics:
            matrix.add_column(str(m.get("label") or m.get("key", "")), justify="right")
        for g in groups:
            gk = g.get("key", "")
            row = [str(g.get("label") or gk)]
            for m in metrics:
                mk = m.get("key", "")
                cell = latest.get((chart_id, gk, mk))
                if cell is None:
                    row.append("—")
                else:
                    row.append(f"{cell.get('value')}")
            matrix.add_row(*row)
        console.print(matrix)
        console.print()

    # Dataset status pills.
    status_table = Table(show_header=True, header_style="bold")
    status_table.add_column("group", style="cyan")
    status_table.add_column("status")
    status_table.add_column("started_at")
    status_table.add_column("completed_at")
    for d in datasets:
        status = str(d.get("status", "pending"))
        colour = _STATUS_COLORS.get(status, "white")
        status_table.add_row(
            str(d.get("group_key", "")),
            f"[{colour}]{status}[/{colour}]",
            str(d.get("started_at") or "—"),
            str(d.get("completed_at") or "—"),
        )
    console.print(status_table)

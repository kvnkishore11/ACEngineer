"""Top-level click group for the ``live-bench`` console script.

Registers the seven subcommands from ``commands/`` and exposes the global
``--server`` / ``--verbose`` flags. Individual commands pull the server URL
out of the click context (``ctx.obj["server"]``) and instantiate a
``LiveBenchClient`` against it.
"""

from __future__ import annotations

import click
from dotenv import load_dotenv

# Load .env from current working directory so LIVE_BENCH_SERVER is picked up.
load_dotenv()

from .commands import (
    complete_cmd,
    emit_cmd,
    list_cmd,
    meta_cmd,
    ping_cmd,
    reset_cmd,
    show_cmd,
    stream_cmd,
    tail_cmd,
)


@click.group()
@click.option(
    "--server",
    envvar="LIVE_BENCH_SERVER",
    default="http://127.0.0.1:8787",
    show_default=True,
    help="Backend base URL (env: LIVE_BENCH_SERVER)",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Verbose logging",
)
@click.pass_context
def cli(ctx: click.Context, server: str, verbose: bool) -> None:
    """live-bench — push benchmark results at the server from anywhere on the LAN."""

    ctx.ensure_object(dict)
    ctx.obj["server"] = server
    ctx.obj["verbose"] = verbose


cli.add_command(list_cmd.list_, name="list")
cli.add_command(show_cmd.show)
cli.add_command(reset_cmd.reset)
cli.add_command(emit_cmd.emit)
cli.add_command(complete_cmd.complete)
cli.add_command(stream_cmd.stream)
cli.add_command(tail_cmd.tail)
cli.add_command(ping_cmd.ping)
cli.add_command(meta_cmd.meta)


if __name__ == "__main__":
    cli()

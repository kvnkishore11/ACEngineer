"""Minimal structured logging setup for live-bench.

A single module-level helper so every module can ``get_logger(__name__)`` and
share one root configuration. Logs to stderr with a compact, grep-friendly
format that carries level, logger name, and message.
"""

from __future__ import annotations

import logging
import os
import sys

_CONFIGURED = False

_FMT = "%(asctime)s %(levelname)-5s %(name)s :: %(message)s"
_DATEFMT = "%Y-%m-%dT%H:%M:%S"


def _configure_root() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    level_name = os.environ.get("LIVEBENCH_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    # Clear any handlers uvicorn may have wired up for the root logger so we
    # don't emit duplicate lines.
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(fmt=_FMT, datefmt=_DATEFMT))
    root.addHandler(handler)
    root.setLevel(level)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module name."""
    _configure_root()
    return logging.getLogger(name)


__all__ = ["get_logger"]

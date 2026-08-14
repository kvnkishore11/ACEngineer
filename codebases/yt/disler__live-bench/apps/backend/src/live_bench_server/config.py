"""YAML benchmark loader.

Reads ``benchmarks/*.yaml`` and validates each against ``BenchmarkFile``.
Raises ``ValueError(f"{filename}: {error}")`` on validation failure so the
caller (``main.py`` on boot) can surface exactly which file is broken.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from live_bench_server.models import BenchmarkFile


def load_benchmarks_dir(path: Path) -> list[tuple[BenchmarkFile, Path]]:
    """Load every ``*.yaml`` file in ``path``.

    Returns a list of ``(benchmark_file, source_path)`` tuples, sorted by file
    name for deterministic ordering on boot. Raises ``ValueError`` with a
    file-accurate message on the first validation failure.
    """
    if not path.exists():
        raise ValueError(f"benchmarks directory not found: {path}")

    files = sorted(path.glob("*.yaml"))
    out: list[tuple[BenchmarkFile, Path]] = []
    for f in files:
        try:
            raw = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise ValueError(f"{f.name}: invalid YAML: {exc}") from exc
        if not isinstance(raw, dict):
            raise ValueError(f"{f.name}: top-level YAML must be a mapping")
        try:
            parsed = BenchmarkFile.model_validate(raw)
        except ValidationError as exc:
            raise ValueError(f"{f.name}: {exc}") from exc
        out.append((parsed, f))
    return out


__all__ = ["load_benchmarks_dir"]

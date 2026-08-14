# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27"]
# ///
"""Context scaling benchmark (3-way) — GraphWalks at 8 context sizes.

Emits per-context-size results to live-bench for 4 chart types
(prefill, decode, wall, accuracy), tagged by hardware (m4/m5).

Uses pre-extracted GraphWalks fixtures from fixtures.json. Three models:
  - Qwen 3.5 35B MLX via Ollama (qwen3.5:35b-a3b-nvfp4)
  - Qwen 3.6 35B MLX via Ollama (qwen3.6:35b-a3b-nvfp4)
  - Gemma 4 26B MLX via MLXRunner

Run on M4:  uv run bench.py --hw m4
Run on M5:  uv run bench.py --hw m5
Smoke test: uv run bench.py --hw m4 --smoke
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _harness import MLXRunner, ollama_chat, run_warm_isolated  # noqa: E402

SESSION = "context-scaling-3way"

BENCH_DIR = Path(__file__).resolve().parent
FIXTURES_PATH = BENCH_DIR / "fixtures.json"
# Reuse the .mlx-venv from qwen35-vs-gemma4 — mlx-vlm is only needed for Gemma 4 MLX,
# and both qwen variants go through Ollama. No need to duplicate the venv.
MLX_VENV = Path(os.environ.get("MLX_VENV", BENCH_DIR.parent / "qwen35-vs-gemma4" / ".mlx-venv"))
MLX_PYTHON = MLX_VENV / "bin" / "python"
MLX_RUNNER = BENCH_DIR / "_mlx_runner.py"

# ── Context sizes (X-axis groups) ────────────────────────────
# ctx_64k is intentionally disabled for this run.
CONTEXT_SIZES = [
    {"key": "ctx_200", "label": "200"},
    {"key": "ctx_500", "label": "500"},
    {"key": "ctx_1k",  "label": "1K"},
    {"key": "ctx_2k",  "label": "2K"},
    {"key": "ctx_4k",  "label": "4K"},
    {"key": "ctx_8k",  "label": "8K"},
    {"key": "ctx_16k", "label": "16K"},
    {"key": "ctx_32k", "label": "32K"},
    # {"key": "ctx_64k", "label": "64K"},
]

# ── Backends ─────────────────────────────────────────────────
OLLAMA_BACKENDS = [
    {
        "metric": "qwen35_mlx",
        "model": "qwen3.5:35b-a3b-nvfp4",
        "label": "Qwen 3.5 (MLX via Ollama)",
    },
    {
        "metric": "qwen36_mlx",
        "model": "qwen3.6:35b-a3b-nvfp4",
        "label": "Qwen 3.6 (MLX via Ollama)",
    },
]
GEMMA4_MLX = {
    "metric": "gemma4_mlx",
    "model": "mlx-community/gemma-4-26b-a4b-it-4bit",
    "label": "Gemma 4 (MLX)",
}

ALL_METRICS = [b["metric"] for b in OLLAMA_BACKENDS] + [GEMMA4_MLX["metric"]]
NUM_METRICS = len(ALL_METRICS)  # 3

# ── Chart types ──────────────────────────────────────────────
CHART_TYPES = ["prefill", "decode", "wall", "accuracy"]


# ── Fixture loading ──────────────────────────────────────────
def load_fixtures() -> dict[str, dict]:
    """Load pre-extracted GraphWalks samples keyed by context size key."""
    with open(FIXTURES_PATH) as f:
        fixtures = json.load(f)
    return {fx["key"]: fx for fx in fixtures}


# ── F1 scoring ───────────────────────────────────────────────
def parse_final_answer(response: str) -> set[str]:
    """Extract node IDs from 'Final Answer: [node1, node2, ...]' in the response."""
    match = re.search(r"Final Answer:\s*\[([^\]]*)\]", response, re.IGNORECASE)
    if not match:
        return set()
    raw = match.group(1)
    nodes = {n.strip().strip("'\"") for n in raw.split(",") if n.strip()}
    return nodes


def f1_score(predicted: set[str], truth: set[str]) -> float:
    """Compute set-level F1 between predicted and ground-truth node sets."""
    if not truth and not predicted:
        return 1.0
    if not truth or not predicted:
        return 0.0
    correct = predicted & truth
    precision = len(correct) / len(predicted)
    recall = len(correct) / len(truth)
    return 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0


# ── CompletionTracker ────────────────────────────────────────
class CompletionTracker:
    """Tracks emits per context size. Marks complete when both metrics have reported."""

    def __init__(self, hw: str, server: str) -> None:
        self._hw = hw
        self._server = server
        self._seen: dict[str, set[str]] = {}

    def emit_and_track(
        self,
        group_key: str,
        metric_key: str,
        metrics: dict,
        *,
        f1: float,
        response_text: str = "",
        truth: set[str] | None = None,
        predicted: set[str] | None = None,
        fixture: dict | None = None,
    ) -> None:
        """Emit all 4 chart values + metadata, then check completion."""
        hw = self._hw
        server = self._server

        # Emit speed metrics to 3 charts
        for chart, value_key in [
            ("prefill", "prefill_tok_s"),
            ("decode", "decode_tok_s"),
            ("wall", "wall_time_s"),
        ]:
            cmd = [
                "live-bench", "--server", server, "emit", SESSION,
                "--chart", f"{chart}_{hw}", "--group", group_key,
                "--metric", metric_key, "--value", str(round(metrics[value_key], 1)),
            ]
            subprocess.run(cmd, check=True)

        # Emit accuracy (F1) to accuracy chart
        cmd = [
            "live-bench", "--server", server, "emit", SESSION,
            "--chart", f"accuracy_{hw}", "--group", group_key,
            "--metric", metric_key, "--value", str(round(f1, 4)),
        ]
        subprocess.run(cmd, check=True)

        # Emit metadata to prefill chart (shared across charts)
        meta: dict = {}
        # Context info from fixture
        if fixture is not None:
            meta["prompt_chars"] = fixture.get("prompt_chars", 0)
            meta["target_tokens"] = fixture.get("target_tokens", 0)
            meta["problem_type"] = fixture.get("problem_type", "")
            meta["synthetic"] = fixture.get("synthetic", False)
            meta["prompt"] = fixture.get("prompt", "")[:2000]
        if response_text:
            meta["responses"] = {metric_key: response_text[:4000]}
        if truth is not None:
            meta["expected_answer"] = sorted(truth)
        if predicted is not None:
            meta["model_answer"] = {metric_key: sorted(predicted)}
        meta["f1"] = {metric_key: round(f1, 4)}
        # Emit chart-specific metadata
        def _emit_meta(chart: str, data: dict) -> None:
            cmd = [
                "live-bench", "--server", server, "meta", SESSION,
                "--chart", f"{chart}_{hw}", "--group", group_key,
                "--json", json.dumps(data),
            ]
            subprocess.run(cmd, check=True)

        # Speed charts: context size + prompt info
        speed_meta: dict = {}
        if fixture is not None:
            speed_meta["prompt_chars"] = fixture.get("prompt_chars", 0)
            speed_meta["target_tokens"] = fixture.get("target_tokens", 0)
            speed_meta["problem_type"] = fixture.get("problem_type", "")
            speed_meta["synthetic"] = fixture.get("synthetic", False)
        if speed_meta:
            _emit_meta("prefill", speed_meta)
            _emit_meta("decode", speed_meta)

        # Wall chart: context size + per-model timing
        wall_meta: dict = {}
        if fixture is not None:
            wall_meta["prompt_chars"] = fixture.get("prompt_chars", 0)
            wall_meta["target_tokens"] = fixture.get("target_tokens", 0)
        wall_meta["wall_s"] = {metric_key: round(metrics["wall_time_s"], 3)}
        _emit_meta("wall", wall_meta)

        # Accuracy chart: expected vs actual answer + F1 + response
        accuracy_meta: dict = {}
        if fixture is not None:
            accuracy_meta["problem_type"] = fixture.get("problem_type", "")
            accuracy_meta["target_tokens"] = fixture.get("target_tokens", 0)
        if truth is not None:
            accuracy_meta["expected_answer"] = sorted(truth)
        if predicted is not None:
            accuracy_meta["model_answer"] = {metric_key: sorted(predicted)}
        accuracy_meta["f1"] = {metric_key: round(f1, 4)}
        if response_text:
            accuracy_meta["responses"] = {metric_key: response_text[:4000]}
        _emit_meta("accuracy", accuracy_meta)

        # Track completion
        seen = self._seen.setdefault(group_key, set())
        seen.add(metric_key)

        if len(seen) == NUM_METRICS:
            print(f"  ✓ {group_key} complete (all {NUM_METRICS} backends reported)", file=sys.stderr)
            for chart in CHART_TYPES:
                cmd = [
                    "live-bench", "--server", server, "complete", SESSION,
                    "--chart", f"{chart}_{hw}", "--group", group_key,
                ]
                subprocess.run(cmd, check=True)


# ── Benchmark functions ──────────────────────────────────────
def bench_ollama(
    fixtures: dict[str, dict],
    context_sizes: list[dict],
    iterations: int,
    hw: str,
    server: str,
    tracker: CompletionTracker,
) -> None:
    """Benchmark every Ollama-hosted MLX backend at each context size."""
    import time as _time

    prev_model: str | None = None
    for cfg in OLLAMA_BACKENDS:
        print(f"\n{'#'*70}", file=sys.stderr)
        print(f"  {cfg['label']}  ({cfg['model']})", file=sys.stderr)
        print(f"{'#'*70}", file=sys.stderr)

        # Unload the previous Ollama model so we don't bloat unified memory
        # across the two Qwen variants.
        if prev_model:
            subprocess.run(["ollama", "stop", prev_model], capture_output=True)
            _time.sleep(2)
        prev_model = cfg["model"]

        for cs in context_sizes:
            fx = fixtures[cs["key"]]
            prompt = fx["prompt"]
            truth = set(fx["answer_nodes"])
            num_ctx = fx["target_tokens"] + 1024

            print(f"\n  {cs['key']} ({cs['label']} tokens, {fx['problem_type']})", file=sys.stderr)

            m = run_warm_isolated(
                lambda p, _cfg=cfg, **kw: ollama_chat(_cfg["model"], p, think=False, **kw),
                prompt,
                iterations=iterations,
                max_tokens=16384,
                num_ctx=num_ctx,
                timeout=1200.0,
            )

            # Score accuracy
            response = m.get("text", "") or ""
            if m.get("raw_runs"):
                response = m["raw_runs"][-1].get("text", "") or response
            predicted = parse_final_answer(response)
            f1 = f1_score(predicted, truth)

            print(
                f"    prefill: {m['prefill_tok_s']:.1f}  decode: {m['decode_tok_s']:.1f}"
                f"  wall: {m['wall_time_s']:.3f}  F1: {f1:.4f}",
                file=sys.stderr,
            )
            tracker.emit_and_track(
                cs["key"], cfg["metric"], m,
                f1=f1, response_text=response, truth=truth, predicted=predicted,
                fixture=fx,
            )


def bench_gemma4_mlx(
    fixtures: dict[str, dict],
    context_sizes: list[dict],
    iterations: int,
    hw: str,
    server: str,
    tracker: CompletionTracker,
) -> None:
    """Benchmark Gemma 4 MLX via long-lived MLXRunner at each context size."""
    cfg = GEMMA4_MLX
    print(f"\n{'#'*70}", file=sys.stderr)
    print(f"  {cfg['label']}  ({cfg['model']})", file=sys.stderr)
    print(f"{'#'*70}", file=sys.stderr)

    if not MLX_PYTHON.exists():
        print(f"  SKIP: {MLX_PYTHON} not found (run setup for .mlx-venv)", file=sys.stderr)
        return

    print(f"  Booting long-lived mlx-vlm runner...", file=sys.stderr)
    runner = MLXRunner(MLX_PYTHON, MLX_RUNNER, cfg["model"])
    print(f"  Runner ready.", file=sys.stderr)

    try:
        for cs in context_sizes:
            fx = fixtures[cs["key"]]
            prompt = fx["prompt"]
            truth = set(fx["answer_nodes"])

            print(f"\n  {cs['key']} ({cs['label']} tokens, {fx['problem_type']})", file=sys.stderr)

            m = run_warm_isolated(
                lambda p, **kw: runner.generate(p, **kw),
                prompt,
                iterations=iterations,
                max_tokens=16384,
            )

            # Score accuracy
            response = m.get("text", "") or ""
            if m.get("raw_runs"):
                response = m["raw_runs"][-1].get("text", "") or response
            predicted = parse_final_answer(response)
            f1 = f1_score(predicted, truth)

            print(
                f"    prefill: {m['prefill_tok_s']:.1f}  decode: {m['decode_tok_s']:.1f}"
                f"  wall: {m['wall_time_s']:.3f}  F1: {f1:.4f}",
                file=sys.stderr,
            )
            tracker.emit_and_track(
                cs["key"], cfg["metric"], m,
                f1=f1, response_text=response, truth=truth, predicted=predicted,
                fixture=fx,
            )
    finally:
        runner.close()


# ── Main ─────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="Context scaling benchmark (3-way) — GraphWalks")
    ap.add_argument(
        "--hw", required=True, choices=["m4", "m5"],
        help="Hardware tag (m4 or m5) — determines which chart IDs to emit to",
    )
    ap.add_argument(
        "--iterations", type=int, default=1,
        help="Measured runs per context size (default 1; use 3+ for publication-grade median)",
    )
    ap.add_argument(
        "--smoke", action="store_true",
        help="Quick validation: 1 context size (ctx_200), 1 iteration",
    )
    ap.add_argument(
        "--server",
        default=os.environ.get("LIVE_BENCH_SERVER", "http://127.0.0.1:8787"),
        help="live-bench server URL (env: LIVE_BENCH_SERVER, default http://127.0.0.1:8787)",
    )
    args = ap.parse_args()

    # Load fixtures
    if not FIXTURES_PATH.exists():
        print(f"ERROR: {FIXTURES_PATH} not found. Run extract_fixtures.py first.", file=sys.stderr)
        return 1
    fixtures = load_fixtures()

    iterations = 1 if args.smoke else args.iterations
    context_sizes = [CONTEXT_SIZES[0]] if args.smoke else CONTEXT_SIZES

    # Verify all requested context sizes have fixtures
    for cs in context_sizes:
        if cs["key"] not in fixtures:
            print(f"ERROR: fixture missing for {cs['key']}", file=sys.stderr)
            return 1

    print(f"=== Context Scaling (3-way) · GraphWalks · {args.hw.upper()} Max ===", file=sys.stderr)
    print(f"    sizes={len(context_sizes)} iterations={iterations}", file=sys.stderr)

    tracker = CompletionTracker(args.hw, args.server)

    bench_ollama(fixtures, context_sizes, iterations, args.hw, args.server, tracker)
    bench_gemma4_mlx(fixtures, context_sizes, iterations, args.hw, args.server, tracker)

    print(f"\n=== {args.hw.upper()} Max benchmark complete ===", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

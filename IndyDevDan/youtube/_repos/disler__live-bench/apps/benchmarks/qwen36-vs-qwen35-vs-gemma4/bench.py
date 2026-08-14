# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "psutil>=5.9"]
# ///
"""Unified benchmark — runs all 6 backends through 5 prompts on one machine.

Emits per-prompt results to live-bench for 3 speed charts (prefill, decode,
wall) plus a memory chart, tagged by hardware (m4/m5). The hardware flag
determines the chart_id suffix:
  --hw m4  →  prefill_m4, decode_m4, wall_m4, memory_m4
  --hw m5  →  prefill_m5, decode_m5, wall_m5, memory_m5

Backends:
  qwen35_gguf · qwen35_mlx · qwen36_gguf · qwen36_mlx · gemma4_gguf · gemma4_mlx

Run on the M4 machine:   uv run bench.py --hw m4
Run on the M5 machine:   uv run bench.py --hw m5
Quick validation:         uv run bench.py --hw m4 --smoke
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import psutil

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _harness import MLXRunner, ollama_chat, run_warm_isolated  # noqa: E402

SESSION = "qwen36-vs-qwen35-vs-gemma4"
MEMORY_SESSION = SESSION  # memory charts are in the same benchmark


def _available_gb() -> float:
    """Current system available RAM in GB."""
    return psutil.virtual_memory().available / (1024 ** 3)


def _wait_stable(target=3, tol=0.5, interval=0.5, max_wait=15) -> float:
    """Wait for available RAM to stabilize, return average."""
    readings: list[float] = []
    for _ in range(int(max_wait / interval)):
        readings.append(_available_gb())
        if len(readings) >= target:
            recent = readings[-target:]
            if max(recent) - min(recent) < tol:
                return sum(recent) / len(recent)
        time.sleep(interval)
    return sum(readings[-3:]) / 3


def measure_memory_before() -> float:
    """Take a stable baseline reading of available RAM."""
    return _wait_stable()


def measure_memory_after(baseline: float) -> float:
    """Compute memory delta from baseline. Returns GB consumed."""
    time.sleep(1)
    after = _wait_stable(target=2, tol=0.5, interval=0.3)
    return round(baseline - after, 1)


def emit_memory(hw: str, group_key: str, memory_gb: float, server: str) -> None:
    """Emit a memory measurement to the memory chart."""
    subprocess.run(
        ["live-bench", "--server", server, "emit", SESSION,
         "--chart", f"memory_{hw}", "--group", group_key,
         "--metric", "memory_gb", "--value", str(memory_gb)],
        check=True,
    )

BENCH_DIR = Path(__file__).resolve().parent
MLX_VENV = Path(os.environ.get("MLX_VENV", BENCH_DIR / ".mlx-venv"))
MLX_PYTHON = MLX_VENV / "bin" / "python"
MLX_RUNNER = BENCH_DIR / "_mlx_runner.py"

# ── Backends ──────────────────────────────────────────────────
# Metric keys must match the YAML metrics.
OLLAMA_BACKENDS = [
    {"metric": "qwen35_gguf", "model": "qwen3.5:35b",           "label": "Qwen 3.5 (GGUF)"},
    {"metric": "qwen35_mlx",  "model": "qwen3.5:35b-a3b-nvfp4", "label": "Qwen 3.5 (MLX)"},
    {"metric": "qwen36_gguf", "model": "qwen3.6:35b-a3b",       "label": "Qwen 3.6 (GGUF)"},
    {"metric": "qwen36_mlx",  "model": "qwen3.6:35b-a3b-nvfp4", "label": "Qwen 3.6 (MLX)"},
    {"metric": "gemma4_gguf", "model": "gemma4:26b",            "label": "Gemma 4 (GGUF)"},
]
GEMMA4_MLX = {
    "metric": "gemma4_mlx",
    "model": "mlx-community/gemma-4-26b-a4b-it-4bit",
    "label": "Gemma 4 (MLX)",
}

# ── Prompts (X-axis groups) ───────────────────────────────────
# Group keys must match the YAML groups: p1..p5.
PROMPTS = [
    {"key": "p1", "label": "Short factual",
     "text": "Explain what a hash table is in 2 sentences."},
    {"key": "p2", "label": "Code generation",
     "text": "Write a Python implementation of quicksort with comments explaining each step."},
    {"key": "p3", "label": "Technical explanation",
     "text": "Explain the differences between TCP and UDP protocols, including use cases, advantages, disadvantages, and when to choose one over the other. Be thorough."},
    {"key": "p4", "label": "Complex code",
     "text": "Implement a binary search tree in Python with insert, delete, search, and in-order traversal methods. Include type hints and docstrings."},
    {"key": "p5", "label": "Deep reasoning + code",
     "text": "Design a rate limiter using the token bucket algorithm in Python. Include the class implementation with thread safety, explain the algorithm step by step, and show example usage with concurrent requests using threading. Include type hints throughout."},
]


ALL_METRICS = [b["metric"] for b in OLLAMA_BACKENDS] + [GEMMA4_MLX["metric"]]
NUM_METRICS = len(ALL_METRICS)  # 6


class CompletionTracker:
    """Tracks emits per prompt. Marks a prompt complete when all 4 metrics have reported."""

    def __init__(self, hw: str, server: str) -> None:
        self._hw = hw
        self._server = server
        self._seen: dict[str, set[str]] = {}
        self._prompts: dict[str, str] = {}  # prompt_key -> prompt text

    def set_prompt(self, prompt_key: str, prompt_text: str) -> None:
        """Store the prompt text for a group (called once per prompt)."""
        self._prompts[prompt_key] = prompt_text

    def emit_and_track(self, prompt_key: str, metric_key: str, metrics: dict,
                       response_text: str = "") -> None:
        """Emit all 3 chart values + metadata, then check if this prompt is now complete."""
        hw = self._hw
        server = self._server

        for chart, value_key in [("prefill", "prefill_tok_s"), ("decode", "decode_tok_s"), ("wall", "wall_time_s")]:
            cmd = ["live-bench", "--server", server, "emit", SESSION,
                   "--chart", f"{chart}_{hw}", "--group", prompt_key,
                   "--metric", metric_key, "--value", str(round(metrics[value_key], 1))]
            subprocess.run(cmd, check=True)

        # Emit metadata (prompt text + this model's response) — merges into existing.
        meta: dict = {}
        if prompt_key in self._prompts:
            meta["prompt"] = self._prompts[prompt_key]
        if response_text:
            meta["responses"] = {metric_key: response_text[:4000]}
        if meta:
            import json as _json
            # Emit to the prefill chart (metadata is per group, shared across charts)
            cmd = ["live-bench", "--server", server, "meta", SESSION,
                   "--chart", f"prefill_{hw}", "--group", prompt_key,
                   "--json", _json.dumps(meta)]
            subprocess.run(cmd, check=True)

        seen = self._seen.setdefault(prompt_key, set())
        seen.add(metric_key)

        if len(seen) == NUM_METRICS:
            print(f"  ✓ {prompt_key} complete (all {NUM_METRICS} backends reported)", file=sys.stderr)
            for chart in ("prefill", "decode", "wall"):
                cmd = ["live-bench", "--server", server, "complete", SESSION,
                       "--chart", f"{chart}_{hw}", "--group", prompt_key]
                subprocess.run(cmd, check=True)


def bench_ollama(prompts: list[dict], iterations: int, hw: str, server: str, tracker: CompletionTracker) -> None:
    """Benchmark all Ollama-hosted backends, emitting per-prompt results."""
    prev_model = None
    for cfg in OLLAMA_BACKENDS:
        print(f"\n{'#'*70}", file=sys.stderr)
        print(f"  {cfg['label']}  ({cfg['model']})", file=sys.stderr)
        print(f"{'#'*70}", file=sys.stderr)

        # Memory measurement: unload previous, measure baseline, warmup loads new
        if prev_model:
            subprocess.run(["ollama", "stop", prev_model], capture_output=True)
            time.sleep(2)
        baseline = measure_memory_before()
        print(f"  Memory baseline: {baseline:.1f} GB available", file=sys.stderr)

        # Warmup loads the model into memory
        ollama_chat(cfg["model"], "Say hi.", max_tokens=8)
        mem_gb = measure_memory_after(baseline)
        print(f"  Memory used: {mem_gb} GB", file=sys.stderr)
        emit_memory(hw, cfg["metric"], mem_gb, server)
        prev_model = cfg["model"]

        for p in prompts:
            print(f"\n  {p['key']} {p['label']}", file=sys.stderr)
            tracker.set_prompt(p["key"], p["text"])
            m = run_warm_isolated(
                lambda prompt, **kw: ollama_chat(cfg["model"], prompt, think=True, **kw),
                p["text"],
                iterations=iterations,
                max_tokens=4096,
                num_ctx=8192,
            )
            print(f"    prefill: {m['prefill_tok_s']:.1f}  decode: {m['decode_tok_s']:.1f}  wall: {m['wall_time_s']:.3f}", file=sys.stderr)
            response = m.get("text", "") or ""
            if m.get("raw_runs"):
                response = m["raw_runs"][-1].get("text", "") or response
            tracker.emit_and_track(p["key"], cfg["metric"], m, response_text=response)


def bench_gemma4_mlx(prompts: list[dict], iterations: int, hw: str, server: str, tracker: CompletionTracker) -> None:
    """Benchmark Gemma 4 MLX via long-lived MLXRunner."""
    cfg = GEMMA4_MLX
    print(f"\n{'#'*70}", file=sys.stderr)
    print(f"  {cfg['label']}  ({cfg['model']})", file=sys.stderr)
    print(f"{'#'*70}", file=sys.stderr)

    if not MLX_PYTHON.exists():
        print(f"  SKIP: {MLX_PYTHON} not found (run setup for .mlx-venv)", file=sys.stderr)
        return

    # Unload any Ollama models to get clean baseline
    for m in [b["model"] for b in OLLAMA_BACKENDS]:
        subprocess.run(["ollama", "stop", m], capture_output=True)
    time.sleep(2)
    baseline = measure_memory_before()
    print(f"  Memory baseline: {baseline:.1f} GB available", file=sys.stderr)

    print(f"  Booting long-lived mlx-vlm runner...", file=sys.stderr)
    runner = MLXRunner(MLX_PYTHON, MLX_RUNNER, cfg["model"])
    print(f"  Runner ready.", file=sys.stderr)

    mem_gb = measure_memory_after(baseline)
    print(f"  Memory used: {mem_gb} GB", file=sys.stderr)
    emit_memory(hw, cfg["metric"], mem_gb, server)

    try:
        for p in prompts:
            print(f"\n  {p['key']} {p['label']}", file=sys.stderr)
            tracker.set_prompt(p["key"], p["text"])
            m = run_warm_isolated(
                lambda prompt, **kw: runner.generate(prompt, **kw),
                p["text"],
                iterations=iterations,
                max_tokens=4096,
            )
            print(f"    prefill: {m['prefill_tok_s']:.1f}  decode: {m['decode_tok_s']:.1f}  wall: {m['wall_time_s']:.3f}", file=sys.stderr)
            response = m.get("text", "") or ""
            if m.get("raw_runs"):
                response = m["raw_runs"][-1].get("text", "") or response
            tracker.emit_and_track(p["key"], cfg["metric"], m, response_text=response)
    finally:
        runner.close()


def main() -> int:
    ap = argparse.ArgumentParser(description="Qwen 3.6 vs Qwen 3.5 vs Gemma 4 benchmark")
    ap.add_argument("--hw", required=True, choices=["m4", "m5"],
                    help="Hardware tag (m4 or m5) — determines which chart IDs to emit to")
    ap.add_argument("--iterations", type=int, default=1,
                    help="Measured runs per prompt (default 1; use 3+ for publication-grade median)")
    ap.add_argument("--smoke", action="store_true",
                    help="Quick validation: 1 prompt, 1 iteration")
    ap.add_argument("--server", default=os.environ.get("LIVE_BENCH_SERVER", "http://127.0.0.1:8787"),
                    help="live-bench server URL (env: LIVE_BENCH_SERVER)")
    args = ap.parse_args()

    iterations = 1 if args.smoke else args.iterations
    prompts = PROMPTS[:1] if args.smoke else PROMPTS

    print(f"=== Qwen 3.6 vs Qwen 3.5 vs Gemma 4 · {args.hw.upper()} Max ===", file=sys.stderr)
    print(f"    prompts={len(prompts)} iterations={iterations}", file=sys.stderr)

    tracker = CompletionTracker(args.hw, args.server)

    bench_ollama(prompts, iterations, args.hw, args.server, tracker)
    bench_gemma4_mlx(prompts, iterations, args.hw, args.server, tracker)

    print(f"\n=== {args.hw.upper()} Max benchmark complete ===", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

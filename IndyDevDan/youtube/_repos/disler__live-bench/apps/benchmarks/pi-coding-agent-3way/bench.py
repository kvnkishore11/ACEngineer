# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27"]
# ///
"""Pi coding agent benchmark (3-way) — 6 tasks × 5 models on one machine.

Emits per-task results to live-bench for 4 charts (wall, score, tokens, tools),
tagged by hardware (m4/m5).

Models: Qwen 3.5 GGUF · Qwen 3.5 MLX · Qwen 3.6 GGUF · Qwen 3.6 MLX · Gemma 4 GGUF

Run on M4:  uv run bench.py --hw m4
Run on M5:  uv run bench.py --hw m5
Smoke test: uv run bench.py --hw m4 --smoke
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pi_runner import PiResult, run_pi_task, warmup_model  # noqa: E402
from _tasks import TASKS, cleanup_task_dir, setup_task_dir  # noqa: E402

SESSION = "pi-coding-agent-3way"
CHART_TYPES = ["wall", "score", "tokens", "tools"]

# ── Models (all via Ollama provider) ─────────────────────────────
MODELS = [
    {"metric": "qwen35_gguf", "model": "qwen3.5:35b",           "label": "Qwen 3.5 GGUF", "provider": "ollama"},
    {"metric": "qwen35_mlx",  "model": "qwen3.5:35b-a3b-nvfp4", "label": "Qwen 3.5 MLX",  "provider": "ollama"},
    {"metric": "qwen36_gguf", "model": "qwen3.6:35b-a3b",       "label": "Qwen 3.6 GGUF", "provider": "ollama"},
    {"metric": "qwen36_mlx",  "model": "qwen3.6:35b-a3b-nvfp4", "label": "Qwen 3.6 MLX",  "provider": "ollama"},
    {"metric": "gemma4_gguf", "model": "gemma4:26b",            "label": "Gemma 4 GGUF",  "provider": "ollama"},
]
NUM_MODELS = len(MODELS)


def _emit(server: str, chart: str, group: str, metric: str, value: float) -> None:
    subprocess.run(
        ["live-bench", "--server", server, "emit", SESSION,
         "--chart", chart, "--group", group,
         "--metric", metric, "--value", str(round(value, 4))],
        check=True,
    )


def _emit_meta(server: str, chart: str, group: str, data: dict) -> None:
    subprocess.run(
        ["live-bench", "--server", server, "meta", SESSION,
         "--chart", chart, "--group", group,
         "--json", json.dumps(data)],
        check=True,
    )


def _emit_complete(server: str, chart: str, group: str) -> None:
    subprocess.run(
        ["live-bench", "--server", server, "complete", SESSION,
         "--chart", chart, "--group", group],
        check=True,
    )


class CompletionTracker:
    """Tracks emits per task. Marks complete when all models have reported."""

    def __init__(self, hw: str, server: str) -> None:
        self._hw = hw
        self._server = server
        self._seen: dict[str, set[str]] = {}
        self._prompts: dict[str, str] = {}

    def set_prompt(self, task_key: str, prompt_text: str) -> None:
        self._prompts[task_key] = prompt_text

    def emit_and_track(
        self,
        task_key: str,
        metric_key: str,
        pi_result: PiResult,
        score: float,
        score_detail: str,
        score_checks: list[dict],
    ) -> None:
        hw = self._hw
        server = self._server

        # 1. Emit numeric values to each chart
        for chart, value in [
            ("wall",   pi_result.wall_time_s),
            ("score",  score),
            ("tokens", pi_result.total_tokens),
            ("tools",  pi_result.tool_calls),
        ]:
            _emit(server, f"{chart}_{hw}", task_key, metric_key, value)

        prompt_text = self._prompts.get(task_key, "")

        # 2. Per-chart metadata

        # wall: prompt + response + timing
        _emit_meta(server, f"wall_{hw}", task_key, {
            "prompt": prompt_text,
            "responses": {metric_key: pi_result.response_text[:4000]},
            "wall_time": {metric_key: {
                "seconds": round(pi_result.wall_time_s, 1),
                "timed_out": pi_result.timed_out,
            }},
        })

        # score: prompt + verification details
        _emit_meta(server, f"score_{hw}", task_key, {
            "prompt": prompt_text,
            "verification": {metric_key: {
                "score": round(score, 4),
                "detail": score_detail,
                "checks": score_checks,
            }},
        })

        # tokens: prompt + per-turn breakdown
        _emit_meta(server, f"tokens_{hw}", task_key, {
            "prompt": prompt_text,
            "token_breakdown": {metric_key: {
                "total": pi_result.total_tokens,
                "input": pi_result.total_input_tokens,
                "output": pi_result.total_output_tokens,
                "turns": pi_result.turn_details,
            }},
        })

        # tools: prompt + tool call sequence
        _emit_meta(server, f"tools_{hw}", task_key, {
            "prompt": prompt_text,
            "tool_calls": {metric_key: pi_result.tool_call_details},
        })

        # 3. Track completion
        seen = self._seen.setdefault(task_key, set())
        seen.add(metric_key)

        if len(seen) == NUM_MODELS:
            print(f"  \u2713 {task_key} complete (all {NUM_MODELS} models reported)", file=sys.stderr)
            for chart in CHART_TYPES:
                _emit_complete(server, f"{chart}_{hw}", task_key)


def main() -> int:
    ap = argparse.ArgumentParser(description="Pi coding agent (3-way) benchmark")
    ap.add_argument("--hw", required=True, choices=["m4", "m5"],
                    help="Hardware tag (m4 or m5)")
    ap.add_argument("--smoke", action="store_true",
                    help="Quick validation: T1 only, first model only")
    ap.add_argument("--server",
                    default=os.environ.get("LIVE_BENCH_SERVER", "http://127.0.0.1:8787"),
                    help="live-bench server URL")
    ap.add_argument("--timeout", type=int, default=300,
                    help="Timeout per task in seconds (default 300)")
    args = ap.parse_args()

    models = MODELS[:1] if args.smoke else MODELS
    tasks = TASKS[:1] if args.smoke else TASKS

    print(f"=== Pi Coding Agent (3-way) \u00b7 {args.hw.upper()} Max ===", file=sys.stderr)
    print(f"    tasks={len(tasks)} models={len(models)}", file=sys.stderr)

    tracker = CompletionTracker(args.hw, args.server)

    for cfg in models:
        print(f"\n{'#'*70}", file=sys.stderr)
        print(f"  {cfg['label']}  ({cfg['model']})", file=sys.stderr)
        print(f"{'#'*70}", file=sys.stderr)

        warmup_model(cfg["model"], provider=cfg["provider"])

        for task in tasks:
            print(f"\n  {task.key}: {task.label}", file=sys.stderr)
            tracker.set_prompt(task.key, task.prompt)

            # Fresh isolated temp dir
            task_dir = setup_task_dir(task)
            print(f"    dir: {task_dir}", file=sys.stderr)

            try:
                # Run Pi agent
                pi_result = run_pi_task(
                    cfg["model"], task.prompt, task_dir,
                    provider=cfg["provider"],
                    timeout=args.timeout,
                )

                status = "TIMEOUT" if pi_result.timed_out else (
                    "OK" if pi_result.exit_code == 0 else f"EXIT {pi_result.exit_code}")
                print(f"    pi: {status} in {pi_result.wall_time_s:.1f}s "
                      f"({pi_result.total_tokens} tok, {pi_result.tool_calls} tools, "
                      f"{pi_result.turns} turns)", file=sys.stderr)

                # Verify
                score, detail, checks = task.verify(task_dir)
                print(f"    verify: {detail} (score={score:.2f})", file=sys.stderr)

                # Emit
                tracker.emit_and_track(
                    task.key, cfg["metric"], pi_result,
                    score, detail, checks,
                )
            except Exception as e:
                print(f"    ERROR: {e}", file=sys.stderr)
                # Emit zeros on error
                error_result = PiResult(
                    wall_time_s=args.timeout, exit_code=-1, timed_out=True)
                tracker.emit_and_track(
                    task.key, cfg["metric"], error_result,
                    0.0, f"error: {e}", [],
                )
            finally:
                cleanup_task_dir(task_dir)

        # Unload model before next
        print(f"\n  Unloading {cfg['model']}...", file=sys.stderr)
        subprocess.run(["ollama", "stop", cfg["model"]], capture_output=True)
        time.sleep(2)

    print(f"\n=== {args.hw.upper()} Max benchmark complete ===", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

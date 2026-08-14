# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27"]
# ///
"""Ping all 4 models back-to-back and report speed metrics.

Quick smoke test to verify every model responds and compare performance
across machines (M4 vs M5). Runs in order: GGUF Qwen, MLX Qwen, GGUF
Gemma 4, MLX Gemma 4. Each model prints its row as soon as it finishes.

Usage:
    uv run apps/benchmarks/ping/run.py
    uv run apps/benchmarks/ping/run.py --prompt "Write a haiku about code"
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx

OLLAMA_URL = "http://localhost:11434"

BENCH_ROOT = Path(__file__).resolve().parent.parent
MLX_VENV = Path(os.environ.get(
    "MLX_VENV",
    BENCH_ROOT / "qwen35-vs-gemma4" / ".mlx-venv",
))
MLX_PYTHON = MLX_VENV / "bin" / "python"
MLX_RUNNER = BENCH_ROOT / "qwen35-vs-gemma4" / "_mlx_runner.py"

MODELS = [
    {"label": "qwen3.5:35b",                              "backend": "ollama"},
    {"label": "qwen3.5:35b-a3b-nvfp4",                    "backend": "ollama"},
    {"label": "gemma4:26b",                                "backend": "ollama"},
    {"label": "gemma-4-26b-a4b-it-4bit", "model": "mlx-community/gemma-4-26b-a4b-it-4bit", "backend": "mlx"},
]


def ping_ollama(model: str, prompt: str) -> dict:
    """Single Ollama /api/chat call, returns metrics."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "keep_alive": -1,
        "options": {"num_ctx": 4096, "num_predict": 2048},
    }
    wall_start = time.perf_counter()
    resp = httpx.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=300)
    wall = time.perf_counter() - wall_start
    resp.raise_for_status()
    d = resp.json()

    ns = 1_000_000_000
    pec = d.get("prompt_eval_count", 0)
    ped = d.get("prompt_eval_duration", 0)
    ec = d.get("eval_count", 0)
    ed = d.get("eval_duration", 0)

    msg = d.get("message", {})
    text = msg.get("content", "") or msg.get("thinking", "")

    return {
        "prefill_tok_s": round(pec / ped * ns if ped else 0, 1),
        "decode_tok_s": round(ec / ed * ns if ed else 0, 1),
        "wall_time_s": round(wall, 3),
        "text": text,
    }


def ping_mlx(model: str, prompt: str) -> dict:
    """Boot MLX runner, send one prompt, shut down. Returns metrics."""
    if not MLX_PYTHON.exists():
        return {"error": f"MLX venv not found at {MLX_PYTHON}"}

    proc = subprocess.Popen(
        [str(MLX_PYTHON), str(MLX_RUNNER), model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    # Wait for ready
    deadline = time.time() + 300
    while True:
        if proc.poll() is not None:
            err = proc.stderr.read() if proc.stderr else ""
            return {"error": f"MLX runner died: {err[:500]}"}
        if time.time() > deadline:
            proc.kill()
            return {"error": "MLX runner ready timeout (300s)"}
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.05)
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("event") == "ready":
            break
        if msg.get("event") == "error":
            return {"error": msg.get("detail", "unknown")}

    # Send prompt
    wall_start = time.perf_counter()
    proc.stdin.write(json.dumps({"prompt": prompt, "max_tokens": 256}) + "\n")
    proc.stdin.flush()

    # Read result
    result = None
    while True:
        line = proc.stdout.readline()
        if not line:
            err = proc.stderr.read() if proc.stderr else ""
            result = {"error": f"MLX runner died mid-call: {err[:500]}"}
            break
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("event") == "result":
            wall = time.perf_counter() - wall_start
            result = {
                "prefill_tok_s": msg.get("prefill_tok_s", 0),
                "decode_tok_s": msg.get("decode_tok_s", 0),
                "wall_time_s": round(wall, 3),
                "text": msg.get("text", ""),
            }
            break
        if msg.get("event") == "error":
            result = {"error": msg.get("detail", "unknown")}
            break

    # Shutdown
    try:
        proc.stdin.write(json.dumps({"cmd": "exit"}) + "\n")
        proc.stdin.flush()
    except (BrokenPipeError, OSError):
        pass
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()

    return result


def truncate(text: str, max_len: int = 80) -> str:
    """Collapse whitespace and truncate for display."""
    flat = " ".join(text.split())
    if len(flat) <= max_len:
        return flat
    return flat[: max_len - 3] + "..."


def main() -> int:
    ap = argparse.ArgumentParser(description="Ping all 4 models")
    ap.add_argument(
        "--prompt",
        default="Explain what a hash table is in one sentence.",
        help="Prompt to send to each model",
    )
    args = ap.parse_args()

    # ANSI colors
    C = "\033[36m"   # cyan — model
    G = "\033[32m"   # green — values
    Y = "\033[33m"   # yellow — response
    R = "\033[31m"   # red — errors
    D = "\033[2m"    # dim — keys
    Z = "\033[0m"    # reset

    print(f"{D}prompt:{Z} {C}{args.prompt}{Z}\n", flush=True)
    W = 28  # model column width
    RW = 20  # response column width
    print(f"{D}{'Model':<{W}} {'Prefill':>10} {'Decode':>10} {'Wall':>8}   {'Response':<{RW}}{Z}", flush=True)
    print(f"{D}{'-'*W} {'-'*10} {'-'*10} {'-'*8}   {'-'*RW}{Z}", flush=True)

    ok = True
    for cfg in MODELS:
        label = cfg["label"]
        model = cfg.get("model", label)

        if cfg["backend"] == "ollama":
            try:
                r = ping_ollama(model, args.prompt)
            except Exception as e:
                print(f"{C}{label:<{W}}{Z} {R}ERROR: {e}{Z}", flush=True)
                ok = False
                continue
        else:
            r = ping_mlx(model, args.prompt)

        if "error" in r:
            print(f"{C}{label:<{W}}{Z} {R}ERROR: {r['error']}{Z}", flush=True)
            ok = False
            continue

        resp = truncate(r["text"], RW)
        print(
            f"{C}{label:<{W}}{Z}"
            f" {G}{r['prefill_tok_s']:>8.1f}/s{Z}"
            f" {G}{r['decode_tok_s']:>8.1f}/s{Z}"
            f" {G}{r['wall_time_s']:>7.3f}s{Z}"
            f"   {Y}{resp}{Z}",
            flush=True,
        )

    print(flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

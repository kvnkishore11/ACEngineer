"""Warm-isolated benchmark harness for Ollama (GGUF) and mlx-vlm (MLX) backends.

The two big problems this module solves:

1. **Cold-process MLX**: previously every MLX measurement was its own
   `subprocess.run([mlx_python, ...])` call. Each spawn paid the lazy weight
   page-fault tax + the Metal kernel JIT tax inside the *first* prefill,
   producing artificially low prefill numbers (~150 tok/s when the warm
   reality is 500-800+).

   Fix: `MLXRunner` boots one long-lived `_mlx_runner.py` subprocess per
   model and feeds it JSON requests on stdin / reads JSON metrics on stdout.
   Weights stay loaded, kernels stay JIT-cached, vision/audio caches persist.

2. **Cross-call cache contamination**: both Ollama and mlx-vlm cache prompt
   prefixes between calls. If we measure the same prompt 3 times, runs 2-3
   are trivial cache hits and the median is meaningless.

   Fix: every measured call gets a unique `[run:<nonce>] ` prefix so the
   cache key is different on every iteration. This forces real
   prefill-from-scratch on every measurement.

Usage:

    from _harness import MLXRunner, run_warm_isolated, ollama_chat

    # MLX side — long-lived process
    mlx = MLXRunner(MLX_PYTHON, MLX_RUNNER_SCRIPT, "mlx-community/gemma-4-26b-a4b-it-4bit")
    metrics = run_warm_isolated(
        lambda p, **kw: mlx.generate(p, max_tokens=4096, **kw),
        prompt="Explain hash tables",
        iterations=3,
    )
    mlx.close()

    # GGUF side — Ollama daemon, kept hot via keep_alive=-1
    metrics = run_warm_isolated(
        lambda p, **kw: ollama_chat("gemma4:26b", p, max_tokens=4096, **kw),
        prompt="Explain hash tables",
        iterations=3,
    )
"""

from __future__ import annotations

import json
import subprocess
import time
import uuid
from pathlib import Path
from statistics import median
from typing import Any, Callable

import httpx

OLLAMA_URL = "http://localhost:11434"


# ─────────────────────────────────────────────────────────────────────
#  Nonce — defeat prompt-prefix caching on both backends
# ─────────────────────────────────────────────────────────────────────

def make_nonce() -> str:
    return uuid.uuid4().hex[:8]


def nonce_prompt(prompt: str) -> str:
    """Prefix a unique nonce so every measured run is a true cache miss."""
    return f"[run:{make_nonce()}] {prompt}"


# ─────────────────────────────────────────────────────────────────────
#  Long-lived MLX subprocess driver
# ─────────────────────────────────────────────────────────────────────

class MLXRunner:
    """Spawns one long-lived mlx-vlm subprocess and reuses it across calls.

    The subprocess loads the model exactly once. From then on it stays warm:
    weights resident in unified memory, Metal kernels JIT-compiled and cached,
    feature caches populated. Every subsequent generate() call hits steady
    state, which is what we want to measure.
    """

    def __init__(self, mlx_python: Path, runner_script: Path, model: str,
                 *, ready_timeout: float = 600.0):
        self.model = model
        self.proc = subprocess.Popen(
            [str(mlx_python), str(runner_script), model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        # Wait for the runner to print {"event": "ready"} on stdout.
        # First load can take a while (mlx-vlm download + lazy weight init).
        deadline = time.time() + ready_timeout
        while True:
            if self.proc.poll() is not None:
                err = self.proc.stderr.read() if self.proc.stderr else ""
                raise RuntimeError(
                    f"MLX runner died before ready: exit={self.proc.returncode}\n{err[:2000]}"
                )
            if time.time() > deadline:
                raise RuntimeError(f"MLX runner ready timeout ({ready_timeout}s)")
            line = self.proc.stdout.readline()
            if not line:
                time.sleep(0.05)
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                # Ignore non-JSON noise (mlx-vlm prints status lines)
                continue
            if msg.get("event") == "ready":
                return
            if msg.get("event") == "error":
                raise RuntimeError(f"MLX runner error: {msg.get('detail')}")

    def generate(self, prompt: str, *, max_tokens: int = 4096,
                 audio: str | None = None, image: str | None = None) -> dict:
        """Send one generate request and return the metrics dict."""
        req: dict[str, Any] = {"prompt": prompt, "max_tokens": max_tokens}
        if audio:
            req["audio"] = audio
        if image:
            req["image"] = image

        self.proc.stdin.write(json.dumps(req) + "\n")
        self.proc.stdin.flush()

        # Read until we get a result line (skip non-JSON noise)
        while True:
            line = self.proc.stdout.readline()
            if not line:
                err = self.proc.stderr.read() if self.proc.stderr else ""
                raise RuntimeError(f"MLX runner died mid-call:\n{err[:2000]}")
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("event") == "result":
                return msg
            if msg.get("event") == "error":
                raise RuntimeError(f"MLX runner error: {msg.get('detail')}")

    def close(self):
        try:
            self.proc.stdin.write(json.dumps({"cmd": "exit"}) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()


# ─────────────────────────────────────────────────────────────────────
#  Ollama wrapper — keep_alive=-1 by default to defeat the 5min eviction
# ─────────────────────────────────────────────────────────────────────

def ollama_chat(model: str, prompt: str, *,
                max_tokens: int = 4096,
                num_ctx: int = 8192,
                think: bool = False,
                images: list[str] | None = None,
                audio: str | None = None,  # noqa: ARG001  (kept for API symmetry)
                image: str | None = None,  # noqa: ARG001  (kept for API symmetry)
                timeout: float = 600.0) -> dict:
    """Single Ollama /api/chat call with keep_alive=-1.

    Always returns the same metrics dict shape as MLXRunner.generate(), so the
    same `run_warm_isolated` driver works for both backends.
    """
    msg: dict[str, Any] = {"role": "user", "content": prompt}
    if images:
        msg["images"] = images

    payload = {
        "model": model,
        "messages": [msg],
        "stream": False,
        "keep_alive": -1,  # never evict — match the warm-mlx-process baseline
        "think": think,
        "options": {
            "num_ctx": num_ctx,
            "num_predict": max_tokens,
        },
    }

    wall_start = time.perf_counter()
    resp = httpx.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=timeout)
    wall = time.perf_counter() - wall_start
    resp.raise_for_status()
    d = resp.json()

    ns = 1_000_000_000
    pec = d.get("prompt_eval_count", 0)
    ped = d.get("prompt_eval_duration", 0)
    ec = d.get("eval_count", 0)
    ed = d.get("eval_duration", 0)

    return {
        "event": "result",
        "prefill_tok_s": round(pec / ped * ns if ped else 0, 1),
        "decode_tok_s": round(ec / ed * ns if ed else 0, 1),
        "prompt_tokens": pec,
        "gen_tokens": ec,
        "wall_time_s": round(wall, 3),
        "text": d.get("message", {}).get("content", ""),
    }


# ─────────────────────────────────────────────────────────────────────
#  Warm-isolated runner — warmup discard + N measured runs + median
# ─────────────────────────────────────────────────────────────────────

METRIC_KEYS = ["prefill_tok_s", "decode_tok_s", "wall_time_s",
               "prompt_tokens", "gen_tokens"]


def median_metrics(results: list[dict]) -> dict:
    out: dict[str, float] = {}
    for k in METRIC_KEYS:
        vals = [float(r.get(k, 0)) for r in results if r.get(k) is not None]
        out[k] = round(median(vals), 3) if vals else 0.0
    return out


def run_warm_isolated(call_fn: Callable[..., dict],
                      prompt: str,
                      *,
                      iterations: int = 3,
                      warmup_prompt: str = "Say hi.",
                      warmup_kwargs: dict | None = None,
                      **call_kwargs) -> dict:
    """Run a single (prompt, settings) measurement with warm-isolated semantics.

    Flow:
        1. One warmup call with `warmup_prompt` — discarded. This faults in
           weight pages and JIT-compiles Metal kernels.
        2. `iterations` measured calls with `prompt` — each gets its own
           unique nonce prefix so neither backend's prompt cache can hit.
        3. Returns the **median** of metric_keys across the measured runs,
           plus the raw runs under "raw_runs" for sanity checking.
    """
    # Warmup — discard. Tiny budget, no nonce needed (it's a different prompt).
    wkw = dict(call_kwargs)
    if warmup_kwargs:
        wkw.update(warmup_kwargs)
    wkw.setdefault("max_tokens", 8)
    try:
        call_fn(warmup_prompt, **wkw)
    except Exception as e:
        # Warmup failure shouldn't kill the bench — log and continue
        print(f"  [warmup failed: {e}]")

    # Measured runs
    results = []
    for i in range(iterations):
        nonced = nonce_prompt(prompt)
        result = call_fn(nonced, **call_kwargs)
        results.append(result)

    medians = median_metrics(results)
    medians["raw_runs"] = results
    medians["iterations"] = iterations
    return medians

# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27", "psutil>=5.9"]
# ///
"""Measure actual memory consumption for all 4 backends.

Uses system-wide available RAM delta — the only metric that captures
ALL memory types (CPU pages, Metal/GPU buffers, mmap'd weights, KV cache)
regardless of backend. Apples-to-apples.

Methodology:
  1. Unload all models, wait for memory to settle
  2. Read psutil.virtual_memory().available (baseline)
  3. Load model + warmup + run inference
  4. Read available again
  5. Delta = memory consumed by this model
"""

import json
import os
import subprocess
import sys
import time

import httpx
import psutil


OLLAMA_URL = "http://localhost:11434"
PROMPT = "Explain what a hash table is in 2 sentences."


def available_gb():
    """Current system available RAM in GB."""
    return psutil.virtual_memory().available / (1024 ** 3)


def wait_stable(target_readings=5, tolerance_gb=0.3, interval=1.0):
    """Wait until available RAM stabilizes (N consecutive readings within tolerance)."""
    readings = []
    for _ in range(30):  # max 30 seconds
        val = available_gb()
        readings.append(val)
        if len(readings) >= target_readings:
            recent = readings[-target_readings:]
            if max(recent) - min(recent) < tolerance_gb:
                return sum(recent) / len(recent)
        time.sleep(interval)
    # Return best estimate
    return sum(readings[-3:]) / 3


def unload_all():
    """Unload all Ollama models from VRAM."""
    for m in ["qwen3.5:35b", "qwen3.5:35b-a3b-nvfp4", "gemma4:26b"]:
        subprocess.run(["ollama", "stop", m], capture_output=True)


def measure_ollama(model, label):
    """Measure memory delta for an Ollama model."""
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"  {label} ({model})", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    # Unload and wait for baseline
    unload_all()
    print(f"  Waiting for memory to settle...", file=sys.stderr)
    time.sleep(3)
    baseline = wait_stable()
    print(f"  Baseline available: {baseline:.2f} GB", file=sys.stderr)

    # Load + warmup
    print(f"  Loading model...", file=sys.stderr)
    httpx.post(f"{OLLAMA_URL}/api/chat", json={
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "stream": False, "keep_alive": -1,
        "options": {"num_predict": 8}
    }, timeout=300)

    # Run real inference
    print(f"  Running inference...", file=sys.stderr)
    httpx.post(f"{OLLAMA_URL}/api/chat", json={
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "stream": False, "keep_alive": -1,
        "options": {"num_predict": 256, "num_ctx": 8192}
    }, timeout=300)

    # Measure after
    time.sleep(1)
    after = wait_stable(target_readings=3, tolerance_gb=0.5, interval=0.5)
    delta = baseline - after
    print(f"  After available:  {after:.2f} GB", file=sys.stderr)
    print(f"  Memory used:      {delta:.2f} GB", file=sys.stderr)
    return delta


def measure_mlx(model_path):
    """Measure memory delta for MLX native backend."""
    label = "Gemma 4 MLX"
    bench_dir = os.path.join(os.path.dirname(__file__), "qwen35-vs-gemma4")
    mlx_python = os.path.join(bench_dir, ".mlx-venv/bin/python")
    runner_script = os.path.join(bench_dir, "_mlx_runner.py")

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"  {label} ({model_path})", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    # Ensure clean baseline
    unload_all()
    print(f"  Waiting for memory to settle...", file=sys.stderr)
    time.sleep(3)
    baseline = wait_stable()
    print(f"  Baseline available: {baseline:.2f} GB", file=sys.stderr)

    # Boot MLX runner (loads model)
    print(f"  Booting MLX runner...", file=sys.stderr)
    proc = subprocess.Popen(
        [mlx_python, runner_script, model_path],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1
    )

    while True:
        line = proc.stdout.readline()
        if not line:
            break
        try:
            msg = json.loads(line)
            if msg.get("event") == "ready":
                break
        except json.JSONDecodeError:
            continue

    # Run inference
    print(f"  Running inference...", file=sys.stderr)
    req = json.dumps({"prompt": PROMPT, "max_tokens": 256})
    proc.stdin.write(req + "\n")
    proc.stdin.flush()

    while True:
        line = proc.stdout.readline()
        if not line:
            break
        try:
            msg = json.loads(line)
            if msg.get("event") == "result":
                break
        except json.JSONDecodeError:
            continue

    # Measure after (model still loaded in subprocess)
    time.sleep(1)
    after = wait_stable(target_readings=3, tolerance_gb=0.5, interval=0.5)
    delta = baseline - after

    print(f"  After available:  {after:.2f} GB", file=sys.stderr)
    print(f"  Memory used:      {delta:.2f} GB", file=sys.stderr)

    # Cleanup
    proc.stdin.write(json.dumps({"cmd": "exit"}) + "\n")
    proc.stdin.flush()
    proc.wait(timeout=10)

    return delta


def main():
    total_ram = psutil.virtual_memory().total / (1024 ** 3)
    print(f"System RAM: {total_ram:.0f} GB", file=sys.stderr)
    print(f"Measurement: system available RAM delta", file=sys.stderr)

    results = {}

    for model, label in [
        ("qwen3.5:35b", "Qwen 3.5 GGUF"),
        ("qwen3.5:35b-a3b-nvfp4", "Qwen 3.5 MLX-via-Ollama"),
        ("gemma4:26b", "Gemma 4 GGUF"),
    ]:
        delta = measure_ollama(model, label)
        results[label] = delta

    delta = measure_mlx("mlx-community/gemma-4-26b-a4b-it-4bit")
    results["Gemma 4 MLX"] = delta

    # Final cleanup
    unload_all()

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  Memory Consumption (system available RAM delta)", file=sys.stderr)
    print(f"  System: {total_ram:.0f} GB · Prompt: \"{PROMPT[:40]}...\"", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    for label, gb in results.items():
        print(f"  {label:25s}  {gb:.1f} GB", file=sys.stderr)


if __name__ == "__main__":
    main()

# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27"]
# ///
"""Test peak RSS measurement for all 4 backends.

Measures the actual process RSS during inference — same metric for both
Ollama (runner process) and MLX (subprocess). Apples-to-apples comparison.
"""

import json
import os
import subprocess
import sys
import threading
import time

import httpx


def get_rss_kb(pid):
    try:
        out = subprocess.check_output(["ps", "-o", "rss=", "-p", str(pid)], text=True)
        return int(out.strip())
    except Exception:
        return 0


class PeakRSSMonitor:
    def __init__(self, pid, interval=0.05):
        self.pid = pid
        self.interval = interval
        self.peak_kb = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._poll, daemon=True)

    def _poll(self):
        while not self._stop.is_set():
            rss = get_rss_kb(self.pid)
            if rss > self.peak_kb:
                self.peak_kb = rss
            self._stop.wait(self.interval)

    def start(self):
        self.peak_kb = get_rss_kb(self.pid)  # baseline
        self._thread.start()
        return self

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=2)
        return self.peak_kb / 1024 / 1024  # GB


def find_ollama_runner_pids():
    try:
        out = subprocess.check_output(["pgrep", "-f", "ollama runner"], text=True)
        return [int(p) for p in out.strip().split("\n") if p.strip()]
    except Exception:
        return []


def test_ollama(model, label):
    print(f"\n  {label}: warming up...", file=sys.stderr)
    httpx.post("http://localhost:11434/api/chat", json={
        "model": model, "messages": [{"role": "user", "content": "hi"}],
        "stream": False, "keep_alive": -1, "options": {"num_predict": 8}
    }, timeout=300)

    time.sleep(0.5)
    pids = find_ollama_runner_pids()
    if not pids:
        print(f"  {label}: no runner PID found", file=sys.stderr)
        return None

    pid = max(pids)
    print(f"  {label}: runner PID={pid}", file=sys.stderr)

    monitor = PeakRSSMonitor(pid).start()

    httpx.post("http://localhost:11434/api/chat", json={
        "model": model,
        "messages": [{"role": "user", "content": "Explain what a hash table is in 2 sentences."}],
        "stream": False, "keep_alive": -1,
        "options": {"num_predict": 256, "num_ctx": 8192}
    }, timeout=300)

    peak_gb = monitor.stop()
    print(f"  {label}: peak RSS = {peak_gb:.2f} GB", file=sys.stderr)
    return peak_gb


def test_mlx(model_path):
    bench_dir = os.path.join(os.path.dirname(__file__), "qwen35-vs-gemma4")
    mlx_python = os.path.join(bench_dir, ".mlx-venv/bin/python")
    runner_script = os.path.join(bench_dir, "_mlx_runner.py")

    print(f"\n  Gemma 4 MLX: booting runner...", file=sys.stderr)
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

    print(f"  Gemma 4 MLX: runner PID={proc.pid}", file=sys.stderr)
    monitor = PeakRSSMonitor(proc.pid).start()

    req = json.dumps({"prompt": "Explain what a hash table is in 2 sentences.", "max_tokens": 256})
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

    peak_gb = monitor.stop()

    proc.stdin.write(json.dumps({"cmd": "exit"}) + "\n")
    proc.stdin.flush()
    proc.wait(timeout=10)

    print(f"  Gemma 4 MLX: peak RSS = {peak_gb:.2f} GB", file=sys.stderr)
    return peak_gb


def main():
    results = {}

    print("Unloading all Ollama models...", file=sys.stderr)
    for m in ["qwen3.5:35b", "qwen3.5:35b-a3b-nvfp4", "gemma4:26b"]:
        subprocess.run(["ollama", "stop", m], capture_output=True)
    time.sleep(2)

    for model, label in [
        ("qwen3.5:35b", "Qwen 3.5 GGUF"),
        ("qwen3.5:35b-a3b-nvfp4", "Qwen 3.5 MLX-via-Ollama"),
        ("gemma4:26b", "Gemma 4 GGUF"),
    ]:
        peak = test_ollama(model, label)
        results[label] = peak
        subprocess.run(["ollama", "stop", model], capture_output=True)
        time.sleep(1)

    peak = test_mlx("mlx-community/gemma-4-26b-a4b-it-4bit")
    results["Gemma 4 MLX"] = peak

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"  Peak RSS During Inference (same metric)", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    for label, gb in results.items():
        if gb is not None:
            print(f"  {label:25s}  {gb:.2f} GB", file=sys.stderr)
        else:
            print(f"  {label:25s}  FAILED", file=sys.stderr)


if __name__ == "__main__":
    main()

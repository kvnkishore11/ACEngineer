"""Pi coding agent runner — invoke Pi with --mode json, parse structured metrics.

Wraps Pi's non-interactive mode to extract per-turn token usage, tool calls,
and response text from the agent_end JSON event.

Usage:
    from _pi_runner import run_pi_task, warmup_model, PiResult

    result = run_pi_task("qwen3.5:35b", "Create hello.py", cwd="/tmp/bench")
    print(result.wall_time_s, result.total_tokens, result.tool_calls)
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import dataclass, field


@dataclass
class PiResult:
    wall_time_s: float
    exit_code: int
    timed_out: bool
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    tool_calls: int = 0
    turns: int = 0
    response_text: str = ""
    stdout: str = ""
    stderr: str = ""
    turn_details: list[dict] = field(default_factory=list)
    tool_call_details: list[dict] = field(default_factory=list)


def _parse_agent_end(stdout: str) -> dict | None:
    """Find and parse the agent_end JSON event from Pi's stdout."""
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if obj.get("type") == "agent_end":
                return obj
        except json.JSONDecodeError:
            continue
    return None


def _extract_metrics(agent_end: dict | None) -> dict:
    """Extract token counts, tool calls, turns, and response text from agent_end."""
    if agent_end is None:
        return {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0,
            "tool_calls": 0,
            "turns": 0,
            "response_text": "",
            "turn_details": [],
            "tool_call_details": [],
        }

    messages = agent_end.get("messages", [])
    total_in = 0
    total_out = 0
    total_tok = 0
    tool_call_count = 0
    turn_count = 0
    response_text = ""
    turn_details: list[dict] = []
    tool_call_details: list[dict] = []

    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        turn_count += 1
        usage = msg.get("usage", {})
        inp = usage.get("input", 0)
        out = usage.get("output", 0)
        tok = usage.get("totalTokens", inp + out)
        total_in += inp
        total_out += out
        total_tok += tok

        # Determine action type for this turn
        action = "response"
        contents = msg.get("content", [])
        for c in contents:
            if c.get("type") == "toolCall":
                tool_call_count += 1
                action = f"toolUse:{c.get('name', '?')}"
                # Extract tool call details
                args = c.get("arguments", {})
                # Truncate large args (e.g., file content)
                truncated_args = {}
                for k, v in args.items():
                    if isinstance(v, str) and len(v) > 200:
                        truncated_args[k] = v[:200] + "..."
                    else:
                        truncated_args[k] = v
                tool_call_details.append({
                    "name": c.get("name", "unknown"),
                    "args": truncated_args,
                })
            elif c.get("type") == "text":
                response_text = c.get("text", "")

        turn_details.append({
            "turn": turn_count,
            "input": inp,
            "output": out,
            "action": action,
        })

    return {
        "total_input_tokens": total_in,
        "total_output_tokens": total_out,
        "total_tokens": total_tok,
        "tool_calls": tool_call_count,
        "turns": turn_count,
        "response_text": response_text,
        "turn_details": turn_details,
        "tool_call_details": tool_call_details,
    }


def run_pi_task(
    model: str,
    prompt: str,
    cwd: str,
    *,
    provider: str = "ollama",
    thinking: str = "high",
    timeout: int = 300,
) -> PiResult:
    """Invoke Pi in non-interactive JSON mode, parse agent_end event."""
    cmd = [
        "pi", "-p",
        "--mode", "json",
        "--provider", provider,
        "--model", model,
        "--thinking", thinking,
        "--no-extensions",
        "--no-skills",
        "--no-prompt-templates",
        "--no-session",
        prompt,
    ]

    wall_start = time.perf_counter()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
        wall_time = time.perf_counter() - wall_start

        agent_end = _parse_agent_end(result.stdout)
        metrics = _extract_metrics(agent_end)

        return PiResult(
            wall_time_s=round(wall_time, 3),
            exit_code=result.returncode,
            timed_out=False,
            stdout=result.stdout,
            stderr=result.stderr,
            **metrics,
        )
    except subprocess.TimeoutExpired:
        wall_time = time.perf_counter() - wall_start
        return PiResult(
            wall_time_s=round(wall_time, 3),
            exit_code=-1,
            timed_out=True,
        )


def warmup_model(model: str, provider: str = "ollama") -> None:
    """Quick Pi call to ensure model/provider are valid and the model is loaded."""
    print(f"  Warming up provider={provider} model={model}...", file=sys.stderr)
    cmd = [
        "pi", "-p",
        "--provider", provider,
        "--model", model,
        "--thinking", "off",
        "--no-extensions",
        "--no-skills",
        "--no-prompt-templates",
        "--no-session",
        "Say hi.",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"warmup timeout for provider={provider} model={model}")

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "pi warmup failed").strip()
        raise RuntimeError(f"warmup failed for provider={provider} model={model}: {detail}")

    print(f"  provider={provider} model={model} ready.", file=sys.stderr)

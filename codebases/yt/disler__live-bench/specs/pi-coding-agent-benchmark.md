# Plan: Pi Coding Agent Benchmark

## Task Description
Build a new live-bench benchmark called `pi-coding-agent` that systematically evaluates the Pi coding agent across 6 increasingly difficult coding tasks in isolated temp directories. Compare 3 models (Qwen 3.5 GGUF, Qwen 3.5 MLX, Gemma 4 GGUF) running through Pi's Ollama provider on both M4 Max and M5 Max hardware. Stream results to the live-bench dashboard in real time across 4 chart types (wall time, correctness score, total tokens, tool calls) — 8 chart instances total.

## Objective
When this plan is complete, running `just bench-pi-m4` on the M4 machine (or `bench-pi-m5` on M5) will execute 6 coding tasks × 3 models through the Pi agent, emit wall time / correctness score / token usage / tool call counts per task to the live-bench server, and display animated results on the dashboard at `/benchmark/pi-coding-agent`. Engineers watching the dashboard will see, in real time, how each model handles tasks from "Hello World" through "multi-file package with tests."

## Problem Statement
The existing benchmarks (qwen35-vs-gemma4, context-scaling) measure raw inference speed — prefill tok/s, decode tok/s, wall time. But engineers using local LLMs for **agentic coding** care about different questions:
- Does the model actually produce working code?
- How many reasoning cycles (turns) does it need?
- How token-efficient is it? (fewer tokens = faster + cheaper)
- How does performance degrade as task complexity increases?

No existing live-bench benchmark measures agent-level capabilities. The Pi coding agent (v0.66.1) is the perfect test harness — it supports file read/write, bash execution, thinking modes, and JSON output with full token/tool-call telemetry.

## Solution Approach
1. **6 tasks, T1–T6**, from trivial to hard, each with deterministic verification (run the code, check output / pytest exit code)
2. **3 models** available through Ollama's Pi provider: `qwen3.5:35b` (GGUF), `qwen3.5:35b-a3b-nvfp4` (MLX), `gemma4:26b` (GGUF)
3. **Isolated temp dirs** — each task × model gets a fresh `tempfile.mkdtemp()` with fixtures copied in, preventing cross-contamination
4. **Pi's `--mode json`** — parse the `agent_end` event to extract total tokens, tool calls, turns, and response text without any guesswork
5. **4 chart types × 2 hardware** = 8 chart instances, emitted via `live-bench emit/meta/complete` CLI
6. **CompletionTracker pattern** from qwen35-vs-gemma4 — marks a task group complete when all 3 models have reported

## Relevant Files
Use these files to complete the task:

**Existing patterns to follow:**
- `apps/benchmarks/qwen35-vs-gemma4/bench.py` — the main benchmark script pattern (CompletionTracker, emit/meta/complete flow, --hw/--smoke/--server args)
- `apps/benchmarks/qwen35-vs-gemma4/run_all.py` — thin CLI wrapper pattern
- `apps/benchmarks/qwen35-vs-gemma4/_harness.py` — warm-isolated harness (reuse `ollama_chat` for warmup only)
- `apps/benchmarks/mock-test/run.py` — simpler benchmark pattern for reference
- `benchmarks/qwen35-vs-gemma4.yaml` — YAML chart definition pattern (per-chart groups, YAML anchors)
- `benchmarks/context-scaling.yaml` — another YAML pattern for reference
- `justfile` — existing benchmark recipes to follow (bench-qg-*, bench-ctx-*)

**Reference from other repos (private sibling repo, not part of this codebase):**
- `pi-agent-playground-v2/bench/bench_pi.py` — Pi agent benchmark that inspired this work (run_pi function, task structure, clean_scratch pattern)

### New Files
- `benchmarks/pi-coding-agent.yaml` — benchmark YAML with 8 charts
- `apps/benchmarks/pi-coding-agent/bench.py` — main benchmark script
- `apps/benchmarks/pi-coding-agent/run_all.py` — thin --hw wrapper
- `apps/benchmarks/pi-coding-agent/_tasks.py` — task definitions + verification logic
- `apps/benchmarks/pi-coding-agent/_pi_runner.py` — Pi agent wrapper (subprocess + JSON parsing)
- `apps/benchmarks/pi-coding-agent/fixtures/data.csv` — fixture for T3 (CSV processing)
- `apps/benchmarks/pi-coding-agent/fixtures/sample.txt` — fixture for T5 (CLI tool)

**Files to modify:**
- `justfile` — add bench-pi-m4, bench-pi-m5, bench-pi-smoke-m4, bench-pi-smoke-m5, bench-pi-reset, bench-pi-kill recipes

## Implementation Phases

### Phase 1: Foundation
- Create the YAML benchmark definition (`benchmarks/pi-coding-agent.yaml`) with 4 chart types × 2 hardware = 8 charts
- Create fixture files (data.csv with deterministic values, sample.txt with known content)
- Create the Pi runner module (`_pi_runner.py`) that invokes Pi with `--mode json`, parses the `agent_end` event, and returns structured metrics
- Create the task definitions module (`_tasks.py`) with 6 tasks, each containing: prompt text, fixture requirements, verification function, scoring logic

### Phase 2: Core Implementation
- Build the main benchmark script (`bench.py`) following the CompletionTracker pattern
- Implement isolated temp dir creation + fixture copying per task
- Implement the model warmup step (quick Ollama call to pre-load weights)
- Implement the emit/meta/complete flow for all 4 chart types
- Build the thin `run_all.py` wrapper with --hw flag

### Phase 3: Integration & Polish
- Add justfile recipes for all benchmark operations
- Test with `--smoke` mode (1 task, 1 model)
- Validate YAML loads correctly and charts appear in the dashboard
- Verify metadata (task prompt + Pi's response) displays in modals

## Task Definitions

Each task has a concrete, multi-check verification pipeline. Every check is a binary pass/fail. The correctness score is `passed_checks / total_checks` — no fuzzy judgment.

### T1: Hello World (trivial)
**Prompt:** "Create a file called hello.py that prints exactly 'Hello, World!' and nothing else."
**Checks (3):**
| # | Check | How |
|---|-------|-----|
| 1 | `hello.py` exists | `os.path.isfile("hello.py")` |
| 2 | Compiles | `python -m py_compile hello.py` exits 0 |
| 3 | Correct output | `python hello.py` stdout stripped == `Hello, World!` |
**Score:** passed / 3

### T2: Pure Function (simple)
**Prompt:** "Create a file called fib.py that implements a function fibonacci(n) using memoization with a dictionary. The main block should print the result of fibonacci(10), which should be 55."
**Checks (3):**
| # | Check | How |
|---|-------|-----|
| 1 | `fib.py` exists | `os.path.isfile("fib.py")` |
| 2 | Compiles | `python -m py_compile fib.py` exits 0 |
| 3 | Correct output | `python fib.py` stdout stripped == `55` |
**Score:** passed / 3

### T3: File I/O + Processing (moderate)
**Prompt:** "Read the file data.csv which has columns 'name' and 'value'. Compute the mean of the 'value' column and print it rounded to 2 decimal places. Save your script as process.py."
**Fixture:** `data.csv` with 10 rows, known mean = 42.50
**Checks (4):**
| # | Check | How |
|---|-------|-----|
| 1 | `process.py` exists | `os.path.isfile("process.py")` |
| 2 | Compiles | `python -m py_compile process.py` exits 0 |
| 3 | Runs without error | `python process.py` exits 0 |
| 4 | Correct output | stdout stripped contains `42.5` (accepts `42.5` or `42.50`) |
**Score:** passed / 4

### T4: Data Structure + Tests (moderate-hard)

**What makes this harder than T3:** Two files that must work together. OOP with specific method contracts. Error handling (raising specific exceptions). Writing tests that verify both happy paths and edge cases.

**Prompt:**
```
Create two files: stack.py and test_stack.py.

## stack.py

Implement a `Stack` class with these exact methods:

- `push(item) -> None` — Add item to the top of the stack.
- `pop() -> Any` — Remove and return the top item. Raise `IndexError` with message "pop from empty stack" if empty.
- `peek() -> Any` — Return the top item without removing it. Raise `IndexError` with message "peek at empty stack" if empty.
- `is_empty() -> bool` — Return True if the stack has no items.
- `size() -> int` — Return the number of items in the stack.
- `to_list() -> list` — Return a list of all items, bottom to top.

The class should use a Python list internally. Include type hints on all methods.

## test_stack.py

Write pytest tests that cover:
1. Push a single item, verify size is 1 and peek returns it.
2. Push 3 items, pop all 3, verify they come back in LIFO order.
3. Pop from an empty stack raises IndexError.
4. Peek at an empty stack raises IndexError.
5. is_empty returns True on a new stack and False after a push.
6. to_list returns items in bottom-to-top order after pushing 1, 2, 3.
7. Size updates correctly after push and pop operations.

Run the tests to make sure they all pass.
```

**Checks (7):**
| # | Check | How |
|---|-------|-----|
| 1 | `stack.py` exists | `os.path.isfile("stack.py")` |
| 2 | `test_stack.py` exists | `os.path.isfile("test_stack.py")` |
| 3 | `stack.py` compiles | `python -m py_compile stack.py` exits 0 |
| 4 | Tests run (no import error) | `python -m pytest test_stack.py -q 2>&1` does NOT contain "ModuleNotFoundError" or "ImportError" |
| 5 | All tests pass | `python -m pytest test_stack.py -q` exits 0 |
| 6 | Pop error message correct | `python -c "from stack import Stack; s=Stack(); s.pop()"` stderr contains "pop from empty stack" |
| 7 | to_list works | `python -c "from stack import Stack; s=Stack(); s.push(1); s.push(2); s.push(3); print(s.to_list())"` stdout contains `[1, 2, 3]` |
**Score:** passed / 7

---

### T5: CLI Tool with Subcommands + Error Handling (hard)

**What makes this harder than T4:** Single-file but complex architecture. Four argparse subcommands with different signatures. Flag handling (`--ignore-case`, `-n`). Error handling with specific exit codes and messages. Formatted tabular output. Must work correctly against a provided fixture file.

**Prompt:**
```
Build a CLI tool at wordcount.py using argparse with four subcommands. The tool operates on text files.

## Subcommands

### count <file>
Print a single line: "N words" where N is the total number of whitespace-separated words in the file.

### freq <file> [-n/--top N]
Print the top N most frequent words (default N=5), one per line, formatted as:
  COUNT WORD
Sorted by count descending, then alphabetically for ties. Words should be lowercased before counting. Example output:
  12 the
   8 and
   5 python

### search <file> <word> [--ignore-case]
Print all lines from the file that contain the given word, prefixed with the 1-based line number:
  3: This line contains the word
  7: Another matching line
If --ignore-case is passed, match case-insensitively. Without the flag, match is case-sensitive.
Print "No matches found" if nothing matches.

### stats <file>
Print a summary with exactly these 4 lines:
  Lines: N
  Words: N
  Characters: N
  Unique words: N
Characters means total characters in the file including whitespace and newlines. Unique words are lowercased before counting.

## Error Handling
- If the file does not exist, print "Error: file not found: <filename>" to stderr and exit with code 1.
- If no subcommand is given, print the help message and exit with code 0.

## Important
- Use `argparse` with `add_subparsers` — not click, not sys.argv parsing.
- The file sample.txt is in the current directory. Do NOT modify sample.txt.
- Run each subcommand against sample.txt to verify your implementation works.
```

**Fixture:** `sample.txt` — 20 lines of text about programming, with deterministic properties:
- Total words: exactly 150
- Top word (lowercased): "the" appearing 12 times
- Lines containing "python" (case-sensitive): exactly 3
- Lines containing "Python" (case-insensitive): exactly 5
- Total unique words (lowercased): exactly 98
- Total characters (including newlines): exactly 892

**Checks (8):**
| # | Check | How |
|---|-------|-----|
| 1 | `wordcount.py` exists | `os.path.isfile("wordcount.py")` |
| 2 | Compiles | `python -m py_compile wordcount.py` exits 0 |
| 3 | `count` correct | `python wordcount.py count sample.txt` stdout contains `150` |
| 4 | `freq -n 1` correct | `python wordcount.py freq sample.txt -n 1` stdout contains `the` |
| 5 | `search` case-sensitive | `python wordcount.py search sample.txt python` stdout has exactly 3 non-empty lines |
| 6 | `search --ignore-case` | `python wordcount.py search sample.txt Python --ignore-case` stdout has exactly 5 non-empty lines |
| 7 | `stats` word count | `python wordcount.py stats sample.txt` stdout contains `Words: 150` |
| 8 | Missing file error | `python wordcount.py count nonexistent.txt 2>&1; echo $?` stderr contains "Error: file not found" AND exit code is 1 |
**Score:** passed / 8

---

### T6: Multi-File Package with Cross-Module Dependencies + Comprehensive Tests (hardest)

**What makes this harder than T5:** Multiple files across two directories that must import each other correctly. Cross-module state (history tracks operations from ops). A decorator pattern (`@traced`). Package `__init__.py` re-exports. A `__main__.py` CLI entry point. Comprehensive pytest suite that tests the integrated system, not just individual functions. Tests must exercise cross-module behavior (calling ops functions and verifying history captures them).

**Prompt:**
```
Create a Python package called `calculator` with full test coverage.

## Package Structure

```
calculator/
  __init__.py
  ops.py
  history.py
  __main__.py
tests/
  __init__.py
  test_ops.py
  test_history.py
  test_integration.py
```

## calculator/ops.py

Implement these pure functions:

- `add(a: float, b: float) -> float`
- `subtract(a: float, b: float) -> float`
- `multiply(a: float, b: float) -> float`
- `divide(a: float, b: float) -> float` — Raise `ValueError` with message "division by zero" if b is 0.
- `power(base: float, exp: float) -> float` — Use `**` operator.
- `modulo(a: float, b: float) -> float` — Raise `ValueError` with message "modulo by zero" if b is 0.

All functions must raise `TypeError` with message "operands must be numeric" if either argument is not an int or float.

## calculator/history.py

Implement `HistoryLog` class:

- `__init__()` — Initialize with an empty log.
- `record(operation: str, a: float, b: float, result: float) -> None` — Append an entry dict: `{"operation": operation, "a": a, "b": b, "result": result}`.
- `get_entries() -> list[dict]` — Return a copy of all entries.
- `last(n: int = 1) -> list[dict]` — Return the last N entries (most recent last). Return empty list if no entries.
- `clear() -> None` — Remove all entries.
- `count() -> int` — Return total number of entries.
- `filter_by_op(operation: str) -> list[dict]` — Return entries matching the given operation name.

Implement a module-level `traced` decorator:

```python
def traced(log: HistoryLog):
    """Decorator factory that records every call to the wrapped function in the given log."""
```

When `@traced(log)` is applied to an ops function like `add`, every call to `add(2, 3)` should automatically call `log.record("add", 2, 3, 5)` using the function's `__name__` as the operation.

## calculator/__init__.py

Re-export all six ops functions and the HistoryLog class:
```python
from .ops import add, subtract, multiply, divide, power, modulo
from .history import HistoryLog, traced
```

## calculator/__main__.py

Entry point for `python -m calculator`. Parse command line args:
```
python -m calculator <op> <a> <b>
```
Where `<op>` is one of: add, subtract, multiply, divide, power, modulo.
Print the result as a single number. On error, print the error message to stderr and exit with code 1.

## Tests

### tests/test_ops.py
- Test all 6 operations with basic inputs (e.g., add(2, 3) == 5).
- Test divide(10, 0) raises ValueError with "division by zero".
- Test modulo(10, 0) raises ValueError with "modulo by zero".
- Test add("a", 1) raises TypeError with "operands must be numeric".

### tests/test_history.py
- Test record and get_entries returns copies (mutating returned list doesn't affect log).
- Test last(2) returns the 2 most recent entries.
- Test clear empties the log.
- Test filter_by_op returns only matching operations.
- Test count reflects the number of recorded entries.

### tests/test_integration.py
- Create a HistoryLog, wrap add and multiply with @traced(log), call add(2, 3) and multiply(4, 5), verify log has 2 entries with correct operation names and results.
- Verify the traced decorator preserves the function's behavior (add(2, 3) still returns 5).
- Test the full cycle: create log, trace ops, perform calculations, filter by op, verify counts.

## Requirements
- All tests must pass when run with: `python -m pytest tests/ -q`
- No external dependencies — stdlib only.
- Type hints on all function signatures.

Run the tests to verify everything passes.
```

**Checks (10):**
| # | Check | How |
|---|-------|-----|
| 1 | `calculator/__init__.py` exists | `os.path.isfile(...)` |
| 2 | `calculator/ops.py` exists | `os.path.isfile(...)` |
| 3 | `calculator/history.py` exists | `os.path.isfile(...)` |
| 4 | `calculator/__main__.py` exists | `os.path.isfile(...)` |
| 5 | `tests/test_ops.py` exists | `os.path.isfile(...)` |
| 6 | `tests/test_integration.py` exists | `os.path.isfile(...)` |
| 7 | Package imports | `python -c "from calculator import add, subtract, multiply, divide, power, modulo, HistoryLog, traced"` exits 0 |
| 8 | CLI works | `python -m calculator add 2 3` stdout stripped == `5.0` or `5` |
| 9 | TypeError raised | `python -c "from calculator import add; add('a', 1)"` exits non-zero and stderr contains "operands must be numeric" |
| 10 | All tests pass | `python -m pytest tests/ -q` exits 0 |
**Score:** passed / 10

## Pi Runner Details (`_pi_runner.py`)

The runner wraps Pi invocation and extracts structured metrics from JSON output:

```python
def run_pi_task(model: str, prompt: str, cwd: str, timeout: int = 300) -> PiResult:
    """Invoke Pi in non-interactive JSON mode, parse agent_end event."""
    cmd = [
        "pi", "-p",
        "--mode", "json",
        "--provider", "ollama",
        "--model", model,
        "--thinking", "high",
        "--no-extensions",
        "--no-skills",
        "--no-prompt-templates",
        "--no-session",
        prompt,
    ]

    wall_start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True,
                            timeout=timeout, cwd=cwd)
    wall_time = time.perf_counter() - wall_start

    # Parse the agent_end JSON line from stdout
    agent_end = parse_agent_end(result.stdout)

    return PiResult(
        wall_time_s=wall_time,
        exit_code=result.returncode,
        timed_out=False,
        total_input_tokens=sum_tokens(agent_end, "input"),
        total_output_tokens=sum_tokens(agent_end, "output"),
        total_tokens=sum_tokens(agent_end, "totalTokens"),
        tool_calls=count_tool_calls(agent_end),
        turns=count_turns(agent_end),
        response_text=extract_final_text(agent_end),
        stdout=result.stdout,
        stderr=result.stderr,
    )
```

The `agent_end` event (last JSON line) contains a `messages` array. Each assistant message has:
- `usage.input` — input token count for that turn
- `usage.output` — output token count for that turn
- `usage.totalTokens` — total for that turn
- `content[]` with `type: "toolCall"` entries — count these for tool calls
- `content[]` with `type: "text"` — the response text

## Chart Design

### YAML Structure (`benchmarks/pi-coding-agent.yaml`)

```yaml
version: 1
benchmark:
  session_id: pi-coding-agent
  title: "Pi Coding Agent — Task Completion"
  subtitle: "Qwen 3.5 vs Gemma 4 · GGUF vs MLX · 6 Coding Tasks · M4 Max vs M5 Max"
  charts:
    # ── Wall Time ──
    - chart_id: wall_m4
      title: "Wall-Clock Time (M4 Max)"
      subtitle: "end-to-end agent execution · seconds · lower is better"
      better: lower
      direction: BT
      x: { label: "Task" }
      y: { label: "Time", unit: "s", min: 0 }
      groups: &task_groups
        - { key: t1, label: "T1 Hello" }
        - { key: t2, label: "T2 Fibonacci" }
        - { key: t3, label: "T3 CSV" }
        - { key: t4, label: "T4 Stack+Tests" }
        - { key: t5, label: "T5 CLI Tool" }
        - { key: t6, label: "T6 Package" }
      metrics: &model_metrics
        - { key: qwen_gguf,   label: "Qwen 3.5 GGUF",  color: "#f59e0b" }
        - { key: qwen_mlx,    label: "Qwen 3.5 MLX",   color: "#fbbf24" }
        - { key: gemma4_gguf,  label: "Gemma 4 GGUF",   color: "#3b82f6" }
    - chart_id: wall_m5
      ...same structure with title "Wall-Clock Time (M5 Max)"...

    # ── Correctness Score ──
    # Score = passed_checks / total_checks per task (concrete, not fuzzy)
    # T1: 3 checks, T2: 3, T3: 4, T4: 5, T5: 5, T6: 6
    - chart_id: score_m4
      title: "Correctness (M4 Max)"
      subtitle: "verification checks passed / total · higher is better"
      better: higher
      direction: BT
      x: { label: "Task" }
      y: { label: "Pass Rate", unit: "", min: 0, max: 1 }
      groups: *task_groups
      metrics: *model_metrics
    - chart_id: score_m5
      ...same with title "Correctness (M5 Max)"...

    # ── Total Tokens ──
    - chart_id: tokens_m4
      title: "Total Tokens (M4 Max)"
      subtitle: "input + output tokens across all turns · lower is better"
      better: lower
      direction: BT
      x: { label: "Task" }
      y: { label: "Tokens", unit: "", min: 0 }
      groups: *task_groups
      metrics: *model_metrics
    - chart_id: tokens_m5
      ...same...

    # ── Tool Calls ──
    - chart_id: tools_m4
      title: "Tool Calls (M4 Max)"
      subtitle: "number of tool invocations · lower is better"
      better: lower
      direction: BT
      x: { label: "Task" }
      y: { label: "Calls", unit: "", min: 0 }
      groups: *task_groups
      metrics: *model_metrics
    - chart_id: tools_m5
      ...same...
```

### Charts Summary

| Chart ID | Metric | Unit | Direction | What it shows |
|----------|--------|------|-----------|---------------|
| `wall_{hw}` | Wall-Clock Time | seconds | lower is better | How fast can each model complete coding tasks? |
| `score_{hw}` | Correctness | passed/total (0.0-1.0) | higher is better | Does the generated code pass all verification checks? |
| `tokens_{hw}` | Total Tokens | count | lower is better | How token-efficient is each model? |
| `tools_{hw}` | Tool Calls | count | lower is better | How many tool invocations needed? |

**Correctness scoring is concrete, not fuzzy.** Each task defines N binary checks (file exists, compiles, runs, correct output, tests pass). Score = passed / N. The metadata modal shows exactly which checks passed/failed for each model.

## Benchmark Execution Flow

For each model (sequential to avoid model loading conflicts):
1. **Warmup** — Quick Ollama API call to ensure model is loaded (`keep_alive=-1`)
2. **For each task T1-T6:**
   a. Create fresh temp dir with `tempfile.mkdtemp(prefix="pi-bench-")`
   b. Copy any required fixtures into the temp dir
   c. Invoke Pi via `_pi_runner.run_pi_task(model, prompt, cwd=temp_dir)`
   d. Run verification function to compute correctness score
   e. Emit results to all 4 chart types via `live-bench emit`
   f. Emit metadata (task prompt + Pi's response) via `live-bench meta`
   g. CompletionTracker checks if all 3 models have reported for this task
   h. Clean up temp dir
3. **Unload model** — `ollama stop <model>` before loading next

## Justfile Recipes

```just
# ── pi-coding-agent benchmark ────────────────────────────────────
# Pi coding agent: 6 tasks × 3 models, 4 chart types × M4/M5.
# Measures wall time, correctness, token efficiency, and tool calls.

bench-pi-m4 *FLAGS: bench-pi-kill
    uv run apps/benchmarks/pi-coding-agent/bench.py --hw m4 {{FLAGS}}

bench-pi-m5 *FLAGS: bench-pi-kill
    uv run apps/benchmarks/pi-coding-agent/bench.py --hw m5 {{FLAGS}}

bench-pi-smoke-m4: bench-pi-kill
    uv run apps/benchmarks/pi-coding-agent/bench.py --hw m4 --smoke

bench-pi-smoke-m5: bench-pi-kill
    uv run apps/benchmarks/pi-coding-agent/bench.py --hw m5 --smoke

bench-pi-kill:
    #!/usr/bin/env bash
    set -uo pipefail
    echo "Killing pi-coding-agent benchmark processes..."
    pkill -f "pi-coding-agent/bench.py" 2>/dev/null || true
    pkill -f "pi -p.*--provider ollama" 2>/dev/null || true
    echo "done"

bench-pi-reset:
    live-bench reset pi-coding-agent --yes
```

## Fixture Data

### `data.csv` (for T3)
```csv
name,value
alpha,35.0
beta,52.5
gamma,28.0
delta,41.5
epsilon,63.0
zeta,19.5
eta,47.0
theta,55.5
iota,31.0
kappa,52.0
```
Mean of value column = (35.0+52.5+28.0+41.5+63.0+19.5+47.0+55.5+31.0+52.0) / 10 = 425.0 / 10 = **42.50**

### `sample.txt` (for T5)
A 20-line text file with exactly **150 words**, where:
- The word "the" appears exactly **12 times** (most frequent)
- The word "python" appears in exactly **3 lines**
- Content is about programming concepts (relevant, not lorem ipsum)

## Metadata for Modals (Per-Chart)

Each chart gets its own metadata tailored to what that chart measures. All 4 charts share the `prompt` field, but the rest is chart-specific. Metadata is emitted via `live-bench meta` per chart, and deep-merges across model runs (so each model's data accumulates under the same group).

### `wall_{hw}` — Wall-Clock Time
What the engineer wants to see: the task prompt, Pi's response, and timing context.
```json
{
  "prompt": "<task prompt text>",
  "responses": {
    "qwen_gguf": "<Pi's final response text (first 4000 chars)>"
  },
  "wall_time": {
    "qwen_gguf": { "seconds": 23.4, "timed_out": false }
  }
}
```

### `score_{hw}` — Correctness Score
What the engineer wants to see: what passed, what failed, why that score.
```json
{
  "prompt": "<task prompt text>",
  "verification": {
    "qwen_gguf": {
      "score": 1.0,
      "detail": "all 3 pytest tests passed",
      "checks": [
        { "name": "file_exists", "passed": true },
        { "name": "runs_without_error", "passed": true },
        { "name": "correct_output", "passed": true }
      ]
    }
  }
}
```

### `tokens_{hw}` — Total Tokens
What the engineer wants to see: token breakdown per turn, input vs output efficiency.
```json
{
  "prompt": "<task prompt text>",
  "token_breakdown": {
    "qwen_gguf": {
      "total": 3314,
      "input": 3174,
      "output": 140,
      "turns": [
        { "turn": 1, "input": 1534, "output": 82, "action": "toolUse:write" },
        { "turn": 2, "input": 1640, "output": 58, "action": "response" }
      ]
    }
  }
}
```

### `tools_{hw}` — Tool Calls
What the engineer wants to see: which tools were used, in what order, with what arguments.
```json
{
  "prompt": "<task prompt text>",
  "tool_calls": {
    "qwen_gguf": [
      { "name": "write", "args": { "path": "hello.py" } },
      { "name": "bash", "args": { "command": "python hello.py" } }
    ]
  }
}
```

### Implementation in CompletionTracker

The `emit_and_track` method emits metadata to ALL 4 charts, not just one:

```python
def emit_and_track(self, task_key, metric_key, pi_result, score, score_detail, score_checks):
    hw, server = self._hw, self._server

    # 1. Emit numeric values to each chart
    for chart, value in [
        ("wall",   pi_result.wall_time_s),
        ("score",  score),
        ("tokens", pi_result.total_tokens),
        ("tools",  pi_result.tool_calls),
    ]:
        subprocess.run(["live-bench", "--server", server, "emit", SESSION,
                        "--chart", f"{chart}_{hw}", "--group", task_key,
                        "--metric", metric_key, "--value", str(round(value, 2))],
                       check=True)

    # 2. Emit per-chart metadata
    prompt_text = self._prompts.get(task_key, "")

    # wall chart: prompt + response + timing
    _emit_meta(server, f"wall_{hw}", task_key, {
        "prompt": prompt_text,
        "responses": {metric_key: pi_result.response_text[:4000]},
        "wall_time": {metric_key: {
            "seconds": round(pi_result.wall_time_s, 1),
            "timed_out": pi_result.timed_out,
        }},
    })

    # score chart: prompt + verification details
    _emit_meta(server, f"score_{hw}", task_key, {
        "prompt": prompt_text,
        "verification": {metric_key: {
            "score": score,
            "detail": score_detail,
            "checks": score_checks,
        }},
    })

    # tokens chart: prompt + per-turn token breakdown
    _emit_meta(server, f"tokens_{hw}", task_key, {
        "prompt": prompt_text,
        "token_breakdown": {metric_key: {
            "total": pi_result.total_tokens,
            "input": pi_result.total_input_tokens,
            "output": pi_result.total_output_tokens,
            "turns": pi_result.turn_details,  # list of {turn, input, output, action}
        }},
    })

    # tools chart: prompt + tool call sequence
    _emit_meta(server, f"tools_{hw}", task_key, {
        "prompt": prompt_text,
        "tool_calls": {metric_key: pi_result.tool_call_details},  # list of {name, args}
    })

    # 3. Track completion
    ...
```
```

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to to the building, validating, testing, deploying, and other tasks.
  - This is critical. You're job is to act as a high level director of the team, not a builder.
  - You're role is to validate all work is going well and make sure the team is on track to complete the plan.
  - You'll orchestrate this by using the Task* Tools to manage coordination between the team members.
  - Communication is paramount. You'll use the Task* Tools to communicate with the team members and ensure they're on track to complete the plan.
- Take note of the session id of each team member. This is how you'll reference them.

### Team Members

- Builder
  - Name: builder-yaml-fixtures
  - Role: Create the benchmark YAML definition and fixture files (data.csv, sample.txt)
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-pi-runner
  - Role: Build the Pi runner module (_pi_runner.py) that invokes Pi with --mode json and parses the agent_end event for structured metrics
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-tasks
  - Role: Build the task definitions module (_tasks.py) with all 6 task prompts, fixture requirements, and verification/scoring logic
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-bench
  - Role: Build the main bench.py script with CompletionTracker, run_all.py wrapper, and justfile recipes
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: validator
  - Role: Run smoke test, verify YAML loads, verify Pi runner parses correctly, check dashboard renders
  - Agent Type: general-purpose
  - Resume: false

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

### 1. Create Benchmark YAML + Fixtures
- **Task ID**: create-yaml-fixtures
- **Depends On**: none
- **Assigned To**: builder-yaml-fixtures
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 2 and 3)
- Create `benchmarks/pi-coding-agent.yaml` with 8 charts (4 types × 2 hardware) using YAML anchors for `&task_groups` and `&model_metrics`
- Create `apps/benchmarks/pi-coding-agent/fixtures/data.csv` with the 10-row dataset (mean = 42.50)
- Create `apps/benchmarks/pi-coding-agent/fixtures/sample.txt` with exactly 150 words, "the" appearing 12 times, "python" on exactly 3 lines
- Verify: `python -c "import yaml; yaml.safe_load(open('benchmarks/pi-coding-agent.yaml'))"` succeeds

### 2. Build Pi Runner Module
- **Task ID**: build-pi-runner
- **Depends On**: none
- **Assigned To**: builder-pi-runner
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 1 and 3)
- Create `apps/benchmarks/pi-coding-agent/_pi_runner.py` as a PEP 723 single-file script (no external deps needed — just stdlib json + subprocess + time)
- Implement `PiResult` dataclass with fields: `wall_time_s`, `exit_code`, `timed_out`, `total_input_tokens`, `total_output_tokens`, `total_tokens`, `tool_calls`, `turns`, `response_text`, `stdout`, `stderr`, `turn_details` (list of dicts: `{turn, input, output, action}`), `tool_call_details` (list of dicts: `{name, args}`)
- Implement `run_pi_task(model, prompt, cwd, timeout=300)` that:
  - Invokes `pi -p --mode json --provider ollama --model <model> --thinking high --no-extensions --no-skills --no-prompt-templates --no-session "<prompt>"`
  - Measures wall time via `time.perf_counter()`
  - Parses stdout for the `agent_end` JSON line (last line with `"type":"agent_end"`)
  - Extracts token counts by summing `usage` from each assistant message in the `messages` array
  - Counts tool calls from `content[]` entries with `"type":"toolCall"`
  - Counts turns as number of assistant messages
  - Extracts final response text from the last assistant message's `content[]` `"type":"text"` entry
  - Handles timeout via `subprocess.TimeoutExpired` → returns PiResult with `timed_out=True`, `wall_time_s=timeout`, all counters at 0
- Implement `warmup_model(model)` that does a quick `ollama_chat` or `pi -p --no-session "Say hi"` to ensure model is loaded

### 3. Build Task Definitions Module
- **Task ID**: build-tasks
- **Depends On**: none
- **Assigned To**: builder-tasks
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 1 and 2)
- Create `apps/benchmarks/pi-coding-agent/_tasks.py`
- Define a `Task` dataclass: `key`, `label`, `prompt`, `fixtures` (list of fixture filenames to copy), `verify` (callable that takes temp dir path, returns score 0.0-1.0 + detail string)
- Implement the `TASKS` list with all 6 tasks (T1-T6) as defined in the Task Definitions section above
- Each verify function:
  - Runs the appropriate command (`python <file>`, `python -m pytest <file> -q`) via subprocess
  - Checks output against expected values
  - Returns a tuple of `(score: float, detail: str)` where score is 0.0-1.0
  - Handles missing files, runtime errors, wrong output gracefully
- Implement `setup_task_dir(task, bench_dir)` that creates a temp dir and copies required fixtures
- Implement `cleanup_task_dir(path)` that removes the temp dir

### 4. Build Main Benchmark Script + Wrapper + Justfile
- **Task ID**: build-bench-script
- **Depends On**: create-yaml-fixtures, build-pi-runner, build-tasks
- **Assigned To**: builder-bench
- **Agent Type**: general-purpose
- **Parallel**: false (depends on 1, 2, 3)
- Create `apps/benchmarks/pi-coding-agent/bench.py` as a PEP 723 single-file script with dependency on `httpx>=0.27`
  - Follow the pattern from `apps/benchmarks/qwen35-vs-gemma4/bench.py`
  - `--hw m4|m5`, `--smoke`, `--server`, `--iterations` (default 1) arguments
  - `--smoke` mode: run only T1 with only the first model
  - Define 3 models: `MODELS = [qwen_gguf, qwen_mlx, gemma4_gguf]` with model IDs, metric keys, labels
  - Implement `CompletionTracker` that:
    - Emits to 4 chart types (`wall_{hw}`, `score_{hw}`, `tokens_{hw}`, `tools_{hw}`)
    - Emits metadata to `wall_{hw}` chart (prompt + response per model)
    - Marks task complete when all 3 models have reported
  - For each model (sequential):
    1. Warmup: call `warmup_model(model)` to preload into Ollama
    2. For each task:
       - `setup_task_dir(task)` → temp dir
       - `run_pi_task(model, prompt, cwd=temp_dir)` → PiResult
       - `verify(temp_dir)` → score + detail
       - `tracker.emit_and_track(task_key, metric_key, result, score, detail)`
       - `cleanup_task_dir(temp_dir)`
    3. Unload: `ollama stop <model>`
- Create `apps/benchmarks/pi-coding-agent/run_all.py` as a thin wrapper (same pattern as qwen35-vs-gemma4 `run_all.py`)
- Add justfile recipes: `bench-pi-m4`, `bench-pi-m5`, `bench-pi-smoke-m4`, `bench-pi-smoke-m5`, `bench-pi-kill`, `bench-pi-reset`

### 5. Validate Everything
- **Task ID**: validate-all
- **Depends On**: build-bench-script
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Start the backend + frontend if not running (`just serve` or `just _ensure-server`)
- Run `just bench-pi-smoke-m4` (or m5 depending on hardware) to verify:
  - YAML loads without errors
  - Pi agent invocation works
  - JSON parsing extracts metrics correctly
  - Verification scoring works
  - Results appear in the dashboard
  - Metadata modal shows prompt + response
- Check that all 8 charts exist at `/benchmark/pi-coding-agent`
- Verify the smoke test emits to wall, score, tokens, and tools charts
- Check logs for any errors

## Acceptance Criteria
- [ ] `benchmarks/pi-coding-agent.yaml` defines 8 charts with correct groups, metrics, directions
- [ ] `just bench-pi-smoke-m4` completes without errors (runs T1 with 1 model, emits to all 4 chart types)
- [ ] Each of the 6 tasks has a deterministic verification that can be run independently
- [ ] Pi's JSON output is correctly parsed for token counts, tool calls, and turns
- [ ] Temp dirs are created fresh and cleaned up after each task
- [ ] CompletionTracker marks groups complete only when all 3 models have reported
- [ ] Metadata modal shows task prompt and each model's response text
- [ ] All justfile recipes work: bench-pi-m4, bench-pi-m5, bench-pi-smoke-*, bench-pi-kill, bench-pi-reset
- [ ] `just test-backend` still passes (no regressions)
- [ ] The dashboard at `/benchmark/pi-coding-agent` renders all 8 charts

## Validation Commands
Execute these commands to validate the task is complete:

- `python -c "import yaml; d=yaml.safe_load(open('benchmarks/pi-coding-agent.yaml')); print(len(d['benchmark']['charts']), 'charts')"` — Should print "8 charts"
- `uv run python -m py_compile apps/benchmarks/pi-coding-agent/bench.py` — Benchmark script compiles
- `uv run python -m py_compile apps/benchmarks/pi-coding-agent/_pi_runner.py` — Pi runner compiles
- `uv run python -m py_compile apps/benchmarks/pi-coding-agent/_tasks.py` — Tasks module compiles
- `just bench-pi-smoke-m4` — Smoke test completes without errors (requires Ollama running with qwen3.5:35b)
- `just test-backend` — No regressions in existing tests
- `just bench-pi-kill` — Kill recipe works without errors

## Notes
- **Pi version**: v0.66.1. The `--mode json` flag emits newline-delimited JSON events to stdout, with `agent_end` as the final event containing the full message history and per-turn token usage.
- **Model availability**: All 3 models (`qwen3.5:35b`, `qwen3.5:35b-a3b-nvfp4`, `gemma4:26b`) must be pulled into Ollama before benchmarking. The benchmark script should check this and warn if a model is missing.
- **Timeout**: 300 seconds per task. Previous benchmarks showed that package + tests tasks (similar to T6) can timeout. If a task times out, emit `wall_time=300`, `score=0`, `tokens=0`, `tools=0`.
- **Thinking mode**: All Pi invocations use `--thinking high` for maximum reasoning capability, matching the pi-agent-playground-v2 methodology.
- **No warmup iterations needed**: Unlike raw inference benchmarks, each Pi task is a complete fresh session. The warmup step just ensures the Ollama model is loaded into VRAM.
- **pytest availability**: Tasks T4 and T6 require pytest. The benchmark should install pytest in each temp dir's environment OR rely on the system python having pytest. Since Pi uses `bash` tool to run commands, Pi itself may install pytest if needed. However, the verification step (run by our script, not Pi) needs pytest available. Ensure `uv run python -m pytest` works from the benchmark script.
- **Fixture file paths**: When Pi runs in the temp dir, it sees `data.csv` and `sample.txt` at the root of its working directory. The prompt should reference them by name, not path.

## Report

**Benchmark**: pi-coding-agent
**Charts**: 8 (wall_m4, wall_m5, score_m4, score_m5, tokens_m4, tokens_m5, tools_m4, tools_m5)
**Tasks**: 6 (T1 Hello → T6 Package+Tests)
**Models**: 3 (Qwen GGUF, Qwen MLX, Gemma 4 GGUF)
**Key insight**: First live-bench benchmark measuring agent-level capabilities — not just speed, but whether the code actually works.

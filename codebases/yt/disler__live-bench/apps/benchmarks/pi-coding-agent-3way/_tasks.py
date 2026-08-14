"""Task definitions for the Pi coding agent benchmark.

Each task has a prompt, optional fixture files, and a verify() function that
returns (score, detail, checks) where:
  - score: float 0.0-1.0 = passed_checks / total_checks
  - detail: human-readable summary
  - checks: list of {"name": str, "passed": bool}
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

# ── Exact fixture properties (computed from fixtures/sample.txt) ──
SAMPLE_WORD_COUNT = 228
SAMPLE_LINE_COUNT = 20
SAMPLE_CHAR_COUNT = 1545
SAMPLE_UNIQUE_WORDS = 163
SAMPLE_TOP_WORD = "the"
SAMPLE_THE_COUNT = 13
SAMPLE_PYTHON_CS_LINES = 3   # lines containing "python" (case-sensitive)
SAMPLE_PYTHON_CI_LINES = 5   # lines containing "python" (case-insensitive)

VerifyResult = tuple[float, str, list[dict]]


@dataclass
class Task:
    key: str
    label: str
    prompt: str
    fixtures: list[str]
    verify: Callable[[str], VerifyResult]


def _run(cmd: str, cwd: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """Run a shell command in cwd, capturing output."""
    return subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        timeout=timeout, cwd=cwd,
    )


def _check(name: str, passed: bool, checks: list[dict]) -> bool:
    checks.append({"name": name, "passed": passed})
    return passed


# ── T1: Hello World ──────────────────────────────────────────────

T1_PROMPT = "Create a file called hello.py that prints exactly 'Hello, World!' and nothing else."


def verify_t1(cwd: str) -> VerifyResult:
    checks: list[dict] = []
    _check("hello.py exists", os.path.isfile(os.path.join(cwd, "hello.py")), checks)
    try:
        r = _run("python -m py_compile hello.py", cwd)
        _check("compiles", r.returncode == 0, checks)
    except Exception:
        _check("compiles", False, checks)
    try:
        r = _run("python hello.py", cwd)
        _check("correct output", r.stdout.strip() == "Hello, World!", checks)
    except Exception:
        _check("correct output", False, checks)

    passed = sum(1 for c in checks if c["passed"])
    return passed / len(checks), f"{passed}/{len(checks)} checks passed", checks


# ── T2: Fibonacci ────────────────────────────────────────────────

T2_PROMPT = (
    "Create a file called fib.py that implements a function fibonacci(n) "
    "using memoization with a dictionary. The main block should print the "
    "result of fibonacci(10), which should be 55."
)


def verify_t2(cwd: str) -> VerifyResult:
    checks: list[dict] = []
    _check("fib.py exists", os.path.isfile(os.path.join(cwd, "fib.py")), checks)
    try:
        r = _run("python -m py_compile fib.py", cwd)
        _check("compiles", r.returncode == 0, checks)
    except Exception:
        _check("compiles", False, checks)
    try:
        r = _run("python fib.py", cwd)
        _check("correct output", r.stdout.strip() == "55", checks)
    except Exception:
        _check("correct output", False, checks)

    passed = sum(1 for c in checks if c["passed"])
    return passed / len(checks), f"{passed}/{len(checks)} checks passed", checks


# ── T3: CSV Processing ──────────────────────────────────────────

T3_PROMPT = (
    "Read the file data.csv which has columns 'name' and 'value'. "
    "Compute the mean of the 'value' column and print it rounded to "
    "2 decimal places. Save your script as process.py."
)


def verify_t3(cwd: str) -> VerifyResult:
    checks: list[dict] = []
    _check("process.py exists", os.path.isfile(os.path.join(cwd, "process.py")), checks)
    try:
        r = _run("python -m py_compile process.py", cwd)
        _check("compiles", r.returncode == 0, checks)
    except Exception:
        _check("compiles", False, checks)
    try:
        r = _run("python process.py", cwd)
        _check("runs without error", r.returncode == 0, checks)
        out = r.stdout.strip()
        _check("correct output", "42.5" in out, checks)
    except Exception:
        _check("runs without error", False, checks)
        _check("correct output", False, checks)

    passed = sum(1 for c in checks if c["passed"])
    return passed / len(checks), f"{passed}/{len(checks)} checks passed", checks


# ── T4: Data Structure + Tests ───────────────────────────────────

T4_PROMPT = """Create two files: stack.py and test_stack.py.

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

Run the tests to make sure they all pass."""


def verify_t4(cwd: str) -> VerifyResult:
    checks: list[dict] = []
    _check("stack.py exists", os.path.isfile(os.path.join(cwd, "stack.py")), checks)
    _check("test_stack.py exists", os.path.isfile(os.path.join(cwd, "test_stack.py")), checks)

    try:
        r = _run("python -m py_compile stack.py", cwd)
        _check("stack.py compiles", r.returncode == 0, checks)
    except Exception:
        _check("stack.py compiles", False, checks)

    try:
        r = _run("python -m pytest test_stack.py -q 2>&1", cwd, timeout=60)
        output = r.stdout + r.stderr
        no_import_err = "ModuleNotFoundError" not in output and "ImportError" not in output
        _check("tests run (no import error)", no_import_err, checks)
        _check("all tests pass", r.returncode == 0, checks)
    except Exception:
        _check("tests run (no import error)", False, checks)
        _check("all tests pass", False, checks)

    try:
        r = _run('python -c "from stack import Stack; s=Stack(); s.pop()"', cwd)
        _check("pop error message correct", "pop from empty stack" in r.stderr, checks)
    except Exception:
        _check("pop error message correct", False, checks)

    try:
        r = _run('python -c "from stack import Stack; s=Stack(); s.push(1); s.push(2); s.push(3); print(s.to_list())"', cwd)
        _check("to_list works", "[1, 2, 3]" in r.stdout, checks)
    except Exception:
        _check("to_list works", False, checks)

    passed = sum(1 for c in checks if c["passed"])
    return passed / len(checks), f"{passed}/{len(checks)} checks passed", checks


# ── T5: CLI Tool ─────────────────────────────────────────────────

T5_PROMPT = """Build a CLI tool at wordcount.py using argparse with four subcommands. The tool operates on text files.

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
- Run each subcommand against sample.txt to verify your implementation works."""


def verify_t5(cwd: str) -> VerifyResult:
    checks: list[dict] = []
    _check("wordcount.py exists", os.path.isfile(os.path.join(cwd, "wordcount.py")), checks)

    try:
        r = _run("python -m py_compile wordcount.py", cwd)
        _check("compiles", r.returncode == 0, checks)
    except Exception:
        _check("compiles", False, checks)

    # count
    try:
        r = _run("python wordcount.py count sample.txt", cwd)
        _check("count correct", str(SAMPLE_WORD_COUNT) in r.stdout, checks)
    except Exception:
        _check("count correct", False, checks)

    # freq -n 1
    try:
        r = _run("python wordcount.py freq sample.txt -n 1", cwd)
        _check("freq correct", SAMPLE_TOP_WORD in r.stdout, checks)
    except Exception:
        _check("freq correct", False, checks)

    # search case-sensitive
    try:
        r = _run("python wordcount.py search sample.txt python", cwd)
        non_empty = [ln for ln in r.stdout.strip().splitlines() if ln.strip()]
        _check("search case-sensitive", len(non_empty) == SAMPLE_PYTHON_CS_LINES, checks)
    except Exception:
        _check("search case-sensitive", False, checks)

    # search --ignore-case
    try:
        r = _run("python wordcount.py search sample.txt Python --ignore-case", cwd)
        non_empty = [ln for ln in r.stdout.strip().splitlines() if ln.strip()]
        _check("search ignore-case", len(non_empty) == SAMPLE_PYTHON_CI_LINES, checks)
    except Exception:
        _check("search ignore-case", False, checks)

    # stats
    try:
        r = _run("python wordcount.py stats sample.txt", cwd)
        _check("stats word count", f"Words: {SAMPLE_WORD_COUNT}" in r.stdout, checks)
    except Exception:
        _check("stats word count", False, checks)

    # missing file error
    try:
        r = _run("python wordcount.py count nonexistent.txt", cwd)
        _check("missing file error", r.returncode == 1 and "file not found" in r.stderr.lower(), checks)
    except Exception:
        _check("missing file error", False, checks)

    passed = sum(1 for c in checks if c["passed"])
    return passed / len(checks), f"{passed}/{len(checks)} checks passed", checks


# ── T6: Multi-File Package ───────────────────────────────────────

T6_PROMPT = r"""Create a Python package called `calculator` with full test coverage.

## Package Structure

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

def traced(log: HistoryLog) that is a decorator factory recording every call to the wrapped function in the given log.

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

Run the tests to verify everything passes."""


def verify_t6(cwd: str) -> VerifyResult:
    checks: list[dict] = []
    _check("calculator/__init__.py exists",
           os.path.isfile(os.path.join(cwd, "calculator", "__init__.py")), checks)
    _check("calculator/ops.py exists",
           os.path.isfile(os.path.join(cwd, "calculator", "ops.py")), checks)
    _check("calculator/history.py exists",
           os.path.isfile(os.path.join(cwd, "calculator", "history.py")), checks)
    _check("calculator/__main__.py exists",
           os.path.isfile(os.path.join(cwd, "calculator", "__main__.py")), checks)
    _check("tests/test_ops.py exists",
           os.path.isfile(os.path.join(cwd, "tests", "test_ops.py")), checks)
    _check("tests/test_integration.py exists",
           os.path.isfile(os.path.join(cwd, "tests", "test_integration.py")), checks)

    # Package imports
    try:
        r = _run('python -c "from calculator import add, subtract, multiply, divide, power, modulo, HistoryLog, traced"', cwd)
        _check("package imports", r.returncode == 0, checks)
    except Exception:
        _check("package imports", False, checks)

    # CLI works
    try:
        r = _run("python -m calculator add 2 3", cwd)
        out = r.stdout.strip()
        _check("CLI works", out in ("5", "5.0"), checks)
    except Exception:
        _check("CLI works", False, checks)

    # TypeError raised
    try:
        r = _run('python -c "from calculator import add; add(\'a\', 1)"', cwd)
        _check("TypeError raised",
               r.returncode != 0 and "operands must be numeric" in (r.stderr + r.stdout), checks)
    except Exception:
        _check("TypeError raised", False, checks)

    # All tests pass
    try:
        r = _run("python -m pytest tests/ -q", cwd, timeout=60)
        _check("all tests pass", r.returncode == 0, checks)
    except Exception:
        _check("all tests pass", False, checks)

    passed = sum(1 for c in checks if c["passed"])
    return passed / len(checks), f"{passed}/{len(checks)} checks passed", checks


# ── Task list ────────────────────────────────────────────────────

TASKS = [
    Task(key="t1", label="Hello World",    prompt=T1_PROMPT, fixtures=[],             verify=verify_t1),
    Task(key="t2", label="Fibonacci",       prompt=T2_PROMPT, fixtures=[],             verify=verify_t2),
    Task(key="t3", label="CSV Processing",  prompt=T3_PROMPT, fixtures=["data.csv"],   verify=verify_t3),
    Task(key="t4", label="Stack + Tests",   prompt=T4_PROMPT, fixtures=[],             verify=verify_t4),
    Task(key="t5", label="CLI Tool",        prompt=T5_PROMPT, fixtures=["sample.txt"], verify=verify_t5),
    Task(key="t6", label="Package + Tests", prompt=T6_PROMPT, fixtures=[],             verify=verify_t6),
]


def setup_task_dir(task: Task) -> str:
    """Create a fresh temp dir with any required fixtures copied in."""
    tmp = tempfile.mkdtemp(prefix=f"pi-bench-{task.key}-")
    for fname in task.fixtures:
        src = FIXTURES_DIR / fname
        if src.exists():
            shutil.copy2(src, os.path.join(tmp, fname))
    return tmp


def cleanup_task_dir(path: str) -> None:
    """Remove a temp dir."""
    shutil.rmtree(path, ignore_errors=True)

# Plan: qwen35-vs-gemma4 Live Benchmark

## Task Description

Build the first real live benchmark for live-bench: a 4-way comparison of **Qwen 3.5 35B-A3B** vs **Gemma 4 26B-A4B** across **GGUF (Ollama)** and **MLX** backends. This benchmark runs actual inference on Apple Silicon hardware and streams results in real time to the live-bench dashboard via SSE.

The benchmark measures three metrics (prefill speed, decode speed, wall-clock time) using the proven warm-isolated methodology from the existing gemma4 and pi-agent-playground-v2 codebases. Each metric gets its own chart in a single multi-chart benchmark YAML. Each chart is driven by its own astral uv single-file Python script that runs the benchmark and emits results via the `live-bench` CLI.

## Objective

When complete:
1. A YAML at `benchmarks/qwen35-vs-gemma4.yaml` defines a 3-chart benchmark (prefill, decode, wall)
2. Three uv single-file scripts in `apps/benchmarks/qwen35-vs-gemma4/` each run one chart's benchmark and emit results live
3. A shared harness (`_harness.py` + `_mlx_runner.py`) implements the warm-isolated methodology
4. Justfile recipes let you run the full benchmark or individual charts
5. The entire pipeline is validated end-to-end: scripts execute, results appear in the UI, Playwright browser tests prove it works

## Problem Statement

The live-bench platform has demo/fixture benchmarks but no real benchmarks that run actual inference workloads. We need to prove the full data path works end-to-end: a benchmark script runs real model inference, emits results via `live-bench emit`, the backend ingests them, SSE broadcasts to the frontend, and animated bars update in real time. This is the first benchmark that closes that loop.

## Solution Approach

Port the warm-isolated benchmark harness from the gemma4 codebase into `apps/benchmarks/qwen35-vs-gemma4/`. Each chart gets its own uv single-file script that:
1. Iterates over 4 backends (qwen35_gguf, qwen35_mlx, gemma4_gguf, gemma4_mlx)
2. For each backend, runs 5 prompts through `run_warm_isolated` (warmup + N=3 measured + median)
3. After each backend completes, emits the **average** metric across all prompts to live-bench
4. Marks the group complete

This means each chart has 4 bars (one per backend), and each bar's value is the average across the 5-prompt suite — matching the summary view from the original benchmarks.

## Relevant Files

### Existing — live-bench platform
- `benchmarks/test-trio.yaml` — reference for multi-chart YAML format (3 charts, shared groups)
- `benchmarks/m5-4way-tps.yaml` — reference for 4-group benchmark with gradient colors
- `apps/backend/src/live_bench_server/models.py` — BenchmarkConfig, ChartDef schema (lines 100-188)
- `apps/backend/src/live_bench_server/http_ingest.py` — ingest endpoint, case-insensitive groups
- `apps/cli/src/live_bench_cli/commands/emit_cmd.py` — emit CLI interface
- `justfile` — existing recipes, pattern for new ones

### Existing — source benchmark codebases (private sibling repos, not part of this codebase)
- `gemma4/bench/_harness.py` — warm-isolated harness (272 lines, the gold standard)
- `gemma4/bench/_mlx_runner.py` — long-lived MLX subprocess (139 lines)
- `pi-agent-playground-v2/bench/bench_mlx_vs_gguf.py` — 4-way benchmark driver (211 lines, closest to what we're building)
- `pi-agent-playground-v2/bench/_harness.py` — Qwen-side harness (identical methodology)

### New Files
- `benchmarks/qwen35-vs-gemma4.yaml` — multi-chart benchmark definition
- `apps/benchmarks/qwen35-vs-gemma4/_harness.py` — ported warm-isolated harness
- `apps/benchmarks/qwen35-vs-gemma4/_mlx_runner.py` — ported MLX subprocess runner
- `apps/benchmarks/qwen35-vs-gemma4/chart_1_prefill.py` — uv single-file script for prefill chart
- `apps/benchmarks/qwen35-vs-gemma4/chart_2_decode.py` — uv single-file script for decode chart
- `apps/benchmarks/qwen35-vs-gemma4/chart_3_wall.py` — uv single-file script for wall-clock chart
- `apps/benchmarks/qwen35-vs-gemma4/run_all.py` — uv single-file script that runs all 3 charts sequentially
- `tests/e2e/test_qwen35_vs_gemma4.py` — Playwright browser validation tests

## Implementation Phases

### Phase 1: Foundation
Create the benchmark YAML and port the harness files. Establish the directory structure and verify the YAML loads correctly in the backend.

### Phase 2: Core Implementation
Build the three chart scripts as uv single-file scripts. Each script embeds its dependencies via `# /// script` metadata, uses the shared harness, and shells out to `live-bench emit` to push results. Add `run_all.py` orchestrator. Add justfile recipes.

### Phase 3: Integration & Polish
End-to-end validation: boot the platform, run `--smoke` benchmarks, verify bars appear in the UI. Write Playwright browser tests that prove the full pipeline. Update README.

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
  - Name: builder-yaml-harness
  - Role: Create the benchmark YAML and port the harness + MLX runner files
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-chart-scripts
  - Role: Build all chart scripts (chart_1_prefill.py, chart_2_decode.py, chart_3_wall.py, run_all.py) and justfile recipes
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-playwright-tests
  - Role: Write Playwright browser validation tests and drive-based terminal validation
  - Agent Type: playwright-bowser-agent
  - Resume: true

- Builder
  - Name: validator
  - Role: Run end-to-end smoke tests, verify UI renders correctly, confirm all acceptance criteria
  - Agent Type: general-purpose
  - Resume: true

## Step by Step Tasks

### 1. Create Benchmark YAML
- **Task ID**: create-yaml
- **Depends On**: none
- **Assigned To**: builder-yaml-harness
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 2)
- Create `benchmarks/qwen35-vs-gemma4.yaml` with:
  - `session_id: qwen35-vs-gemma4`
  - `title: "Qwen 3.5 vs Gemma 4 — Raw Inference"`
  - `subtitle: "35B-A3B vs 26B-A4B · GGUF vs MLX · Apple Silicon"`
  - 4 groups: `qwen35_gguf` ("Qwen 3.5 GGUF"), `qwen35_mlx` ("Qwen 3.5 MLX"), `gemma4_gguf` ("Gemma 4 GGUF"), `gemma4_mlx` ("Gemma 4 MLX")
  - Chart 1 `prefill`: "Prefill Speed", tok/s, BT, higher is better, metric key `prefill_tps`, color warm orange gradient `["#e86b3a", "#f2a66b"]`
  - Chart 2 `decode`: "Decode Speed", tok/s, BT, higher is better, metric key `decode_tps`, color cool blue gradient `["#4a8fe0", "#6fa5e8"]`
  - Chart 3 `wall`: "Wall-Clock Time", seconds, BT, lower is better, metric key `wall_s`, color purple gradient `["#a855f7", "#c084fc"]`
- Verify: `cd apps/backend && uv run python -c "from live_bench_server.store import _load_yaml; _load_yaml()"` or start the server and check `live-bench list` includes the new session

### 2. Port Harness and MLX Runner
- **Task ID**: port-harness
- **Depends On**: none
- **Assigned To**: builder-yaml-harness
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 1)
- Create directory `apps/benchmarks/qwen35-vs-gemma4/`
- Copy `gemma4/bench/_harness.py` (private sibling repo) to `apps/benchmarks/qwen35-vs-gemma4/_harness.py`
  - Keep it identical — this is proven code. Do NOT refactor.
  - The file has zero external dependencies beyond `httpx` (which the chart scripts will declare)
- Copy `gemma4/bench/_mlx_runner.py` (private sibling repo) to `apps/benchmarks/qwen35-vs-gemma4/_mlx_runner.py`
  - Keep it identical — proven code.
  - This file imports `mlx_vlm` at runtime (inside the subprocess that uses `.mlx-venv/bin/python`)

### 3. Build Chart 1 — Prefill Speed
- **Task ID**: build-chart-1
- **Depends On**: port-harness
- **Assigned To**: builder-chart-scripts
- **Agent Type**: general-purpose
- **Parallel**: false (sequential with chart 2, 3 since they share patterns)
- Create `apps/benchmarks/qwen35-vs-gemma4/chart_1_prefill.py` as a uv single-file script
- Script metadata block at top:
  ```python
  # /// script
  # requires-python = ">=3.12"
  # dependencies = ["httpx>=0.27"]
  # ///
  ```
- Import from local `_harness.py` via `sys.path.insert(0, str(Path(__file__).resolve().parent))`
- Define the 4 backend configs (matching `bench_mlx_vs_gguf.py` lines 37-46):
  - `qwen35_gguf`: model=`qwen3.5:35b`, ollama_chat, think=True
  - `qwen35_mlx`: model=`qwen3.5:35b-a3b-nvfp4`, ollama_chat, think=True
  - `gemma4_gguf`: model=`gemma4:26b`, ollama_chat, think=True
  - `gemma4_mlx`: model=`mlx-community/gemma-4-26b-a4b-it-4bit`, MLXRunner
- Define the 5-prompt suite (matching `bench_mlx_vs_gguf.py` lines 48-59)
- For each backend:
  1. Run `run_warm_isolated` for each prompt (iterations=N, default 3)
  2. Compute average `prefill_tok_s` across all prompts
  3. Emit via subprocess: `live-bench emit qwen35-vs-gemma4 --chart prefill --group <group_key> --metric prefill_tps --value <avg>`
  4. Mark complete: `live-bench complete qwen35-vs-gemma4 --chart prefill --group <group_key>`
- CLI flags: `--iterations N` (default 3), `--smoke` (1 prompt, 1 iteration), `--server URL` (passthrough to live-bench)
- MLX runner path: detect `.mlx-venv` relative to script location, or use env var `MLX_VENV`
- Print progress to stderr so terminal shows what's happening
- Exit 0 on success, 1 on failure

### 4. Build Chart 2 — Decode Speed
- **Task ID**: build-chart-2
- **Depends On**: build-chart-1
- **Assigned To**: builder-chart-scripts
- **Agent Type**: general-purpose
- **Parallel**: false
- Create `apps/benchmarks/qwen35-vs-gemma4/chart_2_decode.py` — same structure as chart 1 but:
  - Metric: `decode_tps` (average `decode_tok_s` across prompts)
  - Chart: `--chart decode`
- Factor: since the structure is nearly identical to chart 1, model the scripts to share a common `_bench_and_emit` function or just duplicate (3 files is fine, premature DRY is worse than clear)

### 5. Build Chart 3 — Wall-Clock Time
- **Task ID**: build-chart-3
- **Depends On**: build-chart-2
- **Assigned To**: builder-chart-scripts
- **Agent Type**: general-purpose
- **Parallel**: false
- Create `apps/benchmarks/qwen35-vs-gemma4/chart_3_wall.py` — same structure but:
  - Metric: `wall_s` (average `wall_time_s` across prompts)
  - Chart: `--chart wall`

### 6. Build run_all.py Orchestrator
- **Task ID**: build-run-all
- **Depends On**: build-chart-3
- **Assigned To**: builder-chart-scripts
- **Agent Type**: general-purpose
- **Parallel**: false
- Create `apps/benchmarks/qwen35-vs-gemma4/run_all.py` as uv single-file script
- Script metadata:
  ```python
  # /// script
  # requires-python = ">=3.12"
  # dependencies = ["httpx>=0.27"]
  # ///
  ```
- Runs all 3 charts sequentially by importing and calling their main functions, OR by subprocess calling each script
- Supports `--smoke` and `--iterations N` passthrough
- Optionally resets the session first via `live-bench reset qwen35-vs-gemma4 --yes`

### 7. Add Justfile Recipes
- **Task ID**: add-justfile
- **Depends On**: build-run-all
- **Assigned To**: builder-chart-scripts
- **Agent Type**: general-purpose
- **Parallel**: false
- Add a new section to `justfile` after the trio section:
  ```
  # ── qwen35-vs-gemma4 benchmark ─────────────────────────────
  bench-qg-prefill *FLAGS:
      uv run apps/benchmarks/qwen35-vs-gemma4/chart_1_prefill.py {{FLAGS}}

  bench-qg-decode *FLAGS:
      uv run apps/benchmarks/qwen35-vs-gemma4/chart_2_decode.py {{FLAGS}}

  bench-qg-wall *FLAGS:
      uv run apps/benchmarks/qwen35-vs-gemma4/chart_3_wall.py {{FLAGS}}

  bench-qg *FLAGS:
      uv run apps/benchmarks/qwen35-vs-gemma4/run_all.py {{FLAGS}}

  bench-qg-smoke:
      uv run apps/benchmarks/qwen35-vs-gemma4/run_all.py --smoke

  bench-qg-reset:
      live-bench reset qwen35-vs-gemma4 --yes
  ```
- Update README.md CLI commands table with new recipes under a **qwen35-vs-gemma4** subsection

### 8. Smoke Test — Scripts Execute
- **Task ID**: smoke-scripts
- **Depends On**: add-justfile
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Boot the backend: `just backend` (in background or via drive tmux)
- Run `just bench-qg-smoke` and verify:
  - All 3 chart scripts execute without error
  - Each emits 4 values (one per backend group)
  - `live-bench show qwen35-vs-gemma4` shows the ingested data
- If models aren't available (no Ollama running), mock-validate by checking script `--help` works and that the YAML loads correctly:
  - `uv run apps/benchmarks/qwen35-vs-gemma4/chart_1_prefill.py --help`
  - Start backend, verify `live-bench list` includes `qwen35-vs-gemma4`

### 9. Playwright Browser Validation
- **Task ID**: playwright-validation
- **Depends On**: smoke-scripts
- **Assigned To**: builder-playwright-tests
- **Agent Type**: playwright-bowser-agent
- **Parallel**: false
- Use Playwright headless browser to validate the UI end-to-end:
  1. Navigate to `http://127.0.0.1:5787/`
  2. Verify the benchmark list contains "Qwen 3.5 vs Gemma 4"
  3. Click into the benchmark page (`/benchmark/qwen35-vs-gemma4`)
  4. Verify 3 chart cards render (prefill, decode, wall)
  5. Verify 4 group labels appear per chart (Qwen 3.5 GGUF, Qwen 3.5 MLX, Gemma 4 GGUF, Gemma 4 MLX)
  6. If data was emitted (smoke test ran): verify bars have non-zero width/height
  7. Take screenshots at each step for evidence
- Use /drive tmux sessions to manage the backend + frontend processes
- Save screenshots to `tests/e2e/screenshots/`

### 10. Final Validation
- **Task ID**: validate-all
- **Depends On**: smoke-scripts, playwright-validation
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Run full test suite: `just test` (backend + CLI + frontend tests still pass)
- Verify no regressions in existing benchmarks
- Verify `just --list` shows all new recipes
- Confirm README.md is updated with new benchmark section
- Report final status

## Acceptance Criteria

1. `benchmarks/qwen35-vs-gemma4.yaml` loads without error — backend serves it and `live-bench list` includes the session
2. `uv run apps/benchmarks/qwen35-vs-gemma4/chart_1_prefill.py --help` exits 0 and shows usage
3. `uv run apps/benchmarks/qwen35-vs-gemma4/chart_2_decode.py --help` exits 0
4. `uv run apps/benchmarks/qwen35-vs-gemma4/chart_3_wall.py --help` exits 0
5. `uv run apps/benchmarks/qwen35-vs-gemma4/run_all.py --help` exits 0
6. Each chart script uses the warm-isolated methodology: warmup discard, nonce prefixes, median-of-N, long-lived MLX process
7. Each chart script emits results via `live-bench emit` with correct `--chart`, `--group`, `--metric`, `--value` flags
8. Each chart script marks groups complete via `live-bench complete` after all prompts finish
9. `just bench-qg-smoke` runs end-to-end when Ollama is available (or `--help` validates wiring when not)
10. Frontend renders all 3 charts with 4 bars each on the benchmark page
11. Playwright tests pass proving UI renders correctly
12. `just test` (existing test suite) still passes — no regressions
13. README.md documents the new benchmark recipes

## Validation Commands

Execute these commands to validate the task is complete:

- `cd apps/backend && uv run python -c "from live_bench_server.store import load_benchmarks; import sqlite3; load_benchmarks(sqlite3.connect(':memory:'), 'benchmarks')"` — Verify YAML parses and loads
- `uv run apps/benchmarks/qwen35-vs-gemma4/chart_1_prefill.py --help` — Chart 1 script is valid
- `uv run apps/benchmarks/qwen35-vs-gemma4/chart_2_decode.py --help` — Chart 2 script is valid
- `uv run apps/benchmarks/qwen35-vs-gemma4/chart_3_wall.py --help` — Chart 3 script is valid
- `uv run apps/benchmarks/qwen35-vs-gemma4/run_all.py --help` — Orchestrator is valid
- `just test` — All existing tests pass
- `just bench-qg-smoke` — End-to-end smoke (requires Ollama + models)
- Playwright browser tests — automated UI validation

## Notes

### Models Required

For live benchmarking, the following must be pulled to Ollama:
```bash
ollama pull qwen3.5:35b
ollama pull qwen3.5:35b-a3b-nvfp4
ollama pull gemma4:26b
```

For Gemma 4 MLX, the model downloads automatically from HuggingFace on first use:
- `mlx-community/gemma-4-26b-a4b-it-4bit` (~15.6 GB)

An `.mlx-venv` with `mlx-vlm` installed is required for the MLX runner:
```bash
cd apps/benchmarks/qwen35-vs-gemma4
uv venv .mlx-venv --python 3.12
source .mlx-venv/bin/activate
uv pip install mlx-vlm torchvision
```

### uv Single-File Script Format

Each chart script uses the [PEP 723](https://peps.python.org/pep-0723/) inline metadata format:
```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27"]
# ///
```

This allows `uv run chart_1_prefill.py` to work without a pyproject.toml — uv creates an isolated env on the fly.

### Warm-Isolated Methodology (MUST be preserved)

The five rules from the gemma4 harness — all MUST carry over:
1. **One warmup call** with "Say hi." (discarded) — faults in weight pages + JIT-compiles kernels
2. **Long-lived MLX process** — MLXRunner boots once, weights stay resident in unified memory
3. **Ollama keep_alive=-1** — never evict model from VRAM between calls
4. **Nonce prefixes** — `[run:<uuid>] ` on every measured call defeats prompt cache
5. **Median of N** — default iterations=3, report median across all metrics

### Emit Pattern

After benchmarking all prompts for a given backend, compute the average metric value across the 5-prompt suite and emit once:

```python
avg_prefill = sum(r["prefill_tok_s"] for r in rows) / len(rows)
subprocess.run(["live-bench", "emit", "qwen35-vs-gemma4",
                "--chart", "prefill",
                "--group", group_key,
                "--metric", "prefill_tps",
                "--value", str(round(avg_prefill, 1))],
               check=True)
subprocess.run(["live-bench", "complete", "qwen35-vs-gemma4",
                "--chart", "prefill",
                "--group", group_key],
               check=True)
```

This means each chart gets exactly 4 emit calls (one per backend) rather than 20 (one per prompt per backend). The bars represent average performance across the suite.

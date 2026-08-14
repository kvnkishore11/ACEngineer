---
description: Install live-bench — prerequisites, dependencies, models, and environment for the dashboard server and benchmark client machines
---

# Install live-bench

## Purpose

Set up live-bench for development and live benchmarking. Checks prerequisites, installs dependencies for the three apps (backend, CLI, frontend), configures the environment, and optionally pulls Ollama models + provisions the MLX virtual environment for benchmark client machines. This is an interactive, agentic process — ask the user when choices are needed.

## Variables

SOURCE_REPO: The directory this command is running from
BACKEND_DIR: `apps/backend`
CLI_DIR: `apps/cli`
FRONTEND_DIR: `apps/frontend`
MLX_BENCH_DIR: `apps/benchmarks/qwen35-vs-gemma4` (the canonical `.mlx-venv` location reused by context-scaling and context-scaling-3way)
QG3_BENCH_DIR: `apps/benchmarks/qwen36-vs-qwen35-vs-gemma4` (its own `.mlx-venv`)

## Codebase Structure

```
live-bench/
├── apps/
│   ├── backend/       — FastAPI + SQLite + SSE (Python, uv)
│   ├── cli/           — `live-bench` Click CLI (Python, uv)
│   ├── frontend/      — Vue 3 + Vite (TypeScript, Bun)
│   └── benchmarks/    — uv single-file benchmark scripts
├── benchmarks/        — YAML chart definitions (read on backend boot)
├── .env.sample        — environment template (LIVE_BENCH_SERVER)
└── justfile           — task runner recipes
```

## Instructions

- Run every check via Bash — do not assume anything is installed.
- Show a status line immediately after each check: `[pass]` or `[FAIL]`.
- For auto-installable items (brew, uv tools, bun packages), install them without asking.
- For items requiring user input (LAN IP, model pulls, MLX setup), ask the user with sensible defaults.
- Do NOT read or display env var values — only confirm they are set.
- Do NOT start servers or long-running processes.
- Ask the user upfront: **"Is this machine a server (runs the dashboard), a benchmark client (runs models and emits data), or both?"** — this gates the optional client-only steps.

## Workflow

### Step 1 — Determine Machine Role

Ask the user:
> Is this machine a **server** (runs the dashboard), a **benchmark client** (runs models and emits data), or **both**?

Store the answer. It determines:

- **Server** → just, uv, Python 3.12+, bun, frontend deps, CLI
- **Client** → just, uv, Python 3.12+, CLI, Ollama, models, MLX venv (Apple Silicon)
- **Both** → everything

### Step 2 — Check Prerequisites

Check these in order. Critical items gate the install — stop and guide the user if missing.

1. **just** (critical, all roles): `command -v just`
   - If missing: `brew install just`
   - If brew missing: link to https://github.com/casey/just#installation

2. **uv** (critical, all roles): `command -v uv`
   - If missing: `brew install uv`

3. **Python 3.12+** (critical, all roles): `uv python find 3.12 || uv python install 3.12`

4. **bun** (critical, server only): `command -v bun`
   - If missing: `brew install oven-sh/bun/bun`

5. **mprocs** (optional, server only): `command -v mprocs`
   - If missing: inform user `brew install mprocs` enables `just serve` (one-terminal dev). Without it they can run `just backend` and `just frontend` in two terminals.

6. **Ollama** (critical, client only): `command -v ollama`
   - If missing: `brew install ollama`
   - Verify daemon: `ollama list` (should not error)

### Step 3 — Install Dependencies

Run these based on role:

1. **Frontend deps** (server): `cd apps/frontend && bun install`
2. **CLI global install** (all roles): `cd apps/cli && uv tool install --editable . --force`
3. **Verify CLI**: `live-bench --help` (should print usage)

### Step 4 — Configure Environment

1. Check if `.env` exists at repo root.
   - If missing: `cp .env.sample .env`
2. If role is **client** or **both**, ask:
   > What is the server machine's LAN IP? (run `just lan-ip` on the server, or press enter for `127.0.0.1` if running on the same box)
3. Confirm `LIVE_BENCH_SERVER` is set in `.env`. Do NOT print the value.
4. Verify connectivity (only if the server is already running): `live-bench ping`
   - If the server is not up, skip — tell the user to boot it later with `just serve`.

### Step 5 — Pull Ollama Models (Client Only)

Ask the user: **"Pull the benchmark models now? This downloads ~110 GB total across 5 models."**

If yes, pull each and report status:

1. `ollama pull qwen3.5:35b` (~24 GB) — Qwen 3.5 GGUF
2. `ollama pull qwen3.5:35b-a3b-nvfp4` (~22 GB) — Qwen 3.5 MLX-via-Ollama
3. `ollama pull qwen3.6:35b-a3b` (~24 GB) — Qwen 3.6 GGUF
4. `ollama pull qwen3.6:35b-a3b-nvfp4` (~22 GB) — Qwen 3.6 MLX-via-Ollama
5. `ollama pull gemma4:26b` (~17 GB) — Gemma 4 GGUF

If no, inform the user they can pull on demand before each `just bench-*` recipe.

### Step 6 — Set Up MLX Virtual Environment (Client Only, Apple Silicon)

Check architecture: `uname -m` should be `arm64`. Skip this step on x86 / Linux.

If Apple Silicon, ask: **"Set up the MLX virtual environment for Gemma 4 MLX? (required for the 4th backend in qwen35-vs-gemma4 and for context-scaling)"**

If yes:

1. `cd apps/benchmarks/qwen35-vs-gemma4`
2. `uv venv .mlx-venv --python 3.12`
3. `uv pip install --python .mlx-venv/bin/python mlx-vlm torchvision`
4. Verify: `.mlx-venv/bin/python -c "from mlx_vlm import load; print('ok')"`

Then ask: **"Pre-download the Gemma 4 MLX model now? (~15.6 GB from HuggingFace, otherwise it downloads lazily on first run)"**

If yes:

5. `.mlx-venv/bin/python -c "from mlx_vlm import load; load('mlx-community/gemma-4-26b-a4b-it-4bit'); print('model ready')"`

Then ask: **"Also provision a separate `.mlx-venv` for the 3-way (qwen36-vs-qwen35-vs-gemma4) benchmark? (the 3-way runner expects its own venv at apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/.mlx-venv)"**

If yes:

6. `cd apps/benchmarks/qwen36-vs-qwen35-vs-gemma4 && uv venv .mlx-venv --python 3.12 && uv pip install --python .mlx-venv/bin/python mlx-vlm torchvision`

(`context-scaling` and `context-scaling-3way` reuse the venv from `qwen35-vs-gemma4` — no extra setup needed.)

### Step 7 — Verify Readiness

1. `just --list | head -5` — justfile loads.
2. `live-bench --help` — CLI works.
3. `ls benchmarks/*.yaml | wc -l` — should report **7 or more** YAML files.
4. If server role: confirm `apps/frontend/node_modules` exists.
5. If client role: `ollama list` — verify pulled models are present.

### Step 8 — Report

Print a summary table:

```
live-bench install report
─────────────────────────────────────────
Role:          [server / client / both]

Prerequisites:
  just              [pass/FAIL]
  uv                [pass/FAIL]
  Python 3.12       [pass/FAIL]
  bun               [pass/FAIL/skip]
  mprocs            [pass/skip]
  Ollama            [pass/FAIL/skip]

Dependencies:
  frontend          [pass/skip]
  live-bench CLI    [pass/FAIL]

Environment:
  .env              [pass/FAIL]
  LIVE_BENCH_SERVER [configured/default]

Models (client):
  qwen3.5:35b               [pulled/skip]
  qwen3.5:35b-a3b-nvfp4     [pulled/skip]
  qwen3.6:35b-a3b           [pulled/skip]
  qwen3.6:35b-a3b-nvfp4     [pulled/skip]
  gemma4:26b                [pulled/skip]

MLX venvs (client):
  qwen35-vs-gemma4/.mlx-venv          [ready/skip]
  qwen36-vs-qwen35-vs-gemma4/.mlx-venv [ready/skip]

Benchmarks:
  YAMLs found       [N]
─────────────────────────────────────────
```

Then print next steps based on role:

**Server:**

```
Next steps:
  just serve              # start dashboard (backend :8787 + frontend :5787)
  just lan-ip             # print the LAN URL to share with client machines
  just mock               # fastest UI smoke test (no models required)
```

**Client:**

```
Next steps:
  just ping               # verify connection to LIVE_BENCH_SERVER
  just bench-qg3-smoke-m4 # quick 1-prompt validation on M4
  just bench-3way-m5      # full 3-way matrix on M5 (~45–55 min)
```

**Both:**

```
Next steps:
  just serve              # start dashboard (terminal 1)
  just lan-ip             # show LAN URL
  just mock               # demo run — fake data with animated bars
  just bench-qg3-smoke-m5 # real-inference smoke test (terminal 2)
```

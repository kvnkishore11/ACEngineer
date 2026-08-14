---
description: Load foundational context about the live-bench codebase
---

# Purpose

Orient yourself in the live-bench monorepo — a live benchmarking platform with a FastAPI backend, Click CLI, and Vue 3 frontend that streams hardware/model evaluation results onto animated SVG dashboards via SSE.

## Workflow

1. Run `git ls-files | head -80` to see the repo layout, then glob `benchmarks/*.yaml` to discover all benchmark definitions
2. Read these files for project context:
   - `README.md` — overview, quick start, layout
   - `justfile` — all dev recipes (serve, test, emit, test-drive walkthrough)
   - `spec/init_live_bench.md` — the single source of truth design spec
3. Read stack configs:
   - `apps/backend/pyproject.toml` — Python backend deps
   - `apps/cli/pyproject.toml` — CLI deps (path-deps the backend)
   - `apps/frontend/package.json` — Vue/Vite/Pinia frontend deps
4. Read entry points to understand the runtime shape:
   - `apps/backend/src/live_bench_server/main.py` — FastAPI app bootstrap
   - `apps/cli/src/live_bench_cli/cli.py` — Click CLI entry
   - `apps/frontend/src/App.vue` — Vue root component
   - `apps/frontend/src/router.ts` — frontend routes
5. Summarize your understanding of the project: purpose, stack, monorepo structure, data flow (YAML -> backend -> SSE -> frontend), key entry points, and how to run/test everything

---
description: Install UI Agents — prerequisites, dependencies, team config, and dev server verification
---

# Install UI Agents

## Purpose

Set up the UI Agents infinite UI generation system. Checks that the Multi-Team Agentic Coding foundation is installed, verifies prerequisites, installs app dependencies, validates team config, and confirms the dev server is ready. This is an interactive, agentic process — ask the user when choices are needed.

## Variables

SOURCE_REPO: The directory this command is running from (the repo root containing `apps/infinite-ui/`)
APP_DIR: `apps/infinite-ui` (relative to SOURCE_REPO)
MEMBER_ASSETS_URL: https://agenticengineer.com/tactical-agentic-coding/member-assets
CONFIG_PATH: `.pi/multi-team/multi-team-config.yaml`
PROMPTS_DIR: `.pi/prompts/multi-team/`

## Codebase Structure

```
ui-agents/
├── apps/infinite-ui/           # Vue app (brands, products, trees)
│   ├── src/brands/             # All brand/product data (agents write here)
│   ├── src/schemas/            # Zod schemas (brand + trees)
│   └── src/stores/             # Pinia stores (brand, trees, canvas)
├── .pi/multi-team/
│   ├── multi-team-config.yaml  # Team definitions (8 teams, 12+ agents)
│   ├── agents/                 # Agent system prompts
│   ├── expertise/              # Agent mental models (auto-maintained)
│   └── skills/                 # Shared behavioral rules
├── .pi/prompts/multi-team/     # 9 workflow commands (/generate, /new-brand, etc.)
├── scripts/list.py             # CLI for listing brands/products/trees
└── justfile                    # Task runner (team, dev, list, generate)
```

## Instructions

- Run every check via Bash — do not assume anything is installed.
- Show a status line immediately after each check (✅ or ❌).
- For auto-installable items (like bun dependencies), install them without asking.
- Do NOT read or display API key values — only confirm they are set.
- The `pi` binary and `teams` alias are needed for multi-team agent generation. If either is missing, warn the user but continue — they can still browse the app and view existing brands/components via `just dev`.
- Do NOT install a shell alias here — UI Agents uses the `teams` alias from Multi-Team Agentic Coding via the justfile.

## Workflow

### Step 1 — Check Multi-Team Generation Tools (non-blocking)

Pi and the `teams` alias are only needed for multi-team agent generation (`just team`, `/generate`, `/new-brand`). Without them, `just dev` still works and users can browse existing brands and components. **Always continue to Step 2 even if these are missing.**

1. **Pi coding agent** — `command -v pi`
   - If missing: ⚠️ Warn (do not stop):
     ```
     Pi coding agent is not installed. You can still browse the app with 'just dev',
     but you won't be able to generate or modify UI until Pi is set up.
     
     Download from: https://agenticengineer.com/tactical-agentic-coding/member-assets
     Then build the Multi-Team Agentic Coding (lead-agents) codebase and run /install there.
     ```
   - If found: ✅ Show version with `pi --version`

2. **`teams` alias** — `type teams`
   - If missing: ⚠️ Warn (do not stop):
     ```
     The 'teams' alias is not set up. You can still browse and view existing UI with 'just dev',
     but 'just team', /generate, and /new-brand won't work until it's installed.
     
     Get it from: https://agenticengineer.com/tactical-agentic-coding/member-assets
     Then run /install in that codebase to create the 'teams' shell function.
     ```
   - If found: ✅ Show the alias definition

Proceed to Step 2 regardless of the results above.

### Step 2 — Check Other Prerequisites

Run each check and show the result immediately:

1. **Claude Code** — `command -v claude` → if missing: "Install Claude Code: `npm install -g @anthropic-ai/claude-code`" or https://docs.anthropic.com/en/docs/claude-code
2. **Bun** — `command -v bun` → if missing: "Install: `curl -fsSL https://bun.sh/install | bash`"
3. **Node.js** — `command -v node` → if missing: "Install: https://nodejs.org"
4. **just** — `command -v just` → if missing: "Install: `brew install just`"
5. **uv** — `command -v uv` → if missing: "Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`" (needed for `scripts/list.py`)

If any required prerequisite is missing, stop and tell the user what to install. Do not proceed until prerequisites are met.

### Step 3 — Check Environment

1. **`ANTHROPIC_API_KEY`** — Check if set in the current environment (`[ -n "$ANTHROPIC_API_KEY" ]`). Do NOT display the value.
   - If set: ✅ `ANTHROPIC_API_KEY is configured`
   - If missing: ❌ Tell the user to export it in their shell profile or `.env`

### Step 4 — Install App Dependencies

1. Run `cd apps/infinite-ui && bun install` to install Vue app dependencies.
2. Show ✅ when complete.

### Step 5 — Verify Team Config

1. Check that `.pi/multi-team/multi-team-config.yaml` exists.
2. Check that all agent `.md` files referenced in the config exist. Parse the YAML and verify each `path` field under `orchestrator`, `lead`, and `members`.
3. Count teams, leads, and members. Show the count.
4. If any agent file is missing, show ❌ with the missing path.
5. Check that `.pi/prompts/multi-team/` contains workflow command files. List them with a count.
6. Check that `.pi/multi-team/expertise/` directory exists (mental model storage).
7. Check that `.pi/multi-team/skills/` directory exists and contains skill files.

### Step 6 — Verify Dev Server Readiness

1. Check that `justfile` exists in the project root.
2. Check that `apps/infinite-ui/vite.config.ts` exists.
3. Check that `apps/infinite-ui/package.json` exists and has a `dev` script.
4. Show the available `just` recipes by running `just --list`.

Do NOT start the dev server — just verify the files are in place.

### Step 7 — Report

Show the final summary, then next steps:

```
UI Agents — Install Complete

  [status] Pi coding agent (needed for generation only)
  [status] teams alias (needed for generation only)
  [status] Claude Code
  [status] Bun
  [status] Node.js
  [status] just
  [status] uv
  [status] ANTHROPIC_API_KEY
  [status] App dependencies (apps/infinite-ui)
  [status] Team config ([N] teams, [N] agents)
  [status] Workflow commands ([N] prompts)
  [status] Dev server readiness

Ready: [count]/[total]

Next steps:

  # Start the Vue app
  just dev

  # Start multi-team chat (talk to the Orchestrator)
  just team

  # Prime Claude Code with project context
  /prime

  # Generate your first UI
  just new-brand mybrand "A bold fintech brand"
  just generate mybrand myproduct landing 3 "Hero sections with dynamic typography"

  # See what's already here
  just list-brands
```

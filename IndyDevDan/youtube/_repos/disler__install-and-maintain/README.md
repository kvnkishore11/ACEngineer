# Install and Maintain

<img src="images/install_and_maintain.webp" alt="Install and Maintain" width="800">

**You can tell how great an engineering team is by the time it takes for a new engineer to run the project locally.**

For great teams, it's one link, a few config updates, and a couple commands. For most teams, it's days of pair programming, Slack threads, and outdated docs. In the age of agents, we can do better.

**Agents + code beats agents. Agents + code beats just code.**

Traditional approaches force a choice: pure scripts (deterministic but brittle), pure agents (adaptive but unpredictable), or pure docs (flexible but manual). This pattern combines them. Your deterministic scripts handle execution, agents provide oversight. The result: **a living document that executes.**

## Justfile

Think of the `justfile` as your launch pad. It's where you, your team, and your agents go to run commands without remembering flags or looking up syntax. This project uses [just](https://github.com/casey/just). A command runner similar to `make` but simpler. Run `just` to see available commands, or `just <command>` to execute one.

## Quick Start

> First read `justfile` to see the commands and their descriptions.

```bash
# See all commands
just --dump

# See just the commands with descriptions
just

# Deterministic - fast, predictable, CI-friendly
just cldi

# Agentic - runs hook, analyzes logs, reports status
just cldii

# Interactive - asks questions, adapts to your context
just cldit
```

## The Pattern

```
┌─────────────────────────────────────────────────────────┐
│  DETERMINISTIC          AGENTIC           INTERACTIVE   │
│  (hooks)                (prompts)         (prompts)     │
│                                                         │
│  claude --init          /install          /install true │
│  claude --maintenance   /maintenance                    │
│                                                         │
│  - Fast                 - Supervised      - Asks Qs     │
│  - Predictable          - Diagnostic      - Adapts      │
│  - CI-friendly          - Reports status  - Context-    │
│                                             aware       │
└─────────────────────────────────────────────────────────┘
```

**The script is the source of truth.** Both hooks and prompts execute the same script. The difference is whether an agent supervises—and whether it asks you questions first.

## Commands

| Command      | Mode                                  | What it does                     |
| ------------ | ------------------------------------- | -------------------------------- |
| `just cldi`  | Deterministic                         | Run init hook, exit              |
| `just cldii` | Deterministic + Agentic               | Run hook + prompt + report       |
| `just cldit` | Deterministic + Agentic + Interactive | Run hook, prompt + ask questions |
| `just cldm`  | Deterministic                         | Run maintenance hook, exit       |
| `just cldmm` | Deterministic + Agentic               | Run hook + prompt + report       |
| `just reset` | Deterministic                         | Undo install (for retesting)     |

## When to Use What

| Scenario                          | Use                                  |
| --------------------------------- | ------------------------------------ |
| CI/CD pipeline                    | `claude --init-only` (deterministic) |
| Quick local setup                 | `just cldi` (deterministic)          |
| Setup failed, need diagnosis      | `just cldii` (agentic)               |
| New engineer, unfamiliar codebase | `just cldit` (interactive)           |
| Weekly dependency updates         | `just cldmm` (agentic)               |

## Why This Works

### Determinism Preserved
The hook runs the same script every time. No LLM variance in execution. Agents only analyze *after* the deterministic work is done.

### CI Compatible
```yaml
# GitHub Actions
- run: claude --init-only  # Hook only, no agent, exits cleanly
```

### Interactive When It Matters
Agentic prompts can ask clarifying questions mid-workflow—something scripts can never do:

```
/install true

Agent: Found existing database. How should I proceed?

┌─ Database Setup ────────────────────────────────┐
│  ○ Keep existing data                           │
│  ○ Reset to fresh state (Recommended)           │
│  ○ Let me check first                           │
└─────────────────────────────────────────────────┘
```

## What Gets Installed

**Backend** (Python + uv)
- Dependencies via `uv sync`
- SQLite database with mock data

**Frontend** (Vite + Vue + TypeScript)
- Dependencies via `npm install`

## Run the App

```bash
just be  # Terminal 1 - backend at :8000
just fe  # Terminal 2 - frontend at :5173
```

## Project Structure

```
├── .claude/
│   ├── commands/        # /install, /install-hil, /maintenance, /prime
│   ├── hooks/           # setup_init.py, setup_maintenance.py
│   └── settings.json
├── apps/
│   ├── backend/         # FastAPI + SQLite
│   └── frontend/        # Vite Vue-TS
└── justfile
```

## Requirements

- [Claude Code](https://code.claude.com/docs/en/overview)
- Python 3.11+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+
- [just](https://github.com/casey/just)

## Learn More

- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [A Standard for LLM Executables](https://mintlify.com/blog/llm-executables) — Mintlify's take on this emerging pattern

## Master **Agentic Coding**
> Prepare for the future of software engineering

Learn tactical agentic coding patterns with [Tactical Agentic Coding](https://agenticengineer.com/tactical-agentic-coding?y=inadmnt)

Follow the [IndyDevDan YouTube channel](https://www.youtube.com/@indydevdan) to improve your agentic coding advantage.


---
description: Install Pi Verifier Agent — prerequisites, deps, persona/script validation, and provider env
---

# Install Pi Verifier Agent

## Purpose

Set up the Pi Verifier Agent for development on a fresh clone. Walks the user through every check the system needs — runtime tools (node / python / uv / tmux / sqlite3 / pi), TypeScript dependencies, the verifier persona + script, and an LLM provider API key — without ever starting an interactive Pi session. Interactive: ask the user when a choice is needed (e.g., which API key to set), install what can be installed automatically.

## Variables

SOURCE_REPO: The repo root this command runs from
APP_DIR: `apps/verifier/`
PERSONA: `.pi/verifier/agents/verify_sqlite.md`
SCRIPT: `.pi/verifier/scripts/verify_sqlite.py`
PROMPT_TEMPLATE: `.pi/verifier/prompts/verify_on_stop.md`
SETTINGS: `.pi/settings.json`
DEFAULT_MODEL: `anthropic/claude-sonnet-4-6` (per `verify_sqlite.md` frontmatter)

## Codebase Structure

```
the-verifier-agent/
├── apps/verifier/                  # TypeScript extensions (verifiable.ts + verifier.ts + _shared/)
│   ├── package.json                # post-A1: workspace lives here, not at root
│   └── tsconfig.json
├── .pi/
│   ├── settings.json               # { skills, sessionDir }
│   └── verifier/
│       ├── agents/verify_sqlite.md # persona — frontmatter declares model, max_loops, bash_policy
│       ├── prompts/                # verify_on_stop.md, builder_error.md
│       └── scripts/verify_sqlite.py# astral-uv read-only SQLite wrapper (the only allowed bash cmd)
├── justfile                        # default | verifier | sqlite | image | python | prime | clean
└── .env                            # NOT in repo; user creates with provider API keys
```

## Instructions

- Run every check via Bash — do not assume anything is installed.
- Show a one-line pass/fail status after each check.
- Critical deps (`node`, `pi`, `tmux`) gate the install — stop and instruct the user if missing.
- For optional deps (`drive`, `WezTerm`, etc.) note absence but continue.
- For the API key step: confirm a provider key is set in either `process.env` or `.env`. **Never read or print key values** — only confirm presence.
- Do NOT start `pi`, do NOT run any `just v*` recipe, do NOT open windows — this command verifies readiness only.
- If a `.env` doesn't exist, offer to create one with the chosen provider's key as a placeholder (commented), but never write a real key.

## Workflow

### Step 1 — Critical prerequisites (gate)

If any of these are missing, stop and instruct the user before continuing.

1. Check `node`: `command -v node && node --version`. Need ≥ 20. If missing → `brew install node` (macOS) or use a Node version manager (nvm, fnm, volta).
2. Check `pi`: `command -v pi && pi --version`. The Pi Coding Agent CLI. If missing → `npm install -g @mariozechner/pi-coding-agent` (or the user's preferred install path; consult [Pi Coding Agent docs](https://github.com/mariozechner/pi-coding-agent)).
3. Check `tmux`: `command -v tmux && tmux -V`. Need 3.x+. If missing → `brew install tmux` (macOS) or `apt install tmux` (Debian/Ubuntu).

Stop and report each missing critical dep separately so the user can install incrementally.

### Step 2 — Standard prerequisites

These are all required by the verifier script or the `just` recipes; install missing ones via the listed commands.

4. Check `uv` (astral-uv — runs the SQLite verifier script with inline PEP 723 deps):
   `command -v uv && uv --version`. If missing → `curl -LsSf https://astral.sh/uv/install.sh | sh`.
5. Check `python3` (the verifier script's shebang resolves to `uv run --script` which uses Python ≥ 3.11):
   `command -v python3 && python3 --version`.
6. Check `sqlite3`: `command -v sqlite3 && sqlite3 --version`. Used internally by the verifier script for dot-commands like `.schema`.
7. Check `just`: `command -v just && just --version`. Optional but every workflow command in the README runs through justfile recipes — strongly recommended. If missing → `brew install just` (macOS) or [installation instructions](https://github.com/casey/just#installation).

### Step 3 — Optional environment notes

8. Detect terminal emulator: `echo "$TERM_PROGRAM"`. The launcher's per-emulator dispatch knows about Ghostty, iTerm, Apple_Terminal, WezTerm. If `$TERM_PROGRAM` is something else (e.g., `vscode`, `WarpTerminal`), the launcher falls back to a Terminal.app window via `osascript` — also fine.

### Step 4 — Install TypeScript dependencies

10. Run `cd apps/verifier && npm install`. This installs `@mariozechner/pi-coding-agent`, `@mariozechner/pi-tui`, `typebox`, `typescript`, `@types/node` into `apps/verifier/node_modules/`.

### Step 5 — Verify configuration files

11. Persona file exists and frontmatter is parseable:
    - `[ -f .pi/verifier/agents/verify_sqlite.md ] && echo persona-present`
    - The frontmatter must declare `name`, `description`, `tools`, `model`, `domain`, `bash_policy.{mode, allowed_script, runner}`, optionally `max_loops`. The exact contract is enforced at runtime by `apps/verifier/_shared/frontmatter.ts:parseVerifierPersona`.
12. Script file exists and is executable:
    - `[ -f .pi/verifier/scripts/verify_sqlite.py ] && [ -x .pi/verifier/scripts/verify_sqlite.py ] && echo script-executable`
    - If not executable: `chmod +x .pi/verifier/scripts/verify_sqlite.py`.
13. User-prompt template exists:
    - `[ -f .pi/verifier/prompts/verify_on_stop.md ] && echo prompt-template-present`
14. Project settings exist:
    - `[ -f .pi/settings.json ] && python3 -c 'import json; json.load(open(".pi/settings.json"))' && echo settings-valid-json`

### Step 6 — Verify environment / provider API key

15. Default model across all verifier personas is `openai/gpt-5.5` → the canonical key is `OPENAI_API_KEY`. Check it without printing the value:
    - `[ -n "${OPENAI_API_KEY:-}" ] && echo "OPENAI_API_KEY is set in shell env"`
    - If not in shell env, look for a project-local `.env`: `[ -f .env ] && grep -q '^OPENAI_API_KEY=' .env && echo "OPENAI_API_KEY is set in .env"` (don't print the value).
16. If neither check finds it: ask the user which provider they want to use (Anthropic / DeepSeek / OpenAI / etc.). Both extensions auto-load `.env` from `ctx.cwd` on `session_start` and tmux forwards env via `-e KEY=VAL`, so dropping the key into a project-local `.env` Just Works for both agents.
17. If `.env` does not exist, offer to create a stub with placeholder lines for common providers (commented out — user fills in real values themselves):
    ```
    # ANTHROPIC_API_KEY=sk-ant-...
    # DEEPSEEK_API_KEY=sk-...
    # OPENAI_API_KEY=sk-...
    ```
    Never write a real key to disk.

### Step 7 — Final verification (no servers started)

18. Run `cd apps/verifier && npx tsc --noEmit && cd ../..` — must exit 0. Confirms TypeScript compiles cleanly across both extensions and the shared substrate.

### Step 8 — Report

Present a status table per the Report section.

## Report

Present the install result in this format:

```
Pi Verifier Agent — install ready

  ── Critical prerequisites ──────────────────────
  node           ✓ v[version]
  pi             ✓ [version]
  tmux           ✓ [version]

  ── Standard prerequisites ──────────────────────
  uv             ✓ [version]
  python3        ✓ [version]
  sqlite3        ✓ [version]
  just           ✓ [version]

  ── Optional ────────────────────────────────────
  $TERM_PROGRAM  [value — recognized | falls back to Terminal.app]

  ── Configuration ───────────────────────────────
  apps/verifier/node_modules/                    ✓
  .pi/settings.json (valid JSON)                 ✓
  .pi/verifier/agents/verify_sqlite.md           ✓
  .pi/verifier/scripts/verify_sqlite.py (+x)     ✓
  .pi/verifier/prompts/verify_on_stop.md         ✓

  ── Provider key ────────────────────────────────
  [PROVIDER]_API_KEY   ✓ set in [shell env | .env]

  ── Final verification ──────────────────────────
  npx tsc --noEmit  ✓ exit 0

  Ready: [N]/[total] checks passing.

  ── Next steps ──────────────────────────────────
  Prime a fresh agent session:     /prime
  Launch the verifier loop:        just vsql  (or `just v`, `just vpy`, `just vimg`)
  Or attach manually:              run `pi -e ./apps/verifier/verifiable.ts` and type `/verify` in the builder
```

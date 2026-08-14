---
description: Install Multi-Team Chat — prerequisites, dependencies, shell alias, and new-project setup
---

# Install Multi-Team Chat

## Purpose

Fully set up Multi-Team Chat so the user can run it from any directory. Checks prerequisites, installs dependencies, adds a shell alias, and guides new-project setup. This is an interactive, agentic process — ask the user when choices are needed.

## Variables

SOURCE_REPO: The directory this command is running from (the repo root containing `apps/multi-team-chat/`)
EXTENSION_PATH: `apps/multi-team-chat/extensions/multi-team-chat.ts` (relative to SOURCE_REPO)
DEFAULT_ALIAS: `teams`
DEFAULT_SHELL_FILE: `~/.zshrc` or (check if running on macOS: `~/.bash_profile`)

## Instructions

- Run every check via Bash — do not assume anything is installed.
- Show a status line immediately after each check (✅ or ❌).
- For auto-installable items, install them without asking.
- For items requiring user input (alias name, shell file), ask the user with sensible defaults.
- Do NOT read or display API key values — only confirm they are set.
- The shell alias is a function: `alias() { pi -e "/absolute/path/to/multi-team-chat.ts" "$@"; }`
- Before writing to a shell file, check if the alias already exists. If it does, ask the user if they want to update it.
- After everything is installed, print clear next-steps for using it in a new project.

## Workflow

### Step 1 — Check Prerequisites

Run each check and show the result immediately:

1. **Claude Code** — `command -v claude` → if missing: "Install Claude Code: `npm install -g @anthropic-ai/claude-code`" or https://docs.anthropic.com/en/docs/claude-code
2. **Pi coding agent** — `command -v pi` → if missing: "Install Pi: `npm install -g @mariozechner/pi-coding-agent`" or https://pi.dev
3. **Bun** — `command -v bun` → if missing: "Install: `curl -fsSL https://bun.sh/install | bash`"
4. **Node.js** — `command -v node` → if missing: "Install: https://nodejs.org"
5. **just** — `command -v just` → if missing: "Install: `brew install just`"

If any required prerequisite is missing, stop and tell the user what to install. Do not proceed until prerequisites are met.

### Step 2 — Check Environment

1. **`.env` file** — Check if `.env` exists in the project root. If missing: "Run `cp .env.sample .env` and add your API keys."
2. **`ANTHROPIC_API_KEY`** — If `.env` exists, check that `ANTHROPIC_API_KEY` is set (non-empty after `=`). Do NOT display the value.

### Step 3 — Install Dependencies

1. Run `cd apps/multi-team-chat && bun install` to install extension dependencies (dotenv, etc.)
2. Show ✅ when complete.

### Step 4 — Verify Team Config

1. Check that `.pi/multi-team/multi-team-config.yaml` exists.
2. Check that all agent `.md` files referenced in the config exist.
3. Count teams, leads, and members. Show the count.
4. If any agent file is missing, show ❌ with the missing path.

### Step 5 — Install Shell Alias

First, detect the user's shell and pick the right config file automatically:

```bash
# Detect shell config file
echo $SHELL          # /bin/zsh or /bin/bash
echo $0              # Current shell
```

- If zsh → `~/.zshrc`
- If bash on macOS → `~/.bash_profile`
- If bash on Linux → `~/.bashrc`

Then ask the user two questions:

1. **"What alias do you want for Multi-Team Chat?"** — Default: `teams`. The user types the command name they'll use to launch it.
2. **"I detected your shell is [zsh/bash]. I'll add the alias to [detected file]. OK, or would you prefer a different file?"** — Show detected default + alternatives:
   - `~/.zshrc`
   - `~/.bash_profile`
   - `~/.bashrc`
   - Other (let them type a path)

Then:

1. Resolve the absolute path to the extension: `$(cd <SOURCE_REPO> && pwd)/apps/multi-team-chat/extensions/multi-team-chat.ts`
2. Check if the alias already exists in the shell file (`grep -q "^<alias>()" <shell_file>`)
3. If it exists, ask the user: "Alias '<alias>' already exists. Update it? (y/n)"
4. Append to the shell file:
   ```
   # Multi-Team Chat — pi-based multi-agent orchestration
   <alias>() { pi -e "<absolute_extension_path>" "$@"; }
   ```
5. Show ✅ and remind them to `source <shell_file>`.

### Step 6 — Report

Show the final summary, then next steps:

```
Multi-Team Chat — Install Complete

  [status] Claude Code
  [status] Pi coding agent
  [status] Bun
  [status] Node.js
  [status] just
  [status] .env + ANTHROPIC_API_KEY
  [status] Extension dependencies
  [status] Team config ([N] teams, [N] agents)
  [status] Shell alias '<alias>' → <shell_file>

Ready: [count]/[total]

Next steps:

  source <shell_file>

  # Test in this project:
  <alias>

  # Next run this command to install a new team into a new codebase:
  /install-into-codebase
```

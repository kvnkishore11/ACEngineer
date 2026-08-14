---
description: Check and install all dependencies for the CEO Agents project
---

# Install

## Purpose

Diagnose and install all dependencies required to run the CEO & Board deliberation system. Checks for each prerequisite, installs what's possible automatically, and guides the user on manual steps (like API keys).

## Instructions

- Check each dependency in order — do NOT skip checks even if earlier ones fail.
- For each check, output a status line immediately: green checkmark if present, red X if missing.
- If a dependency can be auto-installed (like bun packages), do it automatically after confirming with the user.
- If a dependency requires manual action (like API keys), show clear instructions but do NOT block on it.
- Use `which` or `command -v` to check CLI tools.
- Do NOT modify `.env` — only check if it exists and has keys set.
- Run all checks before attempting any installs.
- After all checks and installs, show a final summary.

## Workflow

1. **Check Pi coding agent** — Run `command -v pi` to verify Pi is installed. If missing, show install instructions: "Install Pi: `npm install -g @mariozechner/pi-coding-agent`" and link to https://pi.dev
2. **Check Bun** — Run `command -v bun` to verify Bun is installed. If missing, show: "Install Bun: `curl -fsSL https://bun.sh/install | bash`"
3. **Check just** — Run `command -v just` to verify just is installed. If missing, show: "Install just: `brew install just`"
4. **Check .env file** — Check if `.env` exists in the project root. If missing, show: "Run `cp .env.sample .env` and add your API keys." If it exists, check that `ANTHROPIC_API_KEY` is set (non-empty value after the `=`). Do NOT read or display the actual key value — just confirm it's set or not.
5. **Check node_modules** — Check if `apps/ceo/node_modules/` exists. If missing, run `cd apps/ceo && bun install` to install dependencies automatically.
6. **Check configuration** — Verify `.pi/ceo-agents/ceo-and-board-configuration.yaml` exists. If missing, show error — this means the repo is incomplete.
7. **Check board member agents** — Verify at least 2 agent `.md` files exist in `.pi/ceo-agents/agents/`. List the active board members found.
8. **Check briefs** — Count available brief directories in `.pi/ceo-agents/briefs/` (directories containing a `brief.md`). Show the count.
9. **Check Pi theme** — Verify `apps/ceo/.pi/themes/synthwave.json` exists. If missing, warn that the synthwave theme won't load.
10. **Check ElevenLabs (optional)** — If `.env` exists, check if `ELEVENLABS_API_KEY` is set. If not, note it as optional: "TTS audio summaries require an ElevenLabs API key. Get one at https://elevenlabs.io/app/settings/api-keys"
11. Now follow the `Report` section to report the completed work.

## Report

Present the results in this format:

```
CEO Agents — Install Check

  [status] Pi coding agent
  [status] Bun
  [status] just
  [status] .env file
  [status] ANTHROPIC_API_KEY
  [status] Node dependencies (apps/ceo)
  [status] Board configuration
  [status] Board members ([count] active)
  [status] Briefs ([count] available)
  [status] Synthwave theme
  [status] ElevenLabs API key (optional)

Ready: [count]/[total]

[If all required checks pass:]
All systems go. Run `just ceo` to launch, then `/ceo-begin` to start a deliberation.

[If any required checks fail:]
Action needed:
- [list each failed check with its fix instruction]
```

Use checkmark for pass, X for fail, and a dash for optional items that are missing.

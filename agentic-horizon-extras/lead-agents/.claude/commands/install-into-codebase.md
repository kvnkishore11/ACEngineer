---
description: Deploy a fresh Multi-Team Chat team configuration into a new codebase
---

# Install Into Codebase

## Purpose

Deploy the Multi-Team Chat scaffolding into a target codebase so users can run their agent teams in a new project. Copies agent prompts, skills, and team config — but creates fresh empty directories for expertise and sessions so agents build new mental models from scratch.

## Instructions

- This is an interactive command — always ask the user for the target path.
- Validate the target path exists and is a directory before proceeding.
- If `.pi/multi-team/` already exists in the target, warn the user and ask before overwriting. Show exactly what will be replaced.
- Copy the empty expertise placeholder files so agents have valid paths on first boot. Agents will populate these with their own mental models over time.
- NEVER copy session files — create an empty `sessions/` directory.
- Use `cp` commands via Bash for file operations. Copy directories recursively where needed.
- After copying, verify the key files landed correctly.
- Add `.pi/multi-team/sessions/` to the target's `.gitignore` — append if `.gitignore` exists, create it if not. Check if the entry already exists before adding to avoid duplicates.

## Workflow

### Step 1 — Ask for Target

1. Ask the user: **"Where do you want to deploy the team? Enter the absolute path to your target codebase."**
2. Validate the path exists and is a directory using Bash (`test -d`).
3. If invalid, tell the user and ask again.

### Step 2 — Check for Existing Config

1. Check if `<target>/.pi/multi-team/` exists.
2. If it exists, warn:
   - Show that `agents/`, `skills/`, and `multi-team-config.yaml` will be overwritten
   - Note that `expertise/` and `sessions/` will NOT be touched if they already exist
   - Ask: **"This codebase already has a team config. Overwrite agents, skills, and config? (y/n)"**
3. If the user declines, stop.

### Step 3 — Copy Team Scaffolding

Run the following Bash commands:

1. Create the target directory structure:
   ```
   mkdir -p <target>/.pi/multi-team/
   ```
2. Copy `agents/` directory (all `.md` system prompts):
   ```
   cp -R <source>/.pi/multi-team/agents/ <target>/.pi/multi-team/agents/
   ```
3. Copy `skills/` directory (all composable skill `.md` files):
   ```
   cp -R <source>/.pi/multi-team/skills/ <target>/.pi/multi-team/skills/
   ```
4. Copy `multi-team-config.yaml`:
   ```
   cp <source>/.pi/multi-team/multi-team-config.yaml <target>/.pi/multi-team/multi-team-config.yaml
   ```
5. Copy expertise placeholder files (empty `.yaml` files so agent domain paths resolve on first boot):
   ```
   cp -R <source>/.pi/multi-team/expertise/ <target>/.pi/multi-team/expertise/
   ```
6. Create empty directories (only if they don't already exist):
   ```
   mkdir -p <target>/.pi/multi-team/sessions/
   mkdir -p <target>/specs/
   mkdir -p <target>/apps/
   ```
6. Create shared context files if they don't already exist (these are referenced in `multi-team-config.yaml` under `shared_context`):
   ```
   touch <target>/README.md
   touch <target>/CLAUDE.md
   ```
   Only create them if they don't exist — do NOT overwrite existing files.

### Step 4 — Environment File

1. Check if a `.env` file exists in the source repo (cwd).
2. Check if a `.env` already exists in `<target>`.
3. If source `.env` exists and target `.env` does NOT:
   - Ask: **"Found .env in the source repo. Copy it to the target? This contains your ANTHROPIC_API_KEY. (y/n, default: y)"**
   - If **yes** (default): `cp <source>/.env <target>/.env`
   - If **no**: remind them to create one manually: `cp .env.sample .env` or set `ANTHROPIC_API_KEY` in the target's `.env`.
4. If source `.env` exists and target `.env` ALSO exists: skip — tell the user the target already has a `.env`.
5. If no source `.env` exists: remind them they'll need to create a `.env` with `ANTHROPIC_API_KEY` in the target before launching.

### Step 5 — Update .gitignore

1. Ask the user: **"Do you want to track agent sessions in git? Tracking sessions preserves conversation history and agent context across commits, but will increase repo size over time. (y/n, default: n)"**
2. If **no** (default): add `.pi/multi-team/sessions/` to `.gitignore`.
   - Check if `<target>/.gitignore` exists. If not, create it.
   - Check if the entry already exists to avoid duplicates.
   - If not present, append:
     ```
     # Multi-Team Chat — agent session data
     .pi/multi-team/sessions/
     ```
3. If **yes**: skip — sessions will be committed with the repo.

### Step 6 — Verify

1. Count the agent files in `<target>/.pi/multi-team/agents/` — confirm all `.md` files landed.
2. Count the skill files in `<target>/.pi/multi-team/skills/` — confirm all `.md` files landed.
3. Confirm `multi-team-config.yaml` exists in the target.
4. Confirm `expertise/` and `sessions/` directories exist.

### Step 7 — Report

Present the deployment summary in this format:

```
Multi-Team Chat — Deployed to <target>

  Copied:
  ✅ agents/                [N] agent prompts
  ✅ skills/                [N] skill files
  ✅ multi-team-config.yaml

  Created:
  ✅ expertise/             [N] empty placeholder files — agents will populate
  ✅ sessions/              (empty — created on first run)
  ✅ specs/
  ✅ apps/
  ✅ README.md              (created | already existed)
  ✅ CLAUDE.md              (created | already existed)

  Environment:
  ✅ .env                   (copied | skipped | needs manual setup)
  ✅ .gitignore             (sessions/ excluded | sessions/ tracked)

Next steps:

  1. Edit .pi/multi-team/multi-team-config.yaml to add, remove, or rename teams
  2. Edit .pi/multi-team/agents/*.md to customize your orchestrator, team leads, and worker agents for your project
  3. Launch from this directory:

     cd <target>
     teams
```

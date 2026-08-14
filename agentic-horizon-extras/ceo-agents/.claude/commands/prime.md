---
description: Prime context for the CEO & Board strategic decision agents codebase
---

# Purpose

Explore the CEO Agents project — a multi-agent deliberation system built on pi coding agent where a CEO agent orchestrates board member conversations to make high-leverage strategic decisions.

## Workflow

1. Run `git ls-files | head -100` using the Bash tool to see the project structure
2. Read `README.md` and `CLAUDE.md` for project overview and rules
3. Read `specs/init.md` to understand the full system design: tools (`converse`, `end_deliberation`), subagent architecture, file formats (briefs, memos, .jsonl conversation logs), and directory structure
4. Read `.pi/ceo-agents/ceo-and-board-configuration.yaml` to see the active board members, meeting constraints, and configured paths
5. Read `.pi/ceo-agents/agents/` to understand the directory structure of board member system prompts, briefs, deliberations, and memos
6. Read `.pi/ceo-agents/agents/ceo.md` to understand the CEO agent's system prompt, workflow, and decision-making heuristics
7. Read `apps/ceo/extensions/ceo-and-board.ts` (first 100 lines) to understand the pi extension entry point and imports
8. Read `justfile` to see available commands for launching the system
9. Summarize your understanding of the project: purpose, stack, structure, key files, entry points, and how a deliberation flows from brief → board conversation → memo

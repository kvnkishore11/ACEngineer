---
description: Prime context for the Multi-Team Chat orchestration system
---

# Purpose

Explore the Multi-Team Chat project -- a multi-agent orchestration system built on Pi coding agent where a user talks to an Orchestrator who delegates to specialized teams (Planning, Engineering, Validation), each with a Lead + Members. The UI uses a "nuclear" pattern that replaces Pi's chat display with a custom Slack-like experience.

## Workflow

1. Run `git ls-files | head -100` using the Bash tool to see the project structure
2. Read `README.md` and `CLAUDE.md` for project overview and rules
3. Read `ai_docs/pi-agent/owning-the-pi-ui.md` -- the nuclear UI takeover pattern: how we replace Pi's chatContainer via `tui.children[1]` to build a fully custom chat interface while keeping Pi's agent brain intact
4. Read `ai_docs/pi-agent/rendering-internals.md` -- Pi's rendering pipeline and constraints: how components render, invalidation, scroll, and why the nuclear pattern works
5. Read `.pi/multi-team/multi-team-config.yaml` -- team configuration: Orchestrator, 3 teams (Planning, Engineering, Validation), each with a Lead + Members, colors, domain permissions
6. Read `.pi/multi-team/agents/orchestrator.md` -- the Orchestrator system prompt: how it classifies requests, routes to ONE team, synthesizes output, and decides when to answer directly
7. Read `.pi/multi-team/skills/conversational-response.md` -- the response skill: tells agents to write like Slack messages, keep chat concise, push detail to files
8. Read `apps/multi-team-chat/extensions/multi-team-chat.ts` (first 100 lines) -- the nuclear takeover entry point: ChatMsg type, tool emoji map, config loading, stats tracking
9. Read `apps/multi-team-chat/extensions/modules/subprocess.ts` -- how team members are called: Pi subprocess spawning with `--mode json`, persistent sessions, streaming text/tool callbacks, usage tracking
10. Read `apps/multi-team-chat/extensions/modules/config.ts` (first 50 lines) -- config parsing: project root detection, YAML parsing, skill loading via frontmatter
11. Read `justfile` for available commands -- `just multi` launches the system
12. Summarize your understanding:
    - **Purpose**: Multi-agent orchestration with depth-2 delegation (User -> Orchestrator -> Team Leads -> Members)
    - **Architecture**: Orchestrator classifies and routes to one of 3 teams; leads can delegate to members; all agents are Pi subprocesses with persistent sessions
    - **Key files**: `multi-team-chat.ts` (entry point), `subprocess.ts` (agent calling), `config.ts` (YAML + skills), `multi-team-config.yaml` (team roster), agent prompts in `.pi/multi-team/agents/`
    - **Nuclear UI pattern**: Replace `tui.children[1]` to build custom chat with colored avatars, @mentions, tool emojis, streaming indicators, scroll
    - **Delegation flow**: User message -> Orchestrator classifies -> delegates to team lead via `delegate` tool -> lead optionally consults members -> response bubbles back up -> Orchestrator synthesizes for user
    - **Skills system**: Composable markdown skills declared in agent frontmatter, injected into system prompts at load time

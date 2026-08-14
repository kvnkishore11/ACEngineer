# STATUS — `ma-2-lead-agents`

**Status:** DONE
LENS: agent-systems
**Output:** `book/code/ma-2-lead-agents.html`
**Lesson:** Multi-Team Agentic Coding / Lead Agents
**Date:** 2026-07-13

## Agent interfaces covered

- **Human commander interface:** `/install`, `just team-list`, `just team`, `just team-pe`, `just teamc <path>`, one Orchestrator chat surface, acceptance from receipts.
- **Prompt contract:** `.pi/multi-team/agents/*.md` identity, model, tools, domain, expertise, runtime placeholders, routing and synthesis instructions.
- **Skill contract:** `active-listener`, `conversational-response`, `high-autonomy`, `mental-model`, `precise-worker`, and `zero-micro-management` as composable soft behavior.
- **Roster/config contract:** `.pi/multi-team/*-config.yaml` for Orchestrator, team, lead, member, path, color, shared context, and routing metadata.
- **Tool contract:** Orchestrator/lead `delegate` + `tilldone`; worker read/write/edit/bash/search tools; role-specific separation of coordination and execution.
- **Permission contract:** tool allowlist, path-scoped read/upsert/delete rules, exact expertise ownership, line limits, default-deny path behavior, and the bash heuristic caveat.
- **Harness/launcher contract:** `justfile`, `multi-team-chat.ts`, resolved prompt injection, Pi JSON subprocesses, explicit child extensions, environment-variable capability injection, and depth-2 recursion cap.
- **Memory/context contract:** shared `README.md` / `CLAUDE.md`, per-seat expertise files, full conversation log, persistent per-agent session JSONL.
- **Verification contract:** direct and delegated ping smoke tests, `/toggle-workers`, TillDone completion, domain-denial evidence, session logs, filesystem/tests, team cost footer, and provider-dashboard cross-check.
- **Recovery contract:** named config/path errors, clean process relaunch, stale-session avoidance, prompt/config/gate repair, default-config restoration.
- **Build-system boundary:** Claude Code bootloader/meta commands and `Task*` planning flow are distinguished from the Pi runtime’s `delegate`/`tilldone` flow.
- **Scripts-as-agents:** Drive/tmux automation as a repeatable terminal observation harness; SVG/TTS skills acknowledged as artifact producers, not runtime team members.

## Accuracy notes carried into the page

- Shipped default is **3 teams / 10 agents**.
- All 10 shipped expertise files start empty.
- The shipped Frontend and Backend workers both have broad `apps/` ownership; the narrower split was demonstrated live but is not checked in.
- The shipped Orchestrator includes `write`, `edit`, and `tilldone`; the recording shows an earlier state.
- Course-era model IDs are presented as period detail; model tiering is the durable pattern.
- `domain-enforcer.ts` hard-blocks standard file tools by path, but bash checking is heuristic rather than OS-level sandboxing.
- `.claude/commands/prime.md` contains stale `just multi` wording; the executable README/justfile interface is `just team`.
- The worker-cost spec is treated as proof that observability itself must be verified.

## Deliverable checks

- Uses required shared CSS: `tokens.css`, `base.css`, `components.css`, `chrome-v2.css`.
- Includes compact site bar links to Chapter 16, code library, and book hub.
- Includes mission, cast, surface map, in/out-of-loop control loop, four agent contracts, real operating commands, failures, agent-ops lab, six-sentence teach-back, and collapsed 200-file raw index.
- Code excerpts are limited to prompt/permission/launcher evidence; no file-by-file source tour.
- All output for this task is under `IndyDevDan/book/`.

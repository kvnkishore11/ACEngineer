# STATUS: COMPLETE

LENS: agent-systems

Lesson key: `ah-5-agent-experts`
Title: `Agent Experts`
Deliverable: `IndyDevDan/book/code/ah-5-agent-experts.html`
Reworked: 2026-07-13

## Agent interfaces covered

- Human commander boundary: domain choice, outcome, authority, spend, evidence review, recovery, and the prohibition on hand-editing learned expertise.
- Prompt contracts: database/WebSocket question, plan, build, composite plan-build-improve, and self-improve command surfaces.
- Project context contracts: root `CLAUDE.md`, nested orchestrator `CLAUDE.md`, and topic-scoped expertise files.
- Tool contracts: slash-command `allowed-tools`, orchestrator SDK allowlists, Nile’s two-tool MCP surface, and explicit general-tool denials.
- Permission/guardrail contracts: SDK `acceptEdits`/`bypassPermissions`, root hook wiring, dangerous-`rm` prevention, and the distinction between observation and enforcement.
- Persistent-state contracts: database and WebSocket YAML mental models, orchestrator sessions/PostgreSQL state, and Nile’s per-user SQLite JSON expertise.
- Harness/launcher contracts: `start_be.sh`, `start_fe.sh`, `start-orchestrator/SKILL.md`, `ClaudeSDKClient`, `ClaudeAgentOptions`, and in-process MCP servers.
- Multi-agent handoffs: fresh plan → build → self-improve stages, plan-path and diff artifacts, command-agent lifecycle, and context delegation.
- Verification contracts: source revalidation, Git diff, line budget, YAML parse, frontend build, backend tests, real-agent Nile tests, WebSocket observers, and browser validation.
- Recovery contracts: accept justified no-op learning, tighten prompts/tools, repair the self-improve rubric, rerun/reseed, or reject learned-state changes.
- Deterministic operator interfaces: migrations, model synchronization, configuration copying, and service launch scripts.
- Product-expert interface: behavior signals → injected prompt context → constrained shopping tools → streamed UI sections.

## Source discipline

- Inventoried the complete checked-out text surface under `agentic-horizon/agent-experts/`, read the operating and source contracts thoroughly, and excluded binary product images from text analysis.
- Confirmed `.upstream/` is an identical mirror of the current repository tree and did not treat duplicated files as distinct contracts.
- Read `_extracts/ah-5-agent-experts/`, including mission, nuggets, lab, frame plan, accuracy flags, and current-practice notes.
- Read the sibling conceptual chapter at `vol-2-ah/13-agent-experts.html`; the companion links to it and avoids repeating its full conceptual treatment.
- Used only real repository paths in the page.
- Kept all authored deliverables under `IndyDevDan/book/`.

## Accuracy decisions surfaced in the page

- `start-orchestrator/SKILL.md` still names backend port 8002 while `start_be.sh` and the root README default to 9403.
- Both self-improve prompts show raw `python3` for YAML parsing while root `CLAUDE.md` requires all Python execution through Astral UV.
- Nile documentation says JSONB, while the checked-out implementation uses SQLAlchemy `JSON` in a SQLite database.
- WebSocket expertise calls `chatService.ts` a 194-line file; the checked-out file has 193 lines.
- Root `.claude/settings.json` is a hook map, not a comprehensive permission policy.
- The environment-file block in `pre_tool_use.py` is commented out; it is not presented as active protection.
- `send_event.py` is observability with graceful failure, not a blocking verifier.
- The shipped WebSocket event counter is treated as completed-loop archaeology, not a fresh lab task.

## Page structure delivered

1. Compact site bar linking chapter, code library, and hub.
2. One-paragraph agent mission card.
3. Cast-of-agents authority table.
4. Agent surface-map infographic.
5. In-loop/out-of-loop control diagram.
6. Prompt, tool/permission, harness, and verification contracts with short evidence snippets and Dan’s design intent.
7. README-grounded operating runbook and worked loop trace.
8. Agent-system failure matrix with repairs.
9. Agent-ops lab that changes prompt/tool/verifier contracts only.
10. Six-sentence closed-notes teach-back plus collapsible model answer.
11. Collapsible agent-interface file index.

## Verification

- Required stylesheet links present: `../design/tokens.css`, `base.css`, `components.css`, and `chrome-v2.css`.
- Site-bar links resolve to the sibling chapter, code library, and book hub.
- All local fragment links resolve and all section IDs are unique.
- Inline JavaScript parses and targets existing progress/active-section elements.
- HTML uses responsive fallbacks, reduced-motion handling, semantic tables/details, and print rules.
- Prompt/settings snippets are the only syntax-highlighted evidence blocks.
- No lesson-codebase file was modified; only the two requested book deliverables were authored.

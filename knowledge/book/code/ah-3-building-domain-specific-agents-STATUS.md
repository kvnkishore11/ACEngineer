# STATUS: REWORKED ✅

Lesson key: `ah-3-building-domain-specific-agents`  
Output: `code/ah-3-building-domain-specific-agents.html`  
LENS: agent-systems

## Agent interfaces covered

- Human commander boundary: intent, authority, task-shape judgment, and final acceptance.
- Prompt contracts: overwrite vs `claude_code` preset vs preset + `append`; static system values vs per-call user values.
- Core-four configuration: context, model, prompt, and tools through `ClaudeAgentOptions`.
- Tool contracts: `@tool`, in-memory MCP registration, qualified tool names, and deterministic return/error evidence.
- Permission contracts: `allowed_tools`, `disallowed_tools`, `cwd`, permission modes, repo-level command hooks, and SDK inline hooks.
- Context and memory: tool-definition cost, optional MCP context, session IDs, `resume=`, persisted state, bounded reads, and raw-data caching.
- Harnesses and launchers: one-off `query()`, `ClaudeSDKClient`, CLI entrypoints, FastAPI backends, async stream loops, and the Micro SDLC controller.
- Multi-agent handoffs: QA Task subagents; planner → spec path → builder → reviewer; Stream producer → persisted logs → Inspector consumer.
- Verification surfaces: response blocks, result metadata, direct hook tests, diffs, review artifacts, WebSocket state, SQLite/CSV persistence, and observable error states.
- Recovery paths: hook denial, restart after prompt change, retry, context reconnect, Errored state, and human escalation.
- Configuration wiring audit: outer `.claude/settings.json` vs embedded SDK options; present-but-unmounted `context_bundle_builder.py`.
- Current-source corrections: Claude Agent SDK rename, QA Firecrawl sample rename, Micro SDLC `specs/` output, and Ultra Stream frontend port 5175.

## Page structure delivered

1. Compact site bar linking chapter, code library, and book hub.
2. One-paragraph agent mission card.
3. Cast of agents and eight-agent capability ladder.
4. Agent surface-map infographic.
5. In-loop vs out-of-loop control-loop diagram.
6. Prompt, tool/permission, harness, and verification contract sections with short source evidence and Dan's design intent.
7. Worked Micro SDLC run plus real README entrypoints for all eight agents.
8. Agent-system failure modes, including the shipped review-without-gating gap.
9. QA prompt-contract operations lab with observable pass criteria.
10. Six-sentence teach-back and collapsible complete file index.

## Source discipline

- Read the full `agentic-horizon/building-specialized-agents` tree, excluding dependency directories and treating lock/data artifacts as indexes rather than teaching prose.
- Prioritized real prompts, settings, hooks, slash commands, launchers, READMEs, agent options, tests, state stores, and generated handoff artifacts.
- Consumed `_extracts/ah-3-building-domain-specific-agents/`, including mission and outdated/current flags.
- Used `vol-2-ah/11-building-domain-specific-agents.html` as the conceptual spine without duplicating its full chapter treatment.
- All named paths in the page exist in the lesson codebase.
- No files were written outside `IndyDevDan/book/`.

## Accuracy notes surfaced in the page

- Current runnable naming is `claude-agent-sdk` / `claude_agent_sdk` / `ClaudeAgentOptions`; the recording uses the former Claude Code SDK naming.
- Root command hooks and embedded SDK inline hooks are separate governance layers.
- `allowed_tools` gates calls; explicit `disallowed_tools` removes named built-ins from the agent's visible context.
- The shipped Micro SDLC transitions to Shipped after reviewer completion without parsing a verdict or requiring a behavioral test gate.
- Ultra Stream's `clear_context` tool resets a counter and emits status; the outer loop performs disconnect/reinitialize behavior at its threshold.

## Verification

- Rendered and inspected at 1440 × 1000 and 390 × 844; the narrow layout collapses the rail and preserves horizontal table access.
- Rendered a nine-page print artifact; navigation chrome and the keyboard skip link are suppressed in print.
- Confirmed one `<h1>`, ten teaching sections, valid internal fragments, existing local navigation/CSS targets, and parseable inline JavaScript.
- Compared the appendix with the source tree: 152 lesson files indexed, with zero missing or extra entries.
- `git diff --check` passes for both deliverables.

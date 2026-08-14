# STATUS: REWORKED ✅

Lesson key: `ah-4-multi-agent-orchestration-the-o-agent`  
Output: `code/ah-4-multi-agent-orchestration-the-o-agent.html`  
LENS: agent-systems

## Agent interfaces covered

- Human commander boundary: outcome, `--cwd`, acceptable cost/risk, acceptance evidence, and escalation authority.
- Orchestrator prompt contract: full meta-agent overwrite, delegation boundary, eight-tool vocabulary, template-map injection, context compaction, and monitor/report behavior.
- Fleet management tools: `create_agent`, `list_agents`, `command_agent`, `check_agent_status`, `delete_agent`, `interrupt_agent`, `read_system_logs`, and `report_cost` through the in-memory `mgmt` MCP server.
- Managed primary-agent contract: name, custom/template prompt, model, working directory, own session, re-prompting, status, cost, and persistent artifacts.
- Primary agents versus nested Task subagents: promoted templates receive a durable lifecycle; Task subagents remain inside a managed worker run.
- Template surface: fast/Sonnet scouts, builder, reviewer, meta-agent, docs scraper, and Playwright validator with their real model/tool frontmatter.
- Workflow prompts: one-shot lifecycle, scout → build, and plan → build → review with prompt-driven sleep/check monitoring and response → Stop completion evidence.
- Programmable-agent surface: the inner `meta-prompt` skill, prompt template, examples, and command discovery under `<cwd>/.claude/commands/`.
- Tool and permission contracts: orchestrator and worker `allowed_tools`, worker `disallowed_tools`, `permission_mode="acceptEdits"`, project setting sources, optional MCP servers, and cwd blast radius.
- Harness and launcher: `start_be.sh`, `--session`, `--cwd`, FastAPI fire-and-forget trigger, `OrchestratorService`, `AgentManager`, `ClaudeAgentOptions`, `ClaudeSDKClient`, session resume, and background managed-agent execution.
- Context and memory: project files, prompt text, template registry, slash commands, persisted session IDs, Postgres fleet state, prompt/log/chat history, context bars, compacting, and stateless Haiku event summaries.
- Verification plane: inline lifecycle hooks, real database tests, WebSocket events, EventStream agent/tool/category/regex filters, status/cost/context cards, Consumed/Produced files, inline diffs, one-click IDE open, validation commands, and reviewer PASS/FAIL.
- Recovery paths: re-command, compact, interrupt, archive/replace, bounded repair, independent re-review, and human escalation.
- Agent-system audit gaps: template allowlists widen on the current resume path; response → Stop proves completion rather than correctness; the shipped review workflow reports FAIL without repair; optional MCP-backed template tools can be absent; and root/inner docs contain stale port/model details.
- Current source truth: backend 9403, frontend 5175, `claude-agent-sdk`, Sonnet 4.5/Haiku 4.5 code defaults, and `modules/hooks.py` as legacy/orphan relative to the active hook modules.

## Page structure delivered

1. Compact site bar linking the chapter, code library, and book hub.
2. One-paragraph agent mission card with the human/O-agent/worker boundary.
3. Cast table covering commander, O-agent, managed agents, Task subagents, phase specialists, stateless summarizer, and deterministic harness/observer scripts.
4. Three-lane agent surface map for program, mount, and observe interfaces, with `--cwd` as the capability boundary.
5. In-loop versus out-of-loop control-loop diagram plus real PITER mapping.
6. Worked plan → build → review run with human responsibilities and concrete receipts.
7. Prompt, tool/permission, harness/launcher, and verification contract sections using short source evidence only.
8. Real top-level README setup/run commands and source-truth notes for stale documentation.
9. Agent-system failure modes, including the resume allowlist drift and open verifier loop.
10. Prompt-only agent-ops lab that adds one bounded repair and independent re-review pass.
11. Six-sentence teach-back and collapsible agent-interface index.

## Source discipline

- Inventoried the full `agentic-horizon/multi-agent-orchestration` tree, excluding dependency directories and treating binaries, model weights, locks, caches, runtime logs, and generated reference docs as artifacts rather than lesson prose.
- Read the root and app READMEs, both CLAUDE instruction layers, environment/MCP configuration, root settings and hooks, all inner agent templates, orchestration commands, the full meta-prompt skill and examples, backend prompts/options/launchers/hooks/persistence, observer UI surfaces, tests, database runner/schema, supplied AH-4 extracts, and the sibling Volume II chapter.
- Used `vol-2-ah/12-multi-agent-orchestration-the-o-agent.html` only for the conceptual spine; the companion does not reproduce its full chapter treatment.
- All named paths in the page exist in the lesson codebase.
- All writes are confined to `IndyDevDan/book/`.

## Accuracy notes surfaced in the page

- `--cwd` selects the custom template registry and slash-command discovery roots and becomes every managed agent's working directory.
- The inner app directory contains the `review-agent` and orchestration workflows used by the lesson; the root `.claude` layer is a broader interactive Claude Code setup.
- Managed-agent creation honors a template's tools, but `command_agent()` resumes with the comprehensive default allowlist. Read-only templates are therefore not reliably least-privilege after re-command.
- `delete_agent` is a soft archive in the database; produced artifacts persist after the agent leaves the active fleet.
- The prompt-driven completion signal is a response event followed by a Stop hook. It proves the run ended, not that acceptance criteria passed.
- The current plan/build/review command reports PASS/FAIL but has no repair/re-review branch; the lab closes that loop with a single bounded pass.
- The optional Playwright/Firecrawl/Neon tools require MCP configuration; a template definition alone does not mount its tool servers.
- The top README, `config.py`, launcher, and frontend agree on backend 9403/frontend 5175; the inner CLAUDE.md port 8002 line is stale.
- The O-agent prompt's older Haiku alias text is stale relative to `config.py` and `agent_manager.py`.

## Verification completed

- Parsed the inline script, found 24 unique IDs, resolved all 12 unique fragment targets across 23 links, and found no duplicate or missing targets.
- Confirmed all four stylesheet/navigation targets and all 117 paths in the collapsible agent-interface index exist locally.
- Rendered the page in local Chrome at desktop width and in DevTools' iPhone 14 Pro Max emulation; the rail becomes a compact contents disclosure and multi-column surfaces stack at the mobile breakpoint.
- Exercised all three disclosure controls and verified the mobile contents, six-sentence answer, and raw index expand without layout loss.
- Exercised rail navigation, sticky chrome, and reading progress; changed active-section selection to use the section nearest the reading line so bottom-of-page links do not retain the prior highlight.
- DevTools reported zero page console messages. Its device emulator emitted a Chrome-only `file:` unique-origin warning while framing the local document; this is not thrown by the companion script.
- The preferred in-app Node browser bridge was unavailable because its MCP call lacked sandbox policy metadata, so direct local Chrome plus DevTools emulation supplied the visual pass.
- Parallel specification review found no blocking gaps. Standards review findings were resolved before handoff: diagram descendants remain exposed to assistive technology, mobile retains local navigation, the summarizer's unenforced tool boundary is explicit, and page typography uses the shared book tokens.

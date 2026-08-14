# Elite Context Engineering companion — status

STATUS: REWORKED

LENS: agent-systems

## Deliverable

- `code/ah-1-rd-framework-context-window-mastery.html`

## Agent interfaces covered

- Human commander boundary: purpose, scope, authority, budget, acceptance, and recovery
- Interactive primary Claude Code agent
- Sub-agents: `docs-scraper`, `research-agent`, and `meta-agent`
- Planner/builder separation through `/quick-plan` and `/build`
- Independent primary delegation through `/background` and `claude --print`
- Prompt contracts in `.claude/commands/`, `.claude/agents/`, and output styles
- Memory/context contracts: `CLAUDE.md`, task primes, reset-and-prime, and context bundles
- Tool/permission contracts: command/agent allowlists, MCP samples, strict MCP launch, API-key surfaces, and permission bypass risk
- Harnesses/launchers: TypeScript SDK `query()` wrapper, CLI prompt registry, background command, and shell helper
- Verification interfaces: package typecheck/test scripts, `git diff --stat`, hook JSONL, context bundles, report progress, and complete/failed terminal state
- Recovery loop: repair the plan, clear polluted state, replay a bundle, or replace the working agent
- Expert learning loop: plan → build → improve, with `## Expertise` as the allowed mutation boundary

## Source audit

- Read all 53 real files in `agentic-horizon/elite-context-engineering` (6,745 newline-counted text lines; the one-line `apps/cc_ts_wrapper/index.ts` has no trailing newline).
- Read the sibling chapter `vol-2-ah/09-rd-framework-context-window-mastery.html` and its chapter asset CSS for the conceptual spine.
- Read the lesson extract, lab spec, nuggets, frame plan, status, and `outdated-vs-current.md` under `book/_extracts/ah-1-rd-framework-context-window-mastery/`.
- Read the existing archived file-lens companion only as a source audit and visual-shell reference; the new page does not use its file-by-file teaching lens.

## Course-era and repository caveats surfaced

- `quick-plan.md` pins the course-era model ID `claude-opus-4-1-20250805`; the page treats model IDs and token counts as period detail.
- `--dangerously-skip-permissions` appears in the primary-delegation examples; the page treats it as explicit high-risk authority, not a default.
- The active concise `CLAUDE.md` names absent app directories and root commands without matching root scripts, demonstrating that small context can still be stale.
- The generated wrapper README runs `index.ts`, but that real file is only a Bun hello placeholder; the agent CLI lives in `cli.ts`.
- `scripts/bg_claude_code_test.sh` reuses argument 2 for both model and report path, assumes an unshipped active `.mcp.json`, and does not background itself; the lab hardens this agent interface.
- `core.ts` treats a completed SDK stream as success unless an exception occurs; the page identifies explicit result-subtype verification as a missing loop closure.
- Universal hook logs contain full payloads and therefore require privacy, retention, and access controls even though runtime logs are ignored by git.

## Page structure check

- Compact site bar links to chapter, code library, and book hub
- One-paragraph agent mission card
- Cast-of-agents table
- Agent surface map infographic
- In-loop/out-of-loop plan → act → verify → recover diagram
- Four agent contract sections with short source excerpts and Dan’s design intent
- Real operating sequence using repository commands
- Agent-system failure taxonomy
- Agent-ops launcher lab with observable pass criteria
- Six-sentence teach-back
- Collapsible one-line index of all 53 real files

## Validation

- JavaScript parses successfully; the page contains 10 lesson sections, 10 matching rail links, and 2 inline SVG diagrams.
- All fragment targets are present and unique; all local stylesheet, chapter, library, and hub links resolve.
- The appendix contains 53 unique source paths, and every path exists in the lesson codebase.
- Desktop/mobile browser capture was attempted through both the in-app browser and installed Chrome. The managed workspace aborted both browser runtimes before page load, so visual screenshot QA was not available; responsive behavior was checked from the loaded CSS and page media queries instead.

# Seven Levels Agentic Prompt Formats companion — status

STATUS: REWORKED

LENS: agent-systems

## Deliverable

- `code/ah-2-seven-levels-agentic-prompt-formats.html`

## Agent interfaces covered

- Human commander boundary: mission, scope, lowest-capability level, authority, acceptance, and escalation
- Interactive Claude Code primary agent
- Task fan-out and stateless parallel sub-agents
- Specialist system-prompt agents: `docs-scraper`, `meta-agent`, and `crypto-coin-analyzer`
- Independent background primary through `claude --print`
- Scripts-as-agents: lifecycle hooks, context-bundle recorder, universal logger, and shell launcher
- Prompt contracts across all seven levels: call, sequence, guard, delegate, accept a plan, generate a prompt, and update Expertise
- Course-era slash-command and sub-agent packaging versus current discoverable Agent Skills; this lesson repository contains no `SKILL.md`
- User-prompt versus system-prompt scope and persistence
- Context and memory contracts: empty `CLAUDE.md`, repository README, `/prime`, `/prime_cc`, and `/prime_tier_list`
- Tool and permission contracts: command frontmatter, agent frontmatter, MCP samples, environment-key surfaces, and permission-bypass risk
- Harness and launcher contracts: `/background`, report routing, terminal-state naming, and `scripts/bg_claude_code_test.sh`
- Verification contracts: app `bun run build`, command Reports, `git diff --stat`, full diffs, hook JSONL, and durable artifacts
- Recovery loop: early return, bounded repair/retry, failed terminal state, prompt-contract repair, and human escalation
- Level-7 expert loop: plan → build → improve, with only `## Expertise` allowed to change

## Source audit

- Read all 70 real text files in `agentic-horizon/agentic-prompt-engineering` (5,521 newline-counted lines), excluding absent/generated `.git`, `node_modules`, virtual environments, and binary/runtime artifacts.
- Read the sibling chapter `vol-2-ah/10-seven-levels-agentic-prompt-formats.html` and its page asset CSS for the conceptual spine.
- Read the lesson extract, JSON schema, frame plan, lab spec, nuggets, status, and `outdated-vs-current.md` under `book/_extracts/ah-2-seven-levels-agentic-prompt-formats/`.
- Used the existing AH-1 agent-systems companion as a compact chrome and interaction-shell reference; the content and lab are lesson-specific.

## Course-era and repository caveats surfaced

- `CLAUDE.md` is empty, so this checkout provides no persistent repository memory through that file; priming is an explicit interface.
- `apps/prompt_tier_list/src/constants/entities.ts` defines 13 prompt sections and seven formats; older README and `prime_tier_list.md` prose says 12 sections.
- `quick-plan.md` and `background.md` pin `claude-opus-4-1-20250805`; model IDs are treated as course-era configuration.
- Firecrawl and Replicate MCP servers, API keys, tool names, TTLs, and exact CLI flags are treated as swappable capability packaging.
- `.mcp.json.playwright_10k.sample` contains an extra closing brace and does not parse as JSON; the page uses it as a capability-configuration failure example.
- `background.md` and the shell helper use `--dangerously-skip-permissions`; the page treats this as explicit high-risk authority, not a default.
- `scripts/bg_claude_code_test.sh` assigns both MODEL and REPORT_FILE from argument 2, assumes an unshipped active `.mcp.json`, and launches a live agent at file end.
- `crypto-coin-analyzer.md` points at a nonexistent `.claude/commands/agent_prompts/...` path and lacks Read despite instructing the specialist to read its prompt; the lab repairs this contract without launching the agent.
- `/build` reports a summary and diff stat but does not require the app’s real build; the page keeps verification independent.
- Hook files improve observability but do not assert task success, and the universal logger’s full payloads require privacy and retention controls.

## Page structure check

- Compact site bar links to chapter, code library, and book hub
- One-paragraph agent mission card and leverage hook
- Cast-of-agents table
- Agent surface map infographic
- Seven levels mapped to operating-system capabilities without duplicating the chapter
- In-loop/out-of-loop plan → act → verify → recover diagram
- One worked agent run from plan input to independent verification
- Four agent contract sections with short evidence excerpts and Dan’s design intent
- Real operating sequence using repository command interfaces and README app commands
- Agent-system failure taxonomy
- Agent-contract repair lab with observable, no-spend pass criteria
- Six-sentence teach-back
- Collapsible one-line index of all 70 real files

## Validation

- JavaScript parses successfully; explicit opening/closing tags are balanced.
- The page contains 10 lesson sections, 10 matching rail links, and two inline SVG diagrams.
- All fragment targets are present and unique; all local stylesheet, chapter, library, and hub links resolve.
- The appendix contains 70 unique source paths, exactly matching the 70 real lesson files.
- Required agent-first surfaces are present: mission, cast, map, loop, contracts, operation, failures, lab, teach-back, and appendix.
- Desktop/mobile browser capture was attempted through the required in-app browser workflow and installed Chrome. The managed workspace prevented the in-app session from starting and aborted Chrome before page load, so screenshot QA was unavailable. Responsive behavior was checked from the loaded CSS, media queries, width constraints, overflow rules, and balanced DOM structure.
- Two-axis review completed against fixed point `833ee20`: Standards found no hard violations and one accepted self-contained-shell duplication heuristic. Spec review prompted a runnable verbatim launcher excerpt and a current Agent Skills packaging note. Its clean-checkout dependency finding is environmental: the shared design, chapter, library, and hub files all exist in the working book tree but are untracked user-owned inputs outside this two-file deliverable, so they were intentionally not absorbed into scope. The initial two-file delivery is commit `2a96f25`; final review corrections are present in the workspace, but the managed sandbox denied creation of `.git/index.lock`, so a follow-up commit could not be written.

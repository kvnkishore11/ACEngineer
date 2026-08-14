# STATUS: COMPLETE

**Lesson key:** `ah-6-building-agentic-layers`  
**Deliverable:** `code/ah-6-building-agentic-layers.html`  
**LENS: agent-systems**

## Outcome

The code companion has been reworked as a teaching-first Agent Systems page. It avoids a file-by-file application tour and instead teaches the operating layer around the code: commander authority, focused agent roles, mounted context, tool and permission boundaries, launchers, durable receipts, verification gates, and recovery branches.

## Agent interfaces covered

- Human commander contract: outcome, `cwd`, risk, cost, and acceptance evidence
- Project memory and context: `CLAUDE.md`, `specs/`, `ai_docs/`, project setting sources
- Prompt contracts: `prime.md`, `plan.md`, `build.md`, `review.md`, `fix.md`, and orchestration commands
- Agent templates: purpose, model choice, tool frontmatter, and report contracts under `.claude/agents/`
- Skills and MCP mounts: project skills, `.mcp.json.sample`, and Playwright configuration
- Tool and permission contracts: template tool lists, orchestrator allowlist, worker defaults, `acceptEdits`, and ADW `bypass_permissions=True`
- Hook contracts: PreToolUse, PostToolUse, UserPromptSubmit, Stop, event publication, and deterministic blocking
- Harness and launcher contracts: manual ADW trigger, detached `uv run ... --adw-id`, backend/frontend start scripts, `--cwd`, and `--session`
- ADW control loop: plan → build → review → conditional fix, with step status and error recovery
- Orchestrator bridge: 10 typed tools, including `start_adw` and `check_adw`
- Verification receipts: `specs/`, diffs and validation commands, `app_review/`, `app_fix_reports/`, logs, WebSockets, and ADWS swimlanes
- Failure modes: mis-prompting, runtime over-permission, hooks-only settings, wrong `cwd`, open-loop review, chat-as-memory, and human polling
- Agent-ops lab: activating and testing the existing `.env` PreToolUse gate without changing application logic

## Accuracy notes

- Uses the verified backend port `9403` and frontend port `5175`; calls out stale `8002` guidance.
- Uses the verified count of 10 orchestrator tools and 7 database tables.
- Describes `start_adw` as a typed tool call; the README’s “start adw:” text is treated as illustrative intent, not a host-side parser.
- Treats agent-template tools as a declared contract but identifies that the orchestrator command path grants a broad default set instead of enforcing the template list.
- Describes the root `.claude/settings.json` as hooks-only; it does not claim a project permission allowlist exists.
- Uses only paths verified in `agentic-horizon/orchestrator-agent-with-adws`.

## Presentation

- Required shared CSS: `tokens.css`, `base.css`, `components.css`, and `chrome-v2.css`
- Compact sticky site bar and chapter rail
- Warm cream paper theme with clay accent
- Bespoke agent-surface and control-loop SVG diagrams with reduced-motion support
- Short contract snippets only; no source dumps
- Soft animation on expandable teach-back and appendix sections

## Verification completed

- All 11 section IDs are unique and every rail hash resolves.
- Semantic tag pairs balance for sections, articles, figures, SVGs, tables, details, and summaries.
- All four required shared stylesheets and all three site-bar destinations resolve locally.
- Every file path in the raw agent-interface index resolves against the canonical lesson codebase.
- Inline JavaScript passes `node --check`; inline CSS has balanced braces.
- All `aria-labelledby` references resolve and the three diagrams have accessible names.
- No unescaped ampersands were found.
- In-app browser rendering was attempted, but the managed browser session could not initialize because its sandbox policy metadata was unavailable. Local Chrome and Quick Look rendering were also blocked by the managed environment, so final QA is static rather than screenshot-based.

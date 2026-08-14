# TAC-2 code companion status — The 12 Leverage Points

Status: **REWORKED — agent-systems lens**

LENS: agent-systems

## Deliverables

- `tac-2-the-12-leverage-points.html` — teaching-first Agent OS companion
- `tac-2-the-12-leverage-points.assets.css` — compact agent maps, loops, contract cards, lab, animation, and appendix styling
- `tac-2-the-12-leverage-points-STATUS.md` — this status and coverage record

## Agent interfaces covered

- Human commander vs Claude Code / CLI coding-agent responsibilities
- Fresh-session verifier role and replacement-agent cold starts
- Explicit distinction between the coding agent and the application’s OpenAI/Anthropic SQL generator
- `.claude/commands/prime.md` prompt and cold-start contract
- `.claude/commands/install.md` composed install/prime prompt
- `.claude/commands/tools.md` tool-surface introspection prompt
- `.claude/settings.json` automatic allow list, explicit denies, and approval gaps
- `README.md` setup, launch, verification, routes, and troubleshooting interface
- `specs/init_nlq_to_sql_to_table.md` as a large plan/prompt and an intentionally non-authoritative current-operations source
- `ai_docs/` as local external knowledge for agents
- `scripts/start.sh` as the application harness and observable dual-service launcher
- `scripts/stop_apps.sh` as a forceful cleanup surface that requires policy review
- `claude -p "/tools"` as the lesson’s external programmable-agent seed, not a committed repo launcher
- Backend pytest suite, frontend build, `/api/health`, and `/api/schema` as verification surfaces
- Runtime stdout as the missing observation lever in the committed before-state
- Types and architecture as cold-session navigation aids
- `agents/`, `adws/`, and `trees/` as empty scaffolds, not implemented agent layers
- Explicit absence of a committed `CLAUDE.md`, hooks, skills, subagent definitions, verifier configuration, `start.md`, or Claude-launching script

## Pedagogy and structure

- Compact site bar linking the conceptual chapter, code library, and book hub
- Agent mission card
- Cast-of-agents table
- Animated agent surface-map infographic
- Animated plan → act → observe → verify → recover control loop
- In-loop vs out-of-loop ownership comparison
- Four agent-contract sections with short evidence snippets and Dan’s design intent
- Worked run through the planted `orders_(32).csv` visibility failure
- README-grounded operating commands
- Agent-system failure and recovery cards
- Agent-ops lab that modifies the existing cold-start prompt rather than application logic
- Six-sentence teach-back
- Collapsible one-line index of all 49 real TAC-2 files

## Accuracy locks

- The full 49-file TAC-2 tree was inventoried; the raw appendix contains every file and no invented path.
- `_extracts/tac-2-the-12-leverage-points/` is not present, so there were no extract mission or outdated-flag files to apply.
- The sibling conceptual chapter supplied the durable spine—Core Four, eight through-agent levers, closed loops, plans/templates/ADWs, and four KPIs—without being reproduced wholesale.
- The page does not claim TAC-2 ships a `CLAUDE.md`.
- The page does not claim TAC-2 ships subagents, hooks, skills, a verifier agent, or an ADW.
- `scripts/start.sh` is described as an application launcher, not an agent launcher.
- `.claude/commands/start.md` is identified only as a student-created lesson artifact; it is not included in the raw file index.
- The 300-second duration is described as a Bash tool timeout, not a `start.sh` argument.
- The application’s provider LLM is separated from the coding agent.
- The committed server is described as the before-state with missing detailed handler stdout.
- The specification is treated as plan evidence; stale file and command claims are not repeated as current repository facts.
- Every path in the raw index exists under `tac/tac-2`.

## Verification completed

- HTML5 parsing completed with zero parse errors.
- Inline JavaScript parsed and executed in a DOM harness with zero runtime errors.
- All IDs are unique and every local anchor resolves.
- All five linked stylesheets and the page asset’s inherited layout stylesheet resolve locally.
- Both SVG diagrams have accessible labels.
- All 49 appendix entries resolve to real files under `tac/tac-2`.
- The raw-index disclosure opens programmatically and the CSS includes a reduced-motion path.
- Section/progress wiring, active-rail targets, and mobile contents targets passed structural checks.

## Visual QA limitation

- The in-app browser could not initialize because workspace sandbox metadata was unavailable.
- A local headless Chromium fallback was also blocked by the managed macOS process sandbox before page launch.
- Desktop/mobile visual inspection therefore remains pending; no browser-render claim is made.

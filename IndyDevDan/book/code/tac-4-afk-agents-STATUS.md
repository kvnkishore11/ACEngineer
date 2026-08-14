# TAC-4 AFK Agents companion — status

STATUS: COMPLETE
LENS: agent-systems
LESSON: `tac-4-afk-agents`

## Deliverables

- `code/tac-4-afk-agents.html` — teaching-first companion page
- `code/tac-4-afk-agents.assets.css` — lesson-specific cream/clay layout and diagram styles
- `code/tac-4-afk-agents-STATUS.md` — this coverage and verification record

## Agent interfaces covered

- Human commander: issue framing, PITER planning, launch authority, and final review
- Prompt contracts: all 13 real `.claude/commands/*.md` command prompts
- Context and memory: `README.md`, `adws/README.md`, specs, AI docs, generated plans, and explicit absence of `CLAUDE.md`, `AGENTS.md`, and repo-local skills
- Tool and permission contract: `.claude/settings.json`, allow/deny lists, hooks, environment variables, and the programmatic permission-bypass boundary
- Harness and launchers: `adws/agent.py`, `adw_plan_build.py`, webhook and cron triggers, and the shell launch scripts
- Verification and recovery: tests, type checks, linting, health checks, log/result artifacts, GitHub issue/branch/PR state, and cleanup scripts
- Runtime evidence: the eight-agent call sequence and outcomes from real run `5f2e861e`
- System boundaries: no durable queue, no worktree-per-run isolation, no dedicated verifier agent, and no webhook signature validation

## Pedagogical coverage

- Compact mission-first entry point
- Cast of agents and scripts-as-agents
- Agent surface map rather than a file-by-file tour
- Plan → act → verify → recover control loop with in-loop/out-of-loop boundaries
- Prompt, permission, harness, and verification contracts with short evidence snippets
- One worked run using README commands and real run artifacts
- Misconfiguration failures and their observable symptoms
- Agent-ops lab that changes the hook/permission system, with pass criteria
- Six-sentence teach-back exercise
- Collapsible one-line raw index of the 147 inspected, non-secret artifacts

## Verification

- Entire lesson codebase inventoried with `.git`, dependency trees, virtual environments, caches, and binaries excluded
- Secret-bearing `.env` contents deliberately excluded; `.env.sample` contract inspected safely
- 147 raw-index entries checked against real paths
- All internal anchors resolve and all local linked files exist
- All HTML classes resolve against the four shared stylesheets plus the page asset
- Inline JavaScript passes Node syntax validation
- No source/application files were changed
- Automated browser rendering was attempted through the prescribed browser flow and a local headless fallback; both were blocked by the managed macOS process sandbox, so no screenshot claim is made

## Conceptual boundary

The sibling chapter supplies the conceptual spine—leverage, replaceability, programmable agents, and closed loops. This page applies that spine to the concrete TAC-4 agent operating system without reproducing the full chapter.

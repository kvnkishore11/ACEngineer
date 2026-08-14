# TAC-7 Companion Status

STATUS: COMPLETE
LENS: agent-systems

## Deliverable

- code/tac-7-zte-secret-of-agentic-engineering.html

## Agent interfaces covered

- Human command surface: GitHub issue, workflow choice, risk class, credentials, and uppercase ZTE intent
- Trigger surface: adws/adw_triggers/trigger_webhook.py and trigger_cron.py
- Prompt contracts: .claude/commands/*.md, including classification, planning, implementation, test, review, patch, document, and KPI prompts
- Conditional context: .claude/commands/conditional_docs.md, README.md, adws/README.md, specs, and app documentation
- Tool and permission contract: .claude/settings.json, lifecycle hooks, deny/allow rules, and the fail-open PreToolUse configuration
- Browser tool surface: .mcp.json and playwright-mcp-config.json
- Programmatic launcher: adws/adw_modules/agent.py, model-set routing, claude -p, JSONL capture, safe environment filtering, and retry policy
- Persistent memory: adws/adw_modules/state.py, ADWStateData, run artifacts, Git branches, and issue comments
- Isolation surface: git worktrees, per-run ports, .ports.env, setup scripts, and cleanup scripts
- Workflow composition: plan, build, test, review, document, ship, patch, reviewed SDLC, and ZTE orchestrators
- Verification and recovery: structured test results, unit repair loop, agentic spec review, screenshots, blocker patches, re-review, state completeness, and worktree validation
- Shipping boundary: direct --no-ff merge and push behavior verified from adw_ship_iso.py
- Observability: execution logs, saved prompts, JSONL traces, screenshots/R2 publishing, app_docs/, and app_docs/agentic_kpis.md
- Operator path: setup and run commands taken from the real README files
- Failure modes: contradictory prompt schema, broad permission bypass, fail-open hook, hardcoded E2E skip, semantic false-green output, shared environments, documentation drift, and premature global ZTE
- Agent-ops lab: align the review schema and make secret-file access fail closed without changing application logic

## Source notes carried forward

- Tactic name: Zero-Touch Engineering; code/docstring expansion: Zero Touch Execution
- Presence drops from approximately 2 to 1; embedded agentic review remains
- Both composed SDLC paths hardcode --skip-e2e
- ZTE aborts on test/review failure; documentation failure is non-blocking
- README ship wording drifts from executable source; source behavior is reported
- No lesson-local CLAUDE.md, .claude/agents/, or skills directory was invented

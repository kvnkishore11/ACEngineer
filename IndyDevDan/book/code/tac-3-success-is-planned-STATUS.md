# TAC-3 Success is Planned — companion status

STATUS: COMPLETE

LENS: agent-systems

## Deliverable

- `code/tac-3-success-is-planned.html`
- Page asset: `code/tac-3-success-is-planned.assets.css`

## Agent interfaces covered

- Human commander boundaries: work classification, plan review, authority, independent acceptance, and upstream repair.
- Planning prompts: `.claude/commands/chore.md`, `bug.md`, and `feature.md` as class-specific meta-prompts.
- Execution prompt: `.claude/commands/implement.md` as the plan-consuming higher-order prompt.
- Boot context and durable memory: `.claude/commands/prime.md`, `README.md`, `$ARGUMENTS`, and `specs/*.md`.
- Tool and permission boundary: all 12 allow entries and all 3 deny entries in `.claude/settings.json`.
- Harness and launchers: `install.md`, `start.md`, `tools.md`, `scripts/copy_dot_env.sh`, `scripts/start.sh`, and `scripts/stop_apps.sh`.
- Verification: plan-embedded Validation Commands, `uv run pytest`, targeted behavior/search checks, human rerun, and `git diff --stat` reporting.
- Isolation and replaceability: fresh planner vs fresh implementer; no dependency on prior chat.
- Programmatic bridge: the course-run `claude -p` + stream-JSON shape, with the permission-bypass flag explicitly treated as historical/demo-scoped.
- Honest absences: no TAC-3 `CLAUDE.md`, hooks, skills, verifier agent, or subagent definition; `agents/README.md` and `adws/README.md` are empty placeholders.

## Source coverage

- Audited all 56 text/source files under `tac/tac-3` (excluding no files; the tree contains no vendored `node_modules`, virtualenv, or binary payloads).
- Read `_extracts/tac-3-success-is-planned/`, including mission, lab guidance, evidence-count caveats, and outdated-vs-current flags.
- Read sibling chapter `vol-1-tac/03-success-is-planned.html` for the conceptual spine; this companion does not reproduce its full code-tour or chapter pedagogy.

## Page checks

- Required site-bar links: chapter, code library, and book hub.
- Required sections: mission, cast, agent surface map, control loop, four agent contracts, operating runbook, failures, agent-ops lab, six-sentence teach-back, and collapsible 56-file index.
- All asserted repository paths on the page refer to real TAC-3 paths; runtime-generated artifacts are described generically rather than named as shipped files.
- The lab changes only the agent system (`.claude/commands/chore.md` and a generated spec) and requires `app/` to remain unchanged.

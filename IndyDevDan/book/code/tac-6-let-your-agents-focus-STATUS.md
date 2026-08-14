# TAC-6 Let Your Agents Focus — Companion Status

LENS: agent-systems

## Deliverable

- Page: `code/tac-6-let-your-agents-focus.html`
- Lesson source: `tac/tac-6`
- Companion chapter: `vol-1-tac/06-let-your-agents-focus.html`
- State: complete; source fidelity and desktop browser rendering validated

## Agent interfaces covered

- Human commander: issue framing, workflow selection, authority, evidence review, and merge gate
- Focused worker prompts: `.claude/commands/` with special attention to `prime.md`, `conditional_docs.md`, `review.md`, `patch.md`, and `document.md`
- Tool and permission boundary: `.claude/settings.json`, lifecycle hooks, and `.mcp.json`
- Headless process launcher: `adws/adw_modules/agent.py`
- Workflow composers: `adws/adw_sdlc.py`, `adw_plan_build_review.py`, and `adw_plan_build_test_review.py`
- Shared memory and artifacts: `ADWState`, per-agent prompt capture, raw JSONL, plans, diffs, screenshots, and structured results
- Verification and recovery: `adws/adw_test.py`, `adws/adw_review.py`, typed review results, and bounded patch/re-review
- Trigger surface: issue classifier, cron/webhook entry points, workflow registry, and selector drift
- Deterministic helper scripts: start, reset, stop, and application preparation
- Human in-loop versus system out-of-loop control moves

## Source-truth notes surfaced

- The repository uses fresh `claude -p` processes rather than lesson-local native subagent definitions.
- The ADW launcher requests `--dangerously-skip-permissions`; the visible settings allowlist is therefore not presented as the full runtime boundary.
- The review prompt's array/object output wording and E2E path spelling drift from the parser and filesystem.
- Every shipped composer that includes the test stage passes `--skip-e2e` to it.
- Several workflow-produced state keys are filtered out by the five-field `ADWState` schema.
- The classifier advertises workflow selectors that the webhook's typed/runtime allowlists omit.
- Hook commands use `|| true`, so safety enforcement and telemetry behavior are distinguished.

## Pedagogy

- Hook → cast → agent surface picture → control loop → four contracts → worked run → failures → agent-ops lab → six-sentence teach-back
- The page avoids a traditional code tour; source excerpts are limited to agent contracts.
- The lab changes the reviewer prompt and preserves application logic.

## Audit scope

- Full lesson inventory reviewed, excluding `.git`, dependency directories, virtual environments, and binary decoding.
- Extract mission, outdated flags, nuggets, and lab notes reviewed.
- Sibling chapter reviewed for the conceptual spine without reproducing it.
- All 136 real lesson paths are recorded in the collapsed appendix; the two binary assets are indexed but not decoded.
- Desktop browser rendering, navigation targets, collapsible semantics, and responsive breakpoints were checked; no horizontal overflow was observed in the rendered desktop page.

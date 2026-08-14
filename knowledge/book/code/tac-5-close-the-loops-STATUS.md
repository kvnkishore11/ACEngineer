# TAC-5 Close the Loops — companion status

STATUS: COMPLETE

LENS: agent-systems

## Deliverable

- `code/tac-5-close-the-loops.html`
- `code/tac-5-close-the-loops.assets.css`

## Agent interfaces covered

- Human command boundary: issue/workflow choice, authority audit, acceptance, and PR/evidence review.
- Prompt contracts: `.claude/commands/bug.md`, `feature.md`, `chore.md`, `implement.md`, `test.md`, `test_e2e.md`, and both resolver prompts.
- Context and memory: `.claude/commands/prime.md`, `README.md`, `adws/README.md`, generated `specs/*.md`, and the five-field ADW state contract.
- Tool and permission contract: `.claude/settings.json`, lifecycle hooks, secret/removal guards, launcher permission bypass, and the effective-policy audit.
- Browser/tool surface: `.mcp.json`, natural-language E2E specs, deterministic DB reset, application launcher, screenshot evidence, and expected discovery count.
- Programmatic harness: `adws/adw_modules/agent.py`, typed request/response models, stream-JSON output, saved prompts, and raw JSONL traces.
- Orchestration: plan/build/test composition, cron and webhook triggers, issue classification, branches, commits, pushes, and pull requests.
- Verification and recovery: five command validators, unit retry bound (4), E2E retry bound (2), first-E2E-failure stop, one resolver context per failure, counted-failure exit policy, and its parse/discovery false-green gaps.
- Observability: ADW-prefixed GitHub comments, `agents/{adw_id}/` trails, execution logs, prompts, raw output, session IDs, and screenshots.
- Agent-system failure modes: open-loop prompts, contradictory verifier instructions, permission-policy mismatch, masked blocking hooks, unsigned webhook exposure, working-directory-dependent E2E discovery, false green on missing suites, non-determinism, and unbounded retry risk.
- Current-practice bridge: skills for packaging, hooks for non-negotiable rails, schema-validated structured outputs, wider browser tooling, and managed out-loop environments.

## Source grounding

- Entire `tac/tac-5` tree inventoried: 113 files; binary database content was indexed but not dumped.
- Conceptual spine read from `vol-1-tac/05-close-the-loops.html` and the TAC-5 extract package.
- Extract mission, lab guidance, and outdated/current flags reconciled with the live repository.
- README commands are shown in the operating path; live CLI signature drift and fail-open behavior are called out where code diverges from the runbook.

## Pedagogy and presentation

- Teaching path: hook → cast → surface picture → worked run → named pattern → failure → agent-ops retry.
- Compact chrome-v2 layout with cream/clay book theme, responsive HTML diagrams, soft details animation, and no giant hero.
- Code is used only as evidence of agent contracts; prompt/settings snippets alone receive syntax color.
- Optional appendix indexes every real file without source dumps.

## Verification

- HTML5 parser: zero structural errors; one `h1`, one `main`, unique IDs, and every fragment target resolves.
- Source index: 113 listed paths exactly match the 113 real files under `tac/tac-5`; no missing or invented entries.
- Local dependencies: all linked CSS, chapter, library, and hub targets exist; `git diff --check` is clean for the deliverables.
- Desktop Chrome render inspected at 1397×768 around the surface map and control loop; compact chrome, breakout cards, and reading rail rendered without clipping.
- Automated browser/device emulation was unavailable in the local sandbox, so responsive breakpoints and reduced-motion behavior were verified statically rather than through device screenshots.

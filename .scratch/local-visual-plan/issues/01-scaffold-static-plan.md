# 01 — Skill scaffold + static visual plan (end-to-end)

Status: ready-for-agent

## Parent

`.scratch/local-visual-plan/PRD.md`

## What to build

The tracer bullet: scaffold the `local-visual-plan` skill and make it produce a complete static visual plan HTML, end to end, with zero server and zero MCP/hosted dependency.

`SKILL.md` carries policy only: manual `/local-visual-plan` trigger; gating discipline lifted from `visual-plan` (skip trivial work, never single-step filler); read-only-until-the-user-approves; and a local core workflow that replaces every remote `create-*` / `get-plan-blocks` / `update-*` / `get-plan-feedback` / `export-*` call with local steps (research read-only → draft sections → fill the template → write the file → print the path). The `when-to-use` is written richly enough to be promotable to auto-fire later, but v1 stays manual.

The baked-in `assets/template.html` carries the paper-editorial look (Fraunces / Inter / JetBrains Mono via Google Fonts CDN with a system-font fallback stack) and content slots for the plan body: objective, scope, steps, risks, verification, open questions. Diagrams are hand-authored inline SVG. `references/document-quality.md` is lifted from `visual-plan` with the remote-block parts stripped, and is loaded via progressive disclosure ("READ before authoring").

Output is a single self-contained `plans/<slug>.html` in the current project cwd; the agent prints the `file://` path. No interactivity in this slice — this proves the spine: invoke → open → read a real plan.

## Acceptance criteria

- [ ] `/local-visual-plan <task>` produces one self-contained `plans/<slug>.html` with no MCP, hosted, or localhost calls
- [ ] The plan renders objective, scope, steps, risks, verification, and open-questions sections in the paper-editorial look
- [ ] At least one inline-SVG diagram renders
- [ ] Fonts load via CDN and degrade to the system stack offline; content is never network-blocked
- [ ] Every section carries a stable, human-meaningful `id` (foundation for slices 02/03)
- [ ] The agent prints a clickable `file://` path after writing
- [ ] `SKILL.md` enforces read-only-until-approval, gating discipline, and manual-only trigger
- [ ] `references/document-quality.md` is present, de-remoted, and loaded via progressive disclosure
- [ ] The skill has no dependency on `thariq-design`, `kvnk-html`, or any other skill

## Blocked by

None - can start immediately.

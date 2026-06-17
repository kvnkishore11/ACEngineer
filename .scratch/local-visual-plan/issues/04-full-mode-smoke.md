# 04 — Full-mode sample render + round-trip smoke

Status: done

## Parent

`.scratch/local-visual-plan/PRD.md`

## What to build

Render one sample plan that exercises all three modes together (plan + wireframe + click-through prototype) and verify the complete local round-trip end to end.

Confirm the file opens from `file://` with nothing running but the browser, that content renders offline (fonts may fall back, content does not), and that the full feedback loop works: check and annotate a few sections, click "Copy feedback", paste the anchored markdown back, have the agent edit the HTML, and confirm the persisted checkbox/note state survives the edit. Surface the `file://` path for human review of the artifact.

## Acceptance criteria

- [x] One sample `plans/<slug>.html` renders plan + wireframe + click-through prototype together
- [x] Opens from `file://` with no server; content renders offline (fonts may fall back)
- [x] Full round-trip verified: check/note → copy feedback → paste → agent edits HTML → checkbox/note state survives
- [x] The `file://` path is surfaced for human review

## Implementation notes

Rendered `plans/workspace-onboarding.html` in this repo — a screen-facing plan
(the existing `auth-refresh-tokens.html` is backend-only, so a new screen-facing
sample was needed to exercise both screen modes). It carries all three modes in
one self-contained file:

- **Plan body** — objective, scope/non-goals, approach (with a hand-authored
  inline-SVG onboarding state machine), 4 steps, 2 risks, verification,
  open-questions. Every section/step/risk has a stable `id` + `data-fb-title`.
- **Wireframe** (`#wireframe`) — the "Connect a repo" step mock via the `.wf-*`
  helpers + palette tokens, 3 numbered `wf-annos` callouts. No interactivity.
- **Prototype** (`#prototype`) — 3-screen click-through (welcome → connect →
  first-plan), `data-screen` ids, `data-goto` hotspots, verbatim `.proto-bar`.

`<head>` (fonts + CSS) and the trailing feedback `<script>` are byte-identical to
`assets/template.html` (`diff` → IDENTICAL, 210 lines), so `window.LVP` behaves
exactly as the unit-tested contract.

**Verification (all headless via jsdom, no browser, no network):**

- Self-containment: the only external refs are `fonts.googleapis`/`fonts.gstatic`;
  no localhost, MCP, `agent-native`, external `<script src>`/`<img>`, or
  companion files. Content renders offline; only typography falls back.
- 20-assertion round-trip smoke: 3 modes present + 1 SVG + slug + `window.LVP`
  wired; check `step-2` + note `objective`/`risk-1` → `serializeFeedback` emits
  the exact anchored-markdown (titles correct, `☑ checked`, untouched `scope`
  omitted); persisted to `localStorage`; **reload into a fresh DOM with the same
  store restores check + note + `done` class**; `resetState` clears only this
  plan's keys (a seeded `lvp:OTHER-plan:*` key survives). `showScreen`/`goBack`:
  only-target-visible, counter `Screen 2 / 3`, Back restores prior.
- Full paste→edit→survive: applied a real feedback-driven prose edit to `step-3`
  (id + `data-fb-title` preserved) and confirmed a reviewer's pre-existing
  check+note for `step-3` still binds after the edit.
- Skill contract regression: `bun test` → **10 pass, 0 fail** (template
  untouched).

`file:///Users/kvnkishore/WebstormProjects/AgenticEngineer/plans/workspace-onboarding.html`

Deviation: none. (Sample is a new screen-facing plan rather than retrofitting
the backend-only `auth-refresh-tokens.html`, which has no UI surface for the
wireframe/prototype modes.)

## Blocked by

- `02-interactive-feedback.md`
- `03-screen-modes.md`

# 02 — Interactive feedback (checkboxes, notes, persistence, copy-feedback loop)

Status: done

## Parent

`.scratch/local-visual-plan/PRD.md`

## What to build

Make the plan workable in the browser and close the feedback loop — all zero-server.

Add a checkbox per step and a note input per section, both persisted in `localStorage` via `stateKey(slug, sectionId) → "lvp:<slug>:<sectionId>"`. The keying gives per-plan isolation, survives a page refresh, and survives the agent's later edits to the HTML because section IDs are stable. Add a "Reset state" button that clears the current plan's persisted state.

Add a "Copy feedback" button backed by a single named function `serializeFeedback(doc)` that emits the anchored-markdown contract below and writes it to the clipboard. Add the agent-side workflow step in `SKILL.md`: parse pasted anchored-markdown, map each `[§id "title"]` anchor to its section, and edit `plans/<slug>.html` directly so the plan converges without the user hand-editing the file.

The serialized contract (the interface the agent parses back; encodes the grilled decision precisely):

```
## Feedback · plans/<slug>.html

[§step-3 "Add refresh token"]
  ☐ unchecked
  ✎ needs key rotation too

[§risk-2 "Token leak"]
  ☑ checked
  ✎ out of scope — drop this
```

Sections with neither a note nor a changed checkbox are omitted.

## Acceptance criteria

- [x] Each step has a checkbox; each section has a note input; both persist across a refresh
- [x] `stateKey` scopes state per plan — two different slugs never collide
- [x] Persisted state survives an agent edit to the HTML (stable IDs)
- [x] "Reset state" clears the current plan's persisted state only
- [x] "Copy feedback" copies anchored markdown matching the contract; empty sections are omitted
- [x] `SKILL.md` describes parsing pasted feedback and editing the HTML directly to converge
- [x] jsdom test for `serializeFeedback`: checked+note, unchecked+note, and empty→omitted cases assert the exact output string
- [x] jsdom test for `stateKey` + persistence: collision-free across slugs, set→reload→get round-trip, survives re-render with same IDs

## Implementation notes

Built in `~/.claude/skills/local-visual-plan/`:

- `assets/template.html` — added the feedback layer: per-step/per-risk checkbox +
  per-target note, a fixed "Copy feedback" / "Reset state" toolbar, and an inline
  zero-network script. Every feedback target carries `id` + `data-fb` +
  `data-fb-title`; affordances live in a direct-child `.fb` block so nested
  targets never read each other's note. `<body data-plan-slug>` scopes state.
- Three seams on `window.LVP`: `stateKey(slug,id) → "lvp:<slug>:<id>"`,
  `serializeFeedback(doc)`, `resetState(doc)` (plus `restoreState`/`saveTarget`).
- `SKILL.md` — step 4 now mandates `data-plan-slug` + `data-fb-title`; step 6
  parses the anchored-markdown paste back by `id`; added an "Interactive feedback
  contract" section.
- `SKILL.test.ts` — `bun test` + jsdom, 7 tests, all green. Runs the template's
  real script via `new Function` against a controlled DOM (no `runScripts`, no
  network). Added `package.json` + `jsdom` devDep.
- Sample `plans/auth-refresh-tokens.html` re-rendered with the interactive layer;
  headless round-trip verified (persist → serialize → reload-restore → reset).

Deviation: PRD named the test runner "Vitest"; used `bun test` instead — it is
what the cited prior art (`plannotator-setup-goal/SKILL.test.ts`) actually uses
and what's installed. Same jsdom seam, same assertions.

## Blocked by

- `01-scaffold-static-plan.md`

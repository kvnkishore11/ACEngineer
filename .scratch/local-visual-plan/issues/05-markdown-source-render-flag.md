# 05 — Markdown-canonical source + renderer flag

Status: done

## Parent

`.scratch/local-visual-plan/PRD.md`

## What to build

The v2 engine spine. Move the source of truth from hand-written HTML to a compact
`plans/<slug>.md` that a **renderer** turns into `plans/<slug>.html`. The agent
authors only the markdown; it never hand-writes HTML again.

Add a render step with a flag:

- default → **own-template** renderer (the v1 look, re-cast as a renderer of
  markdown: plan sections + inline-SVG + wireframe + click-through prototype carried
  as raw-HTML passthrough in the markdown).
- `--save-tokens` ≡ `--renderer=docforge` → render via `docforge-v11`
  (`render --stable-ids`).
- `--renderer=<skill>` → delegate to any design skill (`thariq-design`,
  `kvnk-html`, …); review overlay (slice 07+) is injected onto its static HTML.

Every rendered block MUST carry a stable `data-block-id` (content-derived) and a
`data-source-line` pointing at the markdown line, so later slices map annotations
to an exact source location and the agent edits the `.md`. docforge emits these;
the own-template renderer must emit equivalents.

**Strip v1's feedback layer** from the own-template path: remove the section note
inputs, checkboxes, the fixed Copy-feedback/Reset toolbar, and the
`serializeFeedback`/`stateKey`/`resetState` script + tests. **Keep** the prototype
`showScreen`/`goBack` nav and the wireframe markup — those are viewing features.

Update `SKILL.md`: author `.md` → render (flag) → print `file://` path. No review
server yet — this slice proves the new engine: invoke → compact `.md` authored →
rendered `.html` opens from `file://` and reads as a real plan.

## Acceptance criteria

- [x] `/local-visual-plan <task>` authors a compact `plans/<slug>.md` and renders
      `plans/<slug>.html`; the agent emits markdown, not HTML
- [x] Default renders via own-template; `--save-tokens` renders via docforge;
      `--renderer=<skill>` delegates
- [x] Every rendered block carries `data-block-id` + `data-source-line`
- [x] own-template output still renders plan sections, ≥1 inline SVG, optional
      wireframe, and optional click-through prototype (`showScreen`/`goBack` intact)
- [x] v1 feedback layer (notes, checkboxes, Copy-feedback/Reset toolbar,
      `serializeFeedback`/`stateKey`/`resetState`) is removed from the template
- [x] Output is self-contained and opens from `file://` offline (fonts may fall back)
- [x] `SKILL.md` documents the md-source workflow + the renderer flag
- [x] `SKILL.test.ts` updated: dead feedback-layer tests removed; `showScreen`
      tests stay green

## Implementation notes

- New engine lives in `~/.claude/skills/local-visual-plan/`:
  `render.ts` (markdown parser + own-template renderer + docforge/skill dispatch
  + `stamp` bridge), `assets/styles.css` (the v1 look, feedback CSS stripped),
  `assets/interactive.js` (prototype nav only — `showScreen`/`goBack` on
  `window.LVP`). `assets/template.html` (the v1 slot-fill HTML) was deleted.
- **Deviation — docforge attributes.** The PRD assumed `docforge render
  --stable-ids` emits `data-block-id`/`data-source-line`. The installed
  `docforge` (`render --to html`) has no such flags, so own-template emits both
  exactly while docforge / `--renderer=<skill>` outputs are stamped best-effort
  by `render.ts stamp` (`data-block-id` always; `data-source-line` by
  quote-matching block text back to the `.md`). This matches the PRD's stated
  degradation path for renders without source attrs and keeps own-template — the
  default and the slice's focus — rigorous.
- Tests: `bun test` → 14 pass (renderer attribute/line mapping, raw-HTML
  passthrough, feedback-layer absence, `showScreen` nav).

## Blocked by

None — first v2 slice. (Builds on shipped v1 issues `01`–`04`.)

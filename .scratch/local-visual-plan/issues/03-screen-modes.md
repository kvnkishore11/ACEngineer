# 03 — Screen modes (wireframe + click-through prototype)

Status: done

## Parent

`.scratch/local-visual-plan/PRD.md`

## What to build

Add the two screen-facing modes to the template, zero-server.

**Wireframe block** — static annotated screen mocks with callouts explaining each region. `references/wireframe.md` is lifted from `visual-plan` with the remote/roughening parts stripped (wireframes are plain static HTML mocks), loaded via progressive disclosure.

**Click-through prototype** — multiple "screens" as divs in the one HTML, navigated by a single named function `showScreen(id)` that shows the target screen and hides the rest, plus a back button that restores the prior screen and a screen counter that tracks position. Honest about being click-through only: no faked backend, no simulated data/state — show/hide navigation only, so the artifact never overpromises what a local file delivers.

Both modes live in the same `assets/template.html` alongside the plan body, selectable per plan.

## Acceptance criteria

- [x] A plan can include a wireframe block of static annotated screen mocks
- [x] `references/wireframe.md` is present, de-remoted, and loaded via progressive disclosure
- [x] A plan can include a click-through prototype of multiple screens in one self-contained HTML
- [x] `showScreen(id)` shows only the target screen; the back button restores the prior screen; the counter reflects position
- [x] Navigation is show/hide only — no fake backend or simulated state
- [x] jsdom test for `showScreen`: only target visible after navigation, back restores prior, counter tracks position

## Implementation notes

Built in `~/.claude/skills/local-visual-plan/`:

- `assets/template.html` — added both screen modes, zero-server:
  - **Wireframe** (`#wireframe`, optional): static annotated screen mock. New
    `.wf-*` helper CSS (frame, chrome bar, card, field, button, pill, inline
    `.wf-mark`) + a numbered `<ol class="wf-annos">` callout list, all
    palette-matched to the template tokens (no hex, no fonts). No interactivity.
  - **Prototype** (`#prototype`, optional): one `[data-proto]` container of
    `div.screen[data-screen]` divs (first visible, rest `hidden`), a `.proto-bar`
    with Back + counter, and `data-goto` hotspots. Both sections are deletable
    per plan and carry TOC entries flagged optional.
- Inline script — added the third seam `showScreen(id)` plus `goBack()`:
  show/hide of `[data-screen]` only (no faked backend/state), a back stack that
  restores the prior screen, and a `Screen N / M` counter. `wireProto()` wires
  hotspots + Back and initialises to screen 1 deterministically regardless of
  `hidden` markup. Both exposed on `window.LVP`.
- `references/wireframe.md` — de-remoted from `visual-plan`: stripped the hosted
  renderer, rough.js sketch overlay, hand-drawn font, `data.html`/`data.surface`
  block contract, surface-preset registry, `--wf-*` tokens, and all
  `update-/get-visual-plan` MCP patch ops. Retargeted to plain static HTML mocks
  using the template's `.wf-*` helpers + palette tokens, plus a new prototype
  section documenting the `[data-proto]` / `data-screen` / `data-goto` contract.
- `SKILL.md` — step 3 now drafts optional screen modes (READ
  `references/wireframe.md` first); step 4 covers the prototype markup contract
  and stable screen ids; the seam list adds `showScreen`/`goBack`; new
  "Screen modes — read `references/wireframe.md`" section.
- `SKILL.test.ts` — added a `showScreen` describe block (3 tests): only target
  visible + counter tracks position, Back restores the prior screen in order, and
  hotspot-advances + Back-disabled-only-at-start. `bun test`: **10 pass, 0 fail**.
  Also smoke-drove the real template's own prototype markup through jsdom (init →
  hotspot → goBack, screens are not `data-fb` targets) — green.

Deviation: none. (Test runner stays `bun test` + jsdom, consistent with slice 02.)

## Blocked by

- `01-scaffold-static-plan.md`

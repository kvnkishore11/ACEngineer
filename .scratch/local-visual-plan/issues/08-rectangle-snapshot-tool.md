# 08 — Rectangle / region "snapshot" tool + coveredSelectors anchor

Status: done

## What to build

The second annotation tool: draw a rectangle directly over the rendered plan to
focus attention on a region and comment on it. Lifted from Picanvas, re-anchored.

Lift from `Picanvas/src/components/artifactOverlay.ts`:

- the SVG overlay layer + drag-draw (`mousedown`/`move`/`up` → SVG `<rect>`) `:199–255`
- `sampleCoveredSelectors(x,y,w,h)` — 9-point sampling + `elementFromPoint`
  (viewport-adjusted) → the set of elements the box covers `:257–287`
- rect rehydrate `:654–664`

**Swap the anchor** from Picanvas's raw page-px box (which breaks on resize and
re-render) to a **semantic** one: map `sampleCoveredSelectors` to those elements'
`data-block-id` / `data-source-line`, and anchor the rect to
`{ coveredBlockIds[], sourceLines[], box? }`. The px box is kept only as a visual;
the durable anchor is the covered blocks, so the rect re-binds after a re-render
that reflows/reorders content. Do NOT screenshot the region (overlay box only).

A rect annotation uses the PRD model (`kind:"rect"`). On Send it serializes over WS;
the agent resolves `sourceLines` to the markdown span the box covers.

## Acceptance criteria

- [x] A reviewer can drag a rectangle over the iframe'd plan and attach a comment
- [x] The rect records `coveredBlockIds` + `sourceLines` (semantic anchor), with the
      px box kept only for display
- [x] The rect re-binds to the same blocks after a re-render that reorders content
- [x] Rect annotation matches the PRD model and serializes over WS to the agent
- [x] Agent-side resolver maps a rect to the markdown lines it covers
- [x] No region screenshot/rasterization (overlay box + semantic anchor only)
- [x] jsdom test: given a box over known elements, the captured
      `coveredBlockIds`/`sourceLines` are correct and survive a reorder re-render

## Implementation notes

- Built on slice 07's machinery in `~/.claude/skills/local-visual-plan/`:
  - `anchor.ts` — added the **semantic rect anchor**: `sampleCoveredBlocks`
    (browser-only 9-point `elementFromPoint` sampling, lifted from Picanvas),
    `buildRectAnchor(coveredEls, box)` → `{ coveredBlockIds[], sourceLines[],
    box? }`, `rebindRectAnchor` (keyed by `data-block-id`, survives reorder),
    `makeRectAnnotation`, a kind-dispatching `serializeAnnotation`, and the
    agent-side `resolveRectToMarkdown` (covered → `.md` line span). The `resolve`
    CLI now handles both kinds.
  - `overlay.ts` — added the SVG rect layer + drag-draw (`mousedown`/`move`/`up`),
    a rect branch in the handle (region info, no PARENT/CHILD), rect commit, rect
    seed/rehydrate (`drawRectFor` over the union box of the re-bound blocks), and
    rect stickies. The new anchor fns are embedded verbatim via `.toString()`
    (same zero-drift approach as slice 07).
  - `server.ts` — enabled the **Draw region** toolbar button; span+rect are
    mutually exclusive; thread panel renders rect rows ("Region · N blocks").
- **Anchor swap (per PRD).** Picanvas's raw page-px box is the VISUAL only; the
  durable anchor is the covered blocks' `data-block-id` / `data-source-line`.
  Capture is split: the px→elements sampling (`sampleCoveredBlocks`, needs layout)
  is browser-only; `buildRectAnchor`/`rebindRectAnchor` operate on elements and
  are the jsdom-tested seam. STALE when some/all covered blocks vanish — survivors
  kept, never silently dropped.
- **No screenshot** (PRD out-of-scope): overlay `<rect>` + semantic anchor only,
  no html2canvas/rasterization.
- Tests: `bun test` → 50 pass across 3 files (was 39). Live boot smoke confirms
  the rect tool is live, the artifact stays clean, and the rect resolver maps a
  region to its `.md` line span.

## Blocked by

- `06-iframe-shell-review-server.md`

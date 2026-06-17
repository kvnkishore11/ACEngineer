# 14 — Element-pick tool (Picanvas DOM walk + semantic anchor)

Status: done

## Parent

`.scratch/local-visual-plan/PRD.md` (v2.1 amendments)

## What to build

A third annotation tool alongside **Select text** and **Draw region**: **Pick
element** — click any rendered element and walk the DOM to pinpoint exactly the
element you mean.

Replicate Picanvas's element-pick interaction **verbatim** (reference:
`PiCanvas/src/components/artifactOverlay.ts`):

- click an element → it gets a solid outline + a floating handle.
- `[` / `]` keys and **PARENT / CHILD** buttons walk the hierarchy: PARENT →
  `parentElement` (stops at `<body>`); CHILD → first child with text/media
  (`firstSignificantChild`).
- a breadcrumb shows the path (`html › body › section › div …`, ~8 levels), current
  element highlighted.
- the tool is mutually exclusive with Select text / Draw region.

Note for the implementer: this drill feature is **Picanvas's**, not Plannotator's —
Plannotator's "pinpoint" only smart-resolves a single element on hover with no
PARENT/CHILD walk, so mine the Picanvas overlay, not Plannotator.

**Anchor — semantic, not Picanvas's bare CSS selector.** A picked element produces
`kind:"element"`:

- the nearest enclosing `data-block-id` + `data-source-line` (the markdown edit
  target),
- the element's selector **within that block** + its tag + a text snapshot (to
  re-find the exact sub-element).

On Send, the payload serializes like span / rect; the agent resolves the element
anchor to the `.md` line(s) and edits there. After a re-render the pick
**rehydrates**: re-find by in-block selector, fall back to the block; mark **stale**
(never silently drop) if the block is gone. Renders without source attrs (delegated
skills) fall back to whole-doc quote search, like the other anchors.

## Acceptance criteria

- [x] A third "Pick element" tool exists; clicking selects an element with outline +
      handle, mutually exclusive with the other two tools
- [x] `[` / `]` + PARENT/CHILD walk widen/narrow along the DOM (parent up to body;
      first-significant-child down) with a breadcrumb path
- [x] A picked element produces a `kind:"element"` anchor: block-id + source-line +
      in-block selector + tag + text snapshot
- [x] The annotation serializes over WS like span / rect; the agent resolves it to the
      exact `.md` location and edits there
- [x] After a re-render the pick rehydrates (in-block selector → block fallback);
      marked stale, not lost, if the block vanished
- [x] Renders without source attrs degrade to whole-doc quote search
- [x] Tests: element anchor build/serialize, resolve-to-markdown, rehydrate after a
      reorder re-render, stale on block removal

## Blocked by

- `11-batch-send-draft-sidebar.md` (the pick commits through the draft-send flow)

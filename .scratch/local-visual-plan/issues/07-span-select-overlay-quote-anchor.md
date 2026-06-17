# 07 — Text-span select overlay + quote anchor

Status: done

## What to build

The first annotation tool: arbitrary text-span selection ("any letter or word"),
lifted from Picanvas and re-anchored.

Inject the vanilla overlay into the iframe (slice 06's injection point) and bridge
it to the shell via `postMessage`. Lift from
`Picanvas/src/components/artifactOverlay.ts`:

- text capture (`getSelection`/`Range`, `range.surroundContents(<span class=hl>)`
  with the extract+wrap fallback for cross-boundary) — `:166–197`
- the **selection handle** with PARENT/CHILD hierarchy nav (`[`/`]` + breadcrumb) to
  widen/narrow the selection — `:289–427`
- `buildSelector` `:498–516`, sticky-comment render `:593–624`, postMessage bridge
  `:671–713`

**Swap the anchor** from Picanvas's offset-in-selector to **quote-based**
(W3C TextQuoteSelector): `{ quote, prefix, suffix, blockId, sourceLine }` taken from
the enclosing block's `data-block-id` / `data-source-line`. Re-bind after a
re-render by re-finding the quote within that block; if the quoted text itself
changed, mark the annotation **stale** (never silently drop it).

A span annotation is created with the model from the PRD (`kind:"span"`, `anchor`,
`category`, `status:"open"`, `thread`). On Send, the payload goes over the WS to the
agent; the agent resolves `sourceLine` + quote to the exact markdown location (no
edit/conversation yet — that's slice 09). Delegated-skill renders without source
attrs fall back to whole-doc quote search.

## Acceptance criteria

- [x] A reviewer can select any text span in the iframe and attach a comment
- [x] Selection handle lets the reviewer widen/narrow along the DOM hierarchy
- [x] Span anchor is quote-based (`quote`+`prefix`+`suffix`+`blockId`+`sourceLine`)
- [x] Highlight re-binds after a re-render; if the quoted text changed it is marked
      `stale`, not lost
- [x] Span annotation matches the PRD model and serializes over WS to the agent
- [x] Agent-side resolver maps an annotation to the exact markdown line+quote
- [x] jsdom tests: quote-anchor rebind (survives surrounding edit; stale on quote
      change) and annotation serialize shape

## Implementation notes

- New files in `~/.claude/skills/local-visual-plan/`:
  - `anchor.ts` — the quote anchor (W3C TextQuoteSelector) + serialize + the
    agent-side `resolveAnnotationToMarkdown` + a `resolve` CLI. Functions are
    closure-free and DOM-generic so they run in BOTH jsdom (tests) and the
    browser (overlay).
  - `overlay.ts` — `buildOverlayScript()`: the injectable vanilla overlay,
    lifted from `Picanvas/artifactOverlay.ts` (capture, selection handle with
    `[`/`]` PARENT/CHILD walker + breadcrumb, sticky comments, postMessage
    bridge), re-anchored to the quote strategy.
  - `overlay.test.ts` — anchor bind/rebind/stale, serialize, resolver, and an
    injected-overlay jsdom smoke.
- **Zero-drift anchor reuse.** The exact `anchor.ts` functions the jsdom tests
  exercise are embedded VERBATIM into the injected overlay via
  `Function.prototype.toString()` (bun strips TS types at transpile, so toString
  yields valid browser JS). One algorithm, two runtimes, no duplicated logic.
- **Anchor swap (per PRD).** Picanvas's offset-in-selector anchor is replaced by
  `{ quote, prefix, suffix, blockId, sourceLine }`. Rebind prefers
  prefix+quote+suffix, degrades to a bare-quote search (so a surrounding edit
  still binds), retries the whole body when the block id changed, and returns
  `stale` (never null/lost) only when the quoted text is gone. Renders without
  source attrs (delegated skills) anchor with `blockId:null` → whole-doc search.
- **Transport.** The shell embeds the overlay (escaping `</` so it can't break
  the `<script>` tag), injects it into the same-origin iframe on each load,
  re-seeds it on `ready` (so highlights re-bind in place after a re-render), and
  forwards each committed span annotation over the WS. The server lands it as one
  JSON line in `<run-dir>/annotations.jsonl` and acks the id. The on-disk
  `plans/<slug>.html` is never touched (verified by test + live smoke).
- **Scope honored.** No edit/conversation/re-render yet (slice 09); the rectangle
  tool is slice 08. The toolbar's "Draw region" button stays disabled.
- Tests: `bun test` → 39 pass across 3 files (was 21).

## Blocked by

- `06-iframe-shell-review-server.md`

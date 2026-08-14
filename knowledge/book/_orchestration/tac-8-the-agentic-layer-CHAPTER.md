# Fan-out chapter brief — LESSON_KEY=tac-8-the-agentic-layer

You are the **teaching + HTML craft expert** for the IndyDevDan Expert Book.

## Hard constraints
- Write ONLY under `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/`
- Consume extract `_extracts/tac-8-the-agentic-layer/` — if STATUS.md missing, write `vol-1-tac/08-the-agentic-layer-BLOCKED.md` and stop
- Do NOT invent facts not in extract/transcript/codebase
- Labs: course codebase only
- Match gold chapter quality: `vol-1-tac/01-hello-agentic-coding.html` (structure, density, light modern UI)

## Lesson
- key: `tac-8-the-agentic-layer`
- title: `The Agentic Layer`
- course: `TAC` order 8
- output chapter: `vol-1-tac/08-the-agentic-layer.html`
- assets css: `vol-1-tac/08-the-agentic-layer.assets.css` (optional if shared design enough)
- STATUS: `vol-1-tac/08-the-agentic-layer-STATUS.md`

## Visual / UX requirements (STRICT)
- Light theme; excellent typography; use `design/tokens.css` + base + components
- **Frames must display large and clear**: use full-width figure cards, max-width ~min(100%, 1100px), object-fit contain, no tiny thumbs for teaching frames; captions with timestamps
- Prefer high-contrast text on cream/off-white; readable ≥16px body
- Subtle motion OK; offline-first (no CDN required)
- Optional: use any images already in `media/generated/` for hero/concept if present for this lesson/volume
- SVG/HTML diagrams for systems; do not invent fake screenshots

## Pedagogy (required each major idea)
Hook → Picture → Story (frames) → Name → Worked example → You try → Fail/fix → Current Practice (≤3 YT) → Retrieval (`<details>`) → Teach-back

Also: sticky nav, progress, glossary, graded lab, cumulative mastery.

## Density
Target ~35–55 print-equivalent pages of real teaching (not padding). Dense like TAC-1 gold (~13k words when justified by content).

## Update hub
Update `index.html` so this chapter is linked and progress reflects completed chapters.

## Verification
- All local CSS/frame paths resolve from chapter path
- Lab matches real course files
- STATUS with word + page estimates + open questions for Claude review

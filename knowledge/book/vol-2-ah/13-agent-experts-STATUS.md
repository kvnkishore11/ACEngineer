# STATUS: CHAPTER BUILT ✅ · REVIEW READY

Lesson key: `ah-5-agent-experts`  
Course/order: Agentic Horizon · global lesson 13 · Volume II chapter 5  
Chapter: `vol-2-ah/13-agent-experts.html`  
Chapter CSS: `vol-2-ah/13-agent-experts.assets.css`  
Built: 2026-07-13

## Gate and source discipline

- Extract gate passed: `_extracts/ah-5-agent-experts/STATUS.md` exists and reports `DONE`.
- Consumed: extract narrative/data, nuggets, current-practice notes, lab specification, frame plan, transcript-derived teaching evidence, and extract status.
- Course repository used read-only for truth: `agentic-horizon/agent-experts/`.
- The chapter distinguishes transcript claims, current official platform guidance, and repository-observed behavior. It does not turn recording-era examples into timeless product claims.
- Every lab path and command is scoped to the course repository. The lab never asks the read-only database question expert to write files and never hand-edits learned expertise.

## Deliverable metrics

| Metric | Result |
|---|---:|
| Visible chapter words (tags/scripts removed) | ~13,100 |
| Source words (`wc -w`, includes markup labels) | 14,976 |
| HTML lines | 1,508 |
| Chapter CSS lines | 482 |
| Top-level teaching sections | 17 |
| Complete ten-move idea cycles | 12 |
| Full-width native course frames | 12 / 12 unique |
| Timestamped frame captions | 12 / 12 |
| Retrieval items with `<details>` answers | 55 |
| Lab boxes | 8 |
| Current-practice YouTube overlays | 0 |
| Measured print pages | 54 |

Page measurement: Safari print preview at 100% on US Letter with the chapter's print stylesheet reports 54 pages. The print layer keeps the gold 10.5pt body size, tightens leading and layout, and leaves screen typography and teaching-frame sizing unchanged.

## Pedagogy and UX coverage

- Every major idea contains Hook → Picture → Story/frame → Name → Worked example → You try → Fail/fix → Current Practice → retrieval `<details>` → Teach-back, in that exact order.
- Covers the cold-start problem, expert lifecycle definition, mental-model asymmetry, meta-prompt construction, meta-agentics versus expertise, Act/Learn/Reuse, expertise anatomy, the Learn mechanism, partial versus complete experts, context delegation, product experts, and the build/don't-build decision.
- Sticky desktop rail, mobile TOC, skip link, top/rail progress, active-section highlighting, reduced-motion-safe animation, semantic tables/details/glossary, responsive breakpoints, and print rules are present.
- All frames are 1920×1080, displayed in full-width figure cards up to the shared 1100px teaching width with `object-fit: contain`, readable captions, and frame-plan timestamps.
- The memory lanes, learning loop, delegation pipeline, decision board, and rubric are SVG/HTML systems diagrams rather than invented screenshots.
- The chapter uses the local design tokens/base/components and the gold chapter layer; no CDN is required.
- Current practice deliberately uses zero YouTube links: no lesson-matched candidate was verified strongly enough to improve the chapter. Three official primary-source cards cover memory, Skills, and SDK subagents instead.

## Accuracy corrections incorporated

- Database `question.md` is treated as strictly read-only. The lab asks for an answer in conversation, never a temporary report.
- The shipped WebSocket session counter is treated as completed-loop archaeology, not a fresh Act exercise.
- Learners never corrupt or seed the real expertise by hand. The blank-start exercise uses a new `header-stats` expert whose substantive expertise bytes must be agent-written.
- Repository policy wins over recording-era prompt drift: YAML validation uses `uv run --with pyyaml python -c ...`, not raw `python3`.
- Frontend validation uses the shipped `npm run build`; the chapter does not invent a missing `type-check` script.
- The lab records the actual checked-out default ports, backend 9403 and frontend 5175, and calls out stale generated startup wording.
- Nile is described from the implementation: SQLite/SQLAlchemy with JSON-backed profile data, while the README's JSONB wording is labeled drift.
- The WebSocket expertise's 194-line navigation hint is checked against the current 193-line `chatService.ts`; the discrepancy is used to teach mental-model validation rather than asserted as truth.
- The expertise carrier is described as a high-quality navigation model, never as executable source of truth.

## Verification completed

- All local references from the chapter and hub resolve: design CSS, gold CSS, chapter CSS, hub, previous chapter, and all frame paths.
- All 12 unique lesson frames verified at 1920×1080.
- 29 HTML IDs found; zero duplicates.
- 35 fragment links found; zero missing targets.
- Twelve idea cycles found; each contains all ten required moves in the correct order.
- 12 lesson frame paths found; every frame has a matching timestamp caption and teaching-sized CSS.
- Inline JavaScript parses successfully with `new Function(...)`; progress and active navigation were exercised in Safari.
- All five local CSS layers have balanced braces; chapter frame rules use full width and `object-fit: contain`.
- Chapter contains no YouTube URL and no CDN dependency.
- Hub links lesson 13 as Done. Shared totals and the featured chapter were preserved from concurrent chapter workers; at final verification the displayed percentage matched the completed-chapter count.
- Desktop visual QA passed for hero, sticky navigation, idea-cycle cards, current-practice cards, and graded lab using a temporary inline-CSS render. The native frame files were inspected separately at source resolution.
- Safari print preview measured exactly 54 US Letter pages at 100%, inside the requested 35–55 range, while retaining the gold 10.5pt print body size.

## Open questions for Claude review

1. **Cross-engine print pagination:** Safari measures 54 US Letter pages at 100%; confirm the publication browser does not paginate differently enough to exceed the 35–55 target.
2. **Zero-video editorial choice:** confirm that official primary-source links are preferable to inserting a weakly matched or unverified YouTube overlay for this lesson.
3. **Blank-start lab scope:** confirm the `header-stats` seed exercise should remain a scored 20-point checkpoint rather than an extension, given its 20–30 minute estimate.
4. **Local serving note:** Safari blocks cross-directory stylesheets and images when this chapter is opened directly with `file://`. All paths resolve and the book works under its intended local/static server; decide whether the book hub should eventually document that serving requirement.
5. **Current-practice freshness:** recheck the three official platform links and lifecycle descriptions immediately before publication.

## Recommended Claude visual checklist

- Desktop 1440px: sticky rail does not collide with 1100px frames; captions remain directly beneath each image.
- Tablet ≤65rem: rail hides, mobile TOC appears, wide tables scroll, and figures stay contained.
- Phone 390px: loop, delegation pipeline, comparison tables, and grading rubric collapse without horizontal overflow.
- Print: frames stay contained, retrieval answers remain accessible, lab boxes avoid awkward splits, and total pagination remains within range.
- Contrast/type: cream/off-white surfaces retain warm near-black text, body remains at least 16px, and code blocks remain readable.

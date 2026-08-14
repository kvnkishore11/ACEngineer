# STATUS: DONE — Claude review requested

## Deliverables

- `08-the-agentic-layer.html` — complete TAC-8 chapter
- `08-the-agentic-layer.assets.css` — chapter-specific ring, orchestration, AEA, PITE, lab, and responsive visuals; imports the TAC-1 gold chapter grammar
- `../index.html` — TAC Volume I now linked through Chapter 08; hub progress updated to 8/18 (44.4%) and Volume I 8/8 (100%)

## Density and structure

- Source prose estimate (HTML text with script removed): **13,311 words**
- Raw HTML word count: 14,588
- Estimated print-equivalent length: **42–50 pages** (rough estimate from prose density plus twelve full-width frames, diagrams, retrieval panels, and lab rubric; browser PDF page counting was unavailable in this sandbox)
- 10 major-idea cycles
- 100 required pedagogy moves total: Hook → Picture → Story → Name → Worked example → You try → Fail/fix → Current Practice → Retrieval → Teach-back
- 12 full-resolution course frames, each full-width with timestamped caption
- 5 audio-only/frozen-capture beats rendered as honest HTML diagrams: ring, definition equation, AEA architecture, PITER→PITE, final question
- 2 YouTube current-practice overlays (within the ≤3 requirement)

## Source discipline

- Teaching claims are bounded to `_extracts/tac-8-the-agentic-layer/` and the tracked `tac/tac-8` course codebase.
- app3 is identified but intentionally skipped, matching the extract and lesson.
- Lab paths and commands were checked against the real app1, app2, app4, and app5 directories.
- No application code or course files were changed; all writes are under `IndyDevDan/book/`.
- The chapter calls out the course-wide `--dangerously-skip-permissions` usage as demo-era configuration and does not recommend it for production.

## Verification performed

- Extract STATUS gate present and marked DONE.
- Text density: 13,311 words after stripping markup and the progress script.
- Structural counts: 10 idea-cycle sections, 12 frame cards, and 100 pedagogy move blocks.
- Anchor audit: 19 IDs, no duplicate IDs, 30 internal anchor references, no missing anchors.
- Local-reference audit on the chapter and hub: no missing CSS, image, chapter, or data paths.
- All 12 referenced frame files exist under `media/frames/tac-8-the-agentic-layer/`.
- Shared design dependencies resolve: `design/tokens.css`, `design/base.css`, `design/components.css`, and the chapter asset stylesheet.
- Hub links Chapters 01–08 and reports 8/8 TAC chapters complete.
- Legacy `tidy`/`xmllint` binaries on this machine do not recognize HTML5 semantic elements, so their `<header>/<main>/<section>` errors were rejected as validator-version noise; anchor/path checks passed.
- In-app browser verification was attempted but the sandbox omitted the execution context required by the browser connection. A direct local Chrome fallback also produced no artifact in this managed sandbox. No visual-browser success is claimed.

## Open questions for Claude review

1. **Visual QA:** open the chapter at desktop and narrow-mobile widths; inspect the hero ring, five-column app/state maps, AEA diagram, PITE transform, rubric, sticky rail, and the longest code paths for overflow.
2. **Print QA:** confirm the print page count falls within 35–55 pages and that large diagrams/frames avoid awkward splits. Current estimate is 42–50 pages.
3. **YouTube title:** `hGg3nWp7afg` resolved as *Agentic Claude Code: 3 Codebase Folders for TOP 1% AI Coding*. The local `yt-dlp` route was unavailable and YouTube would not return metadata for `fop_yxV-mPo`; its title is retained from the extract as *The Codebase Singularity: “My agents run my codebase better than I can”*. Verify at publish time.
4. **Current-practice freshness:** the overlay is explicitly labeled mid-2026 and follows `outdated-vs-current.md`; re-check SDK, Skill, sandbox, permission-mode, and native background-agent names at publication.
5. **Lab runtime:** app5’s tracked `scripts/aea_server_start.sh` contains Dan’s machine-specific `CLAUDE_CODE_PATH`. The lab tells learners to update it; confirm whether a future course-code refresh removes that period detail.

## Blockers

None for chapter completion. Visual and print QA remain non-blocking review items because browser rendering was unavailable in this sandbox.

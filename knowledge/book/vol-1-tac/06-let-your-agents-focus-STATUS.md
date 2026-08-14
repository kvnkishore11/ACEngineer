# STATUS: CHAPTER BUILT ✅ · VISUAL REVIEW PENDING

TAC-6 · **Let Your Agents Focus** · lesson key `tac-6-let-your-agents-focus`

## Deliverables

| File | Result |
|---|---|
| `06-let-your-agents-focus.html` | Complete teaching chapter: orientation, 10 major idea cycles, current-practice bridge, graded lab, cumulative mastery, glossary, sticky navigation, and reading progress |
| `06-let-your-agents-focus.assets.css` | Gold-layout reuse plus focus-window, SDLC-question, typed-contract, severity, patch, documentation-loop, KPI, rubric, responsive, and print components |
| `../index.html` | TAC-6 linked, featured chapter updated, and hub progress synchronized to the completed chapters visible when this build finished |

## Density estimate

- Visible chapter words: **12,233** (main content text; HTML, CSS, and JavaScript excluded).
- Source HTML: **1,228 lines / 138 KB**.
- Estimated print-equivalent pages: **42–50**, based on roughly 240–285 teaching words per page plus 12 full-width 1920×1080 frames, diagrams, disclosure answers, and a six-checkpoint lab.
- Teaching cycles: **10 × 10 required moves = 100 moves**.
- Retrieval disclosures: **47 `<details>` blocks** across the mobile TOC, idea cycles, lab, and cumulative mastery.
- Cumulative mastery: **20 cold-retrieval questions**, scoring bands, and a seven-minute capstone teach-back.
- Glossary: **25 canonical terms**.

## Source grounding

- Extract gate passed: `_extracts/tac-6-let-your-agents-focus/STATUS.md` exists and is DONE.
- Consumed the supplied extract set: `extract.md`, `extract.json`, `nuggets.md`, `frame-plan.json`, `lab-spec.md`, `outdated-vs-current.md`, and `STATUS.md`.
- The TAC-6 working-tree checkout was absent in this dirty workspace, so lab and code claims were verified read-only against the tracked `HEAD:tac-6/...` objects. No course files were restored or modified.
- The lab uses only real TAC-6 course paths and scripts. It introduces no external application repository.
- Demo values—issue #14, PR #15, ADW `490eb6b5`, and the generated patch/doc names—are framed as Dan’s runtime evidence, not committed baseline artifacts or student constants.
- The four-entry committed `conditional_docs.md` baseline, severity Literal, three-attempt retry cap, required ADW ID, prompt path typo, classifier/runtime trigger drift, JSON array/object contradiction, and screenshot-state field drop were cross-checked against tracked source.

## Requirement coverage

- Light, high-contrast, offline-first chapter using `design/tokens.css`, `base.css`, and `components.css`: ✅
- Gold chapter grammar reused through the local TAC-1 asset sheet, with TAC-6-specific responsive additions: ✅
- Desktop sticky rail, mobile TOC, reading progress, and active-section navigation: ✅
- All 12 selected frames used full-width up to 1100px, `object-fit: contain`, with descriptive alt text and timestamp captions; two are deliberately reused to give every major idea a frame-backed Story: ✅
- Hook → Picture → Story → Name → Worked example → You try → Fail/fix → Current Practice → Retrieval → Teach-back for all 10 ideas: ✅
- Two YouTube current-practice overlays, within the ≤3 cap and matching the extract’s phase-one decision: ✅
- Graded course-repo lab with setup, plan/build/review, review contract, patch loop, document loop, stretch work, checklist, and 12-point rubric: ✅
- Cumulative mastery and glossary: ✅
- Hub link and progress update: ✅

## Verification completed

- Nokogiri HTML5 parse: **0 errors**.
- All local HTML stylesheet/image paths and the local CSS import resolve from the chapter directory.
- Unique frame-set comparison: **12 of 12**, no omissions or unapproved frame files; **14 total frame uses** because the typed-contract and misplaced-export frames each teach a second Story move. Every source image reports **1920×1080**.
- No duplicate HTML IDs; all **30** internal fragment-link uses resolve.
- Sticky rail and mobile TOC expose the same 15 chapter anchors in the same order.
- Every idea cycle contains exactly 10 move labels; total **100**.
- Inline JavaScript passes Node syntax validation; chapter CSS has balanced braces.
- Print rules remove navigation, preserve large frames, and reveal closed retrieval answers.
- Course-lab references exist in tracked TAC-6 source; `MAX_REVIEW_RETRY_ATTEMPTS = 3`, `Literal["skippable", "tech_debt", "blocker"]`, the five-field state filter, and document’s local screenshot fallback were verified directly.
- Static responsive audit confirmed the gold rail/mobile switch at 65rem, TAC-6 grid collapse at 50rem, 17px shared body type, and full-width frame-sequence breakout on desktop/mobile.

## Open questions for Claude review

1. **Visual browser pass:** the in-app browser could not initialize because sandbox metadata was missing, and the installed Chrome binary returned without producing headless screenshots. Please inspect at approximately 1440×1000, 390×844, and print—especially the context-window diagram, typed-contract panes, six-node documentation loop, nested before/after frame sequences, and rubric cells.
2. **Density judgment:** 12,233 visible words plus 12 large teaching frames estimates to 42–50 pages. Confirm that the balance feels equivalent to the TAC-1 gold chapter without adding prose for its own sake.
3. **Current-practice freshness:** re-check both YouTube IDs/titles and volatile mid-2026 native-agent, Skill, image-reading, and model-routing wording at publication time.
4. **Artifact lineage:** the tracked course code drops screenshot URLs from state and can copy local review images through a fallback. Confirm whether a later editorial pass should require re-review before documentation so fallback proof always reflects the final patched state.

## Blockers

None for chaptering. Interactive desktop/mobile/print visual QA remains a review follow-up before promotion to a reviewed/published state.

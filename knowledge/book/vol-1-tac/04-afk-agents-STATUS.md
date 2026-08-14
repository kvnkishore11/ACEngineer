# STATUS: CHAPTER BUILT ✅ · VISUAL REVIEW PENDING

TAC-4 “AFK Agents” teaching chapter built from `_extracts/tac-4-afk-agents/` and the course codebase at `tac/tac-4`.

## Deliverables

| File | Purpose | Status |
|---|---|---|
| `04-afk-agents.html` | Full teaching chapter | ✅ |
| `04-afk-agents.assets.css` | Gold-layout reuse plus PITER, ADW, telemetry, ladder, and rubric components | ✅ |
| `../index.html` | Hub link, latest chapter feature, and progress update | ✅ |
| `../data/curriculum.json` | TAC-4 status, chapter path, estimates, tactic, and two overlays | ✅ |

## Content and pedagogy

- Visible prose estimate: **10,317 words** (HTML tags, CSS, and JavaScript excluded).
- Print-equivalent estimate: **38–46 pages**, including 12 large native-resolution course frames, one existing generated hero plate, diagrams, retrieval blocks, and the lab rubric.
- Ten major ideas, each with Hook → Picture → Story → Name → Worked example → You try → Fail/fix → Current Practice → Retrieval → Teach-back.
- Full graded lab: setup gate, chore ADW, JSONL feature ADW, trigger swap, six stretch options, rubric, nine pass criteria, and cumulative oral check.
- Cumulative mastery: 16 retrieval questions, scoring bands, capstone teach-back, and 22-term glossary.
- Current practice: two YouTube overlays, within the ≤3 limit.

## Grounding protected

- JSONL support is explicitly absent from the shipped main branch and remains the student’s feature exercise.
- Demo identifiers and artifacts match the extract: issue #31 → PR #32, ADW `5615f7c8`; issue #33 → PR #34, ADW `cb881e79`.
- The course’s real imperfections remain visible: wrong ADW expansion, nonexistent-file claims, README inaccuracies, branch-docstring drift, and the wrong-directory `Failed to spawn`.
- Lab paths and commands use only `tac/tac-4` files. No external application repository is introduced.
- Course-era model names and CLI wrapper are framed as period implementation details; durable model policy and workflow architecture are preserved.

## Verification completed

- Extract gate: `_extracts/tac-4-afk-agents/STATUS.md` present and DONE.
- All 18 local chapter references resolve: four stylesheet paths, one generated plate, and all 12 distinct teaching frames (one health-check frame is intentionally reused in the lab/adoption narrative).
- No duplicate HTML IDs; all 30 internal anchor references resolve.
- Curriculum JSON parses successfully.
- Inline JavaScript passes syntax validation.
- HTML source order matches sticky/mobile navigation order and remains coherent without JavaScript.
- All 100 required major-idea pedagogy moves are present (10 moves × 10 ideas).
- Static HTML audit produced no non-legacy structural errors after filtering the installed validator’s HTML4-only complaints about HTML5 semantic elements.

## Open questions for Claude review

1. **Visual browser pass:** the in-app browser was unavailable in this sandbox. Please visually confirm desktop, mobile, and print layouts—especially the four-column PITER map, the full-width 1920×1080 frames, and long rubric cells.
2. **Density judgment:** 10.3k visible words plus 13 large figures estimates to 38–46 pages. Confirm whether this volume wants TAC-1’s 13k-word density exactly or accepts this lesson’s more diagram- and lab-heavy treatment.
3. **Current-practice freshness:** re-check the two overlay videos and the headless/SDK wording at publication time; this axis moves quickly.

## Review gate

The chapter build is complete. Interactive desktop/mobile/print visual QA remains required before promoting the curriculum status from `chaptered` to `reviewed`.

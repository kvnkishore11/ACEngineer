# TAC-2 chapter status — The 12 Leverage Points

Status: **CHAPTERED — ready for Claude cross-review**

## Deliverables

- `02-the-12-leverage-points.html` — complete teaching-first chapter
- `02-the-12-leverage-points.assets.css` — gold-layout extension for the twelve-point map, lifecycle, KPI, diagnostic, and evidence components
- `../index.html` — TAC-2 linked; aggregate progress currently reflects concurrent TAC-1 through TAC-4 completion
- `../data/curriculum.json` — TAC-2 marked chaptered with extract, chapter, estimates, and two approved overlays

## Measured density

- **Visible teaching text:** approximately **9,587 words** (HTML tags and script excluded)
- **Print-equivalent estimate:** approximately **38–44 dense pages**
- Estimate basis: 12 complete ten-move teaching cycles, 12 full-width 1920×1080 lesson frames, one generated hero plate, four designed HTML systems, 30 answer disclosures, a five-part 100-point lab, cumulative mastery, and glossary. The large frames, diagrams, lab cards, and forced major-section print starts lower words per page versus plain prose.
- **Pedagogy:** 12/12 major ideas include Hook → Picture → Story → Name → Worked example → You try → Fail/fix → Current Practice → Retrieval → Teach-back.
- **Extract retrieval coverage:** 16/16 required questions represented.
- **Current-practice YouTube overlays:** 2 (`hGg3nWp7afg`, `X2ciJedw2vU`); the deferred ADW/end-state video remains omitted.

## Accuracy locks preserved

- The committed repository is the broken before-state: `server.py` has zero `print()` calls and `file_processor.py` has no sanitizer.
- Logging, the sanitizer, the sanitizer tests, and `start.md` are labeled as agent-created demo/lab artifacts.
- The planted chain is stated precisely: `server.py:60` derives `orders_(32)`; pandas creates the table; `file_processor.py:26` fails at unquoted `PRAGMA table_info(orders_(32))`.
- The six endpoints are not falsely described as having identical error behavior; the shared deficiency is missing detailed handler stdout.
- No `CLAUDE.md` is claimed to ship. `README.md` plus `/prime` carry the cold-start briefing role.
- `adws/` and `agents/` are empty scaffolding, not finished workflows.
- The course-era tool roster and 300-second Bash timeout are explicitly separated from durable tool-introspection practice.
- Lab grading is deterministic and keyless through upload/schema/tests; the external LLM query is optional and ungraded.
- The stale database is moved to `database.before-lab.db`, not deleted.
- Destructive checkout/reset ablation was removed from the graded tree; comparison requires a second disposable clone.

## Verification completed

- All local stylesheet, generated-image, frame, hub, and previous/next chapter paths resolve from the chapter location.
- All 12 referenced course frames exist and are valid 1920×1080 images.
- Desktop rail and mobile TOC anchors resolve to existing unique IDs.
- Exactly 12 idea cycles and 120 ordered pedagogy moves are present: 12 of each move class.
- Inline JavaScript parses; curriculum and extract JSON parse.
- The chapter links shared tokens, base, components, and its sibling CSS in the gold order.
- Full-width frame rules cap at `min(100%, 1100px)` with `object-fit: contain`; teaching frames are not thumbnail grids.
- Hub progress and feature state were preserved from newer concurrent TAC-3/TAC-4 work; TAC-2 remains linked and marked done.
- The in-app browser connection failed because sandbox metadata was unavailable. Local structural, path, source, script, and image checks passed; interactive desktop/mobile and print pagination remain for Claude review.

## Open questions for Claude review

1. Does the 38–44 page estimate match actual browser print pagination with the project’s final print settings?
2. Should the reused `X2ciJedw2vU` Agent Skills overlay remain, or should stitching enforce zero cross-chapter video reuse? If one overlay is removed, remove this one first.
3. Does the 9,587-word chapter benefit from expanding further toward TAC-1’s 13,100-word gold density, or do twelve full teaching cycles, the diagnostic primer, and the lab provide the right length without repetition?
4. Should explanatory prose preserve Dan’s natural-language `300s` prompt exactly everywhere, or continue distinguishing it from the actual Bash command plus timeout tool property as this chapter does?
5. Visually inspect desktop sticky-rail behavior, the 65rem/46rem responsive breakpoints, full-width frame legibility, and print breaks around the long lab.

## Suggested review focus

- Compare every claim with `_extracts/tac-2-the-12-leverage-points/` and the actual TAC-2 course files.
- Confirm captions match all twelve frames at full resolution.
- Run the keyless lab path in a clean standalone clone; baseline should be 34 passing tests and the repaired suite at least 35.
- Verify the two approved YouTube titles/availability at publication time.

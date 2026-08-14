# STATUS: DONE ✅

TAC-1 "Hello Agentic Coding" extract — completed by Claude Fable (resume pass, 2026-07-12).
Scaffold (design/, data/, index.html, README.md, media/frames) was completed in the prior session; this pass produced the full `_extracts/tac-1-hello-agentic-coding/` deliverable set.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — all fields from the orchestration brief, filled from transcript/VTT/notes/codebase | ✅ valid JSON, schema-complete |
| `extract.md` | Master teaching notes — 8 major ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q; VTT-verified timeline map; glossary | ✅ |
| `nuggets.md` | 15 ranked nuggets in 3 tiers for weak learners + micro-quiz | ✅ |
| `outdated-vs-current.md` | 5 course-era→2026 gaps with book treatments; what hasn't aged; strict overlay decision | ✅ |
| `frame-plan.json` | 17 frames mapped (15 prior + 2 new: t0162 commander-of-compute, t1250 replace-yourself→diagram_instead); VTT anchors; unframed-beats rationale | ✅ valid JSON, all files on disk |
| `lab-spec.md` | 4-part lab, course codebase only (tac/tac-1), checkpoints + pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Verification performed

- `extract.json` and `frame-plan.json` parse via `python3 json.load`; all 26 required schema fields present.
- `codebase_map` covers all 7 real files under `tac/tac-1` (README.md, .claude/settings.json, .env.sample, programmable/{prompt.md,sh,py,ts}); runtime artifacts documented separately.
- All 17 frame files exist under `book/media/frames/tac-1/`; visuals spot-verified for t0162, t0790, t0845, t1250.
- Quotes/timestamps cross-checked against the 3690-line VTT; video duration 1311s confirmed via ffprobe.
- README "35 lines" claim verified exact.
- YT overlays: exactly 3 `include_in_phase1: true` (2TIXl2rlA6Q, 6fCqj4xFCZI, X2ciJedw2vU) — within the 1–3 limit; 2 deferred.

## Blockers

None.

## Caveats for the next stage (GPT chapter build)

- YT overlay IDs taken from the orchestration brief seed list; verify they resolve before publishing links (no video fetching done here, per brief).
- `current_practice_gaps` written against mid-2026 Claude Code (Skills, Agent SDK, permission modes); re-check at publish time.
- t1250 is B-roll — render the closing beat as a designed pull-quote (`diagram_instead: true`), not the frame.
- Do NOT rebuild scaffold files; only the vol-1-tac chapter HTML body remains out of scope for extract passes.

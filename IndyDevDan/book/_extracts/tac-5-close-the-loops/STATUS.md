# STATUS: DONE ✅

TAC-5 "Close the Loops" extract — completed by Claude Opus (resume pass, 2026-07-12).
The prior pass (Claude Fable, interrupted at its limit) produced `extract.json`, `extract.md`, `nuggets.md`, `frame-plan.json`, and all 12 frames. This resume pass produced the three remaining deliverables — `lab-spec.md`, `outdated-vs-current.md`, `STATUS.md` — and validated the JSON + frame set. No frames were re-extracted (12 good frames already on disk); the HTML chapter was not touched (out of scope for extract passes).

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — all 35 fields from the orchestration brief, filled from transcript/VTT/codebase | ✅ valid JSON (88.9 KB), schema-complete |
| `extract.md` | Master teaching notes — 10 ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q; VTT-verified timeline; glossary; TAC bridge | ✅ (prior pass) |
| `nuggets.md` | 15 ranked nuggets in 3 tiers for weak learners + 8-question micro-quiz | ✅ (prior pass) |
| `outdated-vs-current.md` | 6 course-era→2026 gaps (hooks, Skills, Agent SDK, computer-use, managed out-loop, model/UI) + what hasn't aged + strict overlay decision | ✅ this pass |
| `frame-plan.json` | 12 frames mapped with VTT anchors + 9 unframed-beats-by-design rationale; `status: complete` | ✅ valid JSON, all files on disk |
| `lab-spec.md` | 6 reproduce drills + 5 stretch drills, course codebase only (tac-5); checkpoints, pass criteria, instructor notes | ✅ this pass |
| `STATUS.md` | this file | ✅ this pass |

## Verification performed

- `extract.json` parses via `python3 json.load` — valid; 35 top-level keys present (all brief fields incl. `loop_model`, `closed_loop_prompt`, `tests_rule_of_law`, `e2e_testing`, `adw_test`, `observability`, `codebase_map`, `current_practice_gaps`, `lab`).
- `frame-plan.json` parses — valid; `status: complete`; 12 frames + 9 unframed-beats-by-design.
- **All 12 frame files present** under `IndyDevDan/book/media/frames/tac-5-close-the-loops/` and each matches a `frame-plan.json` entry (t0105, t0230, t0700, t0725, t0860, t0985, t1030, t1200, t1760, t2460, t2925, t2990). Two title-slide beats captured as `.jpg`, the ten screen-capture beats as `.png`.
- Video duration cross-checked: `frame-plan.video_duration_seconds` = `extract.json.video.duration_seconds` = 3232 s (53:52). ✅ consistent.
- `lab-spec.md` and `outdated-vs-current.md` derived directly from the extracted `lab`, `prerequisites_tools`, `current_practice_gaps`, and `yt_overlay_candidates` fields — no new claims invented; drill commands (ruff/pytest/py_compile/tsc/build/Playwright, `adw_test.py`, `/bug`, `/implement`) trace to `extract.md` worked examples.
- YT overlays: exactly 2 `include_in_phase1: true` (`X2ciJedw2vU` Skills, `6fCqj4xFCZI` Claude-Code-surface) — within the 1–3 limit; `fop_yxV-mPo` (Codebase Singularity) deferred to TAC-4/7/8.

## Blockers

None.

## Caveats for the next stage (chapter build)

- YT overlay IDs taken from the orchestration brief seed list; verify they resolve and titles match before publishing links (no video fetching done here, per brief).
- `current_practice_gaps` written against mid-2026 Claude Code (hooks-as-rails, Agent Skills, Agent SDK structured outputs, computer-use, E2B/managed sandboxes); re-check at publish time.
- Period-detail frames (YOLO "Bypassing Permissions" banner, `think hard` IDK, `'sonnet'|'opus'` model strings) get a one-line margin note, not a rewrite — the loops are unchanged.
- `estimated_print_pages_when_expanded` = 46 — this is the longest TAC lesson; budget chapter layout accordingly.
- Do NOT rebuild scaffold files or re-extract frames; only the vol-1-tac chapter HTML body remains out of scope for extract passes.

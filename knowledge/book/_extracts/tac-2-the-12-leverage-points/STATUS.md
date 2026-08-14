# STATUS: DONE ✅

TAC-2 "The 12 Leverage Points" extract — completed by Claude Fable (technical accuracy pass, 2026-07-12).
Full fan-out deliverable set produced per the locked plan and the tac-1 gold template + `vol-1-tac/01-CROSS-REVIEW-CLAUDE.md` fan-out checklist.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema mirroring tac-1 (28 top-level fields; `phase_model`/`ai_vs_agentic` adapted to `frameworks`/`stdout_demo` per lesson) — 12 core concepts, 33 VTT-anchored quotes, 16 retrieval Qs, full codebase map | ✅ valid JSON |
| `extract.md` | Master teaching notes — 12 ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q; VTT-verified timeline map; glossary with transcript corrections; bridge | ✅ |
| `nuggets.md` | 15 ranked nuggets in 3 tiers + micro-quiz | ✅ |
| `outdated-vs-current.md` | 6 course-era→mid-2026 gaps with book treatments; bonus period details; what hasn't aged; strict overlay decision | ✅ |
| `frame-plan.json` | 12 frames with VTT anchors, per-frame verified_visual notes, and unframed-beats rationale incl. diagram guidance | ✅ valid JSON, matches disk |
| `lab-spec.md` | 5-part graded lab (course codebase only), 4 checkpoints, 5 stretch drills incl. leverage-point ablation, pass criteria, instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

Frames: `book/media/frames/tac-2-the-12-leverage-points/` — 12 files, `t####-label.jpg`.

## Verification performed

- `extract.json` + `frame-plan.json` parse via python3 json; schema-parity diff against tac-1 gold shows only the two intended adaptations (`frameworks`, `stdout_demo`).
- `codebase_map.files` diffed against disk (`tac/tac-2`, excluding .git/node_modules/__pycache__/.venv): **49/49 exact match, zero drift**.
- Frame set triple-checked: disk == frame-plan.json == extract.json frame_plan (12/12); all 1920×1080 native (ffprobe); **every frame visually inspected this session** against its beat/caption (18 candidates extracted, 6 re-shot at nudged timestamps, best 12 promoted, rejects deleted).
- Quotes/timestamps cross-checked against the 2297-cue VTT (10s-bucket condensation); all 33 timestamps within video duration (ffprobe: 2834.08s → 47:14).
- Countable claims verified on disk: install.md **7 lines** (matches "very simple, seven line"); prime.md 7; tools.md 2; README.md 153; spec **749 lines** (matches "some 750 lines"); start.sh 80; tests 621 lines; `file_processor.py:26` is exactly the PRAGMA line the agent cites on-screen (frame t0965).
- Key accuracy finds locked into the extract: the repo ships the **before-state** (zero `print()` in server.py; no `sanitize_table_name`; the on-camera fixes are NOT committed — labs reproduce them); `orders_(32).csv` is the planted bug trigger; **no CLAUDE.md exists in tac-2** despite the verbal nod; `.claude/commands/start.md` is created live on camera (not shipped); settings.json carries TAC's first **deny list**.
- YT overlays: exactly 2 `include_in_phase1: true` (hGg3nWp7afg, X2ciJedw2vU) + 1 deferred (fop_yxV-mPo) — within the 1–3 limit; IDs sourced only from the tac-1-era vetted seed list (none invented, none fetched).

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- **Do not write the fixes into quoted repo listings**: server.py/file_processor.py must be shown in their committed (broken) state; the prints and sanitizer appear only as the demo/lab's agent-produced diffs.
- The one suspect transcript line ("empty set of slash commands" ~31:55) is flagged in confidence_notes — paraphrase as "a minimal starter set (3 commands)", do not quote it.
- t0630's tool roster and llm_processor's model pins (gpt-4.1-mini, claude-3-haiku-20240307) are period details — margin-note them, don't "fix" them.
- X2ciJedw2vU repeats from chapter 1: keep if the stitcher allows cross-chapter reuse, else drop it first (stated in its rationale).
- Render the SDLC five-step beat and the internal/external-docs beat as designed diagrams (see frame-plan `unframed_beats_by_design`); render the phase-one-confession close as a designed pull-quote (tac-1 t1250 pattern).
- Per the fan-out checklist: diff the chapter against `what_student_must_internalize` + all 16 `retrieval_questions` (tac-1's chapter dropped one claim — don't repeat that); update `data/curriculum.json` when the chapter lands; oembed-verify overlay IDs at review time.

# STATUS: DONE ✅

TAC-4 "AFK Agents" extract — completed by Claude Fable (fan-out pass, 2026-07-12), mirroring the tac-1 gold template and the 01-CROSS-REVIEW-CLAUDE fan-out checklist.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — all tac-1 fields adapted to tac-4 (tactic, mission, loop_model, piter, adw, 15 core_concepts, programmable_mode, demos, 31 quotes, 14 retrieval Qs, lab, overlays, frame_plan, full codebase_map) | ✅ valid JSON |
| `extract.md` | Master teaching notes — 10 major ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q; VTT-verified timeline map; glossary with transcript corrections; bridge to TAC-3/5 | ✅ |
| `nuggets.md` | 17 ranked nuggets in 3 tiers for weak learners + 7-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 7 course-era→mid-2026 gaps with book treatments; what hasn't aged; strict overlay decision table | ✅ |
| `frame-plan.json` | 12 frames (brief max) with VTT anchors + verified_visual notes; 7 unframed-beats rationales | ✅ valid JSON, all files on disk |
| `lab-spec.md` | 5-part lab, course codebase only (tac/tac-4 pushed to student's own repo), gated checkpoints + 9 pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Frames (media/frames/tac-4-afk-agents/)

12 frames at native 1920×1080 (video is 1920×1080@15fps, 2785s — never upscaled): 2 JPEG q:v 2 graphic slides (t0240 KPIs, t0521 PITER letter cards) + 10 PNG screen-recording frames (small terminal/editor/browser text kept sharp per brief). 18 candidates were extracted and visually reviewed before selecting 12; all selected frames verified in-session for content (ADW IDs, branch names, PR/issue numbers legible).

## Verification performed

- `extract.json` and `frame-plan.json` parse via python3 json.load.
- `codebase_map` covers **all 88 committed files** under `tac/tac-4` (programmatic walk vs map: 0 missing, 0 unmapped, descriptions 1:1); runtime artifacts (agents/, logs/, .env, *.db, run-branch specs) documented under `generated_not_committed`.
- All 12 frame files exist on disk; `frame-plan.json` and `extract.json.frame_plan` are identical lists; filenames consistent with t_seconds; no orphan files in the frames dir.
- Quotes/timestamps cross-checked against the 9298-line VTT (2234 unique cues, bucketed for scanning); accurate to ~5s.
- Video duration/resolution confirmed via ffprobe (2785.77s, 1920×1080@15fps).
- Countable claims verified against artifacts: adw_plan_build.py=536 lines, agent.py=262, health_check.py=396, 13 commands, 5 hook events, 12-entry allow / 3-entry deny lists, classifier contract (/chore|/bug|/feature|0), demo facts (issue #31→PR #32, ADW 5615f7c8, ~5 min; issue #33→PR #34, ADW cb881e79, feat-33-cb881e79-jsonl-support, ~17 min, 170-line plan).
- YT overlays: exactly 2 include_in_phase1 (hGg3nWp7afg, fop_yxV-mPo) — within the 1–3 cap; 1 listed-but-deferred (6fCqj4xFCZI, already anchors chapter 1). IDs exclusively from the tac-1 seed list (oembed-verified during TAC-1 cross-review); no invented IDs.

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- **Ground truths to protect:** the shipped app rejects non-.csv/.json uploads (server.py:77-78) — JSONL support is intentionally absent; the demo feature is the student's lab exercise. No .jsonl fixtures exist on main.
- **Honest-imperfection exhibits (use, don't sand off):** the demo PR's real errors ('Agentic Developer Workflow' mislabel, hallucinated file names); `adws/README.md`'s agent-flavored inaccuracies ('agent.py line 129' model pointer — reality: data_types.py Literals + adw_plan_build.py call sites; a Commit Format section that contradicts commit.md's `<agent_name>: <issue_class>: <message>` contract); adw_plan_build's docstring branch format drifting from the real /generate_branch_name contract; agent.py's dead 5-minute-timeout handler. These power the 'fix the system' idea and lab S2 — quote them accurately.
- Dan's on-camera 'Failed to spawn' wrong-directory error (~25:11) is preserved deliberately in frame t1540 and the lab — it is the #1 predicted student stall.
- The Mac mini's on-screen `adws/sandbox_poc.py` does NOT ship in the course repo (Dan's local extra) — do not claim it as a course file. agents/ trees on screen are runtime state.
- No secrets in frames: webhook URL was blurred on camera; env values were cut from the recording.
- Transcript is auto-generated — apply the corrections table in extract.md's glossary ('Devon'→Devin, 'Peter'→PITER, 'from principle to decoding'→'from Principled AI Coding', etc.).
- `current_practice_gaps` written against mid-2026 tooling (Agent SDK, GitHub-native agents, sandboxing, Skills); re-verify at publish — this axis moves fast.
- Chapter stem: `04-afk-agents` under `vol-1-tac/`; per the fan-out checklist, update `data/curriculum.json` (status, chapter_html) when the chapter lands and keep the hub in sync.

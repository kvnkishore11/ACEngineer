# STATUS: DONE ✅

TAC-8 "The Agentic Layer" extract — completed by Claude Opus (resume pass, 2026-07-13) after the prior Claude Fable session hit its limit mid-deliverable. The prior session had produced `extract.json`, `extract.md`, and the 12 full-res frames under `media/frames/tac-8-the-agentic-layer/`. This pass produced the five remaining deliverables (`frame-plan.json`, `lab-spec.md`, `outdated-vs-current.md`, `nuggets.md`, `STATUS.md`), rendered from the already-complete `extract.json` sections and the `extract.md` master teaching notes, and validated the full set against the gold TAC-1 extract schema.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — all fields from the orchestration brief, filled from transcript/VTT/codebase | ✅ valid JSON, 33 top-level fields, none empty |
| `extract.md` | Master teaching notes — 10 major ideas (Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q); VTT/audio-verified timeline map; glossary | ✅ (prior session) |
| `nuggets.md` | 15 ranked nuggets in 3 tiers for weak learners + 8-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 7 course-era→2026 gaps (each = packaging upgrade of a still-valid primitive) with book treatments; what hasn't aged; strict overlay decision | ✅ |
| `frame-plan.json` | 17 beats mapped: 12 real frames (all on disk) + 5 `diagram_instead` for beats lost to the capture freeze; mm:ss timestamps + vtt_anchors + capture-defect note | ✅ valid JSON |
| `lab-spec.md` | 6-part lab across app1/app2/app4/app5 (app3 skipped as on camera), course codebase only (tac/tac-8), checkpoints + pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Verification performed

- `extract.json` and `frame-plan.json` both parse via `python3 json.load`; `extract.json` has all 33 top-level schema fields with **no empty/blank critical fields** (`core_concepts`=15, `quotes`=24, `step_by_step_demo`=25, `frame_plan`=17).
- `frame-plan.json` = 17 beats: **12 real** (`file` non-null) + **5 diagram_instead** (`file: null`). A disk check confirms all 12 real frame files exist under `media/frames/tac-8-the-agentic-layer/`; the 13th directory entry is `_cand/` (raw extraction candidates), not a frame.
- Frame timestamps (mm:ss of `t_seconds`) were cross-checked against `extract.md`'s timeline map and per-idea frame references — all 12 align (t0385=6:25 five-apps, t0430=7:10 MVAL, t0515=8:35 /prime, t0610=10:10 chore, t0810=13:30 gateway, t1131=18:51 main.sh, t1320=22:00 seven-tasks, t1400=23:20 in-progress, t1540=25:40 states, t1720=28:40 sparse worktree, t1835=30:35 Notion, t2065=34:25 plan_uv_mcp).
- `lab-spec.md`, `outdated-vs-current.md`, and `nuggets.md` were rendered directly from the corresponding `extract.json` sections (`lab`, `current_practice_gaps` + `yt_overlay_candidates` + `prerequisites_tools`, and `quotes` + `common_weak_student_failures` + `guiding_question` + `tactic`) plus the 10 ideas in `extract.md` — no new claims introduced beyond those sources.
- Video: duration 3799s / 63:19 confirmed from `extract.json.video`.
- YT overlays: `frame_plan`-independent overlay decision uses `yt_overlay_candidates` — exactly **2** `include_in_phase1: true` for this chapter (`fop_yxV-mPo` Codebase Singularity, `hGg3nWp7afg` 3 Codebase Folders), within the 1–3 limit; `X2ciJedw2vU` deferred to avoid double-placement with the TAC-1 chapter.

## Blockers

None.

## Caveats for the next stage (GPT chapter build)

- ⚠️ **Capture defect is material.** The screen-capture freezes at ~34:30 (t~2070s); everything after (~35:45 on) is audio-only in this recording — the Notion board zoom-out, the MCP sysinfo payoff, the **entire app5 AEA demo**, the tactics recap, PITER→PITE, the agentic-layer definition, and the **final-question reveal**. Those five payoff beats are `file: null` / `diagram_instead: true` in `frame-plan.json` and MUST be rendered as designed graphics (ring diagram, AEA app mock, PITER→PITE transform, definition equation card, full-bleed final-question pull-quote), not screenshots. See `extract.json.video.capture_defect`.
- `frame-plan.json` vtt_anchors for the 5 diagram beats are drawn from the `quotes` list / timeline (audio-verified), not from frames — treat their exact timestamps as approximate.
- `current_practice_gaps` written against mid-2026 Claude Code (Agent Skills, Claude Agent SDK, permission modes/sandboxing/hooks, native background+scheduled agents); re-check at publish time.
- YT overlay IDs/titles taken from the orchestration brief's seed list; verify each resolves and matches its title before publishing overlay links (no video fetching performed in this extract pass, per brief).
- The lab runs all ADWs with `--dangerously-skip-permissions` (as the course does); the chapter should carry the safety/permissions callout from `outdated-vs-current.md` §3.
- Do NOT rebuild scaffold files; only the vol-1-tac chapter HTML body remains out of scope for extract passes. `_cand/` under the frames dir can be ignored or pruned — it holds unused raw frame candidates.

---

## Independent technical-accuracy verification (second pass · Claude Opus · 2026-07-13)

A fresh technical-accuracy expert re-ran the fan-out from scratch (not knowing the prior pass had completed), then, on discovering the finished set, switched to **verify-and-reconcile rather than clobber**. Verdict: **PASS — extract confirmed accurate and complete.** Nothing in the extract contradicted independent research; one cosmetic inconsistency was fixed and 9 duplicate candidate frames were pruned.

**Independently re-derived (not trusting the prior pass):**
- **Codebase re-mapped via 4 parallel sub-agents**, one per app (2/3/4/5), plus app1 read directly. Every load-bearing claim corroborated: task-marker glyphs `[]`/`[⏰]`/`[🟡, id]`/`[✅ hash, id]`/`[❌, id]` (verbatim from `app2 data_models.py`); tags `{opus}` / `{adw_plan_implement_update_task}`; cron intervals **5s (app2) / 15s (app4)**, `--once`; `subprocess.Popen(start_new_session=True)`; the `--resume cc_session_id` session exception at **`app5 adw_aea_patch.py:228-233`**; AEA server = FastAPI on **port 8743**; Notion statuses `Not started / In progress / HIL Review / Failed / Done`; `plan_uv_mcp` as the MCP builder; the 12 leverage points printed verbatim in the app1/app2 READMEs.
- **Capture freeze independently confirmed.** Dense frame-hash sampling shows live, forward-progressing content to **~2116s (35:16)**; from ~2148s to the end the video track cycles a tiny loop (only 3 unique frames across 2200–3780s). This matches the prior pass's `capture_defect` exactly — the app5 AEA demo, the 12-leverage recap, PITER→PITE, and the final-question reveal have **no real screen video** and are correctly flagged `diagram_instead`.
- **Frames re-extracted and cross-checked.** Independent decode-based extraction (fast input-seek is unreliable in this file's back half — use frame-number `select`) reproduced **byte-identical** files for t0430 and t1835, and spot-viewing confirmed t0385 (five-app `ls`) and t1131 (composed-ADW payoff: plan path `specs/chore-eae01d83-…md`, the 4 `cc_*`/summary output files, Phase-1 planner → Phase-2 builder, `apps/main.sh`) match their `frame-plan.json` descriptions and multiple `extract.json` claims.

**Automated checks:** `extract.json` + `frame-plan.json` parse; **all 72 `codebase_map.files` paths exist on disk (0 missing)**; app1 `apps/main.py`/`main.ts` print exactly `"Hello, agentic coding world!"` as claimed; PITER/PITE, port 8743, session/`--resume`, AEA, `🟡`, and "Prioritize Agentics" appear consistently across all deliverables; frame-plan references exactly **12 real frames (all present) + 5 `diagram_instead`**.

**Changes applied this pass (surgical only, gold-review discipline):**
1. `extract.json` `video.capture_defect`: "Peter-to-Pete" → **"PITER-to-PITE"** (the only phonetic leak; every other mention already uses the canonical PITER/PITE).
2. Frames dir reduced from 21 → **the canonical 12**: removed 9 duplicate/near-duplicate candidates this pass had extracted under alternate labels (2 were byte-identical to the canonical frames). No canonical frame was touched; `frame-plan.json` still matches the dir exactly.

**Minor note for the chapter author (not corrected — descriptive, on a self-study app):** app3's active `.claude/settings.json` wires the 6 local lifecycle hooks but does **not** invoke `send_event.py`; the observability event flow described in `codebase_map` reflects app3's README/architecture, and app3's copy is partial (no `tasks.md`, some task-board commands absent, a hardcoded app2 target dir). app3 is skipped on camera and assigned as self-study, so this does not affect the on-camera narrative.

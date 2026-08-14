# STATUS: DONE ✅

TAC-7 "ZTE: The Secret of Agentic Engineering" extract — completed by Claude Opus (resume pass, 2026-07-13).
The prior session (Claude Fable, interrupted at its limit) produced `extract.json`, `extract.md`, and all 12 full-resolution frames. This resume pass produced the five missing deliverables — `frame-plan.json`, `nuggets.md`, `lab-spec.md`, `outdated-vs-current.md`, and this `STATUS.md` — reconstructing the frame plan from the embedded `frame_plan` in `extract.json` plus `extract.md`, and re-validating the machine artifacts. No frames were re-extracted and no HTML chapter was written (both out of scope for this pass).

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — 33 sections: tactic, mission, velocity_scale, piter_to_pite, secret, 12 core_concepts, sdlc_zte_pipeline, worktree/trigger mechanics, programmable agent invocation, step-by-step demo, quotes, retrieval Qs, codebase_map, current_practice_gaps, YT overlays, embedded `frame_plan` + `lab`, confidence_notes | ✅ valid JSON, schema-complete, no empty critical fields (535 lines) |
| `extract.md` | Master teaching notes — 12 major ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q; VTT-verified timeline map; Dan-ism glossary; bridge to rest of TAC | ✅ (prior pass) |
| `nuggets.md` | 15 ranked nuggets in 3 tiers for the struggling learner + 6-question micro-quiz | ✅ (this pass) |
| `lab-spec.md` | 7-section capstone lab (setup → adw_sdlc_iso run → deliberate in-loop → heavy compute knob → patch vs SDLC → ZTE ceremony + uppercase interlock → KPIs/cleanup) + 8 stretch drills + pass criteria + instructor notes; course codebase only | ✅ (this pass) |
| `outdated-vs-current.md` | 6 course-era→2026 gaps with book treatments; what hasn't aged; strict phase-1 overlay decision (exactly 3) | ✅ (this pass) |
| `frame-plan.json` | 12 frames mapped with VTT anchors + verified_visual; 3 unframed-beats-by-design | ✅ valid JSON, all files on disk, 1:1 |
| `STATUS.md` | this file | ✅ (this pass) |

## Frames (media/frames/tac-7-zte-secret-of-agentic-engineering/)

12 frames, all present and non-empty, native 1920×1080 (10 PNG for text-heavy UI/code/terminal/browser, 2 JPEG q=2 for the photographic desk-overlay beats):
`t0100-velocity-scale.jpg`, `t0250-issue-as-prompt.png`, `t0372-webhook-events-terminal.png`, `t0535-adws-directory.png`, `t0680-worktrees-trees-dir.png`, `t0890-adw-state-json.png`, `t1010-model-map-agents-py.png`, `t1290-review-screenshot-proof.png`, `t1912-tactic-target-zte.png`, `t2135-zte-initiation-issue.png`, `t2765-secret-composable-primitives.png`, `t2958-zte-shipped-app.jpg`.

## Verification performed (this pass)

- `extract.json` parses via `python3 json.load` — **VALID**, 33 top-level sections, 535 lines. Checked 11 critical fields (`tactic`, `velocity_scale`, `secret`, `core_concepts`, `sdlc_zte_pipeline`, `codebase_map`, `lab`, `frame_plan`, `current_practice_gaps`, `retrieval_questions`, `confidence_notes`) — **none empty**. No fields needed backfilling.
- `frame-plan.json` parses — **VALID**, declares 12 frames; 12 files exist on disk; 0 zero-byte files. Every frame filename maps 1:1 to a file (0 disk files missing from the plan, 0 plan files missing from disk).
- **Spot-verified 2 of 12 frames by opening them this pass** (Read renders images): `t1912-tactic-target-zte.png` — confirmed the "Tactic — Target Zero-Touch Engineering" card, 07 circled red, presence-2→1 definition, and all five Daily Actions incl. "Go from PITER to PITE"; `t2765-secret-composable-primitives.png` — confirmed "The Secret: Composable Agentic Primitives" with the three columns (Agentic Primitives / ADW steps / Composed Workflows incl. "ANY WORKFLOW") and the "SDLC is just one possible composition" caption. Both matched `extract.md` exactly, so the prior pass's frames are trusted; the remaining 10 `verified_visual` descriptions derive from `extract.md`'s Picture/timeline lines and the embedded `frame_plan`, not a fresh open.
- YT overlays: exactly **3** `include_in_phase1: true` (`fop_yxV-mPo`, `6fCqj4xFCZI`, `X2ciJedw2vU`) — within the 1–3 cap; `hGg3nWp7afg` deferred. Overlay decision table in `outdated-vs-current.md` matches `extract.json`'s `yt_overlay_candidates`.
- Companion files cross-checked against `extract.json`/`extract.md` for factual consistency: 14 adw_*.py workflow scripts; 33 command .md (27 + 6 e2e); 10 state fields, ship requires 8 non-null; 18-command model map with exactly 8 heavy→opus; ports 9100–9114/9200–9214 (15 slots); retry `[1,3,5]s`; webhook port 8001; cron 20s; both SDLC orchestrators hardcode `--skip-e2e`; uppercase-ZTE interlock; merge is `--no-ff` + push (not the README's "squash").

## Blockers

None.

## Caveats for the next stage (chapter build)

- **On-video runs are NOT the committed snapshot — do not conflate.** The video's issues #51 (drop zone), #52 (JSON export), the heavy random-data feature, #54 (o4-mini bump; review reported 78 tests passing), the CSV-text patch, and ZTE #62 (background→green, shipped on-screen at 49:14), plus their adw_ids and ports (9106/9206), are Dan's *runtime* values — they are NOT in the distributed repo. The committed snapshot instead carries earlier evidence: issues 3/9/15/47 → five `app_docs/feature-*.md` (incl. light-sky-blue `#E0F6FF` background and the shipped "Upload" button), one spec, `agents/` run dirs, and `agentic_kpis.md` (run cc73faf1, presence 1.0). Render on-video numbers as illustrative; students' values will differ.
- **Doc/code drifts found this pass — do NOT repeat them in the chapter, teach them as the "verify against source" lesson:** `adws/README.md` says ship "approves the PR + squash" but `adw_ship_iso.py` does a manual `git merge --no-ff` + push (Dan's narration matches the CODE); the README's branch-name example lacks the `issue-`/`adw-` prefixes the code and committed artifacts use; `worktree_ops.remove_worktree` has an unimported-`shutil` fallback. And both SDLC orchestrators hardcode `--skip-e2e` — E2E runs only via standalone `adw_test_iso.py`.
- **Naming duality is intentional — keep both:** tactic = **Zero-Touch Engineering** (course card at 31:52); code/docstrings/GitHub-bot comments = **Zero Touch Execution** (`adw_sdlc_zte_iso.py`). Same acronym, both appear in course artifacts.
- **Unframed-by-design beats** (bottleneck/KPI realization ~30:45–31:56; four-futures monologue ~38:55–40:40; highest-leverage close + lesson-8 teaser ~49:38–53:20) should be rendered as designed pull-quotes/diagrams per `frame-plan.json` `unframed_beats_by_design`, **not** as missing frames. Pair the KPI beat with a scoreboard sourced from the committed `agentic_kpis.md`.
- `current_practice_gaps` written against mid-2026 Claude Code / Agent SDK (native worktree-isolated agents, Skills, the Agent SDK, Claude 5-era models) — re-check at publish; this axis moves fast.
- YT overlay IDs come from the orchestration seed pool (oembed-verified in the TAC-1 cross-review); verify each resolves and its content matches its title before publishing links — **no video fetching was performed in this pass**, per brief.
- Do NOT rebuild the extract artifacts or re-extract frames; only the vol-1-tac-7 chapter HTML body remains out of scope for extract passes.

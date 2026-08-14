# STATUS: DONE ✅

AH-6 "Building Agentic Layers" technical-accuracy extract — completed 2026-07-13 (max-reasoning pass).
This is the **capstone** lesson of the whole 14-lesson arc (TAC 1–8 + AH 1–6). Deliverables written only under `book/_extracts/ah-6-building-agentic-layers/` and `book/media/frames/ah-6-building-agentic-layers/`. Course source trees were read only, never modified. No chapter HTML written (Codex builds that next).

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema mirroring tac-1, adapted: tactic, mission, codebase_singularity, agentic_layer_model, full class_grade_taxonomy (Class 1 G1–7, Class 2 G1–2, Class 3 G1–3, each with codebase evidence), core_concepts, recap of the whole course, step_by_step_demo, 31 quotes, retrieval, lab, codebase_map, current_practice_gaps, yt overlays, confidence_notes | ✅ valid JSON (29 keys) |
| `extract.md` | Master teaching notes — 7 major ideas each Hook→Picture→Worked example→Name→Failure→Retrieval; the class/grade ladder table; VTT-verified timeline; glossary; "facts the chapter must not get wrong" | ✅ |
| `nuggets.md` | 18 ranked nuggets in 3 tiers for weak learners + 8-question self-quiz | ✅ |
| `outdated-vs-current.md` | 5 course-era→mid-2026 gaps with book treatments; what has NOT aged; strict overlay decision (1 phase-1) | ✅ |
| `frame-plan.json` | 13 frames mapped with t_seconds, VTT anchors, why_for_weak_student, verified_visual; render-as-quote + unframed-beats rationale | ✅ valid JSON, all 13 on disk |
| `lab-spec.md` | 6-part gradable lab (course codebase only) — layer audit, ADW comprehension, CLI ADW, orchestrator ADW, agent-expert loop, self-grade — with checkpoints + pass bars + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Frames (13, native 1920×1080, all visually verified in-session)

`media/frames/ah-6-building-agentic-layers/`:
1. `t0382-agentic-layer-diagram.jpg` — the class/grade taxonomy (green agentic ring vs dark app layer; Class 1/2/3)
2. `t0558-class3-destination-demo-ui.jpg` — orchestrator UI kicks off `plan_build_review_fix`; ADWS swimlane
3. `t0812-class1-grade2-subagents.jpg` — `fetch_docs.md` sub-agent (haiku → ai_docs/)
4. `t0895-class1-grade3-mcp-tools.jpg` — `.mcp.json` (postgres/firecrawl/atlassian/notion)
5. `t1088-class1-grade4-closed-loop.jpg` — `app_reviews/` outputs
6. `t1288-class1-grade5-templates.jpg` — layer annotated with bug/feature/chore/api templates
7. `t1768-class1-grade6-prompt-chain.jpg` — `scout_then_plan.md` (parallel scouts via Task)
8. `t2015-class1-grade7-agent-experts.jpg` — labeled file tree + agent-expert compute-advantage
9. `t2258-class2-grade1-outloop-webhook.jpg` — out-loop ring: webhook → agent core → prompt
10. `t2464-class2-grade2-adw.jpg` — double ring; nodes = the ADW files
11. `t2776-class3-orchestrator-inventory.png` — full agentic-layer inventory (commands/templates/ADWs/10 tools) [PNG for small text]
12. `t3124-class3-grade3-final-ui.jpg` — final LOGS stream: fix agent "ALL FIXED" + ADW_STEP events
13. `t3518-prioritize-agentics-recap.jpg` — Tactic 08 title card

## Verification performed

- `extract.json` and `frame-plan.json` both parse via `python3 json.load`. extract.json = 29 top-level keys, 31 quotes, 12 retrieval Qs, 8 core_concepts, 3 yt candidates (1 phase-1).
- **All 13 frame files exist on disk and exactly match `frame-plan.json`** (0 missing, 0 orphans); all confirmed native **1920×1080** via ffprobe; every frame visually inspected this session (see `verified_visual` fields).
- **All 40 cited codebase paths verified to exist on disk** (canonical tree, `.upstream/` excluded), including migration `9_ai_developer_workflows.sql`, `review-agent.md`, and `AdwSwimlanes.vue`.
- Video specs confirmed via ffprobe: h264 **1920×1080**, **3983.93s (1:06:24)**. recording.json's 2880×1620 is the CDP capture surface, not the encoded MP4 — no upscaling done.
- Codebase claims cross-checked by direct reads + two independent read-only mapping agents (34 and 62 tool-uses). Key corrections baked in: **10** orchestrator tools (not 8), **7** DB tables (not 6), backend port **9403** (8002 stale), orchestrator default model **opus-4-5**, no literal "start adw:" parser.
- Quote timestamps bucketed from the 12,654-line VTT (~10s accuracy); auto-transcription errors corrected (PITER→"Peter", Agent SDK→"Asian SDK", grade→"Great", etc.).

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- The per-grade "example project structures" are idealized teaching diagrams; the repo consolidates some rungs (templates inside `plan.md`; out-loop via `start_adw`/`adw_manual_trigger.py`, not a literal webhook). Do NOT print idealized filenames as if they exist verbatim — see `current_practice_gaps` and the `codebase_note` fields.
- Render the codebase-singularity definition beat (~4:24) as a **designed pull-quote**, not a frame (it's B-roll). Grade-1 has no standalone frame by design (smallest ring in t0382 covers it).
- YT overlay IDs are proposed conservatively (no seed list in this brief); all flagged `verify: true`. Confirm they resolve before publishing links. Exactly **1** is `include_in_phase1: true` (`fop_yxV-mPo` Codebase Singularity) — within the 1–3 cap.
- `current_practice_gaps` written against mid-2026 Claude Code (Skills, Agent SDK, permission modes); re-check at publish.
- Out of scope, untouched: full chapter HTML, PiCanvas, full YT video downloads.

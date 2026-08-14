# STATUS: DONE ✅

AH-5 "Agent Experts" technical-accuracy extract — completed by Claude (Opus 4.8), single session.
Role: technical accuracy expert. Wrote ONLY under `IndyDevDan/book/`. Course source trees read-only. No chapter HTML (Codex's next step). No PiCanvas. No full-video downloads.

## Files in this extract (`_extracts/ah-5-agent-experts/`)

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — gold tac-1 fields adapted to ah-5 (tactic, mission, act_learn_reuse, self_improving_template_meta_prompt, meta_agentics, 13 core_concepts, two_experts_compared, product_agent_experts, challenges, when-to/not, step_by_step_demo, quotes, retrieval, lab, codebase_map, current_practice_gaps, yt_overlay_candidates, frame_plan, confidence_notes) | ✅ valid JSON (36 top-level keys) |
| `extract.md` | Master teaching notes — 12 major ideas, each Hook → Picture → Worked example → Dan's words → Failure mode → Retrieval; VTT-verified timeline map; glossary | ✅ |
| `nuggets.md` | 17 ranked nuggets in 3 tiers for weak learners + 7-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 6 course-era→mid-2026 gaps with book treatments; what hasn't aged; strict phase-1 overlay decision | ✅ |
| `frame-plan.json` | 12 frames mapped with VTT anchors + in-session `verified_visual` + unframed-beats rationale + coverage_check | ✅ valid JSON; all 12 files on disk |
| `lab-spec.md` | 5-section lab, course codebase only (agent-experts); gradable checkpoints + pass criteria + instructor notes; "never hand-edit expertise" is the graded prime directive | ✅ |
| `STATUS.md` | this file | ✅ |

## Frames (`media/frames/ah-5-agent-experts/`, 12 × native 1920×1080)

t0456 meta-prompt→question-mermaid · t0508 meta-skill→start-orchestrator · t0580 experts dir · t0628 db expert reads-expertise-then-validates (Reuse) · t0742 db ER-diagram answer · t1255 self-improve Learn rubric · t1305 **Act/Learn/Reuse core** · t1598 websocket plan_build_improve composition · t2019 websocket pipeline metrics (81.8k/61.4k, context isolation) · t2182 websocket expertise-file anatomy (677 lines) · t2545 Nile new-user (before) · t2588 Nile personalized generative UI (after).

Arc coverage: concept → meta-agentics (2) → database partial-expert (3) → learn mechanism (1) → websocket complete-expert (3) → product expert before/after (2). 16 candidates extracted, all reviewed in-session, curated to 12; 4 deleted; 3 renamed post-review when live content differed from the label guess.

## Verification performed

- `extract.json` and `frame-plan.json` both parse via `python3 json.load`. extract.json = 36 top-level keys; frame_plan array = 12; yt_overlay_candidates with `include_in_phase1: true` = **2** (within the 1–3 limit).
- All 12 frame files exist on disk at **1920×1080** (ffprobe-confirmed), 97–205 KB each; every frame **visually inspected this session** (see `verified_visual` in frame-plan.json) — not just extracted blind.
- `codebase_map` covers every file demonstrated on-screen plus the two apps the experts operate on; all paths verified to exist under `agentic-horizon/agent-experts`. Line counts confirmed via `wc -l` (database expertise 412 / websocket 676; self-improve 179 / 190).
- Quotes/timestamps cross-checked against the **2991-cue VTT** (flattened to a timestamped digest); video duration 3749 s / 62:29 confirmed via ffprobe.
- Transcript OCR/ASR quirks decoded and noted (Niall→Nile, RAR SQL→raw SQL, JSNP→JSONB, dot claw→.claude, loop box→loot box).

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- **YouTube overlays — fail-loud flag:** the single strongest overlay for this lesson (agent memory / self-improving agents) has **no verified video ID** and is intentionally `video_id: null` / "NEEDS LOOKUP" in extract.json. The two inherited IDs (`X2ciJedw2vU`, `fop_yxV-mPo`) come from the TAC-1 orchestration seed list and must be re-verified for topical match before any link is published. Do not publish overlay links unverified.
- **"99 line prompt" vs current files:** Dan calls the database self-improve a "99 line prompt" on camera; the file in the repo is 179 lines (websocket 190). Likely an earlier/abridged version or the visible-workflow portion — flagged in extract.json confidence_notes. Use the file's real line count in the chapter.
- **Model IDs are period detail:** on-screen IDs are the Claude 4.5 family (opus-4-5-20251101 / sonnet-4-5-20250929 / haiku-4-5-20251001). Add a margin note; don't present them as current.
- **`current_practice_gaps`** written against Claude Code/Anthropic tooling as of mid-2026 (Skills, Agent SDK, memory tool); re-check at publish time — this axis moves fast. The two gaps Dan *gestures at himself* (memory-file-vs-expertise-file; Skill/SDK packaging) are the safest to foreground.
- **Video style:** the recording composites Dan's faint overhead desk-cam over the screen throughout (authentic course look). Present in every frame; content stays legible — not an extraction defect.
- **Do NOT rebuild scaffold** (design/, index.html, media infra). Only the `vol-2-ah/13-agent-experts` chapter HTML body remains, and that is out of scope for this extract pass.

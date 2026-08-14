# STATUS: DONE ✅

AH-2 "Seven Levels Agentic Prompt Formats" extract — completed by Claude (technical-accuracy fan-out pass, 2026-07-13).
Deliverable set produced under `_extracts/ah-2-seven-levels-agentic-prompt-formats/` + 12 frames under `media/frames/ah-2-seven-levels-agentic-prompt-formats/`. Nothing written outside `book/`; course source trees read-only.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — tactic, mission, stakeholder_trifecta, 12 core_concepts, seven_levels, sections_catalog (13), tier_list (grid-verified), input_workflow_output, static/dynamic vars, system_vs_user, step_by_step_demo, 20 quotes, 12 retrieval Qs, codebase_map, current_practice_gaps, yt_overlay_candidates, frame refs, confidence_notes | ✅ valid JSON, 32 top-level keys |
| `extract.md` | Master teaching notes — every major idea as Hook → Picture → Worked example → Name → Failure → Retrieval; the seven-levels table; the graded sections table; frameworks; system-vs-user; cross-refs | ✅ |
| `nuggets.md` | 17 ranked nuggets in 3 tiers for weak learners + 7-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 5 course-era→mid-2026 gaps with book treatments; "what hasn't aged"; strict overlay decision table | ✅ |
| `frame-plan.json` | 12 frames — t_seconds, label, shows, why_for_weak_student; suggested designed diagrams | ✅ valid JSON, all files on disk |
| `lab-spec.md` | 6-part + 4-stretch lab, course codebase only; gradable checkpoints + pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Verification performed

- `extract.json` and `frame-plan.json` parse via `python3 json.load`.
- **Tier list is ground-truth-verified:** all 13 sections + 7 formats reconciled against Dan's spoken grades AND the completed on-screen grid in `t2740-final-tier-list.jpg` (~45:40). Zero conflicts. (e.g. Workflow S/C, delegate S/A, template_metaprompt S/S, Report B/C, Title C/D.)
- All **12 frame files exist** on disk at 1920×1080; `frame-plan.json` filenames == disk filenames (exact set match). Each frame was visually inspected in-session for sharpness + correct content; talking-head/transition candidates rejected and re-shot; two rejected alternates deleted.
- `codebase_map` covers every committed file group: the 22 command/expert prompts, 3 sub-agents, hooks, settings.json, output-styles, utils, ai_docs, and the full `apps/prompt_tier_list/` Vue app (with `entities.ts` as the definitive 13-section + 7-format source). Runtime artifacts (specs/, adws/, agentic_drop_zone/, scraped ai_docs/*.md, settings.local.json) documented as generated-not-committed.
- Quotes/timestamps cross-checked against the 2884-cue VTT; video duration 3441s / 57:21 confirmed via ffprobe + recording.json.
- YT overlays: exactly **2** `include_in_phase1: true` (within the 1–3 limit), 1 deferred.

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- **YT overlay IDs are `null` / `needs_id_verification: true` on purpose** — this brief supplied no seed ID list (unlike TAC-1). Titles/mappings are accurate to the lesson's named gaps and cross-references; source and verify real IndyDevDan video IDs before publishing links. Do NOT fabricate IDs.
- **Capture-vs-code detail to preserve:** `t_metaprompt_workflow.md`'s on-screen purpose says "follow the `Instructions`"; Dan corrects it live to "Workflow"; the shipped file says "Workflow." Frame `t2280` shows the pre-correction video state — caption it accordingly.
- **Doc-drift to note, not fix:** `entities.ts` defines **13** section entities; `prime_tier_list.md` and the README say **12** (they predate "## High Level Prompt" being split out). Canonical count = 13.
- **Model ids are period detail:** `claude-opus-4-1-20250805` is pinned in quick-plan/background metadata; annotate the two frames that show it, don't "correct" it.
- The tier-list grid (`t2740`) should be redrawn as a crisp print figure — it's the chapter centerpiece (see frame-plan `suggested_designed_diagrams`).
- Cross-links resolved for the volume map: AH-1 (R&D / context engineering), AH-3 (Claude Code SDK / system-prompt overwrite), AH-4 (the O-agent / parallel scaling), TAC-7 (ZTE), TAC-4 (AFK).
- Out of scope (untouched, per brief): full chapter HTML, PiCanvas, full YT video downloads.

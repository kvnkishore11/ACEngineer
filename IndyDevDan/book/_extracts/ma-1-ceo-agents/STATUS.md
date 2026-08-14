# STATUS: DONE ✅

MA-1 "CEO Agents" technical-accuracy extract — completed by Claude (Opus, max reasoning), 2026-07-13.
Sources fully read: lesson transcript (2,366-line md), lesson.json/metadata, and the entire `agentic-horizon-extras/ceo-agents` codebase (extension + 5 modules, config YAMLs, all 9 agent prompts, brief template + acquisition brief + context files, a real memo, the CEO expertise scratch pad, the multimodel config, skills, specs). Gold schema mirrored from `tac-1` and adapted to this lesson.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — 31 top-level keys: tactic, mission, three_innovations, 12 core_concepts, innovations_detailed, full system_architecture (incl. verified spec-vs-implementation gaps), deliberation_flow, 9 board_members, brief_to_memo, 27 quotes, retrieval, teach-back, codebase_map (all real files + runtime artifacts), current_practice_gaps, yt_overlays, frame_plan summary, confidence_notes | ✅ valid JSON |
| `extract.md` | Master teaching notes — 12 major ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval; timeline map; glossary | ✅ |
| `nuggets.md` | 20 ranked nuggets in 3 tiers (incl. the two technical gotchas) + 8-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 5 drift items (model versions, 1M-as-table-stakes, the two spec-vs-code gaps, Pi/harness churn, single-vendor vs diversity); what hasn't aged; strict overlay decision | ✅ |
| `frame-plan.json` | 12 frames mapped with transcript anchors, why-for-weak-student, format, caveats; unframed beats; clean-SVG alternatives | ✅ valid JSON, all files on disk |
| `lab-spec.md` | 5-part lab, course codebase only, gradable checkpoints + pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Frames — 12 extracted (native 4K, 3840×2160)

`book/media/frames/ma-1-ceo-agents/` — 7 JPEG (`-q:v 2`) for TUI/diagram/chart/terminal, 5 PNG for dense VS Code text:

- `t0076` 1M-context retrieval chart · `t0585` boot roster + models + 1M badges · `t1672` CEO→board architecture diagram · `t0990` config YAML constraints · `t1122` CEO agent front matter · `t1905` Moonshot personality prompt · `t1235` brief + brief library · `t0760` parallel deliberation + vote tally · `t0900` [MAX REACHED] constraint stop · `t1420` conversation.jsonl observability + SVGs · `t0468` memo decision-map output · `t1052` TTS closing-the-loop summary.

Coverage spans all three innovations + the full brief→deliberation→memo flow. Source is native 4K/AV1, so no upscaling; ~18 candidate timestamps were previewed and the best 12 selected (UI/architecture/code favored over talking heads, per brief).

## Verification performed

- `extract.json` and `frame-plan.json` parse via `python3 json.load`.
- All 12 frame files referenced in `frame-plan.json` exist on disk at 3840×2160 (missing: 0); architecture-diagram + conversation.jsonl frames visually spot-checked for legibility.
- `codebase_map` covers every real file (extension + modules, both config YAMLs, all agent prompts, briefs, expertise, skills, commands, ai_docs, specs); runtime artifacts documented separately under `generated_at_runtime`.
- **Two spec-vs-implementation gaps verified by reading `apps/ceo/extensions/ceo-and-board.ts`:** (1) `converse` fires board members in parallel (`Promise.allSettled`) despite `ceo.md` saying "sequential"; (2) `end_deliberation` collects final statements in config order (Contrarian 4th), despite README/prompts claiming "Contrarian speaks last (enforced)."
- Models verified in source: CEO `anthropic/claude-opus-4-6`, board default `anthropic/claude-sonnet-4-6`; multimodel variant models verified in `agents-multimodel/*.md`.
- Transcript garbles corrected against the codebase (NutraHoldings, Sonnet, BlendStack, justfile, ElevenLabs, Pi, Agentic Horizon…). Video duration 2403s / 40:03 and 4K/AV1 confirmed via ffprobe.
- YT overlays: exactly **1** `include_in_phase1: true` (within the 1–3 limit); it is the Pi-vs-Claude-Code video Dan names on-screen, with `video_id: null` pending verification.

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- **Model version strings are period detail** (Opus/Sonnet 4.6 era). Do not present as latest; the book baseline is newer (Opus 4.8 / Sonnet 5).
- **Teach the two v1 gaps as "docs say X, code does Y"** and re-check against the shipping code at publish time — a later harness version may implement sequential rounds or true Contrarian-last ordering.
- **YT overlay IDs are unverified** (only the lesson's own `TqjmTZRL31E` is confirmed). Source and content-check any overlay from the IndyDevDan channel before publishing links. Do not fabricate IDs.
- **Codebase is member-exclusive** — the lab and chapter must frame it as "inside the course codebase," not a public clone.
- Clean SVG sources exist in `codebase/images/main/` (architecture, deliberation flow, YAML anatomy, brief→memo anatomy) as crisp alternatives to the composited video frame `t1672`.
- Out of scope (untouched, per brief): full chapter HTML, PiCanvas, YT video downloads.

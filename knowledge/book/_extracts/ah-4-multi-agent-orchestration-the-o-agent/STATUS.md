# STATUS: DONE ✅

**AH-4 "Multi-Agent Orchestration: The O-Agent"** technical-accuracy extract — completed by Claude (technical accuracy expert), 2026-07-13.
Role: extract only. The full HTML chapter (vol-2-ah / `12-multi-agent-orchestration-the-o-agent`) is Codex's next step and is intentionally NOT produced here.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — mirrors the tac-1/ah-3 gold schema, adapted: tactic, mission, scale_framework, three_pillars, 18 core_concepts, core_four_at_scale, sdk_mechanics, system_architecture, management_tools (8, with CRUD), agent_templates (7), workflow_commands, piter_outloop, step_by_step_demo, 26 quotes, retrieval, codebase_map, 6 current_practice_gaps, yt_overlay_candidates, 11-frame frame_plan | ✅ valid JSON, 32 top-level keys |
| `extract.md` | Master teaching notes — 11 major ideas each as Hook → Picture → Worked example → Name → Failure → Retrieval; the fleet-at-a-glance tables (8 tools + 7 templates); VTT-verified timeline map; glossary + transcript-artifact key; cross-references | ✅ |
| `nuggets.md` | 18 ranked nuggets in 3 tiers (paradigm → machinery → judgment) + 8-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 7 course-era→2026 items with book treatments (the SDK is ALREADY current here — the AH-3 rename correction does NOT apply); "what hasn't aged"; strict YouTube-overlay decision | ✅ |
| `frame-plan.json` | 11 frames with VTT anchors, `why_for_weak_student`, `verified_visual` notes; 3 documented alternates; 3 unframed-beats-by-design (diagram_instead) | ✅ valid JSON, all 11 files on disk |
| `lab-spec.md` | 8-part progressive lab (course codebase only) — real-infra setup → read the O-agent core four → run the fleet → observability drill → CRUD → ecosystem+templates → the ADW workflow → judgment; gradable checkpoints + 8 pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Frames (critical-quality deliverable)

11 frames, **all native 1920×1080**, extracted with `ffmpeg -ss <t> -i <mp4> -frames:v 1 -q:v 2`, saved to
`book/media/frames/ah-4-multi-agent-orchestration-the-o-agent/`:

`t0258-three-pillars-empty-shell` · `t0300-command-k-capability-palette` · `t0402-populated-observability-3-agents` · `t0528-the-core-four` · `t0636-architecture-mermaid` · `t0690-produced-consumed-assets` · `t1143-crud-delete-all-agents` · `t1445-ecosystem-interop-slash-commands` · `t2148-sleep-check-agent-status` · `t2625-plan-build-review-workflow` · `t3215-reviewer-verify-finale`

Every frame was **visually inspected this session** (not just extracted): terminal/UI/architecture/code beats only, no talking heads, text sharp at full res. ~25 candidates (16 initial + 7 refinement + 2 verification) were extracted and culled to these 11; the `_cand` working folder was removed. The lesson is a single continuous screen recording of a custom dark-theme observability web app (`MULTI-AGENT ORCHESTRATION`, `127.0.0.1:5175`), so every kept frame is UI/code-dense.

## Verification performed

- `extract.json` and `frame-plan.json` both parse via `python3 json.load` (32 / 13 top-level keys).
- Frame count matches (11 on disk == 11 in `frame-plan.json` == 11 in `extract.json` `frame_plan`); every plan `file` path confirmed present on disk (book-relative `media/frames/…`); all confirmed **1920×1080** via ffprobe.
- **Codebase mapping** cross-verified by TWO parallel subagents (backend/DB/architecture + agentic-layer/frontend) plus my own direct reads of the orchestrator system prompt and both `CLAUDE.md` files. Spot-checked 23 mapped paths on disk — **all present** (backend modules, frontend store/components, `.claude/agents` + `.claude/commands` + `.claude/skills`, `orchestrator_db` migrations, both `.claude` layers).
- **SDK naming verified directly:** `backend/pyproject.toml` depends on `claude-agent-sdk`; every import is `from claude_agent_sdk import … ClaudeAgentOptions / ClaudeSDKClient`; **zero** legacy `claude_code_sdk`. Unlike AH-3, Dan also SAYS "Claude Agent SDK" on camera — so **no SDK-rename correction is needed for this chapter.**
- **Model IDs read from source (`config.py`):** `DEFAULT_MODEL = claude-sonnet-4-5-20250929`, `FAST_MODEL = claude-haiku-4-5-20251001`, meta-agent template = Opus; on-screen badges (frames t0402/t0528/t0636/t2625) confirm **SONNET-4.5 / HAIKU-4.5**. Flagged the internal inconsistency: the orchestrator system prompt still documents `haiku → claude-3-5-haiku-20241022` (stale) while the code resolves to Haiku 4.5.
- **The 8 management tools triple-verified:** palette frame `t0300` + orchestrator system prompt (read verbatim) + `agent_manager.py` `@tool` defs all agree; mermaid frame `t0636` labels them "Agent Manager — 8 Management Tools."
- **Sleep-check confirmed PROMPT-driven, not Python:** `orch_scout_and_build.md` / `orch_plan_w_scouts_build_review.md` set `SLEEP_INTERVAL: 15 seconds` + `Bash(sleep)` + `check_agent_status`; frame `t3215` shows a literal `Bash{command:"sleep 20"}`.
- Quotes/timestamps cross-checked against the 2602-cue VTT via a parser; anchor timestamps machine-verified (3:40, 4:01, 6:15, 8:42, 10:17, 11:28, 18:57, 19:46, 20:35, 21:28, 22:08, 22:22, 28:37, 32:12, 48:40, 54:39, 55:35, 56:02). Video 3368.5s / 1920×1080 / 15fps confirmed via ffprobe + `metadata/validation.json` (PASS).
- YT overlays: exactly **2** `include_in_phase1: true` (`fop_yxV-mPo`, `6fCqj4xFCZI`) — within the 1–3 limit; all flagged `verify_before_publish`.

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- **Do NOT lead with an SDK rename.** This is the key difference from AH-3: the repo is already on `claude-agent-sdk` / `ClaudeAgentOptions` and Dan says the current name. Add a one-line reassurance instead ("the SDK names here are current"), and use the current names in all book code samples.
- **Lead with the paradigm, not the app.** Dan is emphatic this is a bespoke reference implementation, not a product ("I don't care what user interface you use"). Teach the transferable pattern — **single interface + CRUD-for-agents + observability + out-loop** — and frame the Vue/FastAPI/Postgres app as a system to learn from.
- **Render three beats as designed graphics** (`diagram_instead` in frame-plan): the **scale ladder** (Base→Better→More→Custom→Orchestrated), the **PITER** out-loop pipeline (map it onto POST /send_chat → FastAPI+asyncio → cwd → WebSocket/DB), and a clean **three-pillar** figure. `t0258` proves the pillars on the real UI; a redrawn figure reads better in print.
- **Fix the transcription artifact in the chapter:** the auto-VTT writes **"Peter"** for **PITER** (Prompt input → Trigger → Environment → Review). It is a lesson concept, **not** a string in the repo; the loot-box notes spell it out. Do the same in the chapter.
- **Model IDs are period detail** — keep as quoted code, teach the selection principle (Haiku/fast for scouts+summaries, Sonnet for primary/build/review, Opus for the meta-agent). Footnote the system-prompt's stale `claude-3-5-haiku-20241022` doc line so a careful reader trusts the code + the 4.5 on-screen badges.
- **Ports: use 9403 (backend) / 5175 (frontend).** The inner `apps/orchestrator_3_stream/CLAUDE.md` says "8002" — it's stale (README + `.env` + `start_be.sh` + the frontend all use 9403). Also flag `modules/hooks.py` as legacy/orphan so no one studies the wrong file.
- **The lesson names its own biggest gap** — no deterministic AI Developer Workflows yet ("this is the big missing piece… upcoming Agentic Horizon lessons"). Present the O-agent as the intermediate step you use WHILE building an agentic layer; ADW integration is forward-looking.
- **The sleep-check is prompt-driven glue** — surface it as a teaching nuance (Bash sleep + check_agent_status in the workflow command), not hidden machinery, so a reader could rebuild it.
- **YT overlay IDs** (`fop_yxV-mPo` Codebase Singularity; `6fCqj4xFCZI` How Claude Code Changed Engineering) are carried from the tac-1 seed list and were NOT fetched — verify each resolves and re-check titles before shipping links. `X2ciJedw2vU` (Agent Skills) is listed for the volume map only (phase1=false).
- **3 alternate frames** (`t0419` TodoWrite/"three times the compute", `t1630` scout-template typed command, `t0168` KPIs title-card B-roll) are documented in `frame-plan.json` if the chapter wants a second beat — not on disk, re-extractable from the listed timestamps.
- Do NOT rebuild scaffold (design/, data/, index.html, media besides these 11 frames). Only the vol-2-ah chapter HTML body remains out of scope for this extract pass.

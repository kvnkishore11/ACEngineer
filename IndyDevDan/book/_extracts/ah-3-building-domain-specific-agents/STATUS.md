# STATUS: DONE ✅

**AH-3 "Building Domain-Specific Agents"** technical-accuracy extract — completed by Claude Fable (technical accuracy expert), 2026-07-13.
Role: extract only. The full HTML chapter (vol-2-ah / `11-building-domain-specific-agents`) is Codex's next step and is intentionally NOT produced here.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — mirrors the tac-1 gold schema, adapted: tactic, mission, progression_model, 16 core_concepts, core_four_control, sdk_mechanics, the_eight_agents (full per-agent spec), step_by_step_demo, 18 quotes, retrieval, lab-relevant fields, codebase_map, 6 current_practice_gaps, yt_overlay_candidates, 12-frame frame_plan | ✅ valid JSON, 27 top-level keys |
| `extract.md` | Master teaching notes — 9 major ideas each as Hook → Picture → Worked example → Name → Failure → Retrieval; the 8-agent ladder table; VTT-verified timeline map; glossary + transcript-artifact key; cross-references | ✅ |
| `nuggets.md` | 17 ranked nuggets in 3 tiers (non-negotiable → SDK machinery → judgment) + 8-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 6 course-era→2026 gaps with book treatments (SDK rename is #1), "what hasn't aged," strict YouTube-overlay decision | ✅ |
| `frame-plan.json` | 12 frames with VTT anchors, why_for_weak_student, verified_visual notes, 3 documented alternates, unframed-beats-by-design | ✅ valid JSON, all 12 files on disk |
| `lab-spec.md` | 7-part progressive lab (course codebase only) — read-the-core-four → run the ladder → the context experiment → hooks → UI agents → judgment → stretch; gradable checkpoints + 7 pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Frames (critical-quality deliverable)

12 frames, **all native 1920×1080**, extracted with `ffmpeg -ss <t> -i <mp4> -frames:v 1 -q:v 2`, saved to
`book/media/frames/ah-3-building-domain-specific-agents/`:

`t0018-the-agentic-path` · `t0225-pong-run-session-stats` · `t0300-pong-system-prompt` · `t0565-echo-mcp-server-model` · `t1040-calc-disallowed-tools` · `t1360-social-hype-stream` · `t1852-consistent-codebase-architecture` · `t2170-qa-hook-block-env` · `t2265-tri-copy-writer-ui` · `t2565-micro-sdlc-kanban-board` · `t2825-planner-write-hook` · `t3060-ultra-stream-dual-panel`

Every frame was **visually inspected this session** (not just extracted): terminal/UI/code beats only, no talking heads, text sharp at full res. ~18 initial + 8 targeted candidates were extracted and culled to these 12; the `_cand` working folder was removed.

## Verification performed

- `extract.json` and `frame-plan.json` both parse via `python3 json.load`.
- Frame count matches (12 on disk == 12 in plan); every plan `file` path confirmed present on disk; all confirmed 1920×1080 via ffprobe.
- **Codebase mapping:** every *taught* source file across all 8 agents is mapped in `extract.json` (`the_eight_agents[].key_files` + `codebase_map`). Cross-check found only 3 unmapped files, all non-taught scaffolding: `custom_4_social_hype_agent/modules/__init__.py` (package init) and `custom_7_micro_sdlc_agent/test_concurrent.py` + `test_websocket.py` (WebSocket load-test helpers Dan never references). Root docs/configs (README, CLAUDE.md, .env.sample, all 4 `.mcp.json.*` samples, `ai_docs/README.md`, outer `.claude/`) are mapped; runtime artifacts (SQLite DBs, `specs/`, `reviews/`, `social_hype_results.csv`) are documented separately as generated-not-committed.
- **SDK naming verified directly:** all `pyproject.toml` depend on `claude-agent-sdk`; all `.py` import `claude_agent_sdk` / `ClaudeAgentOptions`; frames `t0565`/`t1040` still show `ClaudeCodeOptions` on screen — the genuine recorded-vs-current delta, and the migration guide is linked in `ai_docs/README.md`.
- **Model IDs read from source:** `claude-sonnet-4-20250514` (23 refs), `claude-opus-4-1-20250805` (agent-7 `AVAILABLE_MODELS`), `claude-3-5-haiku-20241022` (echo).
- Quotes/timestamps cross-checked against the 3407-cue VTT; anchor timestamps verified (0:07, 0:47, 0:56, 5:03, 19:42, 27:38, 31:33, 36:06, 49:57, 55:33, 1:06:52, 1:07:04). Video duration 4029.9s and 1920×1080 confirmed via ffprobe.
- YT overlays: exactly **2** `include_in_phase1: true` (`6fCqj4xFCZI`, `X2ciJedw2vU`) — within the 1–3 limit; both flagged `verify_before_publish`.

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- **Lead with the SDK rename.** The chapter's single most important correction: Dan says "Claude Code SDK" / on-screen `ClaudeCodeOptions`, but it's the **Claude Agent SDK** (`claude-agent-sdk` / `ClaudeAgentOptions`) — the repo is already updated. Use the new names in all book code samples; footnote the two frames that show the old name.
- **Render two beats as designed graphics, not frames** (`diagram_instead` / unframed_beats): the "when to build custom vs use out-of-the-box" decision framework (narrated over B-roll — build a two-column decision box from the transcript lists) and the `read_stream_file` chunked-read (show as a small annotated code excerpt: `sed` subprocess + `raw_log_cache` + `clear_context`).
- **Model IDs are period detail** — keep as quoted code, teach the selection principle (Haiku/Sonnet/Opus by task), don't hardcode an ID as a takeaway.
- **YT overlay IDs** carried from the tac-1 seed list; both map to this lesson's named gaps but were not fetched — verify each resolves and re-check titles before shipping links.
- Do NOT rebuild scaffold (design/, data/, index.html, media besides these frames). Only the vol-2-ah chapter HTML body remains out of scope for this extract pass.
- 3 alternate frames (`t0700` echo tool-list, `t2690` sdlc "1 workflow running", `t3130` ultra-stream notify-support) are documented in `frame-plan.json` if the chapter wants a second beat for an agent — not on disk, re-extractable from the listed timestamps.

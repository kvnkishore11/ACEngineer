# STATUS — `ma-2-lead-agents` extract

**Status: DONE** ✅
**Role:** technical accuracy expert (extract only — no chapter HTML, per brief).
**Lesson:** Multi-Team Agentic Coding / Lead Agents · MA · order 16 · vol-3-ma · chapter stem `16-lead-agents`.
**Date:** 2026-07-13.

## Deliverables (all under `book/_extracts/ma-2-lead-agents/`)
| File | Purpose | Size |
|---|---|---|
| `extract.json` | Master structured extract (tac-1 schema, adapted). 33 keys, 13 core_concepts, 29 quotes, 14 retrieval Qs, full codebase_map, 5 current-practice gaps, 4 YT overlays. | ~9.4k words |
| `extract.md` | Narrative companion with the weak-student teaching scaffold (Hook→Picture→Worked example→Name→Failure→Retrieval) for 10 ideas + architecture + harness internals. | ~3.0k words |
| `nuggets.md` | 35 distilled, quotable insights (thesis, architecture, domain/safety, memory, skills/config, mindset, under-the-hood). | ~1.2k words |
| `outdated-vs-current.md` | Version drift: (A) recording-vs-shipped (4 items) and (B) ecosystem drift (5 items) + what is timeless + overlay pointers. | ~1.3k words |
| `frame-plan.json` | 11 frames with t_seconds, label, file, format, resolution, concept, transcript_anchor, why_for_weak_student + 4 frames-considered-but-cut. | ~1.2k words |
| `lab-spec.md` | Gradable lab (course codebase only): Setup + CP0–CP5 + S1–S7 stretch + final pass sheet + troubleshooting table. | ~1.6k words |
| `STATUS.md` | This file. | — |

## Frames — 11, full 4K (3840×2160), verified on disk
Location: `book/media/frames/ma-2-lead-agents/` (~21 MB total).

| Frame | Fmt | Concept |
|---|---|---|
| `t0118-ping-orchestrator-leads-cost.jpg` | jpg | chat-room single interface (ping-pong + cost footer) |
| `t0185-lead-domain-block-delegate.jpg` | jpg | three-tier cascade (lead blocked ✗ → delegates) |
| `t0232-toggle-workers-team-tree.jpg` | jpg | 10-agent tree + per-agent cost + opus/sonnet tiering |
| `t0337-classifier-predict-route.png` | png | the demo problem (`just predict` → MID → sonnet) |
| `t0408-ask-all-teams-fanout.jpg` | jpg | multi-perspective (same prompt to 3 teams) |
| `t0768-orchestrator-agent-config.png` | png | agent anatomy (model/expertise/skills/tools/domain) |
| `t0955-validation-security-review.jpg` | jpg | validation team autonomy ("ship it") |
| `t1180-active-listener-10-files.png` | png | skills composition (10 results in 10 files) |
| `t1290-frontend-domain-lock.png` | png | domain locking (frontend scoped to apps/frontend/) |
| `t1420-conversation-jsonl-log.png` | png | conversation awareness (session log + workspace) |
| `t1610-head-to-head-cost-tiering.jpg` | jpg | payoff + $8.28 total + model tiering |

Zero talking-head frames (all terminal/UI/code, per brief). 5 PNG for small-text IDE frames, 6 JPEG (q2) for larger-text chat frames.

## Verification performed
- ✅ `extract.json` and `frame-plan.json` parse as valid JSON (python `json.load`).
- ✅ `frame-plan.json` frame list == `extract.json` `frame_plan` list (11 == 11).
- ✅ All 11 referenced frame files exist on disk; 11 files on disk, none extra, none missing.
- ✅ Every real codebase file mapped in `codebase_map` (root, `.pi/multi-team/` agents/skills/expertise/configs, `apps/multi-team-chat/extensions/*` + modules with exact line counts, `.claude/` commands/agents/skills, images, specs, ai_docs).
- ✅ Agent model/tool/skill/domain matrix read directly from all 10 shipped `agents/*.md` frontmatter; extension internals read in full (multi-team-chat.ts 1432, lead-delegate.ts 197, domain-enforcer.ts 190, tilldone-lead.ts 123, config.ts 446, subprocess.ts 157, etc.), corroborated by both `specs/`.
- ✅ Quotes cross-checked against `transcript/ma-2-lead-agents.md`; transcript mishearings documented (Pi/pie, Sonic=Sonnet, contacts=context, "Claude man and B"=ComplementNB).
- ✅ YT overlay IDs sourced from the lesson's own description (`f8cfH5XX-XU`, `TqjmTZRL31E`) + metadata (`M30gp1315Y4`); flagged for oembed verification.

## Key accuracy flags surfaced (see `outdated-vs-current.md` + `extract.json`.confidence_notes)
1. **Recording predates TillDone** — on-screen `orchestrator.md` (frame t0768) lacks `tilldone`/`write`/`edit`; shipped file has them. Teach from shipped files.
2. **Front/back domain split is a live demo edit** — shipped `frontend-dev.md` == `backend-dev.md` (`apps/` r+u+delete); the `apps/frontend/` scoping (frame t1290) is Dan editing live.
3. **All 10 expertise files ship EMPTY** (0 lines); the on-screen 5k-token backend model was from a previous codebase.
4. **Roster = 3 teams / 10 agents** — Dan's description says "2 teams" in one line; the footer shows 10 rows. Code is authoritative.
5. **Classifier codebase NOT shipped** — lab exercises the tool against its own source repo (README Step 2).
6. **Two orchestration layers** — Pi runtime (`delegate`/`tilldone`) ≠ Claude Code build harness (`Task*` in `plan-w-team.md`/specs). Don't conflate.
7. **Course-era models** (`claude-opus-4-6` / `claude-sonnet-4-6`) — update ids at publish; keep the tiering principle.

## Handoff notes for the chapter author (Codex)
- Spine the chapter on Dan's **6 pillars** (`extract.json`.six_pillars). Every core_concept maps to one.
- Lead with the **ping → domain-block → toggle-workers** arc (frames t0118 → t0185 → t0232) — it teaches the whole architecture in three screenshots.
- Use the **soft-vs-hard enforcement** framing (skill vs domain-enforcer) as the pedagogical core of domain locking; it's the most-missed nuance.
- Honor the honest-simplification discipline: when you show frame t0768 or t1290, flag the recording-vs-shipped drift in adjacent prose.
- Overlay cap: state it in-page. Only 2 phase-1 overlays, both real IDs from the lesson description.

## Out of scope (per brief) — not done
- Full HTML chapter (Codex next).
- PiCanvas.
- Downloading full YouTube videos (overlay IDs listed for verification, not fetched).

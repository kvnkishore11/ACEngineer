# STATUS: DONE ✅

`ma-3-ui-agents` "Infinite UI Agents" extract — completed by the technical-accuracy expert (Claude, max reasoning), 2026-07-13.
Full deliverable set produced under `_extracts/ma-3-ui-agents/` + 11 full-4K frames under `media/frames/ma-3-ui-agents/`. Mirrors the TAC-1 gold template schema, adapted to this lesson, and honors the vol-1 fan-out checklist.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — 32 top-level keys; tactic, mission, levels model, harness definition, 14 core concepts, core-four-in-harness, infinite-ui-system, multi-team architecture, 21-step timestamped demo, 25 quotes, retrieval, codebase_map (+ committed-vs-demo discrepancies), current-practice gaps, 2 phase-1 YT overlays, frame_plan, 11 confidence notes | ✅ valid JSON |
| `extract.md` | Master teaching notes — 9 major ideas each Hook → Picture → Worked example → Dan's term → Failure → Retrieval; the Infinite UI system mapped to the repo; VTT-verified timeline; glossary (+ transcript mishearings); an **Accuracy Ledger** (what ships vs what's on screen) | ✅ |
| `nuggets.md` | 16 ranked nuggets in 3 tiers for weak learners + 7-question micro-quiz with hidden answers | ✅ |
| `outdated-vs-current.md` | 5 gaps (committed-vs-demo, model drift, tool convergence, till-done, preview mechanism) with book treatments; what hasn't aged; strict overlay decision (2 phase-1) | ✅ |
| `frame-plan.json` | 11 real frames + 1 diagram_instead, each with `why_for_weak_student`, timestamp, format; unframed-beats rationale; extraction policy | ✅ valid JSON, all files on disk |
| `lab-spec.md` | 5-part lab (course codebase only): Track A read-the-harness (no API cost, fully gradable) + Track B run/specialize (members); checkpoints + explicit pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Verification performed

- `extract.json` and `frame-plan.json` parse via `python3 json.load` — both VALID. extract.json = 32 keys, 14 core_concepts, 25 quotes, 14 retrieval_questions, 12 frame_plan entries (11 frames + 1 diagram), 2 `include_in_phase1` overlays.
- **All 11 frame files exist on disk**, full native **3840×2160** (verified via ffprobe), non-blank (PNG 2.3–4.4 MB for text-heavy terminal/code, JPEG 196–556 KB for UI/hero). frame-plan.json ↔ disk and extract.json.frame_plan ↔ disk both cross-checked: **0 missing**. Every frame was visually inspected during selection.
- **Codebase fully mapped** from primary sources (read directly) + 4 parallel explorer agents, cross-checked: `.pi/settings.json`, `multi-team-config.yaml`, all 12 `agents/*.md`, all 12 `expertise/*.yaml` (confirmed 1-line stubs), all 7 `skills/*.md`, all 10 `prompts/multi-team/*.md`, `README.md`, `CLAUDE.md`, `justfile`, `scripts/list.py`, the full `apps/infinite-ui/` Vue app, and all 6 `specs/*.md`. `codebase_map` covers every committed file group.
- **Counts verified on disk:** 8 teams / 12 unique agent files / 24 slots; 1 brand (aegis) + _template; 3 products; 7 real trees; 25 `index.vue` (23 real + 2 template). `timeline-stack` = 899 lines (matches Dan's on-screen "899-line SFC" exactly); `glassmorphism-panel` = 972 (Dan said 967 — minor drift).
- **Model IDs verified from the frame itself** (t0352), not memory: `stepfun/step-3.5-flash`, `openrouter/minimax/minimax-m2.7`, `anthropic/claude-sonnet-4-6`.
- **Committed-vs-demo discrepancies confirmed on disk:** no `agents-os/`, no `multi-team-config-min.yaml`, all agents Sonnet, all mental models stubs, one brand — single commit `7d36778`. Documented in `extract.json` and the `extract.md` Accuracy Ledger.
- Quotes/timestamps cross-checked against the transcript (`ma-3-ui-agents.md`); video duration 1946 s and 4K/AV1/29.97fps confirmed via ffprobe; official chapter markers taken from the metadata description.
- Wrote **only** under `book/` (`_extracts/ma-3-ui-agents/` + `media/frames/ma-3-ui-agents/`). Course source trees were read only, never modified. No full chapter HTML written (Codex's job). PiCanvas untouched; no YouTube videos downloaded.

## Blockers

None.

## Caveats for the next stage (GPT/Codex chapter build)

- **Honesty obligation is the #1 requirement here.** This lesson is a live showcase whose on-screen system is a hand-tuned superset of the committed asset. Carry the **Accuracy Ledger** (extract.md) as a boxed sidebar and, wherever the chapter cites an on-screen model ID / mental-model size / brand count / preview mechanism, state the committed value in adjacent prose. Do not describe the demo as what a reader clones.
- **Correct two on-camera imprecisions in prose:** leaf previews are `<iframe>` + `import.meta.glob` (not Vue Teleport); `/generate` has no built-in till-done list (it's the orchestrator's `tilldone` tool). Both are teaching beats, not gotchas.
- **Don't over-assert Dan's "15 unique / 9 min" agent counts** — they come from his live config. Use the committed 12 files / 24 slots / 8 teams as ground truth and present his numbers as live-demo narration.
- **Model IDs and the "Mythos model" are April-2026 specifics** — teach the durable "per-agent, swappable model control" point and date the IDs; re-verify at publish.
- **YT overlay IDs** (`M30gp1315Y4` Agent Teams, `TqjmTZRL31E` Pi CEO Agents) are from the lesson's own description reference list — **oembed-verify they resolve before publishing links** (as TAC-1's cross-review did). Cap honored: exactly 2 phase-1.
- **Frame `harness-six-components` is `diagram_instead: true`** — render the six components (deterministic code, token caching, agent orchestration, prompts, skills, model control) as a designed labeled diagram; the video moment is a B-roll title card, not a usable frame.
- **Chapter stem** `17-ui-agents` under `vol-3-ma/`; update `data/curriculum.json` (`status`, `chapter_html`) and the hub when the chapter lands (report-only scope here — not touched).

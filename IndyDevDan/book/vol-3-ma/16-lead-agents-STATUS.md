# STATUS — MA-2 Multi-Team Agentic Coding / Lead Agents

**Lesson key:** `ma-2-lead-agents`  
**Course / order:** MA / 16  
**Output:** `vol-3-ma/16-lead-agents.html`  
**Status:** READY FOR CLAUDE REVIEW  
**Date:** 2026-07-13

## Deliverables

| File | Result |
|---|---|
| `vol-3-ma/16-lead-agents.html` | Complete teaching chapter, graded lab, cumulative mastery, glossary, sticky navigation, progress UI |
| `vol-3-ma/16-lead-agents.assets.css` | Lesson-specific light-theme diagrams and responsive/print rules; imports the gold TAC-1 chapter CSS |
| `index.html` | Chapter 16 linked and marked complete; current hub state reflects the concurrently completed corpus at 18/18 and Volume III at 4/4 |
| `vol-3-ma/16-lead-agents-STATUS.md` | This review handoff |

## Density and pedagogy

- Approximate prose words (HTML/script/tags stripped): **13,748**.
- Print-equivalent text estimate: **39–46 pages** at roughly 300–350 words per page, before treating full-width frames as additional page area.
- Major teaching cycles: **9**.
- Every cycle contains all required moves: **Hook → Picture → Story/frame → Name → Worked example → You try → Fail/fix → Current Practice → Retrieval (`details`) → Teach-back**.
- Retrieval panels: **44 `<details>` elements** including the mobile contents panel.
- Cumulative mastery: 16 questions, scoring bands, seven-part capstone teach-back.
- Graded lab: 100-point rubric; critical passes for block/delegate, roster reconfiguration, hard domain block, and conversation-log audit.
- Lab scope is limited to the shipped course repository: `agentic-horizon-extras/lead-agents`.

## Frame coverage

All 11 unique extract frames are covered, full width, with timestamped captions and 3840×2160 source dimensions. Two frames are deliberately reused for a second teaching claim, producing 13 frame placements:

1. `t0118-ping-orchestrator-leads-cost.jpg` — single interface and lead fan-out.
2. `t0185-lead-domain-block-delegate.jpg` — blocked lead routes to worker.
3. `t0232-toggle-workers-team-tree.jpg` — ten-agent roster, models, and costs; reused in configuration to prove the roster materialized into runtime seats.
4. `t1290-frontend-domain-lock.png` — live frontend/backend domain-split pattern, explicitly labeled as recording-vs-shipped drift.
5. `t1420-conversation-jsonl-log.png` — conversation, session, and artifact storage layers; reused in runtime to evidence persistent subprocess state.
6. `t0768-orchestrator-agent-config.png` — agent anatomy, explicitly labeled as pre-TillDone recording state.
7. `t1180-active-listener-10-files.png` — fleet-wide skill composition.
8. `t0337-classifier-predict-route.png` — separate demo problem, explicitly excluded from the lab.
9. `t1610-head-to-head-cost-tiering.jpg` — delivered classifier evidence beside recorded cost.
10. `t0408-ask-all-teams-fanout.jpg` — consistent three-team perspective fan-out.
11. `t0955-validation-security-review.jpg` — independent validation evidence.

CSS pins teaching images to `width: 100%`, `max-width: min(100%, 1100px)`, `aspect-ratio: 16/9`, and `object-fit: contain`; no thumbnail grid is used for course frames.

## Accuracy decisions

- Shipped default is taught as **3 teams / 10 agents**, not the inconsistent “2 teams” description line.
- Coordination/application execution is stated carefully: Orchestrator and leads may update permitted expertise, while workers own application-code execution and bash.
- The video’s `apps/frontend/` lock is taught as a live hardening pattern; the checked-in Frontend/Backend worker domains remain broader.
- Per-path enforcement is attributed to ordinary file tools. Bash mutation checks are explicitly taught as coarse heuristics—not target-path authorization or a sandbox—and the graded hard-boundary proof requires a blocked `write`/`edit` call.
- All 10 checked-in expertise files are described as empty by design.
- Pi runtime (`delegate` / `tilldone` / Pi subprocesses) is separated from the Claude Code install/build harness.
- Course-era model IDs remain period detail. The transferable tiering and config-override principles are emphasized without inventing replacement IDs.
- Sequential plan → engineer → validate remains the demonstrated default; parallel-safe fan-out is labeled as roadmap/current-practice nuance.
- The classifier benchmark is described only from the extract and is explicitly not presented as a shipped lab asset.

## Verification completed

- Extract gate `book/_extracts/ma-2-lead-agents/STATUS.md` existed before work began.
- HTML tag stack balances with no unclosed or mismatched explicit tags.
- All 53 chapter `href`/`src` references were checked; all 22 local file references and 29 internal anchors resolve.
- No duplicate IDs.
- Lesson CSS import resolves to the gold TAC-1 asset CSS.
- All 13 frame placements resolve to 11 unique extract files at native 4K resolution.
- All named course-repo lab files and recipes were checked against the shipped codebase.
- Pedagogy class counts are 9 each for `hook`, `picture`, `story`, `name`, `example`, `try`, `fail`, `current`, `check`, and `teach`.
- Current-practice YouTube count is **2**, within the ≤3 cap.
- Hub link, 18/18 progress fraction/percentage, and Volume III 4/4 completion state were checked after the concurrent chapter fan-out completed.
- The in-app browser connection and local headless Chrome were both attempted; sandbox/runtime failures prevented rendered screenshots or PDF output.

## Open questions for Claude review

1. **Rendered QA:** inspect desktop (~1440 px), mobile (~390 px), and print. Pay special attention to the long title, five-column hero system, tier tables, rubric table, and imported sticky rail. The static responsive rules collapse these layouts, but this environment could not render them.
2. **YouTube verification:** independently oEmbed-check `f8cfH5XX-XU` (“Pi vs Claude Code”) and `TqjmTZRL31E` (“CEO Agents”). The IDs/titles are supplied by the lesson extract; `yt-dlp` was unavailable and direct fetch/search could not verify them in this environment.
3. **Publish-time models:** decide whether the publication pass should replace the checked-in course-era model IDs with then-available equivalents. This chapter keeps the source strings and explicitly teaches the tiering principle to avoid inventing current IDs.
4. **Print density:** confirm that full-width frames do not push the rendered chapter beyond the desired 35–55 print-equivalent range. The word-based estimate is 39–46 pages; visual figures may change physical pagination.

## Suggested review route

1. Hero → orientation → six pillars.
2. Sections 01–03 for the ping → blocked lead → domain-lock teaching arc.
3. Sections 04–06 for memory, skills, and configuration truth.
4. Sections 07–09 for cost, trust, and source-level runtime.
5. Lab critical-pass checkpoints and restoration language.
6. Mobile/print render, then hub navigation.

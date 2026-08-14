# STATUS: DONE ✅

TAC-3 "Success is Planned" extract — completed by Claude Fable (fan-out pass, 2026-07-12).
Full deliverable set produced per the fan-out brief, mirroring the tac-1 gold template and the 01-CROSS-REVIEW-CLAUDE fan-out checklist.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — 28 top-level fields; mirrors tac-1 (24 shared fields) with 4 lesson-specific adaptations (phase_model/core_four/ai_vs_agentic/programmable_agent → scaling_ladder/templates_suite/fresh_agents_doctrine/programmatic_preview) | ✅ valid JSON, verified |
| `extract.md` | Master teaching notes — 10 ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q; VTT-verified timeline map; glossary; TAC bridge | ✅ |
| `nuggets.md` | 15 ranked nuggets in 3 tiers + 6-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 6 course-era→mid-2026 gaps with book treatments; not-aged list; strict overlay decision (2 include + 1 defer) | ✅ |
| `frame-plan.json` | 12 frames with VTT anchors, verified_visual notes, unframed-beats rationale | ✅ valid JSON, all files on disk |
| `lab-spec.md` | 5-part lab (setup + chore + bug + headless + 4 stretch drills), course codebase only, gradable checkpoints + pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

Frames: `book/media/frames/tac-3-success-is-planned/` — 12 files, all native 1920×1080 (source 15 fps), PNG for text-heavy shots, JPEG q=2 otherwise. **Every frame visually inspected this session**; 4 additional candidates extracted, inspected, rejected, and deleted (rationale in frame-plan.json notes).

## Verification performed

- `extract.json` + `frame-plan.json` parse via `python3 json.load`; frame lists in both files match disk 1:1 (filenames, labels, existence); all t_seconds ≤ 2792.
- `codebase_map` covers every file/dir on disk under `tac/tac-3` (8 command files, settings.json incl. deny list, 3 scripts, app client+server, ai_docs, adws/agents placeholders, specs/init, .env.sample, .gitignore, README); every mapped path existence-checked programmatically.
- Countable claims verified against artifacts: implement.md displays 12 lines (wc -l 11, no trailing newline — both documented); chore/bug/feature.md = 53/69/91 lines; **exactly 18 print( lines in server.py + 1 in main.py = 19** (the video agent's "20 across 2 files" prose is an off-by-one vs its own correct inventory — flagged in confidence_notes so the chapter quotes the inventory); 37 pre-existing test functions (video's "52 tests / 18 new" documented as run-specific narration); settings.json = 12 allow + 3 deny entries; sql_processor blocklist = 10 keywords; `DROP TABLE IF EXISTS {table_name}` f-string confirmed at server.py:243; specs/init_nlq_to_sql_to_table.md = 749 lines.
- Quotes cross-checked against the 9182-line VTT (~±5 s); video duration 2792 s / 1920×1080 / 15 fps confirmed via ffprobe.
- Exact on-screen artifacts captured verbatim from verified frames: the /chore prompt as typed, the full claude -p command (`--output-format stream-json --dangerously-skip-permissions --model opus --verbose > feature_plan_raw_agent_logs.jsonl`), the HOP slide definition, the JSONL model id `claude-opus-4-20250514`, generated plan filenames (replace-print-with-logging.md, fix-sql-injection-vulnerabilities.md, query-history-panel.md).
- YT overlays: exactly 2 `include_in_phase1: true` (X2ciJedw2vU, 6fCqj4xFCZI) + 1 deferred (fop_yxV-mPo) — within the 1–3 limit.

## Blockers

None.

## Caveats for the next stage (Codex chapter build)

- **No tac-3-specific YT seed list was provided**; the 3 overlay IDs are reused from tac-1's oembed-verified seed list where mapping is genuine. If the orchestrator supplies a dedicated planning/spec-prompting video, slot it ahead and re-verify IDs via oembed at review time (fan-out checklist item 5).
- Quote the /chore prompt from the screen (`...written standard out`, no "to"); quote the tactic definition from the loot box note (the t0200 slide body has a typo: "you your engineering workflows"). The HOP slide text is clean — quote verbatim.
- Do NOT propagate "20 print statements" or "52 tests" as codebase facts — both are run-specific video narration; on-disk truth is 19 prints / 37 tests (see confidence_notes).
- `current_practice_gaps` written against mid-2026 Claude Code (command frontmatter, Agent Skills, thinking controls, sandboxing/hooks/SDK, native plan mode, subagents) — re-verify at publish.
- Honest-simplification discipline (gold-template mandate): every abridged artifact quote in the chapter must flag its abridgement in adjacent prose; all four .claude/commands planning/execution files are short enough to quote in full — prefer that.
- Frames: no `diagram_instead` flags this lesson, but frame-plan's `unframed_beats_by_design` names three beats the chapter should render as designed elements (scaling ladder, fresh-agents/KPI panel, 8-tactic arc + closing pull-quote).
- `data/curriculum.json` not touched (report-only scope for extract passes) — update tac-3 `status`/`chapter_html` when the chapter lands (fan-out checklist item 11).

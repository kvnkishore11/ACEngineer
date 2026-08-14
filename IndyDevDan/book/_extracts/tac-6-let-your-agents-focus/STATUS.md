# STATUS: DONE ✅

TAC-6 "Let Your Agents Focus" extract — completed by Claude Opus (resume pass, 2026-07-12).
The prior session (Claude Fable, interrupted at its limit) produced `extract.json`, `extract.md`, `frame-plan.json`, and all 12 full-resolution frames. This resume pass produced the four missing deliverables — `nuggets.md`, `lab-spec.md`, `outdated-vs-current.md`, and this `STATUS.md` — and re-validated the machine artifacts. No frames were re-extracted and no HTML chapter was written (both out of scope for this pass).

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — tactic, mission, SDLC-question model, KPI model, 16 core concepts, review/patch/document pipelines, one-purpose agent mechanics, composed workflows, step-by-step demo, quotes, retrieval Qs, codebase_map, current_practice_gaps, YT overlays, embedded lab + frame_plan | ✅ valid JSON, schema-complete (537 lines) |
| `extract.md` | Master teaching notes — 10 major ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q; VTT-verified timeline map; Dan-ism glossary; bridge to rest of TAC | ✅ (prior pass) |
| `nuggets.md` | 15 ranked nuggets in 3 tiers for the struggling learner + 6-question micro-quiz | ✅ (this pass) |
| `lab-spec.md` | 6-part lab (setup → plan_build_review → review contract → patch loop → document/close-the-loop → stretch), course codebase only, checkpoints + pass criteria + instructor notes | ✅ (this pass) |
| `outdated-vs-current.md` | 7 course-era→2026 gaps with book treatments; what hasn't aged; strict phase-1 overlay decision | ✅ (this pass) |
| `frame-plan.json` | 12 frames mapped with VTT anchors + verified_visual; unframed-beats-by-design rationale | ✅ valid JSON, all files on disk |
| `STATUS.md` | this file | ✅ (this pass) |

## Frames (media/frames/tac-6-let-your-agents-focus/)

12 frames, all present and non-empty, native 1920×1080:
`t0152-sdlc-as-questions.jpg`, `t0278-tactic-one-agent-one-prompt-one-purpose.jpg`, `t0756-adws-workflow-files.png`, `t1012-composed-workflow-script.png`, `t1068-adw-state-json.png`, `t1305-review-prompt-and-types.png`, `t1912-review-screenshot-misplaced-export.png`, `t2135-playwright-mcp-vision-gap.png`, `t2190-patch-workflow-terminal.png`, `t2255-export-fixed-next-to-hide.png`, `t2742-conditional-docs-updated.png`, `t2815-bug-md-conditional-docs-loop.png`.

## Verification performed (this pass)

- `extract.json` and `frame-plan.json` both parse via `python3 json.load` — VALID. No empty critical fields found; every array/section is populated (the JSON already carries embedded `lab`, `current_practice_gaps`, and `yt_overlay_candidates` sections, which the three new markdown companions expand into pedagogical prose).
- `frame-plan.json` declares 12 frames; 12 files exist on disk; 0 zero-byte files.
- Every frame filename in `frame-plan.json` matches a file in `media/frames/tac-6-let-your-agents-focus/`.
- Companion files cross-checked against `extract.json`/`extract.md` for factual consistency: `MAX_REVIEW_RETRY_ATTEMPTS = 3`; severity Literal `skippable/tech_debt/blocker` (only blockers block + auto-resolve); `conditional_docs.md` ships with exactly 4 entries (5th added agentically); conditional docs read by bug/chore/feature/patch/prime and written by document; `slash_command=` → 14 hits in 4 files; adw_review/adw_document require the adw-id; Dan's 15-vs-14 (PR-vs-issue) stumble; `.claude/commands/e2e` path typo in review.md; classify_adw-vs-allowlist trigger drift.
- YT overlays: exactly 2 `include_in_phase1: true` (`X2ciJedw2vU`, `hGg3nWp7afg`) — within the 1–3 cap; `6fCqj4xFCZI` and `fop_yxV-mPo` deferred. Overlay decision table in `outdated-vs-current.md` matches `extract.json`.

## Blockers

None.

## Caveats for the next stage (chapter build)

- `current_practice_gaps` written against mid-2026 Claude Code (native subagents, Skills, context editing, vision-capable file reads, Claude 5-era models); re-check at publish — this axis moves fast.
- YT overlay IDs come from the orchestration seed pool (oembed-verified in the TAC-1 cross-review); verify each resolves and its content matches its title before publishing links — no video fetching was performed in this pass, per brief.
- Demo-run artifacts (issue #14, PR #15, adw_id `490eb6b5`, `patch-adw-490eb6b5-fix-download-button-position.md`, `feature-490eb6b5-one-click-table-exports.md`) are Dan's runtime values read from frames/transcript — they are NOT in the committed repo; students' values will differ. Render them as illustrative, not literal.
- Unframed-by-design beats (context-pollution monologue 4:55–11:20; the Agentic-Coding-KPIs recap slide at ~3:18; the closing KPI self-grade 54:55–56:10) should be rendered as designed elements/quotes per `frame-plan.json` `unframed_beats_by_design`, not as missing frames.
- Do NOT rebuild the extract artifacts or re-extract frames; only the vol-1-tac-6 chapter HTML body remains out of scope for extract passes.

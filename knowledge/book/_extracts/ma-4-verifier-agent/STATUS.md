# STATUS: DONE ✅

MA-4 "The Pi Verifier Agent" extract — completed this session (technical-accuracy pass).
Full `_extracts/ma-4-verifier-agent/` deliverable set produced from the transcript, metadata, all read codebase files under `the-verifier-agent-system`, and 12 freshly-extracted 4K frames. Mirrors the tac-1 gold schema throughout.

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — every tac-1 field adapted to ma-4 (tactic, mission, 12 core_concepts, both worked examples, report contract, three read-only layers, step_by_step_demo, 19 quotes, retrieval, lab, codebase_map, frame_plan, yt_overlay_candidates, current_practice_gaps) | ✅ valid JSON, schema-complete |
| `extract.md` | Master teaching notes — 9 major ideas, each Hook → Picture → Worked example → Dan's term → Failure mode → Retrieval Q; transcript-verified timeline map; glossary; bridge | ✅ |
| `nuggets.md` | 15 ranked nuggets in 3 tiers for weak learners + 7-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 6 recording-era→mid-2026 items (model drift, doc-vs-disk, harness portability, scope) with book treatments; what hasn't aged; strict overlay decision | ✅ |
| `frame-plan.json` | 12 frames mapped with t_seconds/timestamp/transcript_anchor/why_for_weak_student/format; unframed-beats rationale | ✅ valid JSON, all files on disk (bijective) |
| `lab-spec.md` | 6-part lab, course codebase only; planted-defect SQLite loop + image readability loop + 5 stretch drills; gradable checkpoints + pass criteria + instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Frames (media/frames/ma-4-verifier-agent/) — 12, native 3840×2160

| File | Beat |
|---|---|
| `t0080-two-agent-split-intro.jpg` | hook: builder + input-locked verifier side by side |
| `t0178-builder-gpt-image-skill.png` | Opus writing a gpt-image-2 prompt (one agent prompts another model) |
| `t0196-verifier-kicks-off-unprompted.jpg` | the "UNPROMPTED" auto-start moment |
| `t0246-verifier-prompts-builder.png` | verifier_prompt feedback loop (ack → builder re-runs) |
| `t0298-first-arch-diagram-overloaded.jpg` | text-dense diagram that fails the ≤10-block rule |
| `t0360-failed-report-readability.png` | FAIL report naming MAX_TEXT_ELEMENTS=10 + fix |
| `t0420-verified-report-7of7.png` | VERIFIED · PERFECT, 7/7 atomic claims |
| `t0478-clean-arch-diagram.jpg` | hero architecture diagram (passes readability) |
| `t0835-customized-system-prompt.png` | verify_image.md persona open in VS Code |
| `t1052-just-recipes-vsql-boot.png` | the `just` recipe list (pick your verifier) |
| `t1180-sqlite-verify-16-claims.png` | SQLite example: 2 agents, 16/16 atomic claims, token disparity |
| `t1200-bash-policy-lockdown.png` | verify_sqlite.md frontmatter: bash_policy + model |

## Verification performed

- `extract.json` and `frame-plan.json` both parse via `python3 json.load` (extract.json: 35 top-level keys, 12 core_concepts, 19 quotes, 12 frame_plan entries, 41 codebase files mapped).
- Frame plan is **bijective** with disk: all 12 `frame_plan[].file` paths exist, and no disk frame is unlisted (verified programmatically).
- Every frame was visually opened this session and its on-screen content checked against its label (not just filename-matched). Source is 100% screen-share → no talking-head frames; 3 frames carry Dan's produced overlay text (kept, reinforce the concept).
- `codebase_map` covers the real files read this session: README, justfile, both settings.json, all 4 personas (verifier/verify_sqlite/verify_image/verify_python), both scripts (verify_sqlite.py/verify_python.py), both prompts (verify_on_stop.md/builder_error.md), the 5 core TS files + verifiable-footer.ts + cross-agent.ts, the gpt-image-2 SKILL, prime.md + install.md. Runtime artifacts (arch.jpg, tmp/*.db, socket, breadcrumb, session JSONL) documented under generated_not_committed.
- Quotes cross-checked against the transcript; ASR errors corrected and listed (GLM/Pi/GPT Image/IndyDevDan/Kimi/Qwen). Video duration 1971s / native 3840×2160 confirmed via ffprobe.
- YT overlays: exactly 2 `include_in_phase1: true` (RairMJflUSA, V5A1IU8VVp4), both named by Dan in-lesson — within the 1–3 limit; the teased agentic-security video has no ID (not overlaid).

## Accuracy findings surfaced this pass (documented, not errors in our work)

1. **Model drift:** frame t1200 shows `verify_sqlite.md` with `model: z-ai/glm-5.1` (matching the video's GLM-5.1 SQLite verifier); the file on disk today declares `model: openai/gpt-5.5` (all four personas). Builder is Opus 4.7 throughout. The model is a one-line swap — period detail, documented in outdated-vs-current.md §1 and extract.json confidence_notes.
2. **README vs disk:** README's "Known limitations (v1)" says only SQLite ships and `verifier.md` is a non-functional stub; on disk all four personas are full/functional and two scripts ship, and the code default persona is the *generic* `verifier` (not `verify_sqlite` as prose says). `install.md` line 19 (`DEFAULT_MODEL: anthropic/claude-sonnet-4-6`) is stale, contradicted by its own Step 6. Files are the source of truth — documented in outdated-vs-current.md §2.

## Blockers

None.

## Caveats for the next stage (Codex chapter HTML build)

- Do NOT rebuild scaffold/site files; only the `vol-3-ma/18-verifier-agent` chapter HTML body remains (out of scope for this extract pass).
- The repo's own SVGs — `images/07-two-camps.svg` (Camp A vs Camp B) and `images/arch-loop.svg` (animated architecture) — are better renders of those two ideas than any video frame; consider embedding them alongside the frames.
- When a model name appears on a frame, annotate "video used GLM 5.1 / GPT-5.5; shipped default is openai/gpt-5.5; the model is one line." Don't hard-code either into prose as "the" verifier model.
- YT overlay IDs (RairMJflUSA, V5A1IU8VVp4) come verbatim from the lesson's own description; verify they resolve before publishing links (no video fetching performed, per brief).
- `current_practice_gaps` written against mid-2026 tooling (Pi harness, Claude Code hooks/Agent SDK); the model roster moves fast — re-check at publish time.

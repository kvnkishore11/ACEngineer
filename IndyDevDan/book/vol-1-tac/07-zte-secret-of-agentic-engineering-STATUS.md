# TAC-7 Chapter Status — ZTE Secret of Agentic Engineering

**Status:** COMPLETE — ready for Claude editorial/visual review  
**Lesson key:** `tac-7-zte-secret-of-agentic-engineering`  
**Output:** `vol-1-tac/07-zte-secret-of-agentic-engineering.html`  
**Lesson CSS:** `vol-1-tac/07-zte-secret-of-agentic-engineering.assets.css`

## Build summary

- Teaching-first chapter follows the source lesson’s evidence-before-doctrine order: five-work fan-out → velocity scale → isolation → state → model sets → review proof → KPI bottleneck → tactic → source gates → ZTE ship → composable-primitives secret → belief/posture close.
- All **12 major ideas** use the required ten-move pedagogy exactly once: Hook → Picture → Story → Name → Worked example → You try → Fail/fix → Current Practice → Retrieval (`<details>`) → Teach-back.
- All **12 lesson frames** are used at full teaching width with timestamped captions. Every source image is 1920×1080.
- Includes sticky chapter navigation, top/rail progress, mobile TOC, light shared design system, print rules, 59 paired retrieval disclosures, glossary, 2–3 hour graded capstone, troubleshooting, stretch drills, final pass sheet, and cumulative mastery.
- Current-practice overlay count is exactly **3 YouTube links**, matching the extract cap: isolation, subprocess→Agent SDK, and command prompts→Skills.
- Hub requirement is satisfied: `book/index.html` links Chapter 7 and marks it complete. During this build the parallel Chapter 8 workstream advanced the shared hub to **8/18 total and 8/8 TAC**, so that newer state was preserved rather than overwritten.

## Density estimate

- HTML source: approximately 1,754 lines / 174 KB.
- Approximate visible-text word count (markup and script removed): **15,965 words**.
- Print-equivalent estimate: **48–53 pages** at roughly 300–330 words per teaching page, within the requested 35–55-page target.
- This estimate intentionally includes lab instructions, retrieval answers, glossary, and captions because all are learner-facing teaching content.

## Source-grounding notes

- Video runtime values (#51, #52, #54, #62; the heavy random-data feature; the CSV-text patch; ports 9106/9206) are labeled as demonstration values and are not presented as committed repository artifacts.
- Committed evidence uses the actual snapshot: ADW `cc73faf1`, issue #47, `/chore`, attempts 1, plan 39 lines, diff 274/5/10, average presence 1.0, streak 1.
- Source-backed counts and mechanics are explicit: 14 ADW workflow scripts; 10 state fields; 8 ship-required fields; 18 model-map commands with 8 heavy escalations; three-way worktree validation; ports 9100–9114/9200–9214; blocker-only review failure; test/review abort; documentation nonblocking; `git merge --no-ff`; branch restoration attempts.
- The chapter teaches two real drift corrections instead of repeating the README: both SDLC orchestrators always pass `--skip-e2e`, and ship manually performs a `--no-ff` merge/push rather than the README’s squash description.
- The intentional naming duality is preserved: course tactic = **Zero-Touch Engineering**; code and bot messages = **Zero Touch Execution**.
- The lab operates only on a clone of the tac-7 course repository, pushed to a GitHub repository the learner controls because issue/PR/merge output requires ownership.

## Verification performed

- Extract gate: `_extracts/tac-7-zte-secret-of-agentic-engineering/STATUS.md` exists and reports DONE.
- HTML5 structural check: `tidy` reports no errors when course-used semantic tags are registered.
- Local references: **19 checked, 0 missing** (CSS, frames, hub, and previous chapter).
- Navigation: **16 anchors checked, 0 missing**; 30 IDs, 0 duplicates.
- Pedagogy: **12 idea sections**, each with exactly 10 required moves and no missing/duplicate move type; all 12 Story moves contain a frame or an extract-authorized diagram for an unframed-by-design beat.
- Frames: **12 referenced, 12 present**, all verified at **1920×1080**.
- Retrieval markup: **59 `<details>` / 59 `<summary>`**.
- Document structure: one opening/closing `html`, one opening/closing `main`; no build markers remain.
- YouTube overlay count: **3**.
- CSS is offline-first and reuses the gold chapter shell through the local `01-hello-agentic-coding.assets.css`; lesson-specific diagrams have responsive and print fallbacks.
- Two-axis review completed. Spec review promoted concurrent isolation into required Lab 1B and an unconditional final criterion. Standards review moved/added a visual into every Story move and raised state-card teaching paragraphs to the 17px body token. Both reviewers re-checked the fixes and passed them.

## Verification limitations

- The in-app browser QA connection failed because its runtime sandbox metadata was unavailable. Local Chrome headless also did not emit screenshots in this managed environment. Static HTML/link/frame/responsive-rule checks passed, but a human/Claude visual pass at desktop and mobile widths is still recommended.
- The capstone was not executed end-to-end: doing so requires GitHub writes/merge authority, API credentials, external billing, and 2–3 hours of agent runs. Every lab file/command and source claim was checked against the distributed tac-7 codebase.
- Publication-time YouTube metadata re-verification remains incomplete. `yt-dlp` is not installed and the browser fallback did not return video metadata. The IDs/titles are the extract’s locked, previously oEmbed-verified candidates.

## Open questions for Claude review

1. **Visual rhythm:** Does the 16.0k-word chapter need one additional print break or a shorter hero on narrow screens, especially before the long capstone?
2. **Current-practice wording:** Re-check the mid-2026 descriptions of first-class isolated tasks, Agent SDKs, and Skills immediately before publication; the durable/source sections should remain unchanged.
3. **Video overlays:** Verify that `fop_yxV-mPo`, `6fCqj4xFCZI`, and `X2ciJedw2vU` resolve and still match the displayed titles before publishing live links.
4. **Lab cost:** Confirm whether the required heavy full-SDLC run should remain mandatory for all learners or be an instructor-demonstrated checkpoint when token budget is constrained.
5. **Production guardrail boundary:** Consider adding a volume-level note (not a tac-7 code claim) distinguishing this course’s merge-to-main demonstration from real staged deployment/rollback policy.

## Claude review focus

- Inspect the desktop/mobile layout of the four custom teaching structures: velocity scale, state grid, guardrail stack, and primitive map.
- Sample-check the 12 frames for caption accuracy and legibility at full width.
- Confirm that the strong ZTE language is consistently constrained by “Target,” per-class evidence, and the chores→bugs→features progression.
- Preserve the source-truth warnings about skipped browser E2E, `--no-ff`, lowercase downgrade, and runtime-vs-snapshot evidence.

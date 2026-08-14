# TAC-1 Cross-Review — Claude Fable (technical accuracy)

Reviewer: Claude Fable · 2026-07-12
Scope: `01-hello-agentic-coding.html` + `01-hello-agentic-coding.assets.css` vs the locked extract set (`_extracts/tac-1-hello-agentic-coding/`) and the real course files (`tac/tac-1/`).

## Verdict: **PASS WITH FIXES**

Two small accuracy/navigation defects found and fixed in place (listed below). No open critical issues. Every course-file quotation, permission enumeration, launcher behavior claim, Dan attribution, YouTube overlay, internal path, and pedagogy-structure requirement checked out. This chapter is fit to serve as the gold template.

---

## What was verified (evidence, not vibes)

### Course-file spot checks — all match
- **README.md is exactly 35 lines** (`wc -l` = 35); the chapter's "exactly 35 lines" and "seven files" claims are literally true (7 committed files on disk).
- **Both README prompts are quoted char-for-char** in §05 — including the easy-to-mangle `print a concise explanation of the definition of ai agents` line and the commit message `Demo agentic coding capabilities`.
- **`.claude/settings.json`**: the chapter's code block matches the real 9-entry allowlist; every enumeration derived from it (3 file tools; checkout/branch/add/commit; `Bash(uv run:*)`; `WebSearch` as the single non-local tool; no `git push`) is correct.
- **`programmable/prompt.md`**: RUN / CREATE `main_aic.py` / CREATE `main_tac.py` / RUN / REPORT confirmed; the chapter's "two differences vs the README prompt" (self-contained + REPORT contract) and the verbatim REPORT block are exact.
- **Launcher behavior claims (shell/py/ts) — the hard part — are all accurate:**
  - `programmable.sh` is the 3-statement pattern quoted; the chapter's claim that it does **not** capture stderr and loses the child exit status after the final `echo` is true (no `set -e`; command substitution captures stdout only).
  - `programmable.py`: the chapter's excerpt is a flagged simplification, and its statement that the real file *also* prints stderr and catches exceptions is true; `sys.exit(result.returncode)` propagation confirmed.
  - `programmable.ts`: quoted lines match; catch → `console.error` → `process.exit(1)` confirmed.
- **Lab commands match the README verbatim**: `sh programmable/programmable.sh`, `bun run programmable/programmable.ts`, `uv run python programmable/programmable.py`; clone URL `https://github.com/disler/tac-1.git` matches the extract.
- `.env.sample` = `ANTHROPIC_API_KEY=` — the chapter's "API-key placeholder for the headless billing path" description is fair.

### Concept accuracy
- **Core Four / Big Three**: correct everywhere — superset framing, the precise delta phrase ("prompts that can reliably execute long chains of tools"), and the scale-and-performance rebuttal all match the extract's canonical wording.
- **AI vs Agentic A/B**: the five-action delta (branch / create / execute both / stage+commit / manage+report) mirrors lab-spec Checkpoint 1 exactly; the dependency insight (README Prompt B runs `main_aic.py` but doesn't create it; `prompt.md` fixes that for headless runs) is correct and correctly tested in Mastery Q6.
- **Dan attribution audit — no invented claims found.** Every "Dan says/states" assertion traced to the extract's quotes/timeline: the 2023 domain bet, decade-plus hand-coding and missing it, "they" = boss/company/industry/AI, nothing-in-tech-is-forever, 10x-as-arbitrary-leverage, the twice-said tactic reveal at ~6:47, "seen a million times," the Aider phase-1 analogue, the three essential elements, millions of tokens / pay-to-play, and the contradicting truth (~20:47). The chapter also explicitly declines to invent a dollar estimate — good.

### YouTube overlays (resolves 01-STATUS open question 1)
Exactly 3 cards, all `include_in_phase1: true`, both deferred videos absent. **Live oembed check performed this session — all three IDs resolve to IndyDevDan videos:**

| ID | Real title (oembed) | Chapter card | Status |
|---|---|---|---|
| `2TIXl2rlA6Q` | AI Coding is NOT ENOUGH: Claude Code's NEXT LEVEL Agentic Coding FEATURE | "AI Coding is NOT ENOUGH" | ✅ resolves; card uses the extract's short title (prefix of full title) |
| `6fCqj4xFCZI` | How Claude Code CHANGED Engineering Forever (and what's next) | "How Claude Code CHANGED Engineering Forever" | ✅ resolves; short title |
| `X2ciJedw2vU` | RAW Agentic Coding: ZERO to Agent SKILL | same | ✅ exact match |

Placement is sensible (thesis video in §03, form-factor video in §06, Skills video in §07) and matches each `maps_to` role.

### Paths, anchors, structure
- All 12 frame `src`s, all 4 CSS links, and the hub link resolve on disk; the hub (`../index.html`) links back to the chapter.
- All 12 rail-nav anchors match defined section ids; no duplicate ids.
- Frame-caption timestamps (1:55, 2:04, 2:42, 6:54, 11:40, 12:28, 13:10, 14:05, 15:03, 17:43, 18:25, 20:05) all match `frame-plan.json`.
- t1250 correctly rendered as a designed pull-quote, honoring `diagram_instead: true`.

### Pedagogy completeness
- All **8 ideas × 10 moves** verified programmatically (hook → picture → story → name → worked example → you-try → fail/fix → current practice → retrieval → teach-back), each with 3–4 retrieval questions and a teach-back.
- Graded lab mirrors `lab-spec.md` near-1:1: Checkpoints 0–2, S1–S4 stretch drills, troubleshooting table keyed to the Core Four, final pass sheet including the zero-hand-typing prime directive and the S3 restore step.
- 16-question cumulative mastery check in 4 rounds + capstone teach-back; glossary matches the extract's canonical terms (including the "loop box" transcript-mishearing note).

### Rendering (resolves 01-STATUS open question 4, within a static/browser check)
Loaded in Chrome at 1440×1000 and 390×844: **zero console messages**, zero horizontal overflow at both widths, and a programmatic sweep of all 4 inline SVGs found **no text overflowing any viewBox**. Sticky rail, reading-progress bar, active-section highlight, details/summary reveals, and the mobile TOC (rail hidden, TOC shown) all behave. Print pagination not exercised (no printer emulation in this pass); `break-inside: avoid` rules are present.

### Other STATUS open questions
- **Q2 (mid-2026 current-practice claims):** checked against Claude Code as this reviewer knows it — Agent Skills (`SKILL.md`, on-demand loading), `claude -p` headless flags (`--output-format json|stream-json`, `--allowedTools`, `--permission-mode`, session resume), Agent SDK (Python/TS), permission modes / hooks / sandboxed bash / settings layering, subagents & background tasks & worktree parallelism. All statements are accurate and appropriately hedged with "can add / current practice." Re-verify at publish; this axis moves fast.
- **Q3 (strict all-three-launcher pass):** CONFIRMED correct — `lab-spec.md` pass criteria require "All three (or four, with S2) launchers completed headlessly." The chapter's strict reading (Bun optional at audit, required for full pass) is the locked spec's reading.
- **Q5 (page estimate):** 13,100 words ≈ 29–37 pp as pure dense prose; frames/diagrams/tables/code/disclosures plausibly add ~13–16 pp → the 45–52 claim is reasonable (extract predicted ~40). No action.

---

## Critical issues

**None open.** Two defects were fixed in place during this review (small, surgical, verified):

1. **FIXED — A/B comparison card misrepresented the agentic prompt's shape.** §05's phase-2 card rendered the prompt as four runbook headings (`RUN / CREATE / RUN / RUN`) inside a verbatim-styled code block — the real README has three blocks (`RUN / CREATE / RUN`), and the card's own "Verbs: run, create, run" bullet plus §05-move-4's "compact runbook grammar: RUN, CREATE, RUN" contradicted it. Reflowed the last two lines into one RUN block (`RUN: execute both files,\n     add + commit`). A learner cross-checking against the README now sees a consistent structure.
2. **FIXED — Glossary unreachable from the mobile TOC.** The rail nav lists 12 sections including Glossary; the mobile `<details>` TOC stopped at Mastery check, and the rail is `display:none` below the breakpoint. Added the missing `<li><a href="#glossary">Glossary</a></li>`.

## Medium issues (open — for the chapter author / fan-out template)

1. **The "minutes to hours" scale claim was dropped.** The extract carries it in `core_four.why_scale_matters`, nugget #10, and retrieval Q11 ("How long can agentic coding prompts run…? Minutes to hours, end to end, with and without your oversight"). The chapter teaches scale-and-performance and "environments where you are absent," but never states the duration claim anywhere (grep-verified). One sentence in §04's or §06's story move closes it; consider adding the matching retrieval question.
2. **Frame selection trade-off.** 12 frames used — the maximum of the chapter brief's 5–12 budget — but the four omitted include two the frame plan flags as high-value for weak students at lab-adjacent moments: `t0570` (essential-tools checklist — "audit your setup against Dan's exact list before the lab") and `t1000` (the README-35-lines shot — the "everything in TAC is built on 35 lines" thesis artifact, which §07 references in prose). Within the locked budget this is a judgment call, not a defect; if any swap is ever considered, `t1000` is the strongest omitted candidate.
3. **Loot box appears only in the glossary.** The course's install links and clone link live in the per-lesson loot box; the chapter substitutes direct commands and the clone URL (functionally complete), but one orientation sentence in Lab 0 would help readers following the actual course page.
4. **`data/curriculum.json` is stale**: tac-1 still shows `status: "extracted"`, `chapter_html: null` while the chapter exists and the hub links it. Update to `chaptered`/`reviewed` with the path. (Not touched by this review — report-only write scope.)
5. **`.lab-box__steps` has no CSS rule** despite being the documented markup in `components.css`'s usage comment. Harmless today (base `ul, ol` styles apply), but the fan-out template should either define the class or drop it so 17 more chapters don't cargo-cult a dead class.

## Nitpicks (recorded, no action)

- §04: "It cannot push the commit under this allowlist" — strictly, an allowlist doesn't hard-deny; interactively Claude Code would *ask*. True as stated for headless runs, and it matches the lab-spec's own framing ("Which git subcommands are NOT (e.g. push)"); S3's "halts, refuses, or asks" already teaches the nuance. Consider "is not pre-approved to push" at next touch.
- §06 worked example: "five tool executions" — the t0790 trace could be counted as six discrete calls (checkout, Write, uv ×2, add, commit) unless add+commit ran as one command. Ambiguous on the evidence; left alone because "five actions" is the lab's locked framing.
- §07 diagram compresses `prompt.md` to "RUN/CREATE/REPORT" in an SVG label — acceptable shorthand for the heading vocabulary.

---

## Praise / gold-template notes

- **Honest-simplification discipline is the standout pattern.** When the chapter abridges `programmable.py`, the very next sentence says the real file also prints stderr and catches exceptions. Every simplification is flagged in-line. Mandate this for all remaining lessons.
- **The shell/py/ts error-policy comparison is exactly right** ("wrapper quality determines what an outer system can learn about failure") — accurate to the letter of the course files and genuinely additive over the video.
- **The 10-move cycle is executed, not templated.** Every hook is a concrete failure scenario; every current-practice overlay is dated ("mid-2026") and scoped; every retrieval answer hides behind a disclosure; the overlay cap is stated in-page (§08: "stays within the locked maximum of three").
- **Zero invented Dan.** All attributions trace to the extract; the chapter even refuses to invent a dollar figure for token costs.
- **The lab is gradeable as written** — checkpoints, pass criteria, troubleshooting keyed to the Core Four, reset/restore steps, and destructive-command guardrails ("Do not improvise destructive Git commands") all present.
- **The orientation section's framing device** (delegating *typing* vs delegating an *outcome-producing chain*) is a better on-ramp than the video's own cold open and stays faithful to the thesis.
- **The A/B "compare state transitions, not artifacts" move** and the "runbook as state machine" reading of RUN/CREATE/RUN are the pedagogical core done right — these should be reused wherever later lessons contrast weak vs strong prompts.

## Fan-out checklist (for the remaining 17 lessons)

1. □ Quote course artifacts verbatim, or visibly flag the simplification in adjacent prose ("the actual course file also…").
2. □ Verify every countable claim (line counts, file counts, tool lists, timestamps) against the artifact before writing it.
3. □ Diff the draft against the extract's `what_student_must_internalize` **and** `retrieval_questions` — every dropped item is a defect (this chapter dropped one: minutes-to-hours).
4. □ Reproduce lab-spec checkpoints and pass criteria 1:1; keep every pass criterion checkable from evidence; include reset/restore steps and a scope contract.
5. □ Overlays: only `include_in_phase1: true` IDs, ≤3, each labeled with its `maps_to` role; oembed-verify IDs at review time; state the cap in-page.
6. □ All required moves per idea; per-idea retrieval + teach-back; cumulative mastery check; glossary from the extract's canonical terms.
7. □ Frames within the budget, prioritizing frame-plan entries whose `why_for_weak_student` is lab-critical; honor every `diagram_instead` flag with a designed element.
8. □ Paths: CSS/media/hub links resolve; nav anchors ↔ section ids 1:1; **mobile TOC mirrors the rail TOC exactly, including the last section**.
9. □ Programmatic render pass: console clean; no horizontal overflow at ~1440 and ~390; SVG `<text>` bboxes inside their viewBox.
10. □ No invented quotes, prices, or model names; date every current-practice claim; keep the tool-transferability disclaimer.
11. □ Update `data/curriculum.json` (`status`, `chapter_html`) when the chapter lands; keep the hub in sync.
12. □ Cross-review writes its report next to the chapter (`NN-CROSS-REVIEW-CLAUDE.md`) and applies only small, high-confidence surgical fixes.

---

*Fixes applied in this review: 2 (listed under Critical issues → FIXED). Files touched: `01-hello-agentic-coding.html` only. Report written to this file only.*

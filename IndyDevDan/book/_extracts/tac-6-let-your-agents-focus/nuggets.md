# TAC-6 Nuggets — ranked for the struggling learner

Ordering rule: how much of the rest of your agentic layer collapses if this nugget is missing. Tier 1 is the tactic and its two load-bearing distinctions; Tier 2 is the machinery that makes review and document real; Tier 3 is the posture that keeps you building systems instead of hand-fixing artifacts.

---

## Tier 1 — If you remember nothing else

**1. One agent, one prompt, one purpose — and "one purpose" does NOT mean "small prompt."**
Each workflow step spawns a fresh named agent that runs exactly one slash-command template and exits. No agent ever runs a second prompt. But the prompts are huge — template meta prompts and higher-order prompts from lessons 3–5. Dan is explicit: "this doesn't mean the prompt isn't large or the prompt doesn't do a lot of work." The purpose is singular; the work is not. Gutting your templates to make them "focused" is the #1 way to misread this lesson.
*Test yourself:* search `slash_command=` in the codebase — 14 hits in 4 files is the complete inventory of what any agent can be asked to do. If you can't produce that list, you don't yet see the tactic.

**2. Review is not testing. Different question, different agent.**
Testing asks "does it work?" Review asks "is what we built what we asked for?" — spec conformance, proved, not functionality and not code quality. Dan: grouping them is "a massive mistake, especially in the age of agents." The whole demo is engineered to make this bite: the export button downloads a perfectly correct CSV (testing would pass) and is still in the wrong place (review's job). If your CI is green and you think you're done, you just skipped a question.

**3. The SDLC is five questions, and a step you can phrase as a question is a step you can hand to an agent.**
Plan — what are we building? Build — did we make it real? Test — does it work? Review — is what we built what we planned (prove it)? Document — how does it work? Each question = one ADW script + one prompt. The composers are literally sentences made of questions: `adw_plan_build_review`, `adw_sdlc`. Only Review carries a suffix no other step has: **"(Prove it)."**

**4. More context is not better. Fresh beats big.**
"Isn't more context better for your agent?" Dan: "This is not true." An overloaded window makes a distracted, confused agent that's lost the original task — context pollution / overloading / toxic context. The cure is never a bigger window; it's a fresh, focused window per purpose, holding the minimum context required to solve the one problem. Every token you add is another variable the agent must reason about.
*Corollary weak learners miss:* context engineering in TAC mostly means WITHHOLDING context, not piling it on.

---

## Tier 2 — The working machinery

**5. The review ADW is a typed proof machine, not a vibe check.**
`adw_review.py`: find the spec from state → run `/review` (opus) → parse strict JSON into a pydantic `ReviewResult` → upload 1–5 screenshots to a public bucket so they render on the issue → post a severity-grouped report ending in the raw JSON. A parse failure doesn't pass silently — it synthesizes a *blocker* so the pipeline fails LOUD. The prompt's JSON contract and the code's type are the same shape; that's the leverage.

**6. Severity triage is templated judgment: skippable / tech_debt / blocker.**
"These agents are very agreeable... if you ask them to find something, they'll find something." Without a triage vocabulary, every nitpick blocks the release. Only blockers set `success=false`, and only blockers get auto-resolved. The severity classes aren't bureaucracy — they're how you keep an agreeable, genuinely-good-at-finding-things agent from crying wolf.

**7. The patch loop: a distinct change class that reuses the implementor.**
A patch is not a chore/bug/feature — "we're just changing one thing." `/patch` writes a minimal plan into `specs/patch/` (2–5 steps, scoped to only the `review_change_request`), then `create_and_implement_patch()` hands it to the SAME `/implement` higher-order prompt every other plan uses. Trigger it out-loop by commenting the literal keyword `adw_patch` + your request on the issue.

**8. Conditional documentation is the loop-closer — and it's agentic.**
`/document` does two things: writes `app_docs/feature-{id}-{name}.md` AND appends an entry to `conditional_docs.md` ("read this doc only when the condition matches"). Then bug, chore, feature, patch, and prime all READ `conditional_docs.md` at planning time. Plan → build → test → review → document → back into plan. "This seals the deal. This connects them all." The committed file ships with exactly 4 entries; the 5th appears only after YOUR documenter runs.

**9. Committed prompts are evals you already have the infrastructure for.**
Every step is one committed file with reproducible state. `git checkout` the pre-run state, change ONE knob — model in `SLASH_COMMAND_MODEL_MAP`, thinking mode, agentic tool — `uv run adws/adw_review.py 14 <adw-id>`, and diff the two `ReviewResult` JSONs. That's a literal eval for your agentic layer, built from git. If you can't `git log` your agent's behavior change, you have vibes, not an agentic layer.

**10. adw_review and adw_document REQUIRE the adw-id; pass the issue number, not the PR number.**
Both hard-exit without state ("Run adw_plan.py first" / "documentation can only be generated after..."). The ADW ID chains all phases via `agents/{adw_id}/adw_state.json` (adw_id, issue_number, branch_name, plan_file, issue_class). Dan's on-camera stumble is the lesson: he passed 15 (the PR number) instead of 14 (the issue) — the state echo in the issue comments is how you catch it.

---

## Tier 3 — Posture that keeps you building systems

**11. Three constraints — and model intelligence is NOT one of them.**
You're bounded by (1) the context window, (2) codebase + problem complexity, (3) your abilities. Specialized one-purpose agents bypass two: the window is freed per step, and your ability ceiling matters less because your engineering is templated into committed prompts. Dan draws a hard line: "model intelligence is not a constraint. Don't use this as an excuse... This is a losing mindset."

**12. Compact is a band-aid.**
"If your agent is running compact, it is losing information." Compression is loss by construction. One-purpose agents rarely need it because each starts with a fresh window. Leaning on `/compact` to survive a bloated session is treating the symptom the tactic exists to prevent.

**13. When it breaks, blame the layer — then upgrade the layer.**
The review step itself missed the misplaced button. Dan's response is the most transferable posture in the course: "I'm not blaming the model for this. I'm blaming my skills. I'm blaming the ADWs we have set up right now." Two root causes (test step skipped; screenshots captured but never read), one fix location — the review PROMPT ("for every image you take, be sure to read it in"), not the global `.mcp.json`. Fix the end-to-end portion, not the thing that went wrong.

**14. Build the system that builds the system — even when your hands are faster.**
Dan runs the full patch workflow to nudge one button, and pre-empts you: "Why didn't you just do that by hand? You're missing the point... This isn't about you anymore... It's about teaching your agents how to build on your behalf, so that it can be about you again." A hand-fix leaves the system exactly as fallible as before, and the fix isn't reproducible.

**15. Ideal presence is 2, and proof is what buys it.**
Two human moments per shipped unit: prompt input at the start, review + PR merge at the end. The review system carries a hard/live asset (image, video, report, metrics) to YOU, so you can say yes/no in seconds even when the agent is wrong — that's review velocity. The lesson grades itself honestly: presence hit ~3 this run (the patch cost one), and the scoreboard is a diagnosis, not a vanity metric.

---

## Micro-quiz (close the book first)

1. State the five SDLC questions. Which one demands proof, and why is it a different question from "does it work?"
2. What does "one purpose" NOT mean, and what single search proves the tactic is real in the codebase?
3. Name the three review severity classes. Which block? Which get auto-resolved? What caps the resolution loop?
4. The export button downloaded a correct CSV. Give BOTH reasons review still missed the real bug, and where Dan puts the fix.
5. What two artifacts does `/document` produce or modify, and which five prompts read the second one?
6. Name the three constraints, the two the tactic bypasses, and the one thing Dan refuses to call a constraint.

*(Answers: extract.md ideas 1, 3, 6, 9, 8, 4.)*

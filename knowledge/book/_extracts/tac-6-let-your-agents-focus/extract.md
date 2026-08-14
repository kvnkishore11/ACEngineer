# TAC-6 · Let Your Agents Focus — Master Teaching Notes

> Source of truth for the expanded chapter. Video 57:16 · Advanced (first of three) · Tactic #6: **One Agent, One Prompt, One Purpose**
> Lesson artifact: the tac-6 codebase — the Natural Language SQL app wrapped in a five-step agentic layer. New this lesson: `/review`, `/patch`, `/document`, `conditional_docs.md`, `prepare_app.md`, seven new ADW scripts, and the Cloudflare R2 uploader.

**Lesson thesis in one sentence:** Finish the software developer lifecycle — review (is what we built what we asked for? prove it) and document (how does it work, and when should future agents read about it?) — with dedicated one-purpose agents, because a fresh focused context window per step beats one polluted god-session every time.

**The chapter must land ten ideas.** Each below follows: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q.

---

## Idea 1 — The SDLC is five questions, and two were still unanswered

**Hook.** After five lessons your agents can plan, build, and test. Dan opens with a claim: with just those three steps "you will outperform any cloud-based agentic coding tool." So why are there two more lessons of machinery? Because your agents still can't answer two questions: *did we build what was asked?* and *how does it work?*

**Picture.** Frame t0152 (2:32): the SDLC-as-Questions slide — 1 Plan / 2 Build / 3 Test / 4 Review / 5 Document with all five questions, and Review's carries a suffix no other step has: **"(Prove it)"**.

**Worked example.** The question framing is executable: each question is one ADW script and one prompt. `adws/adw_plan.py`→`/chore|/bug|/feature`, `adw_build.py`→`/implement`, `adw_test.py`→`/test`, `adw_review.py`→`/review`, `adw_document.py`→`/document`. The lesson's composers are literally sentences made of questions: `adw_plan_build_review.py`, `adw_sdlc.py`.

**Dan's term.** *SDLC as questions and answers.* "The plan step asks, what are we building? The build step asks, did we make it real? Testing says, does it work? The review step asks, is what we built what we planned. And then of course, document asks, how does it work?"

**Failure mode.** Treating the five steps as ceremony instead of as a question checklist. The test: for any workflow you own, can you name the question each stage answers? If two stages answer the same question, one of them is redundant; if a question has no stage, you have a hole — most teams' hole is exactly review-as-distinct-from-testing.

**Retrieval Q.** State the five questions, and which step demands proof. *(What are we building / did we make it real / does it work / is what we built what we planned — prove it / how does it work.)*

---

## Idea 2 — Review ≠ testing: different questions, different agents

**Hook.** "Some engineering teams group these together. I think that's a massive mistake, especially in the age of agents." The whole demo is engineered to make this distinction bite: a feature that *works* (testing would pass the download) and still isn't *what was asked* (the button is in the wrong place).

**Picture.** Frame t1912 (31:52): the review's own uploaded screenshot showing the Export button floating mid-header instead of "directly to the left of the 'hide' button" — the spec line the issue highlighted.

**Worked example.** `review.md` says it in bold: "we're not testing. We know the functionality works. We're reviewing the implementation against the spec to make sure it matches what was requested." It reads the spec from `specs/`, diffs against `origin/main`, uses `.claude/commands/e2e/test_*.md` files **only as navigation guides** for where to screenshot, and returns spec-conformance findings — not test results, not code-quality notes ("we're handing all that off to our agents").

**Dan's term.** *Review answers: is what we built what we asked for?* Also *review velocity* — the KPI this step exists to raise.

**Failure mode.** Two directions: (a) merging review into CI ("tests pass = reviewed") — the demo's bug sails through; (b) letting review re-litigate code quality and architecture — that's not its question, and it burns the focused window on someone else's job.

**Retrieval Q.** The demo feature downloaded a correct CSV. Why did review still have work to do? *(It answers a different question: the placement requirement in the spec was violated even though functionality worked.)*

---

## Idea 3 — Tactic #6: One Agent, One Prompt, One Purpose

**Hook.** "This tactic drives great agentic development at scale because it forces us to make a controversial decision and commit to it." The controversy: while big tech chases the all-in-one god model, you go the other way — many small agents, each with one committed prompt and one purpose.

**Picture.** Frame t0278 (4:38): the tactic slide — definition paragraph plus five Daily Actions (dedicated agents per workflow step; prompts focused on single purposes; free up context windows; commit and version-control all agent prompts; evaluate and improve individual agent performance).

**Worked example.** The codebase enforces it structurally: every phase constructs an `AgentTemplateRequest` with a named agent and exactly one slash command. `adw_review.py` declares its cast as constants at the top — `AGENT_REVIEWER = "reviewer"`, `AGENT_REVIEW_PATCH_PLANNER`, `AGENT_REVIEW_PATCH_IMPLEMENTOR` — and no agent runs a second prompt, ever. Search `slash_command=` and you get all 14 call sites in 4 files: the complete inventory of what any agent can be asked to do.

**Dan's term.** *One agent, one prompt, one purpose* — "one, one, one." Crucial nuance kept verbatim: "this doesn't mean the prompt isn't large or the prompt doesn't do a lot of work" — the prompts are template meta prompts and higher-order prompts from lessons 3–5.

**Failure mode.** Reading "one purpose" as "simple prompts" and gutting the templates; or nodding along and then stacking plan+build+review into one interactive mega-session "to save tokens" — which quietly rebuilds the god-session the tactic exists to kill.

**Retrieval Q.** What's the strongest one-sentence proof the tactic is real in this codebase, and what does the tactic NOT mean? *(No agent runs more than a single prompt; it does not mean prompts are small — purpose is singular, work is not.)*

---

## Idea 4 — Context pollution and the minimum context principle

**Hook.** "Isn't more context better for your agent? The more it knows the better it performs?" Dan's answer is flat: "This is not true." He gives the failure a name you'll recognize in your own sessions: a distracted, confused agent that's lost track of the original task.

**Picture.** No slide — this run (4:55–11:20) is deliberately talking-head. Render as a designed spread: one polluted 1M-token window vs five fresh windows, each holding only its step's context. (Frame plan flags this beat `diagram_instead`.)

**Worked example.** The tactic's payoff in numbers Dan names: "you give your agent the full 200K, 500K, 1 million tokens... all of the space and the opportunity to solve the one problem well." And the codebase's implementation of *minimum context*: prompts declare variables at the top (`adw_id: $1`, `spec_file: $2`...) that act as "information dense keywords on the fly," referenced throughout; `conditional_docs.md` loads documentation **only** when a condition matches — "You don't want to excessively read documentation."

**Dan's term.** *Context pollution / context overloading / toxic context*; *the minimum context principle* ("context engineer as little as possible"); *adopt your agent's perspective*. The three constraints: context window, codebase+problem complexity, your abilities — "specialized agents bypass two out of three." And the guardrail: "model intelligence is not a constraint... this is a losing mindset."

**Failure mode.** Cargo-culting context: pasting the whole repo, every doc, every prior transcript into each prompt "to be safe." Every added token is another variable the agent must reason about. Second failure: leaning on `/compact` to survive bloated sessions — "if your agent is running compact, it is losing information." The band-aid is not the cure.

**Retrieval Q.** Name the three constraints, the two the tactic bypasses, and what Dan calls compact. *(Context window / complexity / abilities; bypasses window + abilities; compact is a band-aid fix that loses information.)*

---

## Idea 5 — Committed prompts become evals

**Hook.** A side effect of one-one-one that Dan flags as "a big idea" he won't fully explore: because every step is a committed prompt file with reproducible state, **your codebase becomes evaluable**.

**Picture.** Frame t1305's right half (data_types.py) plus the model map: `/review`→opus, `/document`→sonnet — per-step model routing in eight lines of `SLASH_COMMAND_MODEL_MAP`.

**Worked example.** The eval loop with tools you already have: `git checkout` the state before a run, change one variable (model in the map, thinking mode, agentic tool), rerun `uv run adws/adw_review.py 14 <adw-id>`, diff the two `ReviewResult` JSONs. In-loop runs "battle test" prompts until they're ready to run out-loop in the AFK system. Passive version: you'll form evals in your head just by watching which prompts work.

**Dan's term.** *Evals for the agentic layer of your codebase.* Supporting: "we can easily reproduce and more importantly, improve every single step down to the prompt level," vs. others "running big context windows that'll be blown away at the end."

**Failure mode.** Prompt archaeology: iterating prompts inside chat history, where nothing is committed, nothing reruns, and improvements evaporate. If you can't `git log` your agent's behavior change, you don't have an agentic layer — you have vibes.

**Retrieval Q.** What two properties make a workflow step evaluable, and name two knobs you can turn between runs. *(Committed prompt + reproducible state; model per slash command / thinking mode / agentic tool.)*

---

## Idea 6 — The review ADW: typed proof, severity triage, agentic resolution

**Hook.** "Whenever you want to understand one of these workflows, go right to the main method." The review workflow's docstring already tells the story: find spec → review against it → screenshot critical paths → resolve issues → post results → push and update the PR.

**Picture.** Frame t1305 (21:45): review.md's Output Structure beside the `ReviewResult`/`ReviewIssue` pydantic types — the prompt contract and the code type are the same shape. Frame t1068 (17:48): the 7-line `adw_state.json` that chains every phase.

**Worked example.** The pipeline, exactly as coded in `adw_review.py`: adw-id **required** → load state, checkout the state's branch → `find_spec_file` (state → diff → branch-pattern glob) → init `R2Uploader` (silently disabled unless all four Cloudflare vars exist) → up to `MAX_REVIEW_RETRY_ATTEMPTS = 3`: run `/review` (opus), parse strict JSON into `ReviewResult` (a parse failure synthesizes a *blocker* — the pipeline fails loud) → upload screenshots to `adw/{adw_id}/review/…`, save URLs into state for the documenter → post the grouped report (🚨/⚠️/ℹ️ + raw JSON payload) → if blockers: patch-and-re-review; finally commit, push, update PR; exit 1 if blockers remain. The prompt side: 1–5 numbered screenshots (`01_name.png`), critical paths only, absolute paths, `prepare_app.md` executed first (reset DB, background start).

**Dan's term.** *Severity guidelines* — `skippable` / `tech_debt` / `blocker`; "we don't want to block on skippable or tech debt." And the warning that motivates them: "these agents are very agreeable... if you ask them to find something, they'll find something. You want to give them the tools to delineate what is important."

**Failure mode.** No triage contract → every nitpick blocks the release. No typed output → downstream code parses prose. No retry cap → the loop fixes forever. Each guardrail in this file answers a specific agent pathology; strip one and you rediscover the pathology.

**Retrieval Q.** Which severities block, what caps resolution, and what happens when the review output fails to parse? *(Only blockers; 3 attempts; a synthetic blocker-severity ReviewResult — loud failure.)*

---

## Idea 7 — The patch loop: surgical fixes, reused implementor

**Hook.** The review's proof exposed a real bug (Export not left of Hide). Watch what Dan does *not* do: he doesn't open the CSS. He writes a comment containing `adw_patch` and runs a workflow — "I'm going to operate this like we're working outside the loop just for good practice."

**Picture.** Frame t2190 (36:30): the whole patch run in one terminal — plan at `specs/patch/patch-adw-490eb6b5-fix-download-button-position.md`, commit `patch: fix button layout for export feature`, comments to issue #14, PR #15 updated, "Patch workflow completed successfully." Frame t2255 (37:35): Export now sitting immediately left of Hide.

**Worked example.** `/patch` is a template meta prompt like chore/bug/feature — but its class is different: "we're just changing one thing. We want a simple quick fix." Minimal scope ("Address only the `review_change_request`"), 2–5 steps, validation pulled from the spec or `test.md`, a lines-of-code estimate and risk level. Then `create_and_implement_patch()` validates the returned path (`specs/patch/*.md`) and hands it to the same `/implement` higher-order prompt every other plan uses. Note the on-camera stumble worth teaching: Dan first passed 15 (the PR number) instead of issue 14 — the state echo in the issue comments is how you catch it.

**Dan's term.** *Patch* as a distinct problem class; *create and implement patch* as the shared method; "we're starting to get some reuse of the compositional pieces of our code base."

**Failure mode.** "Why didn't you just do that by hand?" — Dan pre-empts it: "You're missing the point... we are putting in the effort to build the system that builds the system... This isn't about you anymore. It's about teaching your agents how to build on your behalf, so that it can be about you again." Hand-fixes leave the system exactly as fallible as before.

**Retrieval Q.** How is a standalone patch triggered, and which prompt implements the patch plan? *(The literal keyword `adw_patch` in the latest issue comment or body, then `uv run adws/adw_patch.py <issue> [adw-id]`; the reused `/implement` higher-order prompt.)*

---

## Idea 8 — Document: two problems, and the loop that closes the SDLC

**Hook.** "Documentation is simple, but how you document and when to include your documentation is the tricky part." Two problems, two mechanisms — and the second one is the lesson's finale: it makes the whole lifecycle a loop.

**Picture.** Frame t2742 (45:42): `conditional_docs.md` with the fifth entry the documenter just appended (`app_docs/feature-490eb6b5-one-click-table-exports.md` — "When working with CSV export functionality"). Frame t2815 (46:55): search proof that bug, chore, document, feature, patch, and prime all reference conditional docs.

**Worked example.** `adw_document.py` (adw-id required; graceful skip when `git diff origin/main` is empty) passes `[adw_id, spec_path, screenshots_dir]` to `/document`, which: analyzes the diff (--stat, --name-only, per-file for >50-line changes), reads the spec, copies review screenshots into `app_docs/assets/`, writes `app_docs/feature-{adw_id}-{name}.md` from the committed template (Overview → Screenshots → What Was Built → Technical Implementation → How to Use → Configuration → Testing → Notes), **then updates `conditional_docs.md`** and returns exclusively the doc path. Committed baseline: exactly 4 conditional entries; the fifth appears only after your documenter runs. Taxonomy note kept verbatim: "AI docs for third party, app docs is for your codebase."

**Dan's term.** *Conditional documentation*; *the agentic layer feedback loop*: "our agents are fully connected, right, from planning to building to testing to reviewing to documenting their work... This seals the deal. This connects them all." Caveat he states: the conditional pattern relies on model strength — "if they just come in here and read them... scale up your model."

**Failure mode.** Docs written for humans only, stored where no prompt looks, or bulk-loaded into every prompt (pollution again). Also hand-editing `conditional_docs.md` — the entry must be the documenter's job or the loop has a human SPOF.

**Retrieval Q.** What TWO artifacts does the document step produce/modify, and who reads the second one? *(`app_docs/feature-…md` + an appended `conditional_docs.md` entry; read by bug, chore, feature, patch, and prime at planning time.)*

---

## Idea 9 — When review misses: blame the layer, upgrade the layer

**Hook.** The uncomfortable twist: the review step *itself* failed here — the spec said "directly to the left of the hide button," the plan carried it, the agent missed it, and the review report said success. Dan's response is the lesson's most transferable posture: "I'm not blaming the model for this. I'm blaming my skills. I'm blaming the ADWs we have set up right now."

**Picture.** Frame t2135 (35:35): `.mcp.json` with `--vision` typed in — and then rejected ("I don't like this because this is outside of the ADW... keep general configuration here").

**Worked example.** The post-mortem, exactly as run on camera: (1) the test step was **skipped** — `adw_plan_build_review`, not `adw_plan_build_test_review`; "the UI test very likely would have caught this... this is probably the winning workflow." (2) The reviewer captures screenshots it never reads — no vision flow; "the actual screenshots never make it into the agent. The tokens aren't flowing through the vision capabilities of our language model." The fix he chooses belongs in the *prompt*, not the global config: "for every image you take, be sure to read it in during the review process." (3) Verify the chain before blaming a link: was the requirement in the issue? yes. In the plan? yes ("did I have the original request inside the plan... let's just look"). So the gap is review's — now you know *which* prompt to improve.

**Dan's term.** *Fix the end-to-end portion, not the thing that went wrong.* "If something goes wrong, you fix the end to end portion... They're called out-loop systems for a reason."

**Failure mode.** Model-blaming (a losing mindset, and it points you at the one thing you can't fix) — or its mirror, silently hand-patching the artifact and leaving the review prompt exactly as blind as it was. The failure *class* must land in the layer: a prompt instruction, a workflow choice, a template line.

**Retrieval Q.** Give both root causes for the missed placement bug and Dan's chosen fix location. *(Test step skipped; screenshots never read into context — fix goes into the review prompt's instructions, not .mcp.json.)*

---

## Idea 10 — Presence, proof, and the KPI scoreboard

**Hook.** The lesson ends by grading itself. One prompt shipped a real feature — and the scoreboard still shows dents. That honesty is the point: the KPIs tell you where your agentic layer needs work, not how to feel.

**Picture.** Designed scoreboard (no frame — 54:55–56:10 is talking head): Attempts 1→2 (the patch). Size: solid (two endpoints, two UI surfaces, tests, plan, docs — "a couple of prompts, we have 900 lines of code of engineering work"). Streak: broken, reset to 1 (two ADWs for one feature). Presence: ~3 (prompt input; spotting the issue in the review images; patch + re-check) vs the ideal 2 — "one at the beginning for your prompt input, one at the end for your review and your PR merge."

**Worked example.** What made presence cheap even when needed: the review system carried proof to *you* — "we were able to quickly identify this issue thanks to our review images and just patch it." Generalization for non-UI folks, kept explicit: scikit classifiers, data analytics, rapid prototypes — "whatever you would do to review that the thing is what you asked for... this is what you're going to embed into your review step," and it should yield a *hard asset*, ideally "a live asset" (report, image, video).

**Dan's term.** *Agentic proof of value*; *review velocity*; *live asset*. Plus the bridge out: lesson 7 reveals "the secret of Tactical Agentic Coding... hiding in plain sight throughout TAC," and dangerous-mode ADWs shipping to production — "not for serious work... maybe some bugs, maybe some chores." And the closing order: "do not wait to start putting this stuff in your codebase."

**Failure mode.** Reading KPIs as vanity metrics or, worse, gaming them (never patching so attempts stays 1). The scoreboard is a diagnosis: attempts up → improve the prompt that missed; presence up → move that human moment into a workflow.

**Retrieval Q.** Ideal presence is what number, at which two moments — and what does an attempts increase tell you to do? *(2: prompt input, review/PR merge; improve the workflow/prompt whose miss forced the extra attempt.)*

---

## Timeline map (VTT-verified)

| Time | Beat |
|---|---|
| 0:00–2:10 | Advanced-lesson open: review + document complete the SDLC; fleet-of-agents future; "outperform any cloud-based agentic coding tool" |
| 2:10–3:00 | **SDLC as questions** slide; testing-vs-review distinction; "prove it" |
| 3:00–3:40 | Review velocity; KPIs: attempts down, streak up, size up, presence down |
| 3:40–4:20 | Why document: feedback for future agents inside the agentic layer |
| 4:20–4:55 | **Tactic #6 reveal: One Agent, One Prompt, One Purpose** |
| 4:55–7:10 | Context pollution; god-model critique ("they won't, it's not here"); ADWs = compute added to YOUR developer workflows; steps need different context |
| 7:10–8:30 | Free the window (200K/500K/1M); three constraints (bypass 2/3); model intelligence not a constraint; compact = band-aid |
| 8:30–10:04 | Let your agents focus; minimum context principle; agent's perspective; commit prompts → improve at prompt level |
| 10:04–11:20 | Evals for the agentic layer (deep + passive); "one, one, one" |
| 11:20–12:30 | Clone tac-6; YOLO mode + Opus; `/install` (+ Cloudflare R2 teaser) |
| 12:30–13:40 | New ADWs tour: review/patch/document + composers; standalone UV scripts; ADW ID chains state |
| 13:40–15:30 | adw_review docstring read; fork-your-own-repo note; `/start`; app back up |
| 15:30–16:47 | Issue #14 "One Click Table Exports" (prompt source; high-level drifting mid-level) |
| 16:47–18:40 | Fire `adw_plan_build_review.py … 14`; agents own the repo; `agents/{id}/` + `adw_state.json` |
| 18:40–23:00 | Review deep-dive: R2 uploader; `/review` prompt (variables as IDKs, screenshots, JSON contract); ReviewResult/ReviewIssue types; severity classes; agreeable-agents warning |
| 23:00–27:30 | Resolution: 3-attempt cap; blockers only; `/patch` meta prompt; `create_and_implement_patch`; `/implement` reuse |
| 27:30–31:40 | Progress checks; branch changed under him; `git diff --stat origin/main` (plan + generated e2e test); R2 enabled |
| 31:41–33:30 | **Review lands with images**; the misplaced Export exposed; "our agent did not obey this properly" |
| 33:30–35:20 | Click-through: downloads work, placement wrong; post-mortem part 1: test step skipped |
| 35:20–37:45 | Post-mortem part 2: no vision — screenshots never read; prompt-level fix; `adw_patch` comment → patch run → **"Export is now right next to hide"** |
| 37:45–42:30 | "Why didn't you do it by hand? You're missing the point"; CSV verified; out-loop patching via webhook; commander-of-compute callback |
| 42:30–45:30 | `adw_document.py` on same ADW ID; `app_docs/feature-490eb6b5-…md` + assets; doc template; stale screenshot noted (review not rerun) |
| 45:30–48:00 | **Conditional docs**: agentic update; referenced in bug/chore/feature/patch/prime; "this seals the deal" |
| 48:00–53:30 | Issue/PR recap (~900 lines); agents present proof; blame-my-ADWs posture; non-UI review embodiments; live asset |
| 53:30–57:16 | Toy-example disclaimer; velocity teaser; **secret of TAC** teaser; KPI self-grade (attempts 2, streak reset, presence ~3, ideal 2); dangerous-mode teaser; "do not wait" |

## Terminology glossary (Dan-isms, canonical spellings)

- **One agent, one prompt, one purpose** — Tactic #6; no agent runs more than a single prompt
- **Context pollution / context overloading / toxic context** — degraded focus from an overloaded window
- **Minimum context principle** — context engineer as little as possible; minimum context required to solve the problem
- **Three constraints** — context window; codebase+problem complexity; your abilities (model intelligence deliberately excluded)
- **SDLC as questions** — plan/build/test/review/document ↔ their five questions
- **Review velocity** — how fast a human can say yes/no; raised by proof
- **Severity classes** — `skippable` / `tech_debt` / `blocker` (only blockers block)
- **Patch** — a surgical change class distinct from chore/bug/feature
- **Conditional documentation** — docs indexed by read-me-when conditions; updated by the documenter, read by planners
- **app_docs vs ai_docs** — your codebase's docs vs third-party docs
- **Agentic proof of value / live asset** — hard evidence attached to review (image/video/report)
- **Presence** — human-in-the-loop moments per shipped unit; ideal = 2
- **PITER** — Prompt, Input, Trigger, Environment, Review (TAC-4 framework; transcript mishears as "Peter")
- Transcript corrections: "yellow mode" → YOLO mode, "AWID" → ADW ID, "loop box" → loot box, "Huffactor" → (mishear; he's booting the agent)

## Bridge to the rest of TAC (as trailed in-lesson)

- Lesson 7: **the secret of Tactical Agentic Coding** — "hiding in plain sight throughout TAC," starts small and scales up; plus real shipping velocity on the same agentic layer
- Lesson 7 preview: dangerous-mode ADWs straight to production — for bugs and chores, not "serious work"
- Constant thread made explicit here: the value isn't any single workflow — "it's the power of combining workflows, having them separate yet working together... isolated... reviewable... improvable"
- Standing order: "do not wait to start putting this stuff in your codebase. Set up basic ADWs, set up basic agentic prompts... the value here is immense"

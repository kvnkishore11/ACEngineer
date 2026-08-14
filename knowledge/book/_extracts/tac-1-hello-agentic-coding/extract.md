# TAC-1 · Hello Agentic Coding — Master Teaching Notes

> Source of truth for the expanded chapter. Video 21:51 · Beginner · Tactic #1: **Stop Coding**
> Lesson artifact: a 35-line README, one settings file, and three ~20-line launcher scripts. That's the whole codebase, on purpose.

**Lesson thesis in one sentence:** AI coding (generating code from prompts) was phase one; agentic coding — prompts that reliably execute long chains of tools inside a programmable agent — is phase two, and the engineer who commands it becomes irreplaceable by replacing themselves.

**The chapter must land eight ideas.** Each below follows: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q.

---

## Idea 1 — A new role exists: the Agentic Engineer

**Hook.** In 2023, before it was obvious, Dan bought a domain name as a bet: agenticengineer.com. The bet was that a new software role would emerge, defined not by writing code but by *building systems that can take actions as we can*. Lesson 1 opens by declaring the bet settled: the role now exists, and this course exists to move you into it.

**Picture.** Frame t0078 (1:18): the agenticengineer.com page on screen while Dan narrates the 2023 prediction. Frame t0115 (1:55): the two-phase timeline — Phase 1 "AI CODING" (vibe coders born, code commoditized) flowing into Phase 2 "AGENTIC CODING" (real engineers strike back).

**Worked example.** The entire lesson repo *is* the role in miniature: nothing in `tac/tac-1` is application code. It's a README of prompts, a permissions file, and launchers — artifacts of someone who directs systems rather than types programs.

**Dan's term.** *Phase two Agentic Engineer.* Also the era framing: *"In the generative AI age, AI coding was phase one... Agentic coding marks phase two. This is where real engineers strike back."*

**Failure mode.** Hearing "new role" as a title change rather than a job change. The weak student keeps doing phase-1 work (prompt → code → paste) with a new label. The role's actual definition — building systems that take actions — is testable: if nothing runs without you pressing the keys, you're still phase one.

**Retrieval Q.** What defines the agentic engineer role, in Dan's 2023 prediction wording? *(Building systems that can take actions as we can.)*

---

## Idea 2 — The mission: become the engineer they can't replace

**Hook.** "You know who *they* are. It's your boss. It's the company. It's the industry. It's AI." Nothing in tech is forever — and in a world where your grandma or your little brother can build an app with one prompt, what exactly makes *you* hard to replace?

**Picture.** Frame t0124 (2:04): the mission slide. Frame t0162 (2:42): the full-screen **COMMANDER OF COMPUTE** title card — the answer to the question the mission poses.

**Worked example.** The answer performed, not stated: by lesson end, a Python script (`programmable/programmable.py`) does a complete branch-write-run-commit-report cycle while the engineer watches. The engineer's contribution moved up one level: they wrote the prompt and the trigger, not the code.

**Dan's term.** *Commander of compute* — "We do what we always do in technological revolutions. We move up the stack once again." And the strategy: *build systems that build systems*. The economics: the fabled *10x engineer* comes from 10x **leverage**, never 10x time — and the number is arbitrary (2x, 100x) depending on the leverage points you find. Also the end-state: codebases as *self-operating machines* that "literally run themselves."

**Failure mode.** Treating the mission as motivational garnish and skipping to the demo. The mission is load-bearing: every later tactic is justified by "does this increase your leverage per unit of attention?" Students who skip it evaluate tactics by comfort instead.

**Retrieval Q.** Who are "they" in "an engineer they can't replace," and what is the one-word strategy for becoming that engineer? *(Boss, company, industry, AI; leverage — commanding compute to build systems that build systems.)*

---

## Idea 3 — Tactic #1: Stop Coding

**Hook.** The first tactic is dead simple, mission critical, and potentially uncomfortable. Dan says it twice for complete clarity: **Stop coding.** Your hands and your mind are no longer the best tool for the job of writing code. Full stop. This from a man who spent a decade-plus hand-coding at startups and large companies and admits he misses it.

**Picture.** Frame t0414 (6:54): the Tactic #1 reveal. The chapter's headline image.

**Worked example.** Negative space in the codebase: `tac/tac-1` contains zero hand-written application code, and the course promise is that *throughout all of TAC, not a single line of code gets typed*. `main_aic.py` and `main_tac.py` exist only after an agent creates them.

**Dan's term.** *Stop coding.* The supporting cast: "powerful language models [in] agentic loops running on powerful supercomputers are now vastly superior coders than you and I are"; "you're an engineer, not a coder — the difference is massive"; and the reallocation target — *planning, reviewing, and creating closed-loop structures*.

**Failure mode.** Two opposite misreadings, both fatal. (a) "No more code" — wrong: code is still a primary asset that generates features and products; you'll generate more than ever. (b) "No more understanding code" — wrong: code understanding remains critically important; review is where your cycles go. And the behavioral failure: agreeing in theory, then hand-editing the agent's output at the first imperfection instead of re-prompting — which trains you to distrust the loop and forfeits the tactic entirely.

**Retrieval Q.** Name the two things "stop coding" does NOT mean, and where the freed cycles go. *(Doesn't mean stop generating code or stop understanding it; cycles go to planning, reviewing, closed-loop structures.)*

---

## Idea 4 — Big Three → Core Four: the one-dimension delta

**Hook.** Everything that changed between phase one and phase two is a single added dimension. You already know it — it's been hiding in plain sight, getting more capable over time.

**Picture.** Frame t0845 (14:05): the Core Four Venn diagram — CONTEXT (blue), TOOLS (yellow), MODEL (red), PROMPT (green), overlapping over a dimmed view of the lesson README. The one diagram to memorize from lesson 1.

**Worked example.** `.claude/settings.json` is the "tools" circle made concrete — the exact tool surface the demo runs on: `Read`, `Write`, `Edit`, `Bash(uv run:*)`, `Bash(git checkout:*)`, `Bash(git branch:*)`, `Bash(git add:*)`, `Bash(git commit:*)`, `WebSearch`. Read it and you can predict everything the agentic prompt is able to do — and everything it isn't.

**Dan's term.** *The big three* (context, model, prompt — "always there even if you can't see it") upgraded by tools to *the core four*. Precise wording matters: the new element is *"prompts that can reliably execute long chains of tools."* And the pre-emptive rebuttal to "tool calling isn't new": *"It's not a question of new. It's a question of scale and performance."*

**Failure mode.** Shrugging "big whoop, who cares — prompts call tools now" (Dan names this exact shrug). The weak student files the core four as vocabulary instead of as a diagnostic: when an agentic run goes wrong, the cause is always one of the four — wrong context, wrong model, wrong prompt, or wrong/missing tools. Students who internalize it debug systematically; students who don't just re-roll the prompt.

**Retrieval Q.** What upgrades the big three to the core four — exact phrasing — and what is Dan's answer to "tool calling isn't new"? *(Prompts that reliably execute long chains of tools; it's not a question of new but of scale and performance.)*

---

## Idea 5 — Two prompts, one README: AI coding vs agentic coding

**Hook.** The lesson's centerpiece is an A/B test you run on your own machine. Same repo, same agent, same afternoon — two prompts. One generates a file. The other does engineering. The difference between them, Dan insists, is *monumental*.

**Picture.** Before/after pair: frame t0700 (11:40) — the AI coding prompt creating `main_aic.py`, nothing you haven't seen a million times; frame t0748 (12:28) — Claude Code converting the agentic prompt into a todo checklist; frame t0790 (13:10) — the full trace: `git checkout -b demo-agentic-coding`, `Write(main_tac.py)`, both `uv run` outputs, `git add`, `git commit`, todos checked off.

**Worked example.** From `README.md` (35 lines — Dan's count is exact):

- **AI Coding Prompt:** `CREATE main_aic.py: print goodbye ai coding` → one file, one print. Phase 1: code generation, full stop.
- **Agentic Coding Prompt:** `RUN:` checkout new/existing `demo-agentic-coding` branch → `CREATE main_tac.py:` print "hello agentic coding" + a concise definition of AI agents → `RUN:` `uv run main_aic.py`, `uv run main_tac.py`, `git add .`, `git commit -m "Demo agentic coding capabilities"` → the agent plans, executes step by step, cleans up its todos, reports what it did.

Note the prompt's *shape*: RUN/CREATE/RUN reads like a runbook. The prompt is a workflow specification, and the verbs are tool calls.

**Dan's term.** *The Agentic (Coding) Prompt* — "a prompt contains a sequence of tool calls." And the observation that unlocks it: "Claude Code is not just writing code. It's calling tools. It's doing engineering work."

**Failure mode.** Concluding the prompts are equivalent "because both made files appear." The tell that a student missed the lesson: they can't list what the second prompt did that the first didn't (branch, execute, commit, report). Secondary failure: not rerunning the demo after deleting the branch, so they never see that the workflow is *reproducible* — the property everything in later lessons depends on.

**Retrieval Q.** List everything the agentic prompt did that the AI coding prompt didn't. *(Branch checkout, second file creation per spec, running both programs, git add + commit, todo management + report.)*

---

## Idea 6 — Why Claude Code: the three essential elements

**Hook.** If prompts could always call tools, why did agentic coding only now become real? Because the tools changed and the models improved — and one tool combined the ingredients properly first. There's a new form factor of engineering to take into account.

**Picture.** Frame t0903 (15:03): the three-elements slide. Frame t0608 (10:08): the humble on-ramp — VS Code, Cmd+J, `claude`, boot screen.

**Worked example.** The demo itself is the evidence: a 12-line prompt produced a plan, five tool executions in the right order with correct recovery of context between them, and a report — with zero baby-sitting. That reliability across a *long chain* is the differentiator the slide names.

**Dan's term.** The *three essential elements*: (1) a powerful language model that can reason when needed; (2) the ability to consistently call long chains of tools; (3) the right agent architecture. Result: "Reliable agentic coding at scale was not possible before Claude Code." Positioning: "Just as Aider was for the AI coding phase one era, Claude Code represents the best phase two agentic coding tool" — being copied by every other tool. Economics stated plainly: millions and millions of tokens; have the funds or the plan; *pay to play* for maximum ROI. And the anti-lock-in clause: tactics are *transferable* — "don't get stuck on any one tool."

**Failure mode.** Tool fixation in either direction: (a) treating the lesson as expired because the UI/models changed — Dan pre-handles this on camera ("your Claude Code UI might look different... that's all great"); (b) fanboy-ing the tool and missing that the three elements are a *checklist for evaluating any agentic tool*, which is the transferable part.

**Retrieval Q.** Name Claude Code's three essential elements and the claim they justify. *(Reasoning model + consistent long tool chains + right agent architecture; reliable agentic coding at scale wasn't possible before it.)*

---

## Idea 7 — Programmable agentic coding: the agent as a function call

**Hook.** The lesson's biggest unlock is almost a throwaway line: Claude Code runs in the terminal. Which means any programming language with terminal access can *call it*. Which means the agent is no longer an app you sit in front of — it's a component you build with.

**Picture.** Frame t1063 (17:43): the `programmable/` directory — three launchers + `prompt.md`. Frame t1105 (18:25): `programmable.py` on screen, ~30 lines. Frame t1205 (20:05): the headless run's final REPORT in the terminal. Frame t1000 (16:40): the README-35-lines shot that frames this whole section.

**Worked example.** All three launchers are the same five steps in different costumes — read `programmable/prompt.md`, pass it to `claude -p`, capture output, print it, propagate errors:

- `programmable.sh` — `PROMPT_CONTENT="$(cat programmable/prompt.md)"; OUTPUT="$(claude -p "$PROMPT_CONTENT")"; echo "$OUTPUT"` (3 lines; the pattern with nothing else)
- `programmable.py` — `subprocess.run(["claude", "-p", prompt_content], capture_output=True, text=True)`, print stdout/stderr, `sys.exit(returncode)` (the variant Dan runs; the most production-shaped: error handling + exit-code propagation)
- `programmable.ts` — Bun: `await $\`claude -p ${promptContent}\`.text()` then log (proves language choice is irrelevant)

`prompt.md` itself is a *superset* of the README demo and self-contained: it creates BOTH `main_aic.py` and `main_tac.py` (no dependency on a prior interactive run), and adds a fourth block the README prompt lacks — `REPORT: respond with the exact output of both .py files`. That REPORT block is the seed of every report-back/verification pattern in later AI developer workflows: headless runs must *tell you what happened*.

Demo order matters and is worth reproducing exactly: delete the branch from the interactive run first (`git branch -D demo-agentic-coding`), then `uv run python programmable/programmable.py` from `main` — and watch the whole workflow re-materialize without you.

**Dan's term.** *Programmable agentic coding* / a *programmable agentic coding tool*. Why it matters: "we can embed our own agents, our own workflows, our own agentic prompts across the software development lifecycle" — across all developer environments, "including full agentic environments where we're not even present," with *agentic triggers* (a later-course topic) deciding when they fire. "It's not just about the agentic prompt. It's about **where** we can use the agentic prompt."

**Failure mode.** Watching instead of running — the scripts look too trivial to bother with, so the student never feels the qualitative difference between *chatting with* an agent and *invoking* one. Second failure: missing that `prompt.md` ≠ the README prompt (the superset + REPORT differences are exactly the parts that make headless runs viable). Third: not realizing `.env.sample` (`ANTHROPIC_API_KEY=`) marks the API-billing path that headless/CI usage implies.

**Retrieval Q.** What one property of Claude Code makes it programmable, and what does prompt.md's REPORT block demand? *(It runs in the terminal, so any language with terminal access can invoke `claude -p`; REPORT demands the exact output of both .py files.)*

---

## Idea 8 — The contradicting truth: replace yourself

**Hook.** The lesson ends on a paradox sharp enough to be the course's motto: *to become an irreplaceable engineer, you will replace yourself.* The engineer who automates their own work owns the automation — and no vibe coder will replicate what that engineer can do.

**Picture.** t1250 (20:50) is B-roll (hands typing) — render this beat as a designed pull-quote, not a frame (`diagram_instead: true` in the frame plan).

**Worked example.** Lesson 1's arc in miniature already performed it: the engineer ran a prompt interactively (doing the work), then scripted the same prompt (`programmable/*`), making themselves unnecessary for that workflow — permanently. Multiply by every workflow you own: that's the course.

**Dan's term.** *The contradicting truth.* Supporting frame: evolution — "Evolution forces us to leave skills behind to adapt new ones and bet on potential futures. But in the tech industry, this is where all the alpha lies... your asymmetric engineering advantage exists... in the future." Teaser for lesson 2: leverage points such that *10 minutes of your work equals 60+ minutes of another engineer's*.

**Failure mode.** Reading the paradox as job-loss fatalism (and disengaging) instead of as the leverage strategy it is. The resolution the student must be able to articulate: what gets replaced is your *typing*; what becomes irreplaceable is your *judgment about what to build and your ownership of the systems that build it*.

**Retrieval Q.** State the contradicting truth and resolve it in one sentence. *(To become irreplaceable you'll replace yourself — you automate your current work, and the irreplaceable part becomes your command of the systems doing it.)*

---

## Timeline map (VTT-verified)

| Time | Beat |
|---|---|
| 0:13–1:01 | Cold open: AI coding is not enough; lesson goal |
| 1:01–1:57 | 2023 domain-name bet; phase 1 vs phase 2 |
| 1:57–3:14 | Mission (irreplaceable); commander of compute; systems that build systems; engineering ≠ writing code |
| 3:14–4:56 | Course structure: 8 lessons, 8 tactics; loot box; per-lesson codebases; ambition ("land on Mars or the moon") |
| 4:56–6:47 | What winning means: 10x by leverage; 80% of life is noise; self-operating machines |
| 6:47–9:06 | **Tactic #1: Stop coding** (said twice); vastly-superior-coders claim; engineer-not-coder; what still matters (planning, reviewing, closed loops) |
| 9:06–10:00 | Essential tools; fresh dir; clone tac-1; VS Code; Cmd+J; `claude` |
| 10:00–11:18 | Claude Code as primary tool; token economics; Aider analogy; tools-will-change disclaimer; repo tour; check `.claude/settings.json` |
| 11:18–12:03 | AI coding prompt run → `main_aic.py`. "Nothing new." |
| 12:03–13:23 | Agentic coding prompt run → checklist → branch, file, runs, commit, report. "This is agentic coding." |
| 13:23–14:31 | Big three → core four; "reliably execute long chains of tools"; scale-and-performance rebuttal |
| 14:31–16:40 | Claude Code's three essential elements; long-running AI developer workflows (minutes to hours); "35 lines" |
| 16:40–19:00 | Programmable: `claude -p` from sh/ts/py; branch cleanup; headless rerun; embed across the SDLC |
| 19:00–20:21 | Terminal ubiquity; agentic environments without you; agentic triggers teaser; REPORT output lands |
| 20:21–21:52 | Recap; contradicting truth; evolution/alpha; lesson-2 teaser (leverage points); sign-off |

## Terminology glossary (Dan-isms, canonical spellings)

- **TAC** — Tactical Agentic Coding (8 lessons, 8 tactics, one codebase each; per-lesson **loot box** of prompts/links/assets under the video)
- **Big Three** — context, model, prompt (phase-1 primitives)
- **Core Four** — big three + tools (phase-2 primitives)
- **Agentic (coding) prompt** — a prompt containing a sequence of reliably-executed tool calls
- **Commander of compute** — the phase-2 engineer identity
- **Systems that build systems** — what commanders build; ADW seed
- **Self-operating machine** — the end-state codebase
- **Loot box** — per-lesson unlockable assets (transcript mishears as "loop box")
- Transcript corrections: "Cloud Code"→Claude Code, "ADER"→Aider, "Bunn"→Bun, "Identic Prompt"→Agentic Prompt

## Bridge to the rest of TAC (as trailed in-lesson)

- Lesson 2: leverage points (10 min of yours = 60+ of another engineer's)
- Later lessons: closed-loop structures; agentic triggers; scaling the agentic prompt "to the max" across the SDLC
- Constant thread: every lesson = one tactic + one codebase; the tactic is the thing to master

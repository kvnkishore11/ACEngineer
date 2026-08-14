# TAC-8 Nuggets — ranked for the struggling learner

This is the final lesson; it compresses the whole course. Ordering rule: how much of *your practice* collapses if this nugget is missing. Tier 1 is the spine — get these and you can rebuild the rest. Tier 2 is the machinery you actually operate. Tier 3 is the framing that keeps you allocating your time correctly after the course ends.

---

## Tier 1 — If you remember nothing else

**1. Your codebase has two layers, and at least half your time goes to the second.**
The **application layer** is everything classical — app, database, infra, DevOps. The **agentic layer** is the ring wrapped around it: prompts, template meta prompts, and ADWs that operate the app for you. Tactic #8 is *Prioritize Agentics*: ≥50% of engineering time on the ring (more when bootstrapping).
*Say it Dan's way:* "As a good starting point… at least half your engineering time should be spent on the new agentic layer."
*Why weak learners lose it:* they nod at the ratio, then spend 100% of the week in the app layer "for the deadline" — and never build the layer that would have hit the next ten deadlines. The tactic is a **time-allocation change, not a belief.**

**2. One question compresses all eight tactics. Ask it daily.**
*"Am I working on the agentic layer or am I working in the application layer?"* Every KPI, every leverage point, all eight tactics fold into this. There are exactly **three** acceptable reasons to answer "application layer": a deadline, testing something by hand, or running your prompts in-loop to verify they'll work out-loop. Anything else and "you're going sideways while other engineers move up."
*Say it Dan's way:* "Even if you forget all eight tactics, this is all you need to think about."
*Why weak learners lose it:* they answer it once, at course end, instead of "every day when you sit down to work."

**3. The smallest real agentic layer is three directories.**
The **Minimum Viable Agentic Layer**: `.claude/commands/` (prompts) + `specs/` (plans) + `adws/` (workflows). Not a framework, not a platform. The single rule: "you can compose code and reference other files and have this be isolated from your application layer." Scripting language is free choice (UV Python, Bun TS, shell).
*Why weak learners lose it:* they cargo-cult the *scaled* tree (hooks, triggers, state, worktrees, observability) on day one. Thin ring first; the scaled tree is where you END after value compounds.

**4. The most leveraged file isn't code — it's a prompt that writes prompts.**
A **template meta prompt** (like `chore.md`) generates a *plan* in a rigid format that encodes your engineering standards. The load-bearing section is the **Plan Format**: metadata, relevant files, **step-by-step tasks**, and **validation commands** — the plan ends by checking itself. `/implement` is a *higher-order prompt*: it takes that plan as its argument.
*Say it Dan's way:* "These are meta prompts… this is a prompt that generates a prompt."
*Why weak learners lose it:* they write prompts so specific they solve today's task once. Target the **problem class**, not the instance (nugget 10).

---

## Tier 2 — The working machinery

**5. One script is categorically different from all your others: the gateway.**
`adw_prompt.py` doesn't compute a result — it hires an intelligence and files a report. It builds `claude -p "<prompt>" --output-format stream-json --model … --dangerously-skip-permissions`, manages a unique `adw_id` and retries, and lands four files under `agents/{adw_id}/{agent}/`: the JSONL stream → JSON array → **final object** → your custom summary.
*Say it Dan's way:* "This script is the gateway into agentic coding… this ADW is calling an agent. This is distinctly different from any other type of code."
*Why weak learners lose it:* they skip the output tour. If you can't say what's in `cc_final_object.json` vs the summary, every later system (task boards, Notion factory, AEA) feels like magic instead of engineering.

**6. A composed ADW is two prompts and forty lines of glue — and the glue is where the guarantees live.**
`adw_chore_implement.py`: Phase 1 runs `/chore` as agent **planner**; the script **regex-extracts** the plan path from the agent's report; Phase 2 feeds that path to `/implement` as agent **builder**. It works ONLY because `/chore`'s Report section is a machine-parseable **contract** ("Return the path to the plan file created").
*Why weak learners lose it:* they think the halves are independent. Change `/chore`'s Report format and the regex breaks — deterministic code and non-deterministic prompt are **coupled by an explicit contract.**

**7. A multi-agent system can live in a single markdown file.**
app2's **Todone**: `tasks.md` + a 5-second cron loop runs seven agents in parallel. The state machine: `[]` → `[🟡, adw_id]` → `[✅ commit_hash, adw_id]` | `[❌, adw_id] // Failed: reason`; `[⏰]` is eligible only when every task above it is `✅` (a `❌` above blocks forever). Tags configure per task: `{opus}` upgrades the model, `{adw_plan_implement_update_task}` upgrades the workflow.
*Say it Dan's way:* "I'm not doing this, by the way."
*Why weak learners lose it:* they write one giant task and never touch tags or `⏰` — a to-do list with extra steps, not an orchestrator with dependencies, model routing, and workflow routing.

**8. Triggers are how you stay OUT of the loop.**
A trigger fires ADWs without you: a cron over `tasks.md`, a 15s Notion poller, a webhook, the AEA server. Map **PITER** onto any out-loop system: **P**rompt input (a Notion card), **T**rigger (the poll), **E**nvironment (`trees/` worktrees), **R**eview (board columns + live status). The claim trick that prevents double-pickup: flip status to *In progress* + `adw_id` the instant a task is grabbed.
*Why weak learners lose it:* they treat the Review column as bureaucracy. HIL Review + `continue - <prompt>` IS the steering loop — skip it and out-loop becomes fire-and-forget, i.e. fire-and-regret at scale.

**9. One agent, one prompt, one purpose — broken exactly once, on purpose.**
Focused agents mean focused, reproducible, testable context windows. The single sanctioned exception is app5's **AEA** (Agent Embedded Application): a product chat agent that persists `cc_session_id` in SQLite and passes it back with `--resume`, because conversation needs continuity across prompts, refreshes, and restarts. "Outside the loop is inside the application."
*Say it Dan's way:* "The power of agents isn't in one, it's in many."
*Why weak learners lose it:* two symmetric failures — treating the rule as optional (sprawling mega-agents you can't reproduce or test) OR treating it as absolute (refusing session continuity where the use case demands it).

**10. Solve problem classes, not one-off fixes.**
The unit of agentic-layer work is a *class* of problems. When one concise prompt produces an entire working MCP server, Dan declares the class closed.
*Say it Dan's way:* "I have solved the problem class of building Astral UV model context protocol servers. I've solved it. It's done."
*Test:* if your template can't absorb a request you didn't anticipate, you templated an **instance**, not a class.

**11. Always add feedback loops — that's what lets you drop the R.**
Every Plan Format ends in **validation commands**: the plan checks itself. Zero-touch engineering (ZTE) is when a dialed-in ADW is reliable enough that "the time you spend reviewing the work will be useless… you realize you're the bottleneck." Then **PITER → PITE**: drop the R.
*Say it Dan's way:* "You'll drop the R off… you will let your product ship itself."
*Why weak learners lose it:* they delete review before encoding it. The R is **replaced** by encoded feedback loops, never merely removed — PITE without validation is unsupervised risk.

---

## Tier 3 — Framing that keeps you allocating correctly

**12. The app layer is a great place to start and a terrible place to stay.**
Building the agentic layer is **parabolic**: "put 10 minutes in, get two hours of value out or more." Deep application work feels productive, which is exactly the trap.
*Say it Dan's way:* "It's a great place to do deep work… It's a terrible place to stay. So many engineers are going to miss this mark."

**13. Don't think you're smarter than your own templated practices.**
Once your team's best engineering is encoded into a template meta prompt running in an ADW that kicks off five-to-ten agents per problem, you cannot out-execute it by hand.
*Say it Dan's way:* "Don't make the mistake of thinking you can outperform your team's best engineering practices encoded into a template metaprompt… your place of competition is now net-new innovation."
*Why weak learners lose it:* ego. They keep hand-fixing "just this one" and quietly opt out of the compounding system.

**14. Implementation is becoming a commodity; your value moved up the stack.**
"Not only is code a commodity, but the implementation as well." Value now lives in system design, domain encoding, quality control, and creative problem decomposition — "which you'll then encode in your ADWs." An agentic engineer "operates on living pieces of software that work while they sleep."

**15. This is a ring you thicken daily — you're orchestrating intelligence now.**
Picture the ring: thin at first, thicker every time you template a workflow, until machines that carry your judgment ship your way autonomously. That's the whole arc.
*Say it Dan's way:* "When the agents arrived, something changed. We weren't just AI coding anymore. We started orchestrating intelligence."

---

## Micro-quiz (close the book first)

1. Name the two layers. What time split does Tactic #8 prescribe, and what does Dan say it compresses?
2. State the guiding question and its **three** acceptable reasons to be in the application layer.
3. What are the MVAL's three pieces, and the single rule for the scripting layer?
4. What makes a *template meta prompt* different from a good prompt, and which two Plan-Format sections make it self-verifying?
5. Trace the plan path through `adw_chore_implement.py`. Why would editing `/chore`'s Report section break it?
6. Give the full `tasks.md` state machine including the blocking rule, and say what `{opus}` and `{adw_plan_implement_update_task}` each do.
7. State the one-agent rule, why it exists, and the single exception with its mechanism.
8. What has to be true before you convert PITER → PITE?

*(Answers: extract.md Ideas 1/10, 10, 3, 5, 6, 7, 9, 10 — and this file's nuggets 1, 2, 3, 4, 6, 7, 9, 11.)*

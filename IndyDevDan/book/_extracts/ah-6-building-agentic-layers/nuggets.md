# AH-6 Nuggets — ranked for the struggling learner

Ordering rule: how much of the lesson collapses if this nugget is missing. Tier 1 is the load-bearing frame; Tier 2 is the working machinery of the ladder; Tier 3 is the framing that keeps you honest and moving. This is the **capstone** — several nuggets are callbacks to earlier lessons, now assembled.

---

## Tier 1 — If you remember nothing else

**1. Your codebase now has two layers, and one of them is the whole game.**
The **application layer** is the code that serves users. The **agentic layer** is the new ring around it where agents operate that code on your behalf. Building and leveling the agentic layer is the **highest-ROI action** for any engineer in the age of agents. If you only draw one picture, draw the green ring around the dark square.
*Why weak learners lose it:* they think the agentic layer is "just my `.claude` folder." It's a graded, specialized system you invest in like a product.

**2. The agentic layer has a ruler: three Classes, each with Grades.**
**Class 1 = in-loop** (primitives you run in the terminal), **Class 2 = out-loop** (agents run without you), **Class 3 = orchestrated** (an orchestrator agent runs teams of agents). Grades 1..N measure power inside each class. Everything **stacks**. You (a) find your class+grade, (b) raise your grade, (c) jump classes.
*Test yourself:* say your own codebase's class and grade out loud. If you can't, re-read the ladder.

**3. The Class-1 build order is seven concrete steps.**
prime + memory → sub-agents → **custom tools** → **closed loops** → **templates** → **prompt chains** → **agent experts**. That's Grade 1 to Grade 7. This is a checklist for a brand-new codebase, not vague advice.

**4. The destination is the codebase singularity — and it's a target, not a fear.**
"My agents can now run my codebase better than I can. I trust them to ship more than I trust myself or my team." Dan: *"This is not something to fear, it's something to run toward."* Zero-touch engineering (Tactic 7) is the road; the singularity is the town at the end of it.

**5. The meta-tactic that contains everything: Prioritize Agentics.**
"Build the system that builds the system. Prioritize your agentic layer." Every other tactic (stop coding, template, stay out the loop, feedback loops, one-agent-one-purpose, zero-touch) is a way of doing this one.

---

## Tier 2 — The working machinery of the ladder

**6. Grade 3 is where most engineers secretly stall: custom tools.**
Skills, MCP servers, and prime-with-tools all give the same thing — custom tools that enhance the core four. **And skills/MCPs can both be replaced by a well-written prompt** (teach the agent to run PSQL directly; skip the token-heavy MCP). The trap: too many bad tools that burn tokens and don't scale. "Learn to give your agents just what the agent needs."

**7. Grade 4 = feedback loops, and "more compute should mean more trust."**
Closed-loop prompts (request → validate → resolve) let agents review and fix their own work. `review.md` writes a risk-tiered PASS/FAIL report to `app_review/`; `fix.md` resolves it. If adding compute makes you trust the result *less*, you built the loop wrong.

**8. Grade 5 = templates, not plans. This is where you teach agents to build like YOU.**
A bug template ≠ a feature template ≠ a chore template. Each has a required output format with validation baked in. Many engineers write templates without realizing it; do it on purpose. In the repo this lives inside `plan.md`'s `task_type (chore|feature|refactor|fix|enhancement)` switch.

**9. Grade 6 rule: never build a chain you can't run in pieces.**
Plan-then-build, scout-then-plan. But *always* keep `/plan`, `/build`, `/review` runnable individually. "If you can't run the individual pieces, at some point something will go wrong and you will not be able to isolate the one thing that went wrong" — and you can't scale pieces into parallel sub-agents.

**10. Grade 7 = agent experts, and `expertise.yaml` is a mental model, NOT a source of truth.**
An expert keeps working memory of a domain and *validates it against the code* (the code is truth). ACT→LEARN→REUSE: `plan.md` (act), `self-improve.md` (learn — diff expertise vs code, cap the line count), `question.md` (reuse — answer with file/line cites). This is where agents start solving problems end to end without you.

**11. The AI Developer Workflow is the highest leverage point: deterministic code + non-deterministic agents.**
Raw agents are unreliable; raw code is inflexible; combined they're unstoppable. Python owns step order, logging, validation, retries, DB writes; the agent owns reasoning. `adw_plan_build.py` = 2 steps: `/plan` then `/build`. This is what your prompt chains *become*.

**12. The orchestrator has 10 tools — and 2 of them are the bridge to Class 2.**
8 agent-management tools (create/list/command/check/delete/interrupt agent, read logs, report cost) **+ `start_adw` + `check_adw`**. `start_adw` is how a Class-3 orchestrator fires a Class-2 ADW: it's an MCP tool call (not a magic "start adw:" chat string) that writes a DB row and spawns a detached `uv run adw_<type>.py --adw-id` process.

**13. The two class-jumps are the hard, meaningful transitions.**
Class 1 → 2 = **get out of the loop** (stop babysitting small chores/bugs in the terminal). Class 2 → 3 = **add an orchestrator** that commands teams. Grades raise power; jumps change *the kind* of agentic coding you do.

---

## Tier 3 — Framing that keeps you honest and moving

**14. Specialize. Do NOT build a generic, reusable agentic layer.**
The single most-repeated warning. "Your agentic layer should be specialized to fit and wrap your codebase… build to win for the use cases you care about." Reuse is not the goal; winning one codebase is.

**15. Bundle related apps under one `apps/` directory (git submodules).**
So one team of agents can see the whole product — DB, front/back end, DevOps, notebooks. "You want them to be able to see everything and have it all co-located in a single place." If agents don't need to see multiple repos, it's fine to duplicate and specialize a separate layer.

**16. Everything reduces to the core four; the form factor doesn't matter.**
Prompt, sub-agent, skill, prompt chain, ADW, orchestrator — all resolve to context/model/prompt/tools. "It doesn't matter what it's called… everything eventually becomes a core four." Pick whatever form maximizes compute advantage.

**17. Don't start at Class 3.**
"We don't start with powerful orchestration systems. We start with nothing." Sprinting to the orchestrator without the lower rungs gives you an unmaintainable, unobservable mess. Locate yourself honestly first.

**18. Right-size the model per agent (a live AH-3 callback).**
In the repo: scout-fast = **Haiku**, docs-scraper = **Sonnet**, heavy build/plan/review = **Opus**. Match the model to the task; don't put Opus on a trivial transform.

---

## 60-second self-quiz

1. Name the three classes and their unique elements. *(in-loop primitives / out-loop system / orchestrator agent)*
2. Recite the seven Class-1 grades in order.
3. What single element separates Class 2 Grade 1 from Grade 2? *(the full ADW)*
4. Why is the ADW the "highest leverage point"? *(deterministic code + non-deterministic agents)*
5. What exact tool does the orchestrator call to run an ADW? *(`start_adw`)*
6. Is `expertise.yaml` a source of truth? *(No — the code is; it's a mental model.)*
7. What's the one warning Dan repeats most? *(specialize, don't genericize)*
8. What's Tactic 08? *(Prioritize agentics — build the system that builds the system.)*

If you can answer all eight without notes, you own the capstone.

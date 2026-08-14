# AH-5 "Agent Experts" — master teaching notes

> Lesson 13 of the course, lesson 5 of Agentic Horizon. Runtime 62:29. The self-described "most controversial lesson of Agentic Horizon."
>
> **One line:** stop deploying agents that *execute and forget*; wire them into an **Act → Learn → Reuse** loop over a self-maintained **expertise file** (a mental model) so each useful action becomes reusable expertise — with no human in the loop.

Each major idea below follows the same weak-student scaffold: **Hook → Picture → Worked example → Name it (Dan's words) → Failure mode → Retrieval.** Quotes are VTT-verified; timestamps are ±3s.

---

## Idea 1 — The problem is structural: agents forget

**Hook.** You already know agents are forgetful. What you may not have named is *why it's fatal*: normal software gets **better** the more it's used (analytics, usage data, patterns → algorithms). Your agents get exactly as good on run #1000 as on run #1.

**Picture.** Two staircases. Traditional software climbs with usage. Agents flatline — every session starts at the bottom.

**Worked example.** No matter how good your context engineering or agentic prompt engineering gets, a fresh agent pointed at your billing code re-derives the same understanding from scratch, every time, and throws it away when the session ends.

**Name it.** *"Your agents forget. And that means your agents don't learn."* (0:53) The existing tools don't close the gap: **memory files** are global forced context that always loads (and expertise needs to break rules when the time is right) and must be updated by hand; **prime prompts, sub-agents, skills** are powerful but also hand-updated.

**Failure mode.** Believing a bigger context window or a cleverer prompt eventually fixes forgetting. It can't — forgetting is structural. You need a mechanism that *stores* what was learned.

**Retrieval.** What's the one problem great context/prompt engineering can't solve, and why does it matter more than it sounds?

---

## Idea 2 — The fix is one word: **learns**

**Hook.** The whole difference between a generic agent and an expert fits in a single verb.

**Picture.** Same agent, two wirings. Left: `execute → forget`. Right: `execute → learn → (next time) start smarter`.

**Worked example.** Both experts Dan builds use **no custom tools and no specialized system prompt**. They're ordinary agents — the difference is the loop they're wired into.

**Name it.** *"One executes and forgets, the other executes and learns... You don't need to tell an expert to learn. It's in their DNA."* (2:02) Real experts never stop updating their mental model of the **one** domain that matters most to them.

**Failure mode.** Thinking "expert" means a smarter/bigger model or a longer prompt. It means a persistent, self-maintained mental model plus a loop.

**Retrieval.** Define an agent expert in one sentence without using the words "smart" or "model."

---

## Idea 3 — Expertise is a **mental model**, not a source of truth

**Hook.** The instant you propose an expertise file, a good engineer objects: "great, *another* source of truth to drift — code, comments, PRDs, plans, and now this?"

**Picture.** Your own head. You don't carry a source of truth in there; you carry a fuzzy, self-updating **mental model** you refresh when you dive into an area. The file is the agent's version of that.

**Worked example.** The database expert's `expertise.yaml` says "Postgres + asyncpg, lightweight Pydantic over raw SQL, idempotent migrations, 6 tables." That's an *approximation* — a fast index — that the agent re-checks against the code before trusting it.

**Name it.** *"This is not a source of truth. This is your agent's mental model."* (11:20) And its complement: *"The true source of truth is always the code... Not the comments, not the documentation, not the plans."* (12:38)

**Failure mode.** Two symmetrical errors: (a) distrusting the file as "duplicate docs," or (b) trusting it blindly to save time. Correct stance: it's a mental model the agent **always re-validates against code** (that's why "validate against the codebase" appears *twice* in the question prompt).

**Retrieval.** Is the expertise file a source of truth? What is, and what does the expert do with the file before answering?

---

## Idea 4 — The mechanism: a **self-improving template meta prompt**

**Hook.** Dan gives the whole thing a mouthful of a name, then insists it's simple once you decompose it.

**Picture.** Three Lego bricks snapping together: `[meta prompt] + [template] + [self-improving] = agent expert`.

**Worked example.**
- **Meta prompt** = a prompt that builds other prompts. (`meta_prompt.md` writes new slash commands.)
- **Template** meta prompt = does it with a fixed **purpose and structure**. (TAC-3's leverage point.)
- **Self-improving** = updates an isolated file with new info **for next time**.
- Combine them and you have the formal definition of an agent expert.

**Name it.** *"The agent expert is a concrete form of a self improving template meta prompt... Meta prompts are prompts that build other prompts. Template meta prompts are prompts that build other prompts with a specific purpose and structure."* (3:25–3:39)

**Failure mode.** Hearing "meta prompt" as hype. It's mechanical: a prompt whose **output is another prompt or an updated knowledge file**.

**Retrieval.** Name the three parts of a self-improving template meta prompt.

---

## Idea 5 — Meta-agentics: the building blocks (that act but don't learn)

**Hook.** Before experts, Dan builds the *atoms* — and shows you a trap.

**Picture.** Three factories: prompts building prompts, agents building agents, skills building skills. All three ship a product; none of them get better on their own.

**Worked example (all three demoed live and shipped to the repo):**
- **Meta prompt** → `question-w-mermaid-diagrams.md` (a question prompt that always adds mermaid). *[frame t0456]*
- **Meta agent** → `planner.md` (reads an existing prompt and fires it as a sub-agent via `/plan` — so planning scales to many parallel agents).
- **Meta skill** → `start-orchestrator/SKILL.md` (boots the app's front+back end and opens Chrome). *[frame t0508]*

**Name it.** *"There is no code base I create that does not have meta agentics. Every codebase must have meta agentics."* (7:05)

**Failure mode / the trap.** Concluding these are already experts because they "do work." *"They're acting but... they're not learning at all. Nothing... has updated automatically... therefore these are not Agentic Experts."* (8:36) **Agent experts must learn on their own.**

**Retrieval.** Meta-agentics *act*. Why aren't they experts?

---

## Idea 6 — The pattern: **Act · Learn · Reuse** *(the one to memorize)*

**Hook.** Everything collapses to three steps. *[frame t1305 — the branded Act/Learn/Reuse graphic over a real expert prompt]*

**Picture.** A loop: **Act** (☀ take a useful action) → **Learn** (🧠 store new info) → **Reuse** (🔁 pull from the mental model next time) → back to Act.

**Worked example.** Watch which files supply which step (see Idea 9). The keyword is **useful** — and its honest twin: *"after your thorough search, there may be nothing to be done — this is perfectly acceptable."*

**Name it.** *"Act, learn, reuse. Act. First, our agents take a useful action. The keyword there is useful."* (21:41)

**Failure mode.** Building only Reuse + Learn and expecting compounding gains — without an **Act** step there's no useful action to learn from (that's the "partial expert" trap in Idea 9).

**Retrieval.** Three steps, and the keyword? What's the "perfectly acceptable" outcome of a learn pass?

---

## Idea 7 — The expertise file: anatomy of a mental model

**Hook.** "What's actually *in* one of these?" *[frame t2182 — the 677-line websocket file, collapsed to its spine]*

**Picture.** A YAML outline with exact `file:line` references, e.g. `overview → core_implementation → event_types → streaming_architecture → … → architecture_summary`.

**Worked example.** The database file's `session_state.websocketEventCount` entry (in the websocket file) records `lines: "78"`, `reset_on: connect (line 388), disconnect (line 409)`. Dan notes the database file has *"44 instances of specific line numbers"* — so the agent can jump straight to code and re-validate fast.

**Name it.** *"Give your agents a mental model by giving them an expertise file."* (16:08) Format is your choice — Dan likes YAML but says TOML/JSON/CSV/DB-JSONB all work; pick what's easiest for your agents to read.

**Failure mode.** Letting it grow forever. A hard `MAX_LINES: 1000` lives in the self-improve prompt and the agent enforces it on itself (`wc -l`, then trim least-critical). Dan stays under ~1000 lines.

**Retrieval.** What keeps an expertise file from bloating, and why does it carry exact line numbers?

---

## Idea 8 — The self-improve prompt: the **Learn** mechanism (and the golden rule)

**Hook.** How does a file "improve itself"? It doesn't — a prompt improves it. *[frame t1255 — self-improve.md workflow]*

**Picture.** A closed loop: `(git diff) → read current expertise → validate vs codebase → list discrepancies → update → enforce line limit → validate YAML compiles`.

**Worked example.** Run `/experts:database:self-improve`. The agent burns top-to-bottom, checks line count, compiles the YAML (`python3 -c "import yaml; yaml.safe_load(...)"`), and reports discrepancies — or reports there was nothing to do and stops. Dan seeds **loosely** and lets the agent define its own structure ("it's their mental model, not yours").

**Name it (the golden rule).** *"We're not going to update the expertise file... Teach your agents how to directly update it so they can maintain it."* (37:00) → *"Build the system that builds the system. Do not work on the application layer. You're wasting your time."* (37:10)

**Failure mode.** Hand-editing the expertise file when it's wrong. It feels harmless, but it quietly restores manual memory maintenance — the exact problem experts remove — and never fixes the root cause: the **self-improve prompt**.

**Retrieval.** The mental model is wrong. What do you change, and what do you refuse to touch?

---

## Idea 9 — Partial vs complete expert: the **missing Act step**

**Hook.** Dan shows a *partial* expert first — on purpose.

**Picture.** A checklist per expert: `[Act] [Learn] [Reuse]`.

**Worked example.**
| | Database expert | WebSocket expert |
|---|---|---|
| **Reuse** | `question.md` (read expertise → validate → answer; **read-only**) | `plan.md` / `question.md` |
| **Learn** | `self-improve.md` | `self-improve.md` (run with `true` → reads the git diff) |
| **Act** | ❌ none — no prompt changes code | ✅ `build.md` edits real code |
| **Orchestration** | — | `plan_build_improve.md` chains all three *[frame t1598]* |

The database expert is *"completely acceptable"* — a fine partial. The websocket expert adds the Act step (build a session-based nav-bar WebSocket counter), completing the loop.

**Name it.** *"Now, where's our act step? We don't actually have any action prompts here. Nothing is changing."* (22:20) → the missing act = *"updating any code related to the database."*

**Failure mode.** Assuming an expert must always modify code. Read-only experts (Q&A over a mental model) are legitimate — they just run Reuse + Learn without Act.

**Retrieval.** Which step does the database expert lack, and what supplies it in the websocket expert?

---

## Idea 10 — Context delegation & "more compute = more confidence"

**Hook.** A complete expert runs a lot of tokens. How does the top agent not drown?

**Picture.** A conductor (top agent) firing three fresh musicians (sub-agents), each handed only what they need, handing back only a summary. *[frame t2019 — three Task blocks with token stats]*

**Worked example.** `plan_build_improve.md` spawns three `Task` sub-agents in sequence — **plan (81.8k tokens) → build (61.4k tokens, 41 tool uses) → self-improve** — each starting fresh, so the top agent's context stays protected; it just passes the plan into the builder and the git diff into self-improve. Separately, Dan fires the *same* websocket question at **three** experts to co-locate on the answer; websocket-3 fails — and that's the point.

**Name it.** *"Instead of having one agent answer something for you, have three, have five, have 10... more compute equals more confidence."* (25:00) Ties back to TAC-6: **one agent, one prompt, one purpose** — even inside a scaled workflow.

**Failure mode.** Reading parallel experts as waste. For high-stakes answers, redundancy surfaces evidence a single run misses; you compose the survivors.

**Retrieval.** Why isolate plan/build/self-improve into separate sub-agents? Why fire three experts at one question?

---

## Idea 11 — Product agent experts: per-user mental models + generative UI

**Hook.** Point the same pattern at *users* instead of code and you get a seed of a new product class. *[frames t2545 → t2588, a before/after]*

**Picture.** One expertise file **per user**: `{viewed_products, added_to_cart, checked_out}` → a prompt that streams UI components on the fly.

**Worked example (Nile).** New user, empty expertise → **generic** "Welcome to Nile." Dan searches "Nvidia DGX," adds to cart (an **Act**), returns → the agent **learned** and **reused**: "Welcome back! Based on your interest in AI workstations," streaming a personalized "Complete Your AI Workstation" carousel. The system prompt exposes dynamic vars (checked-out/added/viewed products) and static vars (`SECTIONS_RANGE 4-6`, `PRODUCTS_PER_SECTION_RANGE 6-12`); it's driven by the **Claude Agent SDK** (`agent_expert.py`), and Dan drops Opus→Haiku for speed on camera.

**Name it.** *"when they act, your agent learns, and then it reuses to enhance the experience... This is personalization to the max, especially when you combine that with generative UI."* (42:xx)

**Failure mode.** Mistaking this for a production recommendation engine. Dan is explicit: **it isn't** — agents are too slow for that today; study the *pattern in a UI*, and note the "UI hacks" (loading bars, streamed sections) needed to mask latency.

**Retrieval.** In Nile, what's the per-user mental model, and where do Act/Learn/Reuse show up in the shopping flow?

---

## Idea 12 — When to build an expert (and when NOT to)

**Hook.** The scary insight: build these in your *highest-stakes* code, not your safest.

**Picture.** A 2×2 — risk/complexity vs how-much-it-changes. Experts belong top-right; generic agents belong bottom-left.

**Worked example — build one for:** billing (Dan builds none without an expert; they've *"caught revenue changing details"*), security, the database, DevOps, tricky 3–4-way integrations, ML/data-science, APIs, and **data-types-kept-in-sync** across microservices (a great *first* expert — few files to reference). *"As the complexity, as the size of your codebase grows, the agent expert becomes more valuable."* (56:50)

**Don't build one when:** the problem doesn't evolve; the codebase is simple or brand-new (the model has seen its shape); or **you** don't have a mental model of the area — *"If you don't understand the problem, do not build an Agentic expert... It'll make your problems worse, not better."*

**Failure modes / trade-offs to expect (48:09–53:45):** *seeding* (start blank, let the agent define structure, rerun until it stops finding things), the *"another source of truth"* reflex (it's a mental model — invest in teaching your agents), *finite context* (max-line limit), *false expertise* (agents err like we do — expect it), *too-granular* expertise (a prompt-engineering fix: "prioritize actionable, high-value expertise over verbose documentation"), and *too many experts* (routers/reminders; habit: read the expertise file before working an area).

**Name it (the close).** *"Do you want a generalist working on your codebase that forgets every time they work? Or do you want an expert that remembers and learns from the work done?"* (61:29)

**Retrieval.** Name three build-it domains and one don't-build case. What's the risk of building an expert for a domain you don't understand?

---

## VTT-verified timeline map

| Time | Beat |
|---|---|
| 0:11–3:25 | Controversy framing → the massive problem (forget→don't learn) → generic vs expert → mental model → self-improving template meta prompt (definition) |
| 3:25–5:41 | Definition wrap; experts are "always learning"; lesson roadmap (meta-agentics → codebase experts → product experts) |
| 5:41–8:36 | **Meta-agentics** built + reviewed: meta prompt→question-w-mermaid, meta agent→planner, meta skill→start-orchestrator |
| 8:36–9:00 | They act but don't learn ⇒ not experts |
| 9:32–16:10 | **Database (partial) expert:** experts dir → `/question` reads expertise then validates code → ER-diagram report → expertise.yaml anatomy |
| 16:10–21:05 | **self-improve** run + walkthrough (the Learn rubric); seeding loosely; 44 line-refs |
| 21:40–23:52 | Act/Learn/Reuse defined; database = partial (no Act); the missing act = editing code |
| 23:52–34:25 | **WebSocket (complete) expert:** `/plan build improve` fires → scale to 3 experts → plan_build_improve composition → pipeline metrics (81.8k/61.4k) → counter shows ~167 |
| 34:25–38:20 | Surgical diff; git diff of expertise; **never edit the file — fix self-improve**; lock in Act/Learn/Reuse |
| 38:20–40:30 | Favorite codebase experts (billing/security/db/…); these two are simple (no custom tools/system prompt) |
| 40:30–47:20 | **Product experts (Nile):** per-user expertise, Control-K panel, act→personalized generative UI, system-prompt variables |
| 47:20–53:45 | Challenges & trade-offs (seeding, source-of-truth, finite context, false expertise, granularity, too-many) |
| 53:45–59:20 | When to use / when NOT to |
| 59:20–62:29 | Everything is the core four; generalist-vs-expert close; AH-6 teaser (codebase architecture) |

---

## Glossary (say these back cold)

- **Agent expert** — a generic agent wired into Act→Learn→Reuse over a persistent expertise file it maintains itself.
- **Expertise file** — the agent's mental model of one domain (Dan: YAML); NOT documentation, NOT a source of truth.
- **Mental model** — a data structure that evolves with each useful action; re-validated against the code.
- **Self-improving template meta prompt** — meta prompt (builds prompts) + template (fixed purpose/structure) + self-improving (updates an isolated file for next time).
- **Meta-agentics** — meta prompts / meta agents / meta skills; they act but don't learn.
- **Act / Learn / Reuse** — take a useful action / store new info (self-improve) / read + reuse the mental model next time.
- **Partial expert** — has Reuse + Learn but no Act (e.g. the database expert).
- **Context delegation** — isolate plan/build/self-improve into fresh sub-agents so the top agent's context stays protected.
- **Seeding** — creating the first expertise version; do it loosely and let the agent own the structure.
- **False expertise** — the agent stores something wrong; inherent, expected, mitigated not eliminated.
- **Build the system that builds the system** — improve the self-improve step / the agentics, never the application-layer artifact by hand.

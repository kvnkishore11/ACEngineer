# TAC-2 Nuggets — ranked for the struggling learner

Ordering rule: how much of the rest of the course breaks if this nugget is missing. Tier 1 is non-negotiable; Tier 2 is the working machinery; Tier 3 is framing that keeps you honest and improving.

---

## Tier 1 — If you remember nothing else

**1. The 12 = 4 in + 8 through.**
The core four (**context, model, prompt, tools**) live *in* the agent — always there. Eight more levers work *through* it, flowing into the context window: **standard out, types, documentation, tests, architecture, plans, templates, ADWs**. Stack them and "agentic coding success becomes inevitable."
*Why weak learners lose it:* they memorize the list but never use it as a diagnostic. Test: when a run fails, can you name the missing lever?

**2. Tactic #2: Adopt your agent's perspective.**
Your agent is **brilliant, but blind** — every session boots a blank instance, no context, no memories, reset to zero at the end. Before every launch ask the litmus question from the tactic card: *"With my agent's core four, is it possible to complete the task I've given it?"* If no — you, not the model, are the bottleneck.

**3. Your agent can only see what you let it see.**
Standard out is its eyes on runtime. The tac-2 server swallowed every exception into a response field — fine for humans watching the browser, invisible to agents: **bad agentic code**. Logging that reaches the agent's stdout "drastically reduces the state space" it must search.

**4. Fix the system, not the bug.**
Dan knew the bug and refused to fix it: "I'm not actually fixing the issue. I'm setting up my codebase so that my agent can resolve the issue." Once stdout existed and the server ran *inside* the agent, the fix took two prompts: "any issues with the server?" → "resolve: replace bad chars and escape." That inversion — engineer the conditions, delegate the solution — is the whole course in miniature.

---

## Tier 2 — The working machinery

**5. Read your agent's tool definitions. All of them.**
`/tools` dumps the toolset with parameters because it lives in the system prompt. One "hidden secret" — Bash's `timeout` — is what let Dan run a live server inside the agent for 300 seconds. Tools you can't name are leverage you can't use.

**6. Types are IDKs — information dense keywords.**
Copy `DatabaseSchemaResponse` into a fresh, context-free agent and ask how it flows: a subagent traces it through five files (Pydantic model → FastAPI endpoint → mirrored TS interface → API client → the original spec) in 7 tool uses. Precise names create traceable information flows; `DataRequest`-style names mean "your agent is cooked."

**7. Architecture is a tax you pay on every agent boot.**
The **agent navigation problem**: agents boot hundreds and thousands of times, and each one re-explores your codebase. One decision (`app/client` | `app/server`) halves the search space. Antidote: **consistency** — same patterns, folders, names, comment structure. "If it's hard for you, you should assume it'll be hard for your agent." And: **don't refactor yet** — later lessons do it *with* your agent.

**8. Tests are the agent's self-correction machinery.**
"Your agent will make mistakes… The only question is, does it have the right leverage it needs to correct the mistakes?" Run `uv run pytest` *inside* the agent (`!` bash mode) so results land in context: a **closed loop structure**. Dan's era-line: "If you're not writing tests, you're probably vibe coding." Install order: stdout first, tests right next.

**9. Plans are prompts — accurately, they're how you communicate massive work.**
The app came from a 749-line spec Dan never hand-typed. Planning is SDLC step 1 and lesson 3's whole subject; "the plan is the prompt, and that means great planning is great prompting."

**10. Three time makes a pattern — mint a command.**
Templates are "reusable, embeddable, agentic prompts" in `.claude/commands/` (this repo: install, prime, tools — and Dan mints `/start` on camera from a command he'd run three times). `install.md` even runs another prompt: prompts inside prompts, "no different than passing a function inside of a function."

**11. ADWs are the ceiling: prompts + code + trigger.**
"Combine one or more agentic prompts right out of the commands directory, wrap it in arbitrary code, kick it off autonomously with a trigger." Seed shown: `claude -p "/tools"` — programmable mode, result returned to the shell. The empty `adws/` dir in the repo is the course's destination, left visible on purpose.

---

## Tier 3 — Framing that keeps you honest

**12. Bet on what never changes.**
Tools and models churn; the SDLC doesn't. Phase-two compression: **plan, code, test, review, document** — and notice several leverage points ARE its nodes. That's why the list is a system, not trivia.

**13. Four KPIs: size ↑, attempts ↓, streak ↑, presence ↓.**
"If you don't measure it, you can't improve it." Push runs from 5 minutes toward hours (size); drive corrections toward one-shot (attempts — 5–10 means a lever is missing); chain one-shots and when the streak breaks, name the missing lever; and shrink how much you must sit and babysit (presence) toward zero. Streak math: five one-shots vs five prompts needing three fixes each = the fixer is **3x slower**.

**14. Stop looking at error messages.**
The sequel to "stop coding": "Give them to your agent. And only when your agent fails do you take your precious time and dig into the error."

**15. The confession: this whole lesson was phase-one mode.**
Iterative back-and-forth prompting tanks the presence KPI — Dan says so about his own demo. From lesson 3 on: programmable mode, "dial up the autonomy knob all the way to 11," and the uncomfortable discipline of letting go of control. What stays: architecture, direction, planning, thinking. "English is the new programming language." "Master the primitives and you'll master the compositions."

---

## Micro-quiz (close the book first)

1. Two families, twelve members — go.
2. Tactic #2's litmus question, word for word (close enough counts).
3. What made the server "bad agentic code," and what was the actual bug (file, line, cause)?
4. Which Bash parameter let the server run inside the agent, and how did Dan learn it existed?
5. Five files `DatabaseSchemaResponse` flows through, in order.
6. The four KPIs, their directions, and what to do when a streak breaks.
7. What's the three-time rule, and what did Dan create with it on camera?

*(Answers: extract.md ideas 3, 2, 5, 4, 7, 12, 11.)*

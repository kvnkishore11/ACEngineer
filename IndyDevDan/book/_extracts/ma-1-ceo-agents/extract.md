# MA-1 — CEO Agents · Master Teaching Notes

> **Lesson in one breath:** Your agents don't have to be coding worker bees. Wrap specialized, *disagreeing* agents in your own harness and they become a **CEO and board** that turns your hardest questions into decisions — *uncertainty in, decisions out*. Three fresh unlocks make it real: **true 1M context**, a **customizable agent harness (Pi)**, and **compounding agent expertise**.

Course: **MA** · order 15 · video **40:03** (4K) · YouTube `TqjmTZRL31E` ("Pi CEO Agents. Claude 1M Context. Multi-Agent Teams.")
Codebase: `agentic-horizon-extras/ceo-agents` (member-exclusive).

Each idea below is built for a struggling learner: **Hook → Picture → Worked example → Name it (Dan's words) → Failure mode → Retrieval check.**

---

## Idea 1 — Agents can DECIDE, not just code

- **Hook.** Everyone is running an agent right now — coding, planning, taking actions. That's the worker bee. What if the same compute sat at the *center of knowledge work* — the decision itself?
- **Picture.** Seven Claude agents in a synthwave terminal, arranged as a boardroom: a CEO at the head, specialists around the table, arguing. (Frame `t0760`.)
- **Worked example.** You feed the system a question — "Should we take the $12M acquisition offer?" — and it hands you back a memo with a ranked recommendation, every board member's stance, the dissent, and next actions. You never wrote code; you made a decision.
- **Name it.** *"This is my CEO and board multi-agent team... they're helping you make high-level game-time strategic decisions."* Dan calls the category **agentic engineering** (vs agentic *coding*): "we're not just coding anymore."
- **Failure mode.** Treating it like ChatGPT — trying to chat with it. It's a **one-shot system**: the only inputs it accepts are `/ceo-begin`, `stop`, `wrap`. Type anything else and it's blocked.
- **Retrieval.** What is the system's job in five words? *(Uncertainty in, decision out.)*

## Idea 2 — Uncertainty in, decision out (brief → memo)

- **Hook.** Before you build any agent system, answer two questions: what goes *in*, what comes *out*? Get those wrong and nothing else matters.
- **Picture.** A pipe: **brief** (a structured question) → **deliberation** (the debate) → **memo** (the answer). Input node, workflow node, output node. (Frames `t1235` brief, `t0468` memo.)
- **Worked example.** Input = `briefs/2026-03-18-acquisition-offer/brief.md` with Situation, Stakes, Constraints, Key Question — plus `business-metrics.md` and `product-overview.md` riding along. Output = `memos/…/memo.md`: ranked recs, a board-stances table, dissent, a trade-offs table, next actions, a decision SVG, and an MP3 summary.
- **Name it.** *"We have uncertainty in, and we have decisions out. That is the purpose of the CEO and board multi-agent system."* The middle is the **workflow** (a.k.a. the deliberation, a.k.a. the debate).
- **Failure mode.** Believing the memo is the only artifact. The **middle state** — the conversation log, the expertise files, the argument SVGs — is where the reasoning and the dissent live.
- **Retrieval.** Name the three nodes of the flow. *(Brief → deliberation → memo.)*

## Idea 3 — Multi-agent orchestration: one node fans out to many

- **Hook.** How do you spot orchestration in any diagram? Look for one node with many arrows leaving it.
- **Picture.** The architecture diagram: *You → Pi Extension → CEO → converse() → 8 board members.* One CEO node, eight arrows. (Frame `t1672`.)
- **Worked example.** The CEO calls `converse("all", "Board, we're here to make a call on the NutraHoldings acquisition offer.")`. All eight members respond; the CEO reads them, updates its scratch pad, and fires the next round.
- **Name it.** *"Whenever you see a single node going out to multiple agents, immediately think multi-agent orchestration."*
- **Failure mode.** Assuming the board members chat with each other live inside a round. **They don't.** They answer in **parallel and blind** within a round; they only build on each other **across** rounds by re-reading the shared `conversation.jsonl` (their prompts literally say "reread the entire conversation").
- **Retrieval.** In one round, does Revenue see Moonshot's answer before writing its own? *(No — parallel; only across rounds via the log.)*

## Idea 4 — The board is ADVERSARIAL by design

- **Hook.** If you hire eight people who all think alike, you didn't build a board — you built an echo. "If you get a bunch of Chads on your team, every Chad is going to say, 'Yeah, we should use React.'"
- **Picture.** Eight colored cards, each pulling a different direction: Revenue (cash in 90 days) vs Compounder (trust in 24 months); Moonshot (10x bet) vs Contrarian (prove you're not fooling yourself).
- **Worked example.** In the acquisition demo the room went 7 for SELL, but **Moonshot** dissented — "the blend engine is platform infrastructure priced as DTC" — and forced a gated 30-day investor test into the memo. The disagreement produced the *best* recommendation, not a watered-down average.
- **Name it.** *"This is a multi-agent adversarial pattern... multiple perspectives that don't agree so we can really flesh out the mental model."* The CEO even keeps **tension pairs** to exploit (Revenue↔Compounder, Product↔Technical, Customer Oracle↔Moonshot, Revenue↔Moonshot).
- **Failure mode.** Wanting consensus. Consensus means the board added nothing you didn't already believe.
- **Retrieval.** Name two tension pairs and what each side optimizes for.

## Idea 5 — Real constraints: time and budget

- **Hook.** A meeting with no clock runs forever. So does an agent with 1M tokens and no leash.
- **Picture.** Two gauges under the input: **TIME** and **BUDGET**, each with a min marker and a max ceiling. (Frames `t0760`, `t0900`.)
- **Worked example.** Config sets 2–5 min and $1–$5. After every `converse` call the CEO gets a Constraint State block; at 80% of max it starts wrapping; at max the harness prints **[MAX REACHED]** and the CEO must call `end_deliberation`.
- **Name it.** *"For the first time ever, we can actually apply real constraints to the duration and the budget of our meetings."* Min thresholds guarantee depth; max thresholds enforce discipline.
- **Failure mode.** Reading the tiny $1–$5 demo budget as the tool's ceiling. Dan runs production far higher — "I prioritize high-leverage decision-making much more than I prioritize time and compute costs."
- **Retrieval.** What forces the meeting to end, and when can the CEO *not* end early? *(hit_max forces the end; the CEO can't call end_deliberation before min_time unless max is already hit.)*

## Idea 6 — Innovation #1: true 1M context (the enabler)

- **Hook.** Everyone claims a big context window. Zuck claimed 10M with Llama 4 Maverick — "complete garbage." The claim is easy; keeping the model *useful* across the window is the hard part.
- **Picture.** The MRCR retrieval chart: Claude 4.6 lines stay high across 128K→1M; the others fall off after ~250K. (Frame `t0076`.)
- **Worked example.** Because the window is genuinely 1M at **flat price** (no post-200K surcharge), an entire brief + financials + product overview + multi-round debate + long expertise files all fit in one session — no compaction hacks.
- **Name it.** *"It's one price for the full context window, no long context premium... This means that the core four just got a massive buff."* For decisions you don't need perfect retrieval — you need retrieval that **doesn't lose the key ideas**.
- **Failure mode.** Thinking 1M only helps *in-loop* (more room while coding). The bigger win is **out-of-loop**: a tool that holds your whole business/product/life in context and reasons over it.
- **Retrieval.** Why is 1M context specifically the unlock for this system? *(It lets each agent hold the whole business + long compounding expertise in one session.)*

## Idea 7 — Innovation #2: a customizable agent harness (Pi)

- **Hook.** Out-of-box agents give everyone the *same* results. To break out, you need to change the machine, not just the prompt.
- **Picture.** pi.dev: "There are many coding agents, but this one is mine." A `.pi/` directory with your *own* structures — agents, configuration, expertise, briefs, deliberations, memos — not the fixed `.claude/` layout. (Frame concept; `t2172` in video.)
- **Worked example.** A single ~1,300-line TypeScript extension (`ceo-and-board.ts`) registers two custom tools (`converse`, `end_deliberation`), spawns board members as `pi` subprocesses, streams them into a synthwave TUI, and injects the CEO's system prompt on boot. That's impossible with an out-of-box agent.
- **Name it.** *"That second big innovation is a customizable agent harness like Pi... you can go all the way down to the prompt level, the system prompt level, and redesign how things work. This is where vibe coders have no shot."*
- **Failure mode.** Fixating on Pi. The transferable idea is *a harness you can customize to the primitives* — the pattern ports to anything exposing tool registration + subprocess/session control.
- **Retrieval.** Name one thing the custom harness lets you do that a stock agent can't. *(Register custom tools / spawn board subprocesses / override the system prompt at boot / apply meeting constraints.)*

## Idea 8 — Innovation #3: agent expertise that compounds

- **Hook.** "Memory" is vague. What if each agent instead kept notes on the *one thing it's an expert in* — and got sharper every time you used it?
- **Picture.** `expertise/ceo-scratch-pad.md`: a round-1 vote tally, key insights, unresolved tensions, an evolving thesis. One file per member. (Front matter shown in `t1122`.)
- **Worked example.** Across 20 briefs, the revenue agent's log grows to ~11K tokens: it's learned it's "often at odds with the compounder" and how to argue against long-term bias. The CEO tracks which tensions resolve. The board's starting position gets richer every meeting.
- **Name it.** *"Expertise is memory and patterns surrounding a specific problem... This is not memory. It is domain expertise."* The 1M window is what makes tens-of-thousands-of-tokens expertise practical.
- **Failure mode.** Copying the demo's tiny presentational scratch pads and expecting the compounding value — the real files are far larger and accrete over many real decisions.
- **Retrieval.** How is expertise different from memory? *(It's memory + patterns tied to a specific domain, persistent across deliberations, and it compounds.)*

## Idea 9 — Specialize, or get the normal distribution

- **Hook.** Short prompt + stock agent = the exact same output everyone else gets. That's the RL average.
- **Picture.** A bell curve; almost everyone clustered at the mean; a few outliers on the right who changed more than their context.
- **Worked example.** To move right you change the **core four** (context, model, prompt, tools) *and* go up a level: custom harness, fully overridden system prompt, expertise, skills, model choice. The board members completely override the coding-agent persona — "These are not coding agents."
- **Name it.** *"You have the core four, change one of them, change two of them. Don't just rely on your context being different."*
- **Failure mode.** Thinking richer context alone is specialization. Change the model and the tools too.
- **Retrieval.** What are the core four, and what does "don't just rely on context" mean? *(Context/model/prompt/tools; change more than one dimension to leave the normal distribution.)*

## Idea 10 — Template your engineering (forced prompt engineering)

- **Hook.** The reason your agents can't repeat your best work is that you never wrote it down as a template.
- **Picture.** A brief that won't run: a red notice — "missing ## Constraints" — until you add the section. (Validation in `ceo-begin`.)
- **Worked example.** Every brief must contain Situation / Stakes / Constraints / Key Question (case-insensitive). Miss one and the meeting is blocked with instructions. Structure in → serious result out; a lazy two-sentence prompt gets the average.
- **Name it.** *"If you template your engineering, your agents can do exactly what you did."* And: *"Prompt engineering is very much still alive."*
- **Failure mode.** Writing a "stupid two-sentence prompt," then blaming the model. Or dropping `brief.md` with no context files so the board deliberates half-blind.
- **Retrieval.** What are the four required brief sections, and what happens if one is missing? *(Situation/Stakes/Constraints/Key Question; the meeting is blocked with a fix-it notice.)*

## Idea 11 — Observability is not optional

- **Hook.** "If you don't measure it, you cannot improve it. Full stop."
- **Picture.** `conversation.jsonl` scrolling — every turn tagged `from` / `to` / `message` — beside a folder of argument SVGs and `tool-use.jsonl`. (Frame `t1420`.)
- **Worked example.** You can replay any deliberation: who said what to whom, every tool call, every position shift, the exact moment Moonshot said "Position: REJECT."
- **Name it.** *"Observability is a key element of building powerful agentic systems."*
- **Failure mode.** Keeping only the memo and throwing away the debate — then having no way to see why the system decided as it did, or to improve it.
- **Retrieval.** Name two observability artifacts every deliberation produces. *(conversation.jsonl and tool-use.jsonl — plus expertise updates and SVGs.)*

## Idea 12 — How the harness actually runs a round (the technical truth)

- **Hook.** The docs and the code disagree in two places. A precise engineer needs to know which to trust.
- **Picture.** CEO = the Pi agent *itself* (Opus 4.6, system prompt injected at boot). Board members = separate `pi` **subprocesses** with **persistent sessions** (Sonnet 4.6), fired in **parallel**.
- **Worked example.** `converse` runs targets with `Promise.allSettled` (parallel) and streams them into one live widget; `end_deliberation` collects final statements. First subprocess call sets `--system-prompt`/`--model` and preloads context via `@file`; later calls reuse `--session` so context carries.
- **Name it — the two gaps.**
  1. **"Sequential" is wrong.** `ceo.md` says converse calls are sequential; the code (and Dan's narration) says **parallel**. Within a round, members are blind to each other.
  2. **"Contrarian speaks last" is not enforced.** The README/prompts claim it; `end_deliberation` collects statements in **config order** (Contrarian is 4th of 8). Aspirational, not implemented in v1.
- **Failure mode.** Teaching either claim as a guarantee. Trust the shipping code.
- **Retrieval.** Where do the prompts and the code disagree? *(Parallel-not-sequential converse; Contrarian-not-actually-last in end_deliberation.)*

---

## Timeline map (key on-screen beats)

| Time | Beat | Frame |
|---|---|---|
| 0:00–0:35 | Three innovations tease; 7 agents running (CEO + board) | — |
| 1:11–1:20 | 1M context retrieval chart (Opus/Sonnet 4.6 vs GPT-5.4/Gemini 3.1) | `t0076` |
| 2:28–2:52 | "How much is a high-leverage decision worth?" framing | pull-quote |
| 2:53–3:44 | Architecture: uncertainty in → decision out; orchestration diagram | `t1672` |
| 4:00–5:17 | CEO controls the workflow; board with 1M context; final memo | — |
| 5:30–6:06 | Memo opens in VS Code; TTS summary via ElevenLabs | `t1052` |
| 7:46–9:20 | Memo breakdown: decision map, top-3 recs, board stances, tensions | `t0468` |
| 9:34–10:20 | `j ceo` boot; roster + models + 1M badges; constraints | `t0585` |
| 10:22–12:24 | `/ceo-begin`; CEO frames; board responds in parallel; 4-to-1 | `t0760` |
| 14:59–15:08 | **Max reached** — CEO forced to wrap | `t0900` |
| 15:33–16:52 | `.pi/ceo-agents/` structure; configuration.yaml walkthrough | `t0990` |
| 17:14–17:42 | NutraHoldings memo TTS ("five to one… that silence was the signal") | `t1052` |
| 18:36–19:07 | CEO system prompt front matter (expertise, skills, model) | `t1122` |
| 20:28–23:15 | Brief template + acquisition brief + business context files | `t1235` |
| 23:35–25:20 | conversation.jsonl observability; tool use; from/to | `t1420` |
| 25:15–27:20 | Expertise scratch pad; board members' argument SVGs | — |
| 29:18–31:11 | System-prompt structure; static vs runtime vars; "vibe coders have no shot" | — |
| 31:39–34:10 | Moonshot / Revenue personalities; expertise persistence over 20 briefs | `t1905` |
| 34:33–36:40 | Agent model diversity; three-innovations recap | — |

*(Timestamps from the [HH:MM:SS] transcript, ±2–3s.)*

---

## Glossary (say these back without notes)

- **CEO & Board** — a multi-agent team: one orchestrator agent (CEO) + a board of biased specialist agents that debate a decision.
- **Brief** — the structured input (Situation/Stakes/Constraints/Key Question + context files). Validated before a meeting runs.
- **Memo** — the structured output (ranked recs, stances, dissent, next actions, decision SVG, TTS).
- **Deliberation / debate** — the workflow in the middle; logged to `conversation.jsonl`.
- **converse(to, message)** — the CEO's tool to broadcast/target the board; returns responses + constraint state.
- **end_deliberation(message)** — collects final statements and triggers memo synthesis; guarded by min_time.
- **Constraint engine** — measures elapsed time + budget after each converse; forces a halt at max.
- **Agent harness (Pi)** — the customizable terminal agent; extensions register tools, spawn subprocesses, own the TUI.
- **Expertise file** — a persistent, per-agent, domain-specific scratch pad that compounds across deliberations.
- **Agent model diversity** — different model families per agent to sharpen conflict (demo is all-Claude; a multimodel config wires GPT/Gemini/Qwen/Kimi/MiniMax via OpenRouter).
- **The core four** — context, model, prompt, tools. Change more than one to leave the "normal distribution."
- **Agentic engineering** — using agents to *solve problems and make decisions*, not just write code. "Coding is just the beginning."

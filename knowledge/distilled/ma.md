# Multi-Agent (MA) Course — Complete Learning Distillate

Source of truth: full transcripts in `ma-1..4/transcript/`. Cross-checked against `book/_extracts/ma-*/` and the public repo `youtube/_repos/disler__the-verifier-agent` (MA-4).

The four lessons form one arc: **CEO agents** (multi-agent decision-making) → **lead agents** (three-tier multi-team coding) → **UI agents** (a multi-team implementation that operates a product) → **verifier agent** (the simplest two-agent system that attacks the review constraint). All four run on a customized **Pi agent harness** and all four are built around Dan's 2026 theme: **trust and scale**.

---

## MA-1: CEO Agents

**Thesis:** With true 1M-token context models, a customizable agent harness, and persistent agent expertise, you can promote agents from low-level worker bees to a **CEO and board** — a multi-agent adversarial system that takes your hardest strategic questions in as a *brief* and returns a *memo* (a Jeff-Bezos-style recommendation). "Uncertainty in, decisions out."

**Named frameworks & mnemonics:**
- **CEO and board** — a strategic decision-making multi-agent team: one CEO agent (best model, e.g. Opus, running as the Pi agent itself) orchestrating a board of opinionated member agents (Sonnet subprocesses), each with a completely overridden system prompt. "These are not coding agents. This is a CEO and a board built to make strategic decisions on your behalf."
- **Uncertainty in, decision out** — the system's function signature. The three nodes: **brief** (input prompt/question) → **deliberation** (the debate, the workflow) → **memo** (the output decision).
- **The brief** — the input prompt; must contain required sections (Situation, Stakes, Constraints, Key Question) or the harness rejects it. "We are kind of forcing great prompt engineering as a pattern into the agent harness."
- **The memo** — the output: final decision, decision map SVG, board-member stances, resolved/unresolved tensions, trade-offs and risks, next actions, plus an ElevenLabs MP3 summary.
- **Three innovations** — (1) **Claude 1M true context window** at one flat price ("no long context premium"); (2) **customizable agent harness** (Pi: "There are many coding agents, but this one is mine"); (3) **agent expertise** — persistent, domain-specific memory files.
- **Multi-agent adversarial pattern** — multiple perspectives that deliberately don't agree, "so we can really flesh out the mental model that we need to make the best decision possible."
- **Expertise (vs memory)** — "Memory is quite vague, but expertise is memory and patterns surrounding a specific problem." Per-agent scratchpad files that persist and grow across deliberations (Dan's production ones run tens of thousands of tokens).
- **The core four** — context, model, prompt, tools; the 1M window means "the core four just got a massive buff."
- **The board members** — Revenue (cash in 90 days: "gravitational pull towards shipping, selling, and collecting money"), Technical Architect, Compounder (compounding advantage over quarters/years), Product Strategist, Contrarian, **Moonshot** ("What if we're thinking too small?" — advocates 10x, category-defining bets).
- **Constraints engine** — meeting time (e.g. 2–5 min) and budget (e.g. $1–$5) enforced in code; the harness injects "we're over time/budget, wrap it up" back into the CEO's conversation.
- **One-shot multi-agent system** — the harness rejects freeform prompting; the only command is `ceo begin`. "This is not a conversation."

**Nuggets:**
- "It's not just you making key decisions anymore… it's you, your team, and a country of geniuses in a data center."
- "How much is a high-leverage decision really worth to you?" — size time/budget to the value of the decision, not to habit.
- "You must know what's your inputs and what's your outputs" — then design the workflow between them.
- Whenever you see a single node going out to multiple agents, "immediately think multi-agent orchestration."
- Around 250K is where long-context retrieval starts degrading — but "you don't need perfect retrieval. You need retrieval that doesn't lose the key ideas."
- "If you template your engineering, your agents can do exactly what you did."
- "Don't just write a stupid two-sentence prompt. Think. Give your agents serious information to work with and it will give you a serious result."
- "Prompt engineering is very much still alive — don't let anyone make you think that it's not."
- Every board member gets ALL the extra context (product overview, business metrics): "they're all on the same page. This is key."
- "Observability is a key element of building powerful agentic systems. If you don't measure it, you cannot improve it, full stop." (full conversation.jsonl + tool-use logs)
- You want agents "opposing each other at odds, so that they poke holes in each other's strategy."
- "If you get a bunch of Chads on your team, every Chad is going to say 'Yeah, we should use React.'" — engineer diverse, conflicting personas.
- Every agent can generate SVGs "to visually compel the CEO toward their argument."
- "Agent model diversity is super super important for creating better conflict and unique opinion" — the constraint is that models must maintain long context.
- "Specialization is the advantage, and specialization once again increases the trust we have in our agents."
- "If you're not building specialized agents… and customizing your agent harness, you're in the normal distribution of what everyone else is getting."
- "This is where vibe coders have no shot… The awareness just isn't there." (You must know the primitives — system-prompt level, subprocess level.)
- "These are micro applications that do one thing extraordinarily well, the agentic way."
- "We're engineering and solving problems with our agents. We're not just coding anymore." "Coding is just the beginning… it's the lowest hanging fruit."
- In-loop, 1M context = compress less. Out-loop, plugged into your systems, "the leverage you can get is now massive."
- Real value accrues as briefs+memos stack per domain: "a chain and a stack of decisions… that's where there's real value" (expertise gets more valuable with every brief).

**What Dan actually did/built:**
1. Built a **CEO-and-board app as a Pi extension** (~2,000 lines, one extension file) with its own directory layout under `.pi/ceo-agents/`: `agents/`, `config` (YAML), `expertise/`, `briefs/`, `deliberations/`, `memos/` — "with the Pi agent harness you can make your own structures."
2. Launched it via justfile: `j ceo` (J = alias for `just`), then ran the single accepted command `ceo begin`; the harness lists available briefs.
3. Ran the **acquisition-offer brief**: mock company BlendStack (D2C supplement-stack builder) gets a $12M cash offer (11x its $1M ARR) from PE firm Neutra Holdings; auxiliary context files `business-metrics.md` and `product-overview.md` ride along to every board member.
4. Watched the workflow: CEO gathers context → updates its scratchpad/expertise file → runs its `converse` tool to broadcast to the board → Revenue/Technical Architect/Compounder/Product Strategist/Contrarian/Moonshot respond **in parallel** → loop repeats while inside time & budget → harness injects "[MAX REACHED]" → CEO demands "final position, one statement each" → `end_deliberation` → memo written. Total demo cost ~$2.50.
5. Result: board recommends accepting the $12M offer ~5-to-1 with conditions (retention-linked earnout, 90-day knowledge transfer); Moonshot dissents ("reject and run a 30-day investor test"). TTS kicker: "nobody in three rounds could name the root cause of five quarters of decelerating growth. And that silence was the signal."
6. Showed the **custom agent front matter** (expertise, skills, model — parsed by the harness and hot-loaded into the system prompt at boot with runtime variables), the classic prompt format (Purpose / Variables / Instructions / Workflow / Context / Report), agent-generated SVGs (revenue agent's bull/base/bear multi-year exit plan), the ElevenLabs `tts` skill, and the brief-section validation that rejects malformed briefs.
7. Kicked off a second deliberation (FDA-warning brief) to show reuse; earlier had run a shorts-platform marketing brief (fix the retention engine first, then YouTube Shorts).

**Workout module:**
- **Goal:** Build a one-shot "board meeting" multi-agent decision system: brief in → parallel opinionated debate → memo out, under a time/budget constraint.
- **Prerequisites:** Any scriptable agent harness (Pi extension, or Claude Code + headless `claude -p` subprocesses), a model with long context, `just`.
- **Steps:**
  1. `mkdir board && cd board && mkdir agents briefs memos deliberations expertise` — mirror Dan's three essential nodes (briefs, deliberation, memos).
  2. Write `agents/ceo.md` plus 4 board personas with front matter (`model`, `expertise`, `skills`) and fully overridden system prompts: `revenue.md` (maximize cash in 90 days), `compounder.md` (multi-year compounding advantage), `contrarian.md` (attack assumptions), `moonshot.md` ("What if we're thinking too small?"). Give each Temperament / Reasoning patterns / Decision-making heuristics sections.
  3. Write `briefs/_template.md` with required sections `## Situation`, `## Stakes`, `## Constraints`, `## Key Question`; write a validator (script or harness hook) that refuses to run a brief missing any section.
  4. Write the orchestration loop: CEO reads the brief + every `.md` context file in the brief's folder, broadcasts the question to all board members **in parallel** (each member is a separate agent process with a persistent session, preloaded with the same context files), appends every message to `deliberations/<id>/conversation.jsonl` (from/to/message).
  5. Add the constraint engine: after every round, append elapsed time + cumulative cost to the CEO's context; at 80% of max, tell it to wrap; at max, force "final position, one statement each" then a memo.
  6. Add expertise: each agent reads `expertise/<name>.md` on boot and appends notes after the meeting.
  7. Write a real brief about a real decision you're facing (job offer, pricing change, stack migration) with two auxiliary context files; run it end-to-end; read the memo.
- **Done-when:** A malformed brief is rejected; a valid brief produces a `memos/<id>.md` containing a recommendation, per-member stances, at least one explicit dissent, and unresolved tensions; `conversation.jsonl` replays the whole debate; the meeting self-terminates within your time/budget caps.
- **Level-up:** Put different vendors' models behind different board seats (model diversity → better conflict); add an SVG-generation skill so members argue visually; add "backroom talk" (member-to-member messages); grow one agent's expertise file across 5 briefs in the same domain and compare memo quality on brief #1 vs #5.

**Quote of the lesson:** "At this next tier of agentic engineering, it's not just you making key decisions anymore… It's you, your team, and a country of geniuses in a data center."

---

## MA-2: Lead Agents (Multi-Team Agentic Coding)

**Thesis:** One agent is not enough — the next step past Claude Code is **multi-team agentic coding**: a three-tier system (orchestrator → team leads → workers) of specialized **agent experts** that remember, are domain-locked to their part of the codebase, and are all driven through a single chat interface so your cognitive input stays flat as agent count grows.

**Named frameworks & mnemonics:**
- **Multi-team agentic coding** — "specialized teams of agents to outperform the normal distribution of results"; pushes beyond Claude Code via a customized Pi harness re-engineered into a chat room with your agent teams.
- **Three-tier architecture** — **orchestrator → leads → workers**. "You are just talking to the orchestrator, the orchestrator delegates to the teams, and the teams delegate to their workers." Orchestrator + leads get the best models (Opus); workers can be dialed down (Sonnet) — "your thinkers… as smart as they possibly can [be]; your workers… just need to follow instructions and execute."
- **The three key nodes of building software** — **planning, engineering, and validation** (the three default teams).
- **Zero micromanagement (skill)** — shared by orchestrator and leads: "Don't micromanage, delegate the right work at the right time to the workers." / "You're a leader — delegate, never execute."
- **Domain (domain locking)** — front-matter spec of "what the agents can and cannot do and where they can and cannot go" (per-path read/update/delete). Planners read everything, change nothing. Front-end dev writes only `front-end/`; back-end only `back-end/`. "No one should be touching the DevOps files and folders except the DevOps agent — this is like the holy grail of operating mid-to-large-size codebases."
- **Agent experts / mental model** — every agent loads a personal expertise file at boot and updates it after work ("a working mental model about how things work, and this grows over time"). Governed by a ~77-line **mental model skill**; Dan never touches the files. Expertise is a list — you can add **read-only expertise** (`updatable: false`) for opinionated knowledge (billing, migrations) no agent may corrupt.
- **Active listener (skill)** — "read the conversation log before every response" — installed in all 10 agents.
- **Conversational response (skill)** — concise chat-style replies; given to orchestrator/leads, deliberately withheld from workers ("we want our builders to be very, very verbose and very detail-oriented").
- **Delegate (tool)** — the one special tool that defines the hierarchy; orchestrator and leads have it, workers don't.
- **Multi-team config (YAML)** — orchestrator + teams + leads + members, each a name + path to a system prompt. "At any point in time we can just copy our config, change up the teams, and specialize how we need." Kill or add a team by editing one file.
- **Prompt complexity classifier** (the demo codebase) — routes user prompts to high/medium/low-tier models: "You don't want to pay for intelligence that you don't need." Biased toward high as the safe default.
- **Trust and scale** — "The name of the game in 2026 is trust and scale": raise trust until you *know* the team ships when you hit enter, then scale it.

**Nuggets:**
- "One agent is not enough."
- "You stopped using agents that forget and you started using agent experts."
- "If you're a cost min-maxer and you care about saving money over getting results, this video is not for you."
- The lead stepping out of its domain and getting blocked "might seem like an annoyance or a waste of tokens, but it's actually very valuable" — the block routes work to the right specialist.
- "We are not afraid to spend to win here. We're not afraid to give our agents all the relevant context they need."
- "Always be thinking about where the ball is going, not where it is." Three converging trends: rising intelligence + bigger context windows, agent expertise, customizable agent harnesses.
- Ask all teams one question → "a multi-perspective answer" with consensus and split recommendations surfaced.
- Every agent can see the conversation (session JSONL); "every agent is aware of the conversation happening."
- "The lead cannot do work. It is a thinker. It's a planner. It's a coordinator."
- "The way that you're building your agentic coding system is the edge now."
- Leads/orchestrator = Opus, workers = Sonnet — tune the tier-to-model mapping; "if you're going all out, you'll make everything the top best possible model."
- "Every time I boot this up, my agent teams, down to the individual workers, has a stacking, compounding set of memory."
- "You can't have your fingers on everything… You have to let go. You have to teach your agents to operate as you would." (the mental-model file is the prime example)
- Don't be over-rigid with agent experts — give guidelines (77-line skill), let them maintain their own model.
- "Your cognitive input into the system… doesn't need to increase as you increase the total number of specialized agents" — the chat interface + single orchestrator is what makes customization scale.
- Next-gen ideas: a **meta agent / meta team** to fine-tune the team itself; team-based reusable prompts ("plan, build, validate — one of the oldest workflows known to agentic engineers"); read-only expertise for billing/migrations/DevOps.
- "Agent experts will always outperform a generic agent" — same reason you trust the engineer who's done it over and over.
- On the $8 objection: "You're thinking about right now. You're not thinking far enough into the future. Models will improve, costs are going down."
- "I am not spending enough tokens, you are not spending enough tokens, and you are wasting time doing things the old way — and now the old way is one agentic coding tool in the terminal, prompting back and forth."
- "This isn't just Claude capturing memory with everything you've ever said to it over years. That's not going to go well. What is going to go well is specialized agents that have specific purposes."
- "Can you build systems that build systems on your behalf?"

**What Dan actually did/built:**
1. Re-engineered the Pi harness into a **chat room with agent teams** (footer shows orchestrator/leads/context/total cost; `/toggle workers` reveals the full roster; 10 specialized agents).
2. Demo ladder: `ping` (orchestrator ping-pong) → "ping each team lead" (two-layer fan-out and compose) → "have engineering present tree structure of the most important files" (engineering lead hits a domain wall, then **delegates** to front-end + back-end devs — three tiers live on screen).
3. Working codebase: a **prompt-complexity classifier** (route prompts to high/mid/low models). Ran `j predict "summarize this code base"` → label `medium` with confidences.
4. Asked all teams: "what are two additional scikit-learn classifiers we can test against?" → planner/engineer/validator teams each delegate internally; orchestrator synthesizes: LinearSVC + CalibratedClassifierCV unanimous, ComplementNB/SGD split noted.
5. Ran the classic workflow as one prompt: "**plan, engineer, and then validate** — add just commands to test both models (`just prompt both`)" → plan lead reads all context first, back-end dev builds, QA engineer finds issues the security reviewer missed ("ship it, no issues" vs QA's findings — different context windows, different perspectives), orchestrator composes. ~18 minutes of team work.
6. Verified via new just commands (`predict both`, `train both`, head-to-head eval on the holdout set) — orchestrator can't run it, delegates to engineering lead, who delegates to back-end dev.
7. Walked the internals: `multi-team` config YAML (teams/leads/members = paths to system prompts + team color); orchestrator front matter (expertise + max lines 10,000, skills); shared vs withheld skills; the **domain** blocks for planning lead and front-end/back-end devs (read everything, write only your directory); runtime-injected variables (session dir, conversation log, teams from YAML); session storage of every tool call and each agent's fully-templated system prompt; the back-end dev's ~5,000-token self-maintained mental model.
8. Killed the validation team in the YAML and relaunched to show teams are config, not code.

**Workout module:**
- **Goal:** Stand up a three-tier orchestrator→leads→workers team over a real small codebase, with domain locking and per-agent persistent mental models, driven through a single chat entry point.
- **Prerequisites:** A codebase with at least two separable domains (e.g. `frontend/` + `backend/`, or `src/` + `tests/`); Pi (or Claude Code with subagents as the limited fallback); `just`.
- **Steps:**
  1. Create a team config `multi-team.yaml`: one `orchestrator` (best model) and two teams — `engineering` (lead + `backend-dev` + `frontend-dev` workers) and `validation` (lead + `qa-engineer`), each entry = name + path to a system-prompt `.md`.
  2. Write shared skills as small markdown files: `zero-micromanagement.md` ("You're a leader — delegate, never execute"), `active-listener.md` ("Read the conversation log before every response"), `conversational-response.md` (orchestrator/leads only), `mental-model.md` (~75 lines: when to read, when to update, how to structure, max lines).
  3. In each agent's front matter set: `model` (Opus-tier for orchestrator/leads, Sonnet-tier for workers), `skills`, `expertise: [path to its mental-model file]`, `tools` (only orchestrator/leads get `delegate`; only workers get write/edit/bash), and `domain` (workers: read `**/*`, upsert/delete only their own directory; leads: read-only everywhere + their expertise dir).
  4. Enforce domains with a tool-call hook (Pi hooks or Claude Code PreToolUse hook): no matching rule = deny; blocked message should say who to delegate to.
  5. Boot the system; run the ladder: `ping` → "ping each team lead" → "have engineering present tree structure of the most important files" — confirm the lead delegates instead of executing.
  6. Run one full feature as a single prompt: "plan, engineer, and then validate: <small real feature>. Add just commands to test it." Watch plan→build→validate flow through the tiers.
  7. Run 3+ sessions; inspect each agent's mental-model file growing; never edit the files yourself.
- **Done-when:** A lead attempting a file write gets blocked and delegates instead; the front-end worker cannot modify backend files (hard block, not just prompt); one prompt to the orchestrator produces planned+built+validated work with a composed summary; mental-model files contain content you didn't write after session 3.
- **Level-up:** Add a read-only expertise file (`updatable: false`) for a "billing"-style sensitive domain; add a team-based reusable `plan-build-validate` prompt; swap one worker to a different vendor's model via config; build a meta-agent whose job is critiquing and tuning the team's prompts and skills.

**Quote of the lesson:** "I am not spending enough tokens, you are not spending enough tokens, and you are wasting time doing things the old way — and now the old way is one agentic coding tool in the terminal, prompting back and forth."

---

## MA-3: UI Agents (Infinite UI Agents / Harness Engineering)

**Thesis:** The Claude Code leak's real signal is that **the agent harness is the product** — models are being commoditized, so the most viable new skill is **harness engineering**. Dan proves it by pointing his multi-team system at a domain: an **infinite UI generation system** where a team of agent experts builds unlimited brand-consistent UIs — solving a problem class, not a one-off task.

**Named frameworks & mnemonics:**
- **Harness engineering** — "one of the most viable skills an agentic engineer can learn." The harness gives you "deterministic code, token caching, agent orchestration, prompts, skills, and of course, model control." "Without the agent harness, there are no agents, no agentic coding… no agentic engineering."
- **The agent harness is the product** — the Claude Code leak's one takeaway: a $2.5B-ARR business is the harness, not the model; you can build a domain-specialized harness that captures "fractions of that ARR."
- **Problem classes, not one-off tasks** — "When you stop vibe coding and you start agentic engineering teams of agents in your agent harness, you can solve problem classes, not just one-off tasks."
- **Infinite UI system** — brand → product/application → tree → branch/leaf versions; each leaf node is a full UI. "Design a system that allows us to build infinite UIs within a consistent brand design."
- **Three tiers again** — orchestrator → leads → workers; "Leads don't work, orchestrators don't work — they think, they plan, and then they delegate the building." Workers here: scaffold worker, view generator, animation specialist, brand analyst, soft/hard validators.
- **Till-done list** — "not a to-do list, not a to-done list, a till-done list. Our agents are going to work until all these tasks are complete."
- **The orchestrator as prompt engineer** — "I have taught my orchestrator how to prompt engineer" — the orchestrator writes full prompts to teams; leads prompt workers (the meta-meta theme).
- **One agent, one prompt, one purpose** — "Specialization and that focused context window… is a massive advantage in these multi-agent team systems."
- **Claude Code as meta agent / meta builder** — "80% of the time I'm spinning up Claude Code agents to not work on the actual product… I'm building the system that builds the system," then the specialized system outperforms any number of stock instances. "In ands, not ors."
- **Domain (front matter)** — same as MA-2: path-scope each agent (front end only, migrations only, DevOps only, billing only).
- **Input must not scale with agent count** — horizontal team scaling behind a single orchestrator: "our input to the system doesn't scale with the number of agents that we have. This directly limits what you can do."
- **Agentic security** — named as the big adjacent opportunity: "anyone can sit down right now and just write a prompt to exploit an application"; the demo brand (Aegis, an agent security command center) is itself a pitch for it.
- **Big three themes** — "harness engineering, multi-agent orchestration, and then trust and scale. Trust and scale really underlines these first two."

**Nuggets:**
- "The agent harness matters a ton."
- "The models are being quickly commoditized."
- "Claude Code is everywhere. It is now the mainstream. If you want to push beyond, the next step is to learn how to harness engineer."
- "Spinning up parallel agents with blank memories is an improvement, but what we really want is teams of agents that remember."
- "You observe, you act, you learn, and then you iterate" — what expert teams do that one-shot agents don't.
- "There is very little value in prompting your agent to build the thing. What you want… is a team of agents that knows how to build the application on your behalf."
- "This team operates this product. This is like the core of this video."
- Multiple models/teams = resilience: when MiniMax and Step-flash workers returned nothing, "if one agent fails, another agent can pick up the work" — and the leads broke their no-write rule to finish: "Very team lead-like… if someone doesn't perform, it's up to you to get the job done."
- "I could easily add a model rotation system… there's all types of things you can do when you own the agent harness."
- "Once you gain control of your agent harness, you can build out any file structure you want."
- The 7K-token mental model file: "The agent operates, controls, and tracks whatever it thinks it needs to. I don't touch this file ever." (guided only by a ~75-line skill)
- "Every prompt, you have to know the communication stream. Who are you talking to?" — here, always the orchestrator; "delegate" is literally a tool and an information-dense keyword.
- "Like 80% of engineering work — of knowledge work, frankly, probably 90% — is a workflow. A series of tasks." Build teams that execute workflows top to bottom.
- "The point of the agent harness is to increase the trust you have in your system by specializing."
- "When I sit down to build with agents now, I think about solving problem classes, not just the individual problem."
- "We are going to build with agents until we have agents that work while we sleep… agents that operate your product end to end. That's the North Star."
- "Coding is dead. Coding by hand is absolutely dead. You want to start templating… into your agent system prompts, into skills, into reusable prompts."
- "Here's the truth of it all: you are the bottleneck. It's not the models, not the tools, it's not the agent. It's you."
- "I'm scaling my compute to scale my impact."
- "The theme of 2026 is increasing the trust you have in your agents to do larger scales of work over time."

**What Dan actually did/built:**
1. Framed the Claude Code source leak as evidence the harness is the product, then demoed the **infinite UI agents** codebase — the third Agentic Horizon asset, an *implementation* of MA-2's multi-team tool pointed at a domain.
2. The product: a workspace of **three brands** (Aegis — an "agent security command center" — plus AgentX and AgentDan), each brand → applications → trees → branch/leaf UI versions, all rendered in a navigable gallery; existing UIs (threat dashboards, false positives, coverage, performance, deployment control, activity logs) were built by the agent teams in consistent brand style.
3. Pasted one stored reusable prompt to create a net-new application; watched: orchestrator writes a **till-done list**, at-mentions the **setup team** with a full engineered prompt → scaffold worker builds three trees → orchestrator deploys horizontally scaled **UI generation teams A, B, C in parallel** (A/B on open-source MiniMax 2.7 and Step 3.5-flash, C on Sonnet) → leads prompt view-generator/animation-specialist workers.
4. Live failure: open-source workers returned "no response"; team A and B **leads broke the no-write rule** and wrote the components themselves ("The task must complete. Let me update and write the component myself."); team C (Sonnet) worked; validation found "two variants need fixes," orchestrator re-delegated fixes to teams A and C until done.
5. Result: three new agent-stream prototype UIs inside Aegis (glassmorphism dashboard, agents-chatting sidebar, timeline view, compact dashboard), brand-consistent.
6. Walked the harness: custom `multi-team/` structure, `agents-os/` open-source variants, expertise directory (7K-token self-maintained mental model), `multi-team-config-min.yaml` (9 agents) vs full config (15 agents), the view-generator front matter (expertise file, hot-loaded skills, tools, **domain**), and the `/generate` reusable command with parameters (brand, product, tree, count, prompt) in the standard Variables/Instructions/Workflow format.

**Workout module:**
- **Goal:** Turn MA-2's team pattern into a system that *operates a product*: an N-variant generator that produces brand-consistent artifacts (UI pages) in parallel, with validation and till-done tracking.
- **Prerequisites:** MA-2 workout completed (three-tier team + domain locking); a static-site or Vite playground repo; a brand token file.
- **Steps:**
  1. Define the domain model on disk: `brands/<brand>/brand.yaml` (colors, type, radii as CSS custom properties) and `apps/<brand>/<product>/<tree>/<branch-N>/index.html` for generated leaves.
  2. Build the team config: `setup` team (scaffold worker), `ui-gen` teams A/B/C (view-generator + validator workers), one orchestrator. Domain-lock each ui-gen team so it can only write inside its assigned branch directories (parallel writes can't collide).
  3. Teach the orchestrator prompt engineering: its system prompt must require it to (a) write a **till-done list** of every branch, (b) send each team a *complete* prompt (brand file path, target dir, brief), (c) keep re-delegating until every item is done.
  4. Write the reusable command `generate.md` with parameters `<brand> <product> <tree> <count> <brief>` and a numbered Workflow: scaffold dirs → load brand context → write N briefs → round-robin generate across teams A/B/C → validate → fix failures → finalize.
  5. Run `/generate <yourbrand> app landing 3 "bold hero with live activity feed"`; open the three generated leaves in a browser.
  6. Chaos-test resilience: point team B at a flaky/cheap model; confirm the run still completes (another team or the lead picks up the work) and the till-done list ends fully checked.
  7. Change one token in `brand.yaml` and regenerate — confirm all variants pick up the rebrand (no hardcoded values).
- **Done-when:** One command yields N distinct, brand-consistent UI variants written by different teams in parallel; a validator catches at least one issue that gets fixed without you prompting; a dead model does not stall the pipeline; zero hardcoded brand values in the output.
- **Level-up:** Add a brand-analyst worker that scores variants against `brand.yaml`; add model rotation on failure; add a second brand and prove the same team serves both; use Claude Code as your meta agent to improve the team's own prompts ("build the system that builds the system").

**Quote of the lesson:** "The Claude code leak tells us that the agent harness is the product… one of the most viable skills an agentic engineer can learn is harness engineering."

---

## MA-4: The Verifier Agent

**Thesis:** Every benchmark tests one model in isolation, but the real capability is **combinations** of models — and the simplest, highest-value multi-agent system is a two-agent **builder + verifier** pair: an un-promptable observer that decomposes every builder turn into **atomic claims**, proves each against actual state with read-only tools, and prompts the builder back with corrective feedback — directly attacking the **review constraint** of agentic coding.

**Named frameworks & mnemonics:**
- **The verifier agent** — a second Pi agent, auto-spawned, input-locked, that "validates the individual claims the builder agent has made" and "makes sure that what we asked for is what it built." It observes the builder's session JSONL, fires on the stop hook via a Unix socket, and can only touch the builder through one tool: `verifier_prompt`.
- **Builder agent / the verifiable** — your normal primary agent; "the verifier is independent of the verifiable" — it layers on top of whatever your primary agent is.
- **Atomic claims** — "Everything you prompt into your agents — they're all small axioms… units of information that can be proven true or proven false." The art of verification is decomposition: "a single PASS that hides three unverified sub-claims is worse than three explicit FAILs." Evidence beats assertion: the builder's final message "is a CLAIM, never proof."
- **The two constraints of agentic coding** — **planning and reviewing**. "If you're doing things right, you're spending your time planning and reviewing. With the verifier agent, we can improve our review constraint."
- **Spend tokens to save time** — "Quite literally spending 5x tokens to make sure that I spend less of my time." Tokens are cheap; your time is not.
- **The feedback loop / Report flywheel** — every verifier report ends with "What could you not verify?" and "What do you need from me to verify this next time?" — the gap becomes the next thing you template into the persona or script. "This is a compounding system."
- **Un-promptable by design → templated engineering as a habit** — "I can't prompt this… If something goes wrong, I don't just fire off another prompt. I'm effectively forced to improve one or more of the core four: context, model, prompt, or tools."
- **Bash policy / one-script lockdown** — "The bash tool is the most dangerous tool you can give your agents… a ticking time bomb." The verifier's bash is restricted to exactly one read-only script; anything else is "blocked, fully blocked" — "the highest level of control you can give."
- **AND, not OR** — "It's not GPT 5.5 *or* Opus 4.7. It's GPT 5.5 *and* Opus 4.7… Stack intelligence. Orchestrate intelligence." What's missing from every benchmark: they run a single model in isolation.
- **Trust and scale (the verifier's special seat)** — "Most agents increase trust or scale, not both. The verifier does both."
- **Confidence ladder** (repo): PERFECT → VERIFIED → PARTIAL → FEEDBACK → FAILED; the verifier's status bar colors green/orange/red off this grade.
- **Top-down observer** (repo): "the builder doesn't know the verifier exists"; only lifecycle ticks (start/stop/error) cross the socket; loop caps at `max_loops: 3`, then escalates to the human.

**Nuggets:**
- "Model performance is no longer the bottleneck. It's you and I. It's our ability to extract value out of agentic systems at scale, safely."
- "One of the highest-leverage things you and I can do is increase the information density per action for agents."
- "Our verifier agent has kicked off unprompted… My hands are off the keyboard."
- "My verifier agent just prompted my builder agent." (feedback mode — the verifier writes the corrective prompts you'd have written yourself)
- Demo rule that fired: no more than 10 distinct text blocks per generated image — "An image should be worth a thousand words. It shouldn't force you to… read a ton of text. That's what text is for."
- "There is no harm in having an agent validate that that is true" — even for a cracked model's output.
- "One agent, one prompt, one purpose. A focused agent is a performant agent."
- "You can stack more than one of these verifier agents" — image verifier, SQLite verifier, Postgres/Mongo/whatever verifier: specialize and stack.
- Verifications run "non-deterministically, and… deterministically as well" — LLM judgment on top of read-only script ground truth.
- "I am increasing the trust I have in my agent system by having this verifier agent validate the atomic claims."
- "This is a positive feedback loop. It's a flywheel."
- "There's no vibe coding this stuff. I cannot just fire a one-off prompt… There's no one-offs. I am forced to template my engineering into my verifier agent."
- Two sets of engineers, gap widening: those "stuck in the loop prompting back and forth" vs those "stacking up code plus agents to outperform either alone."
- "Every benchmark is missing the true capability of what you can really do with these models."
- "I'm not talking about delegation. I'm talking about multi-agent orchestration… teams of agents that operate better together than alone."
- "There are many coding agents, there are many agent harnesses, but this one is yours… it doesn't change underneath your feet as soon as a new update rolls out."
- "You don't want to be working on your application anymore… you work on the agentic system, the system that builds the system."
- "Vibe coding is the floor. Agentic engineering is the ceiling that no one has even imagined the capabilities of yet."
- "2026 is the year of trust. Do you trust your agents to do what you ask them to? And then, how much? At what scale?"
- "The winning formula is often much more simple and less hype-filled than you realize. All the top performers do two or three things over and over."
- Teaser for next lesson/video: "There is a big hole in everyone's agent right now, and that hole is the bash tool."

**What Dan actually did/built:**
1. Ran two side-by-side specialized Pi agents: **builder** (Opus 4.7) and **verifier** (GPT 5.5) — the verifier harness "takes no input."
2. Demo 1 (image verifier): in the builder — `run prime`, then a GPT-Image-2 skill to `generate arch.jpg` describing the verifier system's architecture. On builder completion (stop hook → Unix socket event), the verifier fired unprompted, decomposed the work into claims (script ran, file exists, right size, is JPG, visually depicts the two-agent system), found a violation of the **max-10-text-blocks readability contract**, and **prompted the builder itself** with corrective feedback → builder regenerated → second cycle: 7/7 atomic claims verified, clean green status.
3. Demo 2: asked for a human figure added to the diagram ("we are the ones prompting the verifiable, also known as the builder"); costs on screen: ~4% Opus vs ~23% GPT 5.5 — "spending 5x tokens" to save review time.
4. Demo 3 (SQLite verifier): `j sql` boots a builder + **verify-SQLite persona** on GLM 5.1; prompt: "find all SQLite DBs in this repo, break down tables, columns, and relationships." Verifier re-proved every claim through its **single allowed script** (any other bash call is hard-blocked); verifier spent ~2x the builder's tokens; report: all claims verified, nothing unverifiable, no feedback needed.
5. Showed the verifier persona's custom front matter (tools without write/edit, `model:` pin, `domain`, `max_loops`, bash policy) and the report contract (STATUS / CONFIDENCE / what did you verify / claims verified-failed-unverified / what could you not verify / what do you need from me).
6. Released it two ways: a **free public repo** (`disler/the-verifier-agent`: `apps/verifier/` extensions — `verifiable.ts`, `verifier.ts`, `cross-agent.ts`; `.pi/verifier/agents/verifier.md` persona; `verify_on_stop.md` prompt template; `just v` to boot; tmux-window verifier with locked input and a confidence-colored status bar) and a souped-up members version with all the domain verifier specialists + the GPT-Image-2 skill.

**Workout module:**
- **Goal:** Run and then extend the real two-agent builder+verifier system so every builder turn is automatically decomposed into atomic claims and verified — including writing your own domain verifier.
- **Prerequisites:** The public repo (local copy at `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/youtube/_repos/disler__the-verifier-agent`), Pi coding agent installed, tmux, API keys for two *different* model providers, `just`.
- **Steps:**
  1. Read `README.md` and the persona at `.pi/verifier/agents/verifier.md` — note the front matter (`tools: read, grep, find, ls, bash, verifier_prompt`; `model:`; `max_loops: 3`) and the confidence ladder (PERFECT/VERIFIED/PARTIAL/FEEDBACK/FAILED).
  2. Copy `.env.sample` → `.env`; run `/install` in Claude Code (or the manual install), then `just v` — builder opens in your terminal, verifier auto-spawns in a sibling tmux window with a locked input bar.
  3. Give the builder a claim-heavy prompt (e.g. "create a SQLite db with users and orders tables, FK between them, seed 5 rows each, report what you did"). Watch the verifier fire on the stop event, read the session-JSONL slice, and emit a `## Report` with per-claim verdicts.
  4. Force the loop: prompt the builder to do something that violates a verifiable expectation (or manually break its output between turns); confirm the verifier calls `verifier_prompt` and the builder receives corrective feedback as a follow-up message, up to 3 loops then human escalation.
  5. Try to type into the verifier window — you can't. Instead, take one item from its "What could you not verify?" section and template it: edit the persona or `verify_on_stop.md` so next run *can* verify it. This is the flywheel.
  6. Build your own domain verifier: copy `verifier.md` → `verify-<yourdomain>.md` (e.g. `verify-pytest.md` or `verify-postgres.md`); write one read-only script that is its *only* allowed bash command; pin a *different* model than the builder's in front matter (AND, not OR).
  7. Run `just clean` when done to tear down stale sockets/tmux sessions.
- **Done-when:** The verifier runs unprompted after every builder turn; a deliberately false builder claim produces a FEEDBACK-grade report *and* an automatic corrective prompt to the builder; a bash call outside the allowed script is blocked; after templating one gap, the previously unverifiable claim verifies on the next run.
- **Level-up:** Stack a second verifier persona for a different domain; port the pattern to Claude Code with a Stop hook + headless `claude -p` verifier reading the session transcript; add a rule contract of your own (like the 10-text-block image rule) and watch it get enforced; instrument token spend to see your own tokens-for-time ratio.

**Quote of the lesson:** "Quite literally spending 5x tokens to make sure that I spend less of my time… Tokens are cheap. Your time is not."

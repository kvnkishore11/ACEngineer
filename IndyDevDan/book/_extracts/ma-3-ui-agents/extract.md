# Infinite UI Agents — Master Teaching Notes

**Lesson:** `ma-3-ui-agents` · MA / Agentic Horizon (asset 3 of the trilogy) · order 17 · 32:26 · YouTube `RairMJflUSA` (uploaded 2026-04-06)
**Tactic:** **Own the Harness (Harness Engineering)** — stop solving one-off tasks with a single agent; own the agent harness and engineer specialized teams of learning agents inside it, so you operate whole problem classes.
**Codebase:** `agentic-horizon-extras/ui-agents` (member asset, single commit `7d36778`).

This lesson is a **live showcase**, not a step-by-step build like TAC-1. Dan runs a multi-team agent system on camera (and it partially fails on purpose-revealing ways), then tours the harness that produced it. The teaching job is to extract the durable ideas from a fast, dense demo and to be honest about the gap between **what Dan shows on screen** and **what ships in the committed asset** (see the Accuracy Ledger at the end).

Teaching frame for every idea below: **Hook → Picture → Worked example → Name (Dan's term) → Failure mode → Retrieval.**

---

## The one-sentence spine

> The Claude Code source-code leak told the whole industry one thing worth acting on: **the agent harness is the product.** Models are commoditizing; the durable leverage is the harness around them — and the skill that captures it is *harness engineering*. When you stop prompting one agent to build one thing and instead own a harness that runs **teams of specialized, learning agents**, you solve entire problem classes — like generating infinite, brand-consistent UI — with a single command to a single orchestrator.

Everything else is detail on that sentence.

---

## Idea 1 — The agent harness is the product

**Hook.** Claude Code leaks. Every tech channel races to cover the features and the new "Mythos model." Dan asks a different question: *what is the $2.5B ARR actually built on?* Not the model — the harness.

**Picture.** Dan's six-part definition of the harness (render as a diagram — it's a talking-head title card in the video): **deterministic code · token caching · agent orchestration · prompts · skills · model control.** (frame beat: `harness-six-components`, diagram.)

**Worked example.** In this very repo the "harness" is legible in one tiny file, `.pi/settings.json`:
```json
{ "thinking": "high", "autoCompact": true, "compactThreshold": 0.8, "prompts": ["./prompts/multi-team"] }
```
That's thinking budget + context auto-compaction (at 80%) + registration of the reusable prompt directory. The rest of the harness surface — which model, which tools, which files each agent may touch — lives per agent in front matter. Owning those knobs is "owning the harness."

**Name.** "**The agent harness is the product.**" And the load-bearing claim: *"Without the agent harness, there are no agents, no agentic coding, and that means there is no agentic engineering."* (0:57)

**Failure mode.** Treating the lesson as a hot-take on the leak (features, drama, the Mythos model). The signal is structural, not gossip: models commoditize, so invest one level down.

**Retrieval.** *What did the Claude Code leak signal, and why does it make harness engineering — not model choice — the skill to invest in?*

---

## Idea 2 — Harness engineering: solve problem classes, not one-off tasks

**Hook.** You could sit in a single Claude Code / Codex / open-code instance and build one UI. Dan did *not* do that. He built a system that builds infinite UIs.

**Picture.** The README tagline, on screen at 16:10 (frame `harness-filetree-readme`): *"Stop solving one off tasks with agents. Build systems (agent teams) that solve entire problem classes."*

**Worked example.** The problem class here is "brand-consistent UI generation." Instead of prompting for a landing page, Dan built four specialized teams (Setup, Brand, UI Generation, Validation) that already understand the domain, then drives them with one command: `/generate aegis app agent-stream 3 "<brief>"`. One sentence → three validated, brand-faithful Vue components on disk. Because **80–90% of engineering (and knowledge) work is a workflow — a series of tasks** — you systematize the workflow once and rerun it forever.

**Name.** "**Harness engineering**" / *"solve problem classes, not just one-off tasks"* (1:55). And the sharp version: *"There is very little value in prompting your agent to build the thing. What you want to be doing instead is... build a team of agents that knows how to build the application on your behalf."* (8:35)

**Failure mode.** Hearing "own the harness" as "abandon Claude Code." Dan is emphatic — *"in ands not ors."* He spends ~80% of his time in Claude Code, but as the **meta-agent** building the systems that then run the product. (See Idea 9.)

**Retrieval.** *Why is prompting an agent to "build the thing" low-value, and what do you build instead?*

---

## Idea 3 — Three tiers: orchestrator → leads → workers (and leads don't write files)

**Hook.** In a great engineering org, leads don't type the code — they plan, delegate, and unblock. Dan builds that org out of agents.

**Picture.** The Pi terminal prints the team as an indented tree (frame `agent-teams-hierarchy-models`, 5:52):
```
Orchestrator (claude-sonnet-4-6)
├─ Setup Lead → Scaffold Worker, Structure Validator
├─ Brand Lead → Brand Analyst
├─ UI Generation Lead → Vue Generator, Animation Specialist   (×A/B/C)
└─ Validation Lead → Soft Validator, Hard Validator           (×A/B/C)
```

**Worked example.** The rule lives in `CLAUDE.md` and is **enforced structurally**, not just requested:
- Leads/orchestrator front matter grants `delegate` + `tilldone` tools, but their `domain:` permissions set `upsert: false` on `apps/infinite-ui/` — they *cannot* write product files, only their own mental model.
- Workers (Vue Generator, Scaffold Worker, Animation Specialist, Brand Analyst) grant `write`/`edit`/`bash` and carry the `precise-worker` skill ("Execute exactly what your lead assigned — no improvising").
- Read-only validators (Soft/Hard/Structure) have *no* write/edit tool at all — they report PASS/FAIL, they never fix.

**Name.** *"Our orchestrator and our leads don't do any work. They're thinkers, they're managers, they're leaders, most importantly, they're delegators."* (6:49) The committed shape: **1 orchestrator + 8 teams = 24 agent slots, backed by 12 unique agent files.**

**Failure mode.** Thinking leads are idle because "they don't work." Their job is classify → delegate → synthesize; removing the write-block turns leads into workers and collapses the tiering (which is exactly what you'll watch happen under stress in Idea 7).

**Retrieval.** *Who writes files and who doesn't in the three tiers — and what two front-matter fields enforce it?*

---

## Idea 4 — One orchestrator interface: your input must not scale with agent count

**Hook.** Add ten agents and, naively, you now have ten things to prompt and babysit. That's a trap — you just became the bottleneck.

**Picture.** The chat layout Dan narrates (5:40–6:47): "scale on the left, structure and communication on the right, chat system on top." You type once, to one orchestrator; the fan-out is invisible to you.

**Worked example.** `orchestrator.md` classifies the request, opens a `tilldone` list, and delegates via the `delegate(team, question)` tool. When Dan wants three new UIs he pastes **one** reusable prompt; the orchestrator @-mentions the Setup team with a full engineered prompt of its own. Dan's phrase: *"I have taught my orchestrator how to prompt engineer."* Horizontal team scaling behind a constant-size human interface.

**Name.** *"We need to make sure that our input to the system doesn't scale with the number of agents that we have."* (5:54)

**Failure mode.** Bolting on more agents/teams while also opening more chats to steer them — reintroducing yourself as the scaling bottleneck the architecture exists to remove.

**Retrieval.** *Why is "one orchestrator interface" a hard requirement rather than a convenience?*

---

## Idea 5 — Front-matter specialization: own the core four per agent

**Hook.** What actually makes a "front-end-only" or "billing-only" agent real, instead of a system prompt that says "please only touch the front end"?

**Picture.** The Vue Generator's front matter, fully legible on screen (frame `agent-frontmatter-specialization`, 17:58):
```yaml
name: vue-generator
model: stepfun/step-3.5-flash        # per-agent model — swappable
expertise:                            # its persistent mental model
  - path: .pi/multi-team/expertise/vue-generator-mental-model.yaml
    updatable: true
    max-lines: 10000
skills:                               # hot-loaded behavior
  - mental-model / active-listener / precise-worker / parallel-mental-model-updates
tools: [read, write, edit, bash, grep, find, ls]
domain:                               # the exact paths it may act on
  - path: apps/infinite-ui/           # read + upsert, no delete
```

**Worked example.** This is the **core four (context, model, prompt, tools)**, set independently for one agent:
- **context** = shared_context files + this agent's expertise file + its session log;
- **model** = `stepfun/step-3.5-flash` here (committed default is `anthropic/claude-sonnet-4-6`);
- **prompt** = the system-prompt body with `{{EXPERTISE_BLOCK}}` / `{{SKILLS_BLOCK}}` injected;
- **tools** = `write/edit/bash` (a doer), no `delegate`;
- plus **`domain`** — the sleeper control — path-scopes where those tools may operate. Dan: *"you can specialize agents to just run on your front end, to just run on your back end, ... your database migrations, ... your devops, ... your billing."*

**Name.** *"The front matter is where a lot of the magic happens."* (18:16) *"We are hot loading the skills into the system prompt."* (18:20) *"One agent, one prompt, one purpose."* (18:51 — Dan's verbal framing; the `precise-worker` skill encodes it in the repo.) *"Full control over the core four ... you really need control of the agent harness."* (20:02)

**Failure mode.** Reading specialization as "just a good system prompt." It's four coordinated controls; skip `domain` and your "focused" agent can still wander the whole repo.

**Retrieval.** *Name the four front-matter fields that specialize an agent, and say which one makes "front-end-only" scoping actually real.*

---

## Idea 6 — Agents that learn: persistent mental models

**Hook.** Spinning up parallel agents with blank memories is an improvement. Teams of agents that *remember* — that observe, act, learn, and iterate like you do — is the real prize.

**Picture.** `vue-generator-mental-model.yaml` open in VS Code (frame `mental-model-7k-tokens`, 16:55): dated `2026-04-02`, full of self-authored patterns — `glassmorphism_split_panel`, `spacing_pattern: "calc(var(--space-unit) * N)"`, `glow_pattern`, `sfc_rules`, `breakpoints` — with **`Tokens: 7753`** in the status bar.

**Worked example.** Each agent owns a YAML expertise file. A ~77-line skill, `mental-model.md`, teaches it the loop: **read at task start; after meaningful work, update (rewrite stale entries, don't just append); after every write, `wc -l` and trim to `max-lines`, then validate the YAML parses.** Dan: *"I don't touch this file ever. All I've done here is give this agent a skill, which very, very simply tells it how to manage its mental model."* (16:28) In parallel A/B/C teams, sibling instances share one file — the `parallel-mental-model-updates` skill reframes write-conflicts as "coordination signals, not bugs."

**Name.** "**Agents that learn / mental models**." *"Teams of agents that remember... You observe, you act, you learn, and then you iterate."* (5:23)

**Failure mode (critical accuracy point).** Believing the mental models ship pre-filled. **In the committed repo all 12 expertise files are one-line stubs** (`# Mental model — auto-maintained by agent`). The 7,753-token file Dan shows is **runtime state** he accumulated. Clone the asset and you start empty; the agents grow their own knowledge as you run them.

**Retrieval.** *How does an agent "learn" here — and what will you actually find in `expertise/*.yaml` the moment you clone the repo?*

---

## Idea 7 — Model control and reliability: heterogeneous models, graceful failure

**Hook.** Owning the harness means you can put a different model behind every agent — and swap it the instant it misbehaves. Dan proves it by *letting it misbehave on camera.*

**Picture.** Two beats:
1. The team tree shows the model per line: Vue Generator = `stepfun/step-3.5-flash`, Vue Generator (B) = `openrouter/minimax/minimax-m2.7`, everyone else `claude-sonnet-4-6` (frame `agent-teams-hierarchy-models`).
2. The lead breaks the rule (frame `lead-writes-when-worker-fails`, 13:26): *"Vue Generator (B) is not writing to disk. Given the silent failure, I need to write the complete SFC myself. As a lead, I normally delegate — but my only team member is non-functional. The CLAUDE.md rules say workers write files, but with a broken worker, I need to produce the output directly to fulfill the task."*

**Worked example.** Teams A and B (open-source models) return "no response"; team C (Sonnet) works. The leads (Claude) detect the dead workers and finish the components themselves — very team-lead-like. Nothing stalls; the pipeline still delivers 3 validated variants. Dan: *"I could easily add a model rotation system into this... if this model is not working, swap it out."* The README's *"Recommended: Use Claude series models... proven reliable"* is the same lesson stated calmly.

**Name.** "**Model control / reliability & redundancy.**" *"At scale, one prompt is not enough."* (24:56)

**Failure mode.** Reading the demo's failures as the *idea* failing. The failures are the argument: because Dan owns the harness, a broken model is survivable — redundancy and rotation keep results flowing. (And: assuming the whole repo runs open-source models — on disk every agent is Sonnet; the open-source swaps were live, uncommitted edits.)

**Retrieval.** *The open-source teams failed mid-demo. Give two reasons that's evidence FOR the tactic.*

---

## Idea 8 — Reusable prompts against teams, the till-done list, and "delegate" as a tool

**Hook.** Once you own a team, you can write prompts *for the team* — a command that drives an entire workflow top to bottom.

**Picture.** The `/generate` command and the TillDone list. The 8-step pipeline in `generate.md`; the running list on screen: `TillDone: Aegis Agent Stream Generation [1/8] ... [11/11]` (frames `parallel-teams-tilldone`, `orchestrator-final-report`).

**Worked example.** `/generate <brand> <product> <tree> <count> <brief>` — consistent **Variables / Instructions / Workflow / Report** shape — runs: (1) Setup scaffolds + writes `trees.yaml`/`activity.yaml` + Zod-validates → (2) Brand loads `brand.yaml` → (3) UI Gen Lead writes N differentiated briefs → (4) **round-robin** branch 1→UI Gen, 2→UI Gen B, 3→UI Gen C, generate in parallel → (5) Setup flips `generating→validating` → (6) round-robin validate across Validation A/B/C → (7) route failures back to the generating team → (8) Setup flips to `validated/failed`, clears `activity.yaml`. The routing vocabulary is deliberately terse: *"Delegate is literally a tool. We're using information-dense keywords... to communicate maximum information."* (21:46)

**Name.** "**Reusable prompts / workflow commands**" and the "**till-done list**" — *"not a to-do list, not a to-done list, we have a till-done list... our agents are going to work until all these tasks are complete."* (6:33)

**Failure mode.** Treating `/generate` as "just a prompt." It's an 8-step, multi-team, round-robin, validated pipeline. *Accuracy nuance:* the committed `generate.md` intentionally carries **no** till-done list (per `specs/parallel-team-duplication.md`, a coordination stress-test); the on-screen TillDone is the orchestrator's own `tilldone` tool. Both are true.

**Retrieval.** *What does `/generate` take, roughly what are its stages, and where does the on-screen "till-done" list actually come from?*

---

## Idea 9 — Claude Code as meta-agent, and the theme of 2026: trust and scale

**Hook.** If the specialized Pi harness runs the product, what runs the *building* of that harness? Claude Code.

**Picture.** Dan's two-tool split, stated repeatedly: *"80% of the time I'm spinning up Cloud Code agents to not work on the actual product... I'm using Cloud Code as a meta builder, a meta agent... building the system that builds the system."* (8:20)

**Worked example.** In this repo, `.claude/commands/` (build, install, plan-w-team, prime) and `.claude/skills/` (bowser = playwright-cli, drive = tmux automation, svg-generate, tts-eleven) are the Claude-Code meta-layer that scaffolds, primes, validates, and drives the Pi multi-team system. `plan-w-team.md` even documents Claude Code's own TaskCreate/addBlockedBy team API — Claude Code builds and orchestrates the thing that then operates the product.

**Name.** "**Claude Code as meta agent**" and the closing thesis: *"The theme of 2026 is increasing the trust you have in your agents to do larger scales of work over time."* (31:56) The two skills to invest in: **harness engineering + multi-agent orchestration**, both underlined by **trust and scale** (26:03).

**Failure mode.** Chasing scale for its own sake. Scale without trust is noise; you build closed, specialized systems precisely so you can trust them with more work.

**Retrieval.** *What does Dan use Claude Code for ~80% of the time, and what single theme does he say underlines both harness engineering and multi-agent orchestration?*

---

## The Infinite UI system (the demo, mapped to the repo)

- **What it builds:** infinite brand-consistent Vue UI. Define brand identity once (`brand.yaml`), generate unlimited variants, browse them all in one Vue app.
- **Hierarchy:** **Brand → Product → Tree → Branch → Leaf.** `aegis` → `app`/`mobile`/`site` → `agent-stream`/`dashboard`/... → `v1`/`v2`/`v3` → `index.vue`. On disk: **1 real brand, 3 products, 7 trees, 23 real generated leaves** (+2 template stubs). The demo's `agent-stream` tree holds exactly the three UIs Dan browses: `compact-dashboard`, `glassmorphism-panel` (972 lines), `timeline-stack` (899 lines — matches his on-screen "899-line SFC").
- **Zero hardcoded values:** every leaf uses CSS custom properties from `brand.yaml`; edit a token → live rebrand.
- **Live preview (accuracy):** a validated branch renders as a real `<iframe>` (1280×720, CSS-scaled, `pointer-events:none`) into the leaf's gallery route, which uses `import.meta.glob` + dynamic `<component :is>`. Dan guesses "teleport"; Vue's Teleport is used only in `Sidebar.vue`.
- **Stack:** Vue 3.5 / Vite 8 / Pinia 3 / vue-router 5 / TS 5.9 / Bun; `@vue-flow/core` + `@dagrejs/dagre` (canvas); `zod` + `yaml` (validated manifests).
- **The four teams:** Setup (scaffold + trees.yaml + Zod), Brand (guard identity, briefs, contrast), UI Generation (write Vue SFCs), Validation (Playwright screenshots, brand/responsive/a11y). Tripled to A/B/C for UI Gen + Validation.

---

## VTT-verified timeline map

| Time | Beat | Frame |
|---|---|---|
| 0:00–2:10 | Claude Code leak → "the harness is the product"; harness engineering is the skill | diagram: six harness components |
| 2:10–3:15 | Infinite UI system intro; three tiers running; open-source models A/B'd vs Sonnet | `hero-infinite-ui-agents` (2:16) |
| 3:15–4:55 | Tour Aegis "agent security command center"; agentic-security opportunity | `canvas-aegis-brand-node` (3:20) |
| 4:55–5:40 | Two big ideas: harness matters; scale (teams that remember) | — |
| 5:40–6:47 | Paste reusable prompt to one orchestrator; till-done; orchestrator prompt-engineers | `agent-teams-hierarchy-models` (5:52) |
| 6:47–8:57 | Leads/orchestrator delegate, don't work; Setup → Scaffold; meta-agent aside | — |
| 8:57–10:10 | Deploy parallel UI Gen A/B/C; reduced/min team; X = out-of-domain | `parallel-teams-tilldone` (8:58) |
| 10:10–12:00 | Workspace tour (3 brands → products → trees → leaves); "this team operates this product" | — |
| 12:00–13:50 | Teams A/B (open-source) fail; leads write components themselves | `lead-writes-when-worker-fails` (13:26) |
| 13:50–17:44 | Harness/codebase tour; expertise 7K-token mental models; multi-team config | `harness-filetree-readme` (16:10), `mental-model-7k-tokens` (16:55) |
| 17:44–20:31 | Vue Generator front matter; own the core four | `agent-frontmatter-specialization` (17:58) |
| 20:31–23:05 | `/generate` command; delegate-as-tool; 80–90% of work is a workflow; pipeline done | — |
| 23:05–26:25 | Browse 3 Aegis agent-stream UIs; Sentinel alert; big themes (harness/orchestration/trust) | `orchestrator-final-report` (23:07), `aegis-agent-stream-rendered` (24:25), `canvas-live-preview-nodes` (26:05) |
| 26:25–32:26 | Agentic Horizon pitch; solve problem classes not tasks; Claude Code as meta-agent; theme of 2026 = trust at scale | — |

---

## Glossary (canonical terms + transcript mishearings)

- **Agent harness** — everything around the model that makes agents possible: deterministic code, token caching, agent orchestration, prompts, skills, model control. "The product."
- **Harness engineering** — building/specializing your own agent harness for your domain (Dan uses the Pi coding agent).
- **Pi coding agent** — the granular-control agent tool at pi.dev. *(Transcript: "pie coding agent" / "PyCoding agent." Title confirms "Pi.")*
- **Core four** — context, model, prompt, tools; owned per-agent via front matter when you control the harness.
- **Orchestrator / lead / worker / validator** — the four roles. Orchestrator + leads delegate (never write files); workers write; validators are read-only reporters.
- **`delegate` / `tilldone`** — literal tools. `delegate(team, question)` routes to a team lead; `tilldone` manages the "work-until-complete" task list.
- **Till-done list** — a task list agents work until every item is done. *(Intentional wordplay, not a mishearing.)*
- **Expertise file / mental model** — a per-agent YAML the agent self-maintains (`.pi/multi-team/expertise/*.yaml`); empty stub in the committed repo, grows at runtime to `max-lines: 10000`.
- **`domain` (front matter)** — path-scoped read/upsert/delete permissions; makes "front-end-only" agents real.
- **Brand → Product → Tree → Branch → Leaf** — the Infinite UI hierarchy; a Leaf is the generated `index.vue`.
- **Aegis** — the demo brand, an "agent security command center." *(Transcript: "Egis.")*
- **Agentix / Indydevdan** — the other two on-screen brands (not committed). *(Transcript: "AgentX / AgentDan.")*
- **Round-robin** — orchestrator assigns branch 1→A, 2→B, 3→C, 4→A... across the parallel teams.
- **Mythos model** — a real model name referenced re: the Claude Code leak (per the official description), not a mishearing.
- **Claude Code as meta-agent** — using Claude Code (~80% of the time) to build the system that runs the product. *(Transcript: "Cloud Code.")*
- **Model IDs seen on screen** — `anthropic/claude-sonnet-4-6` (committed default), `stepfun/step-3.5-flash`, `openrouter/minimax/minimax-m2.7`. *(Transcript: "Sonic," "step 3.5 flash," "minimax 2.7.")*

---

## Accuracy Ledger — what ships vs what's on screen (read before writing the chapter)

The single most important honesty requirement for this chapter. The committed member asset is a **single-commit, all-Claude, empty-mental-model** snapshot; the video runs a hand-tuned superset. Do not describe the demo as if it's what a reader clones.

| Claim | On screen | In the committed repo |
|---|---|---|
| Agent models | Vue Generator = `stepfun/step-3.5-flash`, Vue Generator (B) = `openrouter/minimax/minimax-m2.7`, rest Sonnet | **All 12 agents = `anthropic/claude-sonnet-4-6`** |
| Open-source agent variants | `.pi/multi-team/agents-os/` (vue-generator-b/c, soft-validator-b/c, ...) | **Absent** |
| Min config | `multi-team-config-min.yaml` | **Absent** (only `multi-team-config.yaml`) |
| Mental models | `vue-generator-mental-model.yaml` = ~7,753 tokens, dated 2026-04-02 | **All 12 = 1-line stubs** (`# Mental model — auto-maintained by agent`) |
| Brands | Aegis, Agentix, Indydevdan | **aegis only** (+ `_template`) |
| Agent counts | "15 unique / 9 min" (Dan's live config) | 12 unique files / 24 slots / 8 teams (base = 12) |
| Till-done in `/generate` | TillDone [1/8]→[11/11] runs | `generate.md` has **no** task list by design; it's the orchestrator's `tilldone` tool |
| Leaf preview | Dan: "teleport... iframe underneath" | `<iframe>` + `import.meta.glob` dynamic `<component :is>`; Teleport only in `Sidebar.vue` |
| Aegis brand tokens | report cited "cyan #00D9FF / purple #7B61FF" | `brand.yaml`: font **Play**, primary **#f0f0f5**, secondary **#6e7fff**, accent **#e63946** (authoritative) |
| Leaf line counts | "899-line SFC" (timeline), "967 lines" (glassmorphism) | timeline-stack **899** (exact match); glassmorphism-panel **972** (minor drift) |

Rule for the chapter (from the TAC-1 fan-out checklist): quote artifacts verbatim, and whenever the video and the committed file diverge, **state the divergence in adjacent prose** — "on screen Dan runs X; the committed asset ships Y."

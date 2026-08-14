# Infinite UI Agents — Nuggets for Weak Learners

Sixteen ranked nuggets in three tiers. Tier 1 = the spine you must be able to say out loud. Tier 2 = the mechanics that make it real. Tier 3 = the nuances and honesty flags that separate "watched the video" from "understood the asset." Each nugget: the insight, then **why it matters**.

---

## Tier 1 — The spine (know these cold)

**1. The harness is the product; the model is being commoditized.**
The Claude Code leak's real signal: a $2.5B business is built on the harness (deterministic code, token caching, agent orchestration, prompts, skills, model control), not the model on top.
*Why it matters:* it tells you where to invest — down a level, into the harness — while everyone else argues about model benchmarks.

**2. Stop solving one-off tasks; build teams that solve problem classes.**
Don't prompt an agent to build *the thing*. Build a team of agents that knows how to build (and operate) that whole *class* of things on your behalf.
*Why it matters:* 80–90% of engineering work is a repeatable workflow. Systematize the workflow once; run it forever.

**3. Three tiers: orchestrator → leads → workers. Leads and orchestrator don't write files.**
Orchestrator and leads think, plan, delegate, synthesize. Workers do the writing. Validators only report.
*Why it matters:* it mirrors how great human teams scale — and here it's enforced in code, not just asked for.

**4. Your input must not scale with the number of agents.**
You always talk to one orchestrator, no matter how many agents run behind it. Teams scale horizontally; your interface stays constant.
*Why it matters:* the moment driving the system grows with every added agent, *you* become the bottleneck the whole design exists to remove.

**5. Owning the harness = owning the core four (context, model, prompt, tools) per agent.**
Stock tools give you one blended agent with fixed defaults. The harness lets you set context, model, prompt, and tools independently for every agent.
*Why it matters:* this is the concrete payoff of "own the harness" — otherwise it's a slogan.

**6. The theme of 2026 is trust at scale.**
Harness engineering + multi-agent orchestration are the two skills; trust and scale underline both. Increase, over time, how much work you trust your agents to do — until they run the product end to end.
*Why it matters:* it's the north star that tells you whether you're building the right thing (closed, specialized, trustworthy systems) vs just spawning more agents.

---

## Tier 2 — The mechanics (how it actually works)

**7. Front matter is the specialization surface: expertise + skills + tools + domain.**
Each agent's YAML front matter sets its mental model (`expertise`), hot-loaded behavior (`skills`), capabilities (`tools`), and — the sleeper — the exact paths it may touch (`domain`).
*Why it matters:* "one agent, one prompt, one purpose" is real only because `domain` path-scopes the agent; without it, "front-end-only" is just a wish.

**8. `delegate` and `tilldone` are literally tools.**
Leads/orchestrator get `delegate(team, question)` and `tilldone`; workers get `write/edit/bash`; validators get neither write nor delegate.
*Why it matters:* the role differences aren't personality — they're the tool list. That's how the "leads don't write" rule is enforced.

**9. Agents keep persistent mental models and grow them across sessions.**
Each agent owns a YAML expertise file; a ~77-line skill teaches it to read it at task start and update it after work (rewriting stale entries, trimming to a line limit, validating the YAML). The human never edits it.
*Why it matters:* this is what "teams that remember" means — each round of work makes the next one better.

**10. `/generate` is an 8-step, multi-team, validated pipeline — not a single prompt.**
`/generate <brand> <product> <tree> <count> <brief>` → Setup scaffolds → Brand loads context → UI Gen writes N briefs → round-robin generate across A/B/C → Setup marks validating → round-robin validate across A/B/C → fix failures → Setup finalizes.
*Why it matters:* the value is the workflow the command drives, not the sentence you typed.

**11. Round-robin across parallel teams is how you scale generation.**
Branch 1→UI Gen, 2→UI Gen B, 3→UI Gen C, 4→UI Gen... same assignment mirrored to validation teams. Each branch dir is independent, so parallel writes don't collide.
*Why it matters:* it turns "one agent, one UI" into "three teams, three UIs at once" with no conflict-management burden on you.

**12. Reliability is engineered in: heterogeneous models + team redundancy.**
Different models per agent (Sonnet vs Minimax vs Step), swappable, with a possible rotation system; and if one team's worker dies, its lead — or another team — finishes the job.
*Why it matters:* the demo's open-source failures didn't stall the pipeline. Owning the harness makes a broken model survivable.

**13. Define brand once, generate infinitely — zero hardcoded values.**
Every generated leaf uses CSS custom properties from `brand.yaml`. Edit a token → everything rebrands live; change `brand.yaml` → the whole product rebrands.
*Why it matters:* it's what makes "brand-consistent at scale" true instead of aspirational — consistency is structural, not manual.

---

## Tier 3 — Nuances & honesty flags (the difference-makers)

**14. What you clone is NOT what's on screen.**
The committed asset ships all-Claude agents, empty mental-model stubs, one brand (aegis), and one config. On screen Dan runs a superset: `agents-os/` open-source variants, `multi-team-config-min.yaml`, a 7,753-token mental model, and three brands — hand-tuned, uncommitted.
*Why it matters:* clone it expecting the demo and you'll think it's broken. It isn't — you're starting from the base state and will grow the mental models yourself.

**15. The demo failing is the argument, not a bug.**
Open-source teams returned "no response"; leads broke the "don't write files" rule to finish. That's the reliability point made vivid: redundancy + rotation keep results flowing when a model dies.
*Why it matters:* weak students read the failure as "this doesn't work." Strong students read it as "this is exactly why you own the harness."

**16. Two on-camera details are imprecise — correct them.**
(a) Leaf previews are a real `<iframe>` + `import.meta.glob` dynamic component, not Vue Teleport (Teleport is only in the Sidebar). (b) `/generate` itself has no till-done list by design; the on-screen TillDone is the orchestrator's own `tilldone` tool.
*Why it matters:* if you audit the code trusting the narration, you'll go looking for the wrong things.

---

## Micro-quiz (self-check — answers below)

1. In one sentence: what did the Claude Code leak *signal*, and what should you do about it?
2. Who writes files in the three-tier system, and which two front-matter fields enforce the rule?
3. Name the four things an agent's front matter controls. Which one makes "front-end-only" scoping actually real?
4. You clone `ui-agents` and open `expertise/vue-generator-mental-model.yaml`. What do you find, and why isn't it the 7K-token file from the video?
5. The open-source teams failed on camera. Give two reasons that supports — rather than undermines — the tactic.
6. What does `/generate aegis app landing 3 "bold hero"` actually set in motion (name 3+ of the 8 steps)?
7. Where does the on-screen "till-done" list come from, given `generate.md` doesn't contain one?

<details><summary>Answers</summary>

1. That the agent harness — not the model — is the product (models are commoditizing); so invest in **harness engineering**, building specialized teams of agents you own.
2. **Workers** write files; orchestrator/leads don't. Enforced by **`tools`** (leads get `delegate`/`tilldone`, not the write path in practice) and **`domain`** (leads' `upsert:false` on `apps/`).
3. **context, model, prompt, tools** (the core four). **`domain`** — path-scoped read/upsert/delete — is what makes focused scoping real.
4. A **one-line stub** (`# Mental model — auto-maintained by agent`). The 7,753-token file is **runtime state** Dan accumulated; the committed repo ships empty stubs that grow (up to `max-lines: 10000`) as you run the agents.
5. (a) The **leads finished the dead workers' tasks** — nothing stalled. (b) Owning the harness means you can **rotate/swap models** and run **redundant teams**, so a broken model is survivable.
6. Setup scaffolds branch dirs + `trees.yaml`/`activity.yaml` + Zod → Brand loads `brand.yaml` → UI Gen writes 3 briefs → **round-robin** generate across A/B/C → Setup marks validating → round-robin validate → fix failures → Setup finalizes statuses.
7. The **orchestrator's own `tilldone` tool** (declared in `orchestrator.md`), used autonomously. `generate.md` deliberately omits a task list (a coordination stress-test in `specs/parallel-team-duplication.md`).

</details>

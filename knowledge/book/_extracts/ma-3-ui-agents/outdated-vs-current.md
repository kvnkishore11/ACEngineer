# Infinite UI Agents — Outdated vs. Current (course-era → mid-2026)

**Unusual for this lesson:** it is *already* current. Uploaded 2026-04-06, it references the Claude Code source-code leak, Sonnet/Opus 4.6, 1M-context models, Minimax M2.7, Step 3.5 Flash, and "the theme of 2026." So the "outdated" axis here is **not** a stale-tooling problem like TAC-1. It is two different things:

1. **Committed-asset vs. live-demo divergence** — what a reader clones is a snapshot; the video runs a hand-tuned superset. This is the dominant gap, and it's the chapter's chief honesty obligation.
2. **Forward drift** — model IDs and the pace at which the *mainstream* tool (Claude Code) is absorbing harness features.

Each gap below has a **book treatment** the chapter author should apply.

---

## Gap 1 — What ships ≠ what's on screen (the big one)

**Course-era artifact:** the committed member asset `ui-agents` is a single-commit (`7d36778`), all-Claude, empty-mental-model snapshot with one brand. The video runs a superset: `agents-os/` open-source agent variants, `multi-team-config-min.yaml`, mental models populated to ~7,753 tokens, three brands, and open-source models (`stepfun/step-3.5-flash`, `openrouter/minimax/minimax-m2.7`) swapped into specific agents.

**Why it matters:** a reader who clones the asset expecting the demo will think it's broken or incomplete. It isn't — they're starting from the base state.

**Book treatment:** carry the Accuracy Ledger table (in `extract.md`) as a boxed "What you clone vs. what Dan runs" sidebar. Every time the chapter quotes an on-screen model ID, mental-model size, or brand count, add the committed value in adjacent prose. Frame the difference positively: the empty stubs *are* the feature — they grow as you run the system.

---

## Gap 2 — Model IDs are period-specific and will drift fastest

**Course-era artifact:** `anthropic/claude-sonnet-4-6` / `claude-opus-4-6`, `stepfun/step-3.5-flash`, `openrouter/minimax/minimax-m2.7`, the 1M-context Sonnet/Opus, and the "Mythos model" leak reference are all April-2026 specifics.

**Why it matters:** these names age in weeks, not years. A chapter that leans on them reads dated on publish.

**Book treatment:** teach the *durable* claim — **the harness lets you set and rotate the model per agent** — and treat every ID as period detail (label it "as of April 2026"). Keep the reliability lesson (Sonnet proved reliable; open-source teams struggled) as a transferable point about *matching model capability to workload and building in redundancy*, not as a verdict on any specific model. Re-verify all model names at publish.

---

## Gap 3 — The mainstream tool is absorbing the harness

**Course-era framing:** "own the harness with Pi" is sharpest when the mainstream tool (Claude Code) is a black box you can't customize.

**Why it matters:** Claude Code now exposes subagents, hooks, skills, plugins, output styles, permission modes, and settings layering — a large slice of the very harness surface Dan builds in Pi. `plan-w-team.md` in this repo already documents Claude Code's own multi-agent `TaskCreate`/`addBlockedBy` API.

**Book treatment:** don't present it as "Pi vs. Claude Code." Present the *principle* — whoever controls context/model/prompt/tools + orchestration wins — and note that the open question is **how much you build yourself vs. configure in a tool that's catching up**. Dan's own answer ("in ands not ors," ~80% in Claude Code as meta-agent) is the honest resolution. This axis moves fast; date the claim.

---

## Gap 4 — Till-done in the demo vs. the committed `/generate`

**Course-era artifact:** on screen the orchestrator runs a `TillDone` list ([1/8] → [11/11]). The committed `generate.md` carries **no** task list.

**Why it matters:** a reader auditing `generate.md` to "find the till-done logic" won't find it and may think the video is faked.

**Book treatment:** explain the reconciliation once, clearly: `tilldone` is an **orchestrator tool** (declared in `orchestrator.md`), used autonomously for substantial work; `generate.md` deliberately omits a task list per `specs/parallel-team-duplication.md` (a coordination stress-test — "can the orchestrator coordinate three parallel teams from context + trees.yaml + activity.yaml alone?"). Both facts are true.

---

## Gap 5 — The leaf-preview mechanism vs. Dan's on-camera guess

**Course-era artifact:** Dan narrates the previews as "teleport which probably uses iframe underneath."

**Why it matters:** it's an on-the-fly guess, and a reader who trusts it will go hunting for Vue `Teleport` in the preview path.

**Book treatment:** state the real mechanism plainly — a real `<iframe>` (1280×720, CSS-scaled, `pointer-events:none`) into the leaf's gallery route, which uses `import.meta.glob` + a dynamic `<component :is>`; Vue `Teleport` is used only in `Sidebar.vue`. This is a good "read the code, don't trust the narration" teaching beat.

---

## What has NOT aged (teach as durable principles)

These are the load-bearing ideas; none is tied to a tool version:

- **The harness is the leverage point.** Whoever controls context/model/prompt/tools + orchestration — regardless of tool — has the edge. Models commoditize; the harness endures.
- **Solve problem classes, not tasks.** Build teams that operate a whole domain; 80–90% of work is a repeatable workflow.
- **Three tiers with enforced roles.** Orchestrator/leads delegate and don't write; workers do; validators report. Enforce structurally (tools + domain), not by request.
- **One orchestrator interface.** Input must not scale with agent count.
- **Specialization = one agent, one prompt, one purpose,** via expertise + skills + tools + domain (focused context).
- **Agents that keep persistent mental models** — observe, act, learn, iterate; knowledge compounds across sessions.
- **Reliability by design** — heterogeneous, swappable models + redundant teams; a broken worker is survivable.
- **Trust and scale as the north star** — build closed, specialized systems so you can trust them with ever-larger work.
- **Claude Code as meta-agent** — build the system that builds/operates the system; "in ands not ors."

---

## Strict overlay decision (Current-Practice YouTube, map-to-lesson only)

Per the locked plan: overlays must be strict map-to-lesson / named-gap, IndyDevDan's own channel, max 1–3 `include_in_phase1`. This lesson names its own gaps in-video, which makes the choice clean.

**Include in phase 1 (2 cards):**

| ID | Title | maps_to | Why |
|---|---|---|---|
| `M30gp1315Y4` | Agent Teams (Multi-Team Agentic Coding) | named hole | Dan explicitly links this in-lesson as the video covering the multi-team **harness** UI Agents runs on top of ("we covered that last week... an implementation of the multi-team agent harness"). Fills the single biggest named gap — this lesson *assumes* the harness and only shows an implementation of it. Prerequisite viewing. |
| `TqjmTZRL31E` | Pi CEO Agents | named hole | The first asset in the trilogy (CEO → lead → UI agents) this lesson positions against; Dan references CEO agents for strategic decisions. Grounds the "systems of agents" lineage. |

**Deliberately excluded / not overlays:**
- **Pi Coding Agent (pi.dev)** and **Learn Pi From Zero (github.com/disler/pi-vs-claude-code)** — a tool site and a repo, not videos. List as `reference` resources, not overlays.
- **Claude Code (anthropic.com/claude-code)** — vendor page, reference only.
- **Agentic-security news links** (Autonomous AI Cybercrime, Claude Code RCE, OpenClaw, InversePrompt, Agentic Attack Chains) — third-party context Dan flashes for the Aegis domain; cite as references if the chapter treats the agentic-security angle, but they are not IndyDevDan overlays.

**Cap honored:** exactly 2 `include_in_phase1: true` (≤3). IDs are taken from the lesson's own description reference list (high confidence); **oembed-verify they resolve before publishing links**, exactly as the TAC-1 cross-review did. No 3rd card is added because no additional IndyDevDan video in the reference list maps cleanly to a named hole without topic drift.

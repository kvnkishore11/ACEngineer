# MA-4 — Outdated vs Current (recording era → mid-2026)

This is a very recent lesson (April 2026 model cycle; captured ~3 months before this pass), so almost nothing has *aged* — the drift is mostly **internal inconsistency between the recorded demo, the README prose, and the files actually on disk**, plus the usual "specific model names are period detail" caveat. The pattern itself — a read-only observer agent that decomposes into atomic claims and re-prompts on failure — is current. For each item: what the lesson/repo shows, what's actually true now, and whether the book needs a note or overlay.

---

## 1. Verifier model: video (GLM 5.1 / GPT-5.5) vs shipped persona (`openai/gpt-5.5`)  ⟵ document explicitly

**Recording era:** the image verifier runs **GPT-5.5**; the SQLite verifier runs **GLM 5.1**. Frame `t1200` literally shows `verify_sqlite.md` with `model: z-ai/glm-5.1`, and the transcript confirms "we're using the GLM 5.1 model." Builder is **Opus 4.7** throughout.
**Current (on disk):** all four personas (`verifier`, `verify_sqlite`, `verify_image`, `verify_python`) declare `model: openai/gpt-5.5`. The `z-ai/glm-5.1` line was changed to `openai/gpt-5.5` at some point after recording.
**Why it doesn't matter (and why to teach it):** the model is a **single frontmatter line**, and swapping it is the literal "stack intelligence / AND not OR" point. Nothing is broken. A reader reproducing the lab should expect `gpt-5.5` by default and set it to whatever cracked model they prefer.
**Book treatment:** margin note on any model-bearing frame ("video used GLM 5.1 / GPT-5.5; the shipped default is `openai/gpt-5.5`; the model is one line — that's the point"). No overlay.

## 2. README "Known limitations (v1)" vs the richer shipped tree  ⟵ trust the files

**Repo prose says:** "One domain ships: SQLite. Other domains follow the pattern above but aren't included. A stub `verifier.md` is present as a non-functional placeholder." Prose in a couple of places also says the default persona is `verify_sqlite`.
**On disk it's fuller:** `verifier.md` (generic) is a **full working persona**, and `verify_image.md` + `verify_python.md` ship with their scripts (`verify_python.py`). The code default in `verifiable.ts` (`attach()`) is the **generic `verifier`**, not `verify_sqlite`. `install.md` even has one stale line (`DEFAULT_MODEL: anthropic/claude-sonnet-4-6`) contradicted by its own Step 6 (`openai/gpt-5.5`).
**Current reality:** this local build (`the-verifier-agent-system`) is the fuller, members-style build. The free public GitHub repo is the *basic* version; the members "souped-up" version adds the specialized verifier experts + the gpt-image-2 skill.
**Book treatment:** callout — "the README's v1-limitations paragraph lags the shipped files; when they disagree, the files (and the code default) win." No overlay. Tell the reader to check what *their* clone actually contains.

## 3. Harness: built on Pi → the same shape is buildable in Claude Code / Agent SDK

**Recording era:** the whole system is a custom **Pi** harness because Pi lets Dan lock input, narrow tools (`--tools`), override bash at the tool-call layer (`pi.on("tool_call")`), auto-spawn a child in tmux, and render `--system-prompt`. He's explicit: "own your agent harness... this one is yours."
**Current:** the *concept* is harness-agnostic. Any tool that gives you (a) a lifecycle "stop" hook, (b) a way to read the builder's transcript, (c) a tool allowlist, and (d) a tool-call gate can host the same pattern. Claude Code specifically offers `Stop` / `PreToolUse` / `PostToolUse` hooks, a permission allowlist, and the Claude Agent SDK (Python/TS) for programmatic multi-agent control — the current idiom for building a verifier outside Pi.
**Book treatment:** sidebar — "you don't need Pi; you need harness control. Here's the same shape in Claude Code hooks + the Agent SDK." Concept unchanged.
**Overlay:** none of the seed IDs map cleanly; leave unlinked pending a verified Claude-Code-hooks/Agent-SDK video.

## 4. Models & tool velocity: period detail by design

**Recording era:** April 2026's "highest model-release velocity ever" — Opus 4.7, GPT-5.5, DeepSeek V4, GLM 5.1, Kimi K2.6, the Qwen series — is the cold-open framing. A Pi website update even flashes on screen mid-lesson.
**Current:** the specific model roster and Pi's UI keep moving; the lesson's own thesis pre-handles this ("model performance is no longer the bottleneck — it's you and I"). The verifier pattern is deliberately *above* any single model.
**Book treatment:** one-line margin note on model-name-heavy moments ("roster is period detail; the pattern is model-agnostic — that's the AND-not-OR point"). No overlay.

## 5. Multi-agent scope: one verifier shown → stacks, teams, orchestration

**Recording era:** one builder + one verifier, one specialized verifier at a time — deliberately simplified. Dan says you *can* stack multiple verifiers ("hint hint") but doesn't show it, and contrasts it with the three-layer orchestrator/leads/workers architecture and Stripe's blueprint system covered elsewhere.
**Current:** the ceiling is much higher — stacked specialized verifiers, teams of agents, full orchestration, the "codebase singularity." The verifier is the *entry* multi-agent system, not the frontier.
**Book treatment:** forward-pointer ("this is the simplest multi-agent system; MA/AH scale it to teams and orchestration"). Overlay the two named siblings.
**Overlay candidates:** `RairMJflUSA` — *Multi-Agent Teams* (include_in_phase1: **yes**); `V5A1IU8VVp4` — *Stripe Blueprint Agents* (include_in_phase1: **yes**).

## 6. Agentic security (the bash tool): taught here, deep-dive teased

**Recording era:** the lesson locks bash to one script and names the bash tool the biggest hole in everyone's agent, then teases a dedicated video on "agentic security — damage from within" (explicitly *not* prompt injection).
**Current:** at capture time that video wasn't published, so there's no ID to overlay yet.
**Book treatment:** flag for a later refresh — pair the three-layer read-only model here with that security deep-dive when it lands. No phase-1 overlay.

---

## What has NOT aged (teach with full confidence)

- **The two constraints** (planning + reviewing) as the frame for where an engineer's time goes — the verifier's whole justification.
- **Atomic-claim decomposition** as the definition of verification; "the agent's prose is a claim, never proof."
- **Spend tokens to save time** — costs shift, the logic doesn't; the trade only sharpens as tokens get cheaper.
- **Trust AND scale** as the reason this pattern is special (most moves trade one for the other).
- **Template-your-engineering-by-force** via the un-promptable input lock — a design principle, not a tool detail.
- **Read-only by architecture, three layers, enforcement outside the model** — timeless security posture; "the error message is the documentation."
- **Bash is the most dangerous tool** — restrict it to one script. Do-it-today advice regardless of harness.
- **AND, not OR** — combinations of models beat any single model; benchmarks that test one model miss it.
- **The positive feedback loop** ("what could you not verify / what do you need from me") — the flywheel that makes verifier accuracy compound.
- **Own your harness** — control over the tool surface and lifecycle is the prerequisite for all of the above.

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| 1 | `RairMJflUSA` — Multi-Agent Teams | named hole (where the verifier sits in the bigger multi-agent picture) | ✅ |
| 2 | `V5A1IU8VVp4` — Stripe Blueprint Agents | operationalizes tactic (Camp B / code+agents in production) | ✅ |
| 3 | *(unpublished)* Agentic Security — the bash tool | named hole (deep-dive on the lesson's security teaser) | ❌ no ID yet |

*Caveat: IDs/titles are taken verbatim from this lesson's own description/resources (Dan names both in-lesson); verify each resolves and content matches title before publishing overlay links (no video fetching performed in this extract pass, per brief). The security deep-dive had no ID at capture time — do not overlay until it resolves.*

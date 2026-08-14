# MA-4 · The Pi Verifier Agent — Master Teaching Notes

> Source of truth for the expanded chapter. Video 32:51 · Advanced (top-20% shipping engineers) · Tactic: **The Verifier Agent — spend tokens to save time; verify by architecture**
> Lesson artifact: a custom two-process Pi agent harness — one builder, one read-only verifier — talking over a private unix socket. The verifier watches, decomposes every claim into atoms, proves each deterministically, and re-prompts the builder *unprompted* when a proof fails.

**Lesson thesis in one sentence:** Agentic engineering has exactly two binding constraints — planning and reviewing — and the verifier agent crushes the review side by putting a second, read-only, model-different agent behind your builder that proves every atomic claim and corrects it automatically, so you spend 2–5× the tokens to buy back the one thing tokens can't: your time.

**The chapter must land nine ideas.** Each below follows: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q.

---

## Idea 1 — The Verifier Agent: two agents, one watches the other

**Hook.** Two Pi agents sit side by side and one of them takes no input. You prompt the builder on the right; the moment it finishes, the agent on the left springs to life on its own — reading, checking, and (if needed) prompting the builder back. Dan's hands never touch the keyboard. "How does it work? And what's missing from every benchmark?"

**Picture.** Frame t0080 (1:20): the split screen — builder Pi (`claude-opus-4-7`, "verifier connected") beside the verifier Pi (`VERIFY_IMAGE`, `gpt-5.5`, "connected to builder") whose input box shows a green *locked-cursor* ring. Frame t0478 (7:58): the hero diagram — `BUILDER ←unix socket · JSONL→ VERIFIER · input locked`, `session.jsonl` feeding the verifier, an "only bash: uv run verify_sqlite.py" box, and a "defense in depth" footer.

**Worked example.** `just vimg` boots exactly this: `verifiable.ts` (builder side, owns the socket server + spawns the child) and `verifier.ts` (child side, input-locked status bar + the `verifier_prompt` tool). On the builder's `agent_end`, `verifiable.ts` fires a `stop` event over the socket; `verifier.ts` renders `verify_on_stop.md` and injects it via `pi.sendUserMessage`. The verifier reads the builder's session-JSONL slice and runs its checks. No transcript ever crosses the wire — only lifecycle ticks.

**Dan's term.** *The verifier agent* — "a very simple two-agent system where on completion of any prompt that executes, the verifier is kicking off and doing work." A **top-down observer**: the builder doesn't know the verifier exists.

**Failure mode.** Filing this as "sub-agent delegation." It isn't — nobody delegated anything, the builder is unaware, and the verifier speaks only when a proof fails. The weak student pictures a chat between two bots; the reality is one agent silently proving another's claims and pushing exactly one kind of message back (a correction).

**Retrieval Q.** What triggers the verifier, and what crosses the socket? *(The builder's `stop` event triggers it; only lifecycle ticks — start/stop/error — cross the socket. The verifier pulls substance from the builder's session JSONL on disk.)*

---

## Idea 2 — The two constraints of agentic coding: planning and reviewing

**Hook.** If you're doing agentic engineering *right*, where does your day actually go? Not typing. Two places only: how much you can **plan**, and how much you can **review**. Most engineers drown on the review side — half the day re-checking "I created the table / added the foreign key / applied the migration" by hand.

**Picture.** Frame t0360 (6:00): a real Report doing the reviewing *for* you — atomic claims listed, a readability rule that fired, `atomic_claims_total: 6 / verified: 5 / failed: 1`, and the concrete corrective feedback. The review labor made mechanical.

**Worked example.** The `verify_on_stop.md` template plus a domain persona *is* your review checklist, executed by a machine every turn. The SQLite persona spells out the heuristics you'd apply by hand — "builder declares a FK → run `PRAGMA foreign_key_list`; builder claims a migration applied → `.schema` and diff" — so your reviewing becomes the persona's job, not yours.

**Dan's term.** *The two constraints — planning and reviewing.* "With the verifier agent, we can improve our review constraint... by teaching an agent exactly how we verify, by adding these rules, by making them read the files that you would read."

**Failure mode.** Thinking "review" means skimming the agent's summary paragraph. In this system the agent's prose is a **claim, never proof** — every `verified` verdict must cite a deterministic tool output (a `PRAGMA` row, a `SELECT count(*)`, an exit code, the actual image bytes). A student who trusts the summary has re-created the exact problem the verifier exists to kill.

**Retrieval Q.** Name the two constraints and which one the verifier attacks. *(Planning and reviewing; it attacks reviewing by templating how you verify and re-checking every turn against actual state.)*

---

## Idea 3 — Atomic claims: the art of verification is decomposition

**Hook.** Every prompt you fire is a bundle of little truths. "Find all the SQLite DBs and break down the tables and relationships" is not one thing to check — it's a dozen. The verifier's whole skill is pulling that bundle apart into the smallest propositions that can each be proven true or false.

**Picture.** Frame t1180 (19:40): the SQLite verifier's Report — a wall of individually-proven atoms (`PRAGMA index_list(orders)`, `SELECT count(*)` per table, `PRAGMA integrity_check → "ok"`), ending `atomic_claims_total: 16, verified: 16, failed: 0`. Frame t0420 (7:00): the image version — 7 discrete visual claims, 7/7.

**Worked example.** The persona forces it: *"'I created the users table' is at least five claims (table exists, columns X/Y/Z, primary key on id, FK constraints declared, defaults applied). Pull each apart, validate each independently... A single PASS that hides three unverified sub-claims is worse than three explicit FAILs."* The verifier then routes each atom to a check via the one allowed script.

**Dan's term.** *Atomic claims / small axioms.* "Everything you prompt into your agents, they're all small axioms... units of information that can be proven true or proven false."

**Failure mode.** Accepting a single top-level "✅ done." Granularity IS the value — the coarse PASS is exactly where silent 14%-of-records-skipped bugs hide. The weak student measures success at the bundle; the verifier measures it at the atom, each atom tied to a tool output.

**Retrieval Q.** What is an atomic claim, and why is one big PASS worse than several explicit FAILs? *(The smallest independently-provable proposition; a single PASS can hide unchecked sub-claims, so honest granular FAILs are more trustworthy than a coarse PASS.)*

---

## Idea 4 — Spend tokens to save time

**Hook.** Watch the token meters: the builder burned ~1–4% of its context; the verifier burned 2–5× that. If you're optimizing for tokens, this looks insane — you're paying multiples to check work that "looks fine." But you're not optimizing for tokens. You're optimizing for the one resource you can never get back.

**Picture.** Frame t1180 (19:40): the disparity on screen — builder `claude-opus-4-7` at **1%** beside verifier `z-ai/glm-5.1` at **9%**. Frame t0178 (2:58): the builder itself spending 75 seconds and real money driving GPT Image 2 — compute, spent deliberately.

**Worked example.** In the image demo the split is ~4% Opus vs ~23% GPT-5.5 — "quite literally spending 5x tokens." In the SQLite demo the verifier spends ~2× the builder. Either way the trade is identical: burn compute now so you don't burn an hour re-reviewing later. `README.md` states it flat: "Tokens are cheap. Your time is not. Spend tokens to generate value and time."

**Dan's term.** *Spend tokens to save time* / *scale compute to scale impact.* "How much is your time worth? If you ask me, your time is worth a ton."

**Failure mode.** Reading the token meter as a cost to minimize and killing the verifier to "save money." That's optimizing the cheap resource and spending the expensive one. The math only makes sense once you price your own time in — then paying tokens to reclaim hours is the highest-leverage trade on the board.

**Retrieval Q.** State the trade in one line and the two quantities being exchanged. *(Spend tokens to save time — exchange cheap, falling compute for your scarce, expensive review hours.)*

---

## Idea 5 — Trust AND scale: the rare pattern that does both

**Hook.** Almost every agentic move forces a choice. Review more deeply and you slow down (scale ↓). Push more compute through and you trust any single output less (trust ↓). Dan says the verifier is the rare pattern that refuses the trade — it moves *both* levers up at once. Don't skip this; dial into it.

**Picture.** Frame t0196 (3:16): the "UNPROMPTED" moment — more work happening automatically (scale) that simultaneously *proves* the builder's output (trust). Frame t1200 (20:00): the read-only, bash-locked persona frontmatter — the trust half made structural.

**Worked example.** Same run, both axes: the verifier does *more* (2–5× the tokens, a whole extra agent's worth of work → scale) AND makes the result *more trustworthy* (every atomic claim now has a deterministic check behind it before you read "done" → trust). More work + more proof, at once.

**Dan's term.** *Trust and scale.* "The verifier sits at a very important middle ground between trust and scale. Most agents increase trust or scale, not both. The verifier does both." And the year's theme: "2026 is the year of trust."

**Failure mode.** Believing "more agents = more errors, always." True only if you don't *engineer* them. With the right core four and a harness you control, the second agent lowers your error rate. The weak student adds an un-engineered agent, watches errors rise, and wrongly concludes multi-agent doesn't work.

**Retrieval Q.** Why is the verifier unusual on the trust/scale axes? *(Most agentic moves trade one for the other; the verifier raises both — it does more work AND attaches a deterministic proof to every claim.)*

---

## Idea 6 — Template your engineering — by force

**Hook.** Here's the part that feels wrong the first time: you *cannot type at your own verifier.* Its input bar is dead. When it misses something, you can't lean over and tell it what to do. Annoying? "It's the point."

**Picture.** Frame t0835 (13:55): the persona file open in VS Code — the verification heuristics, the tool policy, the rules. This markdown file, not a chat box, is where every behavior change happens. Frame t0246 (4:06): the only channel that *does* touch the builder — `verifier_prompt ✓ ack: prompt delivered to builder`.

**Worked example.** Two independent locks enforce it: `verifier.ts` swaps the editor for a `CustomEditor` that swallows typing, *and* `pi.on("input")` rejects any non-extension input. The only thing that can drive the verifier is `verify_on_stop.md` rendered against a real `stop` event. So when the ≤10-block rule needs to exist, you don't prompt it in — you add `MAX_TEXT_ELEMENTS: 10` to `verify_image.md`, and now *every* image is checked against it, forever.

**Dan's term.** *Template your engineering (as a habit, by force).* "There's no vibe coding this stuff. I cannot just fire a one-off prompt... I am forced to template my engineering into my verifier agent." Fixing anything means improving *one or more of the core four — context, model, prompt, or tools.*

**Failure mode.** Treating the input lock as a bug to route around. The lock is the mechanism: remove one-off prompting from the menu and the only move left is the one that compounds — solving the whole problem class instead of the single instance you happened to hit. "One-off prompts solve the instance; templated verification solves the class."

**Retrieval Q.** Why can't you prompt the verifier, and what must you do instead? *(Its input is locked by design — two independent layers; the only fix for a miss is editing the persona, script, or prompt template, which solves the entire class.)*

---

## Idea 7 — Read-only by architecture: the bash tool is the ticking time bomb

**Hook.** Security vulnerabilities are going parabolic; agents losing the plot are going parabolic. The single most dangerous tool you hand an agent is **bash** — "a ticking time bomb." An LLM that *decides* to run `rm -rf` cannot be talked out of it by a nice system prompt. So don't ask nicely — make it impossible.

**Picture.** Frame t1200 (20:00): `verify_sqlite.md` frontmatter — `tools: read, grep, find, ls, bash, verifier_prompt` and `bash_policy: { mode: script-only, allowed_script: verify_sqlite.py, runner: "uv run --script" }`. The lockdown as configuration. Frame t1052 (17:32): `just` — each recipe boots a different specialized, restricted verifier.

**Worked example.** Three independent layers, all outside the model, all must fail before anything mutates: **(1)** the persona's `tools:` list has no `write`/`edit`, so Pi never registers them; **(2)** a `pi.on("tool_call")` hook blocks any bash that doesn't start with `uv run --script verify_sqlite.py` and feeds the block reason back as a *teaching message* ("the error message is the documentation"); **(3)** `verify_sqlite.py` opens the DB `mode=ro&immutable=1` and enforces a PRAGMA allowlist, so even a mutation reaching the script is refused by SQLite itself. Authentication is the `/tmp/pi-verifier/` dir at `chmod 0700` — only your UID can connect.

**Dan's term.** *The bash tool is the most dangerous tool / a ticking time bomb.* "I've restricted it to using just one script. This is the highest level of control you can give." Read-only *by architecture*, not by prompt.

**Failure mode.** Believing a persona that says "please be read-only" is secure. Prompts are not enforcement. And a second trap: assuming this is a sandbox — it isn't. It stops the *verifier* from being a source of mutation; a malicious prompt that gets the *builder* to run `rm -rf` is a separate concern, and an untrusted persona can declare its own `allowed_script`. Pin your personas.

**Retrieval Q.** Name the three read-only layers and where each runs. *(Persona tools allowlist — no write/edit registered; tool-call bash hook — non-matching bash blocked with a teaching message; the script itself — ro&immutable connection + PRAGMA allowlist. First two run before any subprocess; the third inside the process.)*

---

## Idea 8 — It's AND, not OR: stack intelligence, own your harness

**Hook.** Every model benchmark on earth makes the same mistake from an engineer's seat: it tests *one model in isolation*. But you're not shipping a benchmark. The real frontier isn't "Opus 4.7 **or** GPT-5.5?" — it's Opus 4.7 **and** GPT-5.5, one building and a *different* one checking, each catching what the other misses.

**Picture.** Frame t1180 (19:40): the AND made literal — `claude-opus-4-7` builds, `z-ai/glm-5.1` verifies, in the same run. Frame t1052 (17:32): the `just` recipe list — the harness you own, one command per specialized verifier.

**Worked example.** The persona's `model:` field pins the verifier's model independent of your global default, so a two-model system is one frontmatter line. In the video the builder is Opus 4.7 while the image verifier runs GPT-5.5 and the SQLite verifier runs GLM 5.1 — three cracked models, orchestrated. And because it's *your* harness (Pi), you can lock input, narrow tools, override bash, and auto-spawn — none of which a stock tool that "changes underneath your feet" reliably lets you do.

**Dan's term.** *Stack intelligence. Orchestrate intelligence.* "It's not about GPT 5.5 or Opus 4.7. It's GPT 5.5 and Opus 4.7. It's an and, not an or." Plus: *own your agent harness* — "this one is yours... it doesn't change underneath your feet."

**Failure mode.** Chasing the single "best" model and running your builder and reviewer on the *same* one — one perspective at one moment of compute, blind to its own misses. The AND is the point: a different verifier model is a second, independent perspective.

**Retrieval Q.** Why "AND, not OR," and what one line makes it real? *(Combinations beat any single model — a builder model plus a different verifier model catch each other's misses; the persona `model:` field pins the verifier's model, so it's a one-line change.)*

---

## Idea 9 — Two camps, one year of trust (the stakes)

**Hook.** There's a widening gap between two kinds of 2026 engineer. Camp A is stuck prompting back and forth with a single agent — which, Dan warns, will feel in 2026 like hand-typing code felt in 2025. Camp B builds systems like the verifier: coordinated agents that scale. The verifier is the simplest door from A into B.

**Picture.** Frame t0196 (3:16): "UNPROMPTED" — Camp B in one word (the system acting on its own). The repo's own `images/07-two-camps.svg` renders the contrast directly: Camp A (prompt → babysit → re-prompt) vs Camp B (build · verify · feedback · repeat).

**Worked example.** The whole lesson performs the crossing: Dan starts by prompting one builder (Camp A), then the verifier turns it into a coordinated pair that builds, verifies, and self-corrects with his hands off the keyboard (Camp B). "You don't want to be working on your application anymore... you work on the agentic system, the system that builds the system."

**Dan's term.** *Two camps* / *the year of trust.* "Vibe coding is the floor. Agentic engineering is the ceiling that no one has even imagined the capabilities of yet." "2026 is the year of trust. Do you trust your agents to do what you ask them to? And then, how much? At what scale?"

**Failure mode.** Hearing the stakes as motivational garnish and skipping to the code. The stakes are load-bearing: every design choice (input lock, atomic claims, bash policy, model diversity) is justified by "does this increase *trust* or *scale*?" A student who skips the framing evaluates the verifier by comfort instead of by those two axes.

**Retrieval Q.** What separates Camp A from Camp B, and what two words define the winning formula? *(Camp A prompts a single agent back and forth; Camp B builds coordinated multi-agent systems. Trust and scale.)*

---

## Timeline map (transcript-verified; chapter anchors from the video's own chapters)

| Time | Beat |
|---|---|
| 0:00–1:35 | Cold open: April 2026 model-release velocity; "model performance is no longer the bottleneck — it's you and I"; two agents, one takes no input |
| 1:35–3:05 | Image example: prompt builder (Opus 4.7) to /prime + run gpt-image-2 skill → generate arch.jpg (~75s) |
| 3:05–4:10 | Verifier (GPT-5.5) kicks off **UNPROMPTED**; reads the image; finds a problem; **prompts the builder back** |
| 4:10–6:10 | Clone the first (overloaded) diagram as backup; break down the FAILED Report — violates the readability contract (>10 text blocks) |
| 6:10–9:40 | Rebuild → VERIFIED / PERFECT (7/7); value props: spend tokens to save time, review constraint, positive feedback loop, template-by-force; second "add us in" round |
| 9:40–12:15 | **The two constraints** — planning & reviewing; one agent/one prompt/one purpose; stack specialized verifiers |
| 12:15–16:40 | The customized system prompt (rules + Report format); template your engineering by force; Camp A vs Camp B |
| 16:55–19:35 | SQLite example: `just` recipes → `just vsql` (GLM 5.1); verifier independent of builder; decompose into atomic claims |
| 19:35–22:40 | Restricted bash (one script); "most dangerous tool"; 16/16 verified; ~2× token spend; trust via atomic-claim validation |
| 23:00–25:38 | What's missing from every benchmark: one model in isolation; **AND, not OR**; stack/orchestrate intelligence; own your harness |
| 25:38–30:25 | TAC / Agentic Horizon pitch; vibe-coding-is-the-floor; operate on the agentic layer; two versions of the verifier shipped |
| 30:25–32:51 | Channel focus: trust & scale; year of trust; verifier does both; teaser — agentic security & the bash tool |

## Terminology glossary (Dan-isms, canonical spellings)

- **The verifier agent** — a read-only observer agent that proves a builder agent's atomic claims and re-prompts it on failure
- **Builder / verifiable** — the primary interactive agent (Dan sometimes calls it "the verifiable"); the thing being verified
- **Atomic claim / small axiom** — the smallest proposition with an unambiguous truth value
- **The two constraints** — planning and reviewing (the verifier attacks reviewing)
- **Spend tokens to save time** — trade cheap compute for scarce review hours
- **Trust and scale** — the two axes; the verifier raises both
- **Template your engineering** — encode fixes into the persona/script/prompt, never a one-off; forced by the input lock
- **Positive feedback loop / flywheel** — "what could you not verify / what do you need from me" → next thing to template
- **Top-down observer** — the builder doesn't know the verifier exists
- **The core four** — context, model, prompt, tools (what you're forced to improve)
- **bash_policy: script-only** — bash locked to one allowed script; "the error message is the documentation"
- **Stack / orchestrate intelligence** — combine multiple models (AND, not OR)
- **Own your agent harness** — control the tool that doesn't change under your feet
- **Camp A / Camp B** — single-agent prompters vs multi-agent system builders
- Transcript ASR corrections: "JLM 5.1"→GLM 5.1, "pie coding"→Pi coding agent, "Andy Dev Dan"→IndyDevDan, "GBT image"→GPT Image, "agenda coding"/"agent decoding"/"AGC"→agentic coding, "Kimmy Cat 2.6"→Kimi K2.6, "Quinn"→Qwen

## Bridge to the rest of MA / the channel (as trailed in-lesson)

- The verifier is the *simplest* multi-agent system; the three-layer orchestrator/leads/workers architecture is the complex sibling (Multi-Agent Teams, `RairMJflUSA`)
- Stripe's blueprint "code + agents" system as Camp B in production (`V5A1IU8VVp4`)
- You can *stack* multiple specialized verifiers behind one builder (teased, not shown)
- Next up on the channel: **agentic security** — "damage from within," the bash tool as the biggest hole in everyone's agent (teased, unpublished at capture)
- Constant thread: increase **trust**, scale your agents — "that's it, that's what we're going to do for the rest of the year"

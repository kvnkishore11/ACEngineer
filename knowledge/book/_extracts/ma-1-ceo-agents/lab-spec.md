# MA-1 Lab Spec — CEO Agents

**Scope rule:** every drill runs inside the **course codebase only** (`agentic-horizon-extras/ceo-agents`, symlinked as `ma-1-ceo-agents/codebase`). It is member-exclusive — no public clone. No external repos.
**Prime directive (graded throughout):** you build and change agents by **editing prompts, config, and briefs** — you author *briefs and system prompts*, not application code. The one code touch allowed is reading the extension to verify how it works (Part 4).
**Time box:** 60–90 minutes. **Token/$ cost:** 3–6 deliberations. Start with the demo's $1–$5 budget; raise it only for the "real decision" in Part 2 (size it to how much the decision is worth — that's the lesson).

Prereqs installed and keyed: **Pi**, **Bun**, **just**, `.env` with `ANTHROPIC_API_KEY` (and optionally `ELEVENLABS_API_KEY` for audio).

---

## 0 · Read the machine before you run it (10 min)

1. Boot: `just ceo` (or `j ceo`). Confirm the roster screen shows the CEO on `claude-opus-4-6` and the board on `claude-sonnet-4-6`, all badged **1M**, with the Time/Budget/Editor constraints. *(Frame `t0585`.)*
2. Open `.pi/ceo-agents/ceo-and-board-configuration.yaml` and answer **in writing**:
   - What are the min/max **time** and **budget**?
   - What four **required brief sections** must every brief contain?
   - How many **board members** are active, and what is each one's TUI color?
3. Open `.pi/ceo-agents/agents/moonshot.md` and name its `CORE_BIAS`, `RISK_TOLERANCE`, and `DEFAULT_STANCE`.

**Checkpoint 0 (graded):** without looking, state what the system takes in, what it returns, and the two ways a meeting can be forced to end (max time, max budget). If you can't, re-read — this is the "know your inputs/outputs/constraints" habit.

## 1 · Reproduce Dan — run a shipped brief (15 min)

1. `/ceo-begin` → select **`2026-03-18-acquisition-offer`**.
2. Watch a full deliberation. As it runs, note out loud:
   - the CEO's opening `converse("all", …)`,
   - the board **all responding at once** (parallel),
   - the **TIME/BUDGET gauges** advancing,
   - the moment **[MAX REACHED]** forces the wrap. *(Frames `t0760`, `t0900`.)*
3. When the memo opens in your editor, find: the ranked recommendation (#1–#3), the **board-stances table**, **Moonshot's dissent**, and the **next actions**. *(Frame `t0468`-style output.)*

**Checkpoint 1 (graded, write it down):**
- What did the board vote? (It will differ from the video's "5–1" — record *your* run's tally.)
- Which member dissented, and what did the dissent add to the memo that a single-agent answer would have missed?

## 2 · Author your own brief — a real decision (20 min)

1. Copy `.pi/ceo-agents/briefs/brief-template.md` into a new dir `briefs/<today>-<your-slug>/brief.md`.
2. Fill **all four** required sections for a decision you actually face (a tech-stack bet, a job offer, a pricing change). Be specific — "garbage in, garbage out."
3. Add **at least one context file** (`metrics.md`, `constraints.md`, whatever's relevant) in the same directory.
4. **Prove validation works:** temporarily delete your `## Constraints` heading, run `/ceo-begin`, and confirm the meeting is **blocked with a missing-section notice**. Restore it.
5. Raise `max_budget` in the config to a number that matches what this decision is worth to you, then run the deliberation.

**Checkpoint 2 (graded):**
- Your brief passed validation *only* after all four sections were present (you saw it fail, then pass).
- The memo references facts from your **context file** (proof it loaded into the board).
- One sentence: how did raising the budget change the depth of the debate?

## 3 · Customize the board (15 min)

Pick **one** (all via prompt/config edits, no app code):

- **3a — Bias a seat.** Edit one board member's `DEFAULT_STANCE` / `Reasoning Patterns` to sharpen its bias (e.g. make Contrarian even more adversarial). Re-run your Part-2 brief and show the changed stance in the new memo.
- **3b — Change the roster.** Comment a member out of the `board:` list (or add one back). Re-run and confirm the footer + memo reflect the new roster.
- **3c — Retune constraints.** Set `min_time_minutes` higher and re-run; show the deliberation refuses to end early until min time is met (the `end_deliberation` guard).

**Checkpoint 3 (graded):** the new memo/behavior demonstrably reflects your change, and you can point to the exact file + line you edited.

## 4 · Prove the technical truths from the logs (15 min)

1. Open the newest `deliberations/<your-slug>-<id>/conversation.jsonl`. Confirm every turn has `from` / `to` / `message`, bookended by `meeting_start` / `meeting_end`. *(Frame `t1420`.)*
2. Open `tool-use.jsonl` in the same dir — find at least one board member's tool call (a Read, or an SVG write).
3. **Parallel check:** in `conversation.jsonl`, look at one round. Note that board members' messages in the *same* round don't quote each other — they only reference prior rounds. Cross-check by reading `apps/ceo/extensions/ceo-and-board.ts` and finding `Promise.allSettled` in `converse`.
4. **Ordering check:** in `end_deliberation`, confirm final statements are collected in **config order** (Contrarian is 4th), *not* last — despite what `ceo.md` / `contrarian.md` claim.

**Checkpoint 4 (graded, one sentence each):**
- Why can two board members in the same round not have built on each other's arguments?
- Name the two places the prompts and the code disagree.

## Stretch (optional)

- **S1 — Model diversity.** Launch with the multimodel config (`ceo-and-board-configuration-multimodel.yaml`, agents in `agents-multimodel/`). Run the same brief and compare the debate's texture to the all-Claude run. *(Requires the relevant provider keys / OpenRouter.)*
- **S2 — Expertise persistence.** Run the same brief **twice**. Diff a member's `expertise/<member>-scratch-pad.md` before and after — show it accumulated notes. Explain why this compounds over 20 briefs.
- **S3 — Close the loop with a skill.** Ensure `ELEVENLABS_API_KEY` is set and confirm the CEO speaks the memo (summary.mp3 saved beside the memo). *(Frame `t1052`.)*

## Pass criteria (all required)

- [ ] Checkpoint 0: can state inputs, outputs, and the two forced-end conditions without notes.
- [ ] Ran a shipped brief end-to-end; recorded the vote tally and named the dissenter's added value (Checkpoint 1).
- [ ] Authored a valid 4-section brief **with a context file**; demonstrated validation *failing then passing* (Checkpoint 2).
- [ ] Made one board/config customization that visibly changed a subsequent memo (Checkpoint 3).
- [ ] Located `conversation.jsonl` + `tool-use.jsonl`; correctly explained the parallel-within-round mechanic and named the two spec-vs-code gaps (Checkpoint 4).
- [ ] Oral check, no notes: the three innovations and why 1M context is the enabler; two board tension-pairs; "uncertainty in, decision out"; and how you'd size budget to a decision's worth.

## Instructor / self-check notes

- **Most common stall:** trying to *type into* the meeting. It's one-shot — only `/ceo-begin`, `stop`, `wrap` are honored. If a student is "stuck," they're usually trying to chat.
- **Second stall:** a brief that won't run. 90% of the time it's a missing/renamed required section, or a context file that isn't `.md`. The blocking notice tells them exactly what's missing — teach them to read it.
- **Budget anxiety:** the demo's $1–$5 is deliberately tiny and produces a shallow memo. The *point* of Part 2 is to feel the difference when you size budget to the decision. If a student can't fund a single run, that budget conversation is the lesson surfacing early.
- **Don't over-teach the harness internals.** Part 4 is a *verification* pass (read enough of `ceo-and-board.ts` to confirm two facts), not a code-modification exercise. Keep the primitive crisp: agents that decide, uncertainty in / decision out.
- **What this lab intentionally does NOT cover:** building a new Pi extension from scratch, RPC/SDK embedding, or multi-vendor tuning at depth — those belong to later Pi/agent-experts material.

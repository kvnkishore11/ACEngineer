# MA-1 Nuggets — ranked for the struggling learner

Ordering rule: how much of the lesson (and the codebase) breaks if this nugget is missing. Tier 1 is the mental model; Tier 2 is the working machinery; Tier 3 is framing + the precise technical gotchas that separate a careful reader from a hand-waver.

---

## Tier 1 — If you remember nothing else

**1. Agents can DECIDE, not just code.**
The whole lesson is a promotion: your agents stop being coding worker bees and become a **CEO and board** that answers your hardest strategic questions. Dan's category name: **agentic engineering**, not agentic coding. "Coding is just the beginning... it's the lowest hanging fruit."
*Why weak learners lose it:* they pattern-match to "another coding demo." It isn't — nothing gets coded here.

**2. Uncertainty in, decision out.**
Design any agent system by nailing input and output first. Here: **brief → deliberation → memo.** A structured question in; a ranked, dissent-annotated recommendation out. The debate is the workflow in the middle.
*Test yourself:* name the three nodes and which one is the "answer."

**3. The board's value is DISAGREEMENT.**
Eight specialists with controlled biases and opposing time horizons (Revenue: 90-day cash; Compounder: 24-month trust; Moonshot: 10x bet; Contrarian: attack assumptions). Their tension exposes flaws you can't see alone. A room that agrees added nothing.
*Say it Dan's way:* "multiple perspectives that don't agree so we can flesh out the mental model."

**4. Three innovations make it possible NOW.**
(1) **True 1M context** at flat price with graceful degradation — the enabler; (2) a **customizable agent harness (Pi)**; (3) **compounding agent expertise**. If you can only justify one as the unlock, it's 1M context: "the core four just got a massive buff."

---

## Tier 2 — The working machinery

**5. A brief is validated — bad prompts don't run.**
Every brief must contain **## Situation, ## Stakes, ## Constraints, ## Key Question** (case-insensitive). Miss one → the meeting is blocked with a fix-it notice. This *forces* prompt engineering as a pattern. "If you template your engineering, your agents can do exactly what you did."

**6. Context files ride along to every agent.**
Any `.md` in the brief directory except `brief.md` is a **context file**, preloaded (via Pi's `@file`) into *every* board member's window. So the whole board shares the same business-metrics.md / product-overview.md before debate starts. Drop only `brief.md` and you've starved the board.

**7. Two custom tools run the meeting.**
`converse(to, message)` — broadcast ("all") or target members; returns their responses **plus a constraint-state block**. `end_deliberation(message)` — collect final statements and trigger the memo. That's the entire orchestration surface.

**8. The constraint engine bounds everything.**
After every `converse`, the CEO sees elapsed time + budget. At **80% of max** it starts wrapping; at max it sees **[MAX REACHED]** and *must* end. It also *can't* end before **min_time** (unless max is already hit). Budget counts every board cost **plus the CEO's own tokens**.

**9. CEO vs board are run differently.**
The **CEO is the Pi agent itself** (Opus 4.6; system prompt injected at `before_agent_start`). **Board members are separate `pi` subprocesses** with **persistent sessions** (`--session`), Sonnet 4.6 by default. First subprocess call sets `--system-prompt`/`--model` + preloads context; later calls reuse the session so context carries.

**10. The whole debate is logged (observability).**
Each meeting writes `conversation.jsonl` (from/to/message), `tool-use.jsonl` (every tool call), expertise updates, and argument SVGs. Replayable, auditable, improvable. "If you don't measure it, you cannot improve it. Full stop."

**11. Expertise compounds; memory doesn't.**
Per-agent scratch pads in `expertise/` **persist across deliberations** and grow (production files: tens of thousands of tokens). The revenue agent learns how to argue against the compounder; the CEO tracks which tensions resolved. The 1M window is what makes that practical.

**12. Skills bolt extra capability onto agents.**
The CEO's front matter lists `svg-generate` (decision-framework diagram) and `tts-eleven` (a 1–4 sentence ElevenLabs audio summary). Board members can also make argument SVGs. Skills are *paths + use-when* in the prompt — the agent reads and runs them itself.

---

## Tier 3 — Framing + the precise technical gotchas

**13. GOTCHA — "sequential" is a lie; converse is PARALLEL.**
`ceo.md` says board calls are "sequential — later members see earlier responses." The code runs them with `Promise.allSettled` (**parallel**), matching Dan's narration ("this runs in parallel... this isn't sequential"). Consequence: **within a round, members answer blind to each other**; they only build on each other **across rounds** by re-reading `conversation.jsonl`. Teach this mechanic explicitly.

**14. GOTCHA — "Contrarian speaks last" is NOT enforced (v1).**
The README and prompts promise Contrarian goes last. `end_deliberation` actually collects final statements in **config order** (Contrarian is 4th of 8) with no reordering. It's aspirational. Don't rely on ordering the code doesn't implement.

**15. Model versions are near-future placeholders.**
Opus 4.6 / Sonnet 4.6 / GPT-5.4 / Gemini 3.1 Pro are as spoken in a March-2026 recording. The book's baseline is newer (Opus 4.8 / Sonnet 5). The tactic is model-agnostic — "the models must be able to maintain long context." Treat version strings (and the `/claude-.*-4-6/` "1M" badge regex) as period detail.

**16. The demo is all-Claude; diversity is the ideal.**
Dan: "agent model diversity is super super important for creating better conflict." But he runs the demo all-Claude (Opus CEO + Sonnet board) because other labs lacked true long context. The shipped `agents-multimodel` config already wires GPT-5.4, Gemini 3.1 Pro, Qwen, Kimi, MiniMax, etc. via OpenRouter — the diversity path.

**17. It's one-shot, not a chat.**
`on('input')` blocks all typed text; ~20 built-in slash commands are shadowed. Only `/ceo-begin`, `stop`, `wrap` are honored. "This is not a conversation. This is a one-shot multi-agent system."

**18. Same brief, different vote — that's expected.**
On-screen TTS said "five to one"; the k8wlei memo says "7–1"; a scratch pad logged "6–2." Non-determinism is normal; Moonshot dissents consistently. Read variance as a feature of a real deliberation, not a bug.

**19. How much is a decision worth?**
Dan's framing question justifies the spend: size time + budget to the **value of the decision**, not to habit. The $1–$5 demo is deliberately tiny; production runs far higher. A good strategic call is worth far more than a few dollars and minutes.

**20. This is where vibe coders have no shot.**
Because you go down to the **system-prompt and subprocess primitives** — overriding the coding-agent persona, registering tools, spawning agents — you're building something a prompt-only user can't. "The awareness just isn't there."

---

## Micro-quiz (close the book first)

1. State the system as a function in five words. Name its three nodes.
2. Name four board members and what each optimizes for. Why do you *want* them to disagree?
3. What are the three innovations, and which is the enabler — why?
4. Within one deliberation round, does a board member see the others' answers? Explain the mechanic.
5. What makes a brief valid, and what happens if it isn't?
6. Where do the prompts and the shipping code disagree — name both gaps.
7. How is the CEO run differently from a board member (agent vs subprocess, model, session)?
8. What forces a meeting to end, and when can the CEO *not* end early?

*(Answers: extract.md ideas 1–2, 4, 6, 3/12, 10, 12, 12, 5.)*

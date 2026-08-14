# AH-1 Nuggets — ranked for the struggling learner

Ordering rule: how much of your agentic-coding practice breaks if this nugget is missing. Tier 1 is the framework you cannot skip; Tier 2 is the working machinery (the 12 techniques, distilled); Tier 3 is framing that keeps you honest and moving. The loot box ships 18 notes — these fold them in and rank them.

---

## Tier 1 — If you remember nothing else

**1. A focused agent is a performant agent.**
Focus isn't tidiness — it's the *mechanism* of performance. A clean, task-scoped window makes better, more surgical decisions and one-shots more often than a bloated one. Everything else is in service of this.
*Why weak learners lose it:* it sounds like a slogan. It's a testable claim — measure the window, then judge the output against it.

**2. There are only two moves: Reduce and Delegate (R&D).**
**Reduce** = strip context out of your *primary* agent. **Delegate** = push context onto *other* agents. Every one of the 12 techniques is one or both. If you can sort a technique into R or D, you understand it.
*Say it Dan's way:* "When you boil it down, there are only two ways to manage your context window, R and D. Reduce and delegate."

**3. Measure before you manage: `/context` + a token counter.**
`/context` shows what's already in the window (system prompt, tools, MCP, agents, memory, messages, free). A tokenizer shows a file's cost *before* it enters. On camera a fresh boot was already 31% full. If you never run `/context`, you're vibe coding.

**4. Own your context window — never hand its control away.**
Not to a bloated CLAUDE.md, not to `/compact`, not to any tool. You own your prompt and your model; own your context the same way. This single principle generates half the techniques (prime not default; clear-and-prime not compact; append-system-prompt to steer the read tool).

---

## Tier 2 — The 12 techniques, distilled (the working machinery)

**5. (T2) Delete the default `.mcp.json`.**
Preloaded MCP servers cost 10–12% of your window on every agent you boot (24.1k tokens on camera). Load only what you need: `claude --mcp-config <file>` (+ `--strict-mcp-config` to beat globals). Five agents/hour × 24k ≈ a quarter of a window wasted.

**6. (T3) Prime, don't default.**
CLAUDE.md is incredible AND terrible for the same reason — it's *always loaded*. Shrink it to true universals (43 lines / 0.2%); use `/prime`, `/prime_cc`, `/prime_bug`… to load task-scoped context on demand. The bloated `CLAUDE.large.md` (2,978 lines) trips Claude Code's own "will impact performance" warning.

**7. (T4) Cap output tokens with output styles.**
Output tokens cost 3–5× input and re-enter the window. A one-word "Done." style cut a ~150-token reply to 2 tokens (~99%). Output styles hot-swap the output-style block in the system prompt. Small per call; huge across hundreds of agents.

**8. (T5) Sub-agents are partially forked windows.**
A sub-agent is a *system* prompt, so custom agents cost ~122 tokens in your primary window while the sub-agent burns its own thousands. `/load_ai_docs` fans out `docs-scraper` sub-agents in parallel and keeps the scrape *off* your primary agent. Caveat: you now track every agent's core four.

**9. (T6) Split the architect from the editor.**
One agent plans (`/quick-plan` → a spec), a *fresh* agent builds (`/build` the spec). The planner is *supposed* to over-gather — "go overboard, then delete" — so the builder gets a clean window for surgical, error-free edits. Don't prompt-chain in one chat window; that's how rot creeps in.

**10. (T7) Reset and prime — don't `/compact`.**
After `/compact` you don't know what's in your window (Ctrl-R to find out). `/clear` then `/prime` leaves a *known* state you own. Out-loop, no single agent should overflow 200k and trigger a compaction you can't predict — if it would, chop up the task.

**11. (T8) Context bundles remount an exploded agent.**
A hook writes an append-only JSONL trail of prompts/reads/writes to `agents/context_bundles/<DAY_HOUR>_<session>.jsonl`. A fresh agent runs `/load_bundle` to dedup and replay ~70% of the prior agent's state. Don't log everything — the trimmed replay is the point.

**12. (T9) One agent, one purpose.**
The summary technique. Plan the work with *no regard for technology*, then plan the *pipeline* of single-purpose agents (an ADW). A focused agent is a performant agent — so give each one exactly one job, and debugging localizes to one piece.

**13. (T10) `--append-system-prompt` steers behavior (print mode only).**
Append to the crafted default (don't overwrite it with the SDK's `customSystemPrompt`). The demo forced "read in 100-line increments" + a ✅/❌ final prefix; the context bundle proved it — `Read(100), Read(100)`. Control behavior → control the window.

**14. (T11) Fire independent primary agents (e.g. `/background`).**
Unlike sub-agents, a background agent is a *full* Claude Code instance (own context/model/settings/keys) that writes a report file and renames it `.complete.md`/`.failed.md`. Compute orchestrating compute — out of loop, no babysitting.

**15. (T12) Agent experts: plan → build → improve, self-updating.**
Specialized agents that own a codebase area *and* auto-update their own knowledge: the **improve** step reads the `git diff` and edits *only* the dedicated `## Expertise` sections (never the Workflow). Encode the engineer who knows that subsystem — and let it maintain itself. Wrap it into an ADW.

---

## Tier 3 — Framing that keeps you going

**16. Adopt your agent's perspective.**
Stop reasoning from your convenience; reason about *this agent's* window right now. Awareness of each agent's state inside your pipelines is what separates context engineering from vibe coding.

**17. It's not about saving tokens — it's about spending them properly.**
The goal isn't a low bill; it's not wasting time and tokens *correcting* the agent. Aim for one-shot out-loop streaks with the fewest attempts, so you can drop your presence.

**18. Context engineering is a safe bet.**
Models lose capability as the window grows (an attention problem). That won't change soon, so investing your time in context management pays off regardless of model or window size. Bet on it — and don't forget prompt engineering; bad prompts waste a perfect context.

**19. This is not vibe coding — you have to invest.**
"If it's easy, a vibe coder is probably doing it, and that isn't irreplaceable." Even one technique saves real time; you have twelve. Pick a couple, deploy them, measure the difference.

**20. Better agents, then more agents.**
Make one agent better = master its window (Reduce). Add more agents = delegation to the max, one purpose each (Delegate). The endgame is in-loop → out-of-loop → ZTE.

---

## Micro-quiz (close the book first)

1. R&D — what do the letters stand for, and sort five techniques into the two buckets.
2. Two tools to measure context, and what a fresh `/context` boot showed on camera.
3. Why is CLAUDE.md "incredible and terrible for the same reason"? What replaces it?
4. Why do sub-agents cost only ~122 tokens in your primary window?
5. Why avoid `/compact`, and what's the two-command alternative?
6. What produces a context bundle, and what reloads it?
7. Which flag appends to the system prompt, what mode is required, and what's the dangerous SDK alternative?
8. Name the three steps of an agent expert and what makes it self-improving.

*(Answers: nuggets/extract Idea 0, 3/T1, T3, T5, T7, T8, T10, T12.)*

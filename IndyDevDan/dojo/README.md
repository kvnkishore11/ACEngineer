# The Agentic Dojo — play and learn IndyDevDan's craft

Twelve fill-in-the-blanks lessons that make you build the exact artifacts Dan builds —
agentic prompts, prime commands, meta prompts, validator hooks, ADWs, sub-agents,
custom agents, orchestrators, agent experts, and a verifier. You fill blanks, run the
closed loop, and iterate until it passes. By lesson 12 you've built his whole toolkit
with your own hands.

## Quickstart

```bash
cd dojo
python3 serve.py           # or: just play — opens the visual dojo in your browser
```

The web UI has everything: the lesson brief, an editor for the blank files, and
Check / Hint / Diff / Reset buttons wired to the same closed loops. Prefer the
terminal? `python3 dojo.py status|next|check|hint|diff|reset` does it all too.

Requirements: Python 3.10+. Nothing else — every check is offline and deterministic.
Optional: `just` for shorter commands, `claude` CLI for the "Run It Live" extras.

## How to play

1. `python3 dojo.py next` — read the lesson's README.
2. Open the lesson's starter files. Every blank is `____` with a `YOUR TURN:` comment.
3. Fill the blanks. Run `python3 dojo.py check NN`. Read the failures — they teach.
4. Stuck? `python3 dojo.py hint NN` (progressive), or `python3 dojo.py diff NN` (the answer — last resort).
5. Pass, read the Level-up, move on. `python3 dojo.py reset NN` restores the starter anytime.

Your journey is logged to `progress.jsonl` — Dan's rule: if you don't measure it,
you can't improve it.

## The curriculum

| Lesson | You build | Dan's principle |
|--------|-----------|-----------------|
| 01 the-agentic-prompt | A purpose/workflow/report prompt, run programmatically | The prompt is the fundamental unit |
| 02 prime-your-codebase | A `/prime` command | Context priming over memory bloat |
| 03 leverage-points | stdout + types on a tiny app | Adopt your agent's perspective |
| 04 plan-is-the-prompt | A `/chore` meta prompt | The plan IS the prompt |
| 05 higher-order-prompt | An `/implement` HOP | Prompts compose like functions |
| 06 close-the-loop | A PostToolUse validator hook | Always add feedback loops |
| 07 adw | An AFK Developer Workflow script | Stay out the loop |
| 08 subagents | Sub-agent defs + parallel fan-out | One agent, one prompt, one purpose |
| 09 custom-agent | An SDK agent: system prompt, tools, hook | The system prompt is the product |
| 10 o-agent | An orchestrator: CRUD over a fleet | Scale compute, not your presence |
| 11 agent-expert | expertise.yaml + self-improve loop | Agents forget; experts learn |
| 12 verifier | An atomic-claims verifier | Spend tokens to save time |

## The meta-lesson

Look around this repo: `.claude/commands/prime.md`, `ai_docs/`, a `justfile`,
uv single-file scripts, JSONL logs, and deterministic validators around
non-deterministic work. The dojo itself is structured the way Dan structures
every repo — the agentic layer wrapped around `lessons/` (the src). Studying
the dojo is studying the answer key.

Companion reading: `../artifacts/agentic-dojo/index.html` — the full curriculum book
with every principle, nugget, and the 12-week program these lessons slot into.

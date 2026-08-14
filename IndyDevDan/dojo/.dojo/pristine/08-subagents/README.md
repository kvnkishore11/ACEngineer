# 08 · Subagents — The Description Is the Routing Contract

One agent, one prompt, one purpose — and a subagent's `description` is the contract the primary agent reads when deciding to delegate.

## The Idea

A subagent file is not a prompt you run. It is a **system prompt** you hand to your primary agent's toolbox — Dan calls out the two big mistakes engineers make: "(1) not realizing the agent .md file is the sub-agent's system prompt, not a user prompt; (2) not realizing sub-agents report back to the primary agent, not to you — the flow of information here is absolutely critical." The flow is always: you → primary agent → prompts subagents → subagents respond to the primary → primary reports to you. If your subagent's Report section talks to "the user," you've broken the chain.

The `description` field is where routing happens. The primary agent never reads your subagent's body when deciding to delegate — it reads the description. So the description must encode *when* to fire ("Use PROACTIVELY when…", "MUST BE USED for…" — Anthropic's information dense keywords) and can even teach the primary *how to prompt it*. Then strip the tools: a scout that only needs Read, Glob, Grep should hold nothing else. Every tool you leave off is a mistake it can't make.

Why bother? Two reasons and only two: **specialization and parallelization**. "If you don't need to parallelize and you don't need to specialize, just create a reusable prompt." When you do need both, subagents are the R&D framework's D — each scout burns its own context window, your primary's stays clean, and "a focused agent is a performant agent." And when the job's done, let them go: "you must treat your agents as deletable resources" that serve a single purpose.

## What Dan Did

In YT-03 (the `disler/claude-code-hooks-mastery` repo) Dan walked `.claude/agents/hello-world-agent.md` — frontmatter (`name`, `description`, `tools`) plus a body whose Report section literally scripts the hand-back: "Claude - respond to the user with this message: …". He tightened descriptions with trigger phrases ("If they say TTS, TTS summary, use this agent") until subagents fired from natural phrasing alone, then built the meta-agent — "my agents are building my agents." In AH-1 he showed the payoff at scale: `/load_ai_docs` fanned out ~10 doc-scraper subagents while the primary's window stayed at ~9K tokens.

## Your Mission

Two files, five blanks:

1. `agents/file-scout.md` — the subagent definition:
   - **description** — the routing contract: what it does, when to use it proactively, at least 80 characters.
   - **tools** — the read-only whitelist: `Read, Glob, Grep`. Nothing that writes or executes.
   - **Report section** — state that the final message is a report back to the primary agent, and give the exact report shape.
2. `commands/fanout.md` — the fan-out command:
   - **the parallel instruction** — all three scouts launched in a single message, in parallel.
   - **the per-scout prompt template** — the primary agent is the prompt engineer for its subagents.
   - **the aggregation step** — one markdown summary table, one row per directory.

## The Loop

```
just check 08          # or: python3 ../../dojo.py check 08
```

The check parses your frontmatter with a tiny stdlib parser and reads your words the way a primary agent would (your `<!-- YOUR TURN -->` comments are stripped first — only what YOU wrote counts). Pass looks like:

```
✅ PASS — 08 subagents
```

## Done-when

- `agents/file-scout.md` frontmatter parses; `name` is `file-scout`.
- The description is ≥ 80 characters and carries a proactive trigger phrase.
- Tools include Read, Glob, Grep and exclude Write, Edit, Bash.
- The body says the final message is a report back to the primary agent, with a Report shape.
- `commands/fanout.md` keeps `$ARGUMENTS`, names `file-scout`, demands all three scouts run in parallel in a single message, and aggregates the reports into one summary table.

## Level-up

Build Dan's meta-agent move: a `meta-scout.md` subagent whose system prompt knows how to write *new* scout definitions (`test-scout`, `docs-scout`, `deps-scout`) into `agents/`, each with its own routing contract. Then re-read your descriptions as a set — can the primary agent always pick exactly one scout without ambiguity? That's decision overload, the failure mode Dan warns about as agent count grows.

## Run It Live

Optional, never required to pass. Copy the files into a real project:

```
cp agents/file-scout.md   <your-repo>/.claude/agents/
cp commands/fanout.md     <your-repo>/.claude/commands/
```

Boot `claude` in that repo and run `/fanout src tests docs`. Watch the primary launch three file-scout Tasks in one message, then hand you a single table. Then try the routing contract itself: ask "what's the shape of the src directory?" with no slash command — if your description is right, the scout fires on its own.

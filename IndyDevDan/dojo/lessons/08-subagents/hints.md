# Hints — 08 subagents

## Hint 1

Open the real thing Dan built: `hello-world-agent.md` from `claude-code-hooks-mastery`. Its description doesn't describe the agent's soul — it tells the primary agent exactly when to fire it ("use proactively when greeting the user. If they say 'hi claude'…"). Yours needs the same move for directory surveys. And notice its Report section: it scripts what goes back to the primary agent, word for word.

## Hint 2

The description blank wants three things in one line: what the scout does, a proactive trigger ("Use PROACTIVELY when you need the shape of a directory…"), and optionally how to prompt it ("give it exactly one directory path"). The tools blank is literally `Read, Glob, Grep` — nothing else. In fanout.md, the check wants your own words (comments don't count) to say "in parallel" / "in a single message", to name `file-scout`, and to "aggregate"/"combine" into a "table".

## Hint 3

Near-answer. Report section for the scout:

```
IMPORTANT: You are not talking to the user. Your final message is a report back
to the primary agent that prompted you. Respond to the primary agent with:
- directory / files / languages / entry points / summary (one line each)
```

Fanout workflow step 2: "Launch three file-scout subagents IN PARALLEL — one per directory, all three Task calls in a single message." Step 3: give each scout its one directory and the report shape you expect back. Report: "Aggregate the three scout reports into ONE markdown summary table — | directory | files | languages | entry points | summary | — one row per directory."

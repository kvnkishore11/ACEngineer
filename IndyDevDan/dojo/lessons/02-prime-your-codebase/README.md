# 02 · Prime Your Codebase

Your agent is brilliant, but blind — a `/prime` command gives every fresh session your
perspective on the codebase in one shot: READ, RUN, REPORT.

## The Idea

Tactic #2 is Adopt Your Agent's Perspective. Dan: "Your agent is brilliant, but blind. With
every new session, it starts as a blank instance… no context, no memories, and no awareness
outside of what you give it." Every fresh agent faces the Agent Navigation Problem — it must
re-explore your codebase from zero. You can let it wander and burn tokens, you can bloat a
memory file it drags into every session, or you can prime it: a reusable command that loads
exactly the context this codebase needs, on demand, every time.

A prime command has three moves. **READ**: the handful of files that give the shape of the
codebase — the map before the territory. **RUN**: a safe, read-only command whose stdout
shows the layout, because standard out is a top leverage point — "your agent can only see
what you let it see." **REPORT**: force the agent to prove the context landed by summarizing
what it now knows and what it would do next.

Priming is deliberate context engineering: the minimum context required to work, not the
maximum you can cram — "we want our codebases to be token efficient." A primed agent starts
every session oriented, which is what pushes the Attempts KPI down toward one-shot and keeps
your Streak alive without you hovering (Presence down too).

## What Dan Did

In TAC-2 Dan booted fresh Claude instances against the tac-2 natural-language→SQL app and
ran `/prime` before anything else — discover the file tree, read the README, summarize the
codebase back. Primed agents then watched the server's stdout live, diagnosed an upload bug
(unescaped special characters), and one-shot fixed it. His workout instruction was literal:
"Create `.claude/commands/prime.md`: run `git ls-files`, read README, summarize the
codebase. Boot `claude`, run `/prime`." This dojo repo eats the same dogfood — look at
`.claude/commands/prime.md` at the repo root.

## Your Mission

`sample_app/` is TaskTrail, a tiny task tracker (CLI entry point, storage layer, config,
README). Fill the blanks in `commands/prime.md`:

- **READ** — three real paths in `sample_app/` worth reading first (bare paths, one per bullet).
- **RUN** — one strictly read-only command that shows the project layout
  (e.g. `find sample_app -type f | head -20`). Nothing that writes, moves, or deletes.
- **REPORT** — three numbered items: what the app is, the key modules, one suggested next step.

## The Loop

```bash
just check 02          # or: python3 ../../dojo.py check 02
```

The check verifies every READ path actually exists on disk and rejects any RUN command that
could write — a prime that reads stale paths or mutates state is worse than no prime at all.

## Done-when

- No `____` blanks remain in `commands/prime.md`.
- `## READ`, `## RUN`, and `## REPORT` sections are all present.
- READ lists 3+ bare paths that exist on disk.
- RUN holds one non-empty, strictly read-only command (no rm/mv/cp/touch/mkdir/`>`
  redirects/state-changing git).
- REPORT has 3+ numbered items with real content.

## Level-up

Write a `/prime` for a real repo you own: `git ls-files | head -50` as the RUN, your true
top-3 files as the READ. Then add a fourth REPORT item — "what I would be careful about" —
and watch how it changes the agent's first move.

## Run It Live

Copy `commands/prime.md` into a real project's `.claude/commands/prime.md`, boot `claude`,
and type `/prime`. Or headless from this lesson directory:
`claude -p "$(cat commands/prime.md)"`.

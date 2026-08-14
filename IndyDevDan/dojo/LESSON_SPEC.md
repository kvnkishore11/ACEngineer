# Dojo Lesson Specification

Every lesson is a self-contained directory under `lessons/` that teaches one IndyDevDan pattern
by making the learner **fill in blanks, run the check, and iterate** — a closed loop, exactly
like Dan builds. This file is the contract; `dojo.py` and every lesson must honor it.

## Directory layout

```
lessons/NN-slug/
  README.md        # The Idea / What Dan Did / Your Mission / Files / Done-when / Level-up / Run It Live
  <starter files>  # the exercise: prompts (.md), scripts (.py/.sh), configs (.yaml/.json) with blanks
  hints.md         # progressive hints: "## Hint 1" … "## Hint N" (first = nudge, last = near-answer)
  check.py         # the closed loop: deterministic validator, stdlib-only, offline, < 5 seconds
  solution/        # reference solution — same relative paths as the starter files, fully filled in
```

## The blank convention

- A blank is the literal token `____` (four underscores).
- Every blank has a nearby `YOUR TURN:` comment explaining what belongs there:
  - Python / shell / YAML: `# YOUR TURN: <what and why>`
  - Markdown prompts: `<!-- YOUR TURN: <what and why> -->`
- Blanks range from one word (a keyword, a section name) to a few lines (a workflow step,
  a validation command). Never more than ~5 lines per blank — learners fill, not author from scratch.

## check.py contract

1. Shebang `#!/usr/bin/env -S uv run --script` with a PEP 723 header declaring **no dependencies**;
   must also run under plain `python3 check.py`.
2. Resolves paths relative to `__file__` — works from any cwd.
3. Step zero: scan starter files for `____` and fail with the count and file names.
4. Then real validation: structure checks, regex on required sections, running learner scripts
   with sample inputs (subprocess), asserting outputs. Deterministic. **Never calls an LLM API.**
   Anything agent-shaped runs in mock mode (`DOJO_MOCK=1` is the default assumption).
5. Output: `✅ PASS — NN <slug>` and exit 0, or `❌ FAIL — NN <slug>` plus a numbered list of
   specific, actionable failures and exit 1. Error messages teach; they name the file and the fix.
6. Must FAIL on the untouched starter and PASS when the starter files are replaced by `solution/`.

## README.md sections (in order)

1. `# NN · Title` + one-line thesis (Dan's framing, with his vocabulary).
2. `## The Idea` — the principle, 2-4 paragraphs, quoting Dan where it lands.
3. `## What Dan Did` — the original demo/repo this replicates, concretely.
4. `## Your Mission` — what to fill in, file by file.
5. `## The Loop` — `just check NN` (or `python3 ../../dojo.py check NN`), what pass looks like.
6. `## Done-when` — bullet criteria mirroring what check.py enforces.
7. `## Level-up` — a harder variation to try after passing (no checker).
8. `## Run It Live` *(optional)* — how to run the artifact against real Claude Code / claude -p
   once the offline check passes. Never required for passing.

## The 12 lessons

| NN | slug | teaches | source |
|----|------|---------|--------|
| 01 | the-agentic-prompt | An agentic prompt = purpose / workflow / report; run it programmatically | TAC-1 |
| 02 | prime-your-codebase | The /prime context-priming command (READ / RUN / REPORT) | TAC-2 |
| 03 | leverage-points | Make code legible to agents: stdout + types on a tiny app | TAC-2 |
| 04 | plan-is-the-prompt | The /chore meta prompt: a template that writes plans | TAC-3 |
| 05 | higher-order-prompt | The /implement HOP: a prompt that takes a plan as argument | TAC-3 |
| 06 | close-the-loop | A PostToolUse validator hook: request → validate → resolve | TAC-5 |
| 07 | adw | An AFK Developer Workflow: code chaining agentic prompts | TAC-4 |
| 08 | subagents | Sub-agent definitions + a parallel fan-out command | AH-4 / YT-03 |
| 09 | custom-agent | A custom agent on the SDK: system prompt, tool whitelist, hook | AH-3 |
| 10 | o-agent | The orchestrator: create / command / status / delete over a fleet | AH-4 |
| 11 | agent-expert | Act–Learn–Reuse: expertise.yaml + question + self-improve prompts | AH-5 |
| 12 | verifier | The verifier agent: decompose claims, verify each, report | MA-4 |

Difficulty rises: 01-03 are one-file fills, 04-08 are multi-file, 09-12 are small systems.

## House style (the lessons must feel like Dan's repos)

- uv single-file Python scripts with PEP 723 headers; stdlib preferred.
- Prompts are markdown with clear section headers; the Workflow section is the S-tier pillar.
- Every artifact reports what it did (stdout is a leverage point).
- Vocabulary: Core Four, R&D, one agent one prompt one purpose, closed loops, ADW, ZTE.
- Second person, confident, zero fluff.

---
description: Gain a general understanding of this repo — the IndyDevDan archive
---

# Prime

Execute the `Run`, `Read` and `Report` sections to understand this codebase,
then summarize your understanding.

## Instructions

Two things a file listing will not tell you. Both cause confidently wrong
answers if missed:

- Every lesson's `codebase/` is a **symlink into a different tree** — `tac/` for
  TAC lessons, `agentic-horizon/` for AH, `agentic-horizon-extras/` for MA.
  Follow the symlink. The code does not live inside the lesson folder.
- Route by the question you are actually asking:
  - what he **said** → `transcript/*.md` (prefer `.md`, then `.txt`, then `.vtt`)
  - what he **built** → `codebase/`, or `IndyDevDan/youtube/_repos/`
  - already distilled → `IndyDevDan/dojo/ai_docs/` — check before re-deriving
  - prior output → `IndyDevDan/artifacts/`

Counts in any README may be stale. Trust the `Run` output over prose.

## Run

ls -d IndyDevDan/tac-* IndyDevDan/ah-* IndyDevDan/ma-*
ls -d IndyDevDan/youtube/yt-* | wc -l
ls IndyDevDan/youtube/_repos | wc -l
ls IndyDevDan/dojo/ai_docs

## Read

IndyDevDan/README.md
IndyDevDan/INDEX.json
REPOS.md

## Report

Summarize your understanding of this repo:

- The three lesson tracks, what each covers, and where each track's code lives
- How many lessons, videos, and cloned repos exist right now
- Which paths answer which kind of question

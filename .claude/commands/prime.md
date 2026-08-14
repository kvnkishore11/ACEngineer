---
description: Gain a general understanding of this repo — the IndyDevDan archive
---

# Prime

Execute the `Run`, `Read` and `Report` sections to understand this repository,
then summarize your understanding.

## Instructions

Two things a file listing will not tell you. Both cause confidently wrong
answers if missed:

- Every lesson's `codebase/` is a **symlink into `codebases/`** — `codebases/tac/`
  for TAC, `codebases/ah/` for AH, `codebases/ma/` for MA, `codebases/yt/` for
  video repos. Follow the symlink; the code is not inside the lesson folder.
  Never edit through it: those are vendored upstream snapshots.
- There are **two kinds of transcript**. `transcripts/<key>/*.vtt` are raw
  per-chapter fragments, often 60–90 seconds each. The readable, whole-lesson
  version is `catalog/courses/<key>/transcript/<key>.md`. Read the second one.

Route by the question you are actually asking:

| Question | Path |
|---|---|
| What did he say? | `catalog/courses/<key>/transcript/<key>.md` |
| What did he build? | `catalog/courses/<key>/codebase/` |
| Already distilled? | `knowledge/distilled/` — check before re-deriving |
| Prior deliverables? | `knowledge/artifacts/` |
| Where did a codebase come from? | `REPOS.md` |

Counts in any prose may be stale. Trust the `Run` output over what a README says.

## Run

ls -d catalog/courses/*/ | wc -l
ls -d catalog/youtube/yt-*/ | wc -l
ls codebases/tac codebases/ah codebases/ma
ls codebases/yt | wc -l
ls knowledge/distilled
uv run tools/tests/validate_structure.py

## Read

CLAUDE.md
CONTEXT.md
catalog/README.md
REPOS.md

## Report

Summarize your understanding of this repo:

- The three lesson tracks, what each covers, and where each track's code lives
- How many lessons, videos, and vendored codebases exist right now
- Which paths answer which kind of question
- Whether `validate_structure.py` passed; if it failed, say what it reported
  rather than proceeding as though the tree were intact

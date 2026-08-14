# AgenticEngineer — agent routing table

A study archive of IndyDevDan's agentic-engineering material: the course
lessons, the YouTube videos, every codebase built in them, and the writing
derived from all of it.

## 1. The one naming rule

**A top-level directory is named for the role it plays, never for where its
contents came from.**

Source-of-origin names carry no information here — *every* directory in this
repository is IndyDevDan material, so a directory called `IndyDevDan/` told you
nothing. If you are adding a top level, name it for its job, or put it inside an
existing one. `tools/tests/validate_structure.py` fails if an unexpected
top-level directory appears.

## 2. Routing table

| Question | Path |
|---|---|
| What did he say? | `catalog/courses/<key>/transcript/<key>.md` |
| What did he build? | `catalog/courses/<key>/codebase/` → resolves into `codebases/` |
| Already distilled? | `knowledge/distilled/` — **check here before re-deriving** |
| Prior deliverables? | `knowledge/artifacts/` |
| The long-form reasoning? | `knowledge/research/` |
| Which lesson covers X? | `catalog/README.md`, `catalog/INDEX.json` |
| Which video covers X? | `catalog/youtube/README.md`, `catalog/youtube/INDEX.json` |
| Where did a codebase come from? | `REPOS.md` |
| How do I rebuild? | `tools/README.md`, `make catalog` |
| What do these words mean? | `CONTEXT.md` |
| Why is it laid out this way? | `docs/adr/` |

Top-level map:

| Directory | Role |
|---|---|
| `catalog/` | Read-only front door to the material: lessons and videos |
| `codebases/` | Every codebase, vendored. **Never edit** |
| `knowledge/` | Everything derived from the archive |
| `media/` | Video bytes — gitignored, manifest tracked |
| `transcripts/` | Raw per-chapter VTT dumps |
| `tools/` | All executable code |
| `docs/` | `agents/`, `adr/` |
| `specs/` | Chore and feature plans |
| `projects/` | Side projects that are **not** the archive |

## 3. Two things a file listing will not tell you

1. **`codebase/` is a symlink.** Every `catalog/**/codebase/` points into
   `codebases/`. A file listing shows it as a directory; it is not one, and
   editing "through" it edits a vendored snapshot.
2. **There are two kinds of transcript.** `transcripts/<key>/*.vtt` are raw
   per-chapter dumps — often 60–90 seconds each. The readable, whole-lesson
   version is `catalog/courses/<key>/transcript/<key>.md`. **Read the second
   one.** Answering from a single raw VTT chapter is the most common way to be
   confidently wrong here.

## 4. Never edit `codebases/`

Those trees are vendored upstream snapshots with no `.git` of their own. An edit
there is indistinguishable from upstream content to the next reader. Copy what
you need into `projects/` instead. Several of them ship their own `.claude/`,
`.cursor/` and `.pi/` directories — that is archived lesson content, not this
repository's agent configuration.

## 5. Counts drift — count at read time

Never trust a number written in prose, including in this file. Produce it:

```sh
ls -d catalog/courses/*/ | wc -l          # course lessons
ls -d catalog/youtube/yt-*/ | wc -l       # videos
ls codebases/tac codebases/ah codebases/ma codebases/yt | wc -l
```

## 6. Prove the tree before trusting it

```sh
make validate     # uv run tools/tests/validate_structure.py
```

It checks that the layout is intact, every symlink resolves, both indexes agree
with what is on disk in both directions, and every backticked path in the
top-level docs actually exists.

## 7. Conventions

- **Issue tracker** — issues and PRDs live as markdown under `.scratch/<feature-slug>/`.
  See `docs/agents/issue-tracker.md`.
- **Triage labels** — canonical role names used as-is (`needs-triage`,
  `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`).
  See `docs/agents/triage-labels.md`.
- **Domain docs** — `CONTEXT.md` at the repo root plus `docs/adr/`.
  See `docs/agents/domain.md`.
- **Media** — never commit `.mp4`/`.m4a`/`.mov`/`.webm`/`.aac`. See
  `docs/adr/0002-media-is-ignored-not-tracked.md`.

# AgenticEngineer

A study archive of IndyDevDan's agentic-engineering material: the paid course
lessons, the public YouTube videos, every codebase built in them, and the
writing derived from all of it.

It is organised by one rule — **a top-level directory is named for the role it
plays, never for where its contents came from** — because every directory here
is IndyDevDan material, so source-of-origin names discriminate nothing. The rule
is enforced by a test, not just documented: see
[`docs/adr/0001-role-based-top-level-layout.md`](docs/adr/0001-role-based-top-level-layout.md).

## Quick Start

Requires [`uv`](https://docs.astral.sh/uv/), `make`, `git`, and Python 3.10+.
Nothing else — every script declares its own dependencies inline (PEP 723), so
there is no install step and no virtualenv to create.

```sh
git clone <this repo> && cd AgenticEngineer
make validate            # prove the tree is intact
```

If `make validate` fails it names the offending path and the check that caught
it; [`tools/tests/README.md`](tools/tests/README.md) explains what each check
means and how to fix it.

Then, depending on why you are here:

- **Reading the material** → [`catalog/README.md`](catalog/README.md).
- **Looking for the summary** → [`knowledge/distilled/`](knowledge/distilled/)
  is the compressed answer. Check it before deriving anything.
- **An agent** → [`CLAUDE.md`](CLAUDE.md) is the routing table;
  [`CONTEXT.md`](CONTEXT.md) defines the vocabulary. Or just run `/prime`.
- **Running something** → [`tools/README.md`](tools/README.md).

A fresh clone has an **empty `media/`**. That is expected — 22 GB of video is
deliberately not in git. See
[`docs/adr/0002-media-is-ignored-not-tracked.md`](docs/adr/0002-media-is-ignored-not-tracked.md).

## Layout

```
AgenticEngineer/
├── README.md                  # you are here
├── CLAUDE.md                  # agent front door — the routing table
├── AGENTS.md                  # symlink → CLAUDE.md, for non-Claude agents
├── CONTEXT.md                 # domain model / vocabulary
├── REPOS.md                   # upstream provenance for every vendored codebase
├── Makefile                   # validate / catalog / youtube / manifest / check-media
│
├── catalog/                   # READ-ONLY front door to the material
│   ├── README.md  CLAUDE.md  INDEX.json      # README + INDEX are GENERATED
│   ├── courses/<track>-<n>-<slug>/           # video/ transcript/ metadata/ codebase/ README.md
│   ├── youtube/yt-NN-<slug>/                 # same shape + INDEX.json, README.md
│   ├── assets -> _source/assets              # shared offline CSS/fonts/images
│   └── _source/                              # raw page dumps, offline pages, ma-download record
│
├── codebases/                 # every codebase, vendored — never edit
│   ├── README.md  CLAUDE.md
│   └── tac/  ah/  ma/  yt/                   # by where the codebase was used
│
├── media/                     # video bytes are gitignored; the record is tracked
│   ├── README.md  MANIFEST.md                # path + size + SHA-256 of every file
│   ├── RECORDING_REPORT.md  SYNC_VALIDATION.{md,json}  PROCESSING-LOG.md
│   ├── final/<key>.mp4                       # hardlinked into catalog/courses/*/video/
│   └── raw/<short-key>/                      # captures, frames, *-sync.json, _archive/, _logs/
│
├── transcripts/               # RAW per-chapter .vtt dumps — see its README first
│   ├── README.md
│   └── <lesson-key>/                         # one directory per lesson
│
├── knowledge/                 # everything derived from the archive
│   ├── README.md  CLAUDE.md
│   ├── distilled/                            # the compressed answer — start here
│   ├── research/                             # the long-form analysis behind it
│   ├── artifacts/                            # rendered HTML deliverables
│   ├── book/                                 # the long-form build
│   ├── dojo/                                 # a runnable practice app
│   └── drafts/                               # unfinished / superseded
│
├── tools/                     # ALL executable code, one home
│   ├── README.md  CLAUDE.md
│   ├── catalog/  youtube/  recorder/  transcripts/  media/
│   └── tests/validate_structure.py           # the structure test — `make validate`
│
├── docs/
│   ├── agents/                               # issue tracker, triage labels, domain
│   └── adr/                                  # architecture decision records
│
├── specs/                     # chore + feature plans
├── projects/                  # side projects that are NOT the archive
│   └── local-visual-plan/
└── .scratch/                  # issue tracker (docs/agents/issue-tracker.md)
```

Each tree carries its own `README.md` (what it holds) and, where an agent needs
rules rather than description, a one-screen `CLAUDE.md` loaded on demand.

## Routing

| Question | Path |
|---|---|
| What did he say? | `catalog/courses/<key>/transcript/<key>.md` |
| What did he build? | `catalog/courses/<key>/codebase/` |
| Already distilled? | `knowledge/distilled/` |
| The reasoning behind it? | `knowledge/research/` |
| Prior deliverables? | `knowledge/artifacts/` |
| Which lesson covers X? | `catalog/README.md`, `catalog/INDEX.json` |
| Which video covers X? | `catalog/youtube/README.md`, `catalog/youtube/INDEX.json` |
| Where did a codebase come from? | `REPOS.md` |
| What do these words mean? | `CONTEXT.md` |
| Why is it laid out this way? | `docs/adr/` |
| How do I rebuild? | `tools/README.md` |

Every `catalog/**/codebase/` is a symlink into `codebases/`. The destination is
guessable from the source, which is the whole point of the layout.

## The one trap worth knowing

There are two kinds of transcript, and both get called "the transcript":

- `transcripts/<key>/*.vtt` — raw, one chapter each, often 60–90 seconds.
- `catalog/courses/<key>/transcript/<key>.md` — stitched, whole lesson. **This one.**

Reading a single raw chapter and answering from it is the most common avoidable
mistake in this repository. See [`transcripts/README.md`](transcripts/README.md).

## Counts

There are no counts written in this file, on purpose. The previous README warned
that its counts drifted and then printed stale ones anyway. Produce them:

```sh
ls -d catalog/courses/*/ | wc -l                      # course lessons
ls -d catalog/youtube/yt-*/ | wc -l                   # videos
ls codebases/tac codebases/ah codebases/ma codebases/yt | wc -l
find catalog -type l | wc -l                          # catalog symlinks
find knowledge/distilled -type f | wc -l              # distillations
```

## Rebuilding

```sh
make validate      # prove the layout, symlinks, indexes and doc paths
make catalog       # rebuild the lesson catalog, its symlinks and INDEX.json
make youtube       # weekly YouTube update, then rebuild the index
make manifest      # regenerate media/MANIFEST.md
make check-media   # audit a populated media/ against the manifest
```

Some files here are **generated** — edit the generator, not the output, or the
next build overwrites your edits:

| Generated file | Written by |
|---|---|
| `catalog/README.md`, `catalog/INDEX.json` | `tools/catalog/build_catalog.py` |
| `catalog/youtube/INDEX.json` and the table in `catalog/youtube/README.md` | `tools/youtube/rebuild_index.py` |
| `media/MANIFEST.md` | `tools/media/make_manifest.py` |

Every script is a PEP 723 single-file script — `uv run tools/<area>/<script>.py`,
no project setup. See [`tools/README.md`](tools/README.md) for what each one does
and whether it is safe to re-run (the builders are idempotent; the recorder is
not).

## Recurring workflows

Three slash commands cover the work that repeats:

| Command | What it does |
|---|---|
| `/prime` | Orient in the repo, then prove the tree with `validate_structure.py` |
| `/weekly` | Fetch new videos, re-link codebases, rebuild the index, validate, commit |
| `/new-lesson` | Ingest a new course lesson end to end |

## Conventions

- **Issues and PRDs** live as markdown under `.scratch/<feature-slug>/` —
  [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md).
- **Triage labels** — [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md).
- **Domain docs** — `CONTEXT.md` + `docs/adr/`, per
  [`docs/agents/domain.md`](docs/agents/domain.md).
- **Never commit** `.mp4`, `.m4a`, `.mov`, `.webm` or `.aac`.
- **Never edit `codebases/`** — vendored upstream snapshots with no `.git` of
  their own. Copy into `projects/` first, and see
  [`codebases/README.md`](codebases/README.md).
- **Counts drift** — count at read time, never trust a number in prose.

# AgenticEngineer

A study archive of IndyDevDan's agentic-engineering material: the paid course
lessons, the public YouTube videos, every codebase built in them, and the
writing derived from all of it.

It is organised by one rule — **a top-level directory is named for the role it
plays, never for where its contents came from** — because every directory here
is IndyDevDan material, so source-of-origin names discriminate nothing.

## First 60 seconds

```sh
git clone <this repo> && cd AgenticEngineer
make validate            # prove the tree is intact
```

Then, depending on who you are:

- **Reading the material** → start at [`catalog/README.md`](catalog/README.md).
- **Looking for the summary** → [`knowledge/distilled/`](knowledge/distilled/)
  is the compressed answer. Check it before deriving anything.
- **An agent** → [`CLAUDE.md`](CLAUDE.md) is the routing table.
  [`CONTEXT.md`](CONTEXT.md) defines the vocabulary.

A fresh clone has an **empty `media/`**. That is expected — 22 GB of video is
deliberately not in git. See
[`docs/adr/0002`](docs/adr/0002-media-is-ignored-not-tracked.md).

## Layout

```
AgenticEngineer/
├── README.md                  # you are here
├── CLAUDE.md / AGENTS.md      # agent front door — the routing table
├── CONTEXT.md                 # domain model / vocabulary
├── REPOS.md                   # upstream provenance for every vendored codebase
├── Makefile                   # validate / catalog / youtube / manifest
├── catalog/                   # READ-ONLY front door to the material
│   ├── courses/<track>-<n>-<slug>/   # video/ transcript/ metadata/ codebase/ README.md
│   ├── youtube/yt-NN-<slug>/         # same shape
│   └── _source/                      # raw page dumps, shared assets, download records
├── codebases/                 # every codebase, vendored — never edit
│   ├── tac/  ah/  ma/  yt/
├── media/                     # video bytes (gitignored) + tracked MANIFEST.md
│   ├── final/<key>.mp4  raw/<short-key>/
├── transcripts/               # raw per-chapter .vtt dumps
├── knowledge/                 # everything derived from the archive
│   ├── distilled/ research/ artifacts/ book/ dojo/ drafts/
├── tools/                     # ALL executable code
│   ├── catalog/ youtube/ recorder/ transcripts/ media/ tests/
├── docs/                      # agents/ adr/
├── specs/                     # chore + feature plans
├── projects/                  # side projects that are NOT the archive
└── .scratch/                  # issue tracker (docs/agents/issue-tracker.md)
```

## Routing

| Question | Path |
|---|---|
| What did he say? | `catalog/courses/<key>/transcript/<key>.md` |
| What did he build? | `catalog/courses/<key>/codebase/` |
| Already distilled? | `knowledge/distilled/` |
| Prior deliverables? | `knowledge/artifacts/` |
| Which lesson covers X? | `catalog/README.md`, `catalog/INDEX.json` |
| Which video covers X? | `catalog/youtube/README.md` |
| Where did a codebase come from? | `REPOS.md` |
| How do I rebuild? | `tools/README.md` |

Every `catalog/**/codebase/` is a symlink into `codebases/`. The destination is
now guessable from the source, which is the whole point of the layout.

## The one trap worth knowing

There are two kinds of transcript, and they are both called "the transcript":

- `transcripts/<key>/*.vtt` — raw, one chapter each, often 60–90 seconds.
- `catalog/courses/<key>/transcript/<key>.md` — stitched, whole lesson. **This one.**

Reading a single raw chapter and answering from it is the most common avoidable
mistake in this repository.

## Counts

There are no counts written in this file, on purpose. The previous README warned
that its counts drifted and then printed stale ones anyway. Produce them:

```sh
ls -d catalog/courses/*/ | wc -l                      # course lessons
ls -d catalog/youtube/yt-*/ | wc -l                   # videos
ls codebases/tac codebases/ah codebases/ma codebases/yt | wc -l
find catalog -type l | wc -l                          # catalog symlinks
```

## Rebuilding

```sh
make validate      # prove the layout, symlinks, indexes and doc paths
make catalog       # rebuild the lesson catalog, its symlinks and INDEX.json
make youtube       # weekly YouTube update, then rebuild the index
make manifest      # regenerate media/MANIFEST.md
make check-media   # verify media/ against the manifest
```

Every script is a PEP 723 single-file script — `uv run tools/<area>/<script>.py`,
no project setup. See [`tools/README.md`](tools/README.md) for what each one does
and whether it is safe to re-run.

## Conventions

- **Issues and PRDs** live as markdown under `.scratch/<feature-slug>/` —
  [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md).
- **Triage labels** — [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md).
- **Domain docs** — `CONTEXT.md` + `docs/adr/`, per
  [`docs/agents/domain.md`](docs/agents/domain.md).
- **Never commit** `.mp4`, `.m4a`, `.mov`, `.webm` or `.aac`.
- **Never edit `codebases/`** — vendored upstream snapshots with no `.git` of
  their own. Copy into `projects/` first.

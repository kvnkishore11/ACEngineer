# AgenticEngineer

A study archive of IndyDevDan's agentic-engineering material — three paid course
tracks, the public YouTube back catalog, and every codebase built in them — kept
offline so agents and humans can read the source instead of recalling it.


## The three lesson tracks

All 18 lessons live as sibling folders in `IndyDevDan/`, named
`<track>-<n>-<slug>`. The prefix tells you which track, and — importantly —
where that track's code lives:

| Prefix | Track | Lessons | Code lives in |
|---|---|---:|---|
| `tac-1` … `tac-8` | **Tactical Agentic Coding** — the foundation | 8 | `tac/` |
| `ah-1` … `ah-6` | **Agentic Horizon** — advanced modules | 6 | `agentic-horizon/` |
| `ma-1` … `ma-4` | **Multi-Agent** — newest; video and code only, no course HTML | 4 | `agentic-horizon-extras/` |

## ⚠ Every `codebase/` is a symlink

Each lesson folder contains a `codebase/` entry that is a **symlink into a
different top-level tree** — never a real directory:

```
IndyDevDan/tac-1-hello-agentic-coding/codebase/  ->  ../../tac/tac-1
IndyDevDan/ah-5-agent-experts/codebase/          ->  ../../agentic-horizon/agent-experts
IndyDevDan/ma-1-ceo-agents/codebase/             ->  ../../agentic-horizon-extras/ceo-agents
```

Reading through the symlink works fine. Writing *paths* based on it does not —
the code does not live inside the lesson folder. Resolve the link before quoting
a path.

## The YouTube tree is live — it grows every week

He publishes roughly one video a week, so `IndyDevDan/youtube/` is never
finished. An idempotent updater discovers new uploads, builds the folder
(transcript + metadata), attaches the codebase, and rebuilds the index:

```bash
python3 IndyDevDan/youtube/weekly_update.py
```

It never re-creates folders for video IDs it already knows, so re-running it is
safe. State lives in `IndyDevDan/youtube/_weekly_last_run.json`, with one
`_weekly_run_<timestamp>.json` per run.

Consequence for anyone reading this file: **the course tracks are stable at 18
lessons, but any video count is a snapshot.** Count them at read time rather
than trusting a number written down — here, in `IndyDevDan/README.md`, or in an
older artifact.

## Where to look for what

| Your question | Read this |
|---|---|
| What did he **say**? | `transcript/*.md` in the lesson or video folder — prefer `.md`, then `.txt`, then `.vtt` |
| What did he **build**? | the lesson's `codebase/`, or `IndyDevDan/youtube/_repos/` for video projects |
| Has it already been **distilled**? | `IndyDevDan/dojo/ai_docs/` — check here before re-deriving anything |
| What has this repo already **produced**? | `IndyDevDan/artifacts/` |
| Which lesson covers X? | `IndyDevDan/README.md` (catalog table) or `IndyDevDan/INDEX.json` |
| Where did a codebase come from? | `REPOS.md` — upstream URLs for every sub-project |

## Layout

```
AgenticEngineer/
├── IndyDevDan/                 # the catalog — the front door for lessons
│   ├── INDEX.json              # machine index of all 18 lessons
│   ├── README.md               # catalog table + per-lesson folder shape
│   ├── <track>-<n>-<slug>/     # video/ transcript/ metadata/ codebase/ README.md
│   ├── youtube/                # public videos, same folder shape
│   │   ├── INDEX.json
│   │   ├── yt-NN-<slug>/
│   │   └── _repos/             # cloned repos the videos build
│   ├── dojo/                   # runnable lesson app + ai_docs/ distilled notes
│   ├── book/                   # long-form build from the lessons
│   ├── artifacts/              # generated HTML artifacts
│   ├── research/               # research write-ups
│   └── raw/                    # scratch notes and drafts
├── tac/tac-1 … tac-8           # TAC codebases
├── agentic-horizon/            # AH codebases
├── agentic-horizon-extras/     # MA codebases
├── videos/                     # raw screen captures, by lesson key
├── tac transcripts/            # original transcript dumps, by course name
├── member-assets/              # symlinks into the codebases + download logs
├── output/                     # cross-cutting analysis write-ups
├── scripts/                    # catalog builders and transcript processors
├── tools/course-recorder/      # capture tooling
└── docs/                       # agents/ and guides/
```

Counts drift as material is added. Trust `ls` over any number written here.

## Conventions

- **Reusable prompts** live in `.claude/commands/`. `/prime` is the context
  primer; run it first in a fresh session.
- **Agent conventions** — issue tracker, triage labels, domain docs — are
  described in `CLAUDE.md` and `docs/agents/`.
- **Sources are never moved.** The `IndyDevDan/` tree hardlinks videos and
  symlinks codebases so the originals stay where they were cloned.

## Rebuilding the catalog

```bash
python3 scripts/materialize_course_pages_offline.py   # offline HTML + assets
python3 scripts/build_indydevdan_catalog.py           # wire into lesson folders
```

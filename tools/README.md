# `tools/` — every executable in the repository

One home for all runnable code. Nothing executable lives inside the data trees
any more: an agent reading `catalog/youtube/` for lesson content used to trip
over build scripts and `__pycache__/`.

Every script is a [PEP 723](https://peps.python.org/pep-0723/) single-file
script, so `uv` resolves its dependencies with no project setup:

```sh
uv run tools/<area>/<script>.py --help
```

All of them are stdlib-only except `youtube/build_video_folder.py`, which
declares `youtube-transcript-api`.

## The scripts

### `catalog/` — builds the lesson catalog

| Script | What it does | Re-runnable? |
|---|---|---|
| `build_catalog.py` | Builds `catalog/courses/<key>/`, hardlinks the video from `media/final/`, creates the `codebase/` symlinks into `codebases/`, writes `catalog/INDEX.json`. **This is what owns the symlinks** — change its path constants and re-run rather than fixing links by hand. | Yes, idempotent |
| `materialize_course_pages.py` | Renders the offline course-page dumps into `catalog/_source/course-pages-offline/`. | Yes, idempotent |
| `postprocess_ma.py` | Normalises a member-asset download into lesson-folder shape. | Yes, idempotent |

### `youtube/` — builds the video catalog

| Script | What it does | Re-runnable? |
|---|---|---|
| `weekly_update.py` | The weekly updater: finds new videos, builds their folders, rebuilds the index. Reads `_weekly_last_run.json` for idempotency — that file is tracked on purpose. | Yes, idempotent |
| `build_video_folder.py` | Builds one `catalog/youtube/yt-NN-<slug>/` with transcript and metadata. | Yes, idempotent |
| `attach_codebases.py` | Creates the YouTube `codebase/` symlinks into `codebases/yt/`. | Yes, idempotent |
| `fill_missing_codebases.py` | Attempts to resolve videos that have no attached codebase. | Yes |
| `rebuild_index.py` | Rewrites `catalog/youtube/INDEX.json` from what is on disk. | Yes, idempotent |

### `transcripts/`

| Script | What it does | Re-runnable? |
|---|---|---|
| `stitch_vtt.py` | Stitches `transcripts/<key>/*.vtt` into one readable transcript. Merges the two former stitchers: the full cleaner plus opt-in `--marker` tagging for a folder holding two lessons' chapters. | Yes |

### `media/`

| Script | What it does | Re-runnable? |
|---|---|---|
| `make_manifest.py` | Regenerates `media/MANIFEST.md` (path, size, SHA-256). `--check` verifies a checkout and exits non-zero on drift. | Yes, idempotent |
| `process_media.sh` | Extracts frames and recombines frames + audio into an MP4. | Yes |

### `recorder/` — captures the lessons

**Not idempotent.** These drive a real browser and write real recordings; re-running
re-records. Read `recorder/README.md` before using them.

### `tests/`

| Script | What it does |
|---|---|
| `validate_structure.py` | The structure test. Asserts the layout invariants and exits non-zero with a specific message on the first failure. See `tests/README.md`. |

## Entry points

The three verbs are wrapped in the `Makefile` so they are discoverable without
reading this file:

```sh
make validate    # prove the tree is intact
make catalog     # rebuild the lesson catalog and its symlinks
make youtube     # run the weekly YouTube update
make manifest    # regenerate media/MANIFEST.md
```

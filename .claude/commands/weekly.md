---
description: Run the weekly YouTube update — fetch new videos, rebuild, validate, commit
---

# Weekly update

Pull new uploads into the video catalog, re-link their codebases, rebuild the
index, prove the tree, and commit.

## Run

uv run tools/youtube/weekly_update.py
uv run tools/youtube/attach_codebases.py
uv run tools/youtube/fill_missing_codebases.py
uv run tools/youtube/rebuild_index.py
uv run tools/tests/validate_structure.py

## Order matters

`attach_codebases.py` removes the `codebase/` symlink from any video whose
description names no repo. That set includes the videos whose codebase is a
*course* codebase rather than a public one — `fill_missing_codebases.py` is what
re-attaches those. Run attach first, fill second. Reversing them silently drops
those links, and the only symptom is a lower symlink count.

## Check before committing

- `git status --porcelain` should show new `catalog/youtube/yt-*/` folders,
  updated `INDEX.json`, and an updated table in `catalog/youtube/README.md`.
- No `.mp4` may appear. If one does, the ignore policy has regressed — fix that
  before committing anything.
- `_weekly_last_run.json` should be updated. It is tracked on purpose: it is the
  idempotency state the updater reads next week.
- Videos reported as `still_none` have no public repo in their description. That
  is expected for opinion and analysis videos, not a failure.

## Commit

git add -A
git commit -m "chore(youtube): weekly catalog update"

Report how many videos were added, how many codebases were attached, and the
result of `validate_structure.py`.

---
description: Ingest a new course lesson into the catalog
---

# New lesson

Add one lesson to `catalog/courses/`. Work in this order — each step depends on
the previous one having produced real files.

## 1. Pick the lesson key

`<track>-<n>-<slug>` — `tac`, `ah` or `ma`, the next number in that track, and a
kebab-case slug from the lesson title. This key names the lesson everywhere:
the catalog folder, the video file, the raw transcript folder. Check it is free:

ls -d catalog/courses/*/ | grep '<track>-'

## 2. Register it in the builder

Add a `dict(...)` entry to `LESSONS` in `tools/catalog/build_catalog.py` with
`order`, `short_key`, `key`, `title`, `slug`, `course`, `video`, `tx`,
`codebase` and `url`. `codebase` is a repo-relative path under `codebases/`.

The builder is the source of truth for the catalog. Do not create the lesson
folder by hand — it will be inconsistent with the other 18 and the next
`make catalog` will not know about it.

## 3. Place the inputs

| Input | Where it goes |
|---|---|
| Finished recording | `media/final/<key>.mp4` |
| Raw capture | `media/raw/<short-key>/` |
| Raw per-chapter VTT | `transcripts/<key>/` |
| Course page dump | `catalog/_source/course-pages/<key>.html` |
| Codebase | `codebases/<tree>/<name>/` — vendored, with its `.git` removed |

If the codebase came from a clone, record its upstream URL and pinned commit in
`REPOS.md` **before** deleting `.git`, or that provenance is gone for good.

## 4. Stitch the transcript

uv run tools/transcripts/stitch_vtt.py transcripts/<key> \
  catalog/courses/<key>/transcript/<key>.md

## 5. Build, then prove

make catalog
make manifest
make validate

## 6. Check the things that fail quietly

- `stat -f '%l' media/final/<key>.mp4` must report `2` — the catalog copy is a
  hardlink, not a second 500 MB file.
- `catalog/courses/<key>/codebase` must resolve, and resolve *into* `codebases/`.
- `git status --porcelain` must show no `.mp4`.

## 7. Commit

git add -A
git commit -m "feat(catalog): add <key>"

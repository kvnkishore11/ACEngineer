# `tools/tests/` — the structure test

```sh
make validate                                   # or:
uv run tools/tests/validate_structure.py        # -v to list every check
```

Exits `0` on success, `1` on the first run that finds anything, printing every
problem with the offending path. Stdlib only, no network.

## Why this exists

The layout in this repository is held together by things that **fail silently**:
a symlink that stops resolving, an index that drifts from disk, a hardlink that
becomes a copy, an absolute path baked into generated JSON. None of them raise
an error at the time. They are discovered later, by someone reading the wrong
file and believing it.

This test converts each of those into a loud failure.

## The checks

| # | Asserts | Catches |
|---|---|---|
| 1 | Every expected top-level directory exists, **and no unexpected one does** | A new `output/`-shaped tree appearing next quarter. This is the check that enforces the naming rule from `docs/adr/0001`. |
| 2 | No tracked path contains a space | The `tac transcripts/` and `final videos/` class of problem returning; paths that must be quoted in every script and glob. |
| 3 | Every `catalog/courses/<key>/` has `video/ transcript/ metadata/ codebase/ README.md`, every `catalog/youtube/yt-*/` has `transcript/ metadata/` | A half-built lesson folder. |
| 4 | Every symlink in the repo resolves | The single most likely breakage — a codebase moved or renamed without re-running the builders. |
| 5 | Every `codebase/` symlink resolves to a path **inside `codebases/`** | A link that resolves but points somewhere wrong, which check 4 cannot see. |
| 6 | Both indexes parse, contain no absolute paths, and their keys match disk **in both directions** | An orphan index entry, an unindexed directory, and the absolute-path bug that broke the YouTube index for everyone except the machine that generated it. |
| 7 | Every backticked path in `README.md`, `CLAUDE.md`, `CONTEXT.md`, `REPOS.md` and `catalog/README.md` exists | Documentation drift. Paths resolve from the repo root *or* the doc's own directory, since both readings are legitimate; bare `host.com/...` tokens are skipped as URLs, not paths. |
| 8 | No `.mp4/.m4a/.mov/.webm/.aac` is tracked | The 22 GB getting into history, permanently. |
| 9 | No `__pycache__`, `node_modules`, `.venv`, `.DS_Store` or `.idea` is tracked | Generated files creeping back into the index. |
| 10 | Every script under `tools/` parses and carries a PEP 723 header | A script that cannot be run with `uv run`, or one broken by an edit. |

## What it deliberately does not check

- **Content.** It proves the shape of the tree, not that a transcript says what
  it should.
- **Hardlink counts.** `media/` is gitignored and is empty in a fresh clone, so
  a link-count assertion would fail for a correct checkout. Check links directly
  with `stat -f '%l' media/final/<key>.mp4` (expect `2`).
- **Media contents.** `make check-media` audits a *populated* `media/` against
  the manifest and names every missing, unlisted or changed file. On a fresh
  clone it exits 1 and says the tree is empty, which is the truth — the bytes
  have not been fetched.
- **Hardcoded home directories in scripts.** Worth adding if it recurs.

## Adding a check

1. Write a function decorated with `@check("N. short name")`.
2. Call `fail(name, msg)` for each problem — do not raise, and do not stop at
   the first one. The point is to report everything in one run.
3. Name the offending path in the message. "`catalog/courses/x/` is missing
   `codebase`" is actionable; "structure invalid" is not.
4. Append it to `CHECKS`.
5. **Prove it can fail.** Break the thing deliberately, confirm the specific
   message appears, then restore. A check that cannot fail is worse than no
   check, because it reports success.

Every check above was verified this way: an unexpected top-level directory, a
broken symlink, a `codebase/` link pointed at `knowledge/`, an unindexed lesson
directory, a nonexistent path in `README.md`, and a script without a PEP 723
header were each injected and each produced its own specific failure.

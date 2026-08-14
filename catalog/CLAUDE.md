# `catalog/` — local rules

Read-only front door to the material. See the root `CLAUDE.md` for routing.

1. **Read the stitched transcript**, `courses/<key>/transcript/<key>.md` — not
   `transcripts/<key>/*.vtt` (raw per-chapter fragments) and not
   `<key>-notes.md` (a companion, not the transcript).
2. **`codebase/` is a symlink** into `codebases/`. Following it leaves the
   catalog and lands in a vendored snapshot you must not edit.
3. **Nothing here is an original byte.** The video is a hardlink into
   `media/final/`. Deleting a lesson's `video/` file breaks the link, not a copy.
4. **`README.md` and `INDEX.json` are generated** by
   `tools/catalog/build_catalog.py`. Edit the generator, then `make catalog`.
   Hand edits are overwritten on the next run.
5. **Indexes hold repo-relative paths only.** An absolute path here breaks the
   catalog for everyone whose checkout is elsewhere; the structure test fails on
   it.
6. `_source/` is raw provenance — page dumps, shared assets, the member-asset
   download record. Not lesson content.

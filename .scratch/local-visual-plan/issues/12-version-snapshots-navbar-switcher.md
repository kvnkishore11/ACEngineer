# 12 — Per-round version snapshots + navbar switcher + fork-restore

Status: done

## Parent

`.scratch/local-visual-plan/PRD.md` (v2.1 amendments)

## What to build

Version the plan across review rounds. After the agent processes a round (slice 11),
if that round produced **≥1 real change to the artifact**, snapshot a new version
`Vn`; if the round changed nothing (e.g. a reply-only / clarification round, slice
13), **do not bump** the version.

Storage: a **full snapshot per version** — the version's `.md` plus its rendered
`.html` — under a per-plan versions directory. Space optimization (base + deltas) is
explicitly **deferred**; full copies are fine for now. The current on-disk
`plans/<slug>.md` / `.html` remain the clean working artifact; version snapshots live
separately.

Surface a **navbar version switcher** in the shell: lists `V1 · V2 · V3 …` with the
**latest focused**. Clicking a version **views it read-only** in the iframe (a badge
marks read-only; you cannot annotate a past version). **Restore** makes a chosen
version the live tip by **forking** — it writes a new version that is a copy of the
chosen one, so forward history is never destroyed (non-destructive).

The version boundary is the send-action / round from slice 11: a batch of 3 comments
the agent applies = one new version capturing all 3 edits.

## Acceptance criteria

- [x] A round that changes the artifact cuts exactly one new version; a no-op round
      cuts none
- [x] Each version stores its full `.md` + rendered `.html` snapshot
- [x] The navbar lists versions V1..Vn with the latest focused
- [x] Clicking a version views it read-only in the iframe (no annotating a past
      version)
- [x] Restore forks a new version that copies the chosen one; all existing versions
      are preserved (non-destructive)
- [x] The current on-disk `.md` / `.html` stay the clean artifact; snapshots live
      separately and `file://` still works
- [x] Tests: no-op round → no bump; edit round → bump; restore forks (does not
      overwrite); switcher lists and focuses correctly

## Blocked by

- `11-batch-send-draft-sidebar.md` (the round / send-action defines the version
  boundary)

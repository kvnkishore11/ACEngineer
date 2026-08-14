# 0001 — A role-based top level

- **Status**: accepted
- **Date**: 2026-08-13

## Context

The repository grew by accretion. Its top level mixed two incompatible naming
axes: some directories were named for **where the material came from**
(`IndyDevDan/`, `tac/`, `agentic-horizon/`, `agentic-horizon-extras/`,
`member-assets/`, `tac transcripts/`), others for **what role they played**
(`output/`, `scripts/`, `tools/`, `docs/`, `videos/`).

There was no rule anyone could apply, so routing was memorised rather than
derived. Concretely:

- The same concept — "a codebase from a lesson" — lived under three unrelated
  names (`tac/`, `agentic-horizon/`, `agentic-horizon-extras/`), which is why
  `README.md` needed a dedicated warning section just to explain where the
  `codebase/` symlinks pointed.
- The same content existed in three or four places: a finished video was in
  `final videos/`, `IndyDevDan/<key>/video/`, and `videos/<key>/`; a transcript
  in `tac transcripts/`, `IndyDevDan/<key>/transcript/`, and
  `member-assets/transcripts/`.
- Source-of-origin naming carried no information at all, because *every*
  directory in the repository is IndyDevDan material. `IndyDevDan/` as a
  top-level name discriminated nothing.
- Executable code was scattered across six homes, some of it inside the data
  trees, so reading `IndyDevDan/youtube/` for lesson content meant tripping over
  build scripts and `__pycache__/`.

## Decision

**A top-level directory is named for the role it plays, never for where its
contents came from.**

```
catalog/      the material, read-only
codebases/    every codebase, vendored
knowledge/    everything derived from the material
media/        the video bytes
transcripts/  raw per-chapter VTT
tools/        all executable code
docs/         agents/, adr/
specs/        chore and feature plans
projects/     side projects that are not the archive
```

The rule is enforced, not just documented: `tools/tests/validate_structure.py`
fails if an expected top-level directory is missing **or an unexpected one
appears**. That second half is the part that stops a new `output/`-shaped tree
from arriving next quarter.

## Alternatives rejected

**Keep source-of-origin names and document the mapping.** This is what the old
`README.md` did. It failed for a structural reason rather than a stylistic one:
a mapping has to be memorised or looked up on every access, and it drifts
silently because nothing verifies it. The `⚠` section explaining the symlinks
existed precisely because the names could not explain themselves.

**Split into multiple repositories** (archive / codebases / media). Rejected:
the hardlink between `media/final/` and the catalog only works inside one
filesystem tree, the `codebase/` symlinks would become cross-repo, and the
common operation — "read the transcript, then read what he built" — would need
two checkouts kept in sync.

**Flatten everything into `catalog/` with codebases nested inside each lesson.**
Rejected: several codebases are shared by more than one lesson and by YouTube
videos, so nesting forces either duplication or a symlink web pointing sideways
into other lessons, which is worse than pointing into one flat `codebases/`.

## Consequences

- Routing is derivable, so `CLAUDE.md` can carry a deterministic
  question → path table instead of prose.
- `codebase/` symlinks now resolve into one predictable tree, shrinking the
  README's warning to a single line.
- Every path in the top-level docs changed. The structure test asserts that
  every backticked path in `README.md`, `CLAUDE.md` and `catalog/README.md`
  exists on disk, so that class of drift now fails loudly.
- History was preserved: the moves were committed as renames
  (`git diff -M` detected 3,148 for the un-recorded root move alone, and 7,437
  for the codebases move), so `git log --follow` still works across them.

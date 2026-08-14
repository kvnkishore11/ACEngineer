# `codebases/` — every codebase built or referenced in the archive

One home for all the code. Four sub-trees, named for where the codebase was
used, not for who wrote it:

| Tree | What lives here |
|---|---|
| `tac/` | The 8 Tactical Agentic Coding lesson codebases (`tac-1` … `tac-8`) |
| `ah/` | The 6 Agentic Horizon module codebases |
| `ma/` | The member-asset bonus codebases |
| `yt/` | Upstream repos referenced by the YouTube videos, as `<owner>__<repo>` |

Count them rather than trusting this file:

```sh
for t in tac ah ma yt; do printf "%s: %s\n" "$t" "$(ls codebases/$t | wc -l)"; done
```

## The one rule: these are read, never edited

Every tree here is a **vendored upstream snapshot**. Read them to see what was
built; do not fix, refactor, or reformat them. An edit here is indistinguishable
from upstream content the next time someone reads the archive, and there is no
longer a per-tree `.git` to diff against.

If you need to change something, copy it out into `projects/` first.

## Why there is no `.git` in each tree

These were independent clones. Their nested `.git` directories were removed so
the contents track as ordinary files in this repository — otherwise `git add`
records them as gitlinks (submodules with no `.gitmodules`) and a fresh clone
gets empty directories. Provenance — upstream URL and the exact commit each tree
was taken from — lives in [`REPOS.md`](../REPOS.md). To recover a tree's own
history, re-clone it from there.

Removing those `.git` directories also removed two GitHub personal access tokens
that were sitting in plaintext in their `config` remote URLs.

## Two trees that are not what they look like

- **`ah/orchestrator-agent-with-adws/.upstream/`** — a pristine snapshot kept
  deliberately because the parent has diverged from it. See the README inside it.
- **`yt/disler__pi-vs-claude-code__pi-to-pi/`** — not a duplicate of
  `yt/disler__pi-vs-claude-code`. It is the enriched working copy from the
  pi-to-pi lesson and is a superset: it adds `.codex/`, `.cursor/`, `.ok/`,
  `.opencode/`, extra skills and `opencode.json`. Both are kept on purpose.

## Vendored agent config

Several of these trees ship their own `.claude/`, `.cursor/` or `.pi/`
directories, including agent skills. That is archived lesson content — it is not
this repository's agent configuration, and it should not be treated as such.

---
description: Gain a general understanding of this repo — the IndyDevDan archive
---

# Prime

> Execute the `Workflow` section to understand this repository, then `Report`.

## Workflow

### Run

`git ls-files | cut -d/ -f1 | sort | uniq -c | sort -rn` — see the shape of the
repository. Summarize rather than list: a bare `git ls-files` prints many
thousands of paths, most of them vendored `codebases/`.

### Read

- `README.md` — what this repository is and how it is laid out.
- `CLAUDE.md` — the routing table and the two things a file listing will not
  tell you.

## Report

Summarize your understanding of the repository.

# Repository Tracking

Source of truth for upstream URLs of all sub-projects under `AgenticEngineer/`.
Use this when pulling updates. All URLs use `github.com/disler/<name>.git`.

> **Auth**: these repos are private. You need a valid GitHub PAT.
> Prefer `gh auth login` or git's credential helper over embedding the PAT in URLs (which leaks it into shell history and git config).

---

## 1. TAC — Tactical Agentic Coding

The foundational 8-week course. These were merged as git subtrees; no matching public upstream repo exists at `github.com/disler/<folder>`.

| Folder | Notes |
|---|---|
| `tac/tac-1` | Foundation — basic prompts, commands, file structure |
| `tac/tac-2` | Structure — slash commands, workflow basics |
| `tac/tac-3` | Workflows — SDLC integration, enhanced commands |
| `tac/tac-4` | Automation — ADW system, agent pipelines |
| `tac/tac-5` | Testing — E2E automation, quality gates |
| `tac/tac-6` | Production — skills, capabilities, documentation |
| `tac/tac-7` | Integration — ISO workflows, complete system |
| `tac/tac-8` | Mastery — 5 architectural patterns |

> **Update**: These have no known upstream. To refresh, re-clone or re-add the source if you have it.

---

## 2. Agentic Horizon — Core Modules

The four mastery-level modules plus supporting repos.

### Independent clones (have their own `.git/`)

| Folder | Upstream | Update command |
|---|---|---|
| `agentic-horizon/building-specialized-agents` | `github.com/disler/building-specialized-agents` | `git -C agentic-horizon/building-specialized-agents pull --ff-only` |

### Git subtrees (vendored into the parent `AgenticEngineer` repo)

Update with `git subtree pull --prefix=<folder> <url> main` from the repo root.
This creates a merge commit in `AgenticEngineer`.

| Folder | Confirmed upstream | Notes |
|---|---|---|
| `agentic-horizon/agentic-prompt-engineering` | `github.com/disler/agentic-prompt-engineering` | not yet diffed against upstream |
| `agentic-horizon/elite-context-engineering` | `github.com/disler/elite-context-engineering` | not yet diffed against upstream |
| `agentic-horizon/multi-agent-orchestration` | `github.com/disler/multi-agent-orchestration` | has local additions on top of upstream — overlay with `rsync` (no deletions) or `git subtree pull` to preserve them |
| `agentic-horizon/agent-experts` | `github.com/disler/agent-experts` | identical to upstream as of last check |
| `agentic-horizon/orchestrator-agent-with-adws` | `github.com/disler/orchestrator-agent-with-adws` | identical to upstream as of last check |

---

## 3. Agentic Horizon — Extras (member assets codebases)

Bonus assets beyond the core modules. All are independent clones under
`agentic-horizon-extras/`, and **also linked at `member-assets/` root**
(symlinks → same trees; video+transcripts live beside them in `member-assets/`).

| Canonical folder | Also via | Upstream | Update command |
|---|---|---|---|
| `agentic-horizon-extras/ceo-agents` | `member-assets/ceo-agents` | `github.com/disler/ceo-agents` | `git -C agentic-horizon-extras/ceo-agents pull --ff-only` |
| `agentic-horizon-extras/lead-agents` | `member-assets/lead-agents` | `github.com/disler/lead-agents` | `git -C agentic-horizon-extras/lead-agents pull --ff-only` |
| `agentic-horizon-extras/ui-agents` | `member-assets/ui-agents` | `github.com/disler/ui-agents` | `git -C agentic-horizon-extras/ui-agents pull --ff-only` |
| `agentic-horizon-extras/the-verifier-agent-system` | `member-assets/the-verifier-agent-system` | `github.com/disler/the-verifier-agent-system` | `git -C agentic-horizon-extras/the-verifier-agent-system pull --ff-only` |

---

## Temporary/scratch clones (safe to delete)

Nesting inside each module keeps the project root clean:

- `agentic-horizon/agent-experts/.upstream/` — diff-check copy
- `agentic-horizon/orchestrator-agent-with-adws/.upstream/` — diff-check copy

## How to overlay upstream changes without deleting local files

```sh
git clone https://<PAT>@github.com/disler/<name>.git /tmp/<name>-upstream
rsync -av --exclude='.git' /tmp/<name>-upstream/ <name>/
rm -rf /tmp/<name>-upstream
git status --short <name>/   # review before committing
```

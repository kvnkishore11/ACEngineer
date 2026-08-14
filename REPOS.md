# Repository provenance

Where every vendored codebase under `codebases/` came from. Use this to refresh
a tree, or to recover its own git history.

> **These trees have no `.git/` of their own.** They were independent clones;
> their nested `.git` directories were removed so the contents track as ordinary
> files in this repository. Without that, `git add` records them as gitlinks —
> submodules with no `.gitmodules` — and a fresh clone gets empty directories.
> Removing them also removed two GitHub personal access tokens that were sitting
> in plaintext in their remote URLs.

> **Auth**: most of these repos are private. Use `gh auth login` or git's
> credential helper. Never embed a PAT in a URL — it leaks into shell history,
> into `.git/config`, and from there into anything that reads the tree.

---

## Refreshing a tree

There is no `git pull` here. Clone upstream to a scratch path and overlay:

```sh
git clone https://github.com/disler/<name>.git /tmp/<name>-upstream
rsync -av --exclude='.git' /tmp/<name>-upstream/ codebases/<tree>/<name>/
rm -rf /tmp/<name>-upstream
git status --short codebases/<tree>/<name>/   # review before committing
```

`rsync` without `--delete` on purpose: several trees carry local work done
while following the lesson, and that is the point of keeping them.

---

## 1. `codebases/tac/` — Tactical Agentic Coding

The foundational 8-week course. Merged as git subtrees; no matching public
upstream repo exists at `github.com/disler/<folder>`.

| Folder | Notes |
|---|---|
| `codebases/tac/tac-1` | Foundation — basic prompts, commands, file structure |
| `codebases/tac/tac-2` | Structure — slash commands, workflow basics |
| `codebases/tac/tac-3` | Workflows — SDLC integration, enhanced commands |
| `codebases/tac/tac-4` | Automation — ADW system, agent pipelines |
| `codebases/tac/tac-5` | Testing — E2E automation, quality gates |
| `codebases/tac/tac-6` | Production — skills, capabilities, documentation |
| `codebases/tac/tac-7` | Integration — ISO workflows, complete system |
| `codebases/tac/tac-8` | Mastery — 5 architectural patterns |

> No known upstream. To refresh, re-add the source if you have it.

---

## 2. `codebases/ah/` — Agentic Horizon modules

| Folder | Upstream | Pinned at |
|---|---|---|
| `codebases/ah/agent-experts` | `github.com/disler/agent-experts` | `cad5e11` |
| `codebases/ah/agentic-prompt-engineering` | `github.com/disler/agentic-prompt-engineering` | — |
| `codebases/ah/building-specialized-agents` | `github.com/disler/building-specialized-agents` | `7cd9ce1` |
| `codebases/ah/elite-context-engineering` | `github.com/disler/elite-context-engineering` | — |
| `codebases/ah/multi-agent-orchestration` | `github.com/disler/multi-agent-orchestration` | — |
| `codebases/ah/orchestrator-agent-with-adws` | `github.com/disler/orchestrator-agent-with-adws` | `fb99cd2` |

`multi-agent-orchestration` and `orchestrator-agent-with-adws` both carry local
additions on top of upstream — overlay, never replace.

`codebases/ah/orchestrator-agent-with-adws/.upstream/` is a pristine snapshot at
`fb99cd2`, kept because the parent diverged from it. See the README inside it.
The equivalent snapshot under `agent-experts/` was byte-identical to its parent
and has been deleted.

---

## 3. `codebases/ma/` — member-asset codebases

| Folder | Upstream | Pinned at |
|---|---|---|
| `codebases/ma/ceo-agents` | `github.com/disler/ceo-agents` | `ccf74c9` |
| `codebases/ma/lead-agents` | `github.com/disler/lead-agents` | `abc75d9` |
| `codebases/ma/the-verifier-agent-system` | `github.com/disler/the-verifier-agent-system` | `d021468` |
| `codebases/ma/ui-agents` | `github.com/disler/ui-agents` | `7d36778` |

`ceo-agents` had 7 uncommitted local changes at the time it was vendored; the
working tree as archived is what is here.

---

## 4. `codebases/yt/` — repos referenced by the YouTube videos

Named `<owner>__<repo>`. All public. Attached to their video by
`tools/youtube/attach_codebases.py`, which reads the GitHub link out of the
video description.

List them with their pinned commits:

```sh
ls codebases/yt/
```

| Folder | Upstream | Pinned at |
|---|---|---|
| `disler__agent-sandbox-skill` | `github.com/disler/agent-sandbox-skill` | `ac460ee` |
| `disler__agent-sandboxes` | `github.com/disler/agent-sandboxes` | `1a72555` |
| `disler__agentic-drop-zones` | `github.com/disler/agentic-drop-zones` | `16a347b` |
| `disler__agentic-finance-review` | `github.com/disler/agentic-finance-review` | `74ea7cd` |
| `disler__bash-damage-from-within` | `github.com/disler/bash-damage-from-within` | `f639414` |
| `disler__beyond-mcp` | `github.com/disler/beyond-mcp` | `db930dc` |
| `disler__big-3-super-agent` | `github.com/disler/big-3-super-agent` | `d5d2c10` |
| `disler__bowser` | `github.com/disler/bowser` | `26541ac` |
| `disler__claude-code-damage-control` | `github.com/disler/claude-code-damage-control` | `f4792c4` |
| `disler__claude-code-hooks-mastery` | `github.com/disler/claude-code-hooks-mastery` | `052ad1c` |
| `disler__claude-code-hooks-multi-agent-observability` | `github.com/disler/claude-code-hooks-multi-agent-observability` | `8a6e5cf` |
| `disler__fork-repository-skill` | `github.com/disler/fork-repository-skill` | `ba196f6` |
| `disler__fusion-harness` | `github.com/disler/fusion-harness` | `5852f2e` |
| `disler__infinite-agentic-loop` | `github.com/disler/infinite-agentic-loop` | `6e9a012` |
| `disler__inkwell-agent-sandboxes-and-software-factory` | `github.com/disler/inkwell-agent-sandboxes-and-software-factory` | `92f1701` |
| `disler__install-and-maintain` | `github.com/disler/install-and-maintain` | `558b5c8` |
| `disler__learning-cmux-with-agents` | `github.com/disler/learning-cmux-with-agents` | `6eaacab` |
| `disler__live-bench` | `github.com/disler/live-bench` | `bb3ca35` |
| `disler__mac-mini-agent` | `github.com/disler/mac-mini-agent` | `0d9fa22` |
| `disler__max-your-cc-sub` | `github.com/disler/max-your-cc-sub` | `2ffa8c9` |
| `disler__nano-agent` | `github.com/disler/nano-agent` | `7518889` |
| `disler__pi-agent-observability` | `github.com/disler/pi-agent-observability` | `cbb8cc3` |
| `disler__pi-vs-claude-code` | `github.com/disler/pi-vs-claude-code` | `0ed11f4` |
| `disler__pi-vs-claude-code__pi-to-pi` | `github.com/disler/pi-vs-claude-code` | `b93c3f1` |
| `disler__planf3` | `github.com/disler/planf3` | `f34b7ba` |
| `disler__super-simple-software-factory` | `github.com/disler/super-simple-software-factory` | `de31374` |
| `disler__the-library` | `github.com/disler/the-library` | `47f455c` |
| `disler__the-verifier-agent` | `github.com/disler/the-verifier-agent` | `aa18d68` |
| `gist__disler__c7719b79a107` | `gist.github.com/disler/c7719b79a10762d87e89617c1f4a11c1` | `cc6d2d0` |
| `pvolok__mprocs` | `github.com/pvolok/mprocs` (branch `master`) | `c2f7667` |

`disler__pi-vs-claude-code__pi-to-pi` is the enriched working copy from the
pi-to-pi lesson, not a duplicate of `disler__pi-vs-claude-code`: it is a
superset, adding `.codex/`, `.cursor/`, `.ok/`, `.opencode/`, extra skills and
`opencode.json`. Both are kept deliberately.

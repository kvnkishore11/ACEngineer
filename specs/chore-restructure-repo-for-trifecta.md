# Chore: Restructure the repository around a role-based top level (team / agents / owner)

## Chore Description

`AgenticEngineer` is a study archive of IndyDevDan's agentic-engineering material —
18 course lessons, 57 YouTube videos, ~30 cloned repos, ~22 GB of media, and every
codebase built in them. It has grown by accretion and the top level no longer
answers the one question everybody (human or agent) asks first: **"where does this
kind of thing live?"**

Concretely, the repo is broken in seven distinct ways. All seven were verified
against the working tree on 2026-08-13.

### 1. Git is lying about the tree — highest severity

The course codebases were physically moved from the repo root into `tac/`,
`agentic-horizon/`, and `agentic-horizon-extras/`, but **that move was never
committed**. `HEAD` still lists `agent-experts/`, `tac-1/` … `tac-8/`,
`orchestrator-agent-with-adws/`, `multi-agent-orchestration/`,
`building-specialized-agents/`, `elite-context-engineering/`, and
`agentic-prompt-engineering/` at the root.

| Measure | Count |
|---|---:|
| Tracked files in `HEAD` | 4,730 |
| Pending deletions in `git status` | 3,269 |
| Untracked paths (`--untracked=all`) | 10,606 |

Everything built since commit `0020813` is untracked: the whole `IndyDevDan/`
catalog (5,573 files), `CLAUDE.md`, `README.md`, `docs/`, `scripts/`, `tools/`,
`videos/`, `final videos/`, `member-assets/`. `git status` is unreadable, `git log
--follow` is broken across the move, and any agent that runs `git status` to orient
itself gets ~14,000 lines of noise instead of signal.

### 2. No ignore policy, so 22 GB of media reads as "changes"

`.gitignore` is four lines and its only real rule points at
`multi-agent-orchestration/asset/*.safetensors` — **a path that no longer exists**
(it is now `agentic-horizon/multi-agent-orchestration/asset/`). The rule is dead.

Untracked and unignored right now: `videos/` (13 GB), `final videos/` (8.9 GB),
`agentic-horizon/multi-agent-orchestration/` (1.2 GB), `tac/tac-7` (179 MB),
`tac/tac-8` (95 MB), plus 14 `node_modules/`, 3 `.venv/`, 246 `__pycache__/`,
92 `dist/`, and 4 `build/` directories. `.git` is already 11 GB.

### 3. Directory names contain spaces

`tac transcripts/` (1,362 tracked files) and `final videos/` (19 files) must be
quoted in every shell command, script, and agent glob. Two of the subdirectories
inside `tac transcripts/` are also misspelled: `Buidling Specialized Agents/` and
`mulit agent orchestration/`. Also `IndyDevDan/raw/prompt-naming_agent copy.md`.

### 4. The top level mixes two incompatible naming axes

Some directories are named for **where the material came from** (`IndyDevDan/`,
`tac/`, `agentic-horizon/`, `agentic-horizon-extras/`, `member-assets/`,
`tac transcripts/`); others are named for **what role they play** (`output/`,
`scripts/`, `tools/`, `docs/`, `videos/`). There is no rule an agent can apply, so
routing is memorised rather than derived. Source-of-origin naming is especially
useless here — *every* directory in the repo is IndyDevDan material, so
`IndyDevDan/` at the top level carries zero discriminating information.

The three-way `tac/` → `agentic-horizon/` → `agentic-horizon-extras/` split is the
same concept ("a codebase from a lesson") under three unrelated names, which is
why `README.md` needs a dedicated ⚠ section just to explain where `codebase/`
symlinks point.

### 5. The same content exists in three or four places

| Content | Duplicate locations |
|---|---|
| Finished lesson video | `final videos/<key>.mp4`, `IndyDevDan/<key>/video/<key>.mp4` (hardlinked, 2 links), `videos/<key>/…-cdp-15fps-audio-fixed.mp4` (separate raw capture) |
| Lesson transcript | `tac transcripts/<Course Name>/*.vtt` (raw), `IndyDevDan/<key>/transcript/*.{vtt,md,txt}` (canonical), `member-assets/transcripts/*` (MA only) |
| Distilled writing | `output/` (24 entries), `IndyDevDan/artifacts/`, `IndyDevDan/research/`, `IndyDevDan/raw/`, `IndyDevDan/book/`, `IndyDevDan/dojo/ai_docs/` |
| "The Indy System" doc | `output/THE-INDY-SYSTEM.md`, `IndyDevDan/artifacts/THE-INDY-SYSTEM.md`, `IndyDevDan/THE-SYSTEM.md` |
| `pi-vs-claude-code` repo | `youtube/pi-to-pi-two-way-agent-orchestration/pi-vs-claude-code/`, `IndyDevDan/youtube/_repos/disler__pi-vs-claude-code/` |
| MA codebases | `agentic-horizon-extras/<name>/` and `member-assets/<name>` (symlink) and `IndyDevDan/ma-N-*/codebase` (symlink) |
| Two full codebase copies | `agentic-horizon/agent-experts/.upstream/` (19 MB, 825 files), `agentic-horizon/orchestrator-agent-with-adws/.upstream/` (20 MB, 900 files) |

`member-assets/` in particular is a *build artifact* — an intermediate staging tree
from the MA download run — that has been left standing next to the finished
`IndyDevDan/ma-*` lesson folders it produced.

### 6. Executable code is scattered across six homes, none of them tested

`scripts/` (3 files), `process_transcripts.py` (repo root), `tools/course-recorder/`
(14 files), `member-assets/postprocess_ma.py`, `IndyDevDan/youtube/*.py` (5 files),
`IndyDevDan/dojo/*.py`, `IndyDevDan/the-build-loop/build.py`, `videos/process_media.sh`.

Python living *inside* the data trees means an agent reading `IndyDevDan/youtube/`
for lesson content trips over build scripts and `__pycache__/`. There is no
dependency manifest, no test, and no lint at the repo level, even though `uv` is
installed and the archived courses all use PEP 723 single-file scripts.

### 7. The agent-context layer is thin, stale, and partly fictional

- Root `CLAUDE.md` is 13 lines. It promises "one `CONTEXT.md` + `docs/adr/` at the
  repo root" — **neither exists**. An agent following that instruction fails.
- No `AGENTS.md`, so non-Claude agents get nothing.
- `.claude/commands/` holds 5 files, two of which (`create-react-component.md`,
  `generate-component-tests.md`) are boilerplate for a React project that does not
  exist in this repo.
- `.claude/worktrees/quirky-williamson-0bbe59/` is a **55 MB stale worktree pinned
  to the pre-move layout** (`7e8ebcb`), and `git worktree list` reports a second,
  prunable worktree pointing at a deleted `AgenticKanban-api-websocket` directory.
- 13 local branches, 10 of them machine-generated ADW names like
  `feature-1760937963849-9461`.
- 2 tracked `.DS_Store` files; `.idea/` is tracked-and-deleted.
- Counts in prose are stale: `IndyDevDan/README.md` says "53 videos", disk says 57.

### 8. A second, unrelated project is squatting in the root

`MISSION.md`, `NOTES.md`, `RESOURCES.md`, `plans/`, `lessons/`, `learning-records/`,
`reference/`, and `docs/guides/local-visual-plan-onboarding.html` are all about
customising the `/visual-plan` Claude skill. They have nothing to do with the
IndyDevDan archive, yet they sort to the top of the root listing and are the first
thing a new teammate or a freshly primed agent reads.

### What this chore delivers

A single naming rule at the top level — **a directory is named for the role it
plays, never for where its contents came from** — applied consistently, with the
git history made truthful, the 22 GB of media ignored rather than pending, all
executable code consolidated under `tools/`, a real agent-routing layer, and an
automated structure test so the layout cannot silently rot again.

**Target top-level layout**

```
AgenticEngineer/
├── README.md                  # human front door
├── CLAUDE.md                  # agent front door — the routing table
├── AGENTS.md                  # symlink → CLAUDE.md (non-Claude agents)
├── CONTEXT.md                 # domain model / ubiquitous language (promised by CLAUDE.md)
├── .gitignore  .gitattributes
├── catalog/                   # ← IndyDevDan/  : READ-ONLY front door to the material
│   ├── README.md  INDEX.json  CLAUDE.md
│   ├── courses/<track>-<n>-<slug>/   # video/ transcript/ metadata/ codebase/ README.md
│   ├── youtube/yt-NN-<slug>/         # same shape
│   └── _source/                      # raw + offline course-page dumps, shared assets
├── codebases/                 # ← tac/ + agentic-horizon/ + agentic-horizon-extras/ + youtube/ + _repos/
│   ├── tac/tac-1 … tac-8
│   ├── ah/<name>
│   ├── ma/<name>
│   └── yt/<owner>__<repo>
├── media/                     # ← videos/ + final videos/   (gitignored bytes, tracked manifest)
│   ├── final/<key>.mp4
│   ├── raw/<key>/
│   └── MANIFEST.md
├── transcripts/               # ← tac transcripts/  : raw per-chapter .vtt dumps
├── knowledge/                 # ← output/ + IndyDevDan/{artifacts,research,raw,book,dojo}
│   ├── distilled/  artifacts/  research/  book/  dojo/  drafts/
├── tools/                     # ALL executable code, one home
│   ├── catalog/  youtube/  recorder/  transcripts/  media/  tests/
├── docs/                      # agents/  guides/  adr/
├── specs/                     # chore + feature plans (this file)
├── projects/                  # side projects that are not the archive
│   └── local-visual-plan/     # ← MISSION/NOTES/RESOURCES + plans/ lessons/ learning-records/ reference/
└── .scratch/                  # issue tracker (unchanged — see docs/agents/issue-tracker.md)
```

## Relevant Files

Use these files to resolve the chore.

### Read first (orientation)

- `README.md` — the current human front door; documents the symlink model, the
  three tracks, and the rebuild commands. Every path in it changes.
- `CLAUDE.md` — 13-line agent front door; references `docs/agents/*` and promises a
  `CONTEXT.md` + `docs/adr/` that do not exist. Rewritten wholesale.
- `IndyDevDan/README.md` — the catalog table + per-lesson folder shape; the
  authoritative description of the lesson tree. Says "53 videos"; disk has 57.
- `IndyDevDan/INDEX.json` — machine index of the 18 lessons, consumed by agents.
- `IndyDevDan/youtube/INDEX.json` — 57-video index; **stores an absolute path**
  (`"root": "/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/youtube"`)
  which breaks for anyone else on the team. Must become repo-relative.
- `REPOS.md` — upstream URLs for every sub-project; its folder column uses the old
  `tac/tac-1`, `agentic-horizon/…` paths.
- `.claude/commands/prime.md` — the context primer agents run first; hardcodes
  `IndyDevDan/tac-*`, `IndyDevDan/youtube/_repos`, `IndyDevDan/dojo/ai_docs`.

### Git + hygiene

- `.gitignore` — 4 lines; its `multi-agent-orchestration/asset/…` rules point at a
  path that moved, so nothing is actually ignored. Rewritten.
- `.gitattributes` — **does not exist**. Needed to mark media binary, normalise line
  endings, and flag generated HTML as `linguist-generated`.
- `.idea/.gitignore`, `.idea/AgenticEngineer.iml`, `.idea/modules.xml` — tracked and
  already deleted on disk; must be removed from the index.
- `.DS_Store`, `IndyDevDan/.DS_Store` — 2 tracked, 7 on disk.
- `.claude/worktrees/quirky-williamson-0bbe59/` — 55 MB stale worktree at the
  pre-move layout; pure confusion for anyone grepping the repo.

### Trees that move (source → destination)

- `IndyDevDan/` (5,573 files, 1.2 GB) → split into `catalog/`, `knowledge/`, `tools/`.
  Its `<lesson>/video/*.mp4` entries are **hardlinks** into `final videos/` (verified:
  2 links, identical 232,324,224-byte inode) — moving both ends on the same volume
  preserves the link and costs no extra bytes.
- `tac/tac-1 … tac-8` (280 MB) → `codebases/tac/`.
- `agentic-horizon/` (6 codebases, 1.4 GB) → `codebases/ah/`.
- `agentic-horizon-extras/` (4 codebases, 52 MB) → `codebases/ma/`.
- `IndyDevDan/youtube/_repos/` (29 repos) → `codebases/yt/`.
- `youtube/pi-to-pi-two-way-agent-orchestration/` — duplicate of
  `_repos/disler__pi-vs-claude-code`; deleted after byte-comparison.
- `final videos/` (8.9 GB, 19 files) → `media/final/`.
- `videos/` (13 GB, 5,410 files) → `media/raw/`.
- `tac transcripts/` (1,362 files, 5.5 MB) → `transcripts/`, subdirectories renamed
  to lesson keys.
- `output/` (181 files, 3.3 MB) → `knowledge/`, deduplicated against
  `IndyDevDan/artifacts/`.
- `member-assets/` (54 files, 4.7 MB) — intermediate staging tree superseded by
  `IndyDevDan/ma-*`; deleted after verifying every asset is present in the catalog.
- `agentic-horizon/agent-experts/.upstream/`,
  `agentic-horizon/orchestrator-agent-with-adws/.upstream/` — 39 MB of duplicate
  codebase copies; deleted if byte-identical to their parent, kept with a README if not.

### Executable code to consolidate under `tools/`

- `scripts/build_indydevdan_catalog.py` → `tools/catalog/build_catalog.py` — builds
  the lesson folders, hardlinks videos, creates the `codebase/` symlinks, writes
  `INDEX.json`. **This is the script that regenerates every symlink**, so re-running
  it after the moves is how the links get re-pointed correctly.
- `scripts/materialize_course_pages_offline.py` → `tools/catalog/materialize_course_pages.py`.
- `scripts/process_tac7_transcripts.py`, `process_transcripts.py` (root) →
  `tools/transcripts/` (two near-identical VTT stitchers; merge into one
  parameterised script).
- `IndyDevDan/youtube/{weekly_update,build_video_folder,attach_codebases,fill_missing_codebases,rebuild_index}.py`
  → `tools/youtube/`. `weekly_update.py` is the live weekly updater documented in
  `README.md`; `attach_codebases.py` creates the 46 YouTube `codebase/` symlinks.
- `tools/course-recorder/` (14 files) → `tools/recorder/`.
- `member-assets/postprocess_ma.py` → `tools/catalog/postprocess_ma.py`.
- `videos/process_media.sh` → `tools/media/process_media.sh`.
- `IndyDevDan/dojo/{dojo,serve}.py`, `IndyDevDan/the-build-loop/build.py` — these are
  *runnable apps*, not build tooling; they move with their content to
  `knowledge/dojo/` and `knowledge/book/the-build-loop/`.

### The side project to extract

- `MISSION.md`, `NOTES.md`, `RESOURCES.md`, `plans/` (3 HTML), `lessons/` (1 HTML),
  `learning-records/` (1 MD), `reference/` (1 HTML),
  `docs/guides/local-visual-plan-onboarding.html` → `projects/local-visual-plan/`.
  `.scratch/local-visual-plan/` stays put — that is the issue-tracker convention.

### New Files

- `specs/chore-restructure-repo-for-trifecta.md` — this plan.
- `.gitattributes` — line endings, binary media, `linguist-generated` for built HTML.
- `AGENTS.md` — symlink to `CLAUDE.md` so non-Claude agents find the routing table.
- `CONTEXT.md` — the domain model `CLAUDE.md` already promises: what a *lesson*, a
  *track*, a *codebase*, an *artifact*, and a *distillation* mean in this repo.
- `docs/adr/0001-role-based-top-level-layout.md` — records this decision and the
  rejected alternatives, per the `docs/agents/domain.md` convention.
- `docs/adr/0002-media-is-ignored-not-tracked.md` — records the 22 GB decision.
- `catalog/CLAUDE.md`, `codebases/CLAUDE.md`, `knowledge/CLAUDE.md`,
  `tools/CLAUDE.md` — one-screen local routing rules loaded on demand.
- `media/MANIFEST.md` — the file list + sizes + SHA-256 for the ignored media, so the
  tree is auditable and reproducible without committing the bytes.
- `tools/tests/validate_structure.py` — PEP 723 single-file, stdlib-only structure
  test. **The durable deliverable**: it is the thing that keeps the layout honest.
- `tools/tests/README.md` — how to run and extend the structure test.
- `tools/README.md` — index of every script, what it does, how to run it.
- `Makefile` (or `justfile`, matching `IndyDevDan/dojo/justfile`) — `make validate`,
  `make catalog`, `make youtube`, so the entry points are discoverable without prose.

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. Take a safety net before touching anything

- Confirm the working directory is `/Users/kvnkishore/WebstormProjects/AgenticEngineer`
  and the branch is `main`.
- Create a restructure branch: `git switch -c chore/restructure-trifecta`.
- Tag the pre-restructure state: `git tag pre-restructure-2026-08-13`.
- Record the current inventory to a file that is **not** in the repo, so it survives
  the moves and can be diffed at the end:
  `find . -path ./.git -prune -o -type f -print | sort > /tmp/pre-restructure-files.txt`
  and `du -sh */ > /tmp/pre-restructure-sizes.txt`.
- Record the symlink map: `find . -path ./.git -prune -o -type l -exec sh -c 'printf "%s -> %s\n" "$1" "$(readlink "$1")"' _ {} \; | sort > /tmp/pre-restructure-symlinks.txt`.
  There are **69 catalog-owned symlinks**: 18 course `codebase/`, 46 YouTube
  `codebase/`, 4 `member-assets/`, and 1 `IndyDevDan/assets`. All resolve today
  (verified: zero broken links repo-wide). A further 12 symlinks live *inside*
  vendored codebases (`.venv/bin/python*`, `.cursor/rules/*.mdc`, `.pi/skills/bowser`)
  — those belong to the upstream projects, are covered by the new ignore policy, and
  must not be touched. This file is the ground truth for step 13.
- Do **not** `git stash`. The 3,269 pending deletions are real and must be committed,
  not shelved.

### 2. Write the ignore policy before staging anything

This must happen before any `git add`, or the 22 GB of media gets committed.

- Replace `.gitignore` with a full policy covering:
  - **OS/editor**: `.DS_Store`, `.idea/`, `.vscode/`, `*.swp`
  - **Python**: `__pycache__/`, `*.py[cod]`, `.venv/`, `venv/`, `.pytest_cache/`,
    `.mypy_cache/`, `.ruff_cache/`
  - **JS**: `node_modules/`, `dist/`, `build/`, `.next/`, `*.tsbuildinfo`
  - **Media bytes** (22 GB): `media/final/`, `media/raw/`, `*.mp4`, `*.m4a`, `*.mov`,
    `*.webm` — with `!media/MANIFEST.md` and `!media/**/*.json` so sync metadata and
    the manifest stay tracked
  - **Model weights**: `**/asset/*.safetensors`, `**/asset/gpt/`, `**/asset/tokenizer/`
    — note the leading `**/`, which fixes the currently-dead rule that assumed
    `multi-agent-orchestration/` sat at the repo root
  - **Agent scratch**: `.claude/worktrees/`, `worktrees/`
  - **Run logs**: `*.log`, `**/_weekly_run_*.json`, `**/_batch_summary_*.json`
    (keep `_weekly_last_run.json` — it is the idempotency state `weekly_update.py`
    depends on, so add `!**/_weekly_last_run.json`)
- Create `.gitattributes`:
  - `* text=auto eol=lf`
  - `*.mp4 -text`, `*.m4a -text`, `*.mov -text`, `*.png -text`, `*.gif -text`
  - `*.vtt text`, `*.md text`
  - `catalog/_source/course-pages-offline/** linguist-generated=true`
  - `knowledge/book/code/*.html linguist-generated=true`
  - `catalog/**/metadata/*.html linguist-generated=true`
- Sanity-check the policy before staging:
  `git status --porcelain --untracked=all | grep -c '^??'` should drop from 10,606
  to roughly the number of real, small, source files (low thousands, not five
  figures). If any `.mp4` still appears, fix the pattern before continuing.

### 3. Make git tell the truth about the tree

The move from root → `tac/` + `agentic-horizon/` was done on disk months ago and
never recorded. Commit it now, **before** any new moves, so git records it as a set
of renames rather than folding it into the restructure diff.

- Remove the already-deleted `.idea/` files from the index:
  `git rm -r --cached .idea` (they are gone from disk; this drops them from `HEAD`).
- Remove the tracked `.DS_Store` files: `git rm --cached .DS_Store IndyDevDan/.DS_Store`.
- Stage everything the new `.gitignore` allows: `git add -A`.
- Verify rename detection worked before committing:
  `git diff --cached -M --stat --diff-filter=R | tail -5` must show renames such as
  `agent-experts/... -> agentic-horizon/agent-experts/...`. If it shows pure
  delete+add, raise `-M`'s threshold with `git config diff.renameLimit 20000` and
  re-check. **Do not commit until renames are detected** — that is the only thing
  preserving history across the move.
- Commit: `chore(git): record the root→tac/agentic-horizon move and add an ignore policy`.
- Confirm `git status --porcelain` is now empty. This single commit takes the repo
  from 13,875 dirty paths to 0 and is the precondition for everything below.

### 4. Prune the dead weight

Each deletion below is verified-then-removed, never removed on assumption.

- **Stale worktrees**: `git worktree list` reports
  `.claude/worktrees/quirky-williamson-0bbe59` (55 MB, detached at the pre-move
  `7e8ebcb`) and a prunable `AgenticKanban-api-websocket`. Run
  `git worktree remove .claude/worktrees/quirky-williamson-0bbe59 --force` then
  `git worktree prune`, and confirm `git worktree list` shows only the main checkout.
- **Machine-named branches**: 13 local branches exist; 10 match
  `feature-*-<epoch>-<n>` or `chore-9-*` from old ADW runs. List them with
  `git branch --format='%(refname:short) %(committerdate:relative)'`, confirm each is
  merged or dead with `git branch --merged main`, then delete the dead ones. Keep
  `main`, `chore/restructure-trifecta`, and anything unmerged — report what you kept.
- **`.upstream/` duplicates**: for each of
  `agentic-horizon/agent-experts/.upstream/` and
  `agentic-horizon/orchestrator-agent-with-adws/.upstream/`, run
  `diff -rq <parent> <parent>/.upstream` (excluding `.upstream` itself). If identical,
  delete. If they differ, **keep them** and write a one-paragraph
  `.upstream/README.md` explaining what the divergence records — do not delete a
  pristine upstream snapshot just because it is large.
- **Duplicate repo clone**: byte-compare
  `youtube/pi-to-pi-two-way-agent-orchestration/pi-vs-claude-code/` against
  `IndyDevDan/youtube/_repos/disler__pi-vs-claude-code/`. If equal, delete the root
  `youtube/` tree entirely. If not, keep the differing files and note why.
- **`member-assets/`**: verify every `ma-N-*/video/*.mp4`, `ma-N-*/transcripts/*`,
  and `ma-N-*/meta/*` has a counterpart under `IndyDevDan/ma-N-*/`. Only when the
  check passes, delete `member-assets/` — but first move `postprocess_ma.py` (step 11)
  and fold `MANIFEST.json` + `SUMMARY.json` + `download.log` into
  `catalog/_source/ma-download/` as provenance.
- **Duplicate distillations**: `output/THE-INDY-SYSTEM.md`,
  `IndyDevDan/artifacts/THE-INDY-SYSTEM.md`, and `IndyDevDan/THE-SYSTEM.md` — diff
  all three, keep the newest/most complete as `knowledge/distilled/the-indy-system.md`,
  delete the other two. Do the same for `output/INDYDEVDAN-UNIVERSAL-METHOD.md` vs
  `IndyDevDan/research/indydevdan-principles.md` if they overlap.
- **Generated caches**: delete all 246 `__pycache__/` directories
  (`find . -type d -name __pycache__ -prune -exec rm -rf {} +`). They are ignored
  now but still clutter every `ls` and every agent file listing.
- Commit: `chore(prune): remove stale worktrees, duplicate trees, and generated caches`.

### 5. Create the target skeleton

- `mkdir -p catalog/courses catalog/youtube codebases/{tac,ah,ma,yt} media/{final,raw} transcripts knowledge/{distilled,artifacts,research,book,drafts} tools/{catalog,youtube,recorder,transcripts,media,tests} docs/adr projects specs`
- Add a `.gitkeep` only where a directory would otherwise be empty at commit time.
- Commit the empty skeleton separately so the subsequent `git mv` commits read as
  pure moves in review.

### 6. Move the codebases into one tree

Use `git mv` for every move in steps 6–12 so rename detection works.

- `git mv tac/tac-1 codebases/tac/tac-1` … through `tac-8`; then remove the empty `tac/`.
- `git mv agentic-horizon/<name> codebases/ah/<name>` for all 6:
  `agent-experts`, `agentic-prompt-engineering`, `building-specialized-agents`,
  `elite-context-engineering`, `multi-agent-orchestration`, `orchestrator-agent-with-adws`.
- `git mv agentic-horizon-extras/<name> codebases/ma/<name>` for all 4:
  `ceo-agents`, `lead-agents`, `the-verifier-agent-system`, `ui-agents`.
- `git mv IndyDevDan/youtube/_repos/<repo> codebases/yt/<repo>` for all 29.
- Write `codebases/README.md`: the four sub-trees, the rule that **these are vendored
  upstream snapshots — never edit them, read them**, and a pointer to `REPOS.md` for
  provenance.
- The `codebase/` symlinks in the lesson folders are now broken. That is expected and
  is fixed wholesale in step 13 by re-running the catalog builder — **do not hand-fix
  symlinks**, there are 64 of them and the builder owns their shape.

### 7. Move the catalog

- `git mv IndyDevDan/<track>-<n>-<slug> catalog/courses/<track>-<n>-<slug>` for all
  18 lesson folders (8 `tac-*`, 6 `ah-*`, 4 `ma-*`).
- `git mv IndyDevDan/youtube/yt-* catalog/youtube/` for all 57 video folders, plus
  the catalog-side JSON state (`INDEX.json`, `_inventory.json`,
  `_weekly_last_run.json`, `_codebase_attach_summary.json`).
- `git mv IndyDevDan/_source catalog/_source`; re-point the
  `IndyDevDan/assets -> _source/assets` symlink as `catalog/assets -> _source/assets`.
- `git mv IndyDevDan/INDEX.json catalog/INDEX.json` and
  `git mv IndyDevDan/README.md catalog/README.md`.
- Move the YouTube council/planning notes (`_council_*.md`, `_council_brief.md`) to
  `knowledge/drafts/youtube-council/` — they are working notes, not catalog data.

### 8. Move the media and stop tracking the bytes

- `git mv "final videos" media/final` — then flatten: the 19 files become
  `media/final/<key>.mp4` (they already use lesson-key names) and
  `media/final/README.md` merges into `media/README.md`.
- `git mv videos media/raw`. Keep the per-lesson subdirectories (`tac-1/`, `ah-1/`, …)
  and the sidecar `*-sync.json` files, which the recorder validation reads.
- Move `videos/_archive_before_fullscreen_capture_2026-06-15_0450/` to
  `media/raw/_archive/` and the loose logs (`ah-recording-queue.log`,
  `overnight-recording.log`, `pause-after-current.log`) to `media/raw/_logs/`.
- Move `MANIFEST.md`, `RECORDING_REPORT.md`, `SYNC_VALIDATION.{md,json}` to
  `media/` — these are the tracked, human-readable record of the 22 GB.
- **Verify the hardlinks survived**: `stat -f "%l %z %N" media/final/tac-1-hello-agentic-coding.mp4 catalog/courses/tac-1-hello-agentic-coding/video/tac-1-hello-agentic-coding.mp4`
  must still report `2` links and identical byte counts. If it reports `1`, the move
  crossed a filesystem boundary and duplicated 8.9 GB — stop and re-link.
- Generate `media/MANIFEST.md`: path, size, and SHA-256 for every file under
  `media/`, so the ignored tree stays auditable. Add a `tools/media/make_manifest.py`
  to regenerate it.
- Confirm the bytes are ignored: `git status --porcelain media/ | grep -c mp4` → `0`.

### 9. Move and normalise the raw transcripts

- `git mv "tac transcripts" transcripts` — the space in the name is gone.
- Rename each subdirectory to the lesson key it belongs to. **Verify each mapping by
  spot-comparing the first chapter's `.vtt` text against
  `catalog/courses/<key>/transcript/<key>.md` before renaming** — do not rename on
  the strength of the folder name alone:

  | Current | Files | Expected key |
  |---|---:|---|
  | `tac-1 vtt` | 45 | `tac-1-hello-agentic-coding` |
  | `tac-2` … `tac-8` | 94–133 | `tac-2-…` … `tac-8-…` |
  | `elite context engineering` | 148 | `ah-1-rd-framework-context-window-mastery` |
  | `Agentic Prompt Engineering` | 115 | `ah-2-seven-levels-agentic-prompt-formats` |
  | `Buidling Specialized Agents` *(sic)* | 135 | `ah-3-building-domain-specific-agents` |
  | `mulit agent orchestration` *(sic)* | 125 | `ah-4-multi-agent-orchestration-the-o-agent` |

  `ah-5`, `ah-6`, and the four `ma-*` lessons have no raw dumps here — that is
  correct, not a gap; note it in `transcripts/README.md`.
- Write `transcripts/README.md` stating plainly: **these are the raw per-chapter VTT
  dumps; the stitched, readable transcript is
  `catalog/courses/<key>/transcript/<key>.md` and that is what you should read.**
  This is the single most common wrong-file mistake an agent can make here.

### 10. Consolidate the derived writing under `knowledge/`

- `git mv IndyDevDan/artifacts knowledge/artifacts` (9 generated HTML/MD artifacts).
- `git mv IndyDevDan/research knowledge/research` (3 write-ups).
- `git mv IndyDevDan/book knowledge/book`; `git mv IndyDevDan/the-build-loop knowledge/book/the-build-loop`.
- `git mv IndyDevDan/dojo knowledge/dojo`; move `dojo/ai_docs/*` (10 distilled files:
  `tac.md`, `ah.md`, `ma.md`, `repos.md`, `yt-01-09.md` … `yt-46-53.md`) to
  `knowledge/distilled/` — these are the highest-value files in the repo and were
  buried three levels down inside an app directory.
- `git mv IndyDevDan/raw knowledge/drafts`; fix the space in
  `prompt-naming_agent copy.md` → `prompt-naming-agent-copy.md`.
- Move the loose root-level `IndyDevDan/` docs: `THE-SYSTEM.md`, `THE-BUILD-LOOP.md`,
  `indydevdan-system-codex.html`, `prompt.md` → `knowledge/distilled/` or
  `knowledge/drafts/` as appropriate (see the dedupe decision in step 4).
- Fold `output/` in: the 12 top-level MD files (`MASTER-GUIDE.md`, `CHEAT-SHEET.md`,
  `BEST-PRACTICES.md`, `GLOSSARY.md`, `FAQ.md`, `LEARNING-PATH.md`, …) →
  `knowledge/distilled/`; `output/analysis/`, `output/case-studies/`,
  `output/diagrams/`, `output/tac-transcript-analysis/`, `output/templates/` →
  `knowledge/research/` under the same names. Delete `output/📊-ANALYSIS-COMPLETE.txt`
  (a completion marker with an emoji filename) and `output/COMPLETION-REPORT.md`
  after confirming they carry no unique content.
- Write `knowledge/README.md` naming the difference between the sub-trees, because it
  is currently unguessable: `distilled/` = the compressed answer an agent should reach
  for first; `research/` = the long-form working analysis behind it; `artifacts/` =
  rendered deliverables; `book/` = the long-form build; `drafts/` = unfinished.
- `IndyDevDan/` should now be empty. Remove it.

### 11. Consolidate every executable into `tools/`

- `git mv scripts/build_indydevdan_catalog.py tools/catalog/build_catalog.py`
- `git mv scripts/materialize_course_pages_offline.py tools/catalog/materialize_course_pages.py`
- `git mv member-assets/postprocess_ma.py tools/catalog/postprocess_ma.py`
- `git mv catalog/youtube/{weekly_update,build_video_folder,attach_codebases,fill_missing_codebases,rebuild_index}.py tools/youtube/`
- `git mv tools/course-recorder tools/recorder`
- Merge `process_transcripts.py` (root) and `scripts/process_tac7_transcripts.py`
  into one `tools/transcripts/stitch_vtt.py` that takes the source directory and
  output path as arguments. Read both first — they are near-identical VTT stitchers
  differing only in hardcoded paths, so the merged version must keep whichever
  cleanup rules differ between them rather than picking one at random.
- `git mv media/raw/process_media.sh tools/media/process_media.sh`
- Remove the now-empty `scripts/` and the root `process_transcripts.py`.
- Add PEP 723 headers (`# /// script` … `requires-python`, `dependencies = []`) to
  every moved script so `uv run tools/<...>.py` works uniformly — this matches the
  single-file-script convention used throughout the archived courses.
- Write `tools/README.md`: a table of every script, one line on what it does, the
  exact `uv run` command, and whether it is safe to re-run (the catalog and YouTube
  builders are idempotent; the recorder is not).
- Add a `Makefile` with `validate`, `catalog`, `youtube`, `manifest`, and `clean`
  targets so the entry points are discoverable without reading prose.

### 12. Extract the unrelated side project

- `mkdir -p projects/local-visual-plan`
- `git mv MISSION.md NOTES.md RESOURCES.md projects/local-visual-plan/`
- `git mv plans lessons learning-records reference projects/local-visual-plan/`
- `git mv docs/guides/local-visual-plan-onboarding.html projects/local-visual-plan/`
- Write `projects/local-visual-plan/README.md` linking back to its issues at
  `.scratch/local-visual-plan/` and stating that this project is **not** part of the
  archive. Leave `.scratch/local-visual-plan/` where it is — `docs/agents/issue-tracker.md`
  defines `.scratch/<feature-slug>/` as the tracker location and that convention holds.
- Add `projects/README.md`: "side projects that live in this repo but are not the
  IndyDevDan archive; each gets one directory and one README."

### 13. Repair every path reference and regenerate the generated tree

The symlinks are broken right now. Fix them by regenerating, not by hand.

- Update the path constants in `tools/catalog/build_catalog.py`: lesson root
  `IndyDevDan/` → `catalog/courses/`, and the codebase source map
  `tac→tac/`, `ah→agentic-horizon/`, `ma→agentic-horizon-extras/` →
  `tac→codebases/tac/`, `ah→codebases/ah/`, `ma→codebases/ma/`. Derive all paths from
  a single `REPO_ROOT = Path(__file__).resolve().parents[2]` rather than from the
  current working directory, so the script runs from anywhere.
- Update `tools/youtube/*.py` the same way: video root → `catalog/youtube/`, repo
  cache → `codebases/yt/`.
- Fix the absolute path in the YouTube index: `"root"` must become the repo-relative
  `"catalog/youtube"`, and `rebuild_index.py` must stop writing absolute paths. This
  is what makes the repo work for the rest of the team, not just this machine.
- Re-run the builders and let them recreate all 68 symlinks and the video hardlinks:
  - `uv run tools/catalog/build_catalog.py`
  - `uv run tools/youtube/attach_codebases.py`
  - `uv run tools/youtube/rebuild_index.py`
- Diff the regenerated link map against the step-1 snapshot:
  `find . -path ./.git -prune -o -type l -exec sh -c 'printf "%s -> %s\n" "$1" "$(readlink "$1")"' _ {} \; | sort > /tmp/post-restructure-symlinks.txt`
  then `diff /tmp/pre-restructure-symlinks.txt /tmp/post-restructure-symlinks.txt`.
  Every difference must be an expected path change, and the catalog-owned count must
  land at **65** — 18 course + 46 YouTube + 1 assets, i.e. the original 69 minus the
  4 deleted `member-assets` links. The 12 vendored in-codebase symlinks should appear
  unchanged apart from their new `codebases/…` prefix.
- Sweep the remaining prose references with `rg` and fix them:
  `rg -l 'IndyDevDan/|agentic-horizon|agentic-horizon-extras|tac transcripts|final videos|member-assets|^scripts/' --glob '!codebases/**' --glob '!knowledge/book/**'`
  — `codebases/` is excluded because those are vendored upstream snapshots that must
  not be edited, and `knowledge/book/**/*-STATUS.md` is excluded because those are
  generated build logs. Report both exclusions rather than silently skipping them.
- Fix `REPOS.md`'s folder column to the new `codebases/{tac,ah,ma,yt}/…` paths.

### 14. Build the agent layer

This is what makes the structure *usable* by agents rather than merely tidy.

- Rewrite root `CLAUDE.md` as the routing table. It must state, in this order:
  1. **The one naming rule**: top-level directories are named for the role they play.
  2. **The routing table** — question → path:
     | Question | Path |
     |---|---|
     | What did he say? | `catalog/courses/<key>/transcript/<key>.md` |
     | What did he build? | `catalog/courses/<key>/codebase/` → resolves into `codebases/` |
     | Already distilled? | `knowledge/distilled/` — **check here before re-deriving** |
     | Prior deliverables? | `knowledge/artifacts/` |
     | Which lesson covers X? | `catalog/README.md`, `catalog/INDEX.json` |
     | Where did a codebase come from? | `REPOS.md` |
     | How do I rebuild? | `tools/README.md`, `make catalog` |
  3. **The two facts a file listing will not tell you**: `codebase/` is a symlink
     into `codebases/`, and `transcripts/` holds raw VTT while
     `catalog/…/transcript/` holds the readable version.
  4. **Never edit `codebases/`** — vendored upstream snapshots.
  5. **Counts drift** — count at read time, never trust a number in prose.
  6. Pointers to `docs/agents/*` (issue tracker, triage labels, domain docs).
- Create `AGENTS.md` as a symlink to `CLAUDE.md` (`ln -s CLAUDE.md AGENTS.md`) so
  non-Claude agents land on the same routing table.
- Write `CONTEXT.md` — the domain model `CLAUDE.md` currently promises but never
  delivered: definitions for *track*, *lesson*, *lesson key*, *codebase*,
  *distillation*, *artifact*, *raw transcript* vs *stitched transcript*.
- Write `docs/adr/0001-role-based-top-level-layout.md` and
  `docs/adr/0002-media-is-ignored-not-tracked.md` recording these decisions and the
  alternatives rejected (keeping source-of-origin names; git-lfs for the 22 GB).
- Add a one-screen `CLAUDE.md` to each of `catalog/`, `codebases/`, `knowledge/`,
  and `tools/` — local rules only, loaded on demand, no duplication of the root.
- Update `.claude/commands/prime.md` to the new paths, and have its `Run` section
  end with `uv run tools/tests/validate_structure.py` so priming also proves the
  tree is intact.
- Delete `.claude/commands/create-react-component.md` and
  `.claude/commands/generate-component-tests.md` — boilerplate for a React project
  that does not exist here.
- Add `.claude/commands/new-lesson.md` (the steps to ingest a new lesson) and
  `.claude/commands/weekly.md` (run the YouTube updater, rebuild, validate, commit)
  so the two recurring workflows are one command each.

### 15. Rewrite `README.md` for a human arriving cold

- Open with what the repo *is* in two sentences, then the layout tree from the
  Chore Description above, then the routing table, then the rebuild commands.
- Replace the "⚠ Every `codebase/` is a symlink" section: with `codebases/` as a
  real top-level tree the warning shrinks to one line, because the destination is
  now guessable from the source.
- **Remove every hardcoded count** ("18 lessons", "53 videos") and replace with the
  command that produces the number. The current README already warns that counts
  drift and then prints stale counts anyway — fix the cause, not the caveat.
- Add a "First 60 seconds" section for a new teammate: clone, `make validate`,
  `/prime`, read `knowledge/distilled/`.
- Update `catalog/README.md` the same way (its "53 videos" is wrong; disk has 57).

### 16. Write the structure test that keeps this from rotting

Create `tools/tests/validate_structure.py` — PEP 723, stdlib only, no dependencies,
exit non-zero with a specific message on any failure. It must assert:

1. Every expected top-level directory exists, and **no unexpected one does** (this is
   what stops a new `output/`-style tree from appearing next quarter).
2. No tracked path contains a space: `git ls-files | grep ' '` returns nothing.
3. Every `catalog/courses/<key>/` has `video/`, `transcript/`, `metadata/`,
   `codebase/`, `README.md`; and every `catalog/youtube/yt-*/` has `transcript/` and
   `metadata/`.
4. Every symlink in the repo resolves — zero broken links, repo-wide.
5. Every `codebase/` symlink resolves to a path **inside `codebases/`** (catches a
   link that resolves but points somewhere wrong).
6. `catalog/INDEX.json` and `catalog/youtube/INDEX.json` parse, contain no absolute
   filesystem paths, and their keys match the directories on disk **both ways**
   (no orphan index entry, no unindexed directory).
7. Every path mentioned in `README.md`, `CLAUDE.md`, and `catalog/README.md` inside
   backticks exists on disk — this is the check that stops documentation drift.
8. No `.mp4`/`.m4a`/`.mov` is tracked by git.
9. No `__pycache__`, `node_modules`, or `.venv` is tracked by git.
10. Every script under `tools/` compiles (`compileall`) and carries a PEP 723 header.

Write `tools/tests/README.md` explaining each assertion and how to add one. Wire it
into the `Makefile` as `make validate` and into `.claude/commands/prime.md`.

### 17. Commit in reviewable slices

Do not squash steps 3–16 into one commit. Use one commit per step, each with a
conventional-commit subject, so `git log` reads as the migration narrative and any
single step can be reverted alone:

`chore(git)`, `chore(prune)`, `chore(skeleton)`, `refactor(codebases)`,
`refactor(catalog)`, `refactor(media)`, `refactor(transcripts)`,
`refactor(knowledge)`, `refactor(tools)`, `refactor(projects)`,
`fix(paths)`, `docs(agents)`, `docs(readme)`, `test(structure)`.

### 18. Run the validation commands

Execute every command in the `Validation Commands` section below. All must pass with
zero errors before the chore is considered complete. If any fails, fix the cause and
re-run the whole set — do not report partial success.

## Validation Commands

Execute every command to validate the chore is complete with zero regressions.

- `uv run tools/tests/validate_structure.py` — the primary gate. Asserts all 10
  structural invariants from step 16 and exits non-zero with a specific message on
  the first failure.
- `python3 -m compileall -q tools/` — every consolidated script still parses.
- `test -z "$(git status --porcelain)" && echo CLEAN || (git status --porcelain | head -50; exit 1)` — the working tree is fully committed; nothing stranded mid-move.
- `test "$(git ls-files | grep -c ' ')" -eq 0 && echo "no spaces in tracked paths"` — the `tac transcripts/` and `final videos/` class of problem is gone.
- `test -z "$(find . -path ./.git -prune -o -type l ! -exec test -e {} \; -print)" && echo "all symlinks resolve"` — every symlink in the repo resolves; catches a broken `codebase/` link.
- `test "$(find catalog -type l | wc -l)" -eq 65 && echo "65 catalog symlinks"` — 18 course + 46 YouTube + 1 assets; catches a lesson whose `codebase/` link the builder failed to recreate.
- `test "$(git ls-files | grep -cE '\.(mp4|m4a|mov|webm)$')" -eq 0 && echo "no media tracked"` — the 22 GB stayed out of git.
- `test "$(git ls-files | grep -cE '(^|/)(__pycache__|node_modules|\.venv|\.DS_Store|\.idea)(/|$)')" -eq 0 && echo "no generated files tracked"`
- `python3 -c "import json,pathlib; [json.loads(pathlib.Path(p).read_text()) for p in ['catalog/INDEX.json','catalog/youtube/INDEX.json']]; print('indexes parse')"`
- `test "$(ls -d catalog/courses/tac-* catalog/courses/ah-* catalog/courses/ma-* | wc -l)" -eq 18 && echo "18 lessons present"` — nothing lost in the catalog move.
- `test "$(ls -d catalog/youtube/yt-* | wc -l)" -eq 57 && echo "57 videos present"`
- `test "$(ls codebases/tac | wc -l)" -eq 8 && test "$(ls codebases/ah | wc -l)" -eq 6 && test "$(ls codebases/ma | wc -l)" -eq 4 && test "$(ls codebases/yt | wc -l)" -eq 29 && echo "47 codebases present"`
- `stat -f '%l' media/final/tac-1-hello-agentic-coding.mp4 | grep -qx 2 && echo "video hardlinks intact"` — proves the 8.9 GB was not silently duplicated by the move.
- `git worktree list | wc -l | grep -qx 1 && echo "no stale worktrees"`
- `uv run tools/catalog/build_catalog.py --dry-run 2>/dev/null || uv run tools/catalog/build_catalog.py` — the catalog builder is idempotent against the new layout; re-running it produces no changes (verify with `git status --porcelain` immediately after).
- `diff <(find . -path ./.git -prune -o -type f -print | sed 's#.*/##' | sort -u) <(sed 's#.*/##' /tmp/pre-restructure-files.txt | sort -u) | grep '^>' | grep -vE '\.pyc$|__pycache__|DS_Store' | head -20` — every filename present before the restructure is still present after, ignoring deliberate deletions. Output should list only the files step 4 intentionally removed; anything else is data loss.

## Notes

### Do this in the stated order — step 3 is load-bearing

Committing the already-done root→`tac/`/`agentic-horizon/` move (step 3) **before**
making any new moves is what lets git record both migrations as renames. Reorder it
after step 6 and the two moves fold together into an unreadable 14,000-path diff with
no rename detection, and the history of every course codebase is severed. If
`git diff --cached -M --stat --diff-filter=R` shows no renames, stop and fix it
before committing.

### The 11 GB `.git` is a known problem and deliberately out of scope

`.git` is 11 GB against ~4,700 tracked files. Large blobs are already in history
(a 3.1 MB `tac-7` blob, a 1.9 MB GIF, a 1.2 MB PNG, a compressed MP4). Shrinking it
requires history rewriting (`git filter-repo` / BFG) plus a force-push to
`origin` — destructive, coordination-requiring, and unrelated to layout. This chore
only stops the bleeding via `.gitignore`. Raise history cleanup as a separate,
explicitly-approved chore; do not attempt it here.

### Media strategy: ignore, do not LFS

git-lfs 3.7.1 is installed but unused. Moving 22 GB into LFS means paying for and
syncing 22 GB on every clone — a poor trade for a study archive where the videos are
re-downloadable and already hardlinked locally. The plan ignores the bytes and tracks
`media/MANIFEST.md` (path + size + SHA-256) instead, so the tree stays auditable and
any missing file is detectable. `docs/adr/0002` records this so it is not silently
re-litigated.

### Deletions are verify-then-remove, never assume-then-remove

Every deletion in step 4 is gated on a `diff` that proves the content exists
elsewhere. `member-assets/`, the two `.upstream/` trees, and the duplicate
`pi-vs-claude-code` clone are each ~20–50 MB of *probably* redundant data. If any
comparison shows a difference, keep the tree and document why — losing a pristine
upstream snapshot to save 20 MB is a bad trade.

### Symlinks are regenerated, never hand-edited

There are 69 catalog-owned symlinks (18 course + 46 YouTube + `assets` + 4
member-asset ones being deleted, leaving 65). `tools/catalog/build_catalog.py` and
`tools/youtube/attach_codebases.py` own their shape. Hand-editing them is how the map and the builder drift apart; the
next builder run would silently overwrite the manual fixes. Change the builders'
path constants, re-run, and diff against the step-1 snapshot.

### Two things that are easy to get wrong and expensive to notice

1. **Hardlink preservation.** `catalog/courses/<key>/video/*.mp4` and
   `media/final/*.mp4` are the same inode. `git mv`/`mv` on the same volume preserves
   this; `cp`, `rsync` without `-H`, or a move across volumes silently duplicates
   8.9 GB. The `stat -f '%l'` check in the validation set exists specifically to catch
   this, because nothing else will.
2. **`transcripts/` vs `catalog/…/transcript/`.** The raw per-chapter VTT dumps and
   the stitched readable transcript are both "the transcript". An agent that reads
   `transcripts/tac-3/0.vtt` gets 90 seconds of a lesson and confidently answers from
   it. `transcripts/README.md` and the root `CLAUDE.md` routing table must both say
   which one to read.

### This is a large, mostly-mechanical change — keep it on a branch

Steps 6–12 move roughly 24,000 files. Work on `chore/restructure-trifecta`, commit
per step, and only merge to `main` after the full validation set passes. The
`pre-restructure-2026-08-13` tag from step 1 is the escape hatch.

### What "best for the trifecta" concretely means here

- **The team**: one naming rule, a `README.md` whose paths are verified by a test, a
  `make validate` that proves a fresh clone is intact, and no 22 GB surprise.
- **The agents**: a deterministic routing table in `CLAUDE.md` + `AGENTS.md`, a clean
  `git status`, per-tree `CLAUDE.md` for progressive disclosure, `knowledge/distilled/`
  promoted out of its burial spot, and a `/prime` that ends by proving the tree.
- **The owner**: `make catalog` / `make youtube` / `make validate` as the three verbs,
  the side project out of the front door, and a structure test that fails loudly the
  next time the layout starts to drift — instead of discovering it 3,269 uncommitted
  deletions later.

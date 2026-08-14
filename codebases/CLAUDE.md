# `codebases/` — local rules

1. **Never edit anything here.** Every tree is a vendored upstream snapshot.
   An edit is indistinguishable from upstream content to the next reader, and
   there is no per-tree `.git` left to diff against. Copy into `projects/` first.
2. **No tree has its own `.git`.** That is deliberate — see `README.md` here and
   `REPOS.md` for the upstream URL and pinned commit of each. Recover a tree's
   history by re-cloning from `REPOS.md`, not by looking for it locally.
3. **Their `.claude/`, `.cursor/` and `.pi/` directories are archived lesson
   content**, not this repository's agent configuration. Skills and commands
   found in them belong to the lesson being studied.
4. **Sub-trees are by usage**: `tac/`, `ah/`, `ma/`, `yt/`. A codebase can be
   referenced by more than one lesson and by YouTube videos — that is why they
   live in one flat tree and are reached by symlink.
5. Two trees are not what they look like: `ah/orchestrator-agent-with-adws/.upstream/`
   is a deliberately kept pristine snapshot, and
   `yt/disler__pi-vs-claude-code__pi-to-pi` is a superset of
   `yt/disler__pi-vs-claude-code`, not a duplicate.

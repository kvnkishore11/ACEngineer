# `.upstream/` — pristine upstream snapshot

This is a byte-for-byte snapshot of
`github.com/disler/orchestrator-agent-with-adws` at commit
`fb99cd2ced29b23b64b3fff2091d56758c22dbc0` (branch `main`).

**It is kept deliberately, because the parent tree has diverged from it.** The
sibling snapshot under `agent-experts/` was byte-identical to its parent and was
deleted; this one was not, so removing it would lose the only record of what the
lesson changed.

## What the divergence records

The parent tree carries local work done while following the lesson:

| Kind | Path |
|---|---|
| Added module | `apps/orchestrator_3_stream/backend/modules/kimi_auth.py` |
| Modified | `apps/orchestrator_3_stream/backend/main.py` |
| Modified | `apps/orchestrator_3_stream/backend/modules/agent_manager.py` |
| Modified | `apps/orchestrator_3_stream/backend/modules/autocomplete_agent.py` |
| Modified | `apps/orchestrator_3_stream/backend/modules/config.py` |
| Modified | `apps/orchestrator_3_stream/backend/modules/single_agent_prompt.py` |
| Modified | `apps/orchestrator_3_stream/backend/prompts/experts/orch_autocomplete/expertise.yaml` |
| Local-only | `.claude/data/`, `logs/`, `temp/`, `.env`, `package-lock.json` |

The interesting change is Kimi/Moonshot auth wired in as an
Anthropic-compatible provider — that is local work, not upstream.

## Seeing the diff

```sh
diff -rq --exclude=.git --exclude=.upstream --exclude=node_modules --exclude=.venv \
  codebases/ah/orchestrator-agent-with-adws \
  codebases/ah/orchestrator-agent-with-adws/.upstream
```

## Provenance

This tree no longer has its own `.git/` — the vendored codebases were flattened
into the parent repository so a fresh clone gets the complete archive. See
`REPOS.md` for the upstream URL and `codebases/README.md` for the rule that
these trees are read, never edited.

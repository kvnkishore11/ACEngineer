# AgenticEngineer

A study archive of IndyDevDan's agentic-engineering material. **Routing table
and layout live in [`README.md`](README.md)** — read it first (`/prime` does).
Conventions (issues, triage, domain) → `docs/agents/`.

## Gotchas (these cause confidently-wrong answers)

- **`codebase/` is a symlink** into `codebases/`; editing "through" it edits a
  vendored snapshot. **Never edit `codebases/`** — no `.git` of their own, and
  their `.claude/`/`.cursor/`/`.pi/` dirs are lesson content, not ours.
- **Two transcript kinds**: `transcripts/<key>/*.vtt` are raw 60–90s chapters;
  `catalog/courses/<key>/transcript/<key>.md` is the readable whole lesson —
  read that one.
- **Counts drift** — never trust a number in prose; count at read time.

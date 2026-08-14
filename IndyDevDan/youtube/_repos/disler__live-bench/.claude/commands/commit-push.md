---
description: Validate changes, commit with 'progress', and push to remote
---

# Commit & Push

## Purpose

Validate that the current working tree has meaningful changes, stage all modifications, commit with the message `progress`, and push to the current remote branch. Designed for rapid iteration — invoke after any set of changes to persist and push without friction.

## Variables

COMMIT_MESSAGE: "progress"

## Instructions

- ALWAYS commit with the exact message `progress` — no Co-Authored-By, no description, no embellishments
- Before committing, run `git status` and `git diff --stat` to confirm there are actual changes to commit
- If there are NO changes (clean working tree), report that and do nothing — do NOT create empty commits
- Stage all tracked and untracked changes with `git add -A`
- After committing, push to the current upstream branch
- If no upstream is set, push with `git push -u origin HEAD`
- If the push fails, report the error — do NOT force push
- Try `gscm` first as a shorthand for staging and committing — if it's not available, fall back to `git add -A && git commit -m 'progress'`

## Workflow

1. Run `git status` and `git diff --stat` to verify there are changes to commit
2. If the working tree is clean, skip to the Report section and report "No changes to commit"
3. Attempt to stage and commit:
   - Try: `gscm` (fast shorthand)
   - If `gscm` is not found, run: `git add -A && git commit -m 'progress'`
4. Run `git push` to push to the remote (use `git push -u origin HEAD` if no upstream is configured)
5. Now follow the `Report` section to report the completed work

## Report

Present results in this format:

**Commit & Push**: [success/failed/no changes]
**Branch**: [branch-name]
**Files changed**: [count]
**Push**: [success/failed with reason]

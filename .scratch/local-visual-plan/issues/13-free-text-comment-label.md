# 13 — Free-text comment label + agent infer edit/reply

Status: done

## Parent

`.scratch/local-visual-plan/PRD.md` (v2.1 amendments)

## What to build

Replace the fixed category select (`change` / `question` / `nit`) with a **free-text
label** the reviewer types per comment, rendered **bold on top** of the comment card.
The label rides in the annotation's WS payload.

The agent **infers intent** (edit the plan vs reply-only) from the free-text label
plus the comment body — there is no fixed enum to branch on. To keep a wrong guess
visible and correctable, the agent **states its read in the thread before acting**
(e.g. "treating this as a question — answering, not editing").

This couples with versioning (slice 12): a reply-only interpretation produces **no
artifact change → no version bump**; an edit interpretation changes the `.md` at the
mapped source line → bump. The label itself never forces a bump — only an actual edit
does.

Supersedes v2's fixed `change` / `question` / `nit` category.

## Acceptance criteria

- [x] The commit form takes a free-text label (no fixed enum); the label renders bold
      on top of the card
- [x] The label round-trips in the annotation WS payload to the agent
- [x] The agent states its inferred read (edit vs reply-only) in the thread before
      acting
- [x] A reply-only interpretation makes no `.md` edit (and therefore no version bump);
      an edit interpretation edits the mapped source line
- [x] Any color-coding / chips that assumed the old enum degrade gracefully to the
      free-text label
- [x] Tests: label round-trip shape; reply-only path produces zero artifact edits;
      edit path edits the mapped line

## Blocked by

- `11-batch-send-draft-sidebar.md` (the label lives on the draft card / round payload)

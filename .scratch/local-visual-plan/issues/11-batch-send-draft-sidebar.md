# 11 — Batch send: draft sidebar + per-item & batch send

Status: done

## Parent

`.scratch/local-visual-plan/PRD.md` (v2.1 amendments)

## What to build

Decouple **creating** an annotation from **sending** it. Today, committing an
annotation fires it straight over the WS to the agent (auto-send on every change).
Instead, committing parks the annotation in the sidebar as an **unsent draft** —
visible, editable, deletable — and the reviewer sends on their own schedule.

Two send affordances:

- **per-card Send** — fire one draft.
- **Send all (N)** — fire the whole queue of unsent drafts at once.

A send (one item or the batch) travels the WS as a single **round**: one or more
annotations delivered together. The agent's attend-loop wakes once per round and
processes every annotation in it as one unit — one edit pass, one re-render (the
version boundary in slice 12). Already-sent annotations are never re-sent by
"Send all."

Unsent drafts must **survive a live re-render**: when the agent applies a round and
the iframe reloads, queued drafts re-bind through the same anchor machinery
(quote / rect / element) and stay in draft state — never lost, never auto-sent.

Supersedes v2's implicit "each committed annotation sends immediately."

## Acceptance criteria

- [x] Committing an annotation parks it in the sidebar as an unsent draft; nothing
      goes over the WS on commit
- [x] A draft can be edited (label + body) and deleted before it is sent
- [x] Per-card Send fires exactly that annotation; Send all (N) fires every unsent
      draft as one round
- [x] The WS payload for a round carries 1+ annotations; the attend-loop wakes once
      per round and processes all of them together (one edit pass, one re-render)
- [x] Already-sent annotations are not re-sent by Send all
- [x] Unsent drafts survive a live re-render (re-bind anchors, stay in draft state,
      not auto-sent)
- [x] Tests: commit-does-not-send, single vs batch round payload shape, draft
      survives a re-render, sent-set is not re-sent

## Blocked by

None — builds on shipped slices `06` (server / attend-loop) and `09` (conversation).

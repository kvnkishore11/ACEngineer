# 10 — Full v2 round-trip smoke + test suite

Status: done

## What to build

Prove the complete v2 spine end to end and lock the contract with tests.

Render one sample plan from a compact `plans/<slug>.md` (default own-template) and
drive the full live round-trip:

1. invoke → compact `.md` authored → rendered `.html`
2. start the review server → shell iframes the pristine plan → overlay injected
3. select a text span + draw a rectangle, comment on each (threads, categories)
4. Send → agent edits the `.md` at the mapped source lines → re-render → iframe
   reloads in place → annotations re-bind → status flips to `addressed`
5. agent asks an in-page question → reviewer answers in-page → agent applies it
6. close the browser → server exits → agent reports "review closed"
7. confirm the on-disk `.html` is overlay-free and opens from `file://`

Also run the same sample through `--save-tokens` (docforge) and one
`--renderer=<skill>` delegation to confirm the overlay injects on each.

Consolidate the test seams across slices into a green suite (`bun test` + jsdom for
pure fns; a headless smoke for the server protocol).

## Acceptance criteria

- [ ] One sample renders from a compact `.md` and drives the full live round-trip
      (span + rect + thread + question) with no copy-paste
- [ ] Agent edits the `.md`, the iframe re-renders in place, and annotations re-bind
- [ ] Browser close shuts the server down and the agent reports "review closed";
      on-disk `.html` is overlay-free and opens from `file://`
- [ ] The same sample renders + reviews under `--save-tokens` (docforge) and one
      `--renderer=<skill>` delegation
- [ ] Test suite green: quote-anchor rebind, rect coveredSelectors anchor,
      annotation serialize, md-edit mapping, server protocol/lifecycle, thread status
- [ ] `file://` path surfaced for human review of the sample

## Blocked by

- `09-live-conversation-attend-loop.md`

# 09 — Full in-page conversation + threaded status + live re-render

Status: done

## What to build

Close the two-way loop: turn annotations into live threads, drive the agent's
attend-loop, and re-render the plan in place as feedback is applied.

**Threaded annotations.** Each span/rect annotation is a thread with a `status`
(`open → addressed → resolved`) and a `category` (`change` / `question` / `nit`,
color-coded). The shell's thread panel shows pins, the thread, the agent's replies,
and a status chip that flips as the agent works.

**Attend-loop processing.** When a reviewer clicks Send or answers an in-page
question, a signal reaches the agent's wait-loop (slice 06). The agent:
1. reads the new annotation(s) / answer(s),
2. edits `plans/<slug>.md` at the mapped `data-source-line` (span: at the quote;
   rect: across the covered lines),
3. re-renders to `plans/<slug>.html`,
4. the server pushes a reload → the **iframe reloads in place**; overlay re-binds
   anchors (slices 07/08),
5. posts its reply/question into the thread and flips status to `addressed`,
6. re-enters the wait.

**Agent questions in-page.** The agent can open a question on a thread (or a global
question) that the reviewer answers **in the page**; the answer travels the same WS
path and wakes the loop. Reviewer can mark a thread `resolved`.

`SKILL.md`: document the attend-loop contract, the edit→re-render→push cycle, and
that the agent acts per turn while the server stays live.

## Acceptance criteria

- [x] Each annotation is a thread with `status` open→addressed→resolved and a
      color-coded `category`
- [x] Send / in-page answer wakes the attend-loop; the agent reads it without the
      reviewer touching chat
- [x] Agent edits the `.md` at the mapped source line, re-renders, and the iframe
      reloads in place (annotations re-bind)
- [x] Agent replies and follow-up questions appear in the page; questions are
      answerable in the page
- [x] Status chip flips to `addressed` when the agent applies an edit; reviewer can
      mark `resolved`
- [x] Closing the browser ends the loop ("review closed") with threads preserved in
      the `.md` edits
- [x] jsdom/headless tests: md-edit mapping (annotation → exact md location), thread
      status transitions, WS conversation round-trip

## Blocked by

- `07-span-select-overlay-quote-anchor.md`
- `08-rectangle-snapshot-tool.md`

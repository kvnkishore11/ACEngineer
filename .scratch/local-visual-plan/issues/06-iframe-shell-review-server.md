# 06 — iframe-shell live review server (bun + WebSocket) + lifecycle

Status: done

## What to build

The live channel and its lifecycle — no annotations yet. A **bun** server (skill
already uses bun; native WS) that the agent starts in the background and owns via a
**Monitor wait-loop** (the attend-loop).

The server serves a **parent shell** page that loads the pristine
`plans/<slug>.html` in a **same-origin iframe** and opens a WebSocket back to the
server. The shell carries the (empty for now) toolbar + thread-panel chrome and the
WS client. The overlay injection point exists but is a stub until slice 07.

Lifecycle (the part the user explicitly wants):

- Server binds an ephemeral localhost port, single client, opens the default
  browser to the shell.
- Browser `beforeunload` → WS disconnect → server writes a **close-signal** and
  exits.
- The agent's attend-loop blocks on a signal (Monitor / until-loop): close-signal →
  loop exits, agent reports "review closed."
- Server is bound to the session process tree: session dies → server dies. No orphan
  processes.

The on-disk `plans/<slug>.html` MUST stay clean — overlay/server code lives only in
the shell/server, injected at serve-time, never written to the artifact.

`SKILL.md`: add the `review` flow — render (slice 05) → start server in background →
enter attend-loop → on close, end.

## Acceptance criteria

- [ ] Bun server serves a shell that iframes the pristine rendered plan
      (same-origin) and opens a WS channel
- [ ] Server binds an ephemeral localhost port, single client, and auto-opens the
      browser
- [ ] Agent starts the server in the background and enters a Monitor wait-loop bound
      to the session
- [ ] `beforeunload` → WS disconnect → close-signal → server exits → attend-loop
      exits ("review closed")
- [ ] Session process tree dies → server dies (no orphan process verified)
- [ ] On-disk `plans/<slug>.html` contains no overlay/server/WS code (artifact stays
      archival; `file://` still works)
- [ ] Headless protocol smoke: connect → ping → `beforeunload`-equivalent →
      close-signal emitted and observed by the loop

## Blocked by

- `05-markdown-source-render-flag.md`

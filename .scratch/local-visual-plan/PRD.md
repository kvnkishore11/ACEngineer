# PRD: `local-visual-plan` v2 — live span/region review

Status: ready-for-agent

`local-visual-plan` v1 turns a text plan into a single self-contained interactive
HTML file, reviewed via section-level notes/checkboxes copied back to chat as
anchored markdown (shipped — see issues `01`–`04`). v2 reshapes the review surface
into a **live, granular, two-way one**: select any text span or draw a rectangle
over the rendered plan, comment on it, and have the feedback flow **directly back
to the agent** — no copy-paste — over a live session in which the agent edits the
plan and you watch it re-render in place. The design is lifted in spirit from
Plannotator (arbitrary-span annotation + direct readback) and in implementation
from the author's own `Picanvas` "artifact theatre" (vanilla overlay: text
selection + rectangle tool + sticky comments).

## Problem Statement

v1's review loop has two ceilings:

1. **Granularity.** Feedback attaches to a whole *section* (a note + a checkbox).
   I cannot point at a single word, phrase, or a specific region of the rendered
   plan and say "this." I want letter/word/span-level precision, plus the ability
   to draw a box over an area to focus attention on it.
2. **Transport.** To give feedback I click "Copy feedback," switch to the chat,
   and paste an anchored-markdown blob. I want to **send straight from the page**,
   see the agent's edits reflected **live**, and answer the agent's follow-up
   questions **in the page** — a real back-and-forth, not a copy-paste relay.

Separately, while specifying v2 I confirmed a misconception worth recording: v1 is
**token-heavy**, not token-light. v1's agent hand-writes the entire 27–44 KB HTML
per plan (slot-fill of an 800-line template). The token-thrifty model I was
thinking of is the original hosted `visual-plan` (compact MDC/MDX blocks rendered
remotely) and its local cousin `docforge`/`editorial-report-v11` (compact `.mdxl`
source → renderer, ~12× less for the LLM to emit). v2 fixes this too.

## Solution

v2 keeps `/local-visual-plan` as the single manual entry point and the
single-self-contained-`.html` deliverable, but changes three things underneath:

1. **Markdown-canonical source.** The agent authors one compact `plans/<slug>.md`
   and a **renderer** turns it into `plans/<slug>.html`. The agent never
   hand-writes HTML again — token-light in every mode. The render is flag-selected
   (see below). Every rendered block carries a stable `data-block-id` and a
   `data-source-line` back to the markdown, so feedback maps to an exact source
   location and the agent edits the `.md`, not the HTML.

2. **Live two-way review server.** Invoking the skill (or `/local-visual-plan
   review <slug>`) starts a **session-bound localhost WebSocket server**. It serves
   a **parent shell** that loads the pristine rendered plan in a **same-origin
   iframe** and injects a **vanilla annotation overlay** (text-span select +
   rectangle tool + sticky threads), bridged to the shell by `postMessage`. You
   annotate; each "Send" travels over the socket to the agent; the agent edits the
   `.md`, re-renders, and the iframe **reloads in place**; the agent's replies and
   follow-up **questions appear in the page** and are answered there. Closing the
   browser shuts the server down and **notifies the agent**. The server lives only
   while the session is up — no orphan processes.

3. **Renderer-as-flag, token-light always.** The `.md` is rendered by, in order of
   default:
   - **own-template** (default) — the v1 look as a *renderer of markdown*: plan
     sections + hand-authored inline SVG + wireframe + click-through prototype,
     carried as raw-HTML passthrough in the markdown.
   - **docforge** via `--save-tokens` — the lean editorial renderer
     (`editorial-report-v11`'s engine). `--save-tokens` is an ergonomic alias for
     `--renderer=docforge`.
   - **any design skill** via `--renderer=<skill>` (e.g. `thariq-design`,
     `kvnk-html`) — maximum-fidelity delegation; review overlay is injected onto
     whatever static HTML it emits.

The artifact stays self-contained and openable from `file://` for archival/offline
reading; the **server and overlay exist only during a live review session** and
never touch the on-disk HTML.

## User Stories

1. As a reviewer, I want to select any text span (down to a word or letter) in the
   rendered plan and attach a comment, so feedback is precise instead of
   section-level.
2. As a reviewer, I want to draw a rectangle over a region of the rendered plan and
   comment on it, so I can focus the agent's attention on an area, not just text.
3. As a reviewer, I want each comment to be a small thread with a status
   (open → addressed → resolved) and a light category (change / question / nit),
   so I can track what the agent has handled.
4. As a reviewer, I want my annotations to **send directly from the page** to the
   agent over a live channel, so I never copy-paste into chat.
5. As a reviewer, I want the agent's edits to **re-render in place** so I watch the
   plan change as feedback is applied.
6. As a reviewer, I want the agent's follow-up questions to appear **in the page**
   and be answerable there, so a review round is a real two-way conversation.
7. As a reviewer, I want closing the browser to shut the server down and tell the
   agent the review is over, so there are no orphan processes and the agent knows
   the session ended.
8. As a reviewer, I want the server to live only while the session is up, so
   nothing keeps running after the session dies.
9. As a reviewer, I want my highlight/rectangle to survive a live re-render of the
   plan, so annotations are not lost when the doc updates under them.
10. As a plan author, I want to author a compact `plans/<slug>.md` and have it
    rendered for me, so I don't burn tokens hand-writing HTML.
11. As a plan author, I want the agent to apply feedback by editing the `.md` at the
    exact `data-source-line` an annotation points to, so edits are targeted.
12. As a plan author, I want `--save-tokens` to render through docforge and
    `--renderer=<skill>` to delegate to any design skill, with own-template as the
    default, so I choose look/fidelity per plan without changing how I author.
13. As a plan author, I want the on-disk `plans/<slug>.html` to stay clean
    (no overlay/server code), so the artifact remains archival and openable offline.
14. As a skill owner, I want the live-review overlay built **once, engine-agnostic**
    (injected by the server onto whatever HTML the renderer produced), so it works
    across own-template, docforge, and delegated skills without per-engine code.
15. As a skill owner, I want the overlay lifted from `Picanvas`'s vanilla
    `artifactOverlay.ts` (text capture, rectangle draw, selection handle, sticky
    comments, postMessage bridge), with the two anchor weaknesses upgraded, so I
    reuse proven code instead of reinventing it.
16. As a skill owner, I want the agent to "attend" a live session via a Monitor
    wait-loop that processes each Send/answer and exits on the close-signal, so the
    turn-based agent can drive a live surface without polling chat.

## Implementation Decisions

**Engine — markdown canonical.** `plans/<slug>.md` is the source of truth and the
only thing the agent edits. A render step produces `plans/<slug>.html`. This
**supersedes** v1's "single HTML is the source of truth, no `.md` companion."

**Renderer — flag-selected, default own-template.**
`--save-tokens` ≡ `--renderer=docforge`; `--renderer=<skill>` delegates to any
design skill; default is own-template (the v1 look, re-cast as a markdown
renderer). Token cost is low in all modes because the agent only emits the `.md`.

**Source mapping.** Every rendered block carries `data-block-id` (stable,
content-derived — docforge's `--stable-ids`; own-template emits equivalents) and
`data-source-line` → the markdown line. Delegated skills that emit neither degrade
to whole-doc quote search.

**Review transport — live WebSocket, session-bound.** A bun server (the skill
already uses bun + has native WS) serves the shell, holds the WS channel, and is
owned by the agent's attend-loop. Browser `beforeunload` → WS disconnect →
close-signal → server exits → attend-loop ends. Session process tree dies → server
dies. This **supersedes** v1's Out-of-Scope rejection of "a localhost annotation
server / plannotator-style auto-readback."

**Overlay attach — iframe-shell.** Server serves a parent shell; pristine rendered
plan loads in a same-origin iframe; the vanilla overlay is injected into the iframe
and bridged to the shell via `postMessage`; the toolbar, thread panel, and WS
client live in the parent. Live re-render reloads only the iframe. The on-disk
HTML never contains overlay/server code.

**Annotation model.**
```
annotation {
  id, kind: "span" | "rect",
  anchor,                       // span: {quote, prefix, suffix, blockId, sourceLine}
                                // rect: {coveredBlockIds[], sourceLines[], box?}
  category: "change" | "question" | "nit",
  status: "open" | "addressed" | "resolved",
  thread: [{ author: "user" | "agent", text, ts }]
}
```

**Anchor model.**
- **Span:** quote-based (W3C TextQuoteSelector — exact quote + short prefix/suffix
  + enclosing block's `data-source-line`). Re-binds after re-render by re-finding
  the quote within the block; marks "stale" (never silently lost) only if the
  quoted text itself changed. Upgrades Picanvas's offset-in-selector anchor.
- **Rect:** anchored to `sampleCoveredSelectors` → those elements' `data-block-id`
  / `data-source-line` (semantic), with the px box kept only as a visual.
  Upgrades Picanvas's raw page-px rect (which breaks on resize/re-render).

**Reuse — Picanvas `artifactOverlay.ts` (vanilla, zero deps).** Lift text capture
(`getSelection`/`Range`, `surroundContents` highlight + extract fallback), the
selection handle with PARENT/CHILD hierarchy nav, the rectangle SVG draw +
`sampleCoveredSelectors`, `buildSelector`, sticky-comment render, and the
postMessage protocol. Swap its two anchor strategies for the upgraded ones above.

**Agent attendance — Monitor wait-loop.** After starting the server in the
background, the agent enters a wait-until-signal loop for the whole session: each
Send / in-page answer writes a signal → agent reads it → edits the `.md` →
re-renders → server pushes the reload + reply live → status flips to `addressed` →
re-enter wait. The close-signal exits the loop ("review closed"). Honest constraint:
the *server* is live continuously; the *agent* acts per turn, so "live" is
instant from the reviewer's side and per-turn on the agent's.

**Strip v1's feedback layer.** Remove the section note inputs, checkboxes, the
fixed Copy-feedback/Reset toolbar, and the `serializeFeedback`/`stateKey`/
`resetState` script + their tests. Keep the prototype `showScreen`/`goBack` nav
(that's viewing, not feedback). The own-template renderer emits the plan from
markdown without any baked-in feedback affordances.

## Testing Decisions

External-behavior assertions only, headless (`bun test` + jsdom; a headless smoke
for the server protocol — no real browser). New seams:

1. **Quote-anchor rebind** — build a block, anchor a span by quote+prefix/suffix,
   mutate surrounding content, re-find: still binds; mutate the quoted text: marked
   `stale`, not lost.
2. **Rect coveredSelectors anchor** — given a box over known elements, assert the
   captured `coveredBlockIds`/`sourceLines`; after a re-render that reorders blocks,
   the rect re-binds to the same blocks.
3. **Annotation serialize** — the WS payload for span and rect annotations matches
   the documented shape; threads/status round-trip.
4. **md-edit mapping** — given an annotation's `sourceLine` + quote, the agent-side
   resolver finds the exact markdown location to edit.
5. **Server protocol / lifecycle** — connect → Send → ack; `beforeunload` →
   close-signal emitted; server exits; attend-loop sees the signal.

## Out of Scope

- Multi-user / concurrent reviewers on one session (single-client localhost only).
- Persisting annotations beyond the live session (no annotation DB; the `.md` edits
  are the durable record).
- Exposing the server beyond localhost / any auth (localhost, ephemeral port,
  single client).
- Screenshotting/rasterizing the rectangle region (overlay box + semantic anchor
  only; no html2canvas).
- Re-introducing the v1 copy-paste loop as a fallback (explicitly removed; the live
  server replaces it).
- Auto-firing the skill / retiring the hosted `visual-plan` (still deferred; v2
  stays manual-trigger).

## Supersedes v1 (reversed decisions, on the record)

| v1 decision | v2 |
|---|---|
| Single `.html` is the source of truth; no `.md` companion | `plans/<slug>.md` is canonical; `.html` is a disposable render artifact |
| Agent hand-fills an 800-line HTML template (token-heavy) | Agent authors compact markdown; a renderer emits HTML (token-light) |
| Section-level note + checkbox feedback | Arbitrary text-span + rectangle-region annotations |
| Copy-feedback → clipboard → paste anchored markdown | Live WebSocket direct-send; no copy-paste |
| Out of Scope: "localhost annotation server / plannotator-style auto-readback" | In scope: session-bound live review server is the core mechanism |
| Out of Scope: stateful prototype only; one-way feedback | Full in-page two-way conversation + live re-render |
| `serializeFeedback` / `stateKey` / `resetState` seams | Removed; replaced by quote/rect anchors + WS protocol seams |

## Further Notes

- The skill lives in `~/.claude/skills/local-visual-plan/`; this PRD and tests are
  tracked here per the local-markdown issue-tracker convention.
- v1 issues `01`–`04` remain as the shipped-v1 record; v2 work is issues `05`–`10`.
- Reference implementation to mine: `Picanvas/src/components/artifactOverlay.ts`
  (vanilla overlay), `artifactOverlay.ts:8–36` (data model),
  `:166–197` (text capture), `:199–287` (rectangle + `sampleCoveredSelectors`),
  `:486–516` (offset/selector utils). Engine reference: `docforge-v11`
  (`render --stable-ids`, `data-source-line`) and `editorial-report-v11/SKILL.md`.
- Design reference for the local-render fork: `lessons/0001-visual-plan-
  architecture-and-customization.html`, Path 2 fork (b) — compact `.md` + local
  render + re-render on feedback.

## v2.1 amendments — live-review refinements (issues 11–14)

A grilling pass on the shipped v2 review surface locked four refinements. They
reshape the review **UX** without changing the **engine** (markdown-canonical source,
renderer-as-flag, iframe-shell server all stand). Dependency: issue `11` is the spine;
`12`, `13`, `14` branch off it and are mutually parallel.

1. **Batch send, not auto-send (issue 11).** Committing an annotation no longer fires
   it over the WS. It parks in the sidebar as an **unsent draft** (editable,
   deletable). The reviewer sends per-card or **Send all (N)**. A send — one item or
   the batch — is one **round**: the attend-loop wakes once and processes every
   annotation in it together (one edit pass, one re-render). Unsent drafts survive a
   live re-render. *Supersedes v2's implicit per-commit auto-send.*

2. **Free-text comment label (issue 13).** The fixed `change / question / nit`
   category select is replaced by a **free-text label** typed per comment, shown bold
   on top of the card. The agent **infers** edit-vs-reply from the label + body and
   **states its read** in the thread before acting. *Supersedes v2's fixed category
   enum.*

3. **Per-round versioning (issue 12).** A round that produces ≥1 real artifact change
   cuts a new version `Vn`; a no-op / reply-only round does **not** bump. Each version
   is a **full snapshot** (`.md` + rendered `.html`); space optimization (base +
   deltas) is deferred. A **navbar switcher** lists `V1 · V2 · V3 …` (latest focused);
   clicking **views** a version read-only; **Restore forks** a new tip
   (non-destructive). The version boundary is the send-action / round from amendment 1.

4. **Element-pick tool (issue 14).** A third tool beside Select text / Draw region:
   **Pick element** — click an element, then `[` / `]` PARENT/CHILD walk the DOM with a
   breadcrumb, lifted **verbatim from Picanvas** (`artifactOverlay.ts`). The drill
   feature is Picanvas's, **not** Plannotator's (Plannotator only smart-resolves one
   element on pinpoint, no walk). Anchored **semantically** (`kind:"element"` →
   `data-block-id` + `data-source-line` + in-block selector + tag + snapshot), not via
   Picanvas's bare CSS selector, so it maps to the `.md` and survives re-render — same
   discipline as the v2 span / rect anchors.

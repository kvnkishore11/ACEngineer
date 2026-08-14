# STATUS: CHAPTER BUILT ✅ · VISUAL REVIEW PENDING

Lesson key: `ah-3-building-domain-specific-agents`  
Course/order: Agentic Horizon · global lesson 11 · Volume II chapter 3  
Chapter: `vol-2-ah/11-building-domain-specific-agents.html`  
Chapter CSS: `vol-2-ah/11-building-domain-specific-agents.assets.css`  
Built: 2026-07-13

## Gate and source discipline

- Extract gate passed: `_extracts/ah-3-building-domain-specific-agents/STATUS.md` exists and reports `DONE`.
- Consumed: `extract.md`, `extract.json`, `nuggets.md`, `outdated-vs-current.md`, `lab-spec.md`, `frame-plan.json`, and extract `STATUS.md`.
- Course repository used read-only for truth: `agentic-horizon/building-specialized-agents/` (also available at the lesson `codebase` symlink).
- No teaching claims were added beyond the extract/transcript-derived notes or shipped course files.
- Every lab command and file remains inside the course repository. Social Hype is optional because it uses a live stream and optional notification/TTS services.

## Deliverable metrics

| Metric | Result |
|---|---:|
| Visible chapter words (HTML tags/scripts removed) | 11,140 |
| Source words (`wc -w`, includes markup labels) | 12,519 |
| HTML lines | 1,434 |
| Chapter CSS lines | 354 |
| Top-level teaching sections | 14 |
| Complete ten-move idea cycles | 9 |
| Full-width native course frames | 12 / 12 unique (14 uses) |
| Retrieval items with `<details>` answers | 43 |
| Lab boxes | 9 |
| Current-practice YouTube overlays | 2 |
| Estimated print-equivalent pages | 41–49 |

Page estimate method: about 11k visible words at the gold chapter's print density, plus twelve large 16:9 teaching frames, eight systems/decision diagrams, code anatomy cards, nine lab boxes, mastery, and glossary. Exact pagination depends on the browser print engine.

## Pedagogy and UX coverage

- Every major idea contains Hook → Picture → Story/frame → Name → Worked example → You try → Fail/fix → Current Practice → retrieval `<details>` → Teach-back.
- Covers the eight-agent ladder, core four, one-off versus client runtime, sessions, custom tools/in-memory MCP, response observability, runtime-locked prompt values, governance hooks, extend versus overwrite, producer/consumer agents, and custom-agent decision discipline.
- Sticky desktop rail, duplicated mobile TOC, skip link, top/rail reading progress, active-section highlighting, reduced-motion-safe animation, semantic tables/details/glossary, and print rules are present.
- All frames are 1920×1080, displayed full width up to 1100px with `object-fit: contain`, readable captions, and exact frame-plan timestamps.
- The custom-agent decision framework and Ultra Stream chunk reader are designed HTML/code visuals, not invented screenshots.
- Body prose is 17px from `design/tokens.css`; surfaces use the existing light cream/off-white theme and high-contrast ink tokens.
- Offline-first: all required CSS and frame assets are local. YouTube links are optional outbound references; no CDN is required.

## Accuracy corrections incorporated

- The chapter leads with the SDK rename: `claude-agent-sdk` / `claude_agent_sdk` / `ClaudeAgentOptions`; frames showing `ClaudeCodeOptions` are labeled recording-era detail.
- Exact built-in tool counts are not treated as timeless. The lab asks learners to observe the installed SDK surface.
- Pinned model IDs are shown only when reading course code; the takeaway is task-to-model-class matching.
- QA Firecrawl setup documents the real `.mcp.json.firecrawl_6k.sample` rename and fallback behavior.
- Micro SDLC uses the shipped `specs/` and `reviews/` write lanes, correcting the older README's `plans/` wording.
- Ultra Stream uses the shipped frontend port 5175, not the older README's 5173.
- Ultra Stream context management is described precisely: bounded reads and an intended `clear_context`/outer-loop reconnect pattern. The chapter does not claim that the tool alone provably wipes all SDK context.
- Calc's restricted `eval()` and Ultra Stream's `shell=True`/`sed` reader are labeled teaching implementations that need production hardening.
- Hooks-cover-subagents is attributed to transcript/source claims; the shipped inline test is accurately described as a direct hook-function test, not an end-to-end Task integration test.

## Verification completed

- All 21 local chapter references resolve: shared CSS, chapter CSS, hub, previous chapter, and frame paths.
- All 12 unique frame files verified at 1920×1080.
- 27 HTML IDs found; zero duplicates.
- 29 fragment links found; zero missing targets.
- Nine idea cycles found; each contains all ten required moves in the correct order.
- 12 unique lesson frame paths found; all are used at teaching size.
- Inline JavaScript parses successfully with `new Function(...)` and uses guarded progress/IntersectionObserver setup.
- Chapter CSS braces balance; imported gold CSS path resolves.
- Two YouTube candidates independently verified against YouTube oEmbed metadata before linking:
  - `6fCqj4xFCZI` — *How Claude Code CHANGED Engineering Forever (and what's next)*
  - `X2ciJedw2vU` — *RAW Agentic Coding: ZERO to Agent SKILL*
- Hub updated concurrently with the completed AH-2 chapter: 10/18 complete, 55.6% global progress, 2/6 Agentic Horizon chapters, and lesson 11 linked as Done.
- `vol-2-ah/README.md` updated to link and mark lesson 11 complete.

## Open questions for Claude review

1. **Visual render:** the in-app browser runtime failed to start because its sandbox metadata was incomplete; the local headless Chrome fallback also produced no screenshot under this sandbox. A human/Claude browser pass should confirm the hero path, sticky rail, frame legibility, lab tables, mobile collapse, and print page breaks. Static DOM/CSS/path checks pass; this is the only release-quality review gap.
2. **Print pagination:** confirm the actual engine remains inside the 35–55 page target; current estimate is 41–49.
3. **Ultra Stream wording:** confirm the chapter's cautious distinction between `clear_context` intent and the shipped reconnect/resume mechanics is the preferred editorial treatment.
4. **Outbound videos:** both links are verified and extract-approved; confirm the book still wants direct YouTube links in this publication phase.

## Recommended Claude visual checklist

- Desktop 1440px: sticky rail does not collide with 1100px frames; captions remain directly beneath each image.
- Tablet ≤65rem: rail hides, mobile TOC appears, wide tables scroll, and figures stay contained.
- Phone 390px: agent path, context ledger, decision board, and producer/consumer diagram collapse without horizontal overflow.
- Print: frames stay contained, retrieval answers remain accessible, lab boxes avoid awkward splits, and total pagination stays within range.
- Contrast/type: cream/off-white surfaces retain warm near-black text, body remains 17px, and code blocks are readable in the terminal palette.

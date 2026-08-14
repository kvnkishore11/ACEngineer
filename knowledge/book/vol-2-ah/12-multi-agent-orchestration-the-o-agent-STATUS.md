# STATUS: CHAPTER BUILT ✅ · STATIC VERIFIED ✅ · VISUAL REVIEW PENDING

Lesson key: `ah-4-multi-agent-orchestration-the-o-agent`  
Course/order: Agentic Horizon · global lesson 12 · Volume II chapter 4  
Chapter: `vol-2-ah/12-multi-agent-orchestration-the-o-agent.html`  
Chapter CSS: `vol-2-ah/12-multi-agent-orchestration-the-o-agent.assets.css`  
Built: 2026-07-13

## Gate and source discipline

- Extract gate passed: `_extracts/ah-4-multi-agent-orchestration-the-o-agent/STATUS.md` exists and reports `DONE`.
- Consumed the full extract set: `STATUS.md`, `extract.md`, `extract.json`, `nuggets.md`, `outdated-vs-current.md`, `lab-spec.md`, and `frame-plan.json`.
- Course repository used read-only for truth: `agentic-horizon/multi-agent-orchestration/`, also available through the lesson `codebase` symlink.
- All lab tasks, source traces, prompts, commands, and produced artifacts remain inside the course repository.
- No generated hero image was added; the chapter uses the eleven supplied native frames plus HTML/CSS diagrams for the scale ladder, three pillars, architecture, and PITER.

## Deliverable metrics

| Metric | Result |
|---|---:|
| Visible chapter words (scripts/styles excluded) | 11,015 |
| HTML source words (`wc`-style) | 11,809 |
| HTML lines | 586 |
| Chapter CSS lines | 339 |
| Top-level teaching sections | 15 |
| Complete ten-move idea cycles | 11 |
| Required pedagogy moves | 110 / 110 |
| Native course frames | 11 / 11 unique, 13 teaching uses |
| Retrieval answers using `<details>` | 46 |
| Graded lab checkpoints | 7 · 100 points total |
| Published YouTube overlays | 0 (two candidates withheld; verification unavailable) |
| Estimated print-equivalent pages | 42–50 |

Page estimate method: approximately 11k visible words at the gold chapter's print density, thirteen large 16:9 frame placements, multiple full-width systems diagrams/tables, seven graded lab boxes, mastery rounds, and glossary. Exact pagination depends on the browser print engine.

## Pedagogy and UX coverage

- Every major idea contains Hook → Picture → Story/frame → Name → Worked example → You try → Fail/fix → Current Practice → retrieval `<details>` → Teach-back.
- Covers the five-rung scale framework; single-interface O-agent; three pillars; all eight management tools; observability pipeline; primary-versus-sub-agent lifecycle; core four + R&D; PITER; focused disposable agents; durable results and defensibility; ecosystem interoperability; prompt-driven sleep-check; plan/build/review; agentic-layer cost and missing pieces.
- Sticky desktop rail, mobile TOC, skip link, top/rail reading progress, active-section highlighting, semantic tables/details/glossary, responsive layouts, and print rules are present.
- Frames use the gold wide-breakout rule up to 1100px, `object-fit: contain`, exact timestamps, descriptive alt text, and explanatory captions.
- Body typography inherits the shared 17px light cream/off-white design tokens. No CDN, web font, remote script, or required network asset is used.
- Hub is updated to link lesson 12 and report 12/18 overall (66.7%) and 4/6 Agentic Horizon (66.7%).

## Course-code accuracy decisions

- SDK naming is already current here: `claude-agent-sdk`, `ClaudeAgentOptions`, and `ClaudeSDKClient`; no AH-3-style rename correction is applied.
- Model identifiers are treated as recording/repository detail; the durable teaching is task-to-model-class allocation.
- Backend/frontend ports use source truth: 9403 / 5175. The inner `CLAUDE.md` 8002 line is labeled stale.
- `modules/hooks.py` is labeled legacy/orphan; active hook surfaces are `command_agent_hooks.py` and `orchestrator_hooks.py`.
- The displayed 200k context denominator is labeled UI/reporting behavior, not a value supplied by this repository's `ClaudeAgentOptions`.
- The lab grades at least three create + three command calls rather than exactly six total calls, since model-driven orchestration may add list/status calls.
- The lab records a real implementation gap: template tools apply on creation, but the current command/resume path widens to the default allowlist. It does not call the resumed fast scout reliably read-only.
- `delete_agent` is taught as a soft archive (`archived = true`), not physical deletion. The non-partial unique name constraint means archived names remain reserved; lab agents use unique suffixes.
- Setup reflects actual env loading: migrations read root `.env`; the backend reads `apps/orchestrator_3_stream/.env`. Optional `.mcp.json.sample` setup is separated from core requirements.
- Verification uses `bun run build`, migration output, health, UI evidence, and workflow review. It does not invent an absent `type-check` script or require the unmanifested backend pytest path.
- Deterministic ADW integration, human decision gates, multi-codebase control, context forking, and prompt autocomplete remain explicitly labeled missing/future.

## Verification completed

- All 17 distinct local chapter references resolve: shared CSS, chapter CSS, hub, previous chapter, and frame files.
- All 11 frame files are present, nonempty, and verified at 1920×1080.
- 19 HTML IDs found; zero duplicates.
- 31 fragment links found; zero missing targets.
- Eleven idea cycles found; each has all ten required moves, and each Story move contains a real course frame.
- Eleven unique frames are used at teaching size; two are deliberately repeated where one frame supports a second major idea.
- Inline JavaScript parses with `node --check`; progress setup guards absent nodes and IntersectionObserver availability.
- Chapter CSS braces balance; chapter CSS inherits the gold layout and print tables remove their screen-only minimum width.
- Hub local references all resolve; progress arithmetic is correct.
- Two-axis review completed: the standards review found frame-width and print-table issues, both fixed; the spec review found omitted interop/judgment lab competencies, optional MCP setup, unverified video, and missing STATUS, all addressed.

## Verification not completed

- In-app browser initialization failed because the session lacked required sandbox metadata.
- A local headless-Chrome fallback did not emit a screenshot under this sandbox.
- Therefore desktop/mobile/print rendering is not claimed as visually approved; static DOM, CSS, path, dimension, and script checks pass.

## Open questions for Claude review

1. **Visual render:** confirm at 1440px that the sticky rail does not collide with the wide frame breakout, all frame text is readable, and the seven lab boxes scan cleanly. At ≤832px, confirm the rail disappears, mobile TOC appears, diagrams collapse, and no table causes viewport overflow.
2. **Print pagination:** print to PDF and confirm the chapter remains inside the 35–55-page target; current estimate is 42–50. Confirm the tool/template tables wrap rather than clip on portrait pages.
3. **Repo-truth corrections:** confirm editorial preference for surfacing the two code-audit gaps (resumed tool widening and soft-archive/name reservation) even though the supplied extract presents the cleaner conceptual model.
4. **Video overlays:** two extract-approved candidates were withheld because `yt-dlp` was unavailable and the web fallback could not verify both current titles. Confirm whether zero overlays is preferred to publishing an unverified outbound link.
5. **Lab duration:** confirm the restored `/question` + `/prime` interop and three-vs-three judgment/PITER exercises still fit the 120–180 minute advanced-lab envelope.

## Recommended Claude visual checklist

- Desktop 1440×1000: hero ladder, sticky rail, capability palette frame, three-pillar cards, PITER diagram, tool table, lab rubric, glossary.
- Mobile 390×844: skip link, site bar, mobile TOC, single-column ladders/cards, full-width contained frames, code scrolling, table scrolling.
- Print preview: page breaks around frames/diagrams/lab boxes, table wrapping, no sticky UI, page estimate.
- Interaction: scroll progress reaches 100%, active rail section changes, retrieval details open, hub link and previous-chapter link resolve.

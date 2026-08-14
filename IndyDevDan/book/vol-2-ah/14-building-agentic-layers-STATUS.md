# STATUS: COMPLETE — Claude review requested

**Lesson key:** `ah-6-building-agentic-layers`  
**Chapter:** `vol-2-ah/14-building-agentic-layers.html`  
**Assets:** `vol-2-ah/14-building-agentic-layers.assets.css`  
**Built:** 2026-07-13

## Outcome

AH-6 is authored as the 14-lesson capstone: a light, offline-first teaching chapter that turns the earlier tactics into one maturity model for the agentic layer. The chapter consumes the completed extract, uses all 13 native lesson frames at teaching width, implements seven full pedagogy cycles, includes the six-part course-codebase capstone lab, and closes with cumulative retrieval, teach-back, and a glossary.

The book hub now links AH-6 and reflects **14 of 18 chapters (77.8%)** overall and **6 of 6 Agentic Horizon chapters (100%)**.

## Measured density

- HTML source: **1,255 lines**, **11,167 whitespace-delimited source words**.
- Visible teaching text after removing markup/script: **~9,885 words**.
- Teaching structures: **314 prose paragraphs**, **6 tables**, **7 lab boxes**, **41 retrieval `<details>` items**.
- Visual structures: **13 course frames**, plus HTML/CSS system maps for the two-layer model, ladder, Class jumps, ADW flow, orchestrator bridge, specialization, Core Four, course arc, tactic strip, evidence, and scoring.
- Estimated print-equivalent length: **~38–44 pages**. Estimate combines ~26 pages of visible text at 375 words/page with 13 large figures and the space consumed by diagrams, tables, labs, retrieval blocks, and callouts.

## Pedagogy coverage

Each of the seven major ideas contains:

1. Hook / concrete failure
2. Picture / system map
3. Story grounded in lesson frames or verified code
4. Name / precise term
5. Worked course-codebase example
6. You try
7. Common fail + fix
8. Current Practice overlay
9. Retrieval in `<details>`
10. Teach-back with pass criteria

Major ideas:

- The application layer vs agentic layer
- Codebase singularity as an evidence-bearing threshold
- Class 1 Grades 1–7
- Class 2 out-loop fabric and ADWs
- Class 3 orchestrator and the ADW bridge
- Specialize, do not genericize
- Everything reduces to the Core Four

## Accuracy anchors preserved

- **10 orchestrator tools**, not 8: eight agent-management tools plus `start_adw` and `check_adw`.
- **7 database tables**, with migration 9 adding `ai_developer_workflows`.
- Canonical backend port **9403**; frontend **5175**. The stale 8002 note is called out only as a failure repair.
- Orchestrator default in this code snapshot: `claude-opus-4-5-20251101`; presented as dated implementation detail, not current-model guidance.
- No literal `start adw:` host parser: the orchestrator emits a typed `start_adw` tool call.
- The class/grade diagrams are identified as idealized teaching structures; real repo consolidation is explicit (`plan.md` task-type templates; CLI/`start_adw` out-loop entry).
- `expertise.yaml` is consistently described as a mental model validated against code, not a source of truth.
- ADW trace matches the code: `TOTAL_STEPS = 2`; `/plan` then `/build`; logging hooks/handlers; detached `uv run adw_<type>.py --adw-id <uuid>` process.

## Verification completed

- Extract gate: `_extracts/ah-6-building-agentic-layers/STATUS.md` exists and reports DONE.
- All local chapter `href`/`src` paths resolve from `vol-2-ah/`.
- CSS imports resolve: tokens + base + components in HTML, and the gold TAC-1 layout grammar through the AH-6 asset stylesheet.
- All 13 files in the lesson frame plan are referenced exactly once in the chapter.
- Every referenced frame is present and confirmed **1920×1080**.
- 13 images have 13 non-empty alt texts and 13 timestamped captions.
- No duplicate IDs; all sticky-nav hash targets exist.
- `<details>` / `<summary>` counts balance at 41/41; `<section>` tags balance; CSS braces balance.
- No unescaped ampersands in HTML.
- Lab evidence paths were checked against the canonical `agentic-horizon/orchestrator-agent-with-adws` tree.
- Seven table-creating migrations were confirmed from source.
- Hub contains the new chapter link in the featured chapter and AH lesson list.

## Verification limitations / open questions for Claude review

1. **Live browser render:** the in-app browser could not initialize because its session metadata lacked the required sandbox policy, and local Chrome/Quick Look rendering was also blocked by the managed sandbox. Static DOM, CSS, asset, accessibility, and path checks passed, but Claude should perform a visual pass at approximately 1440px and 390px widths. Pay particular attention to the imported gold layout, Class-flow grids, wide tables, frame clarity, sticky rail, and mobile stacking.
2. **Runtime lab:** the lab was not executed end to end because it requires a user-provided Anthropic key, Postgres connection, token spend, and local service processes. Every command and course-code path was verified statically. Claude should decide whether the already-present markdown-preview features warrant substituting fresh lab prompts before publication.
3. **Current-practice YouTube:** the extract proposed `fop_yxV-mPo` as a companion but required verification. The YouTube backend was unavailable and the read-only web fallback had no network resolution. The chapter intentionally publishes **0 YouTube overlays** rather than an unverified link. Claude can verify and add at most the phase-1-approved companion later.
4. **Density:** the chapter is ~9.9k visible words rather than the gold chapter's ~13k, but the 13 large frames and numerous diagrams/tables place it inside the requested 35–55 print-equivalent-page band. Claude should confirm that this is sufficiently dense without adding transcript-shaped padding.

## Files changed

- `vol-2-ah/14-building-agentic-layers.html` — new chapter
- `vol-2-ah/14-building-agentic-layers.assets.css` — new capstone visuals and responsive/print rules
- `vol-2-ah/14-building-agentic-layers-STATUS.md` — this review handoff
- `index.html` — AH-6 feature/link and progress update

## Review recommendation

Approve after one desktop/mobile visual pass and a judgment on the two publication-time items: whether to refresh the lab task prompts against the current captured repo state, and whether to add the single verified YouTube companion. No technical-content blocker remains in the authored chapter.

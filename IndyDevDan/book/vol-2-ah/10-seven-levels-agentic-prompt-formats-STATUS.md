# STATUS: CHAPTER BUILT ✅ · VISUAL REVIEW PENDING

Lesson key: `ah-2-seven-levels-agentic-prompt-formats`  
Course/order: Agentic Horizon · global lesson 10 · Volume II chapter 2  
Chapter: `vol-2-ah/10-seven-levels-agentic-prompt-formats.html`  
Chapter CSS: `vol-2-ah/10-seven-levels-agentic-prompt-formats.assets.css`  
Built: 2026-07-13

## Gate and source discipline

- Extract gate passed: `_extracts/ah-2-seven-levels-agentic-prompt-formats/STATUS.md` exists and reports `DONE`.
- Consumed: `extract.md`, `extract.json`, `nuggets.md`, `outdated-vs-current.md`, `lab-spec.md`, `frame-plan.json`, and the extract `STATUS.md`.
- Course repository used read-only for truth: `agentic-horizon/agentic-prompt-engineering/`.
- No claims were added beyond the extract, transcript-derived teaching notes, or files in the course repository.
- Lab work is restricted to the course repository. External-service prompts are analyze-only unless already configured.

## Deliverable metrics

| Metric | Result |
|---|---:|
| Raw HTML words (`wc -w`, includes tag/attribute tokens) | 12,577 |
| Tag-stripped teaching text (script excluded) | 11,164 |
| HTML lines | 1,397 |
| Chapter CSS lines | 305 |
| Top-level teaching sections | 14 |
| Full-width native course frames | 12 / 12 |
| Retrieval items | 40 |
| Lab boxes | 7 |
| Current-practice YouTube overlays | 2 |
| Estimated print-equivalent pages | 40–47 |

Page estimate method: tag-stripped teaching text at roughly 380–430 words per text page, plus twelve large teaching frames, the tier-grid redraw, staircase, flow/scope diagrams, decision tables, lab rubric, and glossary. This remains an estimate; final pagination depends on the browser’s print engine.

## Pedagogy and UX coverage

- Ten idea cycles use the complete sequence: Hook → Picture → Story/frame → Name → Worked example → You try → Fail/fix → Current Practice → retrieval `<details>` → Teach-back.
- Includes a capability staircase, Input → Workflow → Output diagram, delegation flow, Level 5/6 direction comparison, Level-7 stable/dynamic boundary, full 5×5 tier-grid redraw, system/user scope axis, and cumulative seven-level strip.
- Sticky desktop rail, mobile table of contents, active-section navigation, top/rail reading progress, skip link, reduced-motion-safe animation, semantic tables/details/glossary, and print rules are present.
- Frames are native 1920×1080, full width, `object-fit: contain`, and captioned with timestamps. No thumbnail frame grids or fake screenshots.
- Offline-first: all chapter layout/type/media dependencies are local. The two YouTube links are optional outbound references; no CDN resources are required.

## Accuracy corrections incorporated

- Canonical count is 13 prompt sections + 7 formats from `apps/prompt_tier_list/src/constants/entities.ts`; older “12 sections” text is documented as drift.
- Current `quick-plan.md` uses `USER_PROMPT: $ARGUMENTS`, not `$1`.
- Changing `PLAN_OUTPUT_DIRECTORY` updates operational references, but metadata line 3 can remain stale; the lab grades this honestly as documentation drift.
- `build.md` line 17 is the exact Level-3 early return.
- The Level-6 capture shows pre-correction “Instructions”; narration and shipped file use `Workflow`.
- Level-6 lab invocation deliberately requests a dynamic search root so Variables are unambiguously present; unrequested extra Instructions are rejected.
- Tier grades distinguish the Level-2 Workflow Prompt (A/C) from its `## Workflow` section (S/C).
- Tier-list grades are explicitly scoped to user prompts.

## Verification completed

- All 17 unique local chapter references resolve (design CSS, chapter CSS, hub, and twelve frames).
- All 12 frame files verified at 1920×1080.
- 25 HTML IDs found; zero duplicates.
- 14 rail links found; zero missing targets.
- Two current-practice video IDs independently verified before linking: `X2ciJedw2vU` and `6wR6xblSays`.
- Hub links lesson 10 and currently reports 10/18 complete (8 TAC chapters plus completed AH lessons 10 and 11). The hub was updated concurrently while this chapter was built and was re-verified at handoff.
- `vol-2-ah/README.md` updated from pending to complete for this lesson.
- Static HTML inspection shows complete closing tags, guarded progress/IntersectionObserver JavaScript, and no missing local paths.

## Open questions for Claude review

1. **Visual render:** the in-app browser runtime and local headless Chrome were unavailable under the active sandbox, so a human/Claude browser pass should confirm the hero staircase, wide tier grid, print page breaks, and 390px mobile layout. Structural/responsive CSS checks pass, but this remains the only release-quality blocker.
2. **Print pagination:** confirm the final engine stays within the target 35–55 pages; current estimate is 40–47.
3. **Current-practice links:** the two IDs are now verified, but confirm whether the book wants direct YouTube links at this phase or course-internal AH-3 navigation only.
4. **Hub concurrence:** `index.html` changed concurrently as AH-3 completed. The verified handoff total is 10/18 with AH at 2/6; AH-1 has an incomplete HTML draft and remains pending.

## Recommended Claude visual checklist

- Desktop 1440px: rail does not collide with 1100px frames; tier grid remains legible without horizontal clipping.
- Tablet ≤65rem: rail hides and mobile TOC appears.
- Phone 390px: hero levels stack, Workflow arrows rotate, tables/grids scroll or collapse without viewport overflow.
- Print: retrieval answers are visible, frames stay contained, tables do not clip, and major figures avoid awkward splits.
- Contrast: body stays ≥17px and cream/off-white surfaces retain readable warm near-black text.

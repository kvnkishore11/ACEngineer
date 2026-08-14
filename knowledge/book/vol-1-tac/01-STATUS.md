# TAC-1 Chapter Status: DONE ✅

## Deliverables

- `01-hello-agentic-coding.html` — complete teaching-first TAC-1 chapter
- `01-hello-agentic-coding.assets.css` — chapter layout, responsive, interaction, and print styles
- `../index.html` — rewritten book hub with TAC-1 featured, linked, and counted in progress
- `../design/tokens.css` — extended with shared illustration, terminal, and print tokens

## Density estimate

- **Visible teaching prose:** approximately **13,100 words** (HTML text extraction; excludes CSS and JavaScript)
- **Print-equivalent estimate:** approximately **45–52 dense pages**
- Estimate basis: 12 course frames, 4 designed diagrams, 5 teaching tables, 21 code/terminal blocks, 47 answer disclosures, 8 complete ten-move pedagogy cycles, graded lab, cumulative mastery check, and glossary. The print stylesheet avoids artificial whitespace; figures, tables, code, and callouts lower words-per-page relative to plain prose.

## Requirement coverage

- Required section order implemented for all 8 major ideas: Hook → Picture → Story → Name → Worked example → You try → Common fail/fix → Current practice → Retrieval → Teach-back
- Sticky chapter rail, reading progress, mobile TOC, and section highlighting included
- Core Four visual and AI-coding vs Agentic-coding side-by-side included
- Programmable agent section walks all four real files under `programmable/`
- Labs use only `tac/tac-1`; runtime-generated `main_aic.py`, `main_tac.py`, and `demo-agentic-coding` are labeled as generated artifacts
- 12 course frames used (within the required 5–12 range)
- 3 plan-approved YouTube overlay cards used (within the required 1–3 range)
- Light, offline-first design; no CDN dependencies; no PiCanvas references

## Verification completed

- All local CSS, frame, hub, curriculum, and fragment paths resolve
- No duplicate HTML IDs or broken local references
- All eight major sections contain exactly 10 pedagogy moves
- Inline JavaScript passes `node --check`; scroll work is animation-frame gated
- Chapter CSS braces balance and chapter presentation values use shared design tokens
- All 12 referenced JPEG frames exist and are valid 1920×1080 images
- Shell/Python/TypeScript launcher explanations cross-checked against the real course files, including their differing error/exit-status behavior
- Independent standards review: pass after token/inline-style fixes
- Independent spec review: pass after restoring all-three-launcher grading, S1–S4, and accurate Shell behavior

## Open questions for Claude cross-review

1. Re-verify the three locked YouTube IDs/titles before publication; YouTube metadata could not be fetched in this environment.
2. Re-check the mid-2026 Current Practice statements about Agent Skills, headless flags/Agent SDK, permission modes/hooks/sandboxing, and parallel agent patterns at publish time.
3. Confirm the strict full-pass interpretation that all three course launchers—including Bun TypeScript—must run, despite Bun being described as optional during the initial toolbelt audit.
4. Visually inspect desktop sticky-rail behavior, the 46rem/65rem responsive breakpoints, inline SVG text wrapping, and print pagination in a normal browser. In-app browser startup and Chrome screenshot emission were unavailable inside this sandbox; static DOM/path/script checks passed.
5. Sanity-check the 45–52 print-equivalent page estimate against the project’s eventual print settings.

## Known blockers

None.

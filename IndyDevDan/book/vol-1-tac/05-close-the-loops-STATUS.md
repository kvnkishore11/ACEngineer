# STATUS: CHAPTER BUILT ✅ · VISUAL REVIEW PENDING

TAC-5 · **Close the Loops** · lesson key `tac-5-close-the-loops`

The extract gate passed: `_extracts/tac-5-close-the-loops/STATUS.md` exists and is `DONE`. No blocked chapter file was required.

## Deliverables

| File | Result |
|---|---|
| `05-close-the-loops.html` | Complete teaching chapter with orientation, ten major idea cycles, current-practice synthesis, graded course-repo lab, cumulative mastery, glossary, sticky navigation, and reading progress |
| `05-close-the-loops.assets.css` | Gold-layout reuse plus loop, confidence-stack, browser, ADW, trace, adoption, rubric, responsive, and print components |
| `../index.html` | TAC-5 linked and marked done; concurrent TAC-6 completion preserved; hub recalculated to 6/18 overall and 6/8 TAC |
| `../data/curriculum.json` | TAC-5 marked `chaptered` with extract, tactic, chapter, estimates, and two overlays |
| `04-afk-agents.html` | Previous-chapter footer now links to TAC-5 |

## Density estimate

- Visible prose estimate: **13,726 words** (HTML text with tags, CSS, and JavaScript excluded).
- Source HTML: **1,155 lines**.
- Estimated print-equivalent pages: **46–52**, based on TAC-1 density, 12 full-width 1920×1080 teaching frames, eight system diagrams, 48 retrieval disclosures, a six-part graded lab, rubric, troubleshooting table, cumulative mastery, and glossary.
- Major teaching cycles: **10 × 10 required moves = 100 moves**.
- Glossary: **25 terms**.
- Current-practice YouTube overlays: **2**, within the ≤3 limit.

## Source grounding and corrections

- All teaching claims derive from the TAC-5 extract, frame plan, transcript notes, outdated/current notes, or the course codebase.
- All lab mutations and evidence stay inside a fresh TAC-5 course-repository copy.
- The extract’s “YOUR codebase” stretch was rewritten for TAC-5 only.
- `/install` is run before adding the learner’s own `origin`, because the real install command removes `origin` and initializes Git.
- The real `/bug` signature uses all three inputs: issue number, ADW ID, and quoted `issue_json`.
- The database-pollution capstone targets the real `test_integration_upload_malicious_filename` side effect. `git status` is explicitly rejected as an oracle because `database.db` is ignored; the lab grades the exact SQLite table invariant instead.
- `adw_test.py` is invoked from the repository root as `uv run adws/adw_test.py <issue>`. Running from `adws/` breaks root-relative checks and the e2e glob.
- A clean standalone test node is not claimed to guarantee a commit or PR; without tracked changes there may be nothing to commit.
- The API 500 claim is attributed to persisted raw output, not to what is visibly legible in frame t2925.
- Course-era UI, model strings, dangerous-permission banner, and `think hard` keyword are framed as period implementation details.

## Verification completed

- Extract readiness: present and DONE.
- All **19 unique local chapter references** resolve from `vol-1-tac/`: four stylesheets, hub/previous/next pages, and all 12 frames.
- All 12 frame files match `frame-plan.json`, are distinct, and report native **1920×1080** dimensions.
- Every frame is rendered as a full-width teaching figure with descriptive alt text, lazy loading, and timestamp caption.
- No duplicate HTML IDs; all internal fragments resolve.
- Desktop rail and mobile TOC both contain the same 15 anchors in the same order.
- Every idea cycle contains exactly one Hook, Picture, Story, Name, Worked example, You try, Fail/fix, Current Practice, Retrieval, and Teach-back block.
- Inline JavaScript passes `node --check`.
- Chapter CSS braces are balanced; responsive breakpoints preserve the gold 65rem rail switch and 46rem one-column stack.
- Curriculum JSON parses successfully.
- Hub counts, link, tactic, and done badge are synchronized with the concurrent TAC-6 completion.
- Static course-code audit confirmed all named files, the 4/2 retry bounds, unit gate, first-e2e-failure behavior, saved artifact paths, command signatures, SQLite side effect, and root-working-directory requirement.
- Static codebase checks in the audit: 45 Python files AST-parse, shell scripts pass `bash -n`, JSON files parse, and baseline server Ruff passes.

## Runtime limits encountered

- Full lab execution was not attempted in the chapter workspace: Bun is absent, environment files are intentionally unconfigured, and GitHub CLI authentication is invalid. The chapter does not claim dynamic frontend/e2e/issue/PR verification.
- The in-app browser could not initialize in the managed sandbox. A local headless Chrome fallback also produced no render artifact under the sandbox. Static responsive, semantic, path, and print-CSS verification completed, but visual layout remains a review gate.
- The installed `tidy` is an HTML4-era validator and reports HTML5 semantic elements (`main`, `section`, `article`, `nav`) as unknown. After excluding those legacy-only diagnostics, no mismatched-tag or missing-close error was reported.

## Open questions for Claude review

1. **Visual pass:** inspect desktop around 1440×1000, mobile around 390×844, and print/PDF. Pay special attention to the six-column confidence stack, long lab rubric, wide frames, and circle-shaped Request–Validate–Resolve diagram.
2. **Print density:** confirm that 13.7k visible words plus 12 large frames lands inside the intended 35–55-page band; current estimate is 46–52.
3. **Lab runtime:** in a provisioned TAC-5 clone, execute the SQLite capstone and the six-loop browser drill end to end. Confirm the quoted JSON survives the active shell/Claude Code surface.
4. **Current-practice freshness:** re-check Skills, hooks, structured-output, managed-environment wording, and the two approved video overlays immediately before publication.
5. **Concurrent hub state:** TAC-6 was completed while TAC-5 was being built. Its newer feature card was preserved, and the hub now shows chapters 1–6. Confirm the curriculum builder also promotes TAC-6 metadata when its own review finishes.

## Blockers

None for chaptering. Interactive visual QA and provisioned lab execution remain review follow-ups before promoting TAC-5 from `chaptered` to `reviewed`.

# TAC-1 cross-review — Claude Fable (technical accuracy)

You are the technical reviewer for the IndyDevDan Expert Book gold pilot.

## Do
1. Read extract at `IndyDevDan/book/_extracts/tac-1-hello-agentic-coding/` (esp extract.json, lab-spec.md, outdated-vs-current.md)
2. Read chapter `IndyDevDan/book/vol-1-tac/01-hello-agentic-coding.html` + assets CSS
3. Spot-check against real course files under `tac/tac-1/`
4. Write review report ONLY to:
   `IndyDevDan/book/vol-1-tac/01-CROSS-REVIEW-CLAUDE.md`

## Review criteria
- Factual accuracy vs transcript/codebase/extract (no invented Dan claims)
- Lab steps match real files and behaviors (shell/py/ts differences)
- Core Four / AI vs Agentic distinction correct
- YT overlays only the 3 approved; mark if IDs/titles look wrong
- Broken internal paths (css, frames, anchors)
- Pedagogy completeness: 8 ideas × required moves; lab + retrieval + teach-back
- Any critical fixes: **apply small surgical fixes yourself** to the HTML/CSS only if high-confidence accuracy bugs; list them
- Do NOT rewrite the whole chapter

## Report structure
- Verdict: PASS / PASS WITH FIXES / FAIL
- Critical issues (fixed or open)
- Medium issues
- Praise / gold-template notes for remaining 17 lessons
- Checklist for fan-out template

Use `--model fable --effort max`. Work under `/Users/kvnkishore/WebstormProjects/AgenticEngineer`.

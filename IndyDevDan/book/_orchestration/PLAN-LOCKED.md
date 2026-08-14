# IndyDevDan Expert Book — locked plan (Hermes orchestrates only)

## Goal
Become expert at IndyDevDan’s system: operate + teach-back + graded drills. HTML multi-volume site ~800–1000 pages (dense).

## Corpus Phase 1
- TAC 1–8 + AH 1–6 + MA 1–4 (local catalog)
- YT overlays last ~10 months: strict map-to-lesson / named-gap, 1–3 per lesson
- Phase 2: non-course YT later
- Phase 3: PAIC when access arrives

## Structure
Course-spine volumes + Current Practice YT overlays per lesson.
- Vol I TAC, Vol II AH, Vol III MA + synthesis
- Teaching model: Hook → Picture → Worked example → Name → Fail → Retrieval → Lab → Teach-back → Overlay

## Deliverable location
`/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/`

## Labs
Course codebases only (not PiCanvas).

## Workers
- Claude Fable 5 (`--model fable` / `claude-fable-5`, `--effort max`): technical extract, codebase, accuracy, outdated flags
- Codex GPT 5.6 sol xhigh: teaching prose, weak-learner structure, HTML/UI craft
- Cross-review each other; stitch agent merges
- Hermes: prompts, dispatch, verify only — no book body by Hermes

## Build order
1. TAC-1 gold pilot extract (Claude) → gold chapter HTML (GPT) → cross-review + stitch
2. Fan-out remaining 17 with same template

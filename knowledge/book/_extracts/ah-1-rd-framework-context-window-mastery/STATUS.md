# STATUS: DONE ✅

AH-1 "Elite Context Engineering" (the R&D Framework) extract — completed by Claude Fable (technical-accuracy pass).
Lesson #9 · Intermediate · course AH · order 9 · video 73:20 (1920×1080 @ 15fps). Framework: **R&D — Reduce & Delegate**, 12 techniques across 4 levels (Beginner / Intermediate / Advanced / Agentic).

## Files in this extract

| File | Purpose | Status |
|---|---|---|
| `extract.json` | Machine schema — tactic, mission, R&D framework, four levels, core_concepts, **twelve_techniques** (level + R/D + codebase mapping + Dan quote + misconception + timestamp + frame each), future_trends, step_by_step_demo, quotes, retrieval, lab, codebase_map, current_practice_gaps, yt_overlay_candidates, frame_plan, confidence_notes | ✅ valid JSON (53 files mapped, 12 techniques, 23 quotes, 14 retrieval Qs) |
| `extract.md` | Master teaching notes — framework + 13 ideas (12 techniques grouped by level, + future), each Hook → Picture → Worked example → Dan's term → Failure → Retrieval; VTT-verified timeline; glossary; curriculum bridge | ✅ |
| `nuggets.md` | 20 ranked nuggets in 3 tiers for weak learners (folds in the 18 loot-box notes) + 8-question micro-quiz | ✅ |
| `outdated-vs-current.md` | 6 course-era→mid-2026 gaps with book treatments; what hasn't aged; strict phase-1 overlay decision (topic-mapped, IDs flagged for sourcing) | ✅ |
| `frame-plan.json` | 12 extracted frames + 2 diagram_instead beats; VTT anchors, verified_visual, why_for_weak_student, unframed-beats rationale | ✅ valid JSON, all 12 files on disk |
| `lab-spec.md` | 5-part lab (all 12 techniques), course codebase only; Checkpoints 0–4, S1–S5 stretch, pass criteria, instructor notes | ✅ |
| `STATUS.md` | this file | ✅ |

## Frames (media/frames/ah-1-rd-framework-context-window-mastery/)

12 full-resolution 1920×1080 JPEGs (ffmpeg `-q:v 2`), one anchor per framework beat + technique level, all visually verified this session:

| # | File | Technique | t |
|---|---|---|---|
| 1 | t0176-rd-reduce-and-delegate.jpg | R&D framework title | 2:56 |
| 2 | t0266-context-measure-before.jpg | T1 Measure (before state: 63k/31%, MCP 24.1k, memory 23.7k, warning, token counter) | 4:26 |
| 3 | t0505-mcp-strict-config-tree.jpg | T2 Avoid MCP (firecrawl-only, MCP→6.5k) + repo tree | 8:25 |
| 4 | t0786-context-after-prime.jpg | T3 Prime > CLAUDE.md (after: memory 0.2%, 92% free) | 13:06 |
| 5 | t1085-output-styles-done.jpg | T4 Output tokens ("Done." + /output-style menu) | 18:05 |
| 6 | t1492-subagent-docs-scrapers.jpg | T5 Sub-agents (load_ai_docs launching docs-scraper) | 24:52 |
| 7 | t1790-planner-builder-split.jpg | T6 Architect/Editor (planner + /build split) | 29:50 |
| 8 | t2050-avoid-compact.jpg | T7 Avoid /compact (builder report + Compacting) | 34:10 |
| 9 | t2345-context-bundle-jsonl.jpg | T8 Context bundles (JSONL trail + dedup replay) | 39:05 |
| 10 | t2705-append-system-prompt.jpg | T10 System prompt (append-system-prompt read-100 + ✅/❌) | 45:05 |
| 11 | t3195-background-primary-delegation.jpg | T11 Primary delegation (background report + rename) | 53:15 |
| 12 | t3485-agent-experts-triad.jpg | T12 Agent experts (plan/build/improve triad) | 58:05 |

Diagram_instead (no frame; render as designed diagrams): T9 "one agent, one purpose" (agent-pipeline/ADW diagram) and the future-trends recap (five-card future diagram).

## Verification performed

- `extract.json` and `frame-plan.json` both parse via `python3 json.load`.
- **Codebase coverage 100%:** `codebase_map` maps all **53** real files under the elite-context-engineering symlink (verified with `find -L`; the only additions over the 51 taught files are the two auto-generated `bun.lock` lockfiles, noted as not-taught). No mapped file is missing from disk.
- **Frames:** all 12 frame-plan `file` entries exist on disk at 1920×1080; no extra/missing files; the 2 diagram_instead entries correctly carry `file: null`.
- **Quotes/timestamps** cross-checked against the 3,430-cue VTT (parser in /tmp/vtt_search.py); key numbers read directly off the extracted frames (63k/31% boot; MCP 24.1k→6.5k; memory 23.7k→358/0.2%; README 2,650; models claude-opus-4-1-20250805 / claude-sonnet-4-20250514).
- **README claim** verified: 12 techniques enumerated with Level + Framework tags; CLAUDE.large.md is 2,978 lines; settings.json wires the two hooks across 8 events; bundle/log paths confirmed in the hook sources.
- **YT overlays:** AH-1 had **no seed list** (`data/curriculum.json` overlays: []). Per the no-fabrication rule, phase-1 candidates are topic-mapped with `video_id: null` + `needs_id_sourcing: true`; capped at 3.

## Blockers

None.

## Caveats / open questions for the next stage (Codex chapter build + Claude cross-review)

1. **YouTube overlay IDs must be sourced + oembed-verified** at chapter build/review (three phase-1 topics named: context engineering; sub-agents/delegation; hooks/Skills/Agent SDK). Do not publish overlay links until IDs resolve to the right IndyDevDan videos. No IDs were fabricated here.
2. **Course-era model ids are period detail.** `quick-plan.md` pins `claude-opus-4-1-20250805`; /context shows opus-4-1 / sonnet-4. Update to current models when adapting the codebase; the techniques are model-agnostic (Dan says so on camera).
3. **On-camera repo state ≠ shipped repo:** the video tree shows `.mcp.json.all_22k` / `.firecrawl_4k` / `.empty`; the repo ships `.mcp.json.all_16k.sample` / `.firecrawl_7k.sample` / `.sample`. Teach from the shipped filenames; footnote the on-screen names/counts as record-time detail.
4. **Two beats are diagram_instead** (T9 "one agent, one purpose" and the future-trends recap) — the chapter should render designed diagrams (an ADW pipeline; a five-card future) rather than screenshots.
5. **current_practice_gaps** written against mid-2026 Claude Code (Agent Skills, Agent SDK, headless flags, plugins, improved compaction); re-verify at publish — this axis moves fast.
6. **Loot box** = 18 notes per course-notes.md; nuggets.md folds and ranks them but the count reflects capture time and may have changed on agenticengineer.com.

## Out of scope (untouched, per brief)

- Full chapter HTML (`vol-2-ah/09-rd-framework-context-window-mastery.html`) — Codex builds it next from this extract.
- PiCanvas; downloading full YouTube videos.
- No course source trees were modified (read-only); all writes are under `book/_extracts/…` and `book/media/frames/…`.

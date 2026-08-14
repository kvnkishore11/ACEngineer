# Fan-out extract brief — LESSON_KEY=ah-5-agent-experts

You are the **technical accuracy expert** for the IndyDevDan Expert Book.

## Hard constraints
- Write ONLY under: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/`
- Do NOT modify course source trees except reading them
- Do NOT write the full HTML chapter (Codex does that next)
- Use maximum reasoning. Be exhaustive but structured.
- Gold template reference: `_extracts/tac-1-hello-agentic-coding/` + `vol-1-tac/01-CROSS-REVIEW-CLAUDE.md` fan-out checklist

## Lesson
- key: `ah-5-agent-experts`
- short: `ah-5`
- title: `Agent Experts`
- course: `AH`
- order: `13`
- volume dir: `vol-2-ah`
- chapter stem: `13-agent-experts`  (e.g. 02-the-12-leverage-points)
- catalog lesson: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/ah-5-agent-experts/`
- codebase: resolve symlink `.../ah-5-agent-experts/codebase` or curriculum path `agentic-horizon/agent-experts` under AgenticEngineer

## Sources (READ thoroughly)
1. Lesson root: transcript/*.md + *.vtt + notes, metadata/, video/*.mp4
2. Full codebase under the symlink
3. Gold extract schema from tac-1 `extract.json` — mirror all fields adapted to this lesson
4. `_orchestration/PLAN-LOCKED.md`

## Frames (CRITICAL QUALITY)
- Extract **8–12 FULL-RESOLUTION frames** (prefer native 1920×1080+; never upscale blur)
- Use ffmpeg: `-frames:v 1 -q:v 2` JPEG quality max, or PNG for UI-heavy slides
- Prefer terminal/UI/architecture/code moments over talking heads
- Save to: `media/frames/ah-5-agent-experts/t####-label.jpg` (or .png)
- Document in frame-plan.json with t_seconds, label, why_for_weak_student
- If a slide has small text, prefer PNG and a slightly later/earlier frame where text is sharp

## Deliverables
```
_extracts/ah-5-agent-experts/
  extract.json
  extract.md
  nuggets.md
  outdated-vs-current.md
  frame-plan.json
  lab-spec.md
  STATUS.md
```

### extract.json
Same schema as tac-1 (tactic, mission, core_concepts, step_by_step_demo, quotes, retrieval, lab, yt_overlay_candidates 1–3 phase1 max, frame_plan, codebase_map, etc.)

### Teaching model (weak student)
For every major idea: Hook → Picture → Worked example → Name → Failure → Retrieval

### YT overlays
Strict map-to-lesson / named-gap only; max 1–3 include_in_phase1=true

### Lab
Course codebase only. Gradable checkpoints + pass criteria.

## Verification
- extract.json valid JSON
- all real codebase files mapped
- frames on disk match frame-plan
- STATUS.md DONE + file list

## Out of scope
- Full chapter HTML
- PiCanvas
- Downloading full YT videos

# Fan-out extract brief — LESSON_KEY=ma-4-verifier-agent

You are the **technical accuracy expert** for the IndyDevDan Expert Book.

## Hard constraints
- Write ONLY under: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/`
- Do NOT modify course source trees except reading them
- Do NOT write the full HTML chapter (Codex does that next)
- Use maximum reasoning. Be exhaustive but structured.
- Gold template reference: `_extracts/tac-1-hello-agentic-coding/` + `vol-1-tac/01-CROSS-REVIEW-CLAUDE.md` fan-out checklist

## Lesson
- key: `ma-4-verifier-agent`
- short: `ma-4`
- title: `The Pi Verifier Agent`
- course: `MA`
- order: `18`
- volume dir: `vol-3-ma`
- chapter stem: `18-verifier-agent`  (e.g. 02-the-12-leverage-points)
- catalog lesson: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/ma-4-verifier-agent/`
- codebase: resolve symlink `.../ma-4-verifier-agent/codebase` or curriculum path `agentic-horizon-extras/the-verifier-agent-system` under AgenticEngineer

## Sources (READ thoroughly)
1. Lesson root: transcript/*.md + *.vtt + notes, metadata/, video/*.mp4
2. Full codebase under the symlink
3. Gold extract schema from tac-1 `extract.json` — mirror all fields adapted to this lesson
4. `_orchestration/PLAN-LOCKED.md`

## Frames (CRITICAL QUALITY)
- Extract **8–12 FULL-RESOLUTION frames** (prefer native 1920×1080+; never upscale blur)
- Use ffmpeg: `-frames:v 1 -q:v 2` JPEG quality max, or PNG for UI-heavy slides
- Prefer terminal/UI/architecture/code moments over talking heads
- Save to: `media/frames/ma-4-verifier-agent/t####-label.jpg` (or .png)
- Document in frame-plan.json with t_seconds, label, why_for_weak_student
- If a slide has small text, prefer PNG and a slightly later/earlier frame where text is sharp

## Deliverables
```
_extracts/ma-4-verifier-agent/
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

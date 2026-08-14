# TAC-1 Gold Pilot — Claude Fable extract (Hermes-orchestrated)

You are the **technical accuracy expert** for the IndyDevDan Expert Book pilot.

## Hard constraints
- Write ONLY under: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/`
- Do NOT modify course source trees except reading them
- Do NOT build the full HTML chapter (GPT does that next). You produce structured extract + book scaffold + design tokens skeleton.
- Use maximum reasoning effort. Be exhaustive but structured.

## Sources (READ thoroughly)
1. Lesson root: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/tac-1-hello-agentic-coding/`
2. Transcript MD: `.../transcript/tac-1-hello-agentic-coding.md`
3. Transcript VTT (timestamps): `.../transcript/tac-1-hello-agentic-coding.vtt`
4. Notes: `.../transcript/tac-1-hello-agentic-coding-notes.md`
5. Course page HTML + lesson.json under `metadata/`
6. Codebase (symlink): `.../codebase/` → `AgenticEngineer/tac/tac-1` — read ALL files (README, prompts, programmable scripts, .claude settings)
7. Video: `.../video/tac-1-hello-agentic-coding.mp4` (for frame timestamps only; do not re-encode whole video)

## Deliverables (CREATE all of these)

### A) Book scaffold
```
IndyDevDan/book/
  README.md
  index.html                 # temporary stub hub OK
  design/
    tokens.css
    base.css
    components.css
  data/
    curriculum.json          # Phase-1 map: 18 lessons, empty overlays placeholders
  _extracts/
    tac-1-hello-agentic-coding/
      extract.json           # machine schema
      extract.md             # human readable master notes
      nuggets.md             # ranked nuggets for weak learners
      outdated-vs-current.md # course gaps + YT overlay candidates
      frame-plan.json        # timestamps + why each frame matters
      lab-spec.md            # drills on course codebase only
  media/frames/tac-1/        # extract 5–12 frames if ffmpeg available
  vol-1-tac/                 # empty or stub README for later HTML
  vol-2-ah/
  vol-3-ma/
```

### B) extract.json schema (required fields)
```json
{
  "lesson_key": "tac-1-hello-agentic-coding",
  "title": "Hello Agentic Coding",
  "course": "TAC",
  "order": 1,
  "tactic": { "name": "Stop Coding", "one_liner": "...", "why_uncomfortable": "..." },
  "mission": "...",
  "phase_model": { "phase1_ai_coding": "...", "phase2_agentic_coding": "..." },
  "core_concepts": [
    { "id": "...", "name": "...", "plain_english": "...", "dan_words": "...", "misconception": "..." }
  ],
  "core_four": { "context": "", "model": "", "prompt": "", "tools": "", "why_scale_matters": "" },
  "ai_vs_agentic": {
    "ai_coding_prompt_summary": "",
    "agentic_coding_prompt_summary": "",
    "difference_that_matters": "",
    "codebase_paths": []
  },
  "programmable_agent": {
    "why_it_matters": "",
    "languages": ["shell", "typescript+bun", "python+uv"],
    "files": []
  },
  "loot_box_mentions": [],
  "step_by_step_demo": [],
  "quotes": [{ "text": "", "approx_timestamp": "" }],
  "prerequisites_tools": [],
  "what_student_must_internalize": [],
  "common_weak_student_failures": [],
  "teach_back_prompt": "",
  "retrieval_questions": [{ "q": "", "a": "" }],
  "codebase_map": { "files": [], "what_each_does": {} },
  "current_practice_gaps": [
    { "gap": "Agent Skills under-taught in TAC-1 era", "why": "", "yt_candidates": [] }
  ],
  "yt_overlay_candidates": [
    {
      "video_id": "",
      "title": "",
      "maps_to": "named hole | operationalizes tactic | corrects outdated",
      "include_in_phase1": true,
      "rationale": ""
    }
  ],
  "frame_plan": [
    { "t_seconds": 0, "label": "", "why_for_weak_student": "", "diagram_instead": false }
  ],
  "lab": {
    "setup": [],
    "reproduce_dan": [],
    "stretch": [],
    "pass_criteria": []
  },
  "estimated_print_pages_when_expanded": 40,
  "confidence_notes": []
}
```

### C) Teaching extract rules (weak student → expert)
For every major idea: Hook → Picture description → Worked example from codebase → Name Dan’s term → Failure mode → Retrieval Q.

### D) YT overlay selection (strict)
Phase-1 candidates ONLY if they map to TAC-1 named holes:
- Core Four / tools scale
- Programmable Claude Code / ADWs seed
- “AI coding is not enough”
- Stop coding / commander of compute
- Skills as modern encoding of engineering (named gap vs course era)

Suggested seeds (verify relevance before include_in_phase1=true):
- 2TIXl2rlA6Q AI Coding is NOT ENOUGH
- 6fCqj4xFCZI How Claude Code CHANGED Engineering Forever
- X2ciJedw2vU RAW Agentic Coding: ZERO to Agent SKILL (gap: skills)
- fop_yxV-mPo Codebase Singularity
- hGg3nWp7afg 3 Codebase Folders
Max 1–3 include_in_phase1=true for TAC-1.

### E) Frames
If `ffmpeg` exists, extract 5–12 JPGs into `media/frames/tac-1/` using frame-plan timestamps from VTT. Prefer terminal/UI/architecture moments over talking head. Document paths in frame-plan.json.

### F) Design tokens (light theme skeleton only)
`design/tokens.css` — modern light teaching UI: cream/off-white bg, dark ink text, one accent, readable type scale (system + one distinctive display if webfont optional), spacing, card radii. No heavy dark mode. `base.css` resets + prose. `components.css` stubs for: callout, diagram, frame-card, lab-box, retrieval-quiz, current-practice.

### G) index.html stub
Simple hub listing TAC-1 as “in extract”, link to extracts, note GPT chapter pending.

## Verification before you finish
- All deliverable paths exist
- extract.json validates as JSON
- codebase_map covers every real file under tac-1
- lab can be run only with course codebase
- Write `_extracts/tac-1-hello-agentic-coding/STATUS.md` with DONE + file list + any blockers

## Out of scope
- Do not write vol-1-tac chapter HTML body
- Do not fetch/download full YT videos
- Do not touch PiCanvas

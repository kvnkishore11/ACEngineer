# IndyDevDan Expert Book

A multi-volume, HTML-first teaching book built from IndyDevDan's course catalog
(Tactical Agentic Coding, Agentic Horizon, Multi-Agent extras) plus strictly-mapped
YouTube "Current Practice" overlays.




Orchestration prompts and locked plan live in `_orchestration/` (Hermes-managed).
Worker run logs live in `_logs/`.

## Layout

```
book/
  index.html                  # teaching-site hub and chapter progress
  design/
    tokens.css                # design tokens — light teaching theme (single source of truth)
    base.css                  # reset + prose defaults
    components.css            # callout / diagram / frame-card / lab-box / retrieval-quiz / current-practice
  data/
    curriculum.json           # Phase-1 map: all 18 lessons, overlay placeholders
  _extracts/
    tac-1-hello-agentic-coding/   # ✅ gold pilot extract (see STATUS.md inside)
      extract.json            # machine-readable master extract (schema: see _orchestration/TAC1-CLAUDE-EXTRACT.md)
      extract.md              # human-readable master notes
      nuggets.md              # ranked nuggets for weak learners
      outdated-vs-current.md  # course-era gaps + YT overlay candidates
      frame-plan.json         # video frame timestamps + rationale + extracted paths
      lab-spec.md             # drills on the course codebase only
      STATUS.md               # DONE marker + file list + blockers
  media/frames/tac-1/         # JPG frames extracted from lesson video (ffmpeg)
  vol-1-tac/                  # Volume I — Tactical Agentic Coding (1/8 chapters complete)
  vol-2-ah/                   # Volume II — Agentic Horizon (6 chapters, pending)
  vol-3-ma/                   # Volume III — Multi-Agent extras + synthesis (4 chapters, pending)
```

## Teaching model (every chapter)

Hook → Picture → Worked example (course codebase) → Name Dan's term → Failure mode →
Retrieval questions → Lab → Teach-back → Current-practice overlay.

## Rules

- Course source trees are **read-only**; all book output lives here.
- Labs use course codebases only (never PiCanvas).
- YT overlays are strict: 1–3 per lesson, only if they map to a named lesson hole.
- `design/tokens.css` is the single styling source of truth — chapters must not
  introduce ad-hoc colors or type sizes.



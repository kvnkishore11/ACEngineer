# IndyDevDan — agent lesson catalog

Single place for agents to load IndyDevDan (TAC / AH / MA) materials.
Sources under `AgenticEngineer/` are **not moved** — this tree hardlinks videos and symlinks codebases.

## Layout (every lesson)
```
IndyDevDan/<course-n>-<slug>/          # e.g. tac-1-hello-agentic-coding
  video/<...>.mp4
  transcript/*.{vtt,md,txt}
  metadata/course-page.html   # REAL AE page HTML + local CSS/fonts/img
  metadata/lesson.html        # same
  metadata/lesson.json
  metadata/course-notes.md    # loot-box notes companion (TAC/AH)
  codebase/                   # symlink → real repo
  README.md
assets/                       # shared CSS/fonts/images (offline)
```

Raw dumps: `_source/course-pages/`. Offline-styled: `_source/course-pages-offline/`.

## Catalog

| # | Key | Title | Course | Video | TX | HTML | Code |
|--:|-----|-------|--------|:-----:|:--:|:----:|:----:|
| 1 | `tac-1-hello-agentic-coding` | Hello Agentic Coding | TAC | ✓ | ✓ | ✓ | ✓ |
| 2 | `tac-2-the-12-leverage-points` | The 12 Leverage Points | TAC | ✓ | ✓ | ✓ | ✓ |
| 3 | `tac-3-success-is-planned` | Success is Planned | TAC | ✓ | ✓ | ✓ | ✓ |
| 4 | `tac-4-afk-agents` | AFK Agents | TAC | ✓ | ✓ | ✓ | ✓ |
| 5 | `tac-5-close-the-loops` | Close the Loops | TAC | ✓ | ✓ | ✓ | ✓ |
| 6 | `tac-6-let-your-agents-focus` | Let Your Agents Focus | TAC | ✓ | ✓ | ✓ | ✓ |
| 7 | `tac-7-zte-secret-of-agentic-engineering` | ZTE Secret of Agentic Engineering | TAC | ✓ | ✓ | ✓ | ✓ |
| 8 | `tac-8-the-agentic-layer` | The Agentic Layer | TAC | ✓ | ✓ | ✓ | ✓ |
| 9 | `ah-1-rd-framework-context-window-mastery` | Elite Context Engineering | AH | ✓ | ✓ | ✓ | ✓ |
| 10 | `ah-2-seven-levels-agentic-prompt-formats` | Seven Levels Agentic Prompt Formats | AH | ✓ | ✓ | ✓ | ✓ |
| 11 | `ah-3-building-domain-specific-agents` | Building Domain-Specific Agents | AH | ✓ | ✓ | ✓ | ✓ |
| 12 | `ah-4-multi-agent-orchestration-the-o-agent` | Multi-Agent Orchestration: The O-Agent | AH | ✓ | ✓ | ✓ | ✓ |
| 13 | `ah-5-agent-experts` | Agent Experts | AH | ✓ | ✓ | ✓ | ✓ |
| 14 | `ah-6-building-agentic-layers` | Building Agentic Layers | AH | ✓ | ✓ | ✓ | ✓ |
| 15 | `ma-1-ceo-agents` | CEO Agents | MA | ✓ | ✓ | — | ✓ |
| 16 | `ma-2-lead-agents` | Multi-Team Agentic Coding / Lead Agents | MA | ✓ | ✓ | — | ✓ |
| 17 | `ma-3-ui-agents` | Infinite UI Agents | MA | ✓ | ✓ | — | ✓ |
| 18 | `ma-4-verifier-agent` | The Pi Verifier Agent | MA | ✓ | ✓ | — | ✓ |

## Agent quick paths

- Index: `INDEX.json`
- Real course page: `IndyDevDan/<key>/metadata/course-page.html`
- Plain transcript: prefer `transcript/*.md` then `*.txt` then `*.vtt`
- Code: `IndyDevDan/<key>/codebase/`
- **YouTube (public, last 1 year):** `youtube/` — same folder shape; index `youtube/INDEX.json` (53 videos)

## Rebuild

```bash
# 1) optional: re-dump raw HTML via authenticated CDP → _source/course-pages/
python3 scripts/materialize_course_pages_offline.py   # CSS/fonts/img + offline HTML
python3 scripts/build_indydevdan_catalog.py          # wire into lesson folders
```


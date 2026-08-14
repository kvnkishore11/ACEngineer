# Member Assets (MA)

Unified home for the 4 Agentic Horizon **member exclusive** assets:
videos + transcripts + the matching codebases.

Videos sourced from IndyDevDan public YouTube (mapped via title/description ↔ site cards).

| Key | Title | Video | Codebase (member-assets root) |
|-----|-------|-------|-------------------------------|
| `ma-1-ceo-agents` | CEO Agents | `ma-1-ceo-agents/video/` | `ceo-agents/` |
| `ma-2-lead-agents` | Multi-Team Agentic Coding | `ma-2-lead-agents/video/` | `lead-agents/` |
| `ma-3-ui-agents` | Infinite UI Agents | `ma-3-ui-agents/video/` | `ui-agents/` |
| `ma-4-verifier-agent` | The Pi Verifier Agent | `ma-4-verifier-agent/video/` | `the-verifier-agent-system/` |

## Layout
```
member-assets/
  MANIFEST.json
  transcripts/                 # flat copies of all transcripts
  ceo-agents/                  # -> ../agentic-horizon-extras/ceo-agents
  lead-agents/                 # -> ../agentic-horizon-extras/lead-agents
  ui-agents/                   # -> ../agentic-horizon-extras/ui-agents
  the-verifier-agent-system/   # -> ../agentic-horizon-extras/the-verifier-agent-system
  ma-N-*/
    video/ma-N-*.mp4
    transcripts/{.vtt,.md,.txt}
    meta/                      # yt-dlp info, description, thumbs
```

The four repo folders at this root are **symlinks** to the real clones under
`../agentic-horizon-extras/` (each has its own `.git/`). Update either path — same tree.

Also hardlinked into `../final videos/ma-*.mp4` next to TAC/AH finals.

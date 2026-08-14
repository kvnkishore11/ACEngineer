# AgenticEngineer A/V Sync Validation

All TAC CDP videos were remuxed by trimming/advancing the clear Mux audio by the CDP capture-start offset recorded in `recording.log` / `recording.json`. This compensates for the ~1.4s preflight delay before the first encoded video frame.

| Lesson | Sync offset | Duration | Expected | Best audio peak | Output |
|---|---:|---:|---:|---:|---|
| tac-1 — Hello Agentic Coding | 1.443s | 1311.2s | 1312.6s | -1.6 dB | `/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/tac-1/tac-1-hello-agentic-coding-cdp-15fps-audio-synced.mp4` |
| tac-2 — The 12 Leverage Points | 1.441s | 2834.1s | 2834.8s | -1.4 dB | `/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/tac-2/tac-2-the-12-leverage-points-cdp-15fps-audio-synced.mp4` |
| tac-3 — Success is Planned | 1.431s | 2792.4s | 2791.9s | -0.5 dB | `/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/tac-3/tac-3-success-is-planned-cdp-15fps-audio-synced.mp4` |
| tac-4 — AFK Agents | 1.433s | 2785.8s | 2786.8s | -2.6 dB | `/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/tac-4/tac-4-afk-agents-cdp-15fps-audio-synced.mp4` |
| tac-5 — Close the Loops | 1.425s | 3232.1s | 3233.4s | -3.6 dB | `/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/tac-5/tac-5-close-the-loops-cdp-15fps-audio-synced.mp4` |
| tac-6 — Let Your Agents Focus | 1.435s | 3436.0s | 3436.3s | -1.3 dB | `/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/tac-6/tac-6-let-your-agents-focus-cdp-15fps-audio-synced.mp4` |
| tac-7 — ZTE Secret of Agentic Engineering | 1.451s | 3200.7s | 3201.6s | -2.7 dB | `/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/tac-7/tac-7-zte-secret-of-agentic-engineering-cdp-15fps-audio-synced.mp4` |
| tac-8 — The Agentic Layer | 1.428s | 3798.7s | 3790.6s | -2.5 dB | `/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/tac-8/tac-8-the-agentic-layer-cdp-15fps-audio-synced.mp4` |

Notes:
- Use `*-cdp-15fps-audio-synced.mp4` as the watchable set.
- Treat `*-mux-direct.mp4` as audio-source only when video is DRM-corrupted.
- Future `recover_audio_from_mux.py` now auto-infers and applies the same sync offset unless `--no-auto-sync` is passed.

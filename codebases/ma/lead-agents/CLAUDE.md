# Rules

- Prefer bun over npm.
- When testing Multi-Team Chat via `/drive`, always fully kill and recreate the tmux session (`drive session kill` + `drive session create`) between test runs. Do NOT reuse sessions by sending `just team` into an already-running Pi instance — leftover state causes ghost messages. Also wait for the orchestrator to finish (poll/screenshot) before sending the next prompt to avoid "Working — waiting" spam.
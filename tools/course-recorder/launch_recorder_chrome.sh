#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-9223}"
PROFILE_DIR="${RECORDER_CHROME_PROFILE:-/Users/kvnkishore/.agenticengineer/chrome-recorder-profile}"
URL="${RECORDER_LESSON_URL:-https://agenticengineer.com/tactical-agentic-coding/course/hello-agentic-coding}"

mkdir -p "$PROFILE_DIR"

# Use `open -na` so this does not disturb the user's normal Chrome profile/session.
open -na "Google Chrome" --args \
  --user-data-dir="$PROFILE_DIR" \
  --remote-debugging-port="$PORT" \
  --no-first-run \
  --new-window "$URL"

printf 'launched_profile=%s\n' "$PROFILE_DIR"
printf 'cdp_port=%s\n' "$PORT"
printf 'url=%s\n' "$URL"

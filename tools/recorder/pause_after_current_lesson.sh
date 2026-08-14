#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ROOT="$REPO_ROOT/tools/recorder"
VIDEOS="$REPO_ROOT/media/raw"
LOG="$VIDEOS/pause-after-current.log"
cd "$ROOT"

echo "[$(date)] Pause requested: let current record_lesson finish, then stop queue before next lesson." | tee -a "$LOG"

current_line="$(ps aux | grep -E '[r]ecord_lesson_cdp.py' | head -1 || true)"
if [[ -z "$current_line" ]]; then
  echo "[$(date)] No active record_lesson process found; stopping queue now." | tee -a "$LOG"
else
  echo "[$(date)] Current recorder: $current_line" | tee -a "$LOG"
  current_pid="$(awk '{print $2}' <<<"$current_line")"
  current_key="$(sed -n 's/.*record_lesson_cdp.py \([^ ]*\).*/\1/p' <<<"$current_line" | head -1)"
  echo "[$(date)] Waiting for current lesson $current_key pid=$current_pid to finish." | tee -a "$LOG"
  while kill -0 "$current_pid" 2>/dev/null; do
    sleep 5
  done
  echo "[$(date)] Current recorder finished: $current_key" | tee -a "$LOG"
fi

# Stop the queue/orchestrator before it starts another recording.
pkill -TERM -f 'queue_recordings.py --start tac-2' 2>/dev/null || true
pkill -TERM -f './run_full_course_recording.sh' 2>/dev/null || true
pkill -TERM -f 'caffeinate -dimsu ./run_full_course_recording.sh' 2>/dev/null || true
sleep 2
pkill -KILL -f 'queue_recordings.py --start tac-2' 2>/dev/null || true

# Validate any completed non-validated final outputs and regenerate report.
for key in tac-1 tac-2 tac-3 tac-4 tac-5 tac-6 tac-7 tac-8 ah-1 ah-2 ah-3 ah-4 ah-5 ah-6; do
  case "$key" in
    tac-1) slug="hello-agentic-coding";;
    tac-2) slug="the-12-leverage-points";;
    tac-3) slug="success-is-planned";;
    tac-4) slug="afk-agents";;
    tac-5) slug="close-the-loops";;
    tac-6) slug="let-your-agents-focus";;
    tac-7) slug="zte-secret-of-agentic-engineering";;
    tac-8) slug="the-agentic-layer";;
    ah-1) slug="rd-framework-context-window-mastery";;
    ah-2) slug="seven-levels-agentic-prompt-formats";;
    ah-3) slug="building-domain-specific-agents";;
    ah-4) slug="multi-agent-orchestration-the-o-agent";;
    ah-5) slug="agent-experts";;
    ah-6) slug="building-agentic-layers";;
  esac
  file="$VIDEOS/$key/$key-$slug-cdp-15fps.mp4"
  if [[ -f "$file" ]]; then
    echo "[$(date)] Validating $key" | tee -a "$LOG"
    python3 validate_recording.py "$key" --fps 15 --file "$file" >>"$LOG" 2>&1 || true
  fi
done
python3 generate_recording_report.py >>"$LOG" 2>&1 || true

echo "[$(date)] Paused after current lesson. Report: $VIDEOS/RECORDING_REPORT.md" | tee -a "$LOG"

#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/kvnkishore/WebstormProjects/AgenticEngineer/tools/course-recorder"
VIDEOS="/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos"
PORT="9223"
FPS="15"
QUALITY="88"
AUDIO_DEVICE_INDEX="2"
LOG="$VIDEOS/overnight-recording.log"

cd "$ROOT"
mkdir -p "$VIDEOS"

echo "[$(date)] overnight run starting" | tee -a "$LOG"

# Keep a single recorder Chrome profile/window available. launch_recorder_chrome.sh opens
# the lesson URL in the persistent recorder profile. The recorder scripts reuse the first
# page tab and navigate it lesson-by-lesson, rather than opening new tabs.
if ! python3 - <<'PY' >/dev/null 2>&1
import urllib.request
urllib.request.urlopen('http://localhost:9223/json/version', timeout=2).read()
PY
then
  "$ROOT/launch_recorder_chrome.sh" "$PORT" | tee -a "$LOG"
  sleep 4
fi

# Remove stale in-progress files only; keep completed smoke/test artifacts as proof.
find "$VIDEOS" -name '*.recording.mp4' -not -path '*/_archive_*/*' -print -delete | tee -a "$LOG" || true

SwitchAudioSource -s "Multi-Output Device" -t output >/dev/null || true
echo "[$(date)] output device: $(SwitchAudioSource -c -t output 2>/dev/null || true)" | tee -a "$LOG"

python3 -m py_compile recorder_common.py record_lesson_cdp.py validate_recording.py queue_recordings.py generate_recording_report.py

echo "[$(date)] recording/validating full lesson 1" | tee -a "$LOG"
python3 queue_recordings.py --only tac-1 --fps "$FPS" --quality "$QUALITY" --audio-device-index "$AUDIO_DEVICE_INDEX" --port "$PORT" --force 2>&1 | tee -a "$LOG"

echo "[$(date)] lesson 1 passed; recording remaining lessons sequentially" | tee -a "$LOG"
python3 queue_recordings.py --start tac-2 --fps "$FPS" --quality "$QUALITY" --audio-device-index "$AUDIO_DEVICE_INDEX" --port "$PORT" --force 2>&1 | tee -a "$LOG"

echo "[$(date)] generating final report" | tee -a "$LOG"
python3 generate_recording_report.py 2>&1 | tee -a "$LOG"

echo "[$(date)] overnight run complete" | tee -a "$LOG"

#!/usr/bin/env bash
set -euo pipefail
ROOT="/Users/kvnkishore/WebstormProjects/AgenticEngineer/tools/course-recorder"
VIDEOS="/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos"
LOG="$VIDEOS/ah-recording-queue.log"
cd "$ROOT"

exec > >(tee -a "$LOG") 2>&1

echo "[$(date)] AH recording queue starting. Muted CDP video capture + direct Mux audio + auto sync correction."
python3 -m py_compile record_lesson_cdp.py recover_audio_from_mux.py validate_recording.py generate_recording_report.py

for key in ah-1 ah-2 ah-3 ah-4 ah-5 ah-6; do
  slug=$(python3 - <<PY
import json
m=json.load(open('lesson_manifest.json'))
print([x['slug'] for x in m if x['key']=='$key'][0])
PY
)
  out_dir="$VIDEOS/$key"
  video="$out_dir/$key-$slug-cdp-15fps.mp4"
  synced="$out_dir/$key-$slug-cdp-15fps-audio-synced.mp4"
  echo ""
  echo "[$(date)] ===== $key $slug ====="
  mkdir -p "$out_dir"

  if [[ -f "$synced" ]]; then
    echo "[$(date)] $key synced output already exists; validating only: $synced"
  else
    if [[ ! -f "$video" ]]; then
      echo "[$(date)] Recording muted CDP video for $key"
      rm -f "$out_dir/$key-$slug-cdp-15fps.recording.mp4"
      python3 record_lesson_cdp.py "$key" --port 9223 --fps 15 --quality 88 --audio-device-index none --suffix cdp-15fps --attach-existing
    else
      echo "[$(date)] Reusing existing CDP video: $video"
    fi

    echo "[$(date)] Recovering direct Mux audio and muxing with auto sync correction for $key"
    python3 recover_audio_from_mux.py "$key" --port 9223 --video-suffix cdp-15fps --output-suffix cdp-15fps-audio-synced --force
  fi

  echo "[$(date)] Validating synced output for $key"
  python3 validate_recording.py "$key" --fps 15 --file "$synced"
  grep -E 'Overall|Duration|Transcript duration|Audio volume|audio has audible|duration matches|resolution|fps near' "$out_dir/validation.md" || true
  python3 generate_recording_report.py
  echo "[$(date)] Completed $key"
done

python3 generate_recording_report.py

echo "[$(date)] AH recording queue complete. Report: $VIDEOS/RECORDING_REPORT.md"

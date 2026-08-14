#!/bin/bash
# Batch media processor for AgenticEngineer course videos
# Usage: ./process_media.sh [lesson_dir]

set -e

LESSON_DIR="${1:-.}"
cd "$LESSON_DIR"

# Detect files
AUDIO=$(find . -maxdepth 1 -name "*_audio.aac" -o -name "*.aac" | grep -v "_combined" | head -1)
VIDEO=$(find . -maxdepth 1 -name "*.mp4" -o -name "*.mkv" | grep -v "_combined" | head -1)
FRAMES_DIR="./frames"

if [ -n "$VIDEO" ] && [ ! -d "$FRAMES_DIR" ]; then
    echo "[EXTRACT] Extracting frames from $VIDEO..."
    mkdir -p "$FRAMES_DIR"
    ffmpeg -hide_banner -loglevel error -i "$VIDEO" \
        -vf "fps=1,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
        -q:v 2 "$FRAMES_DIR/frame_%06d.jpg"
    echo "[EXTRACT] Done: $(ls "$FRAMES_DIR" | wc -l) frames extracted"
fi

if [ -d "$FRAMES_DIR" ] && [ -n "$AUDIO" ]; then
    FRAME_COUNT=$(ls "$FRAMES_DIR"/frame_*.jpg 2>/dev/null | wc -l | tr -d ' ')
    AUDIO_DURATION=$(ffmpeg -i "$AUDIO" 2>&1 | grep Duration | awk '{print $2}' | tr -d ',')
    AUDIO_SEC=$(echo "$AUDIO_DURATION" | awk -F: '{print ($1*3600)+($2*60)+$3}')

    echo "[COMBINE] Frames: $FRAME_COUNT | Audio: $AUDIO_DURATION (${AUDIO_SEC}s)"

    if [ "$FRAME_COUNT" -ge "$(echo "$AUDIO_SEC - 5" | bc | cut -d. -f1)" ]; then
        OUTPUT="$(basename "$LESSON_DIR")-combined.mp4"
        echo "[COMBINE] Creating $OUTPUT..."
        ffmpeg -y -hide_banner -loglevel error -framerate 1 \
            -i "$FRAMES_DIR/frame_%06d.jpg" -i "$AUDIO" \
            -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
            -c:v libx264 -r 30 -preset medium -crf 23 \
            -c:a aac -b:a 128k -shortest "$OUTPUT"
        echo "[COMBINE] Done: $OUTPUT"
    else
        echo "[SKIP] Not enough frames ($FRAME_COUNT < ${AUDIO_SEC}s). Need full frame extraction first."
    fi
fi

echo "[DONE] $LESSON_DIR"

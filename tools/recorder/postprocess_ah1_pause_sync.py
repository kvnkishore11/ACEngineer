#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
from __future__ import annotations

import json
import math
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEOS = ROOT / 'videos'
LESSON_DIR = VIDEOS / 'ah-1'
KEY = 'ah-1'
SLUG = 'rd-framework-context-window-mastery'
VIDEO = LESSON_DIR / f'{KEY}-{SLUG}-cdp-15fps.mp4'
AUDIO = LESSON_DIR / f'{KEY}-{SLUG}-mux-audio.m4a'
SYNC_META = LESSON_DIR / f'{KEY}-{SLUG}-cdp-15fps-audio-synced-sync.json'
NOTE = LESSON_DIR / 'manual-pause-note.json'
OUT = LESSON_DIR / f'{KEY}-{SLUG}-cdp-15fps-audio-synced-pause-corrected.mp4'
REPORT = LESSON_DIR / f'{KEY}-{SLUG}-pause-correction.json'


def run(cmd: list[str], *, timeout: int | None = None, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, timeout=timeout, text=True, stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)


def duration(path: Path) -> float:
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(path)], capture=True).stdout.strip())


def wait_for_inputs() -> None:
    while True:
        # The queue creates AUDIO after VIDEO; wait until both are finalized and no .recording remains.
        if VIDEO.exists() and AUDIO.exists() and not (LESSON_DIR / f'{KEY}-{SLUG}-cdp-15fps.recording.mp4').exists():
            try:
                if duration(VIDEO) > 100 and duration(AUDIO) > 100:
                    return
            except Exception:
                pass
        time.sleep(30)


def raw_gray_frames(video: Path, start: float, span: float, fps: int = 2, width: int = 160, height: int = 90) -> list[tuple[float, bytes]]:
    frame_size = width * height
    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error',
        '-ss', f'{start:.3f}', '-t', f'{span:.3f}', '-i', str(video),
        '-vf', f'fps={fps},scale={width}:{height},format=gray',
        '-f', 'rawvideo', '-'
    ]
    cp = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    frames = []
    data = cp.stdout
    for i in range(0, len(data), frame_size):
        chunk = data[i:i+frame_size]
        if len(chunk) == frame_size:
            frames.append((start + (len(frames) / fps), chunk))
    return frames


def mean_abs_diff(a: bytes, b: bytes) -> float:
    return sum(abs(x-y) for x, y in zip(a, b)) / len(a)


def detect_pause(video: Path, note: dict, start_offset: float) -> dict:
    window = note.get('estimated_pause_lesson_time_window_seconds') or []
    observed = float(note.get('latest_estimated_pause_lag_seconds') or 0)
    if len(window) == 2:
        # Convert lesson-time window to video timeline. Video t=0 starts at lesson currentTime=start_offset.
        search_start = max(0.0, float(window[0]) - start_offset - 45)
        search_end = max(search_start + 60.0, float(window[1]) - start_offset + 45)
    else:
        # Fallback around 50 minute mark from user report.
        search_start, search_end = 2850.0, 3250.0
    span = min(search_end - search_start, 480.0)
    frames = raw_gray_frames(video, search_start, span, fps=2)
    diffs = []
    for (t0, f0), (t1, f1) in zip(frames, frames[1:]):
        diffs.append((t1, mean_abs_diff(f0, f1)))
    # Very low diff means the encoded screen was effectively unchanged. Build runs.
    threshold = 0.08
    runs = []
    run_start = None
    last_t = None
    for t, d in diffs:
        if d <= threshold:
            if run_start is None:
                run_start = t - 0.5
            last_t = t
        else:
            if run_start is not None and last_t is not None:
                runs.append((run_start, last_t, last_t - run_start))
            run_start = None
            last_t = None
    if run_start is not None and last_t is not None:
        runs.append((run_start, last_t, last_t - run_start))
    # Keep plausible short accidental-pause runs; choose closest duration to measured lag, otherwise longest.
    plausible = [r for r in runs if 1.0 <= r[2] <= 30.0]
    if plausible and observed > 0:
        chosen = min(plausible, key=lambda r: (abs(r[2] - observed), abs(((r[0]+r[1])/2) - ((search_start+search_end)/2))))
    elif plausible:
        chosen = max(plausible, key=lambda r: r[2])
    else:
        # If frame diff cannot identify it, use observed lag and the center of the user-reported window.
        d = max(0.0, observed)
        center_lesson = (float(window[0]) + float(window[1])) / 2 if len(window) == 2 else search_start + span / 2 + start_offset
        start = max(0.0, center_lesson - start_offset - d / 2)
        chosen = (start, start + d, d)
    return {
        'search_start': search_start,
        'search_end': search_start + span,
        'observed_lag_seconds': observed,
        'threshold': threshold,
        'candidate_runs': [{'start': a, 'end': b, 'duration': c} for a, b, c in plausible[:20]],
        'chosen_video_pause_start': chosen[0],
        'chosen_video_pause_end': chosen[1],
        'chosen_pause_duration': chosen[2],
    }


def make_pause_corrected(video: Path, audio: Path, start_offset: float, pause_start: float, pause_duration: float) -> None:
    tmp = OUT.with_suffix('.recording.mp4')
    if tmp.exists():
        tmp.unlink()
    if OUT.exists():
        OUT.unlink()
    audio_before_end = start_offset + pause_start
    audio_after_start = audio_before_end
    filt = (
        f'[1:a]atrim=start={start_offset:.6f}:end={audio_before_end:.6f},asetpts=PTS-STARTPTS[a0];'
        f'anullsrc=r=48000:cl=stereo,atrim=duration={pause_duration:.6f}[sil];'
        f'[1:a]atrim=start={audio_after_start:.6f},asetpts=PTS-STARTPTS[a1];'
        f'[a0][sil][a1]concat=n=3:v=0:a=1[a]'
    )
    run([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'warning',
        '-i', str(video), '-i', str(audio),
        '-filter_complex', filt,
        '-map', '0:v:0', '-map', '[a]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(tmp)
    ], timeout=1800)
    tmp.rename(OUT)


def main() -> int:
    wait_for_inputs()
    note = json.loads(NOTE.read_text()) if NOTE.exists() else {}
    start_offset = 0.0
    if SYNC_META.exists():
        start_offset = float(json.loads(SYNC_META.read_text()).get('sync_offset_seconds') or 0)
    if start_offset <= 0:
        # AH-1 PREP currentTime from the active recording note/log.
        start_offset = 1.48
    detection = detect_pause(VIDEO, note, start_offset)
    pause_duration = max(0.0, float(detection['chosen_pause_duration']))
    if pause_duration < 0.75:
        REPORT.write_text(json.dumps({'ok': True, 'action': 'no_pause_correction_needed', 'detection': detection}, indent=2, sort_keys=True))
        return 0
    make_pause_corrected(VIDEO, AUDIO, start_offset, float(detection['chosen_video_pause_start']), pause_duration)
    vd = duration(OUT)
    report = {
        'ok': True,
        'action': 'inserted_matching_silence_into_direct_audio_at_pause_window',
        'output': str(OUT),
        'video_input': str(VIDEO),
        'audio_input': str(AUDIO),
        'start_offset_seconds': start_offset,
        'output_duration_seconds': vd,
        'detection': detection,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True))
    # Regenerate validation/checkpoint frames for the pause-corrected output.
    run(['python3', 'validate_recording.py', 'ah-1', '--fps', '15', '--file', str(OUT)], timeout=600)
    run(['python3', 'generate_recording_report.py'], timeout=120)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

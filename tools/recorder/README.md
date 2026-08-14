# AgenticEngineer Course Recorder

Fresh fullscreen recording pipeline for Tactical Agentic Coding / Agentic Horizon lessons.

## Current rules

- Record one lesson at a time.
- Start with lesson 1 only.
- Use one explicit fullscreen monitor/display.
- Verify preflight frame before recording.
- Validate each output before continuing.
- Do not proceed to lesson 2 unless lesson 1 passes.
- Old media has been archived out of the active `videos/` tree.

## Files

- `lesson_manifest.json` — lesson metadata and transcript paths.
- `record_lesson_cdp.py` — Chrome CDP fullscreen/tab recorder with optional BlackHole audio.
- `validate_recording.py` — ffprobe/contact-sheet/audio-silence/duration validator.
- `queue_recordings.py` — sequential recorder queue with validation gate.
- `recorder_common.py` — shared helpers.

## Before recording

Chrome must expose CDP from an authenticated session:

```bash
tools/recorder/launch_recorder_chrome.sh 9223
```

If Chrome shows an `Allow remote debugging` prompt, the user must click Allow.

Audio target:

```bash
SwitchAudioSource -s "Multi-Output Device" -t output
```

The recorder captures BlackHole 2ch as avfoundation audio device index `2` on this machine.

## Smoke test

After lesson 1 is visible/playing/fullscreen on the chosen monitor:

```bash
cd tools/recorder
python3 queue_recordings.py --only tac-1 --seconds 60 --fps 15 --quality 88 --audio-device-index 2 --port 9223
```

The smoke test writes `tac-1-hello-agentic-coding-smoke-15fps.mp4` so it does not occupy the final lesson filename.

Check:

- `media/raw/tac-1/preflight-frame.jpg`
- `media/raw/tac-1/contact-sheet.jpg`
- `media/raw/tac-1/validation.md`

## Full lesson 1

Only after the smoke test passes:

```bash
cd tools/recorder
python3 queue_recordings.py --only tac-1 --fps 15 --quality 88 --audio-device-index 2 --port 9223
```

## Overnight queue

Only after full lesson 1 validates:

```bash
cd tools/recorder
caffeinate -dimsu python3 queue_recordings.py --start tac-2 --fps 15 --quality 88 --audio-device-index 2 --port 9223
```

Use Hermes terminal background mode with `notify_on_complete=true` for the overnight run.

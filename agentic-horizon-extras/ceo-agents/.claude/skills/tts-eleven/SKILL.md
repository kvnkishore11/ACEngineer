---
name: tts-eleven
description: Text-to-speech using ElevenLabs API. Speak text aloud, save audio files, or both. Use when the user asks to say something, speak text, read aloud, generate speech, create audio from text, TTS, text to speech, or voice synthesis.
---

# ElevenLabs Text-to-Speech

Convert text to natural speech using the ElevenLabs API with immediate playback, file saving, or both.

## Prerequisites

- `ELEVENLABS_API_KEY` must be set in the project root `.env` file (scripts use `python-dotenv` to load it automatically)
- macOS required for playback (`afplay`)

## Voice Configuration

| Setting          | Value                    |
| ---------------- | ------------------------ |
| **Voice ID**     | `56bWURjYFHyYyVf490Dp` (Emma)  |
| **Model**        | `eleven_v3`        |
| **Fast Model**   | `eleven_flash_v2_5` (~75ms latency) |
| **Output Format**| `mp3_44100_128`          |
| **Stability**    | `0.5`                    |
| **Similarity**   | `0.75`                   |
| **Style**        | `0.0`                    |

These defaults are baked into both scripts. Override any setting via CLI flags.

## Voice Options

| Name | Voice ID | Accent | Age | Notes |
| ---- | -------- | ------ | --- | ----- |
| **Emma** (default) | `56bWURjYFHyYyVf490Dp` | Australian | Mid | Natural, warm tone |
| Ashlee | `56bWURjYFHyYyVf490Dp` | — | — | Previous default |
| Hope (Bubbly) | `uYXf8XasLslADfZ2MB4u` | American | Young | Bubbly, gossipy, girly energy |
| Dakota | `P7x743VjyZEOihNNygQ9` | American | Mid | Engaging and steady |
| Eryn | `kdnRe2koJdOK4Ovxn2DI` | American | Mid | Genuine, friendly and natural |
| Lori | `TbMNBJ27fH2U0VgpSNko` | American | Young | Happy, sweet and compassionate |
| Chelsea | `NHRgOEwqx5WZNClv5sat` | American | Mid | Conversational and bright |
| Chrissy | `3eIAPRQVsX0VrSFmqoTf` | American | Young | Animated, rapid and inviting |

Use `--voice <id>` to switch voices on any command.

## Workflow

### Workflow 1: TTS (Speak Immediately)

Synthesize text and play it back through speakers. No file saved.

1. **Run text_to_speech.py**:
   ```bash
   uv run ~/.claude/skills/tts-eleven/scripts/text_to_speech.py "Your text here"
   ```

3. Audio plays immediately via `afplay`, temp file is cleaned up.

### Workflow 2: TTF (Save to File)

Synthesize text and save the audio file for later use.

1. **Export API key**:
   ```bash
   okey
   ```

2. **Run text_to_file.py** with output path:
   ```bash
   uv run ~/.claude/skills/tts-eleven/scripts/text_to_file.py "Your text here" -o ~/Desktop/output.mp3
   ```

3. File is saved to the specified path. Report the path back to the user.

### Workflow 3: TTS + TTF (Speak and Save)

Synthesize text, save to file, then play it back. Run both scripts sequentially.

1. **Save to file first**:
   ```bash
   uv run ~/.claude/skills/tts-eleven/scripts/text_to_file.py "Your text here" -o ~/Desktop/output.mp3
   ```

3. **Play the saved file**:
   ```bash
   afplay ~/Desktop/output.mp3
   ```

4. Report the saved file path to the user.

## Workflow Inference

Choose the workflow based on user intent:

| User says...                                      | Workflow  |
| ------------------------------------------------- | --------- |
| "say this", "speak this", "read this aloud"       | **TTS**   |
| "save audio", "create mp3", "generate audio file" | **TTF**   |
| "say this and save it", "speak and save"           | **TTS+TTF** |
| ambiguous / just provides text                     | **TTS**   |

When in doubt, default to **TTS** (immediate playback).

## Script Options

Both scripts share the same flags:

| Option                  | Description                              | Default                  |
| ----------------------- | ---------------------------------------- | ------------------------ |
| `<text>`                | Text to speak. Use `-` for stdin.        | Required                 |
| `-o, --output <path>`   | Output file path (**text_to_file only**) | Required for TTF         |
| `-v, --voice <id>`      | ElevenLabs voice ID                      | `56bWURjYFHyYyVf490Dp`  |
| `-m, --model <id>`      | ElevenLabs model ID                      | `eleven_v3`        |
| `--fast`                | Use Flash v2.5 (~75ms latency, overrides `--model`) | `false`       |
| `-f, --format <fmt>`    | Audio format (e.g. `mp3_44100_128`)      | `mp3_44100_128`          |
| `--stability <float>`   | Voice stability (0.0-1.0)                | `0.5`                    |
| `--similarity <float>`  | Similarity boost (0.0-1.0)               | `0.75`                   |
| `--style <float>`       | Style exaggeration (0.0-1.0)             | `0.0`                    |

## Examples

### Speak text immediately
```bash
uv run ~/.claude/skills/tts-eleven/scripts/text_to_speech.py "Welcome to the channel, let's build something cool today."
```

### Save audio to file
```bash
uv run ~/.claude/skills/tts-eleven/scripts/text_to_file.py "This is a test recording." -o ~/Desktop/test.mp3
```

### Pipe text from stdin
```bash
echo "Hello from a pipe" | uv run ~/.claude/skills/tts-eleven/scripts/text_to_speech.py -
```

### Fast mode (low latency)
```bash
uv run ~/.claude/skills/tts-eleven/scripts/text_to_speech.py --fast "Quick response using Flash model."
```

### Speak and save
```bash
uv run ~/.claude/skills/tts-eleven/scripts/text_to_file.py "Both saved and spoken." -o ~/Desktop/both.mp3 && afplay ~/Desktop/both.mp3
```

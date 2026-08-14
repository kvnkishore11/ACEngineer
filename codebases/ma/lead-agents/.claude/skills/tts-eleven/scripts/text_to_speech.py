#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "typer", "python-dotenv"]
# ///
"""
ElevenLabs Text-to-Speech with immediate playback.

Converts text to speech using the ElevenLabs API and plays it back
immediately using macOS afplay.

Usage:
    ./text_to_speech.py "Hello world"
    ./text_to_speech.py "Hello world" --voice <voice_id>
    ./text_to_speech.py "Hello world" --model eleven_multilingual_v2
    echo "Hello world" | ./text_to_speech.py -
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

import httpx
import typer
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Defaults
DEFAULT_VOICE_ID = "56bWURjYFHyYyVf490Dp"
DEFAULT_MODEL = "eleven_v3"
FAST_MODEL = "eleven_flash_v2_5"
DEFAULT_FORMAT = "mp3_44100_128"

app = typer.Typer(add_completion=False, no_args_is_help=True)


def get_api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        typer.echo("Error: ELEVENLABS_API_KEY environment variable not set", err=True)
        typer.echo("Run: okey  (to export your ElevenLabs key)", err=True)
        raise typer.Exit(1)
    return key


def synthesize(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL,
    output_format: str = DEFAULT_FORMAT,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0.0,
) -> bytes:
    """Call ElevenLabs TTS API and return raw audio bytes."""
    api_key = get_api_key()

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
        },
    }

    url = f"{API_URL}/{voice_id}"

    with httpx.Client(timeout=120.0) as client:
        resp = client.post(
            url,
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            params={"output_format": output_format},
            json=payload,
        )
        if resp.status_code != 200:
            typer.echo(f"API Error ({resp.status_code}): {resp.text}", err=True)
            raise typer.Exit(1)
        return resp.content


def play_audio(audio_bytes: bytes, fmt: str = "mp3") -> None:
    """Play audio bytes using macOS afplay."""
    with tempfile.NamedTemporaryFile(suffix=f".{fmt}", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name

    try:
        subprocess.run(["afplay", tmp_path], check=True)
    except FileNotFoundError:
        typer.echo("Error: afplay not found. This script requires macOS.", err=True)
        raise typer.Exit(1)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Playback error: {e}", err=True)
        raise typer.Exit(1)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@app.command()
def main(
    text: str = typer.Argument(..., help="Text to speak. Use '-' to read from stdin."),
    voice: str = typer.Option(DEFAULT_VOICE_ID, "--voice", "-v", help="ElevenLabs voice ID"),
    model: str = typer.Option(DEFAULT_MODEL, "--model", "-m", help="ElevenLabs model ID"),
    fast: bool = typer.Option(False, "--fast", help="Use Flash v2.5 for ~75ms latency (overrides --model)"),
    output_format: str = typer.Option(DEFAULT_FORMAT, "--format", "-f", help="Audio output format"),
    stability: float = typer.Option(0.5, "--stability", help="Voice stability (0.0-1.0)"),
    similarity: float = typer.Option(0.75, "--similarity", help="Similarity boost (0.0-1.0)"),
    style: float = typer.Option(0.0, "--style", help="Style exaggeration (0.0-1.0)"),
):
    """Convert text to speech and play it immediately."""
    # Handle stdin
    if text == "-":
        text = sys.stdin.read().strip()
        if not text:
            typer.echo("Error: No text provided via stdin", err=True)
            raise typer.Exit(1)

    if fast:
        model = FAST_MODEL
        typer.echo(f"Fast mode: using {FAST_MODEL} (~75ms latency)", err=True)

    typer.echo(f"Synthesizing ({len(text)} chars)...", err=True)
    audio = synthesize(
        text=text,
        voice_id=voice,
        model_id=model,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity,
        style=style,
    )
    typer.echo(f"Playing audio ({len(audio)} bytes)...", err=True)
    play_audio(audio)


if __name__ == "__main__":
    app()

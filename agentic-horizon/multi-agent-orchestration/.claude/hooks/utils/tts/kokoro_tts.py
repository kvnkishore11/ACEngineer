#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "kokoro>=0.9.4",
#     "soundfile",
#     "torch",
# ]
# ///

import sys
import tempfile
from pathlib import Path

def main():
    """
    Kokoro TTS Script

    Uses Kokoro-82M for fast, high-quality text-to-speech synthesis.
    Accepts optional text prompt as command-line argument.

    Usage:
    - ./kokoro_tts.py                    # Uses default text
    - ./kokoro_tts.py "Your custom text" # Uses provided text

    Features:
    - Fast local TTS (no API key required)
    - 82M parameter model with excellent quality
    - CPU-efficient
    - Apache-licensed (fully open source)
    - Multiple voices and languages
    """

    try:
        from kokoro import KPipeline
        import soundfile as sf
        import subprocess
        import platform

        print("🎙️  Kokoro TTS")
        print("=" * 15)

        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])
        else:
            text = "Your agent needs your input"

        print(f"🎯 Text: {text}")
        print("🔊 Generating speech...")

        # Initialize Kokoro pipeline
        # lang_code 'a' is for American English
        pipeline = KPipeline(lang_code='a')

        # Generate audio
        # Using 'af_heart' voice (female, clear voice)
        # Other options: 'af_sky', 'am_adam', 'am_michael', etc.
        generator = pipeline(text, voice='af_heart')

        # Get the audio from the generator
        audio = None
        for i, (gs, ps, audio_chunk) in enumerate(generator):
            audio = audio_chunk
            break  # Take first chunk for quick notifications

        if audio is None:
            print("❌ Failed to generate audio")
            sys.exit(1)

        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            temp_path = temp_wav.name
            sf.write(temp_path, audio, 24000)

        print("🔊 Playing audio...")

        # Play the audio file using system audio player
        try:
            system = platform.system()

            if system == "Darwin":  # macOS
                subprocess.run(["afplay", temp_path], check=True)
            elif system == "Linux":
                # Try different players
                for player in ["aplay", "paplay", "ffplay", "mpg123"]:
                    try:
                        subprocess.run([player, temp_path], check=True, stderr=subprocess.DEVNULL)
                        break
                    except (FileNotFoundError, subprocess.CalledProcessError):
                        continue
            elif system == "Windows":
                import winsound
                winsound.PlaySound(temp_path, winsound.SND_FILENAME)
        finally:
            # Clean up temp file
            Path(temp_path).unlink(missing_ok=True)

        print("✅ Playback complete!")

    except ImportError as e:
        print("❌ Error: Required packages not installed")
        print(f"   {e}")
        print("\nThis script uses UV to auto-install dependencies.")
        print("Install manually: pip install kokoro>=0.9.4 soundfile torch")
        print("\nNote: On Linux, you may also need: apt-get install espeak-ng")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

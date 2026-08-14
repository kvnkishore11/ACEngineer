#!/usr/bin/env python3
"""
Process TAC-5 VTT transcript files and create a complete, clean transcript.
"""

import os
import re
from pathlib import Path

def extract_text_from_vtt(vtt_content):
    """Extract only the spoken text from VTT content, removing timestamps and metadata."""
    lines = vtt_content.split('\n')
    text_lines = []

    # Skip WEBVTT header and empty lines
    in_text = False
    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            in_text = False
            continue

        # Skip WEBVTT header
        if line.startswith('WEBVTT'):
            continue

        # Skip timestamp lines (contain -->)
        if '-->' in line:
            in_text = True
            continue

        # If we're in text section (after timestamp), capture the text
        if in_text and not line.isdigit():
            # Remove speaker tags if present (e.g., <v Speaker>)
            line = re.sub(r'<v[^>]*>', '', line)
            line = re.sub(r'</v>', '', line)
            # Remove other VTT tags
            line = re.sub(r'<[^>]*>', '', line)

            if line:
                text_lines.append(line)

    return ' '.join(text_lines)

def process_all_transcripts():
    """Process all VTT files and create a complete transcript."""
    transcript_dir = Path("/Users/kvnkishore/Downloads/tac transcripts/tac-5")
    output_dir = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/tac-5-deep-dive")

    # Get all VTT files
    vtt_files = sorted(transcript_dir.glob("*.vtt"))

    # Sort numerically (handle files like "0.vtt", "10.vtt", "100.vtt" correctly)
    def extract_number(filepath):
        basename = filepath.stem
        # Remove " - 1" suffix if present
        basename = basename.replace(" - 1", "")
        try:
            return int(basename)
        except ValueError:
            return float('inf')

    # Filter out duplicate " - 1" files, keeping the originals
    unique_files = []
    seen_numbers = set()
    for f in vtt_files:
        num = extract_number(f)
        if num not in seen_numbers or " - 1" not in f.name:
            unique_files.append(f)
            seen_numbers.add(num)

    # Sort by extracted number
    unique_files.sort(key=extract_number)

    print(f"Processing {len(unique_files)} VTT files...")

    complete_transcript = []

    for i, vtt_file in enumerate(unique_files):
        print(f"Processing {vtt_file.name}...")

        try:
            with open(vtt_file, 'r', encoding='utf-8') as f:
                content = f.read()

            text = extract_text_from_vtt(content)

            if text:
                # Add section header
                video_number = extract_number(vtt_file)
                complete_transcript.append(f"\n\n## Video {video_number}")
                complete_transcript.append(f"*Source: {vtt_file.name}*\n")
                complete_transcript.append(text)

        except Exception as e:
            print(f"Error processing {vtt_file.name}: {e}")

    # Write complete transcript
    output_file = output_dir / "COMPLETE-TRANSCRIPT.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# TAC-5 Complete Transcript\n\n")
        f.write("This is the complete, chronologically ordered transcript of all TAC-5 videos.\n\n")
        f.write("---\n")
        f.write('\n'.join(complete_transcript))

    print(f"\nComplete transcript saved to: {output_file}")
    print(f"Total videos processed: {len(unique_files)}")

if __name__ == "__main__":
    process_all_transcripts()
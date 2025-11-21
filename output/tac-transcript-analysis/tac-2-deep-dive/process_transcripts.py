#!/usr/bin/env python3
"""
Process TAC-2 VTT transcript files and create a complete, clean transcript.
"""

import re
import os
from pathlib import Path

def extract_text_from_vtt(vtt_content):
    """Extract clean text from VTT content, removing timestamps and metadata."""
    lines = vtt_content.split('\n')
    text_lines = []

    # Skip WEBVTT header
    i = 0
    while i < len(lines) and not lines[i].strip().startswith('00:'):
        i += 1

    # Process transcript blocks
    while i < len(lines):
        line = lines[i].strip()

        # Skip timestamp lines (contain -->)
        if '-->' in line:
            i += 1
            continue

        # Skip cue identifiers (just numbers)
        if line.isdigit():
            i += 1
            continue

        # Skip empty lines
        if not line:
            i += 1
            continue

        # This is actual transcript text
        # Clean up any remaining timestamps or special characters
        clean_line = re.sub(r'^\d+$', '', line)  # Remove lone numbers
        clean_line = re.sub(r'<.*?>', '', clean_line)  # Remove any HTML tags
        clean_line = clean_line.strip()

        if clean_line:
            text_lines.append(clean_line)

        i += 1

    return ' '.join(text_lines)

def process_all_transcripts():
    """Process all VTT files and create a complete transcript."""
    transcript_dir = Path('/Users/kvnkishore/Downloads/tac transcripts/tac-2')
    output_dir = Path('/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/tac-2-deep-dive')

    # Get all VTT files sorted by number
    vtt_files = []
    for f in transcript_dir.glob('*.vtt'):
        # Extract number from filename
        num = int(f.stem)
        vtt_files.append((num, f))

    vtt_files.sort(key=lambda x: x[0])

    complete_transcript = []

    for num, vtt_file in vtt_files:
        print(f"Processing {vtt_file.name}...")

        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        text = extract_text_from_vtt(content)

        if text:
            # Add section header
            complete_transcript.append(f"\n\n## Video {num}\n")
            complete_transcript.append(text)

    # Write complete transcript
    output_file = output_dir / 'COMPLETE-TRANSCRIPT.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# TAC-2 Complete Transcript\n\n")
        f.write("This is the complete, stitched transcript from all TAC-2 video files.\n")
        f.write("\n---\n")
        f.write('\n'.join(complete_transcript))

    print(f"\nComplete transcript saved to: {output_file}")
    print(f"Processed {len(vtt_files)} video transcripts")

if __name__ == "__main__":
    process_all_transcripts()
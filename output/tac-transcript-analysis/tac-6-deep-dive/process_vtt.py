#!/usr/bin/env python3
"""Process VTT transcript files and extract clean text."""

import os
import re
from pathlib import Path

def extract_text_from_vtt(vtt_content):
    """Extract clean text from VTT content."""
    lines = vtt_content.strip().split('\n')
    text_parts = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip WEBVTT header
        if line == 'WEBVTT':
            i += 1
            continue

        # Skip sequence numbers (digits only)
        if line.isdigit():
            i += 1
            continue

        # Skip timestamp lines
        if '-->' in line:
            i += 1
            continue

        # Skip empty lines
        if not line:
            i += 1
            continue

        # This is actual transcript text
        text_parts.append(line)
        i += 1

    return ' '.join(text_parts)

def process_all_vtt_files():
    """Process all VTT files and create complete transcript."""
    vtt_dir = Path('/Users/kvnkishore/Downloads/tac transcripts/tac-6')
    output_dir = Path('/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/tac-6-deep-dive')

    # Get all VTT files sorted numerically
    vtt_files = []
    for f in vtt_dir.glob('*.vtt'):
        # Extract number from filename for proper sorting
        num = int(f.stem)
        vtt_files.append((num, f))

    vtt_files.sort(key=lambda x: x[0])

    # Process each file and collect transcript
    full_transcript = []

    for num, vtt_file in vtt_files:
        print(f"Processing {vtt_file.name}...")

        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        text = extract_text_from_vtt(content)

        if text:
            # Add section marker
            full_transcript.append(f"\n\n## Video Segment {num}\n")
            full_transcript.append(text)

    # Write complete transcript
    output_file = output_dir / 'COMPLETE-TRANSCRIPT.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# TAC-6 Complete Video Transcript\n\n")
        f.write("*Extracted and compiled from all TAC-6 video segments*\n")
        f.write(''.join(full_transcript))

    print(f"\nComplete transcript written to {output_file}")
    print(f"Total segments processed: {len(vtt_files)}")

    return len(vtt_files)

if __name__ == '__main__':
    process_all_vtt_files()
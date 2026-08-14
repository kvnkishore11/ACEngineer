#!/usr/bin/env python3
"""
Process Elite Context Engineering VTT transcripts
Strips WebVTT timing codes and metadata, stitches content in order
"""

import os
import re
from pathlib import Path

def clean_vtt_content(content):
    """
    Clean VTT content by removing timestamps and metadata
    """
    lines = content.split('\n')
    cleaned_lines = []

    # Skip WEBVTT header
    start_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('WEBVTT'):
            start_index = i + 1
            break

    # Process remaining lines
    i = start_index
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Skip timestamp lines (contain -->)
        if '-->' in line:
            i += 1
            continue

        # Skip lines that are just numbers (cue identifiers)
        if line.isdigit():
            i += 1
            continue

        # Skip lines that start with NOTE
        if line.startswith('NOTE'):
            i += 1
            continue

        # This is actual transcript content
        # Remove any remaining HTML tags
        line = re.sub(r'<[^>]+>', '', line)
        # Remove speaker labels if present (e.g., "Speaker 1:")
        line = re.sub(r'^Speaker \d+:\s*', '', line)

        if line:
            cleaned_lines.append(line)

        i += 1

    return ' '.join(cleaned_lines)

def process_transcripts():
    """
    Process all VTT files and create complete transcript
    """
    transcript_dir = Path("/Users/kvnkishore/Downloads/tac transcripts/elite context engineering")
    output_dir = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/elite-context-engineering-deep-dive")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect all VTT files
    vtt_files = []
    for i in range(148):  # 0.vtt through 147.vtt
        file_path = transcript_dir / f"{i}.vtt"
        if file_path.exists():
            vtt_files.append((i, file_path))

    print(f"Found {len(vtt_files)} VTT files")

    # Process and combine
    full_transcript = []
    full_transcript.append("# Elite Context Engineering - Complete Transcript")
    full_transcript.append("\n*Compiled from 148 video segments*\n")
    full_transcript.append("---\n")

    for file_num, file_path in vtt_files:
        print(f"Processing {file_num}.vtt...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned = clean_vtt_content(content)

            if cleaned:
                full_transcript.append(f"\n## Segment {file_num}")
                full_transcript.append(f"\n{cleaned}\n")

        except Exception as e:
            print(f"Error processing {file_num}.vtt: {e}")
            continue

    # Save complete transcript
    output_file = output_dir / "COMPLETE-TRANSCRIPT.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(full_transcript))

    print(f"\nComplete transcript saved to: {output_file}")
    print(f"Total segments processed: {len(vtt_files)}")

if __name__ == "__main__":
    process_transcripts()
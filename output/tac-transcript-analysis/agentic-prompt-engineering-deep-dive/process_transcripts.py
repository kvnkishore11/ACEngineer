#!/usr/bin/env python3
"""
Process Agentic Prompt Engineering VTT transcripts into a single clean document.
Strips WebVTT timing codes and metadata, keeping only spoken content.
"""

import os
import re
from pathlib import Path

def clean_vtt_content(content):
    """Remove VTT metadata and timing, extract only spoken text."""
    lines = content.split('\n')
    cleaned_lines = []
    skip_next = False

    for line in lines:
        line = line.strip()

        # Skip WEBVTT header
        if line == 'WEBVTT':
            continue

        # Skip sequence numbers (single digits or multi-digit numbers on their own line)
        if line.isdigit():
            skip_next = True
            continue

        # Skip timestamp lines (e.g., 00:00:07.201 --> 00:00:12.474)
        if skip_next or '-->' in line:
            skip_next = False
            continue

        # Skip empty lines
        if not line:
            continue

        # Add the actual transcript text
        cleaned_lines.append(line)

    return ' '.join(cleaned_lines)

def process_all_transcripts(input_dir, output_file):
    """Process all VTT files in order and save to single output file."""

    # Get all VTT files and sort them numerically
    vtt_files = []
    for i in range(115):  # We know there are 115 files
        file_path = Path(input_dir) / f"{i}.vtt"
        if file_path.exists():
            vtt_files.append(file_path)

    print(f"Found {len(vtt_files)} VTT files to process")

    # Process each file and collect content
    all_content = []

    for vtt_file in vtt_files:
        print(f"Processing: {vtt_file.name}")

        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned = clean_vtt_content(content)

        if cleaned:
            # Add section marker with file name
            all_content.append(f"\n\n### Section {vtt_file.stem}\n\n{cleaned}")

    # Join all content with proper formatting
    final_content = """# Agentic Prompt Engineering - Complete Video Transcript

This is the complete transcript from the Agentic Prompt Engineering video series,
processed from 115 VTT subtitle files. The content has been cleaned to remove all
timing codes and metadata, preserving only the spoken content.

---
"""

    final_content += '\n'.join(all_content)

    # Add footer
    final_content += """

---

*End of Transcript*

This transcript was automatically processed from VTT subtitle files.
Some minor formatting inconsistencies may exist due to the nature of subtitle timing.
"""

    # Save to output file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"\nTranscript saved to: {output_path}")
    print(f"Total sections processed: {len(all_content)}")

    # Calculate approximate statistics
    word_count = len(final_content.split())
    char_count = len(final_content)

    print(f"Word count: {word_count:,}")
    print(f"Character count: {char_count:,}")

if __name__ == "__main__":
    input_directory = "/Users/kvnkishore/Downloads/tac transcripts/Agentic Prompt Engineering"
    output_file = "/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/agentic-prompt-engineering-deep-dive/COMPLETE-TRANSCRIPT.md"

    process_all_transcripts(input_directory, output_file)
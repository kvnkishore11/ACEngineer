#!/usr/bin/env python3

import os
import re
from pathlib import Path

def extract_vtt_text(vtt_path):
    """Extract text content from VTT file, removing timestamps."""
    try:
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove WebVTT header
        content = re.sub(r'^WEBVTT.*?\n\n', '', content, flags=re.MULTILINE | re.DOTALL)

        # Split into caption blocks (separated by double newlines)
        blocks = content.split('\n\n')

        text_parts = []

        for block in blocks:
            lines = block.strip().split('\n')

            # Process each block
            text_lines = []
            for line in lines:
                # Skip timestamp lines (format: 00:00:00.000 --> 00:00:00.000)
                if '-->' in line:
                    continue
                # Skip numeric indices (usually first line of each caption block)
                if line.strip() and not (line.strip().isdigit() and len(line.strip()) <= 4):
                    # Not a pure number or is a long number (part of actual content)
                    text_lines.append(line.strip())
                elif line.strip() and not line.strip().isdigit():
                    # Any non-numeric, non-empty line
                    text_lines.append(line.strip())

            if text_lines:
                text_parts.append(' '.join(text_lines))

        # Join all text parts with spaces
        full_text = ' '.join(text_parts)

        # Clean up excessive whitespace
        full_text = re.sub(r'\s+', ' ', full_text)

        return full_text.strip()

    except Exception as e:
        print(f"Error processing {vtt_path}: {e}")
        return ""

def process_all_transcripts():
    """Process all VTT files and create complete transcript."""

    transcript_dir = Path("/Users/kvnkishore/Downloads/tac transcripts/tac-4")
    output_dir = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/tac-4-deep-dive")

    # Get all VTT files
    vtt_files = []

    # First, add numbered files in order (0.vtt to 94.vtt)
    for i in range(95):  # 0 to 94
        file_path = transcript_dir / f"{i}.vtt"
        if file_path.exists():
            vtt_files.append(file_path)

    # Then add the " - 1" versions if they exist (these seem to be duplicates or continuations)
    for i in range(10):  # 0 - 1.vtt to 9 - 1.vtt
        file_path = transcript_dir / f"{i} - 1.vtt"
        if file_path.exists():
            vtt_files.append(file_path)

    print(f"Found {len(vtt_files)} VTT files to process")

    # Process each file and collect text
    all_transcripts = []

    for idx, vtt_file in enumerate(vtt_files):
        print(f"Processing {idx + 1}/{len(vtt_files)}: {vtt_file.name}")

        text = extract_vtt_text(vtt_file)

        if text:
            # Add section header for each video
            section_header = f"\n\n{'='*80}\n"
            section_header += f"VIDEO SEGMENT: {vtt_file.name}\n"
            section_header += f"{'='*80}\n\n"

            all_transcripts.append(section_header + text)

    # Create the complete transcript
    complete_transcript = """# TAC-4 Complete Video Transcript

This document contains the complete transcript of all TAC-4 video segments,
processed and stitched together in chronological order.

## Overview

- **Total Video Segments**: {}
- **Module**: TAC-4 (Agentic Development Workflow)
- **Focus**: ADW system, Agent pipelines, Autonomous workflows, Issue-to-PR automation

---

## Complete Transcript

{}
""".format(len(vtt_files), "\n".join(all_transcripts))

    # Save the complete transcript
    output_path = output_dir / "COMPLETE-TRANSCRIPT.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(complete_transcript)

    print(f"\nComplete transcript saved to: {output_path}")
    print(f"Total segments processed: {len(vtt_files)}")
    print(f"Total characters: {len(complete_transcript)}")

    # Also create a cleaner version without segment markers for easier reading
    clean_text = []
    for transcript in all_transcripts:
        # Remove the segment headers
        lines = transcript.split('\n')
        content_lines = []
        skip_next = 0
        for line in lines:
            if '=' * 80 in line:
                skip_next = 2
            elif skip_next > 0:
                skip_next -= 1
            else:
                content_lines.append(line)
        clean_text.append('\n'.join(content_lines).strip())

    clean_transcript = """# TAC-4 Complete Video Transcript (Clean Version)

This is the clean, continuous version of all TAC-4 video transcripts without segment markers.

---

{}
""".format('\n\n'.join(clean_text))

    clean_output_path = output_dir / "COMPLETE-TRANSCRIPT-CLEAN.md"
    with open(clean_output_path, 'w', encoding='utf-8') as f:
        f.write(clean_transcript)

    print(f"Clean transcript saved to: {clean_output_path}")

    return output_path, len(vtt_files)

if __name__ == "__main__":
    output_path, num_segments = process_all_transcripts()
    print(f"\n✅ Successfully created complete transcript from {num_segments} video segments!")
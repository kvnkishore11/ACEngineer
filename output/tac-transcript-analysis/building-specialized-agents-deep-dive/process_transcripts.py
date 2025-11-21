#!/usr/bin/env python3
"""
Process VTT transcripts from Building Specialized Agents module.
Strips timing codes and metadata, keeping only spoken content.
"""

import os
import re
from pathlib import Path

def clean_vtt_content(content):
    """Remove VTT metadata, timing codes, and clean the transcript."""
    lines = content.split('\n')
    cleaned_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        # Skip WEBVTT header
        if line.startswith('WEBVTT'):
            continue

        # Skip timing lines (contain -->)
        if '-->' in line:
            skip_next = False
            continue

        # Skip empty lines
        if not line.strip():
            continue

        # Skip lines that are just numbers (cue identifiers)
        if line.strip().isdigit():
            continue

        # Skip lines that match timestamp patterns
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}', line.strip()):
            continue

        # Add the actual transcript content
        cleaned_lines.append(line.strip())

    # Join lines and clean up extra spaces
    text = ' '.join(cleaned_lines)
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove any remaining timing artifacts
    text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}', '', text)

    return text.strip()

def process_all_transcripts():
    """Process all VTT files and combine into one transcript."""
    transcript_dir = Path("/Users/kvnkishore/Downloads/tac transcripts/Buidling Specialized Agents")
    output_dir = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/building-specialized-agents-deep-dive")

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    all_transcripts = []

    # Process files in numerical order (0.vtt through 134.vtt)
    for i in range(135):
        vtt_file = transcript_dir / f"{i}.vtt"

        if vtt_file.exists():
            print(f"Processing {vtt_file.name}...")

            with open(vtt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            cleaned_content = clean_vtt_content(content)

            if cleaned_content:
                # Add section header
                all_transcripts.append(f"\n\n## Section {i}\n")
                all_transcripts.append(cleaned_content)
        else:
            print(f"Warning: {vtt_file.name} not found")

    # Combine all transcripts
    complete_transcript = ''.join(all_transcripts)

    # Save the complete transcript
    output_file = output_dir / "COMPLETE-TRANSCRIPT.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Building Specialized Agents - Complete Transcript\n\n")
        f.write("*Processed from 135 VTT files*\n\n")
        f.write("---\n")
        f.write(complete_transcript)

    print(f"\nComplete transcript saved to: {output_file}")
    section_count = len([t for t in all_transcripts if t.startswith('\n\n## Section')])
    print(f"Total sections processed: {section_count}")

    # Print some stats
    word_count = len(complete_transcript.split())
    print(f"Total words: {word_count:,}")
    print(f"Approximate reading time: {word_count // 200} minutes")

if __name__ == "__main__":
    process_all_transcripts()
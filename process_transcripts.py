#!/usr/bin/env python3
"""
Process Multi-Agent Orchestration VTT transcripts into a single cleaned document.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def clean_vtt_content(content: str) -> str:
    """
    Remove WebVTT metadata, timing codes, and extract only spoken content.
    """
    lines = content.split('\n')
    cleaned_lines = []

    # Skip WebVTT header
    start_index = 0
    for i, line in enumerate(lines):
        if line.strip() == 'WEBVTT' or line.startswith('Kind:') or line.startswith('Language:'):
            start_index = i + 1
            continue
        if line.strip() and '-->' not in line and not re.match(r'^\d{2}:\d{2}:\d{2}', line):
            break

    # Process the rest
    i = start_index
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Skip timing lines (contain -->)
        if '-->' in line:
            i += 1
            continue

        # Skip standalone timestamps
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}$', line):
            i += 1
            continue

        # Skip cue identifiers (usually just numbers)
        if re.match(r'^\d+$', line):
            i += 1
            continue

        # This should be actual transcript content
        cleaned_lines.append(line)
        i += 1

    # Join lines and clean up spacing
    text = ' '.join(cleaned_lines)

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Clean up common artifacts
    text = text.replace(' .', '.')
    text = text.replace(' ,', ',')
    text = text.replace(' ?', '?')
    text = text.replace(' !', '!')

    return text.strip()

def get_file_order(filename: str) -> Tuple[int, int]:
    """
    Extract the numeric order from filename for sorting.
    Returns (primary_number, is_duplicate)
    """
    # Remove .vtt extension
    name = filename.replace('.vtt', '')

    # Check if it's a duplicate (contains " - 1")
    is_duplicate = ' - 1' in name

    # Extract the number
    if is_duplicate:
        # Format: "N - 1"
        num_str = name.split(' - ')[0]
    else:
        # Format: "N"
        num_str = name

    try:
        num = int(num_str)
    except ValueError:
        # Handle any edge cases
        return (999, 1 if is_duplicate else 0)

    return (num, 1 if is_duplicate else 0)

def process_transcripts(input_dir: str, output_file: str):
    """
    Process all VTT files in the directory and create a single transcript.
    """
    input_path = Path(input_dir)

    # Get all VTT files
    vtt_files = list(input_path.glob('*.vtt'))

    # Sort files by numeric order
    vtt_files.sort(key=lambda f: get_file_order(f.name))

    print(f"Found {len(vtt_files)} VTT files to process")

    # Process each file
    all_content = []

    for i, vtt_file in enumerate(vtt_files):
        print(f"Processing {i+1}/{len(vtt_files)}: {vtt_file.name}")

        try:
            with open(vtt_file, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned = clean_vtt_content(content)

            if cleaned:
                # Add section header
                all_content.append(f"\n## Section {i+1} (from {vtt_file.name})\n")
                all_content.append(cleaned)
                all_content.append("\n")

        except Exception as e:
            print(f"Error processing {vtt_file.name}: {e}")
            continue

    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the complete transcript
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Multi-Agent Orchestration - Complete Transcript\n\n")
        f.write("*Compiled from 125 video transcript segments*\n\n")
        f.write("---\n\n")
        f.write(''.join(all_content))

    print(f"\nComplete transcript saved to: {output_file}")

    # Calculate statistics
    total_words = sum(len(content.split()) for content in all_content if not content.startswith('\n##'))
    print(f"Total words: {total_words:,}")
    print(f"Total sections: {len([c for c in all_content if c.startswith('\n##')])}")

if __name__ == "__main__":
    input_directory = "/Users/kvnkishore/Downloads/tac transcripts/mulit agent orchestration/"
    output_file = "/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/multi-agent-orchestration-deep-dive/COMPLETE-TRANSCRIPT.md"

    process_transcripts(input_directory, output_file)
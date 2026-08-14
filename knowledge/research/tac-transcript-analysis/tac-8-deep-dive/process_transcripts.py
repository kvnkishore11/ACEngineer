#!/usr/bin/env python3
"""
Process TAC-8 VTT transcripts and stitch them into a single, clean transcript.
This script reads all 133 VTT files, removes timing codes and metadata,
and creates a comprehensive transcript preserving the author's teaching.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def extract_number(filename: str) -> Tuple[int, int]:
    """
    Extract the number from a filename for sorting.
    Handles both "10.vtt" and "10 - 1.vtt" formats.
    Returns (primary_number, secondary_number) for sorting.
    """
    base = os.path.basename(filename)
    base = base.replace('.vtt', '')

    # Check for " - 1" format (duplicate/continuation files)
    if ' - ' in base:
        parts = base.split(' - ')
        primary = int(parts[0]) if parts[0].isdigit() else 999
        secondary = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return (primary, secondary)
    else:
        # Regular numbered file
        if base.isdigit():
            return (int(base), 0)

    return (999, 0)  # Default for any unrecognized format

def clean_vtt_content(content: str) -> str:
    """
    Remove WebVTT metadata, timing codes, and clean up the transcript.
    Preserves only the actual spoken content.
    """
    lines = content.split('\n')
    cleaned_lines = []

    skip_next = False
    for line in lines:
        line = line.strip()

        # Skip WebVTT header
        if line == 'WEBVTT' or line.startswith('Kind:') or line.startswith('Language:'):
            continue

        # Skip timing lines (contain -->)
        if '-->' in line:
            skip_next = False
            continue

        # Skip line numbers (typically just a number on its own line)
        if line.isdigit():
            continue

        # Skip empty lines
        if not line:
            continue

        # Skip NOTE blocks
        if line.startswith('NOTE'):
            skip_next = True
            continue

        if skip_next:
            continue

        # Clean up common VTT artifacts
        # Remove speaker labels if present
        line = re.sub(r'^<v [^>]+>', '', line)
        line = re.sub(r'</v>$', '', line)

        # Remove other HTML-like tags
        line = re.sub(r'<[^>]+>', '', line)

        # Clean up special characters
        line = line.replace('&amp;', '&')
        line = line.replace('&lt;', '<')
        line = line.replace('&gt;', '>')
        line = line.replace('&quot;', '"')
        line = line.replace('&#39;', "'")

        if line:
            cleaned_lines.append(line)

    # Join lines with space, but preserve paragraph breaks
    result = []
    current_paragraph = []

    for line in cleaned_lines:
        # Check if this seems like a new thought/sentence
        if current_paragraph and (
            line[0].isupper() or
            line.startswith('"') or
            any(current_paragraph[-1].endswith(p) for p in ['.', '!', '?', ':', ';'])
        ):
            # End current paragraph
            if current_paragraph:
                result.append(' '.join(current_paragraph))
                current_paragraph = []

        current_paragraph.append(line)

    # Don't forget the last paragraph
    if current_paragraph:
        result.append(' '.join(current_paragraph))

    return '\n\n'.join(result)

def process_all_transcripts(input_dir: str, output_file: str):
    """
    Process all VTT files in the input directory and create a single transcript.
    """
    # Find all VTT files
    vtt_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.vtt'):
                vtt_files.append(os.path.join(root, file))

    # Sort files by their numbers
    vtt_files.sort(key=extract_number)

    print(f"Found {len(vtt_files)} VTT files to process")

    # Process each file
    all_content = []

    all_content.append("# TAC-8 Complete Video Transcript")
    all_content.append("\n> **Note**: This is the complete, stitched transcript from all 133 VTT files of TAC-8, the culminating module of Tactical Agentic Coding.")
    all_content.append("\n> **Processing Date**: Generated from raw VTT caption files")
    all_content.append("\n> **Module**: TAC-8 - The Complete System: Production Deployment at Scale")
    all_content.append("\n---\n")

    for i, vtt_file in enumerate(vtt_files):
        filename = os.path.basename(vtt_file)
        file_number = extract_number(vtt_file)

        print(f"Processing {i+1}/{len(vtt_files)}: {filename}")

        try:
            with open(vtt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            cleaned_content = clean_vtt_content(content)

            if cleaned_content.strip():
                # Add section header for each video segment
                all_content.append(f"\n## Video Segment {file_number[0]}")
                if file_number[1] > 0:
                    all_content.append(f"*(Part {file_number[1] + 1})*")
                all_content.append("")
                all_content.append(cleaned_content)
                all_content.append("\n---")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    # Write the complete transcript
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_content))

    print(f"\nComplete transcript saved to: {output_file}")
    print(f"Total size: {len(''.join(all_content))} characters")

def main():
    """Main execution function."""
    input_dir = "/Users/kvnkishore/Downloads/tac transcripts/tac-8/"
    output_file = "/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/tac-8-deep-dive/COMPLETE-TRANSCRIPT.md"

    print("TAC-8 Transcript Processor")
    print("=" * 50)
    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_file}")
    print("=" * 50)

    process_all_transcripts(input_dir, output_file)

    print("\n✅ Processing complete!")
    print("\nNext steps:")
    print("1. Review COMPLETE-TRANSCRIPT.md for accuracy")
    print("2. Analyze TAC-8 codebase")
    print("3. Generate comprehensive analysis documents")

if __name__ == "__main__":
    main()
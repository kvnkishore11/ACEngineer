#!/usr/bin/env python3
"""
Process VTT subtitle files and extract clean transcript
"""
import os
import re
from pathlib import Path

def clean_vtt_content(content):
    """Extract clean text from VTT content, removing timestamps and metadata"""
    lines = content.split('\n')
    clean_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Skip WEBVTT header and metadata
        if line.startswith('WEBVTT') or line.startswith('X-'):
            i += 1
            continue

        # Skip subtitle numbers (just digits)
        if line.isdigit():
            i += 1
            continue

        # Skip timestamp lines (contain -->)
        if '-->' in line:
            i += 1
            continue

        # This is actual subtitle text
        clean_lines.append(line)
        i += 1

    return ' '.join(clean_lines)

def process_all_vtt_files():
    """Process all VTT files in order"""
    vtt_dir = Path("/Users/kvnkishore/Downloads/tac-1 vtt")

    # Collect all VTT files
    vtt_files = []

    # Process numbered files in order
    for i in range(44):  # 0 to 43
        file_path = vtt_dir / f"{i}.vtt"
        if file_path.exists():
            vtt_files.append((i, file_path))

    # Also check for special files
    special_files = ["0 - 1.vtt"]
    for special in special_files:
        file_path = vtt_dir / special
        if file_path.exists():
            # Insert at beginning since it's "0 - 1"
            vtt_files.insert(1, (-0.5, file_path))  # Insert after 0.vtt

    # Sort by order
    vtt_files.sort(key=lambda x: x[0])

    # Process each file
    full_transcript = []

    for order, file_path in vtt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                clean_text = clean_vtt_content(content)
                if clean_text:
                    # Add file marker for reference
                    file_name = file_path.name
                    full_transcript.append(f"\n\n[Video Segment: {file_name}]\n")
                    full_transcript.append(clean_text)
                    print(f"Processed: {file_name}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return ''.join(full_transcript)

if __name__ == "__main__":
    print("Processing VTT files...")
    transcript = process_all_vtt_files()

    # Save the complete transcript
    output_file = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/tac-1-deep-dive/COMPLETE-TRANSCRIPT.md")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# TAC-1 Complete Video Transcript\n\n")
        f.write("This is the complete transcript from all TAC-1 video segments, processed and cleaned from VTT subtitle files.\n\n")
        f.write("---\n\n")
        f.write(transcript)

    print(f"\nTranscript saved to: {output_file}")
    print(f"Total length: {len(transcript)} characters")
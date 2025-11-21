#!/usr/bin/env python3
"""
Process TAC-7 VTT transcripts and stitch them together
"""

import os
import re
from pathlib import Path

def parse_vtt(file_path):
    """Parse a VTT file and extract the text content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove WEBVTT header
    content = re.sub(r'^WEBVTT\s*\n', '', content, flags=re.MULTILINE)

    # Parse blocks
    blocks = re.split(r'\n\n+', content)
    text_parts = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            # Skip the index line and timestamp line
            # Extract only the text content
            text_content = ' '.join(lines[2:])
            if text_content:
                text_parts.append(text_content)

    return ' '.join(text_parts)

def get_file_order(filename):
    """Extract numeric order from filename for sorting"""
    # Handle "0 - 1.vtt" format
    if ' - ' in filename:
        return float(filename.split(' - ')[0])
    # Handle "0.vtt" format
    elif filename.replace('.vtt', '').replace('.', '').isdigit():
        return float(filename.replace('.vtt', ''))
    else:
        return 999  # Put non-numeric files at the end

def main():
    transcript_dir = Path('/Users/kvnkishore/Downloads/tac transcripts/tac-7')
    output_dir = Path('/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/tac-7-deep-dive')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all VTT files
    vtt_files = sorted([f for f in os.listdir(transcript_dir) if f.endswith('.vtt')],
                      key=get_file_order)

    # Identify TAC-7 specific files (lesson 7)
    # Based on our search, these files contain TAC-7 content
    tac7_files = []

    # First, let's check which files are actually TAC-7
    for vtt_file in vtt_files:
        file_path = transcript_dir / vtt_file
        content = parse_vtt(file_path)

        # Check if this is TAC-7 content
        if 'lesson seven' in content.lower() or 'lesson 7' in content.lower():
            print(f"TAC-7 content found in: {vtt_file}")
            tac7_files.append(vtt_file)
        elif any(marker in content.lower() for marker in ['issue structured', 'iso workflow', 'outloop']):
            print(f"TAC-7 related content in: {vtt_file}")
            tac7_files.append(vtt_file)

    # Process all files but mark TAC-6 vs TAC-7
    full_transcript = []
    tac7_transcript = []

    print("\nProcessing all transcript files...")
    for vtt_file in vtt_files:
        file_path = transcript_dir / vtt_file
        content = parse_vtt(file_path)

        # Add file marker
        if vtt_file in tac7_files:
            section_header = f"\n\n[FILE: {vtt_file} - TAC-7]\n"
        else:
            section_header = f"\n\n[FILE: {vtt_file} - TAC-6]\n"

        full_transcript.append(section_header + content)

        if vtt_file in tac7_files:
            tac7_transcript.append(section_header + content)

    # Save complete transcript
    complete_path = output_dir / 'COMPLETE-TRANSCRIPT.md'
    with open(complete_path, 'w') as f:
        f.write("# TAC-6 and TAC-7 Complete Transcript\n\n")
        f.write("This document contains the full stitched transcript from all VTT files.\n")
        f.write("Files are marked as either TAC-6 or TAC-7 content.\n\n")
        f.write("---\n")
        f.write('\n'.join(full_transcript))

    print(f"\nComplete transcript saved to: {complete_path}")

    # Save TAC-7 only transcript
    if tac7_transcript:
        tac7_path = output_dir / 'TAC7-ONLY-TRANSCRIPT.md'
        with open(tac7_path, 'w') as f:
            f.write("# TAC-7 Only Transcript\n\n")
            f.write("This document contains only the TAC-7 specific content.\n\n")
            f.write("---\n")
            f.write('\n'.join(tac7_transcript))
        print(f"TAC-7 only transcript saved to: {tac7_path}")

    print(f"\nTotal files processed: {len(vtt_files)}")
    print(f"TAC-7 specific files: {len(tac7_files)}")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Process TAC-3 VTT transcripts and stitch them into a complete transcript
"""

import os
import re
from pathlib import Path
from typing import List, Dict

def parse_vtt(file_path: str) -> List[Dict]:
    """Parse a VTT file and extract text content with timestamps"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines to get individual subtitle blocks
    blocks = content.split('\n\n')

    transcripts = []
    for block in blocks:
        if '-->' in block:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                # Find the timestamp line
                timestamp_line = None
                text_lines = []

                for line in lines:
                    if '-->' in line:
                        timestamp_line = line
                    elif line and not line.isdigit() and line != 'WEBVTT':
                        text_lines.append(line)

                if timestamp_line and text_lines:
                    # Extract start time
                    match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})', timestamp_line)
                    if match:
                        start_time = match.group(1)
                        text = ' '.join(text_lines)
                        transcripts.append({
                            'time': start_time,
                            'text': text.strip()
                        })

    return transcripts

def natural_sort_key(path):
    """Natural sorting key to handle files like '0.vtt', '0 - 1.vtt', '1.vtt' correctly"""
    name = os.path.basename(path)
    # Extract numbers from filename
    parts = re.split(r'(\d+)', name)
    # Convert numeric parts to integers for proper sorting
    return [int(part) if part.isdigit() else part for part in parts]

def main():
    # Directory containing VTT files
    vtt_dir = Path('/Users/kvnkishore/Downloads/tac transcripts/tac-3')
    output_dir = Path('/Users/kvnkishore/WebstormProjects/AgenticEngineer/output/tac-3-deep-dive')

    # Get all VTT files sorted naturally
    vtt_files = sorted(vtt_dir.glob('*.vtt'), key=lambda p: natural_sort_key(str(p)))

    print(f"Found {len(vtt_files)} VTT files")

    # Process all files and collect transcripts
    all_transcripts = []
    file_boundaries = []

    for i, vtt_file in enumerate(vtt_files):
        print(f"Processing {vtt_file.name}...")
        transcripts = parse_vtt(vtt_file)
        if transcripts:
            # Add file boundary marker
            file_boundaries.append({
                'file': vtt_file.name,
                'start_index': len(all_transcripts),
                'transcript_count': len(transcripts)
            })
            all_transcripts.extend(transcripts)

    # Stitch transcripts together, maintaining paragraph structure
    complete_transcript = []
    complete_transcript.append("# TAC-3 Complete Transcript\n")
    complete_transcript.append("*Compiled from all TAC-3 video transcripts*\n")
    complete_transcript.append(f"*Total segments: {len(all_transcripts)}*\n")
    complete_transcript.append(f"*Total files processed: {len(vtt_files)}*\n\n")

    complete_transcript.append("---\n\n")

    current_file_idx = 0
    current_paragraph = []
    last_time = None

    for idx, segment in enumerate(all_transcripts):
        # Check if we're starting a new file
        if current_file_idx < len(file_boundaries) - 1:
            next_boundary = file_boundaries[current_file_idx + 1]
            if idx >= next_boundary['start_index']:
                # We've moved to a new file
                if current_paragraph:
                    complete_transcript.append(' '.join(current_paragraph))
                    complete_transcript.append('\n\n')
                    current_paragraph = []

                current_file_idx += 1
                current_file = file_boundaries[current_file_idx]['file']
                complete_transcript.append(f"## Video Segment: {current_file}\n\n")
                last_time = None
        elif idx == 0:
            # First file
            current_file = file_boundaries[0]['file']
            complete_transcript.append(f"## Video Segment: {current_file}\n\n")

        # Add timestamp if significant time gap (more than 10 seconds)
        if last_time:
            last_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(last_time.split(':'))))
            current_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(segment['time'].split(':'))))

            if current_seconds - last_seconds > 10:
                # Significant gap, start new paragraph
                if current_paragraph:
                    complete_transcript.append(' '.join(current_paragraph))
                    complete_transcript.append('\n\n')
                complete_transcript.append(f"[{segment['time']}]\n\n")
                current_paragraph = [segment['text']]
            else:
                # Continue current paragraph
                current_paragraph.append(segment['text'])
        else:
            # First segment of file
            complete_transcript.append(f"[{segment['time']}]\n\n")
            current_paragraph = [segment['text']]

        last_time = segment['time']

    # Add any remaining text
    if current_paragraph:
        complete_transcript.append(' '.join(current_paragraph))
        complete_transcript.append('\n\n')

    # Save complete transcript
    output_file = output_dir / 'COMPLETE-TRANSCRIPT.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(complete_transcript))

    print(f"\nComplete transcript saved to: {output_file}")
    print(f"Total text segments: {len(all_transcripts)}")
    print(f"Files processed: {len(vtt_files)}")

    # Also create a file listing for reference
    listing_file = output_dir / 'VIDEO-FILE-LIST.md'
    with open(listing_file, 'w', encoding='utf-8') as f:
        f.write("# TAC-3 Video File List\n\n")
        f.write("Files processed in order:\n\n")
        for i, vtt_file in enumerate(vtt_files):
            boundary = file_boundaries[i] if i < len(file_boundaries) else None
            if boundary:
                f.write(f"{i+1}. **{vtt_file.name}** - {boundary['transcript_count']} segments\n")
            else:
                f.write(f"{i+1}. **{vtt_file.name}**\n")

    print(f"File listing saved to: {listing_file}")

if __name__ == "__main__":
    main()
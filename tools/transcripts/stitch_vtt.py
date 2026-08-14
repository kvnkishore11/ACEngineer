#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Stitch a directory of per-chapter WebVTT files into one readable transcript.

This replaces two near-identical scripts that differed only in hardcoded paths
and in how much cleanup they did:

- `process_transcripts.py` (repo root) had the better cleaner — it stripped the
  WEBVTT header, `Kind:`/`Language:` lines, timing lines, standalone timestamps
  and cue-identifier numbers, then repaired the ` .` / ` ,` / ` ?` / ` !` spacing
  artifacts that fall out of joining cue lines.
- `scripts/process_tac7_transcripts.py` had a feature the other lacked: it
  tagged each chapter by searching its text for marker phrases, because that
  folder held two lessons' chapters mixed together and needed splitting.

Both are kept. The cleaner is always applied; the tagging is opt-in.

    # the common case
    uv run tools/transcripts/stitch_vtt.py transcripts/tac-7-zte-secret-of-agentic-engineering \
        catalog/courses/tac-7-zte-secret-of-agentic-engineering/transcript/tac-7-zte-secret-of-agentic-engineering.md

    # a folder holding two lessons: tag chapters, and also write a filtered file
    uv run tools/transcripts/stitch_vtt.py transcripts/tac-7-... out.md \
        --marker "lesson seven" --marker "iso workflow" \
        --tagged-output tac7-only.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TIMESTAMP_ONLY = re.compile(r"^\d{2}:\d{2}:\d{2}[.,]\d{3}$")
CUE_ID = re.compile(r"^\d+$")
HEADER = ("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE")


def clean_vtt(content: str) -> str:
    """Strip VTT scaffolding and return only spoken text.

    Line-based rather than block-based on purpose: block-based parsing assumes
    every cue is exactly `id / timing / text`, and silently drops multi-line or
    id-less cues.
    """
    out: list[str] = []
    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(HEADER):
            continue
        if "-->" in line:
            continue
        if TIMESTAMP_ONLY.match(line):
            continue
        if CUE_ID.match(line):
            continue
        out.append(line)

    text = " ".join(out)
    text = re.sub(r"<[^>]+>", "", text)          # inline cue tags, e.g. <v Speaker>
    text = re.sub(r"\s+", " ", text)
    for bad, good in ((" .", "."), (" ,", ","), (" ?", "?"), (" !", "!")):
        text = text.replace(bad, good)
    return text.strip()


def file_order(path: Path) -> tuple[float, int]:
    """Sort `0.vtt`, `1.vtt`, ... with `N - 1.vtt` duplicates right after `N`."""
    name = path.stem
    is_dup = " - " in name
    head = name.split(" - ")[0] if is_dup else name
    try:
        num = float(head)
    except ValueError:
        return (float("inf"), 1 if is_dup else 0)
    return (num, 1 if is_dup else 0)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Stitch per-chapter VTT files into one transcript.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("source", type=Path, help="directory holding the .vtt files")
    ap.add_argument("output", type=Path, help="markdown file to write")
    ap.add_argument("--title", help="H1 for the output (default: source dir name)")
    ap.add_argument(
        "--marker",
        action="append",
        default=[],
        metavar="PHRASE",
        help="case-insensitive phrase marking a chapter as tagged; repeatable",
    )
    ap.add_argument(
        "--tagged-output",
        type=Path,
        help="also write a file containing only the tagged chapters",
    )
    ap.add_argument(
        "--no-section-headers",
        action="store_true",
        help="emit continuous prose without per-chapter headers",
    )
    args = ap.parse_args()

    if not args.source.is_dir():
        print(f"error: {args.source} is not a directory", file=sys.stderr)
        return 1

    vtts = sorted(args.source.glob("*.vtt"), key=file_order)
    if not vtts:
        print(f"error: no .vtt files in {args.source}", file=sys.stderr)
        return 1

    title = args.title or args.source.name
    markers = [m.lower() for m in args.marker]

    all_parts: list[str] = []
    tagged_parts: list[str] = []
    tagged_count = 0

    for i, vtt in enumerate(vtts, start=1):
        try:
            text = clean_vtt(vtt.read_text(encoding="utf-8", errors="replace"))
        except OSError as exc:
            print(f"error reading {vtt.name}: {exc}", file=sys.stderr)
            return 1
        if not text:
            continue

        is_tagged = bool(markers) and any(m in text.lower() for m in markers)
        if is_tagged:
            tagged_count += 1

        if args.no_section_headers:
            block = text
        else:
            suffix = " [tagged]" if is_tagged else ""
            block = f"\n## Section {i} — `{vtt.name}`{suffix}\n\n{text}\n"

        all_parts.append(block)
        if is_tagged:
            tagged_parts.append(block)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    header = f"# {title}\n\nStitched from {len(vtts)} chapter transcripts.\n\n---\n"
    args.output.write_text(header + "\n".join(all_parts) + "\n")
    words = sum(len(p.split()) for p in all_parts)
    print(f"wrote {args.output} — {len(vtts)} chapters, ~{words:,} words")

    if args.tagged_output:
        if not markers:
            print(
                "error: --tagged-output requires at least one --marker",
                file=sys.stderr,
            )
            return 1
        args.tagged_output.parent.mkdir(parents=True, exist_ok=True)
        args.tagged_output.write_text(
            f"# {title} — tagged chapters only\n\n"
            f"Chapters matching: {', '.join(args.marker)}\n\n---\n"
            + "\n".join(tagged_parts)
            + "\n"
        )
        print(f"wrote {args.tagged_output} — {tagged_count} tagged chapters")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

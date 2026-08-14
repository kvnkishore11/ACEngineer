#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Organize MA downloads: move metadata, convert VTT → clean md/txt, symlink finals."""
from __future__ import annotations
import json, re, shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
# Operates on a fresh member-asset download staging tree. The original
# member-assets/ staging tree has been folded into the catalog; its provenance
# (MANIFEST.json, SUMMARY.json, download.log) lives here.
ROOT = REPO_ROOT / "catalog" / "_source" / "ma-download"
FINAL = REPO_ROOT / "media" / "final"
TRANSCRIPTS_ROOT = ROOT / "transcripts"  # unified flat transcripts

ASSETS = [
    ("ma-1-ceo-agents", "CEO Agents"),
    ("ma-2-lead-agents", "Multi-Team Agentic Coding"),
    ("ma-3-ui-agents", "Infinite UI Agents"),
    ("ma-4-verifier-agent", "The Pi Verifier Agent"),
]

TS_RE = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}")
TAG_RE = re.compile(r"<[^>]+>")
NOTE_RE = re.compile(r"^NOTE\b")


def vtt_to_text(vtt: str) -> tuple[str, str]:
    """Return (plain_txt, timestamped_md)."""
    lines = []
    md = []
    last = None
    current_ts = None
    for raw in vtt.splitlines():
        line = raw.strip("\ufeff").strip()
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if line.isdigit():
            continue
        if NOTE_RE.match(line):
            continue
        if TS_RE.match(line):
            current_ts = line.split("-->")[0].strip().split(".")[0]
            continue
        # drop alignment/position metadata style lines
        if "align:" in line or "position:" in line:
            continue
        text = TAG_RE.sub("", line).replace("&nbsp;", " ").strip()
        if not text:
            continue
        if text == last:
            continue  # auto-subs often duplicate
        last = text
        lines.append(text)
        if current_ts:
            md.append(f"**[{current_ts}]** {text}")
        else:
            md.append(text)
    plain = "\n".join(lines)
    # paragraph-ish: join short lines
    paras = []
    buf = []
    for t in lines:
        buf.append(t)
        if t.endswith((".", "?", "!", "…")) or len(buf) >= 4:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    plain_para = "\n\n".join(paras)
    md_body = "\n\n".join(md)
    return plain_para, md_body


def pick_vtt(video_dir: Path) -> Path | None:
    cands = sorted(video_dir.glob("*.vtt"))
    if not cands:
        return None
    # prefer en manual over auto
    for p in cands:
        name = p.name.lower()
        if "en" in name and "auto" not in name:
            return p
    for p in cands:
        if "en" in p.name.lower():
            return p
    return cands[0]


def main():
    summary = []
    for key, title in ASSETS:
        d = ROOT / key
        vdir = d / "video"
        tdir = d / "transcripts"
        mdir = d / "meta"
        tdir.mkdir(exist_ok=True)
        mdir.mkdir(exist_ok=True)

        mp4s = list(vdir.glob("*.mp4"))
        if not mp4s:
            summary.append({"key": key, "ok": False, "error": "no mp4"})
            continue
        mp4 = mp4s[0]
        # rename to clean final name if needed
        clean = vdir / f"{key}.mp4"
        if mp4 != clean:
            if clean.exists():
                clean.unlink()
            mp4.rename(clean)
            mp4 = clean

        # move side-car metadata from video/ into meta/
        for pattern in ("*.info.json", "*.description", "*.webp", "*.jpg", "*.png", "*.json"):
            for f in vdir.glob(pattern):
                if f.suffix == ".json" and f.name.endswith(".info.json"):
                    dest = mdir / f"{key}.info.json"
                elif f.suffix == ".description":
                    dest = mdir / f"{key}.description"
                else:
                    dest = mdir / f.name
                shutil.move(str(f), str(dest))

        vtt = pick_vtt(vdir)
        # also check if vtt already elsewhere
        if not vtt:
            vtt = pick_vtt(tdir) or pick_vtt(d)
        plain = md = ""
        if vtt:
            dest_vtt = tdir / f"{key}.en.vtt"
            if vtt != dest_vtt:
                shutil.copy2(vtt, dest_vtt)
                # move originals into meta for provenance
                if vtt.parent == vdir:
                    shutil.move(str(vtt), str(mdir / vtt.name))
            # leftover vtts
            for extra in vdir.glob("*.vtt"):
                shutil.move(str(extra), str(mdir / extra.name))
            plain, md = vtt_to_text(dest_vtt.read_text(encoding="utf-8", errors="replace"))
            (tdir / f"{key}.txt").write_text(plain + "\n", encoding="utf-8")
            (tdir / f"{key}.md").write_text(
                f"# {title}\n\n**Key:** `{key}`\n\n**Source:** YouTube (see meta)\n\n---\n\n{md}\n",
                encoding="utf-8",
            )
            # unified flat copies
            shutil.copy2(tdir / f"{key}.txt", TRANSCRIPTS_ROOT / f"{key}.txt")
            shutil.copy2(tdir / f"{key}.md", TRANSCRIPTS_ROOT / f"{key}.md")
            shutil.copy2(dest_vtt, TRANSCRIPTS_ROOT / f"{key}.en.vtt")

        # hardlink or copy into media/final/ (os.link - no extra disk)
        final_mp4 = FINAL / f"{key}.mp4"
        if final_mp4.exists() or final_mp4.is_symlink():
            final_mp4.unlink()
        try:
            import os
            os.link(mp4, final_mp4)
            link_mode = "hardlink"
        except OSError:
            shutil.copy2(mp4, final_mp4)
            link_mode = "copy"

        size_mb = mp4.stat().st_size / (1024 * 1024)
        summary.append({
            "key": key,
            "title": title,
            "ok": True,
            "video": str(mp4),
            "final_videos": str(final_mp4),
            "size_mb": round(size_mb, 1),
            "transcript_txt": str(tdir / f"{key}.txt") if plain else None,
            "link_mode": link_mode,
            "chars": len(plain),
        })

    (ROOT / "SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    readme = ["# Member Assets (MA)", "", "Unified home for the 4 Agentic Horizon **member exclusive** assets.", "",
              "Videos sourced from IndyDevDan public YouTube (mapped via title/description ↔ site cards).",
              "Codebases already live under `../agentic-horizon-extras/`.", "",
              "| Key | Title | Video | Transcripts |",
              "|-----|-------|-------|-------------|"]
    for s in summary:
        if s.get("ok"):
            readme.append(f"| `{s['key']}` | {s['title']} | `{s['key']}/video/{s['key']}.mp4` ({s['size_mb']} MB) | `{s['key']}/transcripts/` |")
        else:
            readme.append(f"| `{s['key']}` | — | MISSING | — |")
    readme += ["", "## Layout", "```", "catalog/_source/ma-download/",
               "  MANIFEST.json          # youtube ↔ asset mapping",
               "  transcripts/           # flat copies of all transcripts",
               "  ma-N-*/",
               "    video/ma-N-*.mp4",
               "    transcripts/{.vtt,.md,.txt}",
               "    meta/                # yt-dlp info, description, thumbs",
               "```", "",
               "Also hardlinked/copied into `media/final/ma-*.mp4` next to TAC/AH finals.", ""]
    (ROOT / "README.md").write_text("\n".join(readme), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

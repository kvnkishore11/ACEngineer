#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["youtube-transcript-api"]
# ///
"""Build one catalog/youtube/ video folder in course-catalog format.

Layout (mirrors catalog/courses/<key>/):
  youtube/<key>/
    video/<key>.mp4          # optional download (720p preferred)
    transcript/<key>.{md,txt,vtt}
    metadata/lesson.json
    metadata/lesson.html
    metadata/course-page.html  # alias of lesson.html
    metadata/video-info.json   # yt-dlp metadata dump
    README.md

Usage:
  python3 build_video_folder.py --batch _batch_1.json [--download-video]
  python3 build_video_folder.py --id VQy50fuxI34 --order 53 --title "..." ...
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT / "catalog" / "youtube"
PY = sys.executable
YTDLP = "yt-dlp"


def slug_safe(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[’'`]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:60].rstrip("-") or "video"


def fetch_transcript(video_id: str) -> list[dict]:
    """Return list of {text, start, duration} segments."""
    code = f"""
from youtube_transcript_api import YouTubeTranscriptApi
import json
vid = {video_id!r}
try:
    # new API
    api = YouTubeTranscriptApi()
    fetched = api.fetch(vid, languages=['en', 'en-US', 'en-GB'])
    segs = [{{'text': s.text, 'start': s.start, 'duration': s.duration}} for s in fetched]
    print(json.dumps(segs))
except Exception as e1:
    try:
        # legacy
        segs = YouTubeTranscriptApi.get_transcript(vid, languages=['en', 'en-US', 'en-GB'])
        print(json.dumps(segs))
    except Exception as e2:
        try:
            segs = YouTubeTranscriptApi.get_transcript(vid)
            print(json.dumps(segs))
        except Exception as e3:
            print(json.dumps({{'error': str(e1) + ' | ' + str(e2) + ' | ' + str(e3)}}))
"""
    r = subprocess.run([PY, "-c", code], capture_output=True, text=True, timeout=120)
    out = (r.stdout or "").strip()
    if not out:
        return []
    data = json.loads(out)
    if isinstance(data, dict) and data.get("error"):
        print(f"  transcript error: {data['error']}", file=sys.stderr)
        return []
    return data if isinstance(data, list) else []


def fmt_ts(sec: float) -> str:
    sec = max(0, int(sec))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def segs_to_txt(segs: list[dict]) -> str:
    return " ".join(s.get("text", "").replace("\n", " ").strip() for s in segs)


def segs_to_md(title: str, segs: list[dict], meta: dict) -> str:
    lines = [f"# {title}", ""]
    if meta.get("upload_date"):
        lines.append(f"- Upload: {meta['upload_date']}")
    if meta.get("url"):
        lines.append(f"- URL: {meta['url']}")
    if meta.get("duration_sec"):
        lines.append(f"- Duration: {fmt_ts(meta['duration_sec'])}")
    lines.append("")
    lines.append("## Transcript")
    lines.append("")
    # paragraph-ish grouping every ~40s
    bucket = []
    bucket_start = None
    out_paras = []
    for s in segs:
        t = s.get("text", "").replace("\n", " ").strip()
        if not t:
            continue
        start = float(s.get("start", 0))
        if bucket_start is None:
            bucket_start = start
        bucket.append(t)
        if start - bucket_start >= 40:
            out_paras.append((bucket_start, " ".join(bucket)))
            bucket = []
            bucket_start = None
    if bucket:
        out_paras.append((bucket_start or 0, " ".join(bucket)))
    for start, text in out_paras:
        lines.append(f"**[{fmt_ts(start)}]** {text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def segs_to_vtt(segs: list[dict]) -> str:
    lines = ["WEBVTT", ""]
    for i, s in enumerate(segs, 1):
        start = float(s.get("start", 0))
        dur = float(s.get("duration", 2) or 2)
        end = start + max(dur, 0.5)
        text = s.get("text", "").replace("\n", " ").strip()
        if not text:
            continue
        lines.append(str(i))
        lines.append(f"{_vtt_ts(start)} --> {_vtt_ts(end)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def _vtt_ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def fetch_ytdlp_info(url: str, out_json: Path) -> dict:
    cmd = [
        YTDLP,
        "--skip-download",
        "--no-warnings",
        "--print-json",
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if r.returncode != 0 or not r.stdout.strip():
        print(f"  yt-dlp meta fail: {r.stderr[:300]}", file=sys.stderr)
        return {}
    # last JSON line if multiple
    lines = [ln for ln in r.stdout.splitlines() if ln.strip().startswith("{")]
    if not lines:
        return {}
    info = json.loads(lines[-1])
    # slim dump
    slim = {
        k: info.get(k)
        for k in [
            "id",
            "title",
            "description",
            "upload_date",
            "duration",
            "view_count",
            "like_count",
            "channel",
            "channel_id",
            "channel_url",
            "thumbnail",
            "thumbnails",
            "tags",
            "categories",
            "webpage_url",
            "fulltitle",
        ]
        if k in info
    }
    out_json.write_text(json.dumps(slim, indent=2, ensure_ascii=False))
    return slim


def download_video(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1_000_000:
        print(f"  video exists ({dest.stat().st_size} bytes)")
        return True
    # 720p max preferred
    cmd = [
        YTDLP,
        "-f",
        "bv*[height<=720]+ba/b[height<=720]/best[height<=720]/best",
        "--merge-output-format",
        "mp4",
        "-o",
        str(dest),
        "--no-playlist",
        "--no-warnings",
        url,
    ]
    print(f"  downloading video → {dest.name}")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    if r.returncode != 0:
        print(f"  download fail: {r.stderr[-500:]}", file=sys.stderr)
        return False
    return dest.exists()


def render_lesson_html(meta: dict, info: dict) -> str:
    title = html.escape(meta.get("title") or "")
    desc = html.escape((info.get("description") or "")[:4000]).replace("\n", "<br>\n")
    thumb = html.escape(info.get("thumbnail") or f"https://i.ytimg.com/vi/{meta['id']}/hqdefault.jpg")
    url = html.escape(meta.get("url") or "")
    tags = ", ".join(html.escape(t) for t in (info.get("tags") or [])[:20])
    views = info.get("view_count")
    likes = info.get("like_count")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — IndyDevDan YouTube</title>
  <style>
    :root {{ color-scheme: light dark; --bg: #0f1115; --fg: #e8eaed; --muted: #9aa0a6; --card: #1a1d24; --accent: #7c9cff; }}
    body {{ margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif; background: var(--bg); color: var(--fg); line-height: 1.55; }}
    main {{ max-width: 880px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
    .badge {{ display: inline-block; font-size: .75rem; letter-spacing: .04em; text-transform: uppercase; color: var(--accent); border: 1px solid color-mix(in oklab, var(--accent) 50%, transparent); padding: .2rem .55rem; border-radius: 999px; }}
    h1 {{ font-size: 1.65rem; line-height: 1.25; margin: .75rem 0 1rem; }}
    .meta {{ color: var(--muted); font-size: .95rem; display: grid; gap: .25rem; margin-bottom: 1.25rem; }}
    .thumb {{ width: 100%; border-radius: 12px; background: var(--card); aspect-ratio: 16/9; object-fit: cover; }}
    .card {{ background: var(--card); border-radius: 12px; padding: 1.1rem 1.2rem; margin-top: 1.25rem; }}
    a {{ color: var(--accent); }}
    .desc {{ font-size: .95rem; color: #d0d4db; }}
  </style>
</head>
<body>
<main>
  <span class="badge">YouTube · yt-{meta.get('order', 0):02d}</span>
  <h1>{title}</h1>
  <div class="meta">
    <div>Channel: IndyDevDan</div>
    <div>Upload: {html.escape(str(meta.get('upload_date') or ''))}</div>
    <div>Duration: {html.escape(fmt_ts(meta.get('duration_sec') or 0))}</div>
    <div>Views: {views if views is not None else '—'} · Likes: {likes if likes is not None else '—'}</div>
    <div>Video ID: <code>{html.escape(meta.get('id') or '')}</code></div>
    <div><a href="{url}">{url}</a></div>
  </div>
  <img class="thumb" src="{thumb}" alt="thumbnail" />
  <div class="card">
    <h2 style="margin-top:0;font-size:1.05rem">Description</h2>
    <div class="desc">{desc or '<em>No description</em>'}</div>
  </div>
  {f'<div class="card"><h2 style="margin-top:0;font-size:1.05rem">Tags</h2><div class="desc">{tags}</div></div>' if tags else ''}
  <div class="card">
    <h2 style="margin-top:0;font-size:1.05rem">Local assets</h2>
    <div class="desc">
      Transcript: <code>../transcript/</code><br>
      Video: <code>../video/</code><br>
      Metadata JSON: <code>lesson.json</code>
    </div>
  </div>
</main>
</body>
</html>
"""


def build_one(v: dict, do_download_video: bool = False) -> dict:
    key = v["key"]
    folder = ROOT / key
    video_dir = folder / "video"
    tx_dir = folder / "transcript"
    meta_dir = folder / "metadata"
    for d in (video_dir, tx_dir, meta_dir):
        d.mkdir(parents=True, exist_ok=True)

    status = {
        "key": key,
        "id": v["id"],
        "transcript": False,
        "metadata": False,
        "video": False,
        "errors": [],
    }
    print(f"\n== {key} ({v['id']}) ==")

    # metadata via yt-dlp
    info = {}
    try:
        info = fetch_ytdlp_info(v["url"], meta_dir / "video-info.json")
        status["metadata"] = bool(info)
        if info.get("title"):
            v["title"] = info["title"]
        if info.get("duration"):
            v["duration_sec"] = int(info["duration"])
        if info.get("upload_date"):
            v["upload_date"] = info["upload_date"]
    except Exception as e:
        status["errors"].append(f"meta: {e}")
        print(f"  meta exception: {e}", file=sys.stderr)

    lesson = {
        "key": key,
        "short_key": f"yt-{v['order']:02d}",
        "title": v["title"],
        "course": "YOUTUBE",
        "slug": v["slug"],
        "url": v["url"],
        "video_id": v["id"],
        "order": v["order"],
        "upload_date": v.get("upload_date"),
        "duration_sec": v.get("duration_sec"),
        "channel": "IndyDevDan",
        "channel_url": "https://www.youtube.com/@IndyDevDan",
        "video_file": f"{key}.mp4",
        "source": "youtube",
        "layout": "mirrors IndyDevDan course lesson folders",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    (meta_dir / "lesson.json").write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n")

    html_body = render_lesson_html(lesson, info)
    (meta_dir / "lesson.html").write_text(html_body)
    (meta_dir / "course-page.html").write_text(html_body)

    # transcript
    segs = []
    try:
        segs = fetch_transcript(v["id"])
    except Exception as e:
        status["errors"].append(f"transcript: {e}")
        print(f"  transcript exception: {e}", file=sys.stderr)

    if segs:
        (tx_dir / f"{key}.txt").write_text(segs_to_txt(segs) + "\n")
        (tx_dir / f"{key}.md").write_text(segs_to_md(v["title"], segs, lesson))
        (tx_dir / f"{key}.vtt").write_text(segs_to_vtt(segs))
        status["transcript"] = True
        print(f"  transcript: {len(segs)} segments")
    else:
        (tx_dir / f"{key}.txt").write_text(
            f"[no transcript available for {v['id']}]\n"
        )
        (tx_dir / f"{key}.md").write_text(
            f"# {v['title']}\n\nNo transcript available for `{v['id']}`.\n"
        )
        print("  transcript: MISSING")

    # video
    video_path = video_dir / f"{key}.mp4"
    if do_download_video:
        try:
            status["video"] = download_video(v["url"], video_path)
        except Exception as e:
            status["errors"].append(f"video: {e}")
            print(f"  video exception: {e}", file=sys.stderr)
    else:
        # placeholder note
        note = video_dir / "SOURCE.md"
        note.write_text(
            textwrap.dedent(
                f"""\
                # Video source

                - URL: {v['url']}
                - ID: {v['id']}
                - Local mp4: download with:

                ```bash
                yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \\
                  -o "{key}.mp4" "{v['url']}"
                ```

                Or re-run: `python3 build_video_folder.py --batch … --download-video`
                """
            )
        )
        status["video"] = video_path.exists() and video_path.stat().st_size > 1_000_000

    # README
    (folder / "README.md").write_text(
        textwrap.dedent(
            f"""\
            # {key} — {v['title']}

            Course: **YOUTUBE** · order {v['order']} · upload {v.get('upload_date')}

            | Asset | Path |
            |-------|------|
            | Video | `video/{key}.mp4` (or `video/SOURCE.md` if not downloaded) |
            | Transcript | `transcript/` (vtt + md/txt when available) |
            | Lesson HTML | `metadata/lesson.html` |
            | Course page HTML | `metadata/course-page.html` (alias) |
            | Metadata JSON | `metadata/lesson.json` |
            | yt-dlp info | `metadata/video-info.json` |

            Source: {v['url']}
            """
        )
    )

    (folder / "STATUS.json").write_text(json.dumps(status, indent=2) + "\n")
    print(f"  done: tx={status['transcript']} meta={status['metadata']} video={status['video']}")
    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", help="JSON array of video dicts")
    ap.add_argument("--inventory", default=str(ROOT / "_inventory.json"))
    ap.add_argument("--keys", nargs="*", help="Only these keys")
    ap.add_argument("--download-video", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    if args.batch:
        videos = json.loads(Path(args.batch).read_text())
    else:
        inv = json.loads(Path(args.inventory).read_text())
        videos = inv["videos"]

    if args.keys:
        videos = [v for v in videos if v["key"] in args.keys or v["id"] in args.keys]
    if args.limit:
        videos = videos[: args.limit]

    results = []
    for v in videos:
        try:
            results.append(build_one(v, do_download_video=args.download_video))
        except Exception as e:
            print(f"FATAL {v.get('key')}: {e}", file=sys.stderr)
            results.append({"key": v.get("key"), "errors": [str(e)]})

    summary = {
        "processed": len(results),
        "ok_transcript": sum(1 for r in results if r.get("transcript")),
        "ok_metadata": sum(1 for r in results if r.get("metadata")),
        "ok_video": sum(1 for r in results if r.get("video")),
        "results": results,
    }
    out = ROOT / f"_batch_summary_{datetime.utcnow().strftime('%H%M%S')}.json"
    out.write_text(json.dumps(summary, indent=2))
    print("\n=== SUMMARY ===")
    print(json.dumps({k: summary[k] for k in summary if k != "results"}, indent=2))
    print("wrote", out)
    # non-zero if any missing transcript
    if summary["ok_transcript"] < summary["processed"]:
        sys.exit(2)


if __name__ == "__main__":
    main()

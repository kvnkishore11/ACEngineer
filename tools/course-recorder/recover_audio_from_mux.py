#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import time
import urllib.request
from pathlib import Path
from typing import Any

from recorder_common import ensure_output_dir, get_lesson, safe_name, vtt_duration, write_json
from record_lesson_cdp import CDP, find_cdp_base, runtime_eval


def page_tabs(base: str) -> list[dict[str, Any]]:
    return [p for p in json.loads(urllib.request.urlopen(base + "/json/list", timeout=3).read().decode()) if p.get("type") == "page"]


def run(cmd: list[str], timeout: int | None = None) -> None:
    subprocess.run(cmd, check=True, timeout=timeout)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)
    ], text=True).strip()
    return float(out)


def infer_video_start_offset(out_dir: Path) -> float:
    """Return lesson-time elapsed before the first encoded CDP frame."""
    meta_path = out_dir / "recording.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text())
            value = meta.get("last_status", {}).get("currentTime")
            if isinstance(value, (int, float)) and value > 0:
                return float(value)
        except Exception:
            pass
    log_path = out_dir / "recording.log"
    if not log_path.exists():
        return 0.0
    last_value = 0.0
    for line in log_path.read_text(errors="ignore").splitlines():
        if not line.startswith("PREP {"):
            continue
        try:
            value = json.loads(line[5:]).get("currentTime")
            if isinstance(value, (int, float)) and value > 0:
                last_value = float(value)
        except Exception:
            continue
    return last_value


def get_audio_uri(cdp: CDP, lesson: dict[str, Any], expected: float | None) -> dict[str, Any]:
    cdp.cmd("Page.navigate", {"url": lesson["url"]}, timeout=10)
    time.sleep(7)
    # Some course pages lazy-create the real player only after scroll. Keep one tab, scroll it; do not open tab spam.
    for y in (0, 800, 1600, 2400, 3200, 4200):
        runtime_eval(cdp, f"window.scrollTo(0,{y}); null", timeout=5)
        time.sleep(0.7)

    expected_js = "null" if expected is None else repr(float(expected))
    info = runtime_eval(cdp, f"""
(async () => {{
  try {{
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const expected = {expected_js};
    const players = Array.from(document.querySelectorAll('mux-player'));
    const seen = [];
    for (const [i,p] of players.entries()) {{
      try {{ p.scrollIntoView({{block:'center', inline:'center'}}); }} catch(e) {{}}
      await sleep(1000);
      const m = p.media || p;
      seen.push({{
        i,
        duration: m && Number.isFinite(m.duration) ? m.duration : null,
        hasToken: !!p.getAttribute('playback-token'),
        playbackId: p.getAttribute('playback-id')
      }});
    }}
    let ranked = players.map((p, i) => {{
      const m = p.media || p;
      const d = m && Number.isFinite(m.duration) ? m.duration : 0;
      const score = expected ? Math.abs(d - expected) : -d;
      return {{p, i, duration: d, score}};
    }}).filter(x => x.p.getAttribute('playback-id') && x.p.getAttribute('playback-token'));
    ranked.sort((a,b) => a.score - b.score);
    const chosen = ranked[0];
    if (!chosen) return {{ok:false, reason:'no mux-player with playback id/token', url:location.href, title:document.title, players:seen}};
    if (expected && Math.abs(chosen.duration - expected) > 180) {{
      return {{ok:false, reason:'duration mismatch', expected, chosenDuration:chosen.duration, url:location.href, title:document.title, players:seen}};
    }}
    const p = chosen.p;
    const pid = p.getAttribute('playback-id');
    const token = p.getAttribute('playback-token');
    const masterUrl = `https://stream.mux.com/${{pid}}.m3u8?token=${{encodeURIComponent(token)}}`;
    const master = await (await fetch(masterUrl)).text();
    const audioLines = master.split('\\n').filter(l => l.startsWith('#EXT-X-MEDIA') && l.includes('TYPE=AUDIO'));
    if (!audioLines.length) return {{ok:false, reason:'no audio media line', chosenDuration:chosen.duration, players:seen}};
    const line = audioLines[0];
    const uri = (line.match(/URI="([^\"]+)"/) || [])[1];
    if (!uri) return {{ok:false, reason:'audio line missing URI', chosenDuration:chosen.duration, players:seen}};
    const audioText = await (await fetch(uri)).text();
    return {{
      ok: true,
      url: location.href,
      title: document.title,
      playerIndex: chosen.i,
      chosenDuration: chosen.duration,
      expected,
      playbackId: pid,
      audioUri: uri,
      audioDrm: audioText.includes('#EXT-X-KEY') || audioText.includes('SAMPLE-AES') || audioText.includes('urn:uuid'),
      audioSegments: audioText.split('\\n').filter(l => l && !l.startsWith('#')).length,
      players: seen
    }};
  }} catch (e) {{
    return {{ok:false, reason:'exception', message:String(e), stack:e && e.stack ? String(e.stack).slice(0,1200) : null, url:location.href, title:document.title}};
  }}
}})()
""", timeout=45)
    if not info or not info.get("ok"):
        raise SystemExit(f"Failed to get audio URI for {lesson['key']}: {json.dumps(info, indent=2)}")
    if info.get("audioDrm"):
        raise SystemExit(f"Audio playlist is DRM-protected for {lesson['key']}; cannot direct-recover audio")
    return info


def main() -> int:
    ap = argparse.ArgumentParser(description="Recover clear Mux audio and mux it with an existing silent CDP video.")
    ap.add_argument("lesson", help="lesson key/order/slug, e.g. tac-2")
    ap.add_argument("--port", type=int, default=9223)
    ap.add_argument("--video-suffix", default="cdp-15fps")
    ap.add_argument("--output-suffix", default="cdp-15fps-audio-fixed")
    ap.add_argument("--sync-offset", type=float, default=None, help="seconds of source audio to trim/advance to match the first CDP video frame; defaults to recording PREP currentTime")
    ap.add_argument("--no-auto-sync", action="store_true", help="do not infer sync offset from recording.json/recording.log")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    lesson = get_lesson(args.lesson)
    out_dir = ensure_output_dir(lesson)
    expected = vtt_duration(lesson.get("transcript", ""))
    video_in = out_dir / safe_name(lesson, args.video_suffix)
    if not video_in.exists():
        raise SystemExit(f"Missing source video: {video_in}")
    out = out_dir / safe_name(lesson, args.output_suffix)
    audio = out_dir / f"{lesson['key']}-{lesson['slug']}-mux-audio.m4a"
    tmp_audio = audio.with_suffix(".recording.m4a")
    tmp_out = out.with_suffix(".recording.mp4")
    if out.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing output: {out}")
    for p in (tmp_audio, tmp_out):
        if p.exists():
            p.unlink()

    base = find_cdp_base(args.port)
    tabs = page_tabs(base)
    if not tabs:
        raise SystemExit("No CDP page tabs available")
    cdp = CDP(tabs[0]["webSocketDebuggerUrl"])
    cdp.cmd("Runtime.enable")
    cdp.cmd("Page.enable")

    info = get_audio_uri(cdp, lesson, expected)
    print(f"{lesson['key']}: player duration {info['chosenDuration']:.1f}s, audio segments {info['audioSegments']}", flush=True)

    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
        "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-i", info["audioUri"],
        "-vn", "-c:a", "copy", "-movflags", "+faststart", str(tmp_audio),
    ], timeout=1800)
    tmp_audio.rename(audio)
    audio_duration = probe_duration(audio)
    if expected and abs(audio_duration - expected) > 180:
        raise SystemExit(f"Recovered audio duration mismatch: audio={audio_duration:.1f}s expected={expected:.1f}s")

    sync_offset = args.sync_offset
    if sync_offset is None:
        sync_offset = 0.0 if args.no_auto_sync else infer_video_start_offset(out_dir)
    sync_offset = max(0.0, float(sync_offset or 0.0))

    mux_cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(video_in), "-i", str(audio),
    ]
    if sync_offset > 0.001:
        mux_cmd += [
            "-filter_complex", f"[1:a]atrim=start={sync_offset:.6f},asetpts=PTS-STARTPTS[a]",
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(tmp_out),
        ]
    else:
        mux_cmd += [
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(tmp_out),
        ]

    run(mux_cmd, timeout=1800)
    tmp_out.rename(out)
    write_json(out_dir / f"{lesson['key']}-{lesson['slug']}-{args.output_suffix}-sync.json", {
        "lesson": lesson["key"],
        "video_input": str(video_in),
        "audio_input": str(audio),
        "output": str(out),
        "sync_offset_seconds": sync_offset,
        "sync_action": "trim_audio_start_to_match_first_cdp_video_frame" if sync_offset > 0.001 else "none",
        "audio_duration_seconds": audio_duration,
        "expected_duration_seconds": expected,
    })
    print(f"sync_offset_seconds={sync_offset:.6f}")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

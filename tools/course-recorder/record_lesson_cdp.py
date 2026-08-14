#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from recorder_common import get_lesson, ensure_output_dir, safe_name, vtt_duration, write_json


def http_json(url: str, timeout: float = 2.0) -> Any:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode())


def find_cdp_base(port: int) -> str:
    for host in ("localhost", "127.0.0.1"):
        base = f"http://{host}:{port}"
        try:
            http_json(base + "/json/version")
            return base
        except Exception:
            continue
    raise SystemExit(f"No Chrome CDP endpoint on port {port}. Launch/authorize Chrome with --remote-debugging-port={port}.")


def open_new_tab(base: str, url: str) -> dict[str, Any]:
    # Chrome expects PUT for /json/new on recent versions.
    req = urllib.request.Request(base + "/json/new?" + urllib.parse.quote(url, safe=':/?=&'), method="PUT")
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode())


def pick_target(base: str, url: str | None, attach_existing: bool) -> dict[str, Any]:
    targets = http_json(base + "/json/list")
    pages = [t for t in targets if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
    if attach_existing:
        if url:
            for p in pages:
                if url in p.get("url", ""):
                    return p
        if pages:
            return pages[0]
        raise SystemExit("No page targets available to attach.")
    if not url:
        raise SystemExit("URL required unless --attach-existing is used.")
    return open_new_tab(base, url)


class CDP:
    def __init__(self, ws_url: str):
        u = urllib.parse.urlparse(ws_url)
        if u.scheme != "ws":
            raise SystemExit(f"Only ws:// CDP is supported, got {ws_url}")
        self.host = u.hostname or "localhost"
        self.port = u.port or 80
        self.path = (u.path or "/") + (("?" + u.query) if u.query else "")
        self.sock = socket.create_connection((self.host, self.port), timeout=5)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        resp = self.sock.recv(4096)
        if b"101" not in resp.split(b"\r\n", 1)[0]:
            raise SystemExit(f"WebSocket handshake failed: {resp[:200]!r}")
        self.next_id = 1
        self.pending: dict[int, dict[str, Any]] = {}

    def _send_frame(self, payload: bytes) -> None:
        # client frames must be masked
        header = bytearray([0x81])
        n = len(payload)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack("!H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack("!Q", n)
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(header) + mask + masked)

    def _recv_frame(self) -> dict[str, Any]:
        h = self.sock.recv(2)
        if len(h) < 2:
            raise EOFError("websocket closed")
        b1, b2 = h
        opcode = b1 & 0x0F
        masked = bool(b2 & 0x80)
        n = b2 & 0x7F
        if n == 126:
            n = struct.unpack("!H", self._read_exact(2))[0]
        elif n == 127:
            n = struct.unpack("!Q", self._read_exact(8))[0]
        mask = self._read_exact(4) if masked else b""
        payload = self._read_exact(n)
        if masked:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        if opcode == 8:
            raise EOFError("websocket close frame")
        if opcode == 9:  # ping
            return self._recv_frame()
        return json.loads(payload.decode())

    def _read_exact(self, n: int) -> bytes:
        out = bytearray()
        while len(out) < n:
            chunk = self.sock.recv(n - len(out))
            if not chunk:
                raise EOFError("socket closed")
            out += chunk
        return bytes(out)

    def cmd(self, method: str, params: dict[str, Any] | None = None, timeout: float = 10.0) -> dict[str, Any]:
        msg_id = self.next_id
        self.next_id += 1
        self._send_frame(json.dumps({"id": msg_id, "method": method, "params": params or {}}).encode())
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = self._recv_frame()
            if msg.get("id") == msg_id:
                if "error" in msg:
                    raise RuntimeError(f"CDP {method} error: {msg['error']}")
                return msg.get("result", {})
        raise TimeoutError(method)

    def send_no_wait(self, method: str, params: dict[str, Any] | None = None) -> int:
        msg_id = self.next_id
        self.next_id += 1
        self._send_frame(json.dumps({"id": msg_id, "method": method, "params": params or {}}).encode())
        return msg_id


def runtime_eval(cdp: CDP, expression: str, timeout: float = 10.0) -> Any:
    res = cdp.cmd("Runtime.evaluate", {
        "expression": expression,
        "awaitPromise": True,
        "returnByValue": True,
        "userGesture": True,
    }, timeout=timeout)
    return res.get("result", {}).get("value")


PREP_JS = r"""
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const player = document.querySelector('mux-player') || document.querySelector('video');
  if (!player) return { ok:false, reason:'no player/video element', title:document.title, url:location.href };
  const media = (typeof player.play === 'function') ? player : (player.media || player);
  try { player.scrollIntoView({block:'center', inline:'center'}); } catch(e) {}
  try {
    const style = document.createElement('style');
    style.id = 'hermes-recorder-expanded-player-style';
    style.textContent = `
      body { overflow: hidden !important; background: #000 !important; }
      mux-player.video-player, mux-player, video {
        position: fixed !important;
        inset: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        max-width: none !important;
        max-height: none !important;
        z-index: 2147483647 !important;
        background: #000 !important;
        pointer-events: none !important;
      }
    `;
    document.getElementById(style.id)?.remove();
    document.head.appendChild(style);
  } catch(e) {}
  try { await (player.requestFullscreen ? player.requestFullscreen() : document.documentElement.requestFullscreen()); } catch(e) {}
  try { media.currentTime = 0; } catch(e) {}
  try { media.muted = __HERMES_MUTE_PLAYBACK__; media.volume = __HERMES_MUTE_PLAYBACK__ ? 0 : 1; } catch(e) {}
  try { await media.play(); } catch(e) { try { player.click(); await sleep(300); await media.play(); } catch(e2) {} }
  try {
    window.__hermesPauseGuard && clearInterval(window.__hermesPauseGuard);
    window.__hermesPauseGuard = setInterval(() => {
      try {
        const p = document.querySelector('mux-player') || document.querySelector('video');
        const m = p && ((typeof p.play === 'function') ? p : (p.media || p));
        if (m && !m.ended) {
          m.muted = __HERMES_MUTE_PLAYBACK__;
          m.volume = __HERMES_MUTE_PLAYBACK__ ? 0 : 1;
          if (m.paused) m.play().catch(() => {});
        }
      } catch(e) {}
    }, 500);
  } catch(e) {}
  await sleep(1500);
  return {
    ok: !!media && !media.paused,
    reason: media ? null : 'no media',
    title: document.title,
    url: location.href,
    currentTime: media ? media.currentTime : null,
    duration: media ? media.duration : null,
    paused: media ? media.paused : null,
    readyState: media ? media.readyState : null,
    fullscreen: !!document.fullscreenElement,
    width: innerWidth,
    height: innerHeight
  };
})()
"""

STATUS_JS = r"""
(() => {
  const player = document.querySelector('mux-player') || document.querySelector('video');
  const media = player && ((typeof player.play === 'function') ? player : (player.media || player));
  return {
    title: document.title,
    url: location.href,
    currentTime: media ? media.currentTime : null,
    duration: media ? media.duration : null,
    paused: media ? media.paused : null,
    readyState: media ? media.readyState : null,
    fullscreen: !!document.fullscreenElement,
    width: innerWidth,
    height: innerHeight
  };
})()
"""


def capture_jpeg(cdp: CDP, quality: int) -> bytes:
    res = cdp.cmd("Page.captureScreenshot", {"format": "jpeg", "quality": quality, "fromSurface": True, "captureBeyondViewport": False}, timeout=10)
    return base64.b64decode(res["data"])


def start_ffmpeg(out_tmp: Path, fps: int, audio_device_index: str | None, width: int = 1920, height: int = 1080) -> subprocess.Popen:
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
        "-f", "image2pipe", "-framerate", str(fps), "-vcodec", "mjpeg", "-i", "pipe:0",
    ]
    if audio_device_index is not None:
        cmd += ["-f", "avfoundation", "-i", f":{audio_device_index}"]
    cmd += [
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-r", str(fps),
    ]
    if audio_device_index is not None:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-movflags", "+faststart", str(out_tmp)]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> int:
    ap = argparse.ArgumentParser(description="Record AgenticEngineer lesson via Chrome CDP fullscreen tab capture + optional BlackHole audio")
    ap.add_argument("lesson", help="lesson key/order/slug, e.g. tac-1 or 1")
    ap.add_argument("--port", type=int, default=9223)
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--quality", type=int, default=88)
    ap.add_argument("--seconds", type=float, default=None, help="record duration; omit to use transcript duration + padding")
    ap.add_argument("--audio-device-index", default="2", help="avfoundation audio device index for BlackHole 2ch; use 'none' for video-only")
    ap.add_argument("--attach-existing", action="store_true", help="attach to existing active tab instead of opening URL")
    ap.add_argument("--suffix", default=None)
    args = ap.parse_args()

    lesson = get_lesson(args.lesson)
    out_dir = ensure_output_dir(lesson)
    audio_idx = None if args.audio_device_index.lower() == "none" else args.audio_device_index
    fps = args.fps
    suffix = args.suffix or f"cdp-{fps}fps"
    final = out_dir / safe_name(lesson, suffix)
    tmp = out_dir / (final.stem + ".recording.mp4")
    log_path = out_dir / "recording.log"
    meta_path = out_dir / "recording.json"
    preflight = out_dir / "preflight-frame.jpg"
    if final.exists():
        raise SystemExit(f"Refusing to overwrite existing final file: {final}")
    if tmp.exists():
        tmp.unlink()

    duration = args.seconds
    expected = vtt_duration(lesson.get("transcript", ""))
    if duration is None:
        if expected is None:
            raise SystemExit("--seconds required because transcript duration unavailable")
        duration = expected + 8

    with log_path.open("a") as log:
        def logline(s: str) -> None:
            print(s)
            log.write(s + "\n")
            log.flush()

        base = find_cdp_base(args.port)
        target = pick_target(base, None if args.attach_existing else lesson["url"], args.attach_existing)
        logline(f"CDP target: {target.get('title')} {target.get('url')}")
        cdp = CDP(target["webSocketDebuggerUrl"])
        cdp.cmd("Page.enable")
        cdp.cmd("Runtime.enable")
        cdp.cmd("Page.bringToFront")
        cdp.cmd("Emulation.setIdleOverride", {"isUserActive": True, "isScreenUnlocked": True})
        if target.get("url") != lesson["url"]:
            cdp.cmd("Page.navigate", {"url": lesson["url"]}, timeout=10)
            time.sleep(4)
        time.sleep(2)
        prep_js = PREP_JS.replace("__HERMES_MUTE_PLAYBACK__", "true" if audio_idx is None else "false")
        prep = runtime_eval(cdp, prep_js, timeout=20)
        logline("PREP " + json.dumps(prep, sort_keys=True))
        if not prep or not prep.get("ok"):
            logline("PREP_FAILED: player not confirmed playing. User may need to login/click play/fullscreen.")
            return 2
        jpeg = capture_jpeg(cdp, args.quality)
        preflight.write_bytes(jpeg)
        logline(f"Wrote preflight frame: {preflight}")
        cdp.cmd("Page.startScreencast", {"format": "jpeg", "quality": args.quality, "maxWidth": 1920, "maxHeight": 1080, "everyNthFrame": 1}, timeout=10)
        cdp.sock.settimeout(0.05)
        latest_jpeg = jpeg
        ff = start_ffmpeg(tmp, fps=fps, audio_device_index=audio_idx)
        started = time.time()
        next_tick = started
        next_monitor = started + 30
        frames = 0
        last_status = prep
        try:
            while True:
                now = time.time()
                if now - started >= duration:
                    break
                try:
                    msg = cdp._recv_frame()
                    if msg.get("method") == "Page.screencastFrame":
                        params = msg.get("params", {})
                        latest_jpeg = base64.b64decode(params.get("data", ""))
                        sid = params.get("sessionId")
                        if sid is not None:
                            cdp.send_no_wait("Page.screencastFrameAck", {"sessionId": sid})
                except socket.timeout:
                    pass
                except Exception as e:
                    logline(f"WARN screencast receive failed at {now-started:.1f}s: {e}")
                now = time.time()
                if now >= next_tick:
                    assert ff.stdin is not None
                    ff.stdin.write(latest_jpeg)
                    frames += 1
                    next_tick += 1.0 / fps
                if now >= next_monitor:
                    try:
                        logline(f"STATUS t={now-started:.1f}s frames={frames} player={json.dumps(last_status, sort_keys=True)}")
                        monitor = out_dir / "monitor-latest.jpg"
                        monitor.write_bytes(latest_jpeg)
                    except Exception as e:
                        logline(f"ERROR status/screen verification failed: {e}")
                        raise
                    next_monitor += 30
        finally:
            try:
                cdp.send_no_wait("Page.stopScreencast", {})
            except Exception:
                pass
            try:
                if ff.stdin:
                    ff.stdin.close()
            except Exception:
                pass
            stderr = b""
            try:
                stderr = ff.stderr.read() if ff.stderr else b""
            except Exception:
                pass
            rc = ff.wait(timeout=120)
            logline(f"FFMPEG_EXIT rc={rc} frames={frames} stderr_tail={stderr.decode(errors='ignore')[-4000:]}")
        if rc != 0:
            return rc
        final_tmp_hash = hashlib.sha256(tmp.read_bytes()).hexdigest() if tmp.exists() else None
        tmp.rename(final)
        meta = {
            "lesson": lesson,
            "output": str(final),
            "started_at": started,
            "duration_requested_s": duration,
            "fps": fps,
            "quality": args.quality,
            "audio_device_index": audio_idx,
            "frames_written": frames,
            "preflight_frame": str(preflight),
            "last_status": last_status,
            "sha256": final_tmp_hash,
        }
        write_json(meta_path, meta)
        logline(f"DONE output={final}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

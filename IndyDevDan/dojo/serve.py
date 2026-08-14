#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""The Agentic Dojo — local web UI.

  python3 serve.py           start on http://127.0.0.1:4242 and open the browser
  python3 serve.py --port N  pick a port
  python3 serve.py --no-open don't launch the browser

Zero dependencies. The server only binds to localhost and only touches files
inside lessons/. All checking still runs the same check.py closed loops.
"""
from __future__ import annotations

import difflib
import json
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import dojo  # sibling module: lesson discovery, progress log, pristine paths

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web" / "index.html"
PROTECTED = {"check.py", "hints.md", "README.md"}  # visible, never editable
MAX_FILE = 512 * 1024


# ---------- helpers ----------

def get_lesson(nn: str) -> Path:
    hits = [p for p in dojo.lessons() if p.name.startswith(nn.zfill(2) + "-")]
    if not hits:
        raise FileNotFoundError(f"no lesson {nn!r}")
    return hits[0]


def lesson_files(lesson: Path) -> list[dict]:
    """Every text file in the lesson (minus solution/), mission files first."""
    out = []
    for p in sorted(lesson.rglob("*")):
        if not p.is_file() or "solution" in p.parts or "__pycache__" in p.parts:
            continue
        if p.name in ("hints.md", "README.md"):  # hints stay progressive; the brief has its own tab
            continue
        rel = str(p.relative_to(lesson))
        if p.stat().st_size > MAX_FILE:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        editable = p.name not in PROTECTED
        mission = editable and ("____" in text or "YOUR TURN" in text)
        out.append({
            "path": rel,
            "content": text,
            "mission": mission,
            "editable": editable,
            "blanks": text.count("____") if editable else 0,
        })
    out.sort(key=lambda f: (not f["mission"], f["path"]))
    return out


def hints_for(lesson: Path) -> list[str]:
    text = (lesson / "hints.md").read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)
    return ["## " + p.strip() for p in parts if p.strip() and p.lstrip().lower().startswith("hint")]


def status_payload() -> dict:
    items = []
    for p in dojo.lessons():
        res = dojo.last_result(p.name)
        title_line = ""
        readme = p / "README.md"
        if readme.exists():
            for line in readme.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    title_line = line[2:].strip()
                    break
        items.append({
            "name": p.name,
            "nn": p.name[:2],
            "title": title_line,
            "state": "passed" if (res and res["pass"]) else ("failing" if res else "fresh"),
            "blanks": dojo.blanks_left(p),
        })
    nxt = next((i["name"] for i in items if i["state"] != "passed"), None)
    return {"lessons": items, "next": nxt,
            "passed": sum(1 for i in items if i["state"] == "passed"), "total": len(items)}


def safe_lesson_path(name: str, rel: str) -> Path:
    lesson = get_lesson(name[:2])  # find() exits on bad input; names come from our own listing
    target = (lesson / rel).resolve()
    if not str(target).startswith(str(lesson.resolve()) + "/"):
        raise PermissionError("path escapes the lesson directory")
    if target.name in PROTECTED or "solution" in target.relative_to(lesson).parts:
        raise PermissionError("that file is part of the dojo itself — not editable")
    return target


def run_check(lesson: Path) -> dict:
    proc = subprocess.run([sys.executable, str(lesson / "check.py")], cwd=lesson,
                          capture_output=True, text=True, timeout=180)
    passed = proc.returncode == 0
    dojo.log_event({"kind": "check", "lesson": lesson.name, "pass": passed})
    return {"pass": passed, "output": (proc.stdout + proc.stderr).strip()}


def diff_payload(lesson: Path) -> str:
    sol = lesson / "solution"
    chunks = []
    for spath in sorted(p for p in sol.rglob("*") if p.is_file()):
        rel = spath.relative_to(sol)
        yours = lesson / rel
        a = yours.read_text(encoding="utf-8").splitlines(keepends=True) if yours.exists() else []
        b = spath.read_text(encoding="utf-8").splitlines(keepends=True)
        chunks.extend(difflib.unified_diff(a, b, fromfile=f"yours/{rel}", tofile=f"solution/{rel}"))
    return "".join(chunks) or "your files match the reference solution."


def reset_lesson(lesson: Path) -> None:
    src = dojo.PRISTINE / lesson.name
    if not src.exists():
        raise FileNotFoundError(f"no pristine snapshot for {lesson.name}")
    for spath in src.rglob("*"):
        if spath.is_file():
            dest = lesson / spath.relative_to(src)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(spath, dest)
    dojo.log_event({"kind": "reset", "lesson": lesson.name})


# ---------- http ----------

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep the terminal quiet
        pass

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200) -> None:
        self._send(code, json.dumps(obj).encode(), "application/json")

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        try:
            if self.path in ("/", "/index.html"):
                self._send(200, WEB.read_bytes(), "text/html; charset=utf-8")
            elif self.path == "/api/status":
                self._json(status_payload())
            elif m := re.fullmatch(r"/api/lesson/(\d\d)", self.path):
                lesson = get_lesson(m.group(1))
                self._json({
                    "name": lesson.name,
                    "readme": (lesson / "README.md").read_text(encoding="utf-8"),
                    "files": lesson_files(lesson),
                    "hints_total": len(hints_for(lesson)),
                    "hints_seen": dojo.hints_seen(lesson.name),
                })
            elif m := re.fullmatch(r"/api/hint/(\d\d)/(\d+)", self.path):
                lesson = get_lesson(m.group(1))
                hints = hints_for(lesson)
                k = int(m.group(2))
                if not 1 <= k <= len(hints):
                    self._json({"error": f"hints go 1..{len(hints)}"}, 400)
                    return
                dojo.log_event({"kind": "hint", "lesson": lesson.name, "k": k})
                self._json({"hint": hints[k - 1], "k": k, "total": len(hints)})
            elif m := re.fullmatch(r"/api/diff/(\d\d)", self.path):
                self._json({"diff": diff_payload(get_lesson(m.group(1)))})
            else:
                self._json({"error": "not found"}, 404)
        except Exception as e:  # surface, never crash the server
            self._json({"error": str(e)}, 500)

    def do_POST(self):
        try:
            if m := re.fullmatch(r"/api/check/(\d\d)", self.path):
                self._json(run_check(get_lesson(m.group(1))))
            elif self.path == "/api/save":
                body = self._body()
                target = safe_lesson_path(body["lesson"], body["path"])
                target.write_text(body["content"], encoding="utf-8")
                self._json({"ok": True, "blanks": body["content"].count("____")})
            elif m := re.fullmatch(r"/api/reset/(\d\d)", self.path):
                lesson = get_lesson(m.group(1))
                reset_lesson(lesson)
                self._json({"ok": True, "files": lesson_files(lesson)})
            else:
                self._json({"error": "not found"}, 404)
        except PermissionError as e:
            self._json({"error": str(e)}, 403)
        except Exception as e:
            self._json({"error": str(e)}, 500)


def main() -> None:
    port = 4242
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"
    print(f"The Agentic Dojo · {url}  (ctrl-c to stop)")
    if "--no-open" not in sys.argv:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nleaving the dojo — progress is saved in progress.jsonl")


if __name__ == "__main__":
    main()

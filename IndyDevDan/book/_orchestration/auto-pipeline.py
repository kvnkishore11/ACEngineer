#!/usr/bin/env python3
"""Watch extracts and auto-launch chapters when STATUS.md appears. Max 2 concurrent chapters."""
from __future__ import annotations
import json, os, subprocess, time
from pathlib import Path

ROOT = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer")
BOOK = ROOT / "IndyDevDan/book"
PY = BOOK / "_orchestration/fanout-lesson.py"
LOG = BOOK / "_logs/auto-pipeline.log"

def lessons():
    d = json.loads((BOOK / "data/curriculum.json").read_text())
    return [L for L in d["lessons"] if L["key"] != "tac-1-hello-agentic-coding"]

def status_done(key: str) -> bool:
    p = BOOK / f"_extracts/{key}/STATUS.md"
    return p.exists() and "DONE" in p.read_text()

def chapter_done(L: dict) -> bool:
    # stem-based path
    course = L["course"]
    vol = {"TAC": "vol-1-tac", "AH": "vol-2-ah", "MA": "vol-3-ma"}[course]
    order = int(L["order"])
    import re
    m = re.match(r"^(?:tac|ah|ma)-\d+-(.+)$", L["key"])
    slug = m.group(1) if m else L["key"]
    stem = f"{order:02d}-{slug}"
    return (BOOK / vol / f"{stem}.html").exists() and (BOOK / vol / f"{stem}-STATUS.md").exists()

def log(msg: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = time.strftime("%H:%M:%S") + " " + msg
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def launch_chapter(key: str) -> subprocess.Popen:
    env = {
        "HOME": str(Path.home()),
        "USER": os.environ.get("USER", "kvnkishore"),
        "PATH": "/Users/kvnkishore/.nvm/versions/node/v20.19.5/bin:/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin",
    }
    out = open(BOOK / f"_logs/{key}-chapter-run.log", "w")
    return subprocess.Popen(
        ["python3", str(PY), "chapter", key],
        cwd=str(ROOT),
        env=env,
        stdout=out,
        stderr=subprocess.STDOUT,
    )

def main(max_hours: float = 8.0, poll: float = 45.0):
    deadline = time.time() + max_hours * 3600
    running: dict[str, subprocess.Popen] = {}
    launched = set()
    log("auto-pipeline start")
    while time.time() < deadline:
        # reap
        for k, p in list(running.items()):
            if p.poll() is not None:
                log(f"chapter finished {k} exit={p.returncode}")
                del running[k]
        # launch ready
        for L in lessons():
            key = L["key"]
            if key in launched or key in running:
                continue
            if chapter_done(L):
                launched.add(key)
                continue
            if status_done(key) and len(running) < 2:
                log(f"launch chapter {key}")
                running[key] = launch_chapter(key)
                launched.add(key)
        # progress
        done_ex = sum(1 for L in lessons() if status_done(L["key"]))
        done_ch = sum(1 for L in lessons() if chapter_done(L))
        log(f"progress extracts={done_ex}/17 chapters={done_ch}/17 running_chapters={list(running)}")
        if done_ch >= 17 and not running:
            log("ALL CHAPTERS DONE")
            return
        time.sleep(poll)
    log("deadline reached")

if __name__ == "__main__":
    main()

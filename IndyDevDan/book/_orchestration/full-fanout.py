#!/usr/bin/env python3
"""Full fan-out controller: extracts + chapters for all pending lessons.
Models: Claude Opus extracts (EXTRACT_MODEL=opus), Codex gpt-5.6-sol xhigh chapters.
Concurrency: max 3 extracts + max 3 chapters.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path

ROOT = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer")
BOOK = ROOT / "IndyDevDan/book"
PY = BOOK / "_orchestration/fanout-lesson.py"
LOG = BOOK / "_logs/full-fanout.log"


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = time.strftime("%H:%M:%S") + " " + msg
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def lessons() -> list[dict]:
    d = json.loads((BOOK / "data/curriculum.json").read_text())
    return [L for L in d["lessons"] if L["key"] != "tac-1-hello-agentic-coding"]


def vol_stem(L: dict) -> tuple[str, str]:
    course = L["course"]
    vol = {"TAC": "vol-1-tac", "AH": "vol-2-ah", "MA": "vol-3-ma"}[course]
    order = int(L["order"])
    m = re.match(r"^(?:tac|ah|ma)-\d+-(.+)$", L["key"])
    slug = m.group(1) if m else L["key"]
    return vol, f"{order:02d}-{slug}"


def extract_done(key: str) -> bool:
    p = BOOK / f"_extracts/{key}/STATUS.md"
    return p.exists() and "DONE" in p.read_text(errors="ignore")


def chapter_done(L: dict) -> bool:
    vol, stem = vol_stem(L)
    html = BOOK / vol / f"{stem}.html"
    if not html.exists() or html.stat().st_size < 50_000:
        return False
    return (BOOK / vol / f"{stem}-STATUS.md").exists() or (BOOK / vol / f"{stem}.STATUS.md").exists()


def env_for(mode: str) -> dict[str, str]:
    path = "/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin"
    if mode == "chapter":
        path = "/Users/kvnkishore/.nvm/versions/node/v20.19.5/bin:" + path
    return {
        "HOME": str(Path.home()),
        "USER": os.environ.get("USER", "kvnkishore"),
        "PATH": path,
        "EXTRACT_MODEL": os.environ.get("EXTRACT_MODEL", "opus"),
    }


def already_running(mode: str, key: str) -> bool:
    try:
        out = subprocess.check_output(["ps", "-ax", "-o", "command="], text=True)
    except Exception:
        return False
    return f"{mode} {key}" in out


def launch(mode: str, key: str) -> subprocess.Popen:
    logf = open(BOOK / f"_logs/{key}-{mode}-run.log", "a")
    return subprocess.Popen(
        ["python3", str(PY), mode, key],
        cwd=str(ROOT),
        env=env_for(mode),
        stdout=logf,
        stderr=subprocess.STDOUT,
    )


def main(max_hours: float = 16.0, poll: float = 45.0, max_ex: int = 3, max_ch: int = 3) -> None:
    deadline = time.time() + max_hours * 3600
    running_ex: dict[str, subprocess.Popen] = {}
    running_ch: dict[str, subprocess.Popen] = {}
    fail_counts: dict[str, int] = {}
    model = os.environ.get("EXTRACT_MODEL", "opus")
    log(f"full-fanout start max_ex={max_ex} max_ch={max_ch} EXTRACT_MODEL={model}")

    while time.time() < deadline:
        for k, p in list(running_ex.items()):
            if p.poll() is not None:
                rc = p.returncode
                log(f"finished extract {k} exit={rc}")
                if rc not in (0, None):
                    fail_counts[k] = fail_counts.get(k, 0) + 1
                    log(f"fail_count {k}={fail_counts[k]}")
                del running_ex[k]

        for k, p in list(running_ch.items()):
            if p.poll() is not None:
                rc = p.returncode
                log(f"finished chapter {k} exit={rc}")
                if rc not in (0, None):
                    fail_counts[f"ch:{k}"] = fail_counts.get(f"ch:{k}", 0) + 1
                    log(f"fail_count ch:{k}={fail_counts[f'ch:{k}']}")
                del running_ch[k]

        Ls = lessons()

        for L in Ls:
            key = L["key"]
            if extract_done(key) or key in running_ex or already_running("extract", key):
                continue
            if fail_counts.get(key, 0) >= 2:
                continue
            if len(running_ex) >= max_ex:
                break
            log(f"launch extract {key}")
            running_ex[key] = launch("extract", key)

        for L in Ls:
            key = L["key"]
            if chapter_done(L) or key in running_ch or already_running("chapter", key):
                continue
            if not extract_done(key):
                continue
            if fail_counts.get(f"ch:{key}", 0) >= 2:
                continue
            if len(running_ch) >= max_ch:
                break
            log(f"launch chapter {key}")
            running_ch[key] = launch("chapter", key)

        ex_done = sum(1 for L in Ls if extract_done(L["key"]))
        ch_done = sum(1 for L in Ls if chapter_done(L))
        log(
            f"progress extracts={ex_done}/17 (+tac1) chapters={ch_done}/17 "
            f"run_ex={list(running_ex)} run_ch={list(running_ch)}"
        )
        if ch_done >= 17 and not running_ex and not running_ch:
            log("ALL 17 DONE")
            return
        time.sleep(poll)

    log("deadline")


if __name__ == "__main__":
    main()

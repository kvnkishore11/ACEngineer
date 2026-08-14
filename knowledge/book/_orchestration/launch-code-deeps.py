#!/usr/bin/env python3
"""Launch code deep-dive pages via Codex for selected lessons."""
from __future__ import annotations
import json, os, subprocess
from pathlib import Path

ROOT = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer")
BOOK = ROOT / "IndyDevDan/book"
ORCH = BOOK / "_orchestration"
TPL = (ORCH / "TEMPLATE-CODE-DEEP.md").read_text()

def resolve_codebase(L: dict) -> Path | None:
    key = L["key"]
    cb = L.get("codebase") or ""
    p2 = ROOT / "IndyDevDan" / key / "codebase"
    if p2.exists():
        return p2.resolve()
    p1 = ROOT / cb
    if cb and p1.exists():
        return p1
    return None

def main(keys: list[str] | None = None):
    d = json.loads((BOOK / "data/curriculum.json").read_text())
    lessons = {L["key"]: L for L in d["lessons"]}
    if not keys:
        keys = list(lessons)[:6]
    (BOOK / "code").mkdir(exist_ok=True)
    env = {
        "HOME": str(Path.home()),
        "USER": os.environ.get("USER", "kvnkishore"),
        "PATH": "/Users/kvnkishore/.nvm/versions/node/v20.19.5/bin:/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin",
    }
    for key in keys:
        L = lessons[key]
        code = resolve_codebase(L)
        if not code:
            print("skip no codebase", key)
            continue
        prompt = (
            TPL.replace("{{KEY}}", key)
            .replace("{{TITLE}}", L["title"])
            .replace("{{CODEBASE}}", str(code))
        )
        prompt_path = ORCH / f"{key}-CODE-DEEP.md"
        prompt_path.write_text(prompt)
        log = open(BOOK / f"_logs/{key}-code-deep-run.log", "w")
        p = subprocess.Popen(
            [
                "codex", "exec",
                "--model", "gpt-5.6-sol",
                "-c", 'model_reasoning_effort="xhigh"',
                "--full-auto",
                "--skip-git-repo-check",
                prompt,
            ],
            cwd=str(ROOT),
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        print("launched code-deep", key, p.pid)

if __name__ == "__main__":
    import sys
    keys = sys.argv[1:] or [
        "tac-1-hello-agentic-coding",
        "tac-2-the-12-leverage-points",
        "tac-5-close-the-loops",
    ]
    main(keys)

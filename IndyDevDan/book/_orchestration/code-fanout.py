#!/usr/bin/env python3
"""Fan-out code deep-dives for all lessons missing code/<key>.html.
Uses Codex gpt-5.6-sol xhigh. Max 3 concurrent. Rebuilds code/index.html when any complete.
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
ORCH = BOOK / "_orchestration"
CODE = BOOK / "code"
LOG = BOOK / "_logs/code-fanout.log"
def load_tpl() -> str:
    return (ORCH / "TEMPLATE-CODE-DEEP.md").read_text()


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = time.strftime("%H:%M:%S") + " " + msg
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def lessons() -> list[dict]:
    return json.loads((BOOK / "data/curriculum.json").read_text())["lessons"]


def resolve_codebase(L: dict) -> Path | None:
    key = L["key"]
    p2 = ROOT / "IndyDevDan" / key / "codebase"
    if p2.exists():
        return p2.resolve()
    cb = L.get("codebase") or ""
    p1 = ROOT / cb
    if cb and p1.exists():
        return p1
    return None


def code_done(key: str) -> bool:
    p = CODE / f"{key}.html"
    return p.exists() and p.stat().st_size > 5000


def already_running_simple(key: str) -> bool:
    try:
        out = subprocess.check_output(["ps", "-ax", "-o", "command="], text=True)
    except Exception:
        return False
    # codex prompt embeds lesson key
    return ("codex" in out and f"key: {key}" in out) or (f"{key}-code-deep" in out)


def rebuild_index() -> None:
    Ls = lessons()
    published = []
    pending = []
    for L in Ls:
        key = L["key"]
        if code_done(key):
            published.append(L)
        else:
            pending.append(L)

    def card_pub(L: dict) -> str:
        key = L["key"]
        order = int(L["order"])
        st = CODE / f"{key}-STATUS.md"
        blurb = L["title"]
        if st.exists():
            # first non-empty line as optional blurb
            for line in st.read_text(errors="ignore").splitlines():
                if line.strip() and not line.startswith("#") and len(line) > 20:
                    blurb = line.strip()[:160]
                    break
        return f"""
        <a class="card card--ready" href="{key}.html">
          <span class="card__n">{order:02d}</span>
          <span class="card__body">
            <strong>{L['title']}</strong>
            <span class="card__meta">{L['course']} · order {order}</span>
            <span class="card__blurb">{blurb}</span>
          </span>
          <span class="card__cta">Read explainer →</span>
        </a>"""

    def card_pend(L: dict) -> str:
        order = int(L["order"])
        vol = {"TAC": "vol-1-tac", "AH": "vol-2-ah", "MA": "vol-3-ma"}[L["course"]]
        m = re.match(r"^(?:tac|ah|ma)-\d+-(.+)$", L["key"])
        slug = m.group(1) if m else L["key"]
        stem = f"{order:02d}-{slug}"
        ch = f"../{vol}/{stem}.html"
        return f"""
        <article class="card card--pending">
          <div class="card__top"><span>{L['course']} · {order:02d}</span><span class="pill">Pending</span></div>
          <strong>{L['title']}</strong>
          <p>Repository audit → annotated walkthrough → verified lab</p>
          <a href="{ch}">Read chapter {order:02d} →</a>
        </article>"""

    pub_html = "\n".join(card_pub(L) for L in published) or "<p class='empty'>None yet.</p>"
    pend_html = "\n".join(card_pend(L) for L in pending) or "<p class='empty'>All published.</p>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Code Companion Library — IndyDevDan Expert Book</title>
  <link rel="stylesheet" href="../design/tokens.css">
  <link rel="stylesheet" href="../design/base.css">
  <link rel="stylesheet" href="../design/components.css">
  <link rel="stylesheet" href="../design/chrome-v2.css">
  <style>
    body {{ background: var(--bg); color: var(--ink); font-family: var(--font-body); }}
    .wrap {{ width: min(68rem, calc(100% - 2rem)); margin: 0 auto; padding: 1rem 0 3rem; }}
    .top {{ display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:.75rem 0; border-bottom:1px solid var(--border); }}
    .top a {{ color: var(--ink-soft); text-decoration:none; font-size:.9rem; margin-left:1rem; }}
    .kicker {{ color: var(--accent-ink); font-size:.7rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }}
    h1 {{ font-family: var(--font-display); font-size: clamp(1.6rem, 3vw, 2.2rem); margin:.35rem 0 .5rem; line-height:1.15; }}
    .lead {{ max-width: 52ch; color: var(--ink-soft); line-height:1.5; }}
    .stats {{ display:flex; gap:.6rem; margin:1rem 0 1.5rem; }}
    .stat {{ background:#fff; border:1px solid var(--border); border-radius:12px; padding:.65rem .9rem; min-width:5rem; box-shadow: var(--shadow-card); }}
    .stat b {{ display:block; font-size:1.4rem; font-family: var(--font-display); }}
    .stat span {{ font-size:.75rem; color: var(--ink-mute); }}
    h2 {{ font-size:1.15rem; margin:1.5rem 0 .35rem; }}
    .section-head {{ display:flex; justify-content:space-between; align-items:end; gap:1rem; margin-top:1.25rem; }}
    .section-head p {{ font-size:.8rem; color: var(--ink-mute); margin:0; }}
    .grid {{ display:grid; grid-template-columns: 1fr; gap:.75rem; margin-top:.75rem; }}
    @media (min-width: 800px) {{ .grid.pending {{ grid-template-columns: 1fr 1fr; }} }}
    .card {{ display:block; background:#fff; border:1px solid var(--border); border-radius:14px; padding:1rem; text-decoration:none; color:inherit; box-shadow: var(--shadow-card); }}
    a.card--ready {{ display:grid; grid-template-columns: auto 1fr auto; gap:.85rem; align-items:center; }}
    a.card--ready:hover {{ border-color: var(--accent); }}
    .card__n {{ width:2.4rem; height:2.4rem; display:grid; place-items:center; border-radius:10px; background: var(--accent-wash); color: var(--accent-ink); font-weight:700; font-size:.85rem; }}
    .card__meta {{ display:block; font-size:.72rem; color: var(--ink-mute); margin-top:.15rem; }}
    .card__blurb {{ display:block; font-size:.85rem; color: var(--ink-soft); margin-top:.35rem; line-height:1.4; }}
    .card__cta {{ color: var(--accent-ink); font-weight:650; font-size:.85rem; white-space:nowrap; }}
    .card--pending .card__top {{ display:flex; justify-content:space-between; font-size:.75rem; color: var(--ink-mute); margin-bottom:.35rem; }}
    .pill {{ background: var(--bg-inset); border-radius:999px; padding:.1rem .5rem; }}
    .card--pending strong {{ display:block; margin:.2rem 0 .35rem; }}
    .card--pending p {{ font-size:.85rem; color: var(--ink-soft); margin:0 0 .65rem; }}
    .card--pending a {{ color: var(--accent-ink); font-weight:650; font-size:.85rem; text-decoration:none; }}
    .banner {{ margin-top:1.5rem; padding:.9rem 1rem; background: var(--accent-wash); border:1px solid var(--border); border-left:4px solid var(--accent); border-radius:12px; display:flex; justify-content:space-between; gap:1rem; align-items:center; flex-wrap:wrap; font-size:.9rem; }}
    .banner a {{ color: var(--accent-ink); font-weight:700; text-decoration:none; }}
    footer {{ margin-top:2rem; color: var(--ink-mute); font-size:.75rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <strong>IndyDevDan Expert Book</strong>
      <nav>
        <a href="index.html">Code library</a>
        <a href="../index.html">Book hub</a>
      </nav>
    </div>
    <p class="kicker">Code companion library</p>
    <h1>See how the system is built.</h1>
    <p class="lead">Dense, teaching-first explainers for Dan’s course repositories: architecture maps, file-by-file walkthroughs, end-to-end control flow, failure modes, and a change you can verify yourself.</p>
    <div class="stats">
      <div class="stat"><b>{len(published)}</b><span>published</span></div>
      <div class="stat"><b>{len(pending)}</b><span>in the queue</span></div>
      <div class="stat"><b>18</b><span>total lessons</span></div>
    </div>

    <div class="section-head">
      <div>
        <p class="kicker">Ready to read</p>
        <h2>Published explainers</h2>
      </div>
      <p>Only completed HTML companions appear here</p>
    </div>
    <div class="grid ready">{pub_html}</div>

    <div class="section-head">
      <div>
        <p class="kicker">Next on the bench</p>
        <h2>Pending deep-dives</h2>
      </div>
      <p>Repository audit → annotated walkthrough → verified lab</p>
    </div>
    <div class="grid pending">{pend_html}</div>

    <div class="banner">
      <span>Looking for the conceptual model first? Each companion follows its chapter — it does not replace it.</span>
      <a href="../index.html">Browse all 18 chapters →</a>
    </div>
    <footer>Code Deep-Dives · IndyDevDan Expert Book · auto-updated</footer>
  </div>
</body>
</html>
"""
    CODE.mkdir(exist_ok=True)
    (CODE / "index.html").write_text(html)
    (CODE / "HUB-STATUS.md").write_text(
        f"# Code library status\n\npublished={len(published)}\npending={len(pending)}\nupdated={time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    log(f"rebuilt index published={len(published)} pending={len(pending)}")


def launch(key: str, title: str, codebase: Path) -> subprocess.Popen:
    prompt = (
        load_tpl().replace("{{KEY}}", key)
        .replace("{{TITLE}}", title)
        .replace("{{CODEBASE}}", str(codebase))
    )
    (ORCH / f"{key}-CODE-DEEP.md").write_text(prompt)
    env = {
        "HOME": str(Path.home()),
        "USER": os.environ.get("USER", "kvnkishore"),
        "PATH": "/Users/kvnkishore/.nvm/versions/node/v20.19.5/bin:/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin",
    }
    logf = open(BOOK / f"_logs/{key}-code-deep-run.log", "a")
    return subprocess.Popen(
        [
            "codex",
            "exec",
            "--model",
            "gpt-5.6-sol",
            "-c",
            'model_reasoning_effort="xhigh"',
            "--full-auto",
            "--skip-git-repo-check",
            prompt,
        ],
        cwd=str(ROOT),
        env=env,
        stdout=logf,
        stderr=subprocess.STDOUT,
    )


def main(max_hours: float = 20.0, poll: float = 40.0, max_parallel: int = 3) -> None:
    deadline = time.time() + max_hours * 3600
    running: dict[str, subprocess.Popen] = {}
    fails: dict[str, int] = {}
    CODE.mkdir(exist_ok=True)
    rebuild_index()
    log(f"code-fanout start max_parallel={max_parallel}")

    while time.time() < deadline:
        for k, p in list(running.items()):
            if p.poll() is not None:
                rc = p.returncode
                log(f"finished {k} exit={rc}")
                if rc not in (0, None) and not code_done(k):
                    fails[k] = fails.get(k, 0) + 1
                del running[k]
                rebuild_index()

        for L in lessons():
            key = L["key"]
            if code_done(key) or key in running:
                continue
            if already_running_simple(key):
                continue
            if fails.get(key, 0) >= 2:
                continue
            if len(running) >= max_parallel:
                break
            cb = resolve_codebase(L)
            if not cb:
                log(f"skip no codebase {key}")
                fails[key] = 2
                continue
            log(f"launch {key}")
            running[key] = launch(key, L["title"], cb)

        done = sum(1 for L in lessons() if code_done(L["key"]))
        log(f"progress code_deeps={done}/18 running={list(running)}")
        if done >= 18 and not running:
            rebuild_index()
            log("ALL 18 CODE DEEPS DONE")
            return
        time.sleep(poll)

    rebuild_index()
    log("deadline")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Attach codebases to catalog/youtube/ video folders.

Primary source: GitHub (etc.) links in metadata/video-info.json description.
Prefer lines labeled Codebase / Repo / GET THE / Skill.
Clone unique repos under codebases/yt/<owner>__<repo>/ and symlink
each video's codebase/ → primary clone (course-catalog shape).

Also writes:
  metadata/repos.json   — primary + related + raw urls
  updates metadata/lesson.json with codebase fields
  updates README.md codebase row
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT / "catalog" / "youtube"
REPOS = REPO_ROOT / "codebases" / "yt"
URL_RE = re.compile(
    r"https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:/[^\s\)\]\"'<>]*)?",
    re.I,
)
GIST_RE = re.compile(
    r"https?://gist\.github\.com/([A-Za-z0-9_.-]+)/([a-f0-9]+)",
    re.I,
)
LABEL_PRIMARY = re.compile(
    r"(?i)(codebase|repo(?:sitory)?|get the|skill|source code|demo code|github)\s*[:\-–—]?\s*",
)


def clean_repo(owner: str, name: str) -> tuple[str, str] | None:
    name = name.rstrip(".,);]")
    # strip common non-repo suffixes mistakenly captured
    if name.lower() in {"wiki", "issues", "pulls", "actions", "releases", "projects", "settings"}:
        return None
    if owner.lower() in {"topics", "settings", "orgs", "marketplace", "features", "pricing", "about"}:
        return None
    # drop .git
    if name.endswith(".git"):
        name = name[:-4]
    return owner, name


def repo_url(owner: str, name: str) -> str:
    return f"https://github.com/{owner}/{name}"


def clone_key(owner: str, name: str) -> str:
    return f"{owner}__{name}"


def extract_from_description(desc: str) -> dict:
    """Return primary + related repo dicts {owner,name,url,how}."""
    if not desc:
        return {"primary": None, "related": [], "raw_matches": []}

    lines = desc.splitlines()
    candidates: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(owner: str, name: str, how: str, score: int) -> None:
        cleaned = clean_repo(owner, name)
        if not cleaned:
            return
        owner, name = cleaned
        key = (owner.lower(), name.lower())
        if key in seen:
            # bump score if better
            for c in candidates:
                if c["owner"].lower() == owner.lower() and c["name"].lower() == name.lower():
                    c["score"] = max(c["score"], score)
                    if how not in c["how"]:
                        c["how"] += f"|{how}"
            return
        seen.add(key)
        candidates.append(
            {
                "owner": owner,
                "name": name,
                "url": repo_url(owner, name),
                "how": how,
                "score": score,
            }
        )

    # line-aware: higher score for labeled codebase lines
    for line in lines:
        for m in URL_RE.finditer(line):
            owner, name = m.group(1), m.group(2)
            score = 10
            how = "url"
            low = line.lower()
            if "codebase" in low:
                score = 100
                how = "label:codebase"
            elif re.search(r"\brepo\b", low) and "report" not in low:
                score = 80
                how = "label:repo"
            elif "get the" in low or "get this" in low:
                score = 70
                how = "label:get-the"
            elif "skill" in low:
                score = 60
                how = "label:skill"
            elif "source" in low:
                score = 50
                how = "label:source"
            # demote third-party docs/tools slightly if not labeled
            if owner.lower() != "disler" and score < 50:
                score -= 5
            # demote wiki-like path leftovers already filtered
            add(owner, name, how, score)

    # whole-desc catch (no line context)
    for m in URL_RE.finditer(desc):
        add(m.group(1), m.group(2), "desc-scan", 5)

    # gists as fallback primary when no real repo (code snippet demos)
    gists = []
    for m in GIST_RE.finditer(desc):
        owner, gist_id = m.group(1), m.group(2)
        gists.append(
            {
                "owner": owner,
                "name": f"gist-{gist_id[:12]}",
                "url": f"https://gist.github.com/{owner}/{gist_id}",
                "how": "gist",
                "score": 40,
                "kind": "gist",
                "gist_id": gist_id,
            }
        )

    candidates.sort(key=lambda c: (-c["score"], 0 if c["owner"].lower() == "disler" else 1, c["name"]))
    if not candidates and gists:
        candidates = gists
    elif gists:
        # keep as related only if we already have repos
        for g in gists:
            key = (g["owner"].lower(), g["name"].lower())
            if key not in seen:
                candidates.append(g)

    primary = candidates[0] if candidates else None
    related = candidates[1:] if len(candidates) > 1 else []
    return {
        "primary": primary,
        "related": related,
        "raw_matches": [c["url"] for c in candidates],
    }


def ensure_clone(owner: str, name: str, kind: str = "repo", gist_id: str | None = None) -> tuple[Path | None, str]:
    REPOS.mkdir(parents=True, exist_ok=True)
    if kind == "gist" and gist_id:
        dest = REPOS / f"gist__{owner}__{gist_id[:12]}"
        url = f"https://gist.github.com/{owner}/{gist_id}.git"
    else:
        dest = REPOS / clone_key(owner, name)
        url = repo_url(owner, name)
    # A tree that exists is a vendored snapshot and is left exactly as it is,
    # with or without a .git of its own.
    #
    # This used to be `if dest.exists() and not (dest/".git").exists():
    # shutil.rmtree(dest)` — i.e. "a directory with no .git is a broken clone,
    # delete and re-clone it". Since the codebases were vendored (their nested
    # .git directories removed so their contents track in this repository), that
    # condition matches EVERY tree here. Running it deleted 28 archived
    # snapshots and replaced them with current upstream HEAD, silently
    # discarding the pinned versions recorded in REPOS.md.
    #
    # To deliberately refresh a tree, delete it first, or follow the overlay
    # recipe in REPOS.md. This function only fills in what is missing.
    if dest.exists():
        return dest, "exists"
    # shallow clone
    r = subprocess.run(
        ["git", "clone", "--depth", "1", url, str(dest)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if r.returncode != 0:
        # try without depth if shallow fails (empty repo etc.)
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
        r2 = subprocess.run(
            ["git", "clone", url, str(dest)],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if r2.returncode != 0:
            err = (r2.stderr or r.stderr or "")[-400:]
            return None, f"clone_fail: {err}"
        return dest, "cloned"
    return dest, "cloned"


def link_codebase(folder: Path, target: Path) -> None:
    link = folder / "codebase"
    if link.is_symlink() or link.exists():
        if link.is_symlink() or link.is_file():
            link.unlink()
        else:
            shutil.rmtree(link)
    # relative symlink from folder/codebase -> codebases/yt/...
    rel = os.path.relpath(target, folder)
    link.symlink_to(rel)


def patch_readme(folder: Path, primary: dict | None, status: str) -> None:
    readme = folder / "README.md"
    if not readme.exists():
        return
    text = readme.read_text()
    row = (
        f"| Codebase | `codebase/` → `{primary['owner']}/{primary['name']}` ({status}) |"
        if primary
        else "| Codebase | — (none in video description) |"
    )
    if "| Codebase |" in text:
        text = re.sub(r"\| Codebase \|.*\|", row, text)
    else:
        # insert after Metadata JSON row if present
        if "| Metadata JSON |" in text:
            text = re.sub(
                r"(\| Metadata JSON \|.*\|\n)",
                r"\1" + row + "\n",
                text,
            )
        else:
            text = text.rstrip() + "\n" + row + "\n"
    readme.write_text(text)


def process_one(folder: Path, do_clone: bool = True) -> dict:
    key = folder.name
    info_path = folder / "metadata" / "video-info.json"
    info = json.loads(info_path.read_text()) if info_path.exists() else {}
    extracted = extract_from_description(info.get("description") or "")
    primary = extracted["primary"]
    result = {
        "key": key,
        "primary": primary,
        "related": extracted["related"],
        "clone_status": None,
        "codebase_path": None,
        "error": None,
    }

    repos_meta = {
        "primary": primary,
        "related": extracted["related"],
        "raw_matches": extracted["raw_matches"],
        "source": "youtube description (video-info.json)",
    }

    if primary and do_clone:
        path, st = ensure_clone(
            primary["owner"],
            primary["name"],
            kind=primary.get("kind") or "repo",
            gist_id=primary.get("gist_id"),
        )
        result["clone_status"] = st
        if path:
            link_codebase(folder, path)
            result["codebase_path"] = str(path.relative_to(REPO_ROOT))
            repos_meta["local_clone"] = result["codebase_path"]
            repos_meta["symlink"] = "codebase/"
        else:
            result["error"] = st
            repos_meta["local_clone"] = None
            repos_meta["error"] = st
    elif not primary:
        result["clone_status"] = "no_repo_in_description"
        # remove stale symlink
        link = folder / "codebase"
        if link.is_symlink() or link.exists():
            if link.is_symlink() or link.is_file():
                link.unlink()
            else:
                shutil.rmtree(link)
        # write CODEBASE.md note
        (folder / "CODEBASE.md").write_text(
            f"# No public codebase linked\n\n"
            f"Video `{key}` description did not include a GitHub/repo URL.\n"
            f"Related course links (if any) live in `metadata/video-info.json` description.\n"
        )

    (folder / "metadata" / "repos.json").write_text(
        json.dumps(repos_meta, indent=2, ensure_ascii=False) + "\n"
    )

    # lesson.json
    lesson_path = folder / "metadata" / "lesson.json"
    lesson: dict = json.loads(lesson_path.read_text()) if lesson_path.exists() else {"key": key}
    if primary:
        lesson["codebase"] = f"{primary['owner']}/{primary['name']}"
        lesson["codebase_url"] = primary["url"]
        lesson["codebase_local"] = "codebase/" if result.get("codebase_path") else None
        lesson["codebase_related"] = [
            f"{r['owner']}/{r['name']}" for r in extracted["related"]
        ]
    else:
        lesson["codebase"] = None
        lesson["codebase_url"] = None
        lesson["codebase_local"] = None
        lesson["codebase_related"] = []
    lesson_path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n")

    patch_readme(folder, primary, result.get("clone_status") or "n/a")

    # STATUS.json
    status_path = folder / "STATUS.json"
    status = json.loads(status_path.read_text()) if status_path.exists() else {}
    status["codebase"] = bool(result.get("codebase_path"))
    status["codebase_repo"] = (
        f"{primary['owner']}/{primary['name']}" if primary else None
    )
    status["codebase_status"] = result.get("clone_status")
    if result.get("error"):
        status.setdefault("errors", []).append(result["error"])
    status_path.write_text(json.dumps(status, indent=2) + "\n")

    return result


def main() -> int:
    do_clone = "--no-clone" not in sys.argv
    keys = []
    if "--keys" in sys.argv:
        i = sys.argv.index("--keys")
        keys = sys.argv[i + 1 :]

    folders = sorted(p for p in ROOT.glob("yt-*") if p.is_dir())
    if keys:
        folders = [p for p in folders if p.name in keys or any(p.name.startswith(k) for k in keys)]

    results = []
    for folder in folders:
        print(f"== {folder.name} ==")
        try:
            r = process_one(folder, do_clone=do_clone)
            results.append(r)
            prim = r["primary"]
            if prim:
                print(f"  primary: {prim['owner']}/{prim['name']} [{r['clone_status']}]")
            else:
                print("  primary: NONE")
            if r.get("error"):
                print(f"  error: {r['error'][:200]}")
        except Exception as e:
            print(f"  FATAL: {e}")
            results.append({"key": folder.name, "error": str(e)})

    summary = {
        "processed": len(results),
        "with_primary": sum(1 for r in results if r.get("primary")),
        "cloned_or_exists": sum(
            1 for r in results if r.get("clone_status") in ("cloned", "exists")
        ),
        "no_repo": sum(1 for r in results if r.get("clone_status") == "no_repo_in_description"),
        "errors": [r for r in results if r.get("error")],
        "results": results,
    }
    (ROOT / "_codebase_attach_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("\n=== SUMMARY ===")
    print(json.dumps({k: summary[k] for k in summary if k != "results"}, indent=2))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

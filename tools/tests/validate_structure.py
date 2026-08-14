#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Prove the repository layout is intact.

This is the thing that keeps the structure honest. It asserts the invariants
that the layout depends on and that nothing else checks — most of which fail
silently when they break, which is why they are here rather than in prose.

    uv run tools/tests/validate_structure.py        # or: make validate
    uv run tools/tests/validate_structure.py -v     # list every check

Exits non-zero with a specific message naming the offending path. Stdlib only,
no dependencies, no network.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# A top-level directory must be named for the role it plays. Adding one here is
# a deliberate act: the "no unexpected directory" half of check 1 is what stops
# a new output/-shaped tree appearing next quarter.
EXPECTED_DIRS = {
    "catalog",
    "codebases",
    "docs",
    "knowledge",
    "media",
    "projects",
    "specs",
    "tools",
    "transcripts",
}
# Permitted but not required: scratch space that .gitignore already excludes and
# that tooling creates on demand. `worktrees/` is created by the /worktree skill
# and ignored at .gitignore; failing on it would be this test contradicting the
# ignore policy rather than enforcing the layout.
OPTIONAL_DIRS = {"worktrees"}
ALLOWED_HIDDEN = {".git", ".github", ".claude", ".scratch", ".idea", ".vscode"}
EXPECTED_ROOT_FILES = {
    "README.md",
    "CLAUDE.md",
    "AGENTS.md",
    "CONTEXT.md",
    "REPOS.md",
    "Makefile",
    ".gitignore",
    ".gitattributes",
}

MEDIA_EXT = (".mp4", ".m4a", ".mov", ".webm", ".aac")
GENERATED_RE = re.compile(r"(^|/)(__pycache__|node_modules|\.venv|\.DS_Store|\.idea)(/|$)")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")

failures: list[str] = []
checks_run = 0
VERBOSE = False


def check(name: str):
    """Decorator registering a check; collects failures instead of stopping."""

    def wrap(fn):
        def run():
            global checks_run
            checks_run += 1
            before = len(failures)
            try:
                fn()
            except Exception as exc:  # a crashing check is a failing check
                failures.append(f"{name}: check raised {type(exc).__name__}: {exc}")
            if VERBOSE and len(failures) == before:
                print(f"  ok   {name}")
        run.__name__ = fn.__name__
        return run

    return wrap


def fail(name: str, msg: str) -> None:
    failures.append(f"{name}: {msg}")


def git(*args: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in out.stdout.splitlines() if line]


def tracked_files() -> list[str]:
    return git("ls-files")


def is_git_ignored(path: Path) -> bool:
    return (
        subprocess.run(
            ["git", "-C", str(REPO_ROOT), "check-ignore", "-q", str(path)],
            capture_output=True,
        ).returncode
        == 0
    )


# --------------------------------------------------------------------------- 1
@check("1. top-level layout")
def check_top_level():
    name = "1. top-level layout"
    present = {p.name for p in REPO_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")}
    for missing in sorted(EXPECTED_DIRS - present):
        fail(name, f"expected top-level directory is missing: {missing}/")
    for extra in sorted(present - EXPECTED_DIRS - OPTIONAL_DIRS):
        fail(
            name,
            f"unexpected top-level directory: {extra}/ — name it for the role it "
            "plays and add it to EXPECTED_DIRS, or move it inside an existing tree",
        )
    for p in REPO_ROOT.iterdir():
        # Files git already ignores (.DS_Store and friends) are not layout.
        if p.is_file() and p.name not in EXPECTED_ROOT_FILES and not is_git_ignored(p):
            fail(name, f"unexpected file at the repo root: {p.name}")
        if p.is_dir() and p.name.startswith(".") and p.name not in ALLOWED_HIDDEN:
            fail(name, f"unexpected hidden top-level directory: {p.name}/")


# --------------------------------------------------------------------------- 2
@check("2. no spaces in tracked paths")
def check_no_spaces():
    name = "2. no spaces in tracked paths"
    for f in tracked_files():
        if " " in f:
            fail(name, f"tracked path contains a space: {f}")


# --------------------------------------------------------------------------- 3
@check("3. lesson and video folder shape")
def check_folder_shape():
    name = "3. lesson and video folder shape"
    courses = REPO_ROOT / "catalog" / "courses"
    if not courses.is_dir():
        fail(name, "catalog/courses/ is missing")
        return
    lessons = sorted(p for p in courses.iterdir() if p.is_dir())
    if not lessons:
        fail(name, "catalog/courses/ has no lessons")
    for d in lessons:
        for required in ("video", "transcript", "metadata", "codebase", "README.md"):
            if not (d / required).exists():
                fail(name, f"catalog/courses/{d.name}/ is missing {required}")

    yt = REPO_ROOT / "catalog" / "youtube"
    if not yt.is_dir():
        fail(name, "catalog/youtube/ is missing")
        return
    videos = sorted(p for p in yt.iterdir() if p.is_dir() and p.name.startswith("yt-"))
    if not videos:
        fail(name, "catalog/youtube/ has no yt-* folders")
    for d in videos:
        for required in ("transcript", "metadata"):
            if not (d / required).exists():
                fail(name, f"catalog/youtube/{d.name}/ is missing {required}")


# --------------------------------------------------------------------------- 4
@check("4. every symlink resolves")
def check_symlinks_resolve():
    name = "4. every symlink resolves"
    for p in REPO_ROOT.rglob("*"):
        if ".git" in p.parts:
            continue
        if p.is_symlink() and not p.exists():
            rel = p.relative_to(REPO_ROOT)
            fail(name, f"broken symlink: {rel} -> {p.readlink()}")


# --------------------------------------------------------------------------- 5
@check("5. codebase/ symlinks point inside codebases/")
def check_codebase_targets():
    name = "5. codebase/ symlinks point inside codebases/"
    codebases = (REPO_ROOT / "codebases").resolve()
    found = 0
    for p in (REPO_ROOT / "catalog").rglob("codebase"):
        if not p.is_symlink():
            continue
        found += 1
        target = p.resolve()
        if not target.is_relative_to(codebases):
            rel = p.relative_to(REPO_ROOT)
            fail(name, f"{rel} resolves outside codebases/: {target}")
    if found == 0:
        fail(name, "no codebase/ symlinks found at all — the builders did not run")


# --------------------------------------------------------------------------- 6
@check("6. indexes parse, are relative, and agree with disk")
def check_indexes():
    name = "6. indexes parse, are relative, and agree with disk"

    course_index = REPO_ROOT / "catalog" / "INDEX.json"
    yt_index = REPO_ROOT / "catalog" / "youtube" / "INDEX.json"

    # `continue`, never `return`: one missing or malformed index must not stop
    # the other from being checked. Returning here hid an orphan entry in the
    # YouTube index whenever catalog/INDEX.json was absent.
    for path in (course_index, yt_index):
        if not path.is_file():
            fail(name, f"missing index: {path.relative_to(REPO_ROOT)}")
            continue
        raw = path.read_text()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(name, f"{path.relative_to(REPO_ROOT)} is not valid JSON: {exc}")
            continue
        # An absolute filesystem path in a generated index breaks it for every
        # checkout but this one. That is exactly the bug this catches.
        for m in re.finditer(r'"(/[^"]*)"', raw):
            fail(
                name,
                f"{path.relative_to(REPO_ROOT)} contains an absolute path: {m.group(1)}",
            )
        if path is course_index:
            keys = {e["key"] for e in data.get("lessons", [])}
            on_disk = {p.name for p in (REPO_ROOT / "catalog" / "courses").iterdir() if p.is_dir()}
            label = "catalog/courses"
        else:
            keys = {e["key"] for e in data.get("videos", [])}
            on_disk = {
                p.name
                for p in (REPO_ROOT / "catalog" / "youtube").iterdir()
                if p.is_dir() and p.name.startswith("yt-")
            }
            label = "catalog/youtube"
        for orphan in sorted(keys - on_disk):
            fail(name, f"{path.name} lists '{orphan}' but {label}/ has no such directory")
        for unindexed in sorted(on_disk - keys):
            fail(name, f"{label}/{unindexed} exists but is not in {path.name}")


# --------------------------------------------------------------------------- 7
@check("7. backticked paths in the top-level docs exist")
def check_doc_paths():
    name = "7. backticked paths in the top-level docs exist"
    docs = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / "CONTEXT.md",
        REPO_ROOT / "REPOS.md",
        REPO_ROOT / "catalog" / "README.md",
    ]
    # Only treat a backticked token as a path claim when it looks like one and
    # carries no glob/placeholder. Commands and prose must not produce noise.
    # The host pattern matters: REPOS.md cites ~40 bare `github.com/owner/repo`
    # URLs, which are references, not paths in this repository.
    skip = re.compile(
        r"[<>*?|$\s]|^-|^\.\.\.|^https?:|^(?:[\w-]+\.)+(?:com|org|net|io|dev)/"
    )
    for doc in docs:
        if not doc.is_file():
            fail(name, f"missing doc: {doc.relative_to(REPO_ROOT)}")
            continue
        for token in BACKTICK_RE.findall(doc.read_text()):
            t = token.strip()
            if skip.search(t) or "/" not in t.rstrip("/"):
                continue
            if not t.split("/")[0] or t.startswith("."):
                continue
            # A path in a doc may be written from the repo root or relative to
            # the doc itself; catalog/README.md says `_source/course-pages/`.
            # Both readings are legitimate, so accept either.
            cleaned = t.rstrip("/")
            candidates = [REPO_ROOT / cleaned, doc.parent / cleaned]
            if not any(c.exists() or c.is_symlink() for c in candidates):
                fail(
                    name,
                    f"{doc.relative_to(REPO_ROOT)} references `{t}` which does not exist",
                )


# --------------------------------------------------------------------------- 8
@check("8. no media tracked by git")
def check_no_media_tracked():
    name = "8. no media tracked by git"
    for f in tracked_files():
        if f.lower().endswith(MEDIA_EXT):
            fail(name, f"media file is tracked: {f}")


# --------------------------------------------------------------------------- 9
@check("9. no generated files tracked by git")
def check_no_generated_tracked():
    name = "9. no generated files tracked by git"
    for f in tracked_files():
        if GENERATED_RE.search(f):
            fail(name, f"generated path is tracked: {f}")


# -------------------------------------------------------------------------- 10
@check("10. every tools/ script compiles and declares PEP 723")
def check_tools_scripts():
    name = "10. every tools/ script compiles and declares PEP 723"
    scripts = sorted((REPO_ROOT / "tools").rglob("*.py"))
    if not scripts:
        fail(name, "tools/ contains no Python scripts")
    for s in scripts:
        rel = s.relative_to(REPO_ROOT)
        src = s.read_text(encoding="utf-8", errors="replace")
        try:
            ast.parse(src, filename=str(rel))
        except SyntaxError as exc:
            fail(name, f"{rel} does not compile: line {exc.lineno}: {exc.msg}")
            continue
        head = "\n".join(src.splitlines()[:12])
        if "# /// script" not in head:
            fail(name, f"{rel} has no PEP 723 header in its first 12 lines")


CHECKS = [
    check_top_level,
    check_no_spaces,
    check_folder_shape,
    check_symlinks_resolve,
    check_codebase_targets,
    check_indexes,
    check_doc_paths,
    check_no_media_tracked,
    check_no_generated_tracked,
    check_tools_scripts,
]


def main() -> int:
    global VERBOSE
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-v", "--verbose", action="store_true", help="list every check")
    VERBOSE = ap.parse_args().verbose

    for c in CHECKS:
        c()

    if failures:
        print(f"FAIL — {len(failures)} problem(s) across {checks_run} checks:\n", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        print(
            "\nSee tools/tests/README.md for what each check means and how to fix it.",
            file=sys.stderr,
        )
        return 1

    print(f"OK — {checks_run} structural checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

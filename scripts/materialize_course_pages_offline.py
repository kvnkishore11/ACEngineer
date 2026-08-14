#!/usr/bin/env python3
"""Materialize offline course pages: real AE HTML + local CSS/fonts/images (no Nuxt JS)."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer")
SRC_PAGES = ROOT / "IndyDevDan" / "_source" / "course-pages"
ASSETS = ROOT / "IndyDevDan" / "_source" / "assets"
OUT_OFFLINE = ROOT / "IndyDevDan" / "_source" / "course-pages-offline"

# CSS order roughly matches live page
CSS_FILES = [
    "entry.DIesnPDN.css",
    "Tooltip.BcV9Aivw.css",
    "NavFooter.CB_JiNvR.css",
    "TacLessonWithMux.C8uQJajj.css",
    "TacVideoBackground.BCVNxSgk.css",
    "PaicPill.DEDTXCcP.css",
    "index.CQPDvJ3X.css",
]


def local_img_name(url_or_path: str) -> str | None:
    u = url_or_path.strip()
    if u.startswith("data:"):
        return None
    if u.startswith("//"):
        u = "https:" + u
    if u.startswith("https://agenticengineer.com/"):
        path = u[len("https://agenticengineer.com/") :]
    elif u.startswith("/"):
        path = u[1:]
    elif u.startswith("http"):
        # external (mux etc.) — leave as absolute remote
        return None
    else:
        path = u
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", path)


def rewrite_asset_urls(html: str, rel_to_assets: str) -> str:
    """Rewrite AE relative/absolute asset URLs to local assets paths."""

    def map_url(u: str) -> str:
        name = local_img_name(u)
        if name is None:
            # keep absolute external
            if u.startswith("http") or u.startswith("data:"):
                return u
            return u
        img_path = ASSETS / "img" / name
        if img_path.is_file():
            return f"{rel_to_assets}/img/{name}"
        # try fonts
        if name.endswith(".ttf") or "Play-" in name:
            font = name.split("_")[-1] if "_" in name else name
            if (ASSETS / "fonts" / font).is_file():
                return f"{rel_to_assets}/fonts/{font}"
        # CSS handled separately
        if name.endswith(".css"):
            base = Path(name).name
            if (ASSETS / "css" / base).is_file():
                return f"{rel_to_assets}/css/{base}"
        # fallback absolute so online still works
        if u.startswith("/"):
            return "https://agenticengineer.com" + u
        return u

    def repl_attr(m: re.Match) -> str:
        attr, quote, url = m.group(1), m.group(2), m.group(3)
        return f"{attr}={quote}{map_url(url)}{quote}"

    html = re.sub(
        r'''((?:src|href|poster))=("|')([^"']+)\2''',
        repl_attr,
        html,
        flags=re.I,
    )

    def repl_url(m: re.Match) -> str:
        q, url = m.group(1), m.group(2)
        return f"url({q}{map_url(url)}{q})"

    html = re.sub(r'''url\((['"]?)([^'")]+)\1\)''', repl_url, html)
    return html


def strip_scripts_and_remote_noise(html: str) -> str:
    # remove script tags (Nuxt hydration breaks offline SSR)
    html = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", html, flags=re.I)
    html = re.sub(r"<script\b[^>]*/>", "", html, flags=re.I)
    # remove modulepreload / prefetch of js
    html = re.sub(
        r'''<link\b[^>]+rel=["'](?:modulepreload|prefetch|preload)["'][^>]*>''',
        "",
        html,
        flags=re.I,
    )
    # remove existing stylesheet links — we inject local ones
    html = re.sub(
        r'''<link\b[^>]+rel=["']stylesheet["'][^>]*>''',
        "",
        html,
        flags=re.I,
    )
    # analytics leftovers already mostly scripts
    return html


def inject_local_head(html: str, rel_to_assets: str, title: str | None) -> str:
    links = []
    for css in CSS_FILES:
        if (ASSETS / "css" / css).is_file():
            links.append(
                f'<link rel="stylesheet" href="{rel_to_assets}/css/{css}">'
            )
    # offline safety: ensure dark body if something fails
    links.append(
        "<style>"
        "html,body{min-height:100%;}"
        "/* offline: prevent broken external font flash */"
        f"@font-face{{font-family:Play;font-style:normal;font-weight:400;"
        f"src:url('{rel_to_assets}/fonts/Play-Regular.ttf') format('truetype');}}"
        f"@font-face{{font-family:Play;font-style:normal;font-weight:700;"
        f"src:url('{rel_to_assets}/fonts/Play-Bold.ttf') format('truetype');}}"
        "</style>"
    )
    inject = "\n".join(links)
    if re.search(r"<head[^>]*>", html, re.I):
        html = re.sub(r"(<head[^>]*>)", r"\1\n" + inject, html, count=1, flags=re.I)
    else:
        html = f"<head>{inject}</head>" + html
    if title and re.search(r"<title>[^<]*</title>", html, re.I):
        html = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", html, count=1, flags=re.I)
    # base tag not needed with relative assets
    return html


def extract_title(html: str) -> str | None:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if m:
        t = re.sub(r"<[^>]+>", "", m.group(1))
        t = re.sub(r"\s+", " ", t).strip()
        return t[:120] if t else None
    return None


def materialize_one(src: Path, dst: Path, rel_to_assets: str) -> dict:
    raw = src.read_text(encoding="utf-8", errors="replace")
    title = extract_title(raw)
    html = strip_scripts_and_remote_noise(raw)
    html = inject_local_head(html, rel_to_assets, title)
    html = rewrite_asset_urls(html, rel_to_assets)
    # ensure doctype
    if not html.lstrip().lower().startswith("<!doctype"):
        html = "<!doctype html>\n" + html
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html, encoding="utf-8")
    return {
        "src": src.name,
        "dst": str(dst),
        "bytes": dst.stat().st_size,
        "title": title,
        "has_loot": "Loot Box" in html,
        "has_local_css": f"{rel_to_assets}/css/entry" in html,
        "has_local_hero": "hero-tactical-agentic-coding-course-background" in html
        and "assets/img" in html,
    }


def main() -> int:
    assert (ASSETS / "css" / "entry.DIesnPDN.css").is_file(), "missing entry CSS"
    assert (ASSETS / "fonts" / "Play-Regular.ttf").is_file(), "missing fonts"
    OUT_OFFLINE.mkdir(parents=True, exist_ok=True)

    # Public assets alias used by lesson metadata pages:
    # IndyDevDan/<lesson>/metadata/course-page.html → ../../assets
    public_assets = ROOT / "IndyDevDan" / "assets"
    if public_assets.is_symlink() or public_assets.exists():
        if public_assets.is_symlink() or public_assets.is_file():
            public_assets.unlink()
        else:
            # keep real dir if already present
            pass
    if not public_assets.exists():
        public_assets.symlink_to("_source/assets")

    # Two outputs:
    # 1) source mirror (../assets) under course-pages-offline/
    # 2) metadata-ready (../../assets) under course-pages-offline/for-metadata/
    meta_out = OUT_OFFLINE / "for-metadata"
    meta_out.mkdir(parents=True, exist_ok=True)

    results = []
    for src in sorted(SRC_PAGES.glob("*.html")):
        if src.name.startswith("."):
            continue
        for rel, dest_dir in (("../assets", OUT_OFFLINE), ("../../assets", meta_out)):
            if dest_dir == OUT_OFFLINE and rel != "../assets":
                continue
            dst = dest_dir / src.name
            info = materialize_one(src, dst, rel)
            info["rel"] = rel
            results.append(info)
        print(
            f"OK {src.name:50} meta_bytes={ (meta_out/src.name).stat().st_size } "
            f"loot={ 'Loot Box' in (meta_out/src.name).read_text(encoding='utf-8', errors='replace') }"
        )

    (ASSETS / "README.md").write_text(
        "# Offline assets for IndyDevDan course pages\n\n"
        "Pulled from agenticengineer.com for offline `course-page.html` rendering.\n"
        "- `css/` Nuxt stylesheets (entry + lesson components)\n"
        "- `fonts/` Play Regular/Bold\n"
        "- `img/` hero, logo, loot cards, thumbnails\n\n"
        "Lesson pages under `IndyDevDan/<key>/metadata/course-page.html` "
        "reference `../../assets/` (symlink to this tree).\n",
        encoding="utf-8",
    )
    print(f"\nMaterialized offline pages → {OUT_OFFLINE} (+ for-metadata/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

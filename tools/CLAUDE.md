# `tools/` — local rules

1. **Every script is PEP 723 and stdlib-only** unless it declares otherwise.
   Run with `uv run tools/<area>/<script>.py`. Keep it that way — a new
   dependency goes in the script's own header, not in a project manifest.
2. **Derive paths from `REPO_ROOT`**, never from the current working directory
   and never from an absolute `/Users/...` path:
   ```python
   REPO_ROOT = Path(__file__).resolve().parents[2]
   ```
   The structure test does not catch a hardcoded home directory, but a teammate
   will.
3. **Generated output must use repo-relative paths.** Both index builders write
   `"root"` as a relative string; an absolute path there breaks the index for
   every other checkout.
4. **The builders own the symlinks.** `catalog/build_catalog.py` owns the 18
   course `codebase/` links; `youtube/attach_codebases.py` and
   `youtube/fill_missing_codebases.py` own the 46 video ones. To change a link,
   change the constants and re-run. Hand-edited links are silently overwritten.
5. **Run order matters for the YouTube links**: `attach_codebases.py` prunes
   links for videos whose description names no repo, and that set includes the
   ones `fill_missing_codebases.py` attaches to course-local codebases. Attach
   first, fill second, rebuild the index last. `make youtube` does not cover the
   fill step — run it explicitly when a video's codebase goes missing.
6. **Idempotency is documented per script in `README.md`.** The catalog and
   YouTube builders are safe to re-run; the recorder is not — it drives a real
   browser and re-records.
7. After changing anything here: `python3 -m compileall -q tools/` and
   `make validate`.

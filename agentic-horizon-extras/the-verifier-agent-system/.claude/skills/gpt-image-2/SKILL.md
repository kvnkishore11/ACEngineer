---
name: gpt-image-2
description: Generate and edit images exclusively with OpenAI's gpt-image-2 (ChatGPT Images 2.0). Use when creating images from text prompts, editing existing images, masked inpainting, or composing multiple reference images using gpt-image-2. Keywords — gpt-image-2, gpt image, openai image, chatgpt images, image edit, image compose, inpaint, mask.
---

# gpt-image-2

Minimal, focused skill for OpenAI's `gpt-image-2` (released 2026-04-21). Native reasoning, flexible custom sizes, strong instruction following, multi-image composition, and masked inpainting.

> **Effort dial:** gpt-image-2 reasons internally and does **not** expose a `thinking` / `reasoning_effort` parameter on the Images API. Use `--quality` (`low` → `high`) as the de-facto compute/effort knob. Per OpenAI docs: "Use `quality: low` for fast drafts… move to `medium` or `high` for final assets."

## Prerequisite Check (REQUIRED)

**STOP: Before running any script, verify `OPENAI_API_KEY` exists** in environment or in `.env` in the current working directory:

```bash
( [ -n "$OPENAI_API_KEY" ] || grep -q OPENAI_API_KEY .env 2>/dev/null ) && echo "OPENAI_API_KEY found" || echo "OPENAI_API_KEY missing"
```

- If missing → **STOP and ask the user to set it**
- Scripts load `.env` from the **current working directory** (where the agent runs), not from the script location.

## Cookbook

**IMPORTANT:** Always run `--help` on a script before executing to see available options.

### Generate a new image from a text prompt
**Then use:** `generate_gpt_image.py`

```bash
# Check options
uv run scripts/generate_gpt_image.py --help

# Basic generation (auto size, auto quality)
uv run scripts/generate_gpt_image.py "A sunset over mountains" sunset.png

# Pinned size + high quality
uv run scripts/generate_gpt_image.py "Company logo" logo.png --size 1024x1024 --quality high

# Wide cinematic
uv run scripts/generate_gpt_image.py "Wide cinematic shot of a coastline" wide.png --size 2048x1152

# Multiple variants (suffixes _1, _2, ...)
uv run scripts/generate_gpt_image.py "Sticker of a happy frog" frog.png --count 4

# JPEG with compression
uv run scripts/generate_gpt_image.py "Product mockup" mock.jpg --format jpeg --compression 85

# Opaque background (gpt-image-2 does NOT support transparent)
uv run scripts/generate_gpt_image.py "Studio product shot" prod.png --background opaque

# Pin a snapshot
uv run scripts/generate_gpt_image.py "Test prompt" out.png --model gpt-image-2-2026-04-21
```

### Edit, inpaint, or compose existing images
**Then use:** `edit_gpt_image.py`

Multiple input images = composition (gpt-image-2 fuses references).

```bash
uv run scripts/edit_gpt_image.py --help

# Single-image edit
uv run scripts/edit_gpt_image.py "Add a rainbow in the sky" edited.png photo.png

# Multi-image composition
uv run scripts/edit_gpt_image.py "Put the cat on the couch" result.png cat.png couch.png

# Masked inpaint (transparent pixels in mask = regions to edit)
uv run scripts/edit_gpt_image.py "Replace masked area with a window" out.png room.png --mask mask.png

# Edit with explicit size + high quality
uv run scripts/edit_gpt_image.py "Make it watercolor" art.png photo.png --size 2048x2048 --quality high

# Force opaque background on the edit output
uv run scripts/edit_gpt_image.py "Add a rainbow" out.png photo.png --background opaque
```

## Quick Reference — `generate_gpt_image.py`

| Flag | Values | Default |
|------|--------|---------|
| `prompt` (positional) | text | required |
| `output` (positional) | path (e.g. `out.png`) | required |
| `--model`, `-m` | `gpt-image-2`, `gpt-image-2-2026-04-21` (snapshot) | `gpt-image-2` |
| `--size`, `-s` | `auto`, `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `1152x2048`, `3840x2160`, `2160x3840`, or any custom WxH (max edge ≤3840, multiples of 16, aspect ≤3:1, total px 655360–8294400) | `auto` |
| `--quality`, `-q` | `auto`, `low`, `medium`, `high` (effective effort dial) | `auto` |
| `--count`, `-n` | int ≥ 1 (suffixes `_1`, `_2`, … when >1) | `1` |
| `--format`, `-f` | `png`, `jpeg`, `webp` | `png` |
| `--compression` | 0–100 (jpeg/webp only) | — |
| `--moderation` | `auto`, `low` | `auto` |
| `--background` | `auto`, `opaque` (⚠️ `transparent` NOT supported by gpt-image-2) | `auto` |

## Quick Reference — `edit_gpt_image.py`

| Flag | Values | Default |
|------|--------|---------|
| `instruction` (positional) | text | required |
| `output` (positional) | path | required |
| `inputs` (positional, 1+) | one or more input image paths (multiple = composition) | required |
| `--model`, `-m` | `gpt-image-2`, `gpt-image-2-2026-04-21` (snapshot) | `gpt-image-2` |
| `--size`, `-s` | `auto` or any valid WxH (same rules as generate) | `auto` |
| `--quality`, `-q` | `auto`, `low`, `medium`, `high` (effective effort dial) | `auto` |
| `--format`, `-f` | `png`, `jpeg`, `webp` | `png` |
| `--compression` | 0–100 (jpeg/webp only) | — |
| `--mask` | path to mask PNG (transparent pixels = regions to edit) | — |
| `--background` | `auto`, `opaque` (⚠️ `transparent` NOT supported by gpt-image-2) | `auto` |

> Note: `--count` and `--moderation` are **only** available on `generate_gpt_image.py`, not on `edit_gpt_image.py`. Per OpenAI docs, `input_fidelity` is intentionally **not** exposed — gpt-image-2 always processes inputs at high fidelity automatically.

## Pricing (per 1M tokens)

| Type | Price |
|------|-------|
| Image output | $30.00 |
| Image input | $8.00 |
| Cached input | $2.00 |

## Notes

- **No thinking-level parameter.** gpt-image-2 has native internal reasoning but the Images API does not expose `thinking` / `reasoning_effort`. `--quality` is the effective compute/effort dial.
- gpt-image-2 returns base64 PNG by default — use `.png` extension unless overriding `--format`.
- Outputs include C2PA provenance metadata.
- Custom sizes must satisfy: max edge ≤ 3840, both edges multiples of 16, aspect ratio ≤ 3:1, total pixels 655,360–8,294,400.
- **2K+ outputs are experimental.** Per OpenAI: outputs containing more than `2560x1440` (3,686,400 total pixels) are considered experimental — expect occasional quality variance at `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`.
- **Background:** gpt-image-2 supports only `auto` or `opaque`. `transparent` is **not** supported (use Gemini Nano Banana 2 or DALL-E for transparent PNGs).
- **Input fidelity:** gpt-image-2 always processes input images at high fidelity — the `input_fidelity` API parameter must be omitted (and is therefore not exposed as a flag). Edit requests with reference images may use more input tokens as a result.
- For composition, pass multiple input images to `edit_gpt_image.py` — gpt-image-2 fuses references natively.
- Masks: transparent pixels in the mask PNG indicate the region to edit; opaque pixels are preserved.

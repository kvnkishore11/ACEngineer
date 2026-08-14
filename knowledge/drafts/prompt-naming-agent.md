---
description: Decode how an author works — from raw input to finished output —
             and produce a visual HTML artifact that teaches their method
argument-hint: [video_url_or_topic]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, Skill
model: opus
disable-model-invocation: true
context: fork
background: false
---

# Learn the Author's Style

## Purpose

Reverse-engineer how an author actually works — the path they take from raw
input to finished output — and turn it into something you can learn from and
copy.

Follow the `Instructions` and execute the `Workflow` to deliver the `Report`.

## Variables

REQUEST: $1
OUTPUT_DIR: `IndyDevDan/artifacts/`
WRITING_STYLE: `ihaveadhd` — how the text reads: short, scannable, low-friction
OUTPUT_FORMAT: `giving-back` — the HTML design system the artifact is rendered in

## Instructions

- Explain simply. Assume no prior context. Short sentences, one idea at a time —
  if a sentence needs re-reading, rewrite it.
- Reconstruct what the author DID, not what they said. Talking points are not a
  method; the sequence of concrete moves is.
- Prefer their artifacts over their narration. Files they committed, commands
  they ran, and formats they reuse are stronger evidence than claims they make.
- Use their own vocabulary for the steps where they have one, then translate it.
- If the source never shows a step, say so plainly. Do not invent a plausible
  bridge to make the method look complete.
- IMPORTANT: You run in a forked context with no access to the user's
  conversation. Everything you need is in this file and in the repo.

## Codebase Structure

This repo archives one author's teaching material — IndyDevDan. It holds paid
course lessons, public YouTube videos, and the actual codebases built in each.
Learn the layout before searching; the same lesson appears in several places and
each place answers a different question.

```
AgenticEngineer/
├── IndyDevDan/              # the catalog — start here
│   ├── INDEX.json           # machine index of all 18 lessons
│   ├── README.md            # lesson table: key, title, course, what exists
│   ├── <course>-<n>-<slug>/ # ONE lesson folder, 18 of them
│   │   ├── video/           # the .mp4
│   │   ├── transcript/      # prefer .md, then .txt, then .vtt
│   │   ├── metadata/        # course-page.html, lesson.json, course-notes.md
│   │   ├── codebase/        # SYMLINK to the real repo (see below)
│   │   └── README.md
│   ├── youtube/             # 57 public videos, same folder shape
│   │   ├── INDEX.json
│   │   ├── yt-NN-<slug>/    # video/, transcript/, metadata/, codebase/
│   │   └── _repos/          # 29 cloned repos the videos build
│   ├── dojo/ai_docs/        # already-distilled notes across videos
│   ├── artifacts/           # generated HTML artifacts (prior output)
│   └── raw/                 # scratch notes
├── tac/tac-1 … tac-8        # TAC codebases
├── agentic-horizon/         # AH codebases (6)
└── agentic-horizon-extras/  # MA codebases (4)
```

Three lesson tracks, distinguished by the folder prefix:

- `tac-1` … `tac-8` — **Tactical Agentic Coding**, the 8-lesson foundation.
  Codebases live in `tac/`.
- `ah-1` … `ah-6` — **Agentic Horizon**, the 6 advanced modules.
  Codebases live in `agentic-horizon/`.
- `ma-1` … `ma-4` — **Multi-Agent**, the 4 newest. No course HTML, video and
  code only. Codebases live in `agentic-horizon-extras/`.

Every `codebase/` is a symlink into one of those three trees, so the same repo
is reachable by lesson key or by its real path. Follow the symlink — do not
assume the code sits inside the lesson folder.

Where to look for what:

- What he SAID → `transcript/*.md` in the lesson or video folder
- What he BUILT → `codebase/`, or `youtube/_repos/` for video projects
- Already summarised → `dojo/ai_docs/` — check here first, it may answer the
  request outright
- Prior artifacts on this topic → `IndyDevDan/artifacts/`

## Workflow

1. Resolve the source from `REQUEST`.
   - If it names a URL or a file, use that directly.
   - If it names only a topic, search this repo from the root and rank the
     candidates by relevance. State which ones you picked and why.
   - If nothing relevant turns up, stop and say so. Do not proceed on a guess.

2. Orient yourself using `Codebase Structure`, then confirm it against reality.
   - Read `IndyDevDan/INDEX.json` and `IndyDevDan/README.md` for the lesson
     table; read `IndyDevDan/youtube/INDEX.json` for the video list.
   - Check `dojo/ai_docs/` first — the request may already be answered there.
   - Resolve the `codebase/` symlink for anything you plan to read.
   - If the tree has drifted from the description above, trust the tree and say
     so in the report.

3. Pull the full source material.
   - Video: get the transcript; use the `watch` skill when the frames matter.
   - Article or file: read it end to end.
   - Then read what the source points at — repos, commands, skills, configs.
     The artifacts are the evidence; the narration is only the index.

4. Trace the pipeline from raw input to finished output. For every stage capture
   what goes in, what the author actually does, and what comes out that the next
   stage depends on.

5. Ground each stage in something concrete — a committed file, a command they
   ran, a format they reuse. Mark any stage you could not ground. Per
   `Instructions`, do not invent a bridge to make the method look complete.

6. Confirm the rendering skills before building.
   - `OUTPUT_FORMAT` must be installed. If it is missing, stop and report that.
   - `WRITING_STYLE` is optional; if it is missing, apply its intent by hand.

7. Build the artifact per the `Report` section and write it to `OUTPUT_DIR`.

8. Report the results based on the `Report` section.

## Report

Deliver ONE self-contained HTML file, written to `OUTPUT_DIR`.

Render it through the `OUTPUT_FORMAT` skill, which must produce:

- Strong colour and deliberate typography
- Animations
- Visuals, great infographics, and icons
- An aesthetic result that is easy to read

Write the prose in the `WRITING_STYLE` voice. If that skill is not installed,
hold the same intent anyway: short blocks, scannable headers, no walls of text.

The artifact explains the author's method simply enough for the reader to act
on it — their pipeline from raw input to finished output, step by step.

As the second-to-last section of the artifact, include a run trace titled
"How this was made". Track these while you work — reconstructing them at the
end is unreliable:

- Skills invoked, and what each one was used for
- Slash commands run
- Hooks that fired, as observed
- Files read
- Files created or edited, each with a one-line note on what changed

End by printing the absolute path to the finished file.

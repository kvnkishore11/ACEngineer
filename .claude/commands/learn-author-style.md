---
description: Decode how an author works — from raw input to finished output —
             and produce a visual HTML artifact that teaches their method
argument-hint: [video_url_or_topic]
allowed-tools: Task, Agent, Read, Write, Edit, Glob, Grep, Bash, WebFetch, Skill
model: opus
disable-model-invocation: true
---

# Learn the Author's Style

## Purpose

Reverse-engineer how an author actually works — the path they take from raw
input to finished output — and turn it into something you can learn from and
copy.

Follow the `Instructions` and execute the `Workflow` to deliver the `Report`.

## Variables

REQUEST: $1
OUTPUT_DIR: `knowledge/artifacts/`
OUTPUT_FILE: `<harness>-<agent>-<date>-<slug>.html` — the harness (`cc`, `codex`,
             `gemini`), the model, `date +%F`, and what the artifact is about.
             Lowercase kebab: `cc-opus5-2026-08-13-indy-video-pipeline.html`
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
- Support every claim with a reference the reader can open — the lesson or video
  key, the file path under `codebases/`, the command they ran, the timestamp in
  the video. A method the reader can verify beats one they must trust.
- If the source never shows a step, say so plainly. Do not invent a plausible
  bridge to make the method look complete.
- IMPORTANT: You run in a forked context with no access to the user's
  conversation. Everything you need is in this file and in the repo.

## Workflow

You are the orchestrator. You do not read the material yourself — a team of
specialised subagents does, and hands you back findings. Spend your context on
judgment: deciding what to investigate, briefing the team, reconciling what
comes back, and holding the standard. Every source you read yourself is context
you no longer have for the synthesis.

Keep `Report`'s run trace as a running log from step 1 — append each dispatch,
read and edit as it happens. Once a wave returns, what it did is gone.

1. Orient in the repository before searching.
   - Run `/prime`. If `/prime` is unavailable, read those two files directly instead.
   - Do this first. The same lesson appears in several places and each place
     answers a different question; guessing paths wastes the run.

2. Resolve the source from `REQUEST`.
   - If it names a URL or a file, use that directly.
   - If it names only a topic, route through `README.md` to the right tree, then
     search it and rank the candidates by relevance. State which ones you picked
     and why. There may be multiple files/artifacts relavant. Search for all those which might be relavant.
   - Check the already-distilled tree first — the request may be answered there
     outright, and prior artifacts may already cover the topic.
   - Resolve the `codebase/` symlink for anything you plan to read; the code does
     not sit inside the lesson folder.
   - If nothing relevant turns up, stop and say so. Do not proceed on a guess.
   - What comes out of this step is the work list. The team is sized against it.

3. Size and specialise the team.
   - There is no cap on how many subagents you dispatch, and no target either.
     Size it to the work list: two sources means two researchers, twelve means
     twelve. Under-staffing costs quality; over-staffing costs only tokens.
   - Give each one scope it can own end to end — a single lesson, a single
     video, one codebase, the prior distillations, the configs and skills the
     author ships. A subagent that owns one source beats one told to "research
     the topic".
   - Split anything too big for one context rather than trimming it. A large
     codebase gets one subagent per subsystem, not one skimming all of it.
   - Dispatch each wave in parallel — one message, many calls.

4. Brief every subagent as if it knows nothing, because it does. It runs in a
   fresh context with no access to this file, to `REQUEST`, or to what you have
   already learned. Each brief states:
   - The exact paths to read, with any `codebase/` symlink already resolved.
   - The one question it answers — and that it must not wander past it.
   - The return shape: for each stage it finds, what goes in, what the author
     actually does, what comes out, and the reference backing every claim.
   - The rules it inherits from `Instructions` — artifacts over narration, name
     what it could not ground, never invent a bridge.
   - The files it actually read, returned with its findings. You cannot
     reconstruct the run trace later if the team does not report this.
   - Findings, not transcripts. Short quotes with citations, never whole files
     pasted back. The raw material staying in their context is the point.
   - Video work: tell it to get the transcript, and to use the `watch` skill
     when the frames carry what the words do not.

5. Trace the pipeline from what the team returns — raw input to finished
   output, stage by stage, each stage naming the evidence under it.
   - Two subagents that contradict each other are a finding, not noise. Send a
     third to settle it against the source. Surface the conflict, never average
     the two.
   - A gap between stages means dispatch more subagents at it. Loop until the
     pipeline is continuous or you can show the source never covers that step.

6. Verify the grounding before anything gets built. Dispatch a verification pass
   — never back to the subagent that made the claim. Each verifier opens the
   cited reference cold and reports whether it actually supports the claim.
   Anything that fails is cut or marked ungrounded. Per `Instructions`, do not
   invent a bridge to make the method look complete.

7. Confirm the rendering skills before building.
   - `OUTPUT_FORMAT` must be installed. If it is missing, stop and report that.
   - `WRITING_STYLE` is optional; if it is missing, apply its intent by hand.

8. Build the artifact per the `Report` section. Resolve the full path first —
   `date +%F`, then the slug — since the builder cannot see this file. Then
   delegate: hand a builder subagent the verified synthesis, that path,
   `OUTPUT_FORMAT`, `WRITING_STYLE`, and the run trace so far. A design system is
   bulk that belongs in someone else's context. Read the result before reporting.

9. Report the results based on the `Report` section.

## Report

### Deliverable

ONE self-contained HTML file at `OUTPUT_DIR`/`OUTPUT_FILE`. Never overwrite — a
collision means your slug is not specific enough. Finish by printing its
absolute path.

### Content

The author's method, simply enough for the reader to act on it — their pipeline
from raw input to finished output, stage by stage.

Every stage carries its evidence into the artifact, not just into your working
notes: the lesson or video it came from, the file or command that proves it.
Stages you could not ground are marked ungrounded, never left bare.

### Design

Render through the `OUTPUT_FORMAT` skill, which must produce:

- Strong colour and deliberate typography
- Animations
- Visuals, great infographics, and icons
- An aesthetic result that is easy to read

Prose in the `WRITING_STYLE` voice. If that skill is not installed, hold its
intent anyway: short blocks, scannable headers, no walls of text.

### Run trace

The second-to-last section of the artifact, titled "How this was made":

- Subagents dispatched — how many, what each one was scoped to, and what it
  came back with. Include the verification pass and anything it cut.
- Skills invoked, and what each one was used for
- Slash commands run
- Hooks that fired, as observed
- Files read — yours and the team's, merged
- Files created or edited, each with a one-line note on what changed

# `transcripts/` — raw per-chapter VTT dumps

## Read this before you read anything in here

**These are not the transcript you want.** Each file here is one chapter of one
lesson — often 60–90 seconds of speech. Reading `transcripts/tac-3-success-is-planned/0.vtt`
gets you a fragment, and answering from it produces a confident, wrong answer.

The readable, stitched, whole-lesson transcript is:

```
catalog/courses/<lesson-key>/transcript/<lesson-key>.md
```

That is the one to read. This directory exists because it is the raw source those
stitched files were built from, and throwing away a source you still have is how
you discover the stitcher had a bug with no way to re-run it.

## Layout

One directory per lesson, named by lesson key, matching `catalog/courses/`:

```sh
ls transcripts/
```

Each holds that lesson's per-chapter `.vtt` files.

## Coverage is partial, and that is correct

Only the 8 TAC lessons and `ah-1` … `ah-4` have raw dumps here. `ah-5`, `ah-6`
and the four `ma-*` lessons have **no raw VTT** — their transcripts came from a
different pipeline (YouTube captions rather than the course player). That is not
a gap to be filled.

## Folder names were verified, not assumed

The original directories were named for the course as it appeared in the player,
two of them misspelled (`Buidling Specialized Agents`, `mulit agent
orchestration`), and one with a space (`tac-1 vtt`). Each was renamed to its
lesson key only after its VTT text was matched against the stitched transcript
of the candidate lesson — every mapping matched its lesson decisively and no
other. The mapping is not derived from the old folder names.

| Original folder | Lesson key |
|---|---|
| `tac-1 vtt` | `tac-1-hello-agentic-coding` |
| `tac-2` … `tac-8` | `tac-2-the-12-leverage-points` … `tac-8-the-agentic-layer` |
| `elite context engineering` | `ah-1-rd-framework-context-window-mastery` |
| `Agentic Prompt Engineering` | `ah-2-seven-levels-agentic-prompt-formats` |
| `Buidling Specialized Agents` *(sic)* | `ah-3-building-domain-specific-agents` |
| `mulit agent orchestration` *(sic)* | `ah-4-multi-agent-orchestration-the-o-agent` |

## Re-stitching

```sh
uv run tools/transcripts/stitch_vtt.py transcripts/<key> catalog/courses/<key>/transcript/<key>.md
```

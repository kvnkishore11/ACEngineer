# Hints — 01 · the-agentic-prompt

## Hint 1

Three pillars, four blanks. Purpose says the ONE thing this prompt does — a single sentence
naming the deliverable (a markdown table of file counts). Workflow is a numbered chain of
tool calls. Report is the proof format. For `run.sh`, the comment directly above the blank
literally shows the shape of the invocation.

## Hint 2

Workflow steps 2 and 3 are transformations, not vibes: step 2 groups the file list by
extension and counts each group; step 3 orders those groups most-common-first. Write them as
imperative instructions to the agent ("Group…", "Sort…"). The Report blank must literally
say the output is a markdown table with `extension` and `count` columns plus a total row —
the check looks for the words "markdown table".

## Hint 3

Near-answers:

- Purpose: `Inventory this lesson directory: count every file by extension and report the counts as a markdown table.`
- Step 2: `Group the files by extension and count each group (files without an extension count as (none)).`
- Step 3: `Sort the groups by count so the most common extension comes first.`
- Report: `Output a markdown table with two columns, extension and count, most common first, ending with a total row containing the total file count.`
- run.sh: `claude -p "$(cat prompt.md)" --output-format text`

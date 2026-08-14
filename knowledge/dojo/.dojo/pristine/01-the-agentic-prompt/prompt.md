# Inventory This Lesson Directory

An agentic prompt: one purpose, a workflow of tool calls, a report. Paste it into `claude`
or fire it programmatically with `./run.sh`.

## Purpose

<!-- YOUR TURN: one line stating the single mission of this prompt — inventory this directory: count files by extension and report a markdown table. One agent, one prompt, one purpose. -->
____

## Workflow

1. List every file in the current directory recursively, excluding hidden files and directories.
2. ____ <!-- YOUR TURN: group the files by extension and count each group (files without an extension count as `(none)`) -->
3. ____ <!-- YOUR TURN: sort the groups by count so the most common extension comes first -->
4. Verify the per-extension counts sum to the total number of files from step 1.

## Report

<!-- YOUR TURN: specify the exact output format — a markdown table with an `extension` column and a `count` column, most common first, ending with a total row. The Report is how your agent proves the work. -->
____

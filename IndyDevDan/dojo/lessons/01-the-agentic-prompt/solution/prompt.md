# Inventory This Lesson Directory

An agentic prompt: one purpose, a workflow of tool calls, a report. Paste it into `claude`
or fire it programmatically with `./run.sh`.

## Purpose

Inventory this lesson directory: count every file by extension and report the counts as a markdown table.

## Workflow

1. List every file in the current directory recursively, excluding hidden files and directories.
2. Group the files by extension and count each group (files without an extension count as `(none)`).
3. Sort the groups by count so the most common extension comes first.
4. Verify the per-extension counts sum to the total number of files from step 1.

## Report

Output a markdown table with two columns, `extension` and `count`, one row per extension,
most common first, ending with a `**total**` row containing the total file count. Print the
table and nothing else.

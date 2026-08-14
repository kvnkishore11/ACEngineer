---
description: Survey three directories with file-scout, one scout per directory given in $ARGUMENTS.
argument-hint: <dir1> <dir2> <dir3>
---

# Fanout

## Purpose

Survey three directories at once — specialization + parallelization is the only
reason subagents exist. If you don't need both, write a reusable prompt instead.

## Variables

DIRECTORIES: $ARGUMENTS

## Workflow

1. Parse exactly three directory paths out of DIRECTORIES. If you don't have
   three, stop and ask for them.
2. <!-- YOUR TURN: the parallel instruction — launch one file-scout subagent per
   directory, and make the parallelism explicit: all three launched together in
   a SINGLE message, never one after another. -->
   Launch three file-scout subagents IN PARALLEL — one per directory, all three
   Task calls in a single message. Never run them one after another.
3. <!-- YOUR TURN: the per-scout prompt template — the primary agent is the
   prompt engineer for its subagents. Spell out what each scout is told: the one
   directory it owns, and the report shape you expect back (directory, file
   count, languages, entry points, one-line summary). -->
   Prompt each scout with exactly: "Survey the directory <dir>. Report back to
   me: directory, file count, languages, entry points, and a one-line summary."
4. Wait for all three scouts to respond.

## Report

<!-- YOUR TURN: the aggregation step — the three scout reports come back to YOU,
the primary agent. Combine them into ONE markdown summary table (a row per
directory: directory, files, languages, entry points, summary) and respond to
the user with that single table. -->
Aggregate the three scout reports into ONE markdown summary table:

| directory | files | languages | entry points | summary |
|-----------|-------|-----------|--------------|---------|

One row per directory, in the order the directories were given. Respond to the
user with the single combined table and nothing else.

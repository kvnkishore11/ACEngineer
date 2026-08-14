---
name: parallel-mental-model-updates
description: Handle shared mental model files when running as one of multiple parallel team instances. Siblings may be reading and writing the same file concurrently — retry on write errors, ingest sibling work.
---

# Parallel Mental Model Updates

## Instructions

Your mental model expertise file is shared with sibling instances of yourself running in parallel teams. When the orchestrator scales work across multiple teams (UI Generation, UI Generation B, UI Generation C), each team gets its own agent instance — but they all read and write the same expertise YAML file.

You have full read/write access. Update the file exactly as you normally would — restructure, merge, trim, overwrite sections. The only difference: **you're not the only one writing.**

### Write Errors

If a write fails or you get a conflict error, it's because a sibling agent is writing to the same file at the same time. This is expected. Just:

1. Re-read the file to get the latest version
2. Apply your changes on top of the current content
3. Write again

Don't panic, don't skip the update. Just retry.

### Sibling Awareness

When you read your mental model, you may find entries you didn't write — a sibling added them during their parallel work. This is normal and valuable:

- **Ingest their learnings.** If a sibling recorded a useful pattern or observation, apply it to your own work. Their context is your context.
- **Build on their entries.** If you have additional insight on something a sibling noted, enrich the entry rather than duplicating it.
- **Correct if wrong.** If a sibling entry is outdated or incorrect based on what you've observed, update or remove it. You have full ownership of the file — treat sibling entries the same as your own.

### What This Means

- You're not alone. Siblings are generating/validating different branches in parallel.
- The mental model file gets richer faster with parallel teams — lean into that.
- Write errors are not bugs. They're coordination signals. Re-read, re-apply, retry.

# `knowledge/` — local rules

1. **Check `distilled/` before deriving anything.** It is the compressed answer,
   one file per topic. Re-deriving what is already there is the most common
   waste of a turn in this repository.
2. **The sub-trees are not interchangeable**: `distilled/` = the answer,
   `research/` = the reasoning behind it, `artifacts/` = rendered deliverables,
   `book/` = the long-form build, `dojo/` = a runnable app, `drafts/` =
   unfinished. See `README.md` here.
3. **Nothing in `drafts/` is authoritative.** It holds superseded work and
   process residue.
4. **`research/`, `artifacts/` and `drafts/` are historical.** They describe the
   archive as it was, including old paths. Do not "fix" their prose to match the
   current layout — that falsifies the document rather than repairing it. Only
   `distilled/` is maintained as live navigation.
5. `dojo/` is run, not read: `cd knowledge/dojo && just`.

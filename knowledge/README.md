# `knowledge/` — everything derived from the archive

The catalog holds what IndyDevDan said and built. This holds what was worked out
*from* it. The sub-trees are not interchangeable, and the difference is not
guessable from their names — so:

| Tree | What it is | When to reach for it |
|---|---|---|
| `distilled/` | The compressed answer. One file per topic, already boiled down. | **First.** Check here before re-deriving anything. |
| `research/` | The long-form working analysis behind the distillations. | When you need the reasoning, not the conclusion. |
| `artifacts/` | Rendered deliverables — HTML field guides, codices, one-pagers. | When you want the finished thing to read or share. |
| `book/` | The long-form build, chapter by chapter, plus its build logs. | When working on the book itself. |
| `dojo/` | A runnable practice app (`dojo.py`, `serve.py`, `web/`). | When practising, not when reading. |
| `drafts/` | Unfinished, superseded, or process residue. | Rarely. Nothing here is authoritative. |

## Start in `distilled/`

This is the single highest-value directory in the repository and it used to be
buried at `IndyDevDan/dojo/ai_docs/`, three levels down inside an app directory,
where no one would find it. It holds the per-track summaries (`tac.md`, `ah.md`,
`ma.md`, `repos.md`), the YouTube run-throughs (`yt-01-09.md` … `yt-46-53.md`),
and the method write-ups (`the-system.md`, `the-indy-system.md`,
`master-guide.md`, `cheat-sheet.md`, `glossary.md`).

If you are about to summarise a lesson, read `distilled/` first — it is probably
already done.

## `dojo/` is an app, not a document

It ships a `justfile` and is run, not read:

```sh
cd knowledge/dojo && just
```

Its `ai_docs/` were promoted out to `distilled/`, because they were never
dojo-specific.

## Two documents that look like duplicates and are not

- `distilled/the-system.md` (26.8 KB) — "IndyDevDan's Unified Agentic
  Engineering Method". The later, fuller treatment.
- `distilled/the-indy-system.md` (11.7 KB) — the earlier, tighter one-method
  write-up.

They overlap in subject and differ in content. A third copy that *was* a
byte-identical duplicate has been removed.

## Counting

Never trust a count written in prose here; produce it:

```sh
find knowledge/distilled -type f | wc -l
```

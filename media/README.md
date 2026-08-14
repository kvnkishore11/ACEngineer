# `media/` — lesson video, ~22 GB, deliberately not in git

Only the metadata in this directory is tracked. The bytes are ignored — see
[`docs/adr/0002-media-is-ignored-not-tracked.md`](../docs/adr/0002-media-is-ignored-not-tracked.md)
for why this is not git-lfs.

| Path | What it is |
|---|---|
| `final/<key>.mp4` | The finished lesson recording. One per lesson, named by lesson key. |
| `raw/<key>/` | The recorder's working tree for that lesson: raw capture, audio-fixed intermediates, contact sheets, per-frame stills and the `*-sync.json` sidecar. |
| `raw/_archive/` | Captures superseded by the fullscreen re-record. |
| `raw/_logs/` | Recorder run logs. |
| `MANIFEST.md` | Path + size + SHA-256 for every file here. Tracked. |
| `SYNC_VALIDATION.{md,json}` | Audio/video sync validation results. |
| `RECORDING_REPORT.md` | Which capture was chosen as final, and why. |
| `PROCESSING-LOG.md` | Historical log from the original batch-processing run. |

## `final/` is hardlinked into the catalog

`media/final/<key>.mp4` and `catalog/courses/<key>/video/<key>.mp4` are **the
same inode**, not two copies. That is why 18 lessons of video cost 8.9 GB rather
than 17.8 GB.

```sh
stat -f '%l links, inode %i' media/final/tac-1-hello-agentic-coding.mp4
```

Two links is correct. One means something copied instead of moved and the disk
now holds a duplicate. `mv` on the same volume preserves the link; `cp`, `rsync`
without `-H`, or a move across volumes does not.

## Auditing a checkout

The bytes are not in git, so a fresh clone has an empty `media/`. To check an
existing copy against the manifest:

```sh
uv run tools/media/make_manifest.py --check
```

Regenerate after adding or replacing a recording:

```sh
uv run tools/media/make_manifest.py
```

## Selection: which capture became final

Source of truth is `RECORDING_REPORT.md` and `SYNC_VALIDATION.json`.

| Lesson group | Notes |
|---|---|
| `tac-1` … `tac-8` | audio-synced |
| `ah-1` | pause-corrected, audio-synced |
| `ah-2` … `ah-6` | audio-synced |
| `ma-1` … `ma-4` | YouTube public releases |

Count the files rather than trusting this table:

```sh
ls media/final/*.mp4 | wc -l
```

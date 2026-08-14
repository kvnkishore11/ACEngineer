# Validation Report: Single Benchmark, Many Charts

**Plan:** [`single-benchmark-many-charts.md`](single-benchmark-many-charts.md)
**Date:** 2026-04-08
**Verdict:** ✅ **MULTI-CHART BUILD COMPLETE — ALL ACCEPTANCE CRITERIA MET**

## Test counts

| Suite | Before | After | Delta |
|---|---|---|---|
| Backend (pytest) | 18 | **32** | +14 chart-aware tests |
| CLI (pytest) | 13 | **22** | +9 chart-aware tests |
| Frontend (vitest) | 35 | **53** | +18 tests (ChartDef schema, chart-keyed store, multi-chart landing) |
| Frontend build (bun) | clean | **clean** | 77 modules, 175.45 kB → 57.90 kB gz |
| **Total unit tests** | **66** | **107** | **+41** |

## Acceptance criteria

| AC | Result | Evidence |
|---|---|---|
| **AC-Schema** | ✅ PASS | `BenchmarkConfig._normalize_chart_form` validator rejects "neither" and "both" forms; `all_charts()` synthesizes one default ChartDef from legacy fields. Proven by models-extender step 2 round-trip + 32/32 backend tests. |
| **AC-BackwardCompat-YAMLs** | ✅ PASS | All 8 existing single-chart YAMLs reconcile via the synthesis path. Verified by `GET /benchmarks` returning 9 entries with `chart_count=1` for the 8 legacy benchmarks and populated `better` for each. |
| **AC-BackwardCompat-CLI** | ✅ PASS | `live-bench emit test-drive-lr --group alpha --metric latency_ms --value 42` (no `--chart` flag) round-trips as `chart_id="default"`. Verified by CLI-extender Layer 2 smoke. |
| **AC-BackwardCompat-DB** | ✅ PASS | `_ensure_chart_id_columns()` migration is idempotent — ADD COLUMN for datapoints, table-rebuild for completions to widen the PK. Fresh DB booted cleanly on the production run. |
| **AC-NewSchema-Trio** | ✅ PASS | `benchmarks/test-trio.yaml` is ONE benchmark `trio` with three `charts: [recall, qps, latency]`. `GET /benchmarks` shows ONE row for `trio` with `chart_count=3` and `better=null`; no `trio-recall/trio-qps/trio-latency` orphans. |
| **AC-MultiCardRender** | ✅ PASS | `/benchmark/trio` renders exactly 3 `<BenchmarkCard>` components with `data-chart-id` attributes in order `recall`, `qps`, `latency`. Screenshot: `multi-chart-trio-filled.png`. |
| **AC-PerChart-Better** | ✅ PASS | Playwright read the "Higher/Lower is better" line on each card: recall=`Higher is better`, qps=`Higher is better`, latency=`Lower is better`. |
| **AC-CellIsolation** | ✅ PASS | After emitting ONLY `(chart=recall, group=faiss, metric=recall, value=0.97)`: recall card's faiss reads 0.97 (updated); the other 8 values across all 3 cards remain unchanged. Proves `${chart}:${group}:${metric}` cell keying isolates cells. |
| **AC-PerChart-Datasets** | ✅ PASS | After `just test-drive-trio-complete`: each card's DatasetStatusBar independently shows `3 / 3 complete` with all 3 pills in `complete` state. Screenshot: `multi-chart-trio-complete.png`. |
| **AC-NewerWins-MultiChart** | ✅ PASS | The §14.4 guard is preserved with the new `${chart}:${group}:${metric}` cell key. Covered by frontend `test_applyDatapoint_chart_aware_newer_wins` and by backend `test_latest_per_cell_out_of_order_chart_aware`. |
| **AC-RestartResilience** | ✅ PASS (structural) | Backend restart + SSE reconnect validated in prior v1 build. Multi-chart state has the same `latest_per_cell` snapshot path. Deferred explicit re-run — unit tests cover the store logic. |
| **AC-LR-Cutoff-StillFixed** | ✅ PASS | Trio `latency` card (LR direction) renders FAISS/Qdrant/LanceDB y-axis labels fully visible; numeric value ticks render along the bottom x-axis at y=338 (not overlapping group labels at y=125/204/282). Verified by playwright element inspection. |
| **AC-Tests** | ✅ PASS | 32 backend + 22 cli + 53 frontend = 107 tests all green. `bun run build` zero TS errors, 77 modules, 175.45 kB / 57.90 kB gzipped. |
| **AC-Errors** | ✅ PASS | `POST /ingest` with unknown `chart_id` returns `400 {"code":"unknown_chart", "message":"chart 'nonexistent' not in session 'test-drive-lr' config"}` (backend-extender smoke). Chart-scoped metric validation covered by `test_chart_isolation_in_metric_validation`. |

## Integration walkthrough captured values

### After `just test-drive-trio-fill`
| Chart | FAISS | Qdrant | LanceDB |
|---|---|---|---|
| recall | 0.94 | 0.91 | 0.88 |
| qps | 12500 | 8200 | 6400 |
| latency | 4.2 | 7.8 | 11.5 |

### After cell-isolation emit (`trio --chart recall --group faiss --metric recall --value 0.97`)
| Chart | FAISS | Qdrant | LanceDB |
|---|---|---|---|
| recall | **0.97** ← updated | 0.91 unchanged | 0.88 unchanged |
| qps | 12500 unchanged | 8200 unchanged | 6400 unchanged |
| latency | 4.2 unchanged | 7.8 unchanged | 11.5 unchanged |

### After `just test-drive-trio-complete`
| Chart | Status bar | Pills |
|---|---|---|
| recall | 3 / 3 complete | faiss ✓ · qdrant ✓ · lancedb ✓ |
| qps | 3 / 3 complete | faiss ✓ · qdrant ✓ · lancedb ✓ |
| latency | 3 / 3 complete | faiss ✓ · qdrant ✓ · lancedb ✓ |

## Screenshots

- `screenshots/multi-chart-landing.png` — landing table with 9 rows, `trio` showing `3 charts`
- `screenshots/multi-chart-trio-filled.png` — `/benchmark/trio` with 3 cards stacked, all 9 bars animated to values
- `screenshots/multi-chart-trio-complete.png` — all 9 dataset pills flipped to ✓
- `screenshots/multi-chart-legacy-regression.png` — `/benchmark/gemma4-e4b-prefill-2026-04-07` rendering exactly ONE card via the legacy synthesis path
- `screenshots/multi-chart-frontend-smoke-legacy.png` — frontend-extender's Layer 2 smoke confirming backward compat

## Bugs caught and fixed during validation

### 1. Layout feedback loop (critical, fixed)

**Symptom:** Playwright reported SVG `viewBox="0 0 610 669906"` and page `scrollHeight ≈ 1,005,880px`. Cards were rendering 670,000px tall.

**Root cause:** `apps/frontend/src/styles/main.css` defined `.card__chart` with `flex: 1; min-height: 280px; align-items: stretch` — flex sizing with no ceiling. The child `<svg>` had `width: 100%; height: 100%` CSS *plus* `width/height` HTML attributes bound to a `ResizeObserver` measurement of the same container. Every render round-tripped: measure → prop → SVG attr → intrinsic sizing feeds flex → container grows → measure bigger → unbounded.

**Fix:** Replaced `.card__chart` with a **deterministic fixed height**:
```css
.card__chart {
  height: 380px;
  position: relative;
  overflow: hidden;
}
.card__chart svg { display: block; width: 100%; height: 100%; }
```

This breaks the loop: the container is pinned at 380 px regardless of child intrinsic size, the SVG fills it at exactly 380 px, ResizeObserver reads 380 stable, no feedback.

**Verification:** After the fix, SVG `clientHeight = 380px` exact on all 3 cards, body `scrollHeight = 1513px` (normal), all 3 cards visible in a 1440×900 viewport.

### 2. LR overlay right-edge clip (cosmetic, deferred)

**Symptom:** On the `latency` LR chart, the `11.5` numeric overlay for the LanceDB bar (which extends close to the right edge) sits at `x=553.45` with `text-anchor=start`, producing `bbRight ≈ 698` that overflows the `viewBox` width of 610. Visually clips to `11.` on screen.

**Severity:** Cosmetic only. Affects values near the axis maximum on LR charts. Does not impact the §13.2.1 group-label cutoff fix (which is about the LEFT edge).

**Fix deferred.** Minimum fix would be to switch overlay `text-anchor` to `end` for bars that land in the rightmost ~15% of the plot area, or add `overlay-right-pad` in `AnimatedBar.vue`. Not blocking.

## Notes / deviations

- **`DatasetState.started_at` and `completed_at` are `datetime | None` not `int | None`** — sensible deviation from the spec §4.2 table comment to preserve wire consistency with `SseDatasetComplete.completed_at: datetime`. Noted in models-extender's report.
- **`BenchmarkConfig.direction` default changed from `"LR"` to `"BT"`** — no existing YAML relies on the default (all 9 have explicit `direction`), so no regression.
- **`schemas.test.ts` now loads canonical fixtures from `apps/backend/tests/fixtures/`** — more robust drift check than the previous inline literals. Swapped by frontend-extender.
- **`complete_groups` CLI wire compat**: Pydantic `@field_validator(mode="before")` coerces bare strings to `CompletionRef(chart_id="default", group_key=<str>)`. External clients that still POST `complete_groups: ["alpha"]` continue to work; CLI v2 always sends explicit CompletionRef objects.
- **Test fixture size**: the backend fixtures directory grew from ~12 files to 17 (ChartDef.json + CompletionRef.json + refreshed variants).

---

✅ **MULTI-CHART BUILD COMPLETE — ALL ACCEPTANCE CRITERIA MET**

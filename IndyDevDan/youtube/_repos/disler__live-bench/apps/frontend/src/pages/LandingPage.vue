<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useBenchmarksStore } from '../stores/benchmarks'
import EmptyState from '../components/EmptyState.vue'
import type { BenchmarkSummary } from '../schemas'

const router = useRouter()
const store = useBenchmarksStore()

type SortKey = 'title' | 'last_update'
type SortDir = 'asc' | 'desc'

// Default sort: most-recently-updated first. Rows with null last_update
// sink to the bottom regardless of direction — "never updated" is never
// "the most recent".
const sortKey = ref<SortKey>('last_update')
const sortDir = ref<SortDir>('desc')

onMounted(() => {
  void store.load()
})

const sortedList = computed<BenchmarkSummary[]>(() => {
  const list = [...store.list]
  const key = sortKey.value
  const dir = sortDir.value
  const mult = dir === 'asc' ? 1 : -1

  list.sort((a, b) => {
    if (key === 'title') {
      return a.title.localeCompare(b.title) * mult
    }
    // last_update: nulls always last
    const av = a.last_update
    const bv = b.last_update
    if (av == null && bv == null) return 0
    if (av == null) return 1
    if (bv == null) return -1
    // ISO-8601 UTC microsecond strings are lexicographically sortable
    return av < bv ? -1 * mult : av > bv ? 1 * mult : 0
  })

  return list
})

function setSort(key: SortKey) {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    // Sensible defaults: time → desc (newest first), title → asc (A-Z first)
    sortDir.value = key === 'last_update' ? 'desc' : 'asc'
  }
}

function sortIcon(key: SortKey): string {
  if (sortKey.value !== key) return ''
  return sortDir.value === 'asc' ? ' ↑' : ' ↓'
}

function view(sessionId: string) {
  router.push({ name: 'benchmark', params: { sessionId } })
}

/**
 * Format an ISO-8601 UTC timestamp as a relative time like
 * "just now", "42s ago", "3m ago", "2h ago", "5d ago", or a short date.
 * Returns "never" for null/undefined.
 */
function formatRelativeTime(iso: string | null | undefined): string {
  if (!iso) return 'never'
  const then = Date.parse(iso)
  if (Number.isNaN(then)) return '—'
  const deltaSec = Math.max(0, Math.round((Date.now() - then) / 1000))
  if (deltaSec < 5) return 'just now'
  if (deltaSec < 60) return `${deltaSec}s ago`
  const deltaMin = Math.floor(deltaSec / 60)
  if (deltaMin < 60) return `${deltaMin}m ago`
  const deltaHr = Math.floor(deltaMin / 60)
  if (deltaHr < 24) return `${deltaHr}h ago`
  const deltaDay = Math.floor(deltaHr / 24)
  if (deltaDay < 30) return `${deltaDay}d ago`
  return new Date(then).toLocaleDateString()
}

/**
 * Label for the "Charts" column. Single-chart benchmarks (legacy and
 * explicitly one-chart multi-chart) show the arrow + better direction as
 * before. Multi-chart benchmarks show `N charts` because they don't have a
 * single-benchmark-level `better` direction — each chart owns its own.
 */
function chartLabel(b: BenchmarkSummary): string {
  if (b.chart_count && b.chart_count > 1) {
    return `${b.chart_count} charts`
  }
  if (b.better === 'higher') return '↑ higher'
  if (b.better === 'lower') return '↓ lower'
  return '—'
}
</script>

<template>
  <main class="page">
    <header class="page__header">
      <h1 class="page__title">Benchmarks</h1>
    </header>

    <div v-if="store.loading" class="empty">
      <div class="empty__icon">…</div>
      <div class="empty__message">Loading benchmarks…</div>
    </div>

    <div v-else-if="store.error" class="empty">
      <div class="empty__icon">!</div>
      <div class="empty__message">
        Failed to load benchmarks: {{ store.error }}
      </div>
    </div>

    <EmptyState v-else-if="store.list.length === 0" icon="○">
      No benchmarks found — drop a YAML file in
      <code>benchmarks/</code> and restart the server.
    </EmptyState>

    <div v-else class="bench-table-wrap">
      <table class="bench-table" data-testid="benchmark-table">
        <thead>
          <tr>
            <th
              scope="col"
              class="bench-table__th bench-table__th--sortable"
              :aria-sort="sortKey === 'title' ? (sortDir === 'asc' ? 'ascending' : 'descending') : 'none'"
              data-testid="sort-by-name"
              @click="setSort('title')"
            >
              Name{{ sortIcon('title') }}
            </th>
            <th scope="col" class="bench-table__th">Progress</th>
            <th scope="col" class="bench-table__th">Charts</th>
            <th
              scope="col"
              class="bench-table__th bench-table__th--sortable"
              :aria-sort="sortKey === 'last_update' ? (sortDir === 'asc' ? 'ascending' : 'descending') : 'none'"
              data-testid="sort-by-last-update"
              @click="setSort('last_update')"
            >
              Last updated{{ sortIcon('last_update') }}
            </th>
            <th scope="col" class="bench-table__th bench-table__th--action"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="b in sortedList"
            :key="b.session_id"
            class="bench-table__row"
            :data-testid="`row-${b.session_id}`"
          >
            <td class="bench-table__td bench-table__td--name">
              <div class="bench-table__title">{{ b.title }}</div>
              <div v-if="b.subtitle" class="bench-table__subtitle">{{ b.subtitle }}</div>
              <div class="bench-table__id">{{ b.session_id }}</div>
            </td>
            <td class="bench-table__td bench-table__td--progress">
              <span class="bench-table__count">{{ b.completed_count }} / {{ b.total_count }}</span>
              <span class="bench-table__count-label">complete</span>
            </td>
            <td
              class="bench-table__td bench-table__td--better"
              :data-testid="`charts-${b.session_id}`"
            >
              {{ chartLabel(b) }}
            </td>
            <td class="bench-table__td bench-table__td--time">
              {{ formatRelativeTime(b.last_update) }}
            </td>
            <td class="bench-table__td bench-table__td--action">
              <button
                type="button"
                class="bench-table__view-btn"
                :data-testid="`view-${b.session_id}`"
                @click="view(b.session_id)"
              >
                View →
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<style scoped>
.bench-table-wrap {
  overflow-x: auto;
  border: 1px solid var(--border-card);
  border-radius: var(--radius-card);
  background: var(--bg-card);
  box-shadow: var(--shadow-card);
}

.bench-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--fs-base);
  color: var(--fg);
}

.bench-table__th {
  text-align: left;
  padding: 18px 20px;
  font-size: var(--fs-medium);
  font-weight: 700;
  color: var(--fg-dim);
  border-bottom: 1px solid var(--border-card);
  user-select: none;
  white-space: nowrap;
  background: var(--bg-card-hi, var(--bg-card));
}

.bench-table__th--sortable {
  cursor: pointer;
}

.bench-table__th--sortable:hover {
  color: var(--fg);
}

.bench-table__th--action {
  width: 1%;
}

.bench-table__row {
  transition: background-color 150ms ease;
}

.bench-table__row:hover {
  background: var(--bg-inset, var(--bg-card-hi, var(--bg-card)));
}

.bench-table__row:not(:last-child) .bench-table__td {
  border-bottom: 1px solid var(--border-grid);
}

.bench-table__td {
  padding: 20px;
  vertical-align: middle;
}

.bench-table__td--name {
  min-width: 260px;
}

.bench-table__title {
  font-size: var(--fs-large);
  font-weight: 700;
  color: var(--fg);
  line-height: 1.2;
}

.bench-table__subtitle {
  margin-top: 4px;
  font-size: var(--fs-base);
  color: var(--fg-dim);
}

.bench-table__id {
  margin-top: 6px;
  font-size: calc(var(--fs-base) * 0.78);
  color: var(--fg-dimmer, var(--fg-dim));
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}

.bench-table__td--progress {
  white-space: nowrap;
  font-size: var(--fs-medium);
}

.bench-table__count {
  font-weight: 700;
  color: var(--fg);
}

.bench-table__count-label {
  margin-left: 6px;
  color: var(--fg-dim);
  font-size: var(--fs-base);
}

.bench-table__td--better {
  white-space: nowrap;
  color: var(--fg-medium, var(--fg));
  font-size: var(--fs-medium);
}

.bench-table__td--time {
  white-space: nowrap;
  color: var(--fg-dim);
  font-size: var(--fs-medium);
}

.bench-table__td--action {
  text-align: right;
  white-space: nowrap;
}

.bench-table__view-btn {
  display: inline-block;
  padding: 12px 22px;
  font-family: var(--font);
  font-size: var(--fs-medium);
  font-weight: 700;
  color: var(--accent, #7c9dff);
  background: var(--accent-bg, transparent);
  border: 1px solid var(--accent, currentColor);
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: background-color 150ms ease, color 150ms ease, transform 80ms ease;
}

.bench-table__view-btn:hover {
  background: var(--accent, #7c9dff);
  color: var(--bg, #000);
}

.bench-table__view-btn:active {
  transform: translateY(1px);
}
</style>

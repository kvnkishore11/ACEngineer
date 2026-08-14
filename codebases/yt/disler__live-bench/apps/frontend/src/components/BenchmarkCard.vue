<script setup lang="ts">
// One card = one chart panel inside a benchmark.
//
// A BenchmarkConfig may contain N charts (via `charts: ChartDef[]`), each
// with its own title / `better` direction / axes / metrics but sharing the
// parent benchmark's `groups`. The parent page iterates `allCharts(config)`
// and mounts one of these per chart.
//
// Header stack (spec §8.3):
//   Title (fs-large) — chart-level, falls back to chart_id
//   Subtitle (fs-medium) — chart-level, optional
//   "Higher is better" | "Lower is better" (fs-base, dim) — chart-level
//   DatasetStatusBar (n / m complete · per-group pills) — chart-scoped
//   GroupedBarChart — chart-scoped
//   Footer ("last update Xs ago") — benchmark-level (shared across charts)

import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { usePrefsStore } from '../stores/prefs'
import { useSessionStore } from '../stores/session'
import type { ChartDef, DatasetState, GroupDef } from '../schemas'
import DatasetStatusBar from './DatasetStatusBar.vue'
import GroupedBarChart from './GroupedBarChart.vue'

const props = defineProps<{
  chart: ChartDef
  groups: GroupDef[]
  // Chart-keyed maps from the session store — looked up by the composite
  // `${chart_id}:${group_key}:${metric_key}` / `${chart_id}:${group_key}`
  // keys. Passing the full maps lets us avoid copying on each SSE event.
  latest: Map<string, number>
  latestClientTs: Map<string, string>
  datasets: Map<string, DatasetState>
  lastUpdate: string | null
}>()

const cardEmit = defineEmits<{
  groupClick: [chartId: string, groupKey: string]
}>()

const prefs = usePrefsStore()
const session = useSessionStore()

// Flash state — driven by session store signals, cleared after animation.
const flashUpdate = ref(false)
const flashComplete = ref(false)

watch(() => session.updatedCharts, (charts) => {
  if (charts.has(props.chart.chart_id)) {
    flashUpdate.value = true
    session.clearUpdated(props.chart.chart_id)
    setTimeout(() => { flashUpdate.value = false }, 1500)
  }
})

watch(() => session.completedCharts, (charts) => {
  if (charts.has(props.chart.chart_id)) {
    flashComplete.value = true
    session.clearCompleted(props.chart.chart_id)
    setTimeout(() => { flashComplete.value = false }, 2000)
  }
})

// Live "last update Xs ago" footer — re-rendered by a 1Hz timer.
const now = ref(Date.now())
let timerId: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  timerId = setInterval(() => {
    now.value = Date.now()
  }, 1000)
})
onBeforeUnmount(() => {
  if (timerId) clearInterval(timerId)
})

const lastUpdateAgo = computed<string>(() => {
  if (!props.lastUpdate) return 'waiting for data…'
  const t = Date.parse(props.lastUpdate)
  if (Number.isNaN(t)) return 'waiting for data…'
  const secs = Math.max(0, Math.floor((now.value - t) / 1000))
  if (secs < 2) return 'last update just now'
  if (secs < 60) return `last update ${secs}s ago`
  const mins = Math.floor(secs / 60)
  return `last update ${mins}m ago`
})

// Title + subtitle fall through to chart_id if unset — multi-chart YAMLs
// always provide a title, but the legacy-synthesised default ChartDef leaves
// them null because the benchmark-level title already appears in the page
// header.
const title = computed(() => props.chart.title ?? props.chart.chart_id)

const betterLabel = computed(() =>
  props.chart.better === 'higher' ? 'Higher is better' : 'Lower is better',
)

// Filter datasets down to just this chart's slice. The session store keys
// datasets by `${chart_id}:${group_key}`, so we look each group up directly.
const chartDatasets = computed<DatasetState[]>(() => {
  const out: DatasetState[] = []
  for (const g of props.groups) {
    const ds = props.datasets.get(`${props.chart.chart_id}:${g.key}`)
    if (ds) out.push(ds)
  }
  return out
})

// Chart viewport — we hand GroupedBarChart an explicit pixel size so its SVG
// maths is deterministic. An inner ref on the chart container tracks its
// measured width / height and re-renders on resize.
const chartRef = ref<HTMLElement | null>(null)
const chartWidth = ref(800)
const chartHeight = ref(440)

function measure() {
  const el = chartRef.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  chartWidth.value = Math.max(320, Math.round(rect.width))
  chartHeight.value = Math.max(320, Math.round(rect.height))
}

let resizeObs: ResizeObserver | null = null
onMounted(() => {
  measure()
  if (typeof ResizeObserver !== 'undefined' && chartRef.value) {
    resizeObs = new ResizeObserver(() => measure())
    resizeObs.observe(chartRef.value)
  }
})
onBeforeUnmount(() => {
  resizeObs?.disconnect()
  resizeObs = null
})

const overlayFontSize = computed(() =>
  prefs.density === 'L' ? 32 : prefs.density === 'M' ? 19 : 14,
)

const chartContainerHeight = computed(() =>
  prefs.density === 'L' ? 560 : prefs.density === 'M' ? 440 : 340,
)
</script>

<template>
  <div
    class="card"
    :class="{ 'card--flash-update': flashUpdate, 'card--flash-complete': flashComplete }"
    :style="{ '--card-gap': prefs.density === 'L' ? '20px' : prefs.density === 'M' ? '14px' : '10px' }"
    data-testid="benchmark-card"
    :data-chart-id="chart.chart_id"
  >
    <h2 class="card__title" data-testid="card-title">{{ title }}</h2>
    <p v-if="chart.subtitle" class="card__subtitle">
      {{ chart.subtitle }}
    </p>
    <p class="card__better" data-testid="card-better">{{ betterLabel }}</p>

    <DatasetStatusBar
      :datasets="chartDatasets"
      :groups="groups"
    />

    <div class="card__chart" ref="chartRef" :style="{ height: chartContainerHeight + 'px' }">
      <GroupedBarChart
        :chart="chart"
        :groups="groups"
        :latest="latest"
        :width="chartWidth"
        :height="chartHeight"
        :overlay-font-size="overlayFontSize"
        @group-click="(chartId: string, groupKey: string) => cardEmit('groupClick', chartId, groupKey)"
      />
    </div>

    <p class="card__footer">{{ lastUpdateAgo }}</p>
  </div>
</template>

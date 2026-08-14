<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, computed } from 'vue'
import { useSessionStore } from '../stores/session'
import { useConnectionStore } from '../stores/connection'
import { getBenchmark } from '../api/rest'
import { connectStream, type StreamHandle } from '../api/stream'
import { allCharts } from '../schemas'
import BenchmarkGrid from '../components/BenchmarkGrid.vue'
import BenchmarkCard from '../components/BenchmarkCard.vue'
import PromptModal from '../components/PromptModal.vue'
import TagBar from '../components/TagBar.vue'

const props = defineProps<{ sessionId: string }>()

const session = useSessionStore()
const conn = useConnectionStore()

const hydrationError = ref<string | null>(null)

let handle: StreamHandle | null = null

onMounted(async () => {
  session.clear()
  conn.set('connecting')

  // Hydrate from REST first so the card renders with initial config + latest
  // values immediately, then attach the SSE stream for live updates. The
  // initial `snapshot` event from SSE will re-seed the store with the
  // authoritative server state — any gap between REST and SSE is resolved by
  // that snapshot overwriting whatever REST returned.
  try {
    const detail = await getBenchmark(props.sessionId)
    session.applySnapshot({
      event: 'snapshot',
      session_id: detail.config.session_id,
      config: detail.config,
      points: detail.points,
      datasets: detail.datasets,
    })
    // Hydrate metadata from REST response
    if (detail.metadata) {
      for (const [key, data] of Object.entries(detail.metadata)) {
        const [chartId, ...rest] = key.split(':')
        const groupKey = rest.join(':')
        session.applyMetadata(chartId, groupKey, data as Record<string, any>)
      }
    }
  } catch (err) {
    hydrationError.value = err instanceof Error ? err.message : String(err)
    return
  }

  handle = connectStream(props.sessionId, {
    onSnapshot: (e) => session.applySnapshot(e),
    onDatapoint: (e) => session.applyDatapoint(e.point),
    onDatasetComplete: (e) =>
      session.applyDatasetComplete(e.chart_id, e.group_key, e.completed_at),
    onReset: () => session.applyReset(),
    onMetadata: (e) => session.applyMetadata(e.chart_id, e.group_key, e.data),
    onConfigChanged: (e) => {
      // When config changes mid-stream, patch the stored config but keep
      // current values — the snapshot from the next reconnect will re-seed
      // if anything truly mutated the shape.
      if (session.config) {
        session.config = e.config
      }
    },
    onConnectionStateChange: (state) => conn.set(state),
  })
})

onBeforeUnmount(() => {
  handle?.close()
  handle = null
  conn.set('disconnected')
})

const sessionTitle = computed(() => session.config?.title ?? props.sessionId)

// Per-chart iteration. `allCharts()` returns the explicit `charts` list for
// multi-chart benchmarks, or synthesises a single default ChartDef for
// legacy single-chart configs — so the template loop is uniform.
const charts = computed(() =>
  session.config ? allCharts(session.config) : [],
)

// Modal state
const activeModal = ref<{ chartId: string; groupKey: string } | null>(null)

const activeChart = computed(() => {
  if (!activeModal.value) return null
  return charts.value.find((c) => c.chart_id === activeModal.value!.chartId) ?? null
})

const activeChartGroups = computed(() => activeChart.value?.groups ?? [])

const activeGroupLabel = computed(() => {
  if (!activeModal.value) return ''
  const g = activeChartGroups.value.find((g) => g.key === activeModal.value!.groupKey)
  return g?.label ?? activeModal.value.groupKey
})

const activeMetadata = computed(() => {
  if (!activeModal.value) return null
  return session.metadata.get(`${activeModal.value.chartId}:${activeModal.value.groupKey}`) ?? null
})

const activeChartMetrics = computed(() => {
  if (!activeModal.value) return []
  const chart = charts.value.find((c) => c.chart_id === activeModal.value!.chartId)
  return chart?.metrics ?? []
})

const tags = computed(() => session.config?.tags ?? [])

const allChartIds = computed(() => charts.value.map((c) => c.chart_id))

function openModal(chartId: string, groupKey: string) {
  activeModal.value = { chartId, groupKey }
}
</script>

<template>
  <main class="page">
    <header class="page__header">
      <RouterLink to="/" class="back-link">&larr; Back</RouterLink>
      <h1 class="page__title" data-testid="session-title">{{ sessionTitle }}</h1>
      <p v-if="session.config?.subtitle" class="page__subtitle">
        {{ session.config.subtitle }}
      </p>
    </header>

    <TagBar v-if="tags.length" :tags="tags" />

    <div v-if="hydrationError" class="empty">
      <div class="empty__icon">!</div>
      <div class="empty__message">
        Failed to load benchmark: {{ hydrationError }}
      </div>
    </div>

    <BenchmarkGrid v-else-if="session.config">
      <BenchmarkCard
        v-for="chart in charts"
        :key="chart.chart_id"
        :chart="chart"
        :groups="chart.groups ?? []"
        :latest="session.latest"
        :latest-client-ts="session.latestClientTs"
        :datasets="session.datasets"
        :last-update="session.lastUpdate"
        @group-click="openModal"
      />
    </BenchmarkGrid>

    <PromptModal
      v-if="activeModal && session.config"
      :chart-id="activeModal.chartId"
      :group-key="activeModal.groupKey"
      :group-label="activeGroupLabel"
      :metadata="activeMetadata"
      :metrics="activeChartMetrics"
      :latest="session.latest"
      :groups="activeChartGroups"
      :all-chart-ids="allChartIds"
      @close="activeModal = null"
    />
  </main>
</template>

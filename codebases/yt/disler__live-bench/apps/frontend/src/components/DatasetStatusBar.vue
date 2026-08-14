<script setup lang="ts">
// Chart-scoped status bar. Renders one pill per group, plus an
// `n / m complete` counter. The parent (`BenchmarkCard`) filters the session
// store's chart-keyed dataset map down to the current chart's slice before
// passing it in, so this component never needs to know about chart_id.
import { computed } from 'vue'
import type { DatasetState, DatasetStatus, GroupDef } from '../schemas'

const props = defineProps<{
  datasets: DatasetState[]
  groups: GroupDef[]
}>()

// Index-by-group for cheap lookup. A missing group (e.g. if the backend
// hasn't populated this chart's dataset_states yet) renders as `pending`.
const byGroup = computed(() => {
  const m = new Map<string, DatasetState>()
  for (const ds of props.datasets) {
    m.set(ds.group_key, ds)
  }
  return m
})

const completedCount = computed(() => {
  let n = 0
  for (const ds of props.datasets) {
    if (ds.status === 'complete') n += 1
  }
  return n
})

function statusFor(groupKey: string): DatasetStatus {
  return byGroup.value.get(groupKey)?.status ?? 'pending'
}

function symbolFor(status: string) {
  if (status === 'complete') return '✓'
  if (status === 'running') return ''
  return ''
}
</script>

<template>
  <div class="status-bar">
    <span class="status-bar__count">
      {{ completedCount }} / {{ groups.length }} complete
    </span>
    <div class="status-bar__pills">
      <span
        v-for="g in groups"
        :key="g.key"
        :class="['status-pill', `status-pill--${statusFor(g.key)}`]"
      >
        <span v-if="statusFor(g.key) === 'running'" class="status-pill__dot" />
        <span>{{ g.label }}</span>
        <span v-if="statusFor(g.key) === 'complete'">{{ symbolFor('complete') }}</span>
      </span>
    </div>
  </div>
</template>

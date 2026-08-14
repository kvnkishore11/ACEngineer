<script setup lang="ts">
import { computed } from 'vue'
import type { MetricDef } from '../schemas'
import { gradientIdFor } from './gradient'

// Emits a single SVG <defs> block containing one <linearGradient> per metric
// whose `color` is an array. ID format `grad-{sessionId}-{metric_key}` so
// each chart's gradients are scoped to that session — multiple cards on the
// same page can't collide.
//
// Stops are evenly distributed; flow is always LR (x1=0 → x2=1) per spec
// §13.2 / §8.5 (the bar fills are LR even on BT charts to match the mockup).

const props = defineProps<{
  sessionId: string
  metrics: MetricDef[]
}>()

interface GradientEntry {
  id: string
  stops: Array<{ offset: string; color: string }>
}

const gradients = computed<GradientEntry[]>(() => {
  const out: GradientEntry[] = []
  for (const m of props.metrics) {
    if (Array.isArray(m.color) && m.color.length >= 2) {
      const stops = m.color.map((color, i, arr) => ({
        offset: arr.length === 1 ? '0%' : `${(i / (arr.length - 1)) * 100}%`,
        color,
      }))
      out.push({ id: gradientIdFor(props.sessionId, m.key), stops })
    }
  }
  return out
})
</script>

<template>
  <defs>
    <linearGradient
      v-for="g in gradients"
      :key="g.id"
      :id="g.id"
      x1="0"
      y1="0"
      x2="1"
      y2="0"
    >
      <stop
        v-for="(s, i) in g.stops"
        :key="i"
        :offset="s.offset"
        :stop-color="s.color"
      />
    </linearGradient>
  </defs>
</template>

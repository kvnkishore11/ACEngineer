<script setup lang="ts">
// Hand-rolled SVG grouped bar chart — the only chart type live-bench supports.
//
// The chart is driven by a single `ChartDef` (not the whole `BenchmarkConfig`):
// one card per chart per multi-chart benchmark. Groups are passed in
// separately because they live at the benchmark level and are shared across
// every chart in the stack.
//
// Layout maths:
//
//   BT (vertical bars):
//     plot area is the svg rect minus left/bottom padding for axes.
//     x-axis is categorical with N group slots, evenly distributed.
//     Inside each slot, M metric sub-bars are rendered side-by-side with a
//     small gap. Each bar grows from the bottom baseline up.
//
//   LR (horizontal bars):
//     plot area is the svg rect minus left/bottom padding.
//     y-axis is categorical with N group rows.
//     Inside each row, M metric sub-bars stack vertically. Each bar grows
//     rightward from the left baseline.
//
// Axis range: use chart.y.min / chart.y.max when set, otherwise
// min(0, observed min) to observed max * 1.1 (clamped to be non-zero).

import { computed, ref } from 'vue'
import type { ChartDef, GroupDef } from '../schemas'
import AnimatedBar from './AnimatedBar.vue'
import BarGradientDefs from './BarGradientDefs.vue'
import { gradientIdFor } from './gradient'

const emit = defineEmits<{
  groupClick: [chartId: string, groupKey: string]
}>()

const props = defineProps<{
  chart: ChartDef
  groups: GroupDef[]
  // Full session `latest` map keyed by `${chart_id}:${group_key}:${metric_key}`.
  // We look up values with the chart-qualified key so multi-chart benchmarks
  // don't bleed values between panels.
  latest: Map<string, number>
  width: number
  height: number
  overlayFontSize?: number
}>()

// Helper — build the chart-qualified cell key. Centralised so every code
// path uses the same shape as the session store.
function cellKey(groupKey: string, metricKey: string): string {
  return `${props.chart.chart_id}:${groupKey}:${metricKey}`
}

// ── Plot geometry ──────────────────────────────────────────
// Padding switches on direction:
//   BT — left padding holds the numeric value ticks (small).
//   LR — left padding holds the GROUP labels (e.g. "Charlie"), so we need
//        much more room or the labels clip against the card edge. This is
//        the §13.2.1 LR cutoff fix — do NOT reduce PAD_LEFT_LR without
//        retesting the latency card in the trio benchmark.
const PAD_LEFT_LR = 140
const PAD_BOTTOM_LR = 64

const hasGroupIcons = computed(() => props.groups.some((g) => g.icon))
const hasMetricIcons = computed(() => props.chart.metrics.some((m) => m.icon))

// Density level: 0=S, 1=M, 2=L — derived from overlayFontSize
const densityLevel = computed(() => {
  const ov = props.overlayFontSize ?? 19
  if (ov >= 28) return 2 // L
  if (ov >= 16) return 1 // M
  return 0               // S
})

// Fixed padding per density — no multiplicative scaling, just tested values
const PAD_PRESETS = [
  /* S */ { left: 56, right: 20, top: 50, bottom: 70, bottomIcon: 90 },
  /* M */ { left: 72, right: 24, top: 80, bottom: 90, bottomIcon: 120 },
  /* L */ { left: 80, right: 28, top: 110, bottom: 100, bottomIcon: 135 },
] as const

const pads = computed(() => PAD_PRESETS[densityLevel.value])

const padLeft = computed(() =>
  props.chart.direction === 'LR' ? PAD_LEFT_LR : pads.value.left,
)
const padRight = computed(() => pads.value.right)
const padTop = computed(() => pads.value.top + (hasMetricIcons.value ? 30 : 0))
const padBottom = computed(() => {
  if (props.chart.direction === 'LR') return PAD_BOTTOM_LR
  return hasGroupIcons.value ? pads.value.bottomIcon : pads.value.bottom
})

const plotX = computed(() => padLeft.value)
const plotY = computed(() => padTop.value)
const plotW = computed(() => Math.max(0, props.width - padLeft.value - padRight.value))
const plotH = computed(() => Math.max(0, props.height - padTop.value - padBottom.value))

// ── Value range ────────────────────────────────────────────
const values = computed(() => {
  const out: number[] = []
  for (const g of props.groups) {
    for (const m of props.chart.metrics) {
      const v = props.latest.get(cellKey(g.key, m.key))
      if (typeof v === 'number') out.push(v)
    }
  }
  return out
})

const valueRange = computed(() => {
  const cfgMin = props.chart.y.min
  const cfgMax = props.chart.y.max

  if (cfgMin != null && cfgMax != null) {
    return { min: cfgMin, max: cfgMax }
  }

  if (values.value.length === 0) {
    return { min: cfgMin ?? 0, max: cfgMax ?? 1 }
  }

  const observedMin = Math.min(...values.value)
  const observedMax = Math.max(...values.value)

  const min = cfgMin ?? Math.min(0, observedMin)
  // Use 1.1x headroom so a new incoming record doesn't clip at the edge.
  // Ensure max is strictly greater than min so range math stays safe.
  const rawMax = cfgMax ?? observedMax * 1.1
  const max = rawMax > min ? rawMax : min + 1
  return { min, max }
})

// ── Cell geometry (per-group, per-metric) ──────────────────
interface Cell {
  groupKey: string
  groupLabel: string
  groupIcon: string | null
  metricKey: string
  metricColor: string | string[] | undefined
  metricLabel: string
  metricIcon: string | null
  gradientId: string | null
  value: number
  slotX: number
  slotY: number
  slotWidth: number
  slotHeight: number
}

// ── Tooltip state ─────────────────────────────────────────
interface TooltipData {
  metricLabel: string
  groupLabel: string
  icon: string | null
  value: number
  rank: number       // 1-based rank within the group (1 = best)
  totalInGroup: number
  unit: string | null
  better: string     // 'higher' | 'lower'
  color: string
  x: number
  y: number
}

const tooltip = ref<TooltipData | null>(null)

function showTooltip(cell: Cell, event: MouseEvent) {
  // Compute rank within this group (same groupKey, across all metrics)
  const groupCells = cells.value.filter((c) => c.groupKey === cell.groupKey)
  const sorted = [...groupCells].sort((a, b) =>
    props.chart.better === 'lower' ? a.value - b.value : b.value - a.value,
  )
  const rank = sorted.findIndex((c) => c.metricKey === cell.metricKey) + 1

  const color = Array.isArray(cell.metricColor) ? cell.metricColor[0] : cell.metricColor ?? '#888'

  tooltip.value = {
    metricLabel: cell.metricLabel,
    groupLabel: cell.groupLabel,
    icon: cell.groupIcon,
    value: cell.value,
    rank,
    totalInGroup: groupCells.length,
    unit: props.chart.y.unit ?? null,
    better: props.chart.better,
    color,
    x: event.offsetX,
    y: event.offsetY,
  }
}

function hideTooltip() {
  tooltip.value = null
}

function formatTooltipValue(v: number): string {
  if (Math.abs(v) >= 100) return Math.round(v).toString()
  if (Math.abs(v) >= 10) return v.toFixed(1)
  return v.toFixed(2)
}

// Label font size scales with overlay (S=10, M=13, L=18)
const labelFontSize = computed(() => {
  const ov = props.overlayFontSize ?? 30
  return Math.max(10, Math.round(ov * 0.65))
})

function rankSuffix(n: number): string {
  if (n === 1) return '1st'
  if (n === 2) return '2nd'
  if (n === 3) return '3rd'
  return `${n}th`
}

const cells = computed<Cell[]>(() => {
  const out: Cell[] = []
  const groups = props.groups
  const metrics = props.chart.metrics
  if (groups.length === 0 || metrics.length === 0) return out

  const GROUP_PAD_RATIO = 0.15 // gap between group slots
  const METRIC_PAD_RATIO = 0.12 // gap between metrics within a group slot

  if (props.chart.direction === 'BT') {
    const slotOuter = plotW.value / groups.length
    const slotInner = slotOuter * (1 - GROUP_PAD_RATIO)
    const slotStart = (slotOuter - slotInner) / 2

    const barOuter = slotInner / metrics.length
    const barInner = barOuter * (1 - METRIC_PAD_RATIO)
    const barStart = (barOuter - barInner) / 2

    groups.forEach((g, gi) => {
      const slotLeft = plotX.value + gi * slotOuter + slotStart
      metrics.forEach((m, mi) => {
        const barLeft = slotLeft + mi * barOuter + barStart
        const v = props.latest.get(cellKey(g.key, m.key)) ?? 0
        out.push({
          groupKey: g.key,
          groupLabel: g.label,
          groupIcon: g.icon ?? null,
          metricKey: m.key,
          metricColor: m.color ?? undefined,
          metricLabel: m.label,
          metricIcon: m.icon ?? null,
          gradientId:
            Array.isArray(m.color) && m.color.length >= 2
              ? gradientIdFor(props.chart.chart_id, m.key)
              : null,
          value: v,
          slotX: barLeft,
          slotY: plotY.value,
          slotWidth: barInner,
          slotHeight: plotH.value,
        })
      })
    })
  } else {
    // LR
    const slotOuter = plotH.value / groups.length
    const slotInner = slotOuter * (1 - GROUP_PAD_RATIO)
    const slotStart = (slotOuter - slotInner) / 2

    const barOuter = slotInner / metrics.length
    const barInner = barOuter * (1 - METRIC_PAD_RATIO)
    const barStart = (barOuter - barInner) / 2

    groups.forEach((g, gi) => {
      const slotTop = plotY.value + gi * slotOuter + slotStart
      metrics.forEach((m, mi) => {
        const barTop = slotTop + mi * barOuter + barStart
        const v = props.latest.get(cellKey(g.key, m.key)) ?? 0
        out.push({
          groupKey: g.key,
          groupLabel: g.label,
          groupIcon: g.icon ?? null,
          metricKey: m.key,
          metricColor: m.color ?? undefined,
          metricLabel: m.label,
          metricIcon: m.icon ?? null,
          gradientId:
            Array.isArray(m.color) && m.color.length >= 2
              ? gradientIdFor(props.chart.chart_id, m.key)
              : null,
          value: v,
          slotX: plotX.value,
          slotY: barTop,
          slotWidth: plotW.value,
          slotHeight: barInner,
        })
      })
    })
  }
  return out
})

// ── Axis tick generation ───────────────────────────────────
// The "value axis" is the y-axis for BT (vertical bars grow upward) and the
// x-axis for LR (horizontal bars grow rightward). We compute ticks once for
// the value range and let the template pick the right coordinate per mode.
// This is the §13.2.1 LR cutoff fix — both BT and LR modes render ticks
// against the value range; do NOT remove either branch without retesting
// the trio benchmark's latency card.
interface ValueTick {
  value: number
  /** y coordinate when ticks are on the y-axis (BT mode) */
  y: number
  /** x coordinate when ticks are on the x-axis (LR mode) */
  x: number
}

const valueTicks = computed<ValueTick[]>(() => {
  const { min, max } = valueRange.value
  const steps = 4
  const out: ValueTick[] = []
  for (let i = 0; i <= steps; i++) {
    const t = i / steps
    const v = min + (max - min) * t
    const y = plotY.value + plotH.value - t * plotH.value
    const x = plotX.value + t * plotW.value
    out.push({ value: v, y, x })
  }
  return out
})

const ICON_SIZE = 27 // px — icon between label and bar

interface GroupLabel {
  key: string
  label: string
  icon: string | null
  x: number
  y: number
  /** Position for the icon (centered above the label for BT, left of label for LR) */
  iconX: number
  iconY: number
  anchor: 'middle' | 'start' | 'end'
}

const groupLabels = computed<GroupLabel[]>(() => {
  const groups = props.groups
  if (props.chart.direction === 'BT') {
    const slotOuter = plotW.value / groups.length
    const hasAnyIcon = groups.some((g) => g.icon)
    // Icon sits below baseline with 4px margin below it; label below that, slanted.
    const iconTop = 8 // gap from baseline to icon top
    const iconBottom = iconTop + ICON_SIZE + 4 // 4px margin below icon
    const labelOffset = hasAnyIcon ? iconBottom + 16 : 26
    return groups.map((g, i) => ({
      key: g.key,
      label: g.label,
      icon: g.icon ?? null,
      x: plotX.value + i * slotOuter + slotOuter / 2,
      y: plotY.value + plotH.value + labelOffset,
      iconX: plotX.value + i * slotOuter + slotOuter / 2 - ICON_SIZE / 2,
      iconY: plotY.value + plotH.value + iconTop,
      anchor: 'middle',
    }))
  }
  const slotOuter = plotH.value / groups.length
  return groups.map((g, i) => ({
    key: g.key,
    label: g.label,
    icon: g.icon ?? null,
    x: plotX.value - 10,
    y: plotY.value + i * slotOuter + slotOuter / 2 + 6,
    iconX: plotX.value - 10 - ICON_SIZE - 6, // left of label
    iconY: plotY.value + i * slotOuter + slotOuter / 2 - ICON_SIZE / 2 + 2,
    anchor: 'end',
  }))
})

function legendSwatchColor(color: string | string[] | null | undefined): string {
  if (Array.isArray(color) && color.length > 0) return color[0]
  if (typeof color === 'string') return color
  return 'var(--fg-dim)'
}

function formatTick(v: number): string {
  if (Math.abs(v) >= 100) return Math.round(v).toString()
  if (Math.abs(v) >= 10) return v.toFixed(1)
  return v.toFixed(2)
}
</script>

<template>
  <div>
    <div class="chart-legend">
      <div
        v-for="m in chart.metrics"
        :key="m.key"
        class="chart-legend__item"
      >
        <span
          class="chart-legend__swatch"
          :style="{ background: legendSwatchColor(m.color) }"
        />
        <span>{{ m.label }}</span>
      </div>
    </div>
    <svg
      :viewBox="`0 0 ${width} ${height}`"
      :width="width"
      :height="height"
      preserveAspectRatio="xMidYMid meet"
      role="img"
      aria-label="Grouped bar chart"
    >
      <BarGradientDefs
        :session-id="chart.chart_id"
        :metrics="chart.metrics"
      />

      <!-- Grid lines + value-axis ticks -->
      <!-- BT: horizontal grid lines, value labels on the LEFT (y-axis) -->
      <g v-if="chart.direction === 'BT'" class="chart-grid">
        <line
          v-for="tick in valueTicks"
          :key="`gl-${tick.value}`"
          :x1="plotX"
          :x2="plotX + plotW"
          :y1="tick.y"
          :y2="tick.y"
          stroke="var(--border-grid)"
          stroke-dasharray="4 6"
        />
        <text
          v-for="tick in valueTicks"
          :key="`gt-${tick.value}`"
          :x="plotX - 8"
          :y="tick.y + 5"
          text-anchor="end"
          font-size="14"
          fill="var(--fg-dimmer)"
          font-family="var(--font)"
        >
          {{ formatTick(tick.value) }}
        </text>
      </g>
      <!-- LR: vertical grid lines, value labels on the BOTTOM (x-axis) -->
      <g v-else class="chart-grid">
        <line
          v-for="tick in valueTicks"
          :key="`gl-${tick.value}`"
          :x1="tick.x"
          :x2="tick.x"
          :y1="plotY"
          :y2="plotY + plotH"
          stroke="var(--border-grid)"
          stroke-dasharray="4 6"
        />
        <text
          v-for="tick in valueTicks"
          :key="`gt-${tick.value}`"
          :x="tick.x"
          :y="plotY + plotH + 22"
          text-anchor="middle"
          font-size="14"
          fill="var(--fg-dimmer)"
          font-family="var(--font)"
        >
          {{ formatTick(tick.value) }}
        </text>
      </g>

      <!-- Y-axis label (BT) / X-axis label (LR) — rotated along the value axis -->
      <text
        v-if="chart.direction === 'BT' && chart.y.label"
        :x="16"
        :y="plotY + plotH / 2"
        text-anchor="middle"
        :transform="`rotate(-90, 16, ${plotY + plotH / 2})`"
        font-size="13"
        fill="var(--fg-dim)"
        font-family="var(--font)"
      >
        {{ chart.y.label }}{{ chart.y.unit ? ` (${chart.y.unit})` : '' }}
      </text>
      <text
        v-if="chart.direction === 'LR' && chart.x.label"
        :x="plotX + plotW / 2"
        :y="plotY + plotH + 48"
        text-anchor="middle"
        font-size="13"
        fill="var(--fg-dim)"
        font-family="var(--font)"
      >
        {{ chart.x.label }}{{ chart.x.unit ? ` (${chart.x.unit})` : '' }}
      </text>

      <!-- Axis lines -->
      <line
        :x1="plotX"
        :x2="plotX"
        :y1="plotY"
        :y2="plotY + plotH"
        stroke="var(--border-card)"
      />
      <line
        :x1="plotX"
        :x2="plotX + plotW"
        :y1="plotY + plotH"
        :y2="plotY + plotH"
        stroke="var(--border-card)"
      />

      <!-- Group icons -->
      <image
        v-for="g in groupLabels.filter((gl) => gl.icon)"
        :key="`icon-${g.key}`"
        :href="g.icon!"
        :x="g.iconX"
        :y="g.iconY"
        :width="ICON_SIZE"
        :height="ICON_SIZE"
      />

      <!-- Group labels (slanted ~30° for BT to improve readability, clickable) -->
      <text
        v-for="g in groupLabels"
        :key="`lbl-${g.key}`"
        :x="g.x"
        :y="g.y"
        :text-anchor="chart.direction === 'BT' ? 'middle' : g.anchor"
        :transform="chart.direction === 'BT' ? `rotate(-30, ${g.x}, ${g.y})` : undefined"
        :font-size="labelFontSize"
        fill="var(--fg-medium)"
        font-family="var(--font)"
        class="group-label--clickable"
        @click="emit('groupClick', chart.chart_id, g.key)"
      >
        {{ g.label }}
      </text>

      <!-- Bars: rects painted first (bottom layer) -->
      <g class="bar-rects">
        <AnimatedBar
          v-for="cell in cells"
          :key="`${cell.groupKey}:${cell.metricKey}`"
          :value="cell.value"
          :min="valueRange.min"
          :max="valueRange.max"
          :direction="chart.direction"
          :slot-x="cell.slotX"
          :slot-y="cell.slotY"
          :slot-width="cell.slotWidth"
          :slot-height="cell.slotHeight"
          :color="cell.metricColor"
          :gradient-id="cell.gradientId"
          :overlay-font-size="overlayFontSize"
          layer="rect"
        />
      </g>
      <!-- Bar text overlays painted second (top layer — always above all rects) -->
      <g class="bar-texts">
        <AnimatedBar
          v-for="cell in cells"
          :key="`overlay-${cell.groupKey}:${cell.metricKey}`"
          :value="cell.value"
          :min="valueRange.min"
          :max="valueRange.max"
          :direction="chart.direction"
          :slot-x="cell.slotX"
          :slot-y="cell.slotY"
          :slot-width="cell.slotWidth"
          :slot-height="cell.slotHeight"
          :color="cell.metricColor"
          :gradient-id="cell.gradientId"
          :overlay-font-size="overlayFontSize"
          :icon="cell.metricIcon"
          layer="text"
        />
      </g>
      <!-- Hover rects (top layer — capture mouse events over bars) -->
      <rect
        v-for="cell in cells"
        :key="`hover-${cell.groupKey}:${cell.metricKey}`"
        :x="cell.slotX"
        :y="cell.slotY"
        :width="cell.slotWidth"
        :height="cell.slotHeight"
        fill="transparent"
        style="cursor: pointer;"
        @mouseenter="showTooltip(cell, $event)"
        @mouseleave="hideTooltip"
      />
    </svg>

    <!-- Tooltip -->
    <div
      v-if="tooltip"
      class="bar-tooltip"
      :style="{ left: tooltip.x + 'px', top: (tooltip.y - 10) + 'px' }"
    >
      <div class="bar-tooltip__header">
        <img v-if="tooltip.icon" :src="tooltip.icon" class="bar-tooltip__icon" />
        <span class="bar-tooltip__model" :style="{ color: tooltip.color }">{{ tooltip.metricLabel }}</span>
      </div>
      <div class="bar-tooltip__value">
        {{ formatTooltipValue(tooltip.value) }}
        <span v-if="tooltip.unit" class="bar-tooltip__unit">{{ tooltip.unit }}</span>
      </div>
      <div class="bar-tooltip__rank">
        {{ rankSuffix(tooltip.rank) }} of {{ tooltip.totalInGroup }} in {{ tooltip.groupLabel }}
      </div>
    </div>
  </div>
</template>

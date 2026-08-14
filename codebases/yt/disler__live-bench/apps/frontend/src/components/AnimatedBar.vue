<script setup lang="ts">
// One bar in the GroupedBarChart. Owns the §14.1 state machine:
//
//   state:
//     current: number   // what's on screen
//     target:  number   // what we're animating toward; = current when idle
//     pending: number | null
//
//   - On a new value `v` while idle (current === target, pending === null):
//       target = v   → CSS transition runs from current to v over 1s.
//   - On a new value `v` while animating (current !== target):
//       pending = v  → current animation continues, pending is overwritten by
//                      any later updates so only the latest survives.
//   - On `transitionend`:
//       current = target. If pending !== null:
//         target = pending; pending = null   → new animation kicks off.
//       Otherwise idle.
//
// The numeric overlay text uses a requestAnimationFrame loop that eases from
// `current` to `target` with the same duration / easing as the bar
// transition. The loop stops when the rect's transitionend fires (so they
// stay perfectly in lock-step).

import { ref, watch, onBeforeUnmount, computed } from 'vue'

const props = defineProps<{
  value: number
  max: number
  min: number
  direction: 'BT' | 'LR'
  // The slot the bar is rendered into. The bar always grows from baseline:
  //   BT: baseline is `slotY + slotHeight`, bar grows up
  //   LR: baseline is `slotX`,              bar grows right
  slotX: number
  slotY: number
  slotWidth: number
  slotHeight: number
  color: string | string[] | undefined
  gradientId: string | null
  // Numeric overlay format hint (e.g. unit suffix); applied via Intl.NumberFormat
  unit?: string | null
  // Optional fixed font-size for the overlay; defaults to var(--fs-xlarge)
  overlayFontSize?: number
  // Render layer: 'both' (default), 'rect' (bar only), 'text' (overlay only).
  // Use 'rect' + 'text' in two passes so text always paints above all bars.
  layer?: 'both' | 'rect' | 'text'
  // Optional metric icon rendered between bar top and value text (BT mode).
  icon?: string | null
}>()

const METRIC_ICON_SIZE = 20

// ── Animation state machine ────────────────────────────────
// For text-only layer, skip animation — just track props.value directly.
const isTextOnly = (props.layer ?? 'both') === 'text'
const current = ref(props.value)
const target = ref(props.value)
const pending = ref<number | null>(null)
const displayValue = ref(props.value)

// rAF id for the overlay numeric easing loop. Cleared on transitionend / unmount.
let rafId: number | null = null
let easeStart = 0
let easeFrom = props.value
let easeTo = props.value
const ANIM_MS = 1000

function easeOutExpo(t: number): number {
  // Mirrors --ease-bar (cubic-bezier(0.22, 1, 0.36, 1)) closely enough for
  // numeric overlay sync — the bar uses the actual cubic-bezier via CSS.
  return t === 1 ? 1 : 1 - Math.pow(2, -10 * t)
}

function startOverlayEasing() {
  if (rafId !== null) cancelAnimationFrame(rafId)
  easeStart = performance.now()
  easeFrom = displayValue.value
  easeTo = target.value
  const tick = (now: number) => {
    const t = Math.min(1, (now - easeStart) / ANIM_MS)
    const e = easeOutExpo(t)
    displayValue.value = easeFrom + (easeTo - easeFrom) * e
    if (t < 1) {
      rafId = requestAnimationFrame(tick)
    } else {
      rafId = null
    }
  }
  rafId = requestAnimationFrame(tick)
}

function stopOverlayEasing() {
  if (rafId !== null) cancelAnimationFrame(rafId)
  rafId = null
  displayValue.value = target.value
}

watch(
  () => props.value,
  (newVal) => {
    if (isTextOnly) {
      // Text-only layer: no rect to transition, just snap values.
      current.value = newVal
      target.value = newVal
      displayValue.value = newVal
      return
    }
    if (current.value === target.value && pending.value === null) {
      // Idle → start a new animation.
      target.value = newVal
      startOverlayEasing()
    } else {
      // Animation in progress → buffer the latest. Any earlier pending value
      // is silently discarded; only the most recent survives.
      pending.value = newVal
    }
  },
)

function onTransitionEnd() {
  current.value = target.value
  if (pending.value !== null) {
    target.value = pending.value
    pending.value = null
    startOverlayEasing()
  } else {
    // Idle — make sure the overlay snapped to the final value.
    stopOverlayEasing()
  }
}

onBeforeUnmount(() => {
  if (rafId !== null) cancelAnimationFrame(rafId)
})

// ── Geometry ───────────────────────────────────────────────
// Map the *target* value (where we're animating to) into pixels. The CSS
// transition smoothly interpolates from the previous geometry.
const range = computed(() => {
  const span = props.max - props.min
  return span <= 0 ? 1 : span
})

const ratio = computed(() => {
  const r = (target.value - props.min) / range.value
  if (Number.isNaN(r)) return 0
  return Math.max(0, Math.min(1, r))
})

const rectGeom = computed(() => {
  if (props.direction === 'BT') {
    const height = props.slotHeight * ratio.value
    return {
      x: props.slotX,
      y: props.slotY + props.slotHeight - height,
      width: props.slotWidth,
      height,
    }
  }
  // LR
  const width = props.slotWidth * ratio.value
  return {
    x: props.slotX,
    y: props.slotY,
    width,
    height: props.slotHeight,
  }
})

// ── Fill ───────────────────────────────────────────────────
const fill = computed(() => {
  if (props.gradientId) return `url(#${props.gradientId})`
  if (typeof props.color === 'string') return props.color
  if (Array.isArray(props.color) && props.color.length > 0) return props.color[0]
  return '#888'
})

// ── Numeric overlay ────────────────────────────────────────
const overlayText = computed(() => {
  const v = displayValue.value
  // Round to a sensible precision based on magnitude.
  if (Math.abs(v) >= 100) return Math.round(v).toString()
  if (Math.abs(v) >= 10) return v.toFixed(1)
  return v.toFixed(2)
})

const overlayPrimary = computed(() => {
  if (Array.isArray(props.color) && props.color.length > 0) return props.color[0]
  if (typeof props.color === 'string') return props.color
  return 'currentColor'
})

const overlayPos = computed(() => {
  if (props.direction === 'BT') {
    // Above the bar, centered. When an icon is present, shift text up to
    // make room for the icon between text and bar top.
    const iconOffset = props.icon ? METRIC_ICON_SIZE + 8 : 0
    return {
      x: rectGeom.value.x + rectGeom.value.width / 2,
      y: Math.max(props.slotY - 10, rectGeom.value.y - 10) - iconOffset,
      anchor: 'middle' as const,
    }
  }
  // LR — at the right end of the bar, slightly outside.
  const iconOffset = props.icon ? METRIC_ICON_SIZE + 6 : 0
  return {
    x: rectGeom.value.x + rectGeom.value.width + 8 + iconOffset,
    y: rectGeom.value.y + rectGeom.value.height / 2 + 6,
    anchor: 'start' as const,
  }
})

const iconPos = computed(() => {
  if (props.direction === 'BT') {
    // Icon centered on bar, between value text and bar top.
    const barTop = Math.max(props.slotY - 10, rectGeom.value.y - 10)
    return {
      x: rectGeom.value.x + rectGeom.value.width / 2 - METRIC_ICON_SIZE / 2,
      y: barTop - METRIC_ICON_SIZE - 4,
    }
  }
  // LR — icon right of bar, before value text.
  return {
    x: rectGeom.value.x + rectGeom.value.width + 8,
    y: rectGeom.value.y + rectGeom.value.height / 2 - METRIC_ICON_SIZE / 2,
  }
})

// Expose internals to vitest. They're plain refs so tests can read .value.
defineExpose({ current, target, pending, displayValue, onTransitionEnd })
</script>

<template>
  <g class="animated-bar">
    <rect
      v-if="(layer ?? 'both') !== 'text'"
      :x="rectGeom.x"
      :y="rectGeom.y"
      :width="rectGeom.width"
      :height="rectGeom.height"
      :fill="fill"
      rx="4"
      @transitionend="onTransitionEnd"
    />
    <text
      v-if="(layer ?? 'both') !== 'rect'"
      :x="overlayPos.x"
      :y="overlayPos.y"
      :text-anchor="overlayPos.anchor"
      :font-size="overlayFontSize ?? 40"
      :fill="overlayPrimary"
      font-weight="700"
      font-family="var(--font)"
    >
      {{ overlayText }}<tspan
        v-if="unit"
        :font-size="(overlayFontSize ?? 40) * 0.5"
        fill="var(--fg-dim)"
      > {{ unit }}</tspan>
    </text>
    <image
      v-if="icon && (layer ?? 'both') !== 'rect'"
      :href="icon"
      :x="iconPos.x"
      :y="iconPos.y"
      :width="METRIC_ICON_SIZE"
      :height="METRIC_ICON_SIZE"
    />
  </g>
</template>

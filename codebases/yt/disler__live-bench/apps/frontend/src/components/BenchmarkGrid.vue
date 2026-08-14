<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { usePrefsStore } from '../stores/prefs'

// Spec §8.2 — columns derived from density × viewport width.
//   Large  : 1 column always (hero shot)
//   Medium : 2 cols ≥ 1000px, else 1
//   Small  : 4 cols ≥ 1400px, 3 ≥ 1000px, 2 < 1000px

const prefs = usePrefsStore()
const winWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1400)

function onResize() {
  winWidth.value = window.innerWidth
}

onMounted(() => window.addEventListener('resize', onResize))
onBeforeUnmount(() => window.removeEventListener('resize', onResize))

const cols = computed(() => {
  const w = winWidth.value
  if (prefs.density === 'L') return 1
  if (prefs.density === 'M') {
    return w >= 1000 ? 2 : 1
  }
  // Small
  if (w >= 1400) return 4
  if (w >= 1000) return 3
  return 2
})
</script>

<template>
  <div class="grid" :style="{ '--cols': cols }">
    <slot />
  </div>
</template>

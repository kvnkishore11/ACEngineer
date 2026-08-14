<script setup lang="ts">
import { usePrefsStore, type Density } from '../stores/prefs'

const prefs = usePrefsStore()

const densities: Density[] = ['S', 'M', 'L']
</script>

<template>
  <div class="layout-switcher" role="group" aria-label="Layout density">
    <button
      v-for="d in densities"
      :key="d"
      type="button"
      :class="{ 'is-active': prefs.density === d }"
      :aria-pressed="prefs.density === d"
      @click="prefs.setDensity(d)"
    >
      {{ d }}
    </button>
  </div>
</template>

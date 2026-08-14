<script setup lang="ts">
import { computed } from 'vue'
import { usePrefsStore } from '../stores/prefs'
import { THEMES, type ThemeName } from '../themes'

const prefs = usePrefsStore()

const currentSwatch = computed(
  () => THEMES.find((t) => t.name === prefs.theme)?.swatch ?? '#000',
)

function onChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value as ThemeName
  prefs.setTheme(value)
}
</script>

<template>
  <label class="theme-switcher">
    <span class="theme-switcher__swatch" :style="{ background: currentSwatch }" />
    <select :value="prefs.theme" @change="onChange" aria-label="Theme">
      <option v-for="t in THEMES" :key="t.name" :value="t.name">
        {{ t.label }}
      </option>
    </select>
  </label>
</template>

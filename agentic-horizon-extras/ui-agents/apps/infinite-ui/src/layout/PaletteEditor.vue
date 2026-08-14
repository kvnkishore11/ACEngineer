<script setup lang="ts">
import { useBrandStore } from '../stores/brand'

const brandStore = useBrandStore()

const paletteKeys = [
  'primary', 'secondary', 'accent', 'background',
  'bg-secondary', 'surface', 'text', 'muted',
  'border', 'overlay', 'error', 'warning', 'success',
] as const

function getColor(key: string): string {
  const palette = brandStore.config?.palette as Record<string, string> | undefined
  return palette?.[key] ?? '#000000'
}

function setColor(key: string, value: string) {
  brandStore.update({
    palette: {
      ...brandStore.config?.palette,
      [key]: value,
    },
  })
}
</script>

<template>
  <div class="editor-section" v-if="brandStore.config">
    <h4 class="section-title">Palette</h4>
    <div class="swatch-grid">
      <div v-for="key in paletteKeys" :key="key" class="swatch-item">
        <input
          type="color"
          :value="getColor(key).startsWith('rgba') ? '#000000' : getColor(key)"
          @input="setColor(key, ($event.target as HTMLInputElement).value)"
          class="color-input"
        />
        <span class="swatch-label">{{ key }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.editor-section {
  border-top: 1px solid var(--brand-border);
  padding-top: calc(var(--space-unit) * 2);
}

.section-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--brand-muted);
  letter-spacing: 0.05em;
  margin-bottom: calc(var(--space-unit) * 1.5);
}

.swatch-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: calc(var(--space-unit) * 1.5);
}

.swatch-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.color-input {
  width: 40px;
  height: 40px;
  border: 2px solid var(--brand-border);
  border-radius: var(--radius-sm);
  padding: 2px;
  cursor: pointer;
  background: transparent;
}

.color-input:hover {
  border-color: var(--brand-primary);
}

.swatch-label {
  font-size: 0.6rem;
  color: var(--brand-muted);
  text-align: center;
  text-transform: capitalize;
}
</style>

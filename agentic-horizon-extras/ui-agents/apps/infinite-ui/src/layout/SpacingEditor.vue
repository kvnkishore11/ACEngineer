<script setup lang="ts">
import { useBrandStore } from '../stores/brand'

const brandStore = useBrandStore()

function updateSpacing(key: string, value: string) {
  brandStore.update({
    spacing: {
      ...brandStore.config?.spacing,
      [key]: value,
    },
  })
}

function parseNum(val: string): number {
  return parseFloat(val) || 0
}
</script>

<template>
  <div class="editor-section" v-if="brandStore.config">
    <h4 class="section-title">Spacing</h4>

    <div class="slider-row">
      <label class="slider-label">Unit</label>
      <input
        type="range"
        min="0.25"
        max="1"
        step="0.125"
        :value="parseNum(brandStore.config.spacing.unit)"
        @input="updateSpacing('unit', ($event.target as HTMLInputElement).value + 'rem')"
      />
      <span class="slider-val">{{ brandStore.config.spacing.unit }}</span>
    </div>

    <div class="slider-row">
      <label class="slider-label">Radius SM</label>
      <input
        type="range"
        min="0"
        max="2"
        step="0.125"
        :value="parseNum(brandStore.config.spacing['radius-sm'])"
        @input="updateSpacing('radius-sm', ($event.target as HTMLInputElement).value + 'rem')"
      />
      <span class="slider-val">{{ brandStore.config.spacing['radius-sm'] }}</span>
    </div>

    <div class="slider-row">
      <label class="slider-label">Radius MD</label>
      <input
        type="range"
        min="0"
        max="2"
        step="0.125"
        :value="parseNum(brandStore.config.spacing['radius-md'])"
        @input="updateSpacing('radius-md', ($event.target as HTMLInputElement).value + 'rem')"
      />
      <span class="slider-val">{{ brandStore.config.spacing['radius-md'] }}</span>
    </div>

    <div class="slider-row">
      <label class="slider-label">Radius LG</label>
      <input
        type="range"
        min="0"
        max="2"
        step="0.125"
        :value="parseNum(brandStore.config.spacing['radius-lg'])"
        @input="updateSpacing('radius-lg', ($event.target as HTMLInputElement).value + 'rem')"
      />
      <span class="slider-val">{{ brandStore.config.spacing['radius-lg'] }}</span>
    </div>

    <div class="slider-row">
      <label class="slider-label">Container</label>
      <input
        type="range"
        min="800"
        max="1600"
        step="50"
        :value="parseNum(brandStore.config.spacing['container-max'])"
        @input="updateSpacing('container-max', ($event.target as HTMLInputElement).value + 'px')"
      />
      <span class="slider-val">{{ brandStore.config.spacing['container-max'] }}</span>
    </div>
  </div>
</template>

<style scoped>
.editor-section {
  border-top: 1px solid var(--brand-border);
  padding-top: calc(var(--space-unit) * 2);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1.5);
}

.section-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--brand-muted);
  letter-spacing: 0.05em;
}

.slider-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.slider-label {
  font-size: 0.7rem;
  color: var(--brand-muted);
  width: 72px;
  flex-shrink: 0;
}

.slider-row input[type="range"] {
  flex: 1;
  accent-color: var(--brand-primary);
  background: transparent;
  border: none;
  padding: 0;
}

.slider-val {
  font-size: 0.65rem;
  color: var(--brand-muted);
  font-family: var(--font-mono);
  width: 64px;
  text-align: right;
  flex-shrink: 0;
}
</style>

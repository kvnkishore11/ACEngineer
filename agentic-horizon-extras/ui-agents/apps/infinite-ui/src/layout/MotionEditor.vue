<script setup lang="ts">
import { useBrandStore } from '../stores/brand'

const brandStore = useBrandStore()

const easingPresets = [
  'ease',
  'ease-in',
  'ease-out',
  'ease-in-out',
  'linear',
  'cubic-bezier(0.4, 0, 0.2, 1)',
  'cubic-bezier(0.33, 1, 0.68, 1)',
  'cubic-bezier(0.65, 0, 0.35, 1)',
]

function updateMotion(key: string, value: string) {
  brandStore.update({
    motion: {
      ...brandStore.config?.motion,
      [key]: value,
    },
  })
}

function parseMs(val: string): number {
  return parseInt(val) || 0
}
</script>

<template>
  <div class="editor-section" v-if="brandStore.config">
    <h4 class="section-title">Motion</h4>

    <div class="slider-row">
      <label class="slider-label">Fast</label>
      <input
        type="range"
        min="50"
        max="1000"
        step="25"
        :value="parseMs(brandStore.config.motion['duration-fast'])"
        @input="updateMotion('duration-fast', ($event.target as HTMLInputElement).value + 'ms')"
      />
      <span class="slider-val">{{ brandStore.config.motion['duration-fast'] }}</span>
    </div>

    <div class="slider-row">
      <label class="slider-label">Normal</label>
      <input
        type="range"
        min="50"
        max="1000"
        step="25"
        :value="parseMs(brandStore.config.motion['duration-normal'])"
        @input="updateMotion('duration-normal', ($event.target as HTMLInputElement).value + 'ms')"
      />
      <span class="slider-val">{{ brandStore.config.motion['duration-normal'] }}</span>
    </div>

    <div class="slider-row">
      <label class="slider-label">Slow</label>
      <input
        type="range"
        min="50"
        max="1000"
        step="25"
        :value="parseMs(brandStore.config.motion['duration-slow'])"
        @input="updateMotion('duration-slow', ($event.target as HTMLInputElement).value + 'ms')"
      />
      <span class="slider-val">{{ brandStore.config.motion['duration-slow'] }}</span>
    </div>

    <div class="field">
      <label class="field-label">Easing</label>
      <select
        :value="brandStore.config.motion.easing"
        @change="updateMotion('easing', ($event.target as HTMLSelectElement).value)"
      >
        <option v-for="e in easingPresets" :key="e" :value="e">{{ e }}</option>
      </select>
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
  width: 52px;
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
  width: 52px;
  text-align: right;
  flex-shrink: 0;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.field select {
  width: 100%;
}
</style>

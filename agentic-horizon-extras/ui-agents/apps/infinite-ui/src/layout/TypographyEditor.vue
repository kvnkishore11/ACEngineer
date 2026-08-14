<script setup lang="ts">
import { computed } from 'vue'
import { useBrandStore } from '../stores/brand'

interface ScaleEntry {
  size: string
  weight: number
  tracking?: string
  'line-height'?: number
}

const brandStore = useBrandStore()

const defaultFonts = [
  'Inter', 'Play', 'Roboto', 'Open Sans', 'Lato', 'Montserrat',
  'Poppins', 'Raleway', 'Nunito', 'Playfair Display', 'Merriweather',
  'Source Sans 3', 'PT Sans', 'Noto Sans', 'Ubuntu', 'Fira Sans',
  'DM Sans', 'Space Grotesk', 'Plus Jakarta Sans', 'JetBrains Mono', 'Fira Code',
]

const fonts = computed(() => {
  if (!brandStore.config) return defaultFonts
  const active = [
    brandStore.config.typography.heading,
    brandStore.config.typography.body,
    brandStore.config.typography.mono,
  ]
  const extra = active.filter(f => !defaultFonts.includes(f))
  return [...new Set([...extra, ...defaultFonts])].sort()
})

const scaleEntries = computed<[string, ScaleEntry][]>(() => {
  if (!brandStore.config) return []
  return Object.entries(brandStore.config.typography.scale) as [string, ScaleEntry][]
})

function updateFont(key: 'heading' | 'body' | 'mono', value: string) {
  if (!brandStore.config) return
  brandStore.update({
    typography: {
      heading: brandStore.config.typography.heading,
      body: brandStore.config.typography.body,
      mono: brandStore.config.typography.mono,
      scale: brandStore.config.typography.scale,
      [key]: value,
    },
  })
}

function updateScale(scaleKey: string, field: string, value: string | number) {
  if (!brandStore.config) return
  const currentScale: Record<string, ScaleEntry> = {}
  for (const [k, v] of Object.entries(brandStore.config.typography.scale)) {
    currentScale[k] = { ...(v as ScaleEntry) }
  }
  currentScale[scaleKey] = {
    ...currentScale[scaleKey],
    [field]: value,
  }
  brandStore.update({
    typography: {
      heading: brandStore.config.typography.heading,
      body: brandStore.config.typography.body,
      mono: brandStore.config.typography.mono,
      scale: currentScale,
    },
  })
}
</script>

<template>
  <div class="editor-section" v-if="brandStore.config">
    <h4 class="section-title">Typography</h4>

    <div class="font-selectors">
      <div class="field">
        <label class="field-label">Heading</label>
        <select :value="brandStore.config.typography.heading" @change="updateFont('heading', ($event.target as HTMLSelectElement).value)">
          <option v-for="f in fonts" :key="f" :value="f">{{ f }}</option>
        </select>
      </div>
      <div class="field">
        <label class="field-label">Body</label>
        <select :value="brandStore.config.typography.body" @change="updateFont('body', ($event.target as HTMLSelectElement).value)">
          <option v-for="f in fonts" :key="f" :value="f">{{ f }}</option>
        </select>
      </div>
      <div class="field">
        <label class="field-label">Mono</label>
        <select :value="brandStore.config.typography.mono" @change="updateFont('mono', ($event.target as HTMLSelectElement).value)">
          <option v-for="f in fonts" :key="f" :value="f">{{ f }}</option>
        </select>
      </div>
    </div>

    <div class="scale-editors">
      <div v-for="[key, val] in scaleEntries" :key="key" class="scale-item">
        <span class="scale-name">{{ key }}</span>
        <div class="scale-controls">
          <label class="mini-label">size</label>
          <input
            type="range"
            min="0.5"
            max="5"
            step="0.125"
            :value="parseFloat(val.size)"
            @input="updateScale(key, 'size', ($event.target as HTMLInputElement).value + 'rem')"
          />
          <span class="range-val">{{ val.size }}</span>
        </div>
        <div class="scale-controls">
          <label class="mini-label">wt</label>
          <input
            type="range"
            min="100"
            max="900"
            step="100"
            :value="val.weight"
            @input="updateScale(key, 'weight', Number(($event.target as HTMLInputElement).value))"
          />
          <span class="range-val">{{ val.weight }}</span>
        </div>
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

.font-selectors {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
  margin-bottom: calc(var(--space-unit) * 2);
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

.scale-editors {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1.5);
}

.scale-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.scale-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--brand-text);
}

.scale-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mini-label {
  font-size: 0.6rem;
  color: var(--brand-muted);
  width: 28px;
  flex-shrink: 0;
}

.scale-controls input[type="range"] {
  flex: 1;
  accent-color: var(--brand-primary);
  background: transparent;
  border: none;
  padding: 0;
}

.range-val {
  font-size: 0.65rem;
  color: var(--brand-muted);
  font-family: var(--font-mono);
  width: 48px;
  text-align: right;
  flex-shrink: 0;
}
</style>

<script setup lang="ts">
import { useBrandStore } from '../stores/brand'
import IdentityEditor from './IdentityEditor.vue'
import PaletteEditor from './PaletteEditor.vue'
import TypographyEditor from './TypographyEditor.vue'
import SpacingEditor from './SpacingEditor.vue'
import MotionEditor from './MotionEditor.vue'
import MediaPanel from './MediaPanel.vue'

const brandStore = useBrandStore()
</script>

<template>
  <div class="brand-panel" v-if="brandStore.config">
    <div class="panel-header">
      <h3>{{ brandStore.config.name }}</h3>
      <span class="tagline">{{ brandStore.config.tagline }}</span>
    </div>

    <div class="panel-section">
      <label class="field-label">Name</label>
      <input
        type="text"
        :value="brandStore.config.name"
        @input="brandStore.update({ name: ($event.target as HTMLInputElement).value })"
      />
    </div>

    <div class="panel-section">
      <label class="field-label">Tagline</label>
      <input
        type="text"
        :value="brandStore.config.tagline"
        @input="brandStore.update({ tagline: ($event.target as HTMLInputElement).value })"
      />
    </div>

    <div class="panel-section">
      <label class="field-label">Tone</label>
      <input
        type="text"
        :value="brandStore.config.tone"
        @input="brandStore.update({ tone: ($event.target as HTMLInputElement).value })"
      />
    </div>

    <div class="panel-section">
      <label class="field-label">Audience</label>
      <input
        type="text"
        :value="brandStore.config.audience"
        @input="brandStore.update({ audience: ($event.target as HTMLInputElement).value })"
      />
    </div>

    <IdentityEditor />
    <PaletteEditor />
    <TypographyEditor />
    <SpacingEditor />
    <MotionEditor />
    <MediaPanel />

    <div class="panel-actions">
      <div v-if="brandStore.isDirty" class="dirty-indicator">
        &#x25CF; Unsaved changes
      </div>
      <div class="action-buttons">
        <button class="btn-save" @click="brandStore.save()">Save</button>
        <button class="btn-reset" @click="brandStore.load(brandStore.activeBrand!, brandStore.activeProduct!)">Reset</button>
      </div>
    </div>
  </div>
  <div v-else class="no-brand">
    <p>Navigate to a product to edit brand settings.</p>
  </div>
</template>

<style scoped>
.brand-panel {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.panel-header h3 {
  font-size: 1.125rem;
  font-weight: 700;
}

.tagline {
  font-size: 0.8rem;
  color: var(--brand-muted);
}

.panel-section {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.field-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--brand-muted);
  letter-spacing: 0.05em;
}

.panel-section input {
  width: 100%;
}

.panel-actions {
  border-top: 1px solid var(--brand-border);
  padding-top: calc(var(--space-unit) * 2);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.dirty-indicator {
  font-size: 0.8rem;
  color: var(--brand-warning);
}

.action-buttons {
  display: flex;
  gap: calc(var(--space-unit) * 1);
}

.btn-save {
  flex: 1;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  background: var(--brand-primary);
  color: var(--brand-bg);
  font-weight: 600;
  font-size: 0.875rem;
  transition: opacity var(--duration-fast) var(--easing);
}

.btn-save:hover {
  opacity: 0.9;
}

.btn-reset {
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--brand-border);
  color: var(--brand-muted);
  font-size: 0.875rem;
  transition: all var(--duration-fast) var(--easing);
}

.btn-reset:hover {
  border-color: var(--brand-text);
  color: var(--brand-text);
}

.no-brand {
  text-align: center;
  padding: calc(var(--space-unit) * 6);
  color: var(--brand-muted);
}
</style>

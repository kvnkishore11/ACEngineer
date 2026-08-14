<script setup lang="ts">
import { computed } from 'vue'
import { useBrandStore } from '../stores/brand'

const brandStore = useBrandStore()

const mediaItems = computed(() => brandStore.config?.assets?.media ?? [])
</script>

<template>
  <div class="editor-section" v-if="brandStore.config">
    <h4 class="section-title">Media</h4>

    <div class="media-info">
      <div class="field-row">
        <span class="field-label">Logo</span>
        <span class="field-value">{{ brandStore.config.assets.logo }}</span>
      </div>
      <div class="field-row">
        <span class="field-label">Favicon</span>
        <span class="field-value">{{ brandStore.config.assets.favicon }}</span>
      </div>
    </div>

    <div v-if="mediaItems.length > 0" class="media-list">
      <div v-for="(item, i) in mediaItems" :key="i" class="media-item">
        <span class="media-path">{{ item.path }}</span>
        <span class="media-desc">{{ item.description }}</span>
      </div>
    </div>
    <p v-else class="empty-media">No media assets defined.</p>
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

.media-info {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
  margin-bottom: calc(var(--space-unit) * 2);
}

.field-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.field-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.field-value {
  font-size: 0.75rem;
  font-family: var(--font-mono);
  color: var(--brand-text);
}

.media-list {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.media-item {
  background: var(--brand-surface);
  padding: calc(var(--space-unit) * 1) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.media-path {
  font-size: 0.7rem;
  font-family: var(--font-mono);
  color: var(--brand-primary);
}

.media-desc {
  font-size: 0.7rem;
  color: var(--brand-muted);
}

.empty-media {
  font-size: 0.8rem;
  color: var(--brand-muted);
}
</style>

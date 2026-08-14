<script setup lang="ts">
import { computed } from 'vue'
import { useCanvasStore } from '../stores/canvas'

const canvasStore = useCanvasStore()

const activePreset = computed(() => {
  const { width } = canvasStore.previewSize
  if (width === 480) return 'small'
  if (width === 640) return 'medium'
  if (width === 960) return 'large'
  return null
})
</script>

<template>
  <div class="preview-controls">
    <button
      class="size-btn"
      :class="{ active: activePreset === 'small' }"
      @click="canvasStore.setPreviewSize('small')"
    >
      S
    </button>
    <button
      class="size-btn"
      :class="{ active: activePreset === 'medium' }"
      @click="canvasStore.setPreviewSize('medium')"
    >
      M
    </button>
    <button
      class="size-btn"
      :class="{ active: activePreset === 'large' }"
      @click="canvasStore.setPreviewSize('large')"
    >
      L
    </button>
  </div>
</template>

<style scoped>
.preview-controls {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  display: flex;
  gap: 4px;
  padding: 4px;
  border-radius: var(--radius-md);
  background: color-mix(in srgb, var(--brand-surface) 80%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--brand-border);
}

.size-btn {
  width: 32px;
  height: 28px;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--brand-muted);
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--duration-fast) var(--easing);
}

.size-btn:hover {
  color: var(--brand-text);
  background: color-mix(in srgb, var(--brand-primary) 15%, transparent);
}

.size-btn.active {
  color: var(--brand-primary);
  background: color-mix(in srgb, var(--brand-primary) 20%, transparent);
}
</style>

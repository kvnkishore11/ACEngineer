<script setup lang="ts">
import { computed } from 'vue'
import { Handle, Position } from '@vue-flow/core'
import { useRoute } from 'vue-router'
import { useCanvasStore } from '../stores/canvas'

const props = defineProps<{
  data: {
    slug: string
    name: string
    description: string
    status: string
    treeSlug: string
  }
}>()

const route = useRoute()
const canvasStore = useCanvasStore()

const brand = computed(() => route.params.brand as string)
const product = computed(() => route.params.product as string)

const previewUrl = computed(
  () => `/${brand.value}/${product.value}/gallery/${props.data.treeSlug}/${props.data.slug}`
)

const containerWidth = computed(() => canvasStore.previewSize.width)
const containerHeight = computed(() => canvasStore.previewSize.height)
const iframeScale = computed(() => canvasStore.previewSize.scale)

const statusColor = computed(() => {
  switch (props.data.status) {
    case 'validated': return 'var(--brand-success)'
    case 'draft': return 'var(--brand-warning)'
    case 'generating': return 'var(--brand-accent)'
    case 'failed': return 'var(--brand-error)'
    default: return 'var(--brand-muted)'
  }
})
</script>

<template>
  <div class="preview-branch-node">
    <Handle type="target" :position="Position.Left" />
    <Handle type="source" :position="Position.Right" />

    <div
      class="preview-wrapper"
      :style="{
        width: containerWidth + 'px',
        height: containerHeight + 'px',
      }"
    >
      <iframe
        :src="previewUrl"
        width="1280"
        height="720"
        :style="{
          transform: `scale(${iframeScale})`,
          transformOrigin: 'top left',
        }"
        class="preview-iframe"
        frameborder="0"
      />
      <span class="status-badge" :style="{ backgroundColor: statusColor }" />
    </div>

    <span class="branch-label">{{ data.name }}</span>
  </div>
</template>

<style scoped>
.preview-branch-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: box-shadow var(--duration-fast) var(--easing);
}

.preview-branch-node:hover {
  box-shadow: var(--shadow-lg);
}

.preview-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-md);
  border: 2px solid var(--brand-border);
  background: var(--brand-surface);
}

.preview-iframe {
  pointer-events: none;
  border: none;
  display: block;
}

.status-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid var(--brand-surface);
}

.branch-label {
  margin-top: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--brand-text);
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
}
</style>

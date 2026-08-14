<script setup lang="ts">
import { computed } from 'vue'
import { Handle, Position } from '@vue-flow/core'

const props = defineProps<{
  data: {
    slug: string
    name: string
    description: string
    status: string
    treeSlug: string
  }
}>()

const isLoading = computed(() =>
  props.data.status === 'generating' || props.data.status === 'validating'
)

const statusColor = computed(() => {
  switch (props.data.status) {
    case 'validated': return 'var(--brand-success)'
    case 'draft': return 'var(--brand-warning)'
    case 'generating': return 'var(--brand-accent)'
    case 'validating': return 'var(--brand-warning)'
    case 'failed': return 'var(--brand-error)'
    default: return 'var(--brand-muted)'
  }
})

const statusIcon = computed(() => {
  switch (props.data.status) {
    case 'validated': return '\u2713'
    case 'draft': return '\u25CF'
    case 'generating': return '\u25CB'
    case 'validating': return '\u25CB'
    case 'failed': return '\u2717'
    default: return '\u25CB'
  }
})

const statusLabel = computed(() => {
  switch (props.data.status) {
    case 'generating': return 'Generating...'
    case 'validating': return 'Validating...'
    default: return ''
  }
})
</script>

<template>
  <div class="branch-node" :style="{ borderColor: statusColor }">
    <Handle type="target" :position="Position.Left" />
    <div class="branch-header">
      <span class="status-icon" :style="{ color: statusColor }">{{ statusIcon }}</span>
      <span class="branch-name">{{ data.name }}</span>
    </div>
    <div v-if="isLoading" class="branch-loading">
      <div class="loading-bar">
        <div class="loading-fill" :style="{ backgroundColor: statusColor }" />
      </div>
      <span class="loading-label" :style="{ color: statusColor }">{{ statusLabel }}</span>
    </div>
    <p class="branch-desc">{{ data.description }}</p>
    <Handle type="source" :position="Position.Right" />
  </div>
</template>

<style scoped>
.branch-node {
  background: var(--brand-surface);
  border: 2px solid var(--brand-border);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  min-width: 140px;
  max-width: 180px;
  cursor: pointer;
  transition: box-shadow var(--duration-fast) var(--easing);
}

.branch-node:hover {
  box-shadow: var(--shadow-md);
}

.branch-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.status-icon {
  font-size: 0.875rem;
}

.branch-name {
  font-weight: 600;
  font-size: 0.8rem;
  color: var(--brand-text);
}

.branch-loading {
  margin: 6px 0;
}

.loading-bar {
  width: 100%;
  height: 3px;
  background: color-mix(in srgb, var(--brand-border) 50%, transparent);
  border-radius: 2px;
  overflow: hidden;
}

.loading-fill {
  width: 40%;
  height: 100%;
  border-radius: 2px;
  animation: loading-slide 1.5s ease-in-out infinite;
}

.loading-label {
  display: block;
  font-size: 0.6rem;
  font-weight: 600;
  margin-top: 3px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.branch-desc {
  font-size: 0.7rem;
  color: var(--brand-muted);
  line-height: 1.3;
}

@keyframes loading-slide {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(200%); }
  100% { transform: translateX(-100%); }
}
</style>

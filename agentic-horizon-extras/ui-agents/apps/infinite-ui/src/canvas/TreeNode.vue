<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

defineProps<{
  data: {
    slug: string
    name: string
    description: string
    icon: string
    branches: Array<{ slug: string; name: string; status: string }>
  }
}>()
</script>

<template>
  <div class="tree-node">
    <Handle type="target" :position="Position.Left" />
    <div class="tree-node-header">
      <span class="tree-icon">&#x1F333;</span>
      <span class="tree-name">{{ data.name }}</span>
    </div>
    <p class="tree-desc">{{ data.description }}</p>
    <span class="tree-count">{{ data.branches?.length ?? 0 }} branches</span>
    <Handle type="source" :position="Position.Right" />
  </div>
</template>

<style scoped>
.tree-node {
  background: var(--brand-surface);
  border: 2px solid var(--brand-primary);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  min-width: 160px;
  max-width: 200px;
}

.tree-node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.tree-icon {
  font-size: 1.1rem;
}

.tree-name {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--brand-text);
}

.tree-desc {
  font-size: 0.75rem;
  color: var(--brand-muted);
  margin-bottom: 6px;
  line-height: 1.3;
}

.tree-count {
  font-size: 0.7rem;
  color: var(--brand-muted);
  font-weight: 500;
}
</style>

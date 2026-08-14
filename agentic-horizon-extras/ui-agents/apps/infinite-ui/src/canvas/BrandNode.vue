<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'
import { useBrandStore } from '../stores/brand'
import { useTreesStore } from '../stores/trees'
import { useActivityStore } from '../stores/activity'

defineProps<{
  data: {
    label: string
  }
}>()

const brandStore = useBrandStore()
const treesStore = useTreesStore()
const activityStore = useActivityStore()
</script>

<template>
  <div class="brand-node">
    <div class="brand-header">
      <span class="brand-name">{{ data.label }}</span>
      <span class="brand-product">/ {{ treesStore.manifest?.product }}</span>
    </div>
    <div v-if="brandStore.config?.tagline" class="brand-tagline">
      {{ brandStore.config.tagline }}
    </div>
    <div v-if="brandStore.config?.palette" class="brand-palette">
      <span
        class="palette-dot"
        :style="{ backgroundColor: brandStore.config.palette.primary }"
      />
      <span
        class="palette-dot"
        :style="{ backgroundColor: brandStore.config.palette.secondary }"
      />
      <span
        class="palette-dot"
        :style="{ backgroundColor: brandStore.config.palette.accent }"
      />
      <span
        class="palette-dot"
        :style="{ backgroundColor: brandStore.config.palette.success }"
      />
      <span
        class="palette-dot"
        :style="{ backgroundColor: brandStore.config.palette.error }"
      />
    </div>
    <div class="brand-metrics">
      {{ treesStore.treeCount }} trees &middot; {{ treesStore.branchCount }} branches &middot; {{ treesStore.validatedCount }} validated
    </div>
    <div v-if="activityStore.isActive" class="activity-pulse" />
    <Handle type="source" :position="Position.Right" />
  </div>
</template>

<style scoped>
.brand-node {
  position: relative;
  width: 220px;
  background: var(--brand-surface);
  border: 2px solid var(--brand-primary);
  border-radius: var(--radius-md);
  padding: 14px 16px;
}

.brand-header {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.brand-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--brand-text);
  text-transform: capitalize;
}

.brand-product {
  font-weight: 400;
  font-size: 0.75rem;
  color: var(--brand-muted);
}

.brand-tagline {
  font-size: 0.7rem;
  color: var(--brand-muted);
  line-height: 1.3;
  margin-top: 4px;
  max-height: calc(0.7rem * 1.3 * 2);
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.brand-palette {
  display: flex;
  flex-direction: row;
  gap: 6px;
  margin: 8px 0;
}

.palette-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.brand-metrics {
  font-size: 0.65rem;
  color: var(--brand-muted);
  font-weight: 500;
}

.activity-pulse {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brand-accent);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.4);
    opacity: 0.6;
  }
}
</style>

<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

defineProps<{
  data: {
    label: string
  }
}>()
</script>

<template>
  <div class="leaf-node">
    <span class="leaf-label">{{ data.label }}</span>
    <Handle type="source" :position="Position.Right" />
  </div>
</template>

<style scoped>
.leaf-node {
  background: var(--brand-primary);
  color: var(--brand-bg);
  border-radius: var(--radius-md);
  padding: 10px 20px;
  font-weight: 700;
  font-size: 0.9rem;
  text-transform: capitalize;
  min-width: 120px;
  text-align: center;
}
</style>

<script setup lang="ts">
defineProps<{
  icon?: string
}>()
</script>

<template>
  <div class="empty">
    <div class="empty__icon">{{ icon ?? '○' }}</div>
    <div class="empty__message">
      <slot />
    </div>
    <div v-if="$slots.cta">
      <slot name="cta" />
    </div>
  </div>
</template>

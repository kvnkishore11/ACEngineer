<script setup lang="ts">
import { computed } from 'vue'
import { useConnectionStore } from '../stores/connection'

const conn = useConnectionStore()

const label = computed(() => {
  switch (conn.state) {
    case 'connecting':
      return 'connecting'
    case 'live':
      return 'live'
    case 'ping_received':
      return 'Ping Received'
    case 'reconnecting':
      return 'reconnecting'
    case 'disconnected':
      return 'offline'
  }
})
</script>

<template>
  <span :class="['conn-badge', `conn-badge--${conn.state}`]" data-testid="conn-badge">
    <span class="conn-badge__dot" />
    <span>{{ label }}</span>
  </span>
</template>

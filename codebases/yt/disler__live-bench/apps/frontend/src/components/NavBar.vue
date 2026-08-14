<script setup lang="ts">
import { computed } from 'vue'
import { useConnectionStore } from '../stores/connection'
import ConnectionBadge from './ConnectionBadge.vue'
import LayoutSwitcher from './LayoutSwitcher.vue'
import ThemeSwitcher from './ThemeSwitcher.vue'

const conn = useConnectionStore()
const isPing = computed(() => conn.state === 'ping_received')
</script>

<template>
  <nav class="navbar" :class="{ 'navbar--ping': isPing }">
    <RouterLink to="/" class="navbar__brand">live-bench</RouterLink>
    <div class="navbar__right">
      <ConnectionBadge />
      <LayoutSwitcher />
      <ThemeSwitcher />
    </div>
  </nav>
</template>

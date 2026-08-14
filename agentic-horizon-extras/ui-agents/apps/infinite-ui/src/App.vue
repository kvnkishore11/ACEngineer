<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBrandStore } from './stores/brand'
import { useTreesStore } from './stores/trees'
import { useSidebarStore } from './stores/sidebar'
import { useBrandTokens } from './brand/tokens'
import BreadcrumbBar from './layout/BreadcrumbBar.vue'
import Sidebar from './layout/Sidebar.vue'

const route = useRoute()
const brandStore = useBrandStore()
const treesStore = useTreesStore()
const sidebarStore = useSidebarStore()

useBrandTokens()

const navVisible = ref(true)

// Watch route params to load/clear stores
watch(
  () => [route.params.brand, route.params.product],
  async ([brand, product]) => {
    if (brand && product) {
      await Promise.all([
        brandStore.load(brand as string, product as string),
        treesStore.load(brand as string, product as string),
      ])
    } else {
      brandStore.clear()
      treesStore.clear()
    }
  },
  { immediate: true }
)

function handleKeydown(e: KeyboardEvent) {
  // Ctrl+H — toggle breadcrumb visibility
  if (e.ctrlKey && e.key === 'h') {
    e.preventDefault()
    navVisible.value = !navVisible.value
  }
  // Ctrl+S — toggle sidebar (prevent browser save)
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault()
    sidebarStore.toggle()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <BreadcrumbBar :visible="navVisible" />
  <Sidebar />
  <main class="app-content" :class="{ 'nav-hidden': !navVisible }">
    <router-view />
  </main>
</template>

<style scoped>
.app-content {
  padding-top: 48px;
  min-height: 100vh;
  transition: padding-top var(--duration-fast) var(--easing);
}

.app-content.nav-hidden {
  padding-top: 0;
}
</style>

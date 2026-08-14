<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSidebarStore } from '../stores/sidebar'

defineProps<{
  visible: boolean
}>()

const route = useRoute()
const sidebarStore = useSidebarStore()

interface Crumb {
  label: string
  to: string | null
}

const crumbs = computed<Crumb[]>(() => {
  const parts: Crumb[] = [{ label: 'Workspace', to: '/' }]
  const brand = route.params.brand as string | undefined
  const product = route.params.product as string | undefined
  const tree = route.params.tree as string | undefined
  const branch = route.params.branch as string | undefined

  if (brand) parts.push({ label: brand, to: `/${brand}` })
  if (product) parts.push({ label: product, to: `/${brand}/${product}` })

  if (route.path.includes('/gallery')) {
    parts.push({ label: 'gallery', to: `/${brand}/${product}/gallery` })
    if (tree) parts.push({ label: tree, to: `/${brand}/${product}/gallery/${tree}` })
    if (branch) parts.push({ label: branch, to: null })
  }

  // Last crumb has no link
  if (parts.length > 0 && !route.path.includes('/gallery')) {
    parts[parts.length - 1].to = null
  }

  return parts
})
</script>

<template>
  <nav v-show="visible" class="breadcrumb-bar">
    <button class="menu-btn" @click="sidebarStore.toggle()" title="Toggle sidebar (Ctrl+S)">
      &#9776;
    </button>

    <div class="crumbs">
      <template v-for="(crumb, i) in crumbs" :key="i">
        <span v-if="i > 0" class="separator">/</span>
        <router-link v-if="crumb.to" :to="crumb.to" class="crumb-link">
          {{ crumb.label }}
        </router-link>
        <span v-else class="crumb-current">{{ crumb.label }}</span>
      </template>
    </div>

    <span class="hotkey-hints">Ctrl+S&nbsp;&nbsp;Ctrl+H</span>
  </nav>
</template>

<style scoped>
.breadcrumb-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 48px;
  display: flex;
  align-items: center;
  padding: 0 calc(var(--space-unit) * 2);
  background: color-mix(in srgb, var(--brand-bg) 80%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--brand-border);
}

.menu-btn {
  font-size: 1.25rem;
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  color: var(--brand-text);
  transition: background var(--duration-fast) var(--easing);
  flex-shrink: 0;
}

.menu-btn:hover {
  background: var(--brand-surface);
}

.crumbs {
  flex: 1;
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  margin-left: calc(var(--space-unit) * 1);
  overflow: hidden;
  white-space: nowrap;
}

.separator {
  color: var(--brand-muted);
  font-size: 0.875rem;
}

.crumb-link {
  font-size: 0.875rem;
  color: var(--brand-muted);
  transition: color var(--duration-fast) var(--easing);
  text-transform: capitalize;
}

.crumb-link:hover {
  color: var(--brand-primary);
}

.crumb-current {
  font-size: 0.875rem;
  color: var(--brand-text);
  font-weight: 600;
  text-transform: capitalize;
}

.hotkey-hints {
  font-size: 0.7rem;
  color: var(--brand-muted);
  opacity: 0.6;
  flex-shrink: 0;
  margin-left: auto;
}
</style>

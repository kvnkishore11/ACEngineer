<script setup lang="ts">
import { useSidebarStore } from '../stores/sidebar'
import BrandPanel from './BrandPanel.vue'
import TreesPanel from './TreesPanel.vue'

const sidebarStore = useSidebarStore()

const tabs = ['brand', 'trees', 'settings'] as const
</script>

<template>
  <Teleport to="body">
    <!-- Backdrop -->
    <Transition name="fade">
      <div
        v-if="sidebarStore.isOpen"
        class="sidebar-backdrop"
        @click="sidebarStore.toggle()"
      />
    </Transition>

    <!-- Sidebar Panel -->
    <Transition name="slide">
      <aside
        v-if="sidebarStore.isOpen"
        class="sidebar"
        :style="{ width: sidebarStore.width + 'px' }"
      >
        <div class="sidebar-header">
          <div class="sidebar-tabs">
            <button
              v-for="tab in tabs"
              :key="tab"
              class="tab-btn"
              :class="{ active: sidebarStore.activeTab === tab }"
              @click="sidebarStore.setTab(tab)"
            >
              {{ tab }}
            </button>
          </div>
          <button class="close-btn" @click="sidebarStore.toggle()" title="Close (Ctrl+S)">
            &#x2715;
          </button>
        </div>

        <div class="sidebar-content">
          <BrandPanel v-if="sidebarStore.activeTab === 'brand'" />
          <TreesPanel v-else-if="sidebarStore.activeTab === 'trees'" />
          <div v-else class="settings-placeholder">
            <p>Settings</p>
            <p class="muted">Preferences will go here.</p>
          </div>
        </div>
      </aside>
    </Transition>
  </Teleport>
</template>

<style scoped>
.sidebar-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 899;
  background: var(--brand-overlay);
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 900;
  background: var(--brand-bg);
  border-right: 1px solid var(--brand-border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 2);
  border-bottom: 1px solid var(--brand-border);
  flex-shrink: 0;
}

.sidebar-tabs {
  display: flex;
  gap: 4px;
}

.tab-btn {
  font-size: 0.8rem;
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  text-transform: capitalize;
  font-weight: 500;
  color: var(--brand-muted);
  transition: all var(--duration-fast) var(--easing);
}

.tab-btn:hover {
  background: var(--brand-surface);
  color: var(--brand-text);
}

.tab-btn.active {
  background: var(--brand-primary);
  color: var(--brand-bg);
}

.close-btn {
  font-size: 1rem;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  color: var(--brand-muted);
  transition: all var(--duration-fast) var(--easing);
}

.close-btn:hover {
  background: var(--brand-surface);
  color: var(--brand-text);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: calc(var(--space-unit) * 2);
}

.settings-placeholder {
  text-align: center;
  padding: calc(var(--space-unit) * 6);
}

.muted {
  color: var(--brand-muted);
  font-size: 0.875rem;
  margin-top: calc(var(--space-unit) * 1);
}

/* Transitions */
.slide-enter-active,
.slide-leave-active {
  transition: transform var(--duration-normal) var(--easing);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--duration-normal) var(--easing);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

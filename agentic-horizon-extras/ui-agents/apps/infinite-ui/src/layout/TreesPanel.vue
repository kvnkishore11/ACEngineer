<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTreesStore } from '../stores/trees'

const router = useRouter()
const treesStore = useTreesStore()

const expandedTrees = ref<Set<string>>(new Set())

const brand = computed(() => treesStore.activeBrand)
const product = computed(() => treesStore.activeProduct)

function toggleTree(slug: string) {
  if (expandedTrees.value.has(slug)) {
    expandedTrees.value.delete(slug)
  } else {
    expandedTrees.value.add(slug)
  }
}

function isExpanded(slug: string): boolean {
  return expandedTrees.value.has(slug)
}

function statusIcon(status: string): string {
  switch (status) {
    case 'validated': return '\u2713'
    case 'draft': return '\u25CF'
    case 'generating': return '\u25CB'
    case 'failed': return '\u2717'
    default: return '\u25CB'
  }
}

function statusClass(status: string): string {
  return `status-${status}`
}

function navigateToBranch(treeSlug: string, branchSlug: string) {
  if (brand.value && product.value) {
    router.push(`/${brand.value}/${product.value}/gallery/${treeSlug}/${branchSlug}`)
  }
}
</script>

<template>
  <div class="trees-panel">
    <div v-if="brand && product && treesStore.trees.length > 0" class="tree-explorer">
      <!-- Brand root -->
      <div class="explorer-item root-item">
        <span class="item-label">{{ brand }}</span>
      </div>

      <!-- Product -->
      <div class="explorer-item product-item" style="padding-left: 16px;">
        <span class="item-label">{{ product }}</span>
      </div>

      <!-- Trees -->
      <div v-for="tree in treesStore.trees" :key="tree.slug" class="tree-group">
        <div
          class="explorer-item tree-item"
          style="padding-left: 32px;"
          @click="toggleTree(tree.slug)"
        >
          <span class="chevron">{{ isExpanded(tree.slug) ? '\u25BC' : '\u25B6' }}</span>
          <span class="item-label">{{ tree.name }}</span>
          <span class="item-count">({{ tree.branches.length }})</span>
        </div>

        <!-- Branches (collapsible) -->
        <template v-if="isExpanded(tree.slug)">
          <div
            v-for="branch in tree.branches"
            :key="branch.slug"
            class="explorer-item branch-item"
            style="padding-left: 52px;"
            @click="navigateToBranch(tree.slug, branch.slug)"
          >
            <span class="status-dot" :class="statusClass(branch.status)">
              {{ statusIcon(branch.status) }}
            </span>
            <span class="item-label">{{ branch.name }}</span>
          </div>
        </template>
      </div>
    </div>

    <div v-else class="empty-trees">
      <p>No trees available.</p>
      <p class="hint">Navigate to a product to view its tree hierarchy.</p>
    </div>
  </div>
</template>

<style scoped>
.trees-panel {
  font-size: 0.85rem;
}

.tree-explorer {
  display: flex;
  flex-direction: column;
}

.explorer-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  border-radius: var(--radius-sm);
  cursor: default;
  user-select: none;
  position: relative;
}

.tree-item {
  cursor: pointer;
}

.tree-item:hover {
  background: var(--brand-surface);
}

.branch-item {
  cursor: pointer;
  border-left: 1px solid var(--brand-border);
  margin-left: 40px;
  padding-left: 12px !important;
}

.branch-item:hover {
  background: var(--brand-surface);
}

.root-item {
  font-weight: 700;
  text-transform: capitalize;
}

.product-item {
  font-weight: 600;
  color: var(--brand-primary);
  text-transform: capitalize;
}

.chevron {
  font-size: 0.6rem;
  color: var(--brand-muted);
  width: 12px;
  flex-shrink: 0;
}

.item-label {
  flex: 1;
}

.item-count {
  font-size: 0.7rem;
  color: var(--brand-muted);
}

.status-dot {
  font-size: 0.75rem;
  width: 16px;
  flex-shrink: 0;
  text-align: center;
}

.status-validated { color: var(--brand-success); }
.status-draft { color: var(--brand-warning); }
.status-generating { color: var(--brand-accent); }
.status-failed { color: var(--brand-error); }

.empty-trees {
  text-align: center;
  padding: calc(var(--space-unit) * 4);
  color: var(--brand-muted);
}

.hint {
  font-size: 0.8rem;
  margin-top: calc(var(--space-unit) * 1);
}
</style>

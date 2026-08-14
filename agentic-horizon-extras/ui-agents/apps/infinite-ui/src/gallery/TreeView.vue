<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTreesStore } from '../stores/trees'

const router = useRouter()
const route = useRoute()
const treesStore = useTreesStore()

const brand = computed(() => route.params.brand as string)
const product = computed(() => route.params.product as string)
const treeSlug = computed(() => route.params.tree as string)
const tree = computed(() => treesStore.getTree(treeSlug.value))

function statusIcon(status: string): string {
  switch (status) {
    case 'validated': return '\u2713'
    case 'draft': return '\u25CF'
    case 'generating': return '\u25CB'
    case 'failed': return '\u2717'
    default: return '\u25CB'
  }
}
</script>

<template>
  <div class="tree-view">
    <template v-if="tree">
      <h1 class="tree-title">{{ tree.name }}</h1>
      <p class="tree-desc">{{ tree.description }}</p>

      <div class="branch-grid">
        <div
          v-for="branch in tree.branches"
          :key="branch.slug"
          class="branch-card"
          :class="branch.status"
          @click="router.push(`/${brand}/${product}/gallery/${treeSlug}/${branch.slug}`)"
        >
          <div class="branch-header">
            <span class="status-badge" :class="branch.status">
              {{ statusIcon(branch.status) }} {{ branch.status }}
            </span>
          </div>
          <h2 class="branch-name">{{ branch.name }}</h2>
          <p class="branch-desc">{{ branch.description }}</p>
          <span class="branch-date">{{ branch.created }}</span>
        </div>
      </div>
    </template>
    <div v-else class="empty-state">Tree not found.</div>
  </div>
</template>

<style scoped>
.tree-view {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 8) calc(var(--space-unit) * 4);
}

.tree-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: calc(var(--space-unit) * 1);
}

.tree-desc {
  color: var(--brand-muted);
  margin-bottom: calc(var(--space-unit) * 4);
}

.branch-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: calc(var(--space-unit) * 3);
}

.branch-card {
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 3);
  cursor: pointer;
  transition: all var(--duration-normal) var(--easing);
}

.branch-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.branch-card.validated { border-left: 3px solid var(--brand-success); }
.branch-card.draft { border-left: 3px solid var(--brand-warning); }
.branch-card.generating { border-left: 3px solid var(--brand-accent); }
.branch-card.failed { border-left: 3px solid var(--brand-error); }

.branch-header {
  margin-bottom: calc(var(--space-unit) * 1);
}

.status-badge {
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.validated {
  background: color-mix(in srgb, var(--brand-success) 20%, transparent);
  color: var(--brand-success);
}

.status-badge.draft {
  background: color-mix(in srgb, var(--brand-warning) 20%, transparent);
  color: var(--brand-warning);
}

.status-badge.generating {
  background: color-mix(in srgb, var(--brand-accent) 20%, transparent);
  color: var(--brand-accent);
}

.status-badge.failed {
  background: color-mix(in srgb, var(--brand-error) 20%, transparent);
  color: var(--brand-error);
}

.branch-name {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: calc(var(--space-unit) * 1);
}

.branch-desc {
  font-size: 0.875rem;
  color: var(--brand-muted);
  margin-bottom: calc(var(--space-unit) * 1);
}

.branch-date {
  font-size: 0.75rem;
  color: var(--brand-muted);
}

.empty-state {
  text-align: center;
  padding: calc(var(--space-unit) * 8);
  color: var(--brand-muted);
}
</style>

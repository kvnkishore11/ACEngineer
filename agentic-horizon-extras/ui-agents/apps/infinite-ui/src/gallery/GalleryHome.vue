<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTreesStore } from '../stores/trees'

const router = useRouter()
const route = useRoute()
const treesStore = useTreesStore()

const brand = computed(() => route.params.brand as string)
const product = computed(() => route.params.product as string)
</script>

<template>
  <div class="gallery">
    <h1 class="gallery-title">Gallery</h1>
    <p class="gallery-subtitle">{{ treesStore.treeCount }} trees, {{ treesStore.branchCount }} branches</p>

    <div class="tree-grid">
      <div
        v-for="tree in treesStore.trees"
        :key="tree.slug"
        class="tree-card"
        @click="router.push(`/${brand}/${product}/gallery/${tree.slug}`)"
      >
        <div class="tree-card-header">
          <h2 class="tree-card-name">{{ tree.name }}</h2>
          <span class="branch-count">{{ tree.branches.length }}</span>
        </div>
        <p class="tree-card-desc">{{ tree.description }}</p>
        <div class="tree-card-branches">
          <span
            v-for="b in tree.branches"
            :key="b.slug"
            class="branch-badge"
            :class="b.status"
          >
            {{ b.name }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="treesStore.trees.length === 0" class="empty-state">
      No trees found for this product.
    </div>
  </div>
</template>

<style scoped>
.gallery {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 8) calc(var(--space-unit) * 4);
}

.gallery-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: calc(var(--space-unit) * 1);
}

.gallery-subtitle {
  color: var(--brand-muted);
  margin-bottom: calc(var(--space-unit) * 4);
}

.tree-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: calc(var(--space-unit) * 3);
}

.tree-card {
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 3);
  cursor: pointer;
  transition: all var(--duration-normal) var(--easing);
}

.tree-card:hover {
  border-color: var(--brand-primary);
  box-shadow: var(--shadow-md);
}

.tree-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: calc(var(--space-unit) * 1);
}

.tree-card-name {
  font-size: 1.125rem;
  font-weight: 600;
}

.branch-count {
  background: var(--brand-bg-secondary);
  color: var(--brand-muted);
  padding: 2px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
}

.tree-card-desc {
  color: var(--brand-muted);
  font-size: 0.875rem;
  margin-bottom: calc(var(--space-unit) * 2);
}

.tree-card-branches {
  display: flex;
  flex-wrap: wrap;
  gap: calc(var(--space-unit) * 1);
}

.branch-badge {
  font-size: 0.7rem;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  font-weight: 500;
}

.branch-badge.validated {
  background: color-mix(in srgb, var(--brand-success) 20%, transparent);
  color: var(--brand-success);
}

.branch-badge.draft {
  background: color-mix(in srgb, var(--brand-warning) 20%, transparent);
  color: var(--brand-warning);
}

.branch-badge.generating {
  background: color-mix(in srgb, var(--brand-accent) 20%, transparent);
  color: var(--brand-accent);
}

.branch-badge.failed {
  background: color-mix(in srgb, var(--brand-error) 20%, transparent);
  color: var(--brand-error);
}

.empty-state {
  text-align: center;
  padding: calc(var(--space-unit) * 8);
  color: var(--brand-muted);
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const brands = ref<string[]>([])

onMounted(async () => {
  const res = await fetch('/api/workspace/brands')
  brands.value = await res.json()
})
</script>

<template>
  <div class="workspace">
    <h1 class="workspace-title">Workspace</h1>
    <p class="workspace-subtitle">Select a brand to explore its products</p>
    <div class="brand-grid">
      <div
        v-for="brand in brands"
        :key="brand"
        class="brand-card"
        @click="router.push(`/${brand}`)"
      >
        <div class="brand-icon">{{ brand[0]?.toUpperCase() }}</div>
        <h2 class="brand-name">{{ brand }}</h2>
      </div>
      <div
        v-if="brands.length === 0"
        class="empty-state"
      >
        No brands found. Create a brand directory in src/brands/.
      </div>
    </div>
  </div>
</template>

<style scoped>
.workspace {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 8) calc(var(--space-unit) * 4);
}

.workspace-title {
  font-size: 3rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: calc(var(--space-unit) * 1);
}

.workspace-subtitle {
  color: var(--brand-muted);
  font-size: 1.125rem;
  margin-bottom: calc(var(--space-unit) * 6);
}

.brand-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: calc(var(--space-unit) * 3);
}

.brand-card {
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 4);
  cursor: pointer;
  transition: all var(--duration-normal) var(--easing);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.brand-card:hover {
  border-color: var(--brand-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.brand-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  background: var(--brand-primary);
  color: var(--brand-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  font-weight: 700;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 600;
  text-transform: capitalize;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: calc(var(--space-unit) * 8);
  color: var(--brand-muted);
  font-size: 1.125rem;
}
</style>

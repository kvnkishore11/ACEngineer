<script setup lang="ts">
import { computed, shallowRef, watchEffect } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const brand = computed(() => route.params.brand as string)
const product = computed(() => route.params.product as string)
const tree = computed(() => route.params.tree as string)
const branch = computed(() => route.params.branch as string)

const leafModules = import.meta.glob('../brands/**/*/index.vue')

const LeafComponent = shallowRef<ReturnType<typeof import('vue')['defineComponent']> | null>(null)
const loadError = shallowRef(false)

watchEffect(async () => {
  loadError.value = false
  LeafComponent.value = null

  const path = `../brands/${brand.value}/products/${product.value}/trees/${tree.value}/${branch.value}/index.vue`
  const loader = leafModules[path]

  if (loader) {
    try {
      const mod = await loader() as { default: ReturnType<typeof import('vue')['defineComponent']> }
      LeafComponent.value = mod.default
    } catch {
      loadError.value = true
    }
  } else {
    loadError.value = true
  }
})
</script>

<template>
  <div class="branch-preview">
    <component v-if="LeafComponent" :is="LeafComponent" />
    <div v-else-if="loadError" class="preview-error">
      <p>Could not load component:</p>
      <code>{{ brand }}/{{ product }}/{{ tree }}/{{ branch }}</code>
    </div>
    <div v-else class="preview-loading">
      Loading...
    </div>
  </div>
</template>

<style scoped>
.branch-preview {
  width: 100%;
  min-height: calc(100vh - 56px);
}

.preview-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: var(--brand-error);
  gap: calc(var(--space-unit) * 2);
}

.preview-error code {
  background: var(--brand-surface);
  padding: calc(var(--space-unit) * 1) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
}

.preview-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: var(--brand-muted);
}
</style>

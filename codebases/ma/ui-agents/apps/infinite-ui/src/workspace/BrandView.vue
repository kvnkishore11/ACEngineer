<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import yaml from 'yaml'

const router = useRouter()
const route = useRoute()
const brand = route.params.brand as string
const products = ref<string[]>([])
const brandConfig = ref<Record<string, unknown> | null>(null)

onMounted(async () => {
  const [productsRes, brandRes] = await Promise.all([
    fetch(`/api/workspace/products/${brand}`),
    fetch(`/api/brand/${brand}`),
  ])
  products.value = await productsRes.json()
  if (brandRes.ok) {
    brandConfig.value = yaml.parse(await brandRes.text())
  }
})

const palette = ['primary', 'secondary', 'accent', 'background', 'surface', 'text', 'muted', 'border', 'error', 'warning', 'success'] as const

function getPaletteColor(key: string): string {
  const p = brandConfig.value?.palette as Record<string, string> | undefined
  return p?.[key] ?? '#333'
}
</script>

<template>
  <div class="brand-view">
    <h1 class="brand-title">{{ brand }}</h1>
    <p class="brand-tagline" v-if="brandConfig">
      {{ (brandConfig as Record<string, unknown>).tagline }}
    </p>

    <div class="palette-strip" v-if="brandConfig">
      <div
        v-for="key in palette"
        :key="key"
        class="palette-swatch"
        :style="{ backgroundColor: getPaletteColor(key) }"
        :title="key"
      />
    </div>

    <h2 class="section-title">Products</h2>
    <div class="product-grid">
      <div
        v-for="product in products"
        :key="product"
        class="product-card"
        @click="router.push(`/${brand}/${product}`)"
      >
        <h3 class="product-name">{{ product }}</h3>
        <span class="product-arrow">&rarr;</span>
      </div>
      <div v-if="products.length === 0" class="empty-state">
        No products found for this brand.
      </div>
    </div>
  </div>
</template>

<style scoped>
.brand-view {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 8) calc(var(--space-unit) * 4);
}

.brand-title {
  font-size: 3rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  text-transform: capitalize;
  margin-bottom: calc(var(--space-unit) * 1);
}

.brand-tagline {
  color: var(--brand-muted);
  font-size: 1.125rem;
  margin-bottom: calc(var(--space-unit) * 4);
}

.palette-strip {
  display: flex;
  gap: 4px;
  margin-bottom: calc(var(--space-unit) * 6);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.palette-swatch {
  width: 48px;
  height: 32px;
  transition: transform var(--duration-fast) var(--easing);
}

.palette-swatch:hover {
  transform: scaleY(1.3);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: calc(var(--space-unit) * 3);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: calc(var(--space-unit) * 3);
}

.product-card {
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 4);
  cursor: pointer;
  transition: all var(--duration-normal) var(--easing);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.product-card:hover {
  border-color: var(--brand-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.product-name {
  font-size: 1.25rem;
  font-weight: 600;
  text-transform: capitalize;
}

.product-arrow {
  font-size: 1.5rem;
  color: var(--brand-muted);
  transition: color var(--duration-fast) var(--easing);
}

.product-card:hover .product-arrow {
  color: var(--brand-primary);
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: calc(var(--space-unit) * 8);
  color: var(--brand-muted);
}
</style>

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import yaml from 'yaml'
import { BrandSchema, type BrandConfig } from '../schemas/brand.schema'

function deepMerge(target: Record<string, unknown>, source: Record<string, unknown>): Record<string, unknown> {
  const result = { ...target }
  for (const key of Object.keys(source)) {
    const sv = source[key]
    const tv = target[key]
    if (sv && typeof sv === 'object' && !Array.isArray(sv) && tv && typeof tv === 'object' && !Array.isArray(tv)) {
      result[key] = deepMerge(tv as Record<string, unknown>, sv as Record<string, unknown>)
    } else {
      result[key] = sv
    }
  }
  return result
}

export const useBrandStore = defineStore('brand', () => {
  const config = ref<BrandConfig | null>(null)
  const isDirty = ref(false)
  const lastSaved = ref<Date | null>(null)
  const activeBrand = ref<string | null>(null)
  const activeProduct = ref<string | null>(null)

  const tokens = computed(() => {
    if (!config.value) return {}
    const { palette, typography, spacing, motion, breakpoints, shadows } = config.value
    return {
      '--brand-primary': palette.primary,
      '--brand-secondary': palette.secondary,
      '--brand-accent': palette.accent,
      '--brand-bg': palette.background,
      '--brand-bg-secondary': palette['bg-secondary'],
      '--brand-surface': palette.surface,
      '--brand-text': palette.text,
      '--brand-muted': palette.muted,
      '--brand-border': palette.border,
      '--brand-overlay': palette.overlay,
      '--brand-error': palette.error,
      '--brand-warning': palette.warning,
      '--brand-success': palette.success,
      '--font-heading': typography.heading,
      '--font-body': typography.body,
      '--font-mono': typography.mono,
      '--space-unit': spacing.unit,
      '--radius-sm': spacing['radius-sm'],
      '--radius-md': spacing['radius-md'],
      '--radius-lg': spacing['radius-lg'],
      '--container-max': spacing['container-max'],
      '--duration-fast': motion['duration-fast'],
      '--duration-normal': motion['duration-normal'],
      '--duration-slow': motion['duration-slow'],
      '--easing': motion.easing,
      '--bp-sm': breakpoints.sm,
      '--bp-md': breakpoints.md,
      '--bp-lg': breakpoints.lg,
      '--bp-xl': breakpoints.xl,
      '--shadow-sm': shadows.sm,
      '--shadow-md': shadows.md,
      '--shadow-lg': shadows.lg,
    }
  })

  async function load(brand: string, product: string) {
    activeBrand.value = brand
    activeProduct.value = product

    const brandRes = await fetch(`/api/brand/${brand}`)
    const brandRaw = yaml.parse(await brandRes.text())

    const productRes = await fetch(`/api/brand/${brand}/${product}`)
    const productRaw = productRes.ok
      ? yaml.parse(await productRes.text())
      : {}

    const merged = deepMerge(brandRaw, productRaw ?? {})
    config.value = BrandSchema.parse(merged)
    isDirty.value = false
  }

  function update(patch: Record<string, unknown>) {
    if (!config.value) return
    const merged = deepMerge(config.value as unknown as Record<string, unknown>, patch)
    config.value = merged as unknown as BrandConfig
    isDirty.value = true
  }

  async function save() {
    if (!activeBrand.value || !activeProduct.value || !config.value) return
    const validated = BrandSchema.parse(config.value)
    await fetch(`/api/brand/${activeBrand.value}/${activeProduct.value}`, {
      method: 'POST',
      body: yaml.stringify(validated),
    })
    isDirty.value = false
    lastSaved.value = new Date()
  }

  function clear() {
    config.value = null
    isDirty.value = false
    lastSaved.value = null
    activeBrand.value = null
    activeProduct.value = null
  }

  return { config, isDirty, lastSaved, activeBrand, activeProduct, tokens, load, update, save, clear }
})

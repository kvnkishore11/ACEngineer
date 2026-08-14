import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import yaml from 'yaml'
import dagre from '@dagrejs/dagre'
import { TreesManifestSchema, type TreesManifest, type Tree, type Branch } from '../schemas/trees.schema'
import { useCanvasStore } from './canvas'

export const useTreesStore = defineStore('trees', () => {
  const manifest = ref<TreesManifest | null>(null)
  const activeBrand = ref<string | null>(null)
  const activeProduct = ref<string | null>(null)

  const trees = computed(() => manifest.value?.trees ?? [])
  const treeCount = computed(() => trees.value.length)
  const branchCount = computed(() =>
    trees.value.reduce((sum, t) => sum + t.branches.length, 0)
  )

  const statusCounts = computed(() => {
    const counts = { validated: 0, generating: 0, validating: 0, draft: 0, failed: 0 }
    trees.value.forEach(t => t.branches.forEach(b => {
      if (b.status in counts) counts[b.status as keyof typeof counts]++
    }))
    return counts
  })

  const validatedCount = computed(() => statusCounts.value.validated)

  const treeBySlug = computed(() =>
    Object.fromEntries(trees.value.map(t => [t.slug, t]))
  )

  function getTree(slug: string): Tree | undefined {
    return treeBySlug.value[slug]
  }

  function getBranch(treeSlug: string, branchSlug: string): Branch | undefined {
    return getTree(treeSlug)?.branches.find(b => b.slug === branchSlug)
  }

  const nodes = computed(() => {
    if (!manifest.value) return []

    const canvasStore = useCanvasStore()
    const pSize = canvasStore.previewSize

    const g = new dagre.graphlib.Graph()
    g.setDefaultEdgeLabel(() => ({}))
    g.setGraph({ rankdir: 'LR', nodesep: 120, ranksep: 200 })

    const brandId = 'brand'
    g.setNode(brandId, { width: 220, height: 140 })

    trees.value.forEach(tree => {
      const treeId = `tree-${tree.slug}`
      g.setNode(treeId, { width: 160, height: 50 })
      g.setEdge(brandId, treeId)

      tree.branches.forEach(branch => {
        const branchId = `branch-${tree.slug}-${branch.slug}`
        const isPreview = branch.status === 'validated'
        const nodeWidth = isPreview ? pSize.width + 40 : 180
        const nodeHeight = isPreview ? pSize.height + 60 : (branch.forkedFrom ? 200 : 80)
        g.setNode(branchId, { width: nodeWidth, height: nodeHeight })
        if (branch.forkedFrom) {
          const parentId = `branch-${tree.slug}-${branch.forkedFrom}`
          g.setEdge(parentId, branchId)
        } else {
          g.setEdge(treeId, branchId)
        }
      })
    })

    dagre.layout(g)

    const result: Array<{
      id: string
      type: string
      position: { x: number; y: number }
      data: Record<string, unknown>
    }> = []

    const brandNode = g.node(brandId)
    result.push({
      id: brandId,
      type: 'brand',
      position: { x: brandNode.x - 110, y: brandNode.y - 70 },
      data: { label: manifest.value?.brand ?? '' },
    })

    trees.value.forEach(tree => {
      const treeId = `tree-${tree.slug}`
      const tn = g.node(treeId)
      result.push({
        id: treeId,
        type: 'tree',
        position: { x: tn.x - 80, y: tn.y - 25 },
        data: { ...tree },
      })

      tree.branches.forEach(branch => {
        const branchId = `branch-${tree.slug}-${branch.slug}`
        const bn = g.node(branchId)
        const isPreview = branch.status === 'validated'
        const nodeWidth = isPreview ? pSize.width + 40 : 180
        const nodeHeight = isPreview ? pSize.height + 60 : (branch.forkedFrom ? 200 : 80)
        result.push({
          id: branchId,
          type: isPreview ? 'preview-branch' : 'branch',
          position: { x: bn.x - nodeWidth / 2, y: bn.y - nodeHeight / 2 },
          data: { ...branch, treeSlug: tree.slug },
        })
      })
    })

    return result
  })

  const edges = computed(() => {
    const result: Array<{ id: string; source: string; target: string }> = []
    trees.value.forEach(tree => {
      result.push({
        id: `brand->${tree.slug}`,
        source: 'brand',
        target: `tree-${tree.slug}`,
      })
      tree.branches.forEach(branch => {
        const source = branch.forkedFrom
          ? `branch-${tree.slug}-${branch.forkedFrom}`
          : `tree-${tree.slug}`
        result.push({
          id: `${tree.slug}->${branch.slug}`,
          source,
          target: `branch-${tree.slug}-${branch.slug}`,
        })
      })
    })
    return result
  })

  async function load(brand: string, product: string) {
    activeBrand.value = brand
    activeProduct.value = product
    const res = await fetch(`/api/trees/${brand}/${product}`)
    if (res.ok) {
      const raw = await res.text()
      manifest.value = TreesManifestSchema.parse(yaml.parse(raw))
    } else {
      manifest.value = null
    }
  }

  async function save() {
    if (!activeBrand.value || !activeProduct.value || !manifest.value) return
    const validated = TreesManifestSchema.parse(manifest.value)
    await fetch(`/api/trees/${activeBrand.value}/${activeProduct.value}`, {
      method: 'POST',
      body: yaml.stringify(validated),
    })
  }

  function clear() {
    manifest.value = null
    activeBrand.value = null
    activeProduct.value = null
  }

  return {
    manifest, activeBrand, activeProduct,
    trees, treeCount, branchCount, statusCounts, validatedCount, treeBySlug,
    getTree, getBranch,
    nodes, edges,
    load, save, clear,
  }
})

<script setup lang="ts">
import { computed, markRaw, onMounted, onUnmounted } from 'vue'
import { VueFlow, type NodeMouseEvent } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { MiniMap } from '@vue-flow/minimap'
import { useRouter, useRoute } from 'vue-router'
import { useTreesStore } from '../stores/trees'
import { useCanvasStore } from '../stores/canvas'
import { useActivityStore } from '../stores/activity'
import TreeNode from './TreeNode.vue'
import BranchNode from './BranchNode.vue'
import PreviewBranchNode from './PreviewBranchNode.vue'
import BrandNode from './BrandNode.vue'
import PreviewControls from './PreviewControls.vue'
import ActivityPanel from './ActivityPanel.vue'

const router = useRouter()
const route = useRoute()
const treesStore = useTreesStore()
const canvasStore = useCanvasStore()
const activityStore = useActivityStore()

const brand = computed(() => route.params.brand as string)
const product = computed(() => route.params.product as string)

const nodeTypes: Record<string, unknown> = {
  brand: markRaw(BrandNode),
  tree: markRaw(TreeNode),
  branch: markRaw(BranchNode),
  'preview-branch': markRaw(PreviewBranchNode),
}

function onNodeClick(event: NodeMouseEvent) {
  const node = event.node
  canvasStore.selectNode(node.id)
  if (node.type === 'branch' || node.type === 'preview-branch') {
    const treeSlug = (node.data as Record<string, unknown>).treeSlug as string
    const branchSlug = (node.data as Record<string, unknown>).slug as string
    router.push(`/${brand.value}/${product.value}/gallery/${treeSlug}/${branchSlug}`)
  }
}

onMounted(() => {
  if (brand.value && product.value) {
    activityStore.startPolling(brand.value, product.value)
  }
})

onUnmounted(() => {
  activityStore.stopPolling()
})
</script>

<template>
  <div class="canvas-container">
    <PreviewControls />
    <VueFlow
      :nodes="(treesStore.nodes as any)"
      :edges="(treesStore.edges as any)"
      :node-types="(nodeTypes as any)"
      :default-zoom="1"
      :min-zoom="0.2"
      :max-zoom="3"
      fit-view-on-init
      @node-click="onNodeClick"
    >
      <Background />
      <MiniMap />
    </VueFlow>
    <ActivityPanel />
  </div>
</template>

<style scoped>
.canvas-container {
  position: relative;
  width: 100%;
  height: calc(100vh - 56px);
}
</style>

<style>
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/minimap/dist/style.css';

.vue-flow {
  background-color: var(--brand-bg-secondary);
}
</style>

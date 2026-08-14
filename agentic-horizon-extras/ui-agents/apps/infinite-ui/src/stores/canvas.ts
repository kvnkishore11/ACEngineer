import { defineStore } from 'pinia'
import { ref } from 'vue'

interface PreviewSize {
  width: number
  height: number
  scale: number
}

const previewSizePresets: Record<string, PreviewSize> = {
  small:  { width: 480, height: 270, scale: 0.375 },
  medium: { width: 640, height: 360, scale: 0.5 },
  large:  { width: 960, height: 540, scale: 0.75 },
}

export type PreviewSizePreset = 'small' | 'medium' | 'large'

export const useCanvasStore = defineStore('canvas', () => {
  const zoom = ref(1)
  const pan = ref({ x: 0, y: 0 })
  const selectedNode = ref<string | null>(null)
  const hoveredNode = ref<string | null>(null)
  const previewSize = ref<PreviewSize>({ ...previewSizePresets.small })
  const activityPanelOpen = ref(true)

  function selectNode(id: string | null) {
    selectedNode.value = id
  }

  function setPreviewSize(preset: PreviewSizePreset) {
    const size = previewSizePresets[preset]
    previewSize.value = { ...size }
  }

  function resetView() {
    zoom.value = 1
    pan.value = { x: 0, y: 0 }
  }

  function toggleActivityPanel() { activityPanelOpen.value = !activityPanelOpen.value }

  return { zoom, pan, selectedNode, hoveredNode, previewSize, activityPanelOpen, selectNode, setPreviewSize, resetView, toggleActivityPanel }
})

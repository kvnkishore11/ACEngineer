import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import yaml from 'yaml'
import { useTreesStore } from './trees'

interface ActivityBranch {
  slug: string
  tree: string
  phase: string
  team: string
}

interface ActivityData {
  active: boolean
  started: string
  pipeline: string
  brief: string
  branches: ActivityBranch[]
}

export const useActivityStore = defineStore('activity', () => {
  const activity = ref<ActivityData | null>(null)
  const pollInterval = ref<ReturnType<typeof setInterval> | null>(null)

  const isActive = computed(() => activity.value?.active === true)
  const branches = computed(() => activity.value?.branches ?? [])
  const pipeline = computed(() => activity.value?.pipeline ?? '')
  const brief = computed(() => activity.value?.brief ?? '')

  async function poll(brand: string, product: string) {
    try {
      const res = await fetch(`/api/activity/${brand}/${product}`)
      if (res.ok) {
        const raw = await res.text()
        activity.value = yaml.parse(raw) as ActivityData
      } else {
        activity.value = null
      }
    } catch {
      activity.value = null
    }
    // Also refresh trees to pick up status changes
    const treesStore = useTreesStore()
    if (treesStore.activeBrand && treesStore.activeProduct) {
      treesStore.load(treesStore.activeBrand, treesStore.activeProduct)
    }
  }

  function startPolling(brand: string, product: string) {
    stopPolling()
    poll(brand, product)
    pollInterval.value = setInterval(() => poll(brand, product), 3000)
  }

  function stopPolling() {
    if (pollInterval.value) {
      clearInterval(pollInterval.value)
      pollInterval.value = null
    }
    activity.value = null
  }

  return { activity, isActive, branches, pipeline, brief, startPolling, stopPolling }
})

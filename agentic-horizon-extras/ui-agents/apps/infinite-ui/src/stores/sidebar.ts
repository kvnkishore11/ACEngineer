import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSidebarStore = defineStore('sidebar', () => {
  const isOpen = ref(false)
  const activeTab = ref<'brand' | 'trees' | 'settings'>('brand')
  const width = ref(400)

  function toggle() {
    isOpen.value = !isOpen.value
  }

  function setTab(tab: 'brand' | 'trees' | 'settings') {
    activeTab.value = tab
  }

  return { isOpen, activeTab, width, toggle, setTab }
})

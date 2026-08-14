import { watchEffect } from 'vue'
import { useBrandStore } from '../stores/brand'

export function useBrandTokens() {
  const brandStore = useBrandStore()

  watchEffect(() => {
    const tokens = brandStore.tokens
    const root = document.documentElement
    for (const [key, value] of Object.entries(tokens)) {
      if (value) {
        root.style.setProperty(key, value)
      }
    }
  })
}

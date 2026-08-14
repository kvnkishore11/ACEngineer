// live-bench frontend entry point. Wires Vue 3 + Pinia + vue-router, applies
// the persisted theme before mounting so the first paint already has the
// correct colour palette (no "flash of unthemed content").

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import { DEFAULT_THEME, type ThemeName } from './themes'

// Pre-mount theme application — read localStorage BEFORE we let any component
// mount so the <html data-theme> attribute is already correct on first paint.
function applyInitialTheme() {
  let theme: ThemeName = DEFAULT_THEME
  try {
    const stored = localStorage.getItem('live-bench-theme')
    if (stored) {
      theme = stored as ThemeName
    }
  } catch {
    /* localStorage unavailable; stick with default */
  }
  document.documentElement.dataset.theme = theme
}
applyInitialTheme()

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

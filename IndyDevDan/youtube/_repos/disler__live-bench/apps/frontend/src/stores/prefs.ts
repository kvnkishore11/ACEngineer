// Presentation preferences — theme + density. Persisted to localStorage so a
// presenter who flips to a theme survives a refresh on camera. Theme is also
// reflected onto <html data-theme> so the CSS variable cascade picks it up
// without a re-render.

import { defineStore } from 'pinia'
import { DEFAULT_THEME, type ThemeName } from '../themes'

export type Density = 'S' | 'M' | 'L'

const THEME_KEY = 'live-bench-theme'
const DENSITY_KEY = 'live-bench-density'

const VALID_THEMES: ThemeName[] = [
  'obsidian',
  'midnight',
  'matrix',
  'vaporwave',
  'tokyo',
  'sunset',
  'arctic',
  'paper',
  'mono',
  'solarized',
]

function readTheme(): ThemeName {
  try {
    const raw = localStorage.getItem(THEME_KEY)
    if (raw && (VALID_THEMES as string[]).includes(raw)) {
      return raw as ThemeName
    }
  } catch {
    /* localStorage may not exist (SSR / tests) */
  }
  return DEFAULT_THEME
}

function readDensity(): Density {
  try {
    const raw = localStorage.getItem(DENSITY_KEY)
    if (raw === 'S' || raw === 'M' || raw === 'L') return raw
  } catch {
    /* swallow */
  }
  return 'M'
}

export const usePrefsStore = defineStore('prefs', {
  state: () => ({
    theme: readTheme(),
    density: readDensity() as Density,
  }),
  actions: {
    setTheme(theme: ThemeName) {
      this.theme = theme
      try {
        localStorage.setItem(THEME_KEY, theme)
      } catch {
        /* swallow */
      }
      if (typeof document !== 'undefined') {
        document.documentElement.dataset.theme = theme
      }
    },
    setDensity(density: Density) {
      this.density = density
      try {
        localStorage.setItem(DENSITY_KEY, density)
      } catch {
        /* swallow */
      }
    },
  },
})

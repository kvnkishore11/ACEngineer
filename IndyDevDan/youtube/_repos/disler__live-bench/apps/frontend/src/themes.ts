// Theme registry — exported names + display labels + swatch colours used by
// the ThemeSwitcher dropdown. The actual CSS variable values for each theme
// live in src/styles/themes.css under [data-theme="..."] blocks; this file is
// only the lightweight TypeScript metadata layer.
//
// Default theme is `obsidian` per spec §13.2.

export type ThemeName =
  | 'obsidian'
  | 'midnight'
  | 'matrix'
  | 'vaporwave'
  | 'synthwave'
  | 'tokyo'
  | 'sunset'
  | 'arctic'
  | 'paper'
  | 'mono'
  | 'solarized'

export interface ThemeEntry {
  name: ThemeName
  label: string
  swatch: string
}

export const THEMES: ThemeEntry[] = [
  { name: 'obsidian', label: 'Obsidian', swatch: '#080c17' },
  { name: 'midnight', label: 'Midnight', swatch: '#0b1020' },
  { name: 'matrix', label: 'Matrix', swatch: '#000000' },
  { name: 'vaporwave', label: 'Vaporwave', swatch: '#1a0b2e' },
  { name: 'synthwave', label: 'SynthWave 84', swatch: '#262335' },
  { name: 'tokyo', label: 'Tokyo Night', swatch: '#1a1b26' },
  { name: 'sunset', label: 'Sunset', swatch: '#1f0f1a' },
  { name: 'arctic', label: 'Arctic', swatch: '#eef4ff' },
  { name: 'paper', label: 'Paper', swatch: '#faf8f3' },
  { name: 'mono', label: 'Mono', swatch: '#000000' },
  { name: 'solarized', label: 'Solarized', swatch: '#002b36' },
]

export const DEFAULT_THEME: ThemeName = 'obsidian'

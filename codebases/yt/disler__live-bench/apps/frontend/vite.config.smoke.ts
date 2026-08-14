// Smoke-only vite config — proxies to the smoke backend on 18789 and serves
// the dev bundle on 15787. Not used by normal `pnpm dev`; explicitly passed
// via `--config vite.config.smoke.ts` during frontend smoke runs so they
// don't collide with the main backend on 8787.
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const BACKEND = 'http://127.0.0.1:18789'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 15787,
    strictPort: true,
    proxy: {
      '/benchmarks': BACKEND,
      '/ingest': BACKEND,
      '/stream': {
        target: BACKEND,
        changeOrigin: true,
        // SSE needs no body buffering, but vite handles that for us — keep
        // `ws: false` since SSE is plain HTTP, not upgraded websocket.
        ws: false,
      },
      '/healthz': BACKEND,
    },
  },
})

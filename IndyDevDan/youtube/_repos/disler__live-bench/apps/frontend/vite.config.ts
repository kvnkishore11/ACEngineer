import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const BACKEND = 'http://127.0.0.1:8787'

export default defineConfig({
  plugins: [vue()],
  server: {
    // Bind to all interfaces so both http://localhost and http://127.0.0.1
    // work (and the dashboard is reachable from any LAN device on shoot day).
    // Vite's default "localhost" binds IPv6 (::1) only on modern Node, which
    // makes `http://127.0.0.1:5787` fail with ECONNREFUSED — see #1 in the README.
    host: true,
    port: 5787,
    strictPort: true,
    proxy: {
      '/benchmarks': BACKEND,
      '/ingest': BACKEND,
      '/stream': BACKEND,
      '/healthz': BACKEND,
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
  },
})

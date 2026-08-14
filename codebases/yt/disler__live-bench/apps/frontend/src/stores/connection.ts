// Trivial global store for the active SSE connection state, so the NavBar's
// ConnectionBadge can render it without having to thread the state through
// props from BenchmarkPage (the only page that has a live stream).

import { defineStore } from 'pinia'
import type { ConnectionState } from '../api/stream'

export const useConnectionStore = defineStore('connection', {
  state: (): { state: ConnectionState } => ({ state: 'disconnected' }),
  actions: {
    set(state: ConnectionState) {
      this.state = state
    },
  },
})

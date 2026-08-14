// Pinia store for the landing page — the catalogue of benchmarks loaded from
// `benchmarks/*.yaml` on backend boot. Mirrors GET /benchmarks. Loaded once on
// LandingPage mount; not reactive to live updates (this is a directory listing,
// not a chart).

import { defineStore } from 'pinia'
import { listBenchmarks } from '../api/rest'
import type { BenchmarkSummary } from '../schemas'

interface BenchmarksStoreState {
  list: BenchmarkSummary[]
  loading: boolean
  error: string | null
}

export const useBenchmarksStore = defineStore('benchmarks', {
  state: (): BenchmarksStoreState => ({
    list: [],
    loading: false,
    error: null,
  }),
  actions: {
    async load() {
      this.loading = true
      this.error = null
      try {
        const res = await listBenchmarks()
        this.list = res.benchmarks
      } catch (err) {
        this.error = err instanceof Error ? err.message : String(err)
        this.list = []
      } finally {
        this.loading = false
      }
    },
  },
})

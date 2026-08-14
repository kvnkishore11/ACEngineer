// Vue Router configuration — two routes only (spec §8.1).
//
//   /                    → LandingPage (dropdown of benchmarks)
//   /benchmark/:sessionId → BenchmarkPage (live chart for that session)

import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from './pages/LandingPage.vue'
import BenchmarkPage from './pages/BenchmarkPage.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingPage,
    },
    {
      path: '/benchmark/:sessionId',
      name: 'benchmark',
      component: BenchmarkPage,
      // `props: true` unwraps the route param straight into the component's
      // `defineProps<{ sessionId: string }>()` — cleaner than reading
      // useRoute().params.sessionId everywhere.
      props: true,
    },
  ],
})

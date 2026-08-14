/**
 * LandingPage — sortable table behaviour.
 *
 * Covers:
 *   - default sort is last_update DESC (most-recent first)
 *   - rows with null last_update sink to the bottom regardless of direction
 *   - clicking the name header sorts by title (ASC by default, toggles on re-click)
 *   - clicking the last-updated header re-applies descending sort then toggles
 *   - the View button navigates to /benchmark/:sessionId
 */

import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { createMemoryHistory, createRouter, type Router } from 'vue-router'
import LandingPage from './LandingPage.vue'
import { useBenchmarksStore } from '../stores/benchmarks'

// Stub the REST module so load() resolves synchronously to a known fixture.
vi.mock('../api/rest', () => ({
  listBenchmarks: vi.fn(),
}))
import { listBenchmarks } from '../api/rest'

const FIXTURE = [
  {
    session_id: 'alpha-bench',
    title: 'Alpha',
    subtitle: 'the first',
    better: 'higher' as const,
    completed_count: 1,
    total_count: 3,
    last_update: '2026-04-07T10:00:00.000000+00:00',
    chart_count: 1,
  },
  {
    session_id: 'charlie-bench',
    title: 'Charlie',
    subtitle: null,
    better: 'lower' as const,
    completed_count: 0,
    total_count: 2,
    last_update: '2026-04-07T12:00:00.000000+00:00', // newest
    chart_count: 1,
  },
  {
    session_id: 'bravo-bench',
    title: 'Bravo',
    subtitle: 'the second',
    better: 'higher' as const,
    completed_count: 2,
    total_count: 2,
    last_update: null, // never updated
    chart_count: 1,
  },
  {
    session_id: 'delta-bench',
    title: 'Delta',
    subtitle: null,
    better: 'higher' as const,
    completed_count: 0,
    total_count: 4,
    last_update: '2026-04-07T11:00:00.000000+00:00',
    chart_count: 1,
  },
  {
    session_id: 'multi-bench',
    title: 'Multi',
    subtitle: 'three charts',
    better: null,
    completed_count: 0,
    total_count: 6,
    last_update: '2026-04-07T13:00:00.000000+00:00',
    chart_count: 3,
  },
]

function makeRouter(): Router {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', name: 'landing', component: { template: '<div/>' } },
      { path: '/benchmark/:sessionId', name: 'benchmark', component: { template: '<div/>' } },
    ],
  })
}

async function mountLanding() {
  vi.mocked(listBenchmarks).mockResolvedValue({ benchmarks: FIXTURE })
  const pinia = createPinia()
  setActivePinia(pinia)
  const router = makeRouter()
  await router.push('/')
  await router.isReady()

  const wrapper = mount(LandingPage, {
    global: {
      plugins: [pinia, router],
    },
  })
  // wait for onMounted → store.load() → list to populate
  await flushPromises()
  await flushPromises()
  return { wrapper, router }
}

function rowSessionIds(wrapper: ReturnType<typeof mount>): string[] {
  return wrapper
    .findAll('tbody tr')
    .map((r) => r.attributes('data-testid')?.replace(/^row-/, '') ?? '')
}

describe('LandingPage table', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders one row per benchmark', async () => {
    const { wrapper } = await mountLanding()
    expect(wrapper.findAll('tbody tr')).toHaveLength(FIXTURE.length)
  })

  it('default sort is last_update DESC, nulls last', async () => {
    const { wrapper } = await mountLanding()
    // expected order: multi (13:00), charlie (12:00), delta (11:00), alpha (10:00), bravo (null)
    expect(rowSessionIds(wrapper)).toEqual([
      'multi-bench',
      'charlie-bench',
      'delta-bench',
      'alpha-bench',
      'bravo-bench',
    ])
  })

  it('clicking Name header sorts by title ASC, nulls intermingled by title', async () => {
    const { wrapper } = await mountLanding()
    await wrapper.find('[data-testid="sort-by-name"]').trigger('click')
    expect(rowSessionIds(wrapper)).toEqual([
      'alpha-bench',
      'bravo-bench',
      'charlie-bench',
      'delta-bench',
      'multi-bench',
    ])
  })

  it('clicking Name header twice toggles to DESC', async () => {
    const { wrapper } = await mountLanding()
    const head = wrapper.find('[data-testid="sort-by-name"]')
    await head.trigger('click') // asc
    await head.trigger('click') // desc
    expect(rowSessionIds(wrapper)).toEqual([
      'multi-bench',
      'delta-bench',
      'charlie-bench',
      'bravo-bench',
      'alpha-bench',
    ])
  })

  it('null last_update always sinks to the bottom regardless of direction', async () => {
    const { wrapper } = await mountLanding()
    // Default (desc) → bravo (null) last
    expect(rowSessionIds(wrapper).at(-1)).toBe('bravo-bench')
    // Switch to ASC — bravo should STILL be last (nulls are always "never")
    await wrapper.find('[data-testid="sort-by-last-update"]').trigger('click')
    expect(rowSessionIds(wrapper).at(-1)).toBe('bravo-bench')
  })

  it('View button navigates to /benchmark/:sessionId', async () => {
    const { wrapper, router } = await mountLanding()
    await wrapper.find('[data-testid="view-charlie-bench"]').trigger('click')
    await flushPromises()
    expect(router.currentRoute.value.name).toBe('benchmark')
    expect(router.currentRoute.value.params.sessionId).toBe('charlie-bench')
  })

  it('Charts column renders "N charts" for multi-chart benchmarks', async () => {
    const { wrapper } = await mountLanding()
    const multi = wrapper.find('[data-testid="charts-multi-bench"]')
    expect(multi.exists()).toBe(true)
    expect(multi.text()).toBe('3 charts')
  })

  it('Charts column renders "↑ higher" / "↓ lower" for single-chart benchmarks', async () => {
    const { wrapper } = await mountLanding()
    const alpha = wrapper.find('[data-testid="charts-alpha-bench"]')
    expect(alpha.text()).toBe('↑ higher')
    const charlie = wrapper.find('[data-testid="charts-charlie-bench"]')
    expect(charlie.text()).toBe('↓ lower')
  })
})

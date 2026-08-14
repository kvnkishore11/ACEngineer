// Exercises the §14.1 state machine inside AnimatedBar.vue.
//
// The bar coalesces fast updates: while an animation is in flight, any new
// value is stored in `pending` (overwriting any earlier pending), and only
// the most recent pending value is animated to next. Intermediate values are
// silently dropped — so a rapid 10 → 20 → 30 → 40 burst during one
// animation window produces exactly two animation legs (to 10 and then to
// 40), skipping 20 and 30.

import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import AnimatedBar from './AnimatedBar.vue'

// Vue component instance type with our exposed refs.
interface AnimatedBarExposed {
  current: { value: number }
  target: { value: number }
  pending: { value: number | null }
  displayValue: { value: number }
  onTransitionEnd: () => void
}

function mountBar(value: number) {
  return mount(AnimatedBar, {
    props: {
      value,
      min: 0,
      max: 100,
      direction: 'BT',
      slotX: 0,
      slotY: 0,
      slotWidth: 100,
      slotHeight: 200,
      color: '#e86b3a',
      gradientId: null,
    },
  })
}

function exposed(wrapper: ReturnType<typeof mountBar>): AnimatedBarExposed {
  // vm.$.exposed holds the defineExpose() contents.
  const vm = wrapper.vm as unknown as { $: { exposed: AnimatedBarExposed } }
  return vm.$.exposed
}

describe('AnimatedBar state machine (§14.1)', () => {
  beforeEach(() => {
    // No global timers needed; the state machine is driven manually via
    // onTransitionEnd() + reactive prop updates.
  })

  it('starts a new animation when idle and the value changes', async () => {
    const wrapper = mountBar(0)
    const e = exposed(wrapper)
    expect(e.current.value).toBe(0)
    expect(e.target.value).toBe(0)
    expect(e.pending.value).toBeNull()

    await wrapper.setProps({ value: 10 })

    expect(e.current.value).toBe(0) // still at start
    expect(e.target.value).toBe(10) // animating toward the new value
    expect(e.pending.value).toBeNull()
  })

  it('buffers a second update into `pending` while the bar is animating', async () => {
    const wrapper = mountBar(0)
    const e = exposed(wrapper)

    await wrapper.setProps({ value: 10 })
    expect(e.target.value).toBe(10)
    expect(e.pending.value).toBeNull()

    await wrapper.setProps({ value: 20 })
    expect(e.target.value).toBe(10) // first animation continues uninterrupted
    expect(e.pending.value).toBe(20) // second update buffered
  })

  it('overwrites pending with the latest value when a third update arrives', async () => {
    const wrapper = mountBar(0)
    const e = exposed(wrapper)

    await wrapper.setProps({ value: 10 })
    await wrapper.setProps({ value: 20 })
    await wrapper.setProps({ value: 30 })

    // Still animating toward the first value; pending holds the latest of
    // the subsequent updates (30 wins, 20 was dropped).
    expect(e.target.value).toBe(10)
    expect(e.pending.value).toBe(30)
  })

  it('promotes pending to the next target on transitionend', async () => {
    const wrapper = mountBar(0)
    const e = exposed(wrapper)

    await wrapper.setProps({ value: 10 })
    await wrapper.setProps({ value: 20 })
    await wrapper.setProps({ value: 30 })

    // Finish the first leg — current should snap to 10 and a new leg should
    // start toward pending (30). Pending is cleared.
    e.onTransitionEnd()
    expect(e.current.value).toBe(10)
    expect(e.target.value).toBe(30)
    expect(e.pending.value).toBeNull()

    // Finish the second leg — idle.
    e.onTransitionEnd()
    expect(e.current.value).toBe(30)
    expect(e.target.value).toBe(30)
    expect(e.pending.value).toBeNull()
  })

  it('idles cleanly when transitionend fires with no pending update', async () => {
    const wrapper = mountBar(0)
    const e = exposed(wrapper)

    await wrapper.setProps({ value: 42 })
    expect(e.current.value).toBe(0)
    expect(e.target.value).toBe(42)

    e.onTransitionEnd()
    expect(e.current.value).toBe(42)
    expect(e.target.value).toBe(42)
    expect(e.pending.value).toBeNull()
  })

  it('coalesces a rapid burst into exactly two animation legs (spec §14 invariant)', async () => {
    const wrapper = mountBar(0)
    const e = exposed(wrapper)

    // Burst of four updates with no transitionend between them.
    await wrapper.setProps({ value: 10 })
    await wrapper.setProps({ value: 20 })
    await wrapper.setProps({ value: 30 })
    await wrapper.setProps({ value: 40 })

    // First leg animates to 10, pending holds the latest (40).
    expect(e.target.value).toBe(10)
    expect(e.pending.value).toBe(40)

    // End first leg → second leg jumps straight to 40, skipping 20 / 30.
    e.onTransitionEnd()
    expect(e.target.value).toBe(40)
    expect(e.pending.value).toBeNull()

    e.onTransitionEnd()
    expect(e.current.value).toBe(40)
  })
})

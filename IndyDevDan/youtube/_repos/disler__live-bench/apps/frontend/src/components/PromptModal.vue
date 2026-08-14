<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount } from 'vue'
import type { MetricDef, GroupDef } from '../schemas'

const props = defineProps<{
  chartId: string
  groupKey: string
  groupLabel: string
  metadata: Record<string, any> | null
  metrics: MetricDef[]
  latest: Map<string, number>
  groups: GroupDef[]
  allChartIds: string[]
}>()

const emit = defineEmits<{ close: [] }>()

const prompt = computed(() => props.metadata?.prompt ?? null)

const expectedAnswer = computed(() => {
  const ea = props.metadata?.expected_answer
  if (!ea || !Array.isArray(ea)) return null
  return ea as string[]
})

const modelAnswers = computed(() => {
  const ma = props.metadata?.model_answer
  if (!ma || typeof ma !== 'object') return null
  return ma as Record<string, string[]>
})

const f1Scores = computed(() => {
  const f1 = props.metadata?.f1
  if (!f1 || typeof f1 !== 'object') return null
  return f1 as Record<string, number>
})

const responses = computed(() => {
  const resp = props.metadata?.responses
  if (!resp || typeof resp !== 'object') return []

  return props.metrics
    .filter((m) => resp[m.key])
    .map((m) => {
      const group = props.groups.find((g) => g.key === props.groupKey)
      const color = Array.isArray(m.color) ? m.color[0] : m.color ?? '#888'

      // Look up metric values across all chart types (prefill, decode, wall)
      const values: { label: string; value: number | null }[] = props.allChartIds.map((cid) => {
        const key = `${cid}:${props.groupKey}:${m.key}`
        const v = props.latest.get(key)
        const chartLabel = cid.replace(/_m[45]$/, '')
        return { label: chartLabel, value: v ?? null }
      })

      return {
        metricKey: m.key,
        label: m.label,
        color,
        icon: group?.icon ?? null,
        text: resp[m.key] as string,
        values,
      }
    })
})

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))

function formatValue(v: number): string {
  if (Math.abs(v) >= 100) return Math.round(v).toString()
  if (Math.abs(v) >= 10) return v.toFixed(1)
  return v.toFixed(2)
}
</script>

<template>
  <Teleport to="body">
    <div class="modal-backdrop" @click.self="emit('close')">
      <div class="modal-card">
        <div class="modal-header">
          <h2 class="modal-header__title">{{ groupLabel }}</h2>
          <button class="modal-header__close" @click="emit('close')">&times;</button>
        </div>

        <div class="modal-body">
          <!-- Prompt -->
          <div v-if="prompt" class="modal-prompt">
            <div class="modal-prompt__label">Prompt</div>
            <div class="modal-prompt__text">{{ prompt }}</div>
          </div>
          <div v-else class="modal-prompt modal-prompt--empty">
            No metadata available yet.
          </div>

          <!-- Accuracy: expected vs model answers -->
          <div v-if="expectedAnswer" class="modal-accuracy">
            <div class="modal-accuracy__section">
              <div class="modal-accuracy__label">Expected Answer</div>
              <div class="modal-accuracy__nodes">{{ expectedAnswer.join(', ') }}</div>
            </div>
            <div v-if="modelAnswers" class="modal-accuracy__section">
              <div class="modal-accuracy__label">Model Answers</div>
              <div
                v-for="(nodes, metricKey) in modelAnswers"
                :key="metricKey"
                class="modal-accuracy__model"
              >
                <span
                  class="modal-accuracy__model-name"
                  :style="{ color: metrics.find(m => m.key === metricKey)?.color as string ?? '#888' }"
                >{{ metrics.find(m => m.key === metricKey)?.label ?? metricKey }}</span>
                <span class="modal-accuracy__model-nodes">{{ nodes.length ? nodes.join(', ') : '(empty)' }}</span>
                <span v-if="f1Scores?.[metricKey] != null" class="modal-accuracy__f1">
                  F1: {{ f1Scores[metricKey].toFixed(4) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Responses -->
          <div v-if="responses.length" class="modal-responses">
            <div class="modal-responses__label">Responses</div>
            <details
              v-for="r in responses"
              :key="r.metricKey"
              class="modal-response"
            >
              <summary class="modal-response__header">
                <img v-if="r.icon" :src="r.icon" class="modal-response__icon" />
                <span class="modal-response__name" :style="{ color: r.color }">{{ r.label }}</span>
                <span class="modal-response__metrics">
                  <span
                    v-for="v in r.values.filter((x) => x.value != null)"
                    :key="v.label"
                    class="modal-response__metric"
                  >
                    {{ v.label }}: {{ formatValue(v.value!) }}
                  </span>
                </span>
              </summary>
              <div class="modal-response__text">{{ r.text }}</div>
            </details>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

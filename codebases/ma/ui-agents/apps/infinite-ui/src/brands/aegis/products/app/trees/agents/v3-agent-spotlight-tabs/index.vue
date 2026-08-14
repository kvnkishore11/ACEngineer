<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/agents/v3-agent-spotlight-tabs
// Layout: sticky header · tablist (4 agent tabs) · hero spotlight panel ·
//         metrics row · deployment controls · activity log

// ── Types ──────────────────────────────────────────────────────────────
interface Agent {
  id: string
  name: string
  role: string
  icon: string
  status: 'active' | 'standby' | 'offline'
  active: boolean
  uptime: string
  neutralized: number
  lastAction: string
  lastActionAt: string
  sparkline: number[]
  responseTime: number
  falsePositiveRate: number
  coverage: number
  configEntries: { key: string; value: string }[]
}

interface ActivityEntry {
  id: number
  agentId: string
  type: 'detection' | 'response' | 'scan' | 'config'
  message: string
  at: string
}

// ── Agent data ─────────────────────────────────────────────────────────
const agents = ref<Agent[]>([
  {
    id: 'scanner', name: 'Scanner', role: 'Vulnerability scanning',
    icon: '⬡', status: 'active', active: true,
    uptime: '99.97%', neutralized: 142,
    lastAction: 'Flagged CVE-2024-4891 on api-gateway-01',
    lastActionAt: '2s ago',
    sparkline: [12, 18, 15, 22, 31, 28, 45, 38, 52, 47, 61, 55, 48, 63, 71, 58, 44, 67, 72, 69, 81, 76, 88, 83],
    responseTime: 187, falsePositiveRate: 0.02, coverage: 94,
    configEntries: [
      { key: 'Scan depth',      value: 'Deep'        },
      { key: 'Interval',        value: '60s'         },
      { key: 'CVE feed',        value: 'NVD + MITRE' },
      { key: 'Alert threshold', value: 'HIGH'        },
    ],
  },
  {
    id: 'monitor', name: 'Monitor', role: 'Traffic analysis',
    icon: '◈', status: 'active', active: true,
    uptime: '99.91%', neutralized: 87,
    lastAction: 'Detected anomalous request pattern on llm-worker-07',
    lastActionAt: '14s ago',
    sparkline: [8, 12, 19, 14, 23, 28, 33, 41, 36, 44, 38, 51, 47, 55, 49, 62, 57, 64, 71, 68, 74, 78, 72, 81],
    responseTime: 203, falsePositiveRate: 0.035, coverage: 88,
    configEntries: [
      { key: 'Sampling rate',   value: '100%'       },
      { key: 'Baseline window', value: '7d'         },
      { key: 'Sensitivity',     value: 'High'       },
      { key: 'Protocol',        value: 'HTTP/gRPC'  },
    ],
  },
  {
    id: 'responder', name: 'Responder', role: 'Threat containment',
    icon: '◉', status: 'active', active: true,
    uptime: '99.85%', neutralized: 203,
    lastAction: 'Isolated orchestrator-02 from network segment',
    lastActionAt: '34s ago',
    sparkline: [22, 31, 28, 41, 38, 52, 47, 61, 55, 48, 63, 71, 58, 44, 67, 72, 69, 81, 76, 88, 83, 91, 86, 94],
    responseTime: 142, falsePositiveRate: 0.018, coverage: 97,
    configEntries: [
      { key: 'Isolation mode',  value: 'Network + Process' },
      { key: 'Auto-escalate',   value: 'CRITICAL'          },
      { key: 'Rollback timer',  value: '15m'               },
      { key: 'Notify',          value: 'All channels'      },
    ],
  },
  {
    id: 'sentinel', name: 'Sentinel', role: 'Perimeter watch',
    icon: '◇', status: 'standby', active: false,
    uptime: '98.40%', neutralized: 56,
    lastAction: 'Completed perimeter sweep — no anomalies',
    lastActionAt: '4m ago',
    sparkline: [5, 8, 6, 9, 7, 11, 8, 14, 10, 12, 9, 16, 13, 11, 15, 12, 18, 14, 17, 13, 19, 16, 21, 18],
    responseTime: 312, falsePositiveRate: 0.041, coverage: 82,
    configEntries: [
      { key: 'Sweep interval',  value: '5m'         },
      { key: 'Perimeter scope', value: 'All zones'  },
      { key: 'Alert on',        value: 'Unknown IPs'},
      { key: 'Mode',            value: 'Passive'    },
    ],
  },
])

// ── Activity log ───────────────────────────────────────────────────────
const activityLog: ActivityEntry[] = [
  { id: 1,  agentId: 'scanner',   type: 'detection', message: 'CVE-2024-4891 flagged on api-gateway-01 — CRITICAL (9.8)',                   at: '2s ago'   },
  { id: 2,  agentId: 'monitor',   type: 'detection', message: 'Anomalous request pattern on llm-worker-07 — 4× baseline rate',              at: '14s ago'  },
  { id: 3,  agentId: 'responder', type: 'response',  message: 'Isolated orchestrator-02 from network segment — circuit breaker active',     at: '34s ago'  },
  { id: 4,  agentId: 'scanner',   type: 'scan',      message: 'Deep scan completed on api-gateway cluster — 3 new fingerprints logged',     at: '1m ago'   },
  { id: 5,  agentId: 'monitor',   type: 'detection', message: 'Token privilege escalation probe on auth-service — blocked at ingress',      at: '2m ago'   },
  { id: 6,  agentId: 'sentinel',  type: 'scan',      message: 'Perimeter sweep completed — no anomalies detected across 12 endpoints',      at: '4m ago'   },
  { id: 7,  agentId: 'responder', type: 'response',  message: 'Containment boundary restored for llm-worker-07 — traffic rerouted',         at: '6m ago'   },
  { id: 8,  agentId: 'scanner',   type: 'detection', message: 'CVE-2024-4887 flagged on llm-worker-02 — HIGH severity (8.9)',               at: '8m ago'   },
  { id: 9,  agentId: 'monitor',   type: 'scan',      message: 'Baseline recalibrated for api-gateway cluster — 847 requests sampled',       at: '12m ago'  },
  { id: 10, agentId: 'responder', type: 'config',    message: 'Containment threshold updated: trigger reduced to 2 anomaly events',         at: '18m ago'  },
  { id: 11, agentId: 'sentinel',  type: 'config',    message: 'Sweep interval adjusted to 4m from 6m — high-threat window active',         at: '21m ago'  },
  { id: 12, agentId: 'scanner',   type: 'scan',      message: 'Vulnerability scan complete — fine-tune cluster clear',                      at: '29m ago'  },
  { id: 13, agentId: 'monitor',   type: 'detection', message: 'Unusual embedding query pattern on vector-store-01 — monitoring elevated',   at: '34m ago'  },
  { id: 14, agentId: 'responder', type: 'response',  message: 'Patch deployment for CVE-2024-2208 verified — memory-store-01 secured',      at: '42m ago'  },
  { id: 15, agentId: 'scanner',   type: 'config',    message: 'Signature database updated — 847 new patterns ingested',                     at: '1h ago'   },
]

// ── Selected tab state ─────────────────────────────────────────────────
const selectedId = ref('scanner')

const selectedAgent = computed(() => agents.value.find(a => a.id === selectedId.value)!)

function selectAgent(id: string) {
  selectedId.value = id
}

// ── Tab keyboard navigation (WCAG 2.1 AA — roving tabindex, Arrow/Home/End)
function handleTabKeydown(event: KeyboardEvent, currentId: string) {
  const ids = agents.value.map(a => a.id)
  const idx = ids.indexOf(currentId)
  let targetIdx: number | null = null

  if (event.key === 'ArrowRight') {
    event.preventDefault()
    targetIdx = (idx + 1) % ids.length
  } else if (event.key === 'ArrowLeft') {
    event.preventDefault()
    targetIdx = (idx - 1 + ids.length) % ids.length
  } else if (event.key === 'Home') {
    event.preventDefault()
    targetIdx = 0
  } else if (event.key === 'End') {
    event.preventDefault()
    targetIdx = ids.length - 1
  }

  if (targetIdx !== null) {
    selectAgent(ids[targetIdx])
    nextTick(() => {
      const el = document.getElementById(`tab-${ids[targetIdx as number]}`)
      el?.focus()
    })
  }
}

// ── Deployment toggle ──────────────────────────────────────────────────
function toggleAgent(agent: Agent) {
  agent.active = !agent.active
  agent.status = agent.active ? 'active' : 'standby'
}

// ── Activity filter ────────────────────────────────────────────────────
const activityFilters = [
  { value: 'all',       label: 'All'       },
  { value: 'detection', label: 'Detection' },
  { value: 'response',  label: 'Response'  },
  { value: 'scan',      label: 'Scan'      },
  { value: 'config',    label: 'Config'    },
]

const activeFilter = ref('all')

function setFilter(value: string) {
  activeFilter.value = value
}

const filteredLog = computed(() =>
  activeFilter.value === 'all'
    ? activityLog
    : activityLog.filter(e => e.type === activeFilter.value)
)

// ── Helpers ────────────────────────────────────────────────────────────
function agentName(id: string): string {
  return agents.value.find(a => a.id === id)?.name ?? id
}

function sparklinePath(values: number[]): string {
  const max = Math.max(...values)
  const min = Math.min(...values)
  const range = max - min || 1
  return values.map((v, i) => {
    const x = (i / (values.length - 1)) * 120
    const y = 40 - ((v - min) / range) * 36 + 2
    return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`
  }).join(' ')
}

function sparklineAreaPath(values: number[]): string {
  return `${sparklinePath(values)} L120,42 L0,42 Z`
}

function fprLabel(rate: number): string {
  return (rate * 100).toFixed(1) + '%'
}

// ── Computed stats ─────────────────────────────────────────────────────
const activeCount  = computed(() => agents.value.filter(a => a.status === 'active').length)
const standbyCount = computed(() => agents.value.filter(a => a.status === 'standby').length)
const maxResponseTime = computed(() => Math.max(...agents.value.map(a => a.responseTime)))

// ── Live clock ─────────────────────────────────────────────────────────
const liveTime = ref('')
let clockInterval: ReturnType<typeof setInterval> | null = null

function updateClock() {
  const now = new Date()
  liveTime.value = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

// ── Mount ──────────────────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  updateClock()
  clockInterval = setInterval(updateClock, 1000)
  // nextTick is mandatory — ensures opacity:0 is painted before transition fires
  nextTick(() => { isMounted.value = true })
})

onUnmounted(() => {
  if (clockInterval !== null) {
    clearInterval(clockInterval)
    clockInterval = null
  }
})
</script>

<template>
  <div class="page" :class="{ 'is-mounted': isMounted }">
    <h1 class="sr-only">Aegis Agent Management</h1>

    <!-- ── Page header ─────────────────────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Agent management page header">
      <div class="page-header__inner">
        <div class="page-header__brand">
          <span class="brand-word">AEGIS</span>
          <span class="brand-sep" aria-hidden="true">/</span>
          <span class="brand-sub">Agent Command</span>
        </div>

        <div class="page-header__stats" aria-label="Agent status summary">
          <span class="hdr-stat">
            <span class="hdr-stat__dot hdr-stat__dot--active" aria-hidden="true"></span>
            <span class="hdr-stat__val">{{ activeCount }}</span>
            <span class="hdr-stat__lbl">Active</span>
          </span>
          <span class="hdr-sep" aria-hidden="true"></span>
          <span class="hdr-stat">
            <span class="hdr-stat__dot hdr-stat__dot--standby" aria-hidden="true"></span>
            <span class="hdr-stat__val">{{ standbyCount }}</span>
            <span class="hdr-stat__lbl">Standby</span>
          </span>
        </div>

        <div class="page-header__time" aria-label="Current time">
          <span class="hdr-time">{{ liveTime }}</span>
        </div>
      </div>
    </header>

    <!-- ── Body ────────────────────────────────────────────────────────── -->
    <main class="page-body">
      <div class="body-inner">

        <!-- ── Tab + Spotlight ─────────────────────────────────────────── -->
        <section class="spotlight-section" aria-label="Agent spotlight">

          <!-- ARIA tablist — roving tabindex, Arrow/Home/End navigation -->
          <div
            role="tablist"
            aria-label="Select agent"
            class="agent-tabs"
          >
            <button
              v-for="agent in agents"
              :key="agent.id"
              type="button"
              role="tab"
              :id="`tab-${agent.id}`"
              :aria-selected="selectedId === agent.id"
              :aria-controls="`panel-${agent.id}`"
              :tabindex="selectedId === agent.id ? 0 : -1"
              class="agent-tab"
              :class="[
                `agent-tab--${agent.status}`,
                { 'agent-tab--selected': selectedId === agent.id }
              ]"
              @click="selectAgent(agent.id)"
              @keydown="handleTabKeydown($event, agent.id)"
            >
              <span class="agent-tab__dot" :class="`agent-tab__dot--${agent.status}`" aria-hidden="true"></span>
              <span class="agent-tab__name">{{ agent.name }}</span>
              <span class="agent-tab__role">{{ agent.role }}</span>
            </button>
          </div>

          <!-- Tabpanels — v-show (NOT v-if) so DOM + aria refs stay intact -->
          <div
            v-for="agent in agents"
            :key="agent.id"
            role="tabpanel"
            :id="`panel-${agent.id}`"
            :aria-labelledby="`tab-${agent.id}`"
            tabindex="0"
            class="spotlight-panel"
            :class="[
              `spotlight-panel--${agent.status}`,
              { 'spotlight--active': agent.status === 'active' }
            ]"
            v-show="selectedId === agent.id"
          >
            <!-- Panel top: icon + identity + status + toggle -->
            <div class="spotlight-hero">
              <div class="spotlight-hero__left">
                <span class="spotlight-icon" :class="`spotlight-icon--${agent.status}`" aria-hidden="true">
                  {{ agent.icon }}
                </span>
              </div>

              <div class="spotlight-hero__main">
                <div class="spotlight-identity">
                  <div class="spotlight-identity__top">
                    <h2 class="spotlight-name" :class="`spotlight-name--${agent.status}`">{{ agent.name }}</h2>
                    <span
                      class="spotlight-status-dot"
                      :class="`spotlight-status-dot--${agent.status}`"
                      aria-hidden="true"
                    ></span>
                    <span
                      class="spotlight-badge"
                      :class="`spotlight-badge--${agent.status}`"
                      :aria-label="`Status: ${agent.status}`"
                    >{{ agent.status.toUpperCase() }}</span>
                  </div>
                  <p class="spotlight-role">{{ agent.role }}</p>
                </div>

                <!-- Deployment toggle -->
                <button
                  type="button"
                  class="deploy-toggle"
                  role="switch"
                  :aria-checked="agent.active"
                  :aria-label="`${agent.active ? 'Deactivate' : 'Activate'} ${agent.name} agent`"
                  @click="toggleAgent(agent)"
                >
                  <span class="deploy-toggle__track" aria-hidden="true">
                    <span class="deploy-toggle__thumb"></span>
                  </span>
                  <span class="deploy-toggle__label">
                    {{ agent.active ? 'Active' : 'Standby' }}
                  </span>
                </button>
              </div>
            </div>

            <!-- Stats row: uptime · neutralized · last action · last action time -->
            <div class="spotlight-stats" aria-label="Agent statistics">
              <div class="spotlight-stat">
                <span class="spotlight-stat__val">{{ agent.uptime }}</span>
                <span class="spotlight-stat__lbl">Uptime</span>
              </div>
              <div class="spotlight-stat-divider" aria-hidden="true"></div>
              <div class="spotlight-stat">
                <span class="spotlight-stat__val spotlight-stat__val--threats">{{ agent.neutralized }}</span>
                <span class="spotlight-stat__lbl">Neutralized</span>
              </div>
              <div class="spotlight-stat-divider" aria-hidden="true"></div>
              <div class="spotlight-stat spotlight-stat--last-action">
                <span class="spotlight-stat__val spotlight-stat__val--action">{{ agent.lastAction }}</span>
                <span class="spotlight-stat__lbl">Last action · {{ agent.lastActionAt }}</span>
              </div>
            </div>

            <!-- Sparkline + config entries -->
            <div class="spotlight-lower">
              <!-- Sparkline: 24h activity -->
              <div class="spotlight-sparkline-wrap">
                <span class="spotlight-sparkline-label">24h activity</span>
                <svg
                  class="spotlight-sparkline"
                  viewBox="0 0 120 44"
                  aria-hidden="true"
                  preserveAspectRatio="none"
                >
                  <defs>
                    <linearGradient :id="`spark-area-${agent.id}`" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%"   :stop-color="`var(--brand-${agent.status === 'active' ? 'primary' : agent.status === 'standby' ? 'secondary' : 'error'})`" stop-opacity="0.25" />
                      <stop offset="100%" :stop-color="`var(--brand-${agent.status === 'active' ? 'primary' : agent.status === 'standby' ? 'secondary' : 'error'})`" stop-opacity="0" />
                    </linearGradient>
                  </defs>
                  <path
                    class="sparkline-area"
                    :d="sparklineAreaPath(agent.sparkline)"
                    :fill="`url(#spark-area-${agent.id})`"
                  />
                  <path
                    class="sparkline-line"
                    :class="`sparkline-line--${agent.status}`"
                    :d="sparklinePath(agent.sparkline)"
                    fill="none"
                    stroke-width="1.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>

              <!-- Config summary -->
              <div class="spotlight-config" aria-label="Agent configuration summary">
                <h3 class="spotlight-config__heading">Configuration</h3>
                <dl class="spotlight-config__list">
                  <div
                    v-for="entry in agent.configEntries"
                    :key="entry.key"
                    class="config-entry"
                  >
                    <dt class="config-entry__key">{{ entry.key }}</dt>
                    <dd class="config-entry__val">{{ entry.value }}</dd>
                  </div>
                </dl>
              </div>
            </div>

          </div><!-- /spotlight-panel -->
        </section>

        <!-- ── Performance Metrics ──────────────────────────────────────── -->
        <section class="metrics-section card" aria-labelledby="metrics-heading">
          <div class="card__header">
            <h2 class="card__title" id="metrics-heading">Performance Metrics</h2>
          </div>
          <div class="metrics-grid">

            <!-- Response times -->
            <div class="metric-group" role="region" aria-labelledby="metric-response-heading">
              <h3 class="metric-group__heading" id="metric-response-heading">Response Time</h3>
              <ul class="metric-bars" role="list" aria-label="Response times per agent">
                <li
                  v-for="agent in agents"
                  :key="agent.id"
                  class="metric-bar-row"
                  :class="{ 'metric-bar-row--dimmed': agent.status === 'offline' }"
                  :aria-label="`${agent.name}: ${agent.responseTime}ms response time`"
                >
                  <span class="metric-bar-row__name">{{ agent.name }}</span>
                  <div class="metric-bar-track">
                    <div
                      class="metric-bar-fill"
                      :class="`metric-bar-fill--${agent.status}`"
                      :style="{ width: `${(agent.responseTime / maxResponseTime) * 100}%` }"
                      aria-hidden="true"
                    ></div>
                  </div>
                  <span class="metric-bar-row__val">{{ agent.responseTime }}ms</span>
                </li>
              </ul>
            </div>

            <!-- False positive rates -->
            <div class="metric-group" role="region" aria-labelledby="metric-fpr-heading">
              <h3 class="metric-group__heading" id="metric-fpr-heading">False Positive Rate</h3>
              <ul class="metric-list" role="list" aria-label="False positive rates per agent">
                <li
                  v-for="agent in agents"
                  :key="agent.id"
                  class="metric-item"
                  :class="{ 'metric-item--dimmed': agent.status === 'offline' }"
                  :aria-label="`${agent.name}: ${fprLabel(agent.falsePositiveRate)} false positive rate`"
                >
                  <span class="metric-item__name">{{ agent.name }}</span>
                  <span
                    class="metric-item__val"
                    :class="agent.falsePositiveRate < 0.02 ? 'val--good' : agent.falsePositiveRate <= 0.04 ? 'val--mid' : 'val--high'"
                  >{{ fprLabel(agent.falsePositiveRate) }}</span>
                </li>
              </ul>
            </div>

            <!-- Coverage -->
            <div class="metric-group" role="region" aria-labelledby="metric-coverage-heading">
              <h3 class="metric-group__heading" id="metric-coverage-heading">Coverage</h3>
              <ul class="metric-bars" role="list" aria-label="Coverage per agent">
                <li
                  v-for="agent in agents"
                  :key="agent.id"
                  class="metric-bar-row"
                  :class="{ 'metric-bar-row--dimmed': agent.status === 'offline' }"
                  :aria-label="`${agent.name}: ${agent.coverage}% coverage`"
                >
                  <span class="metric-bar-row__name">{{ agent.name }}</span>
                  <div class="metric-bar-track">
                    <div
                      class="metric-bar-fill"
                      :class="`metric-bar-fill--${agent.status}`"
                      :style="{ width: `${agent.coverage}%` }"
                      aria-hidden="true"
                    ></div>
                  </div>
                  <span class="metric-bar-row__val">{{ agent.coverage }}%</span>
                </li>
              </ul>
            </div>

          </div><!-- /metrics-grid -->
        </section>

        <!-- ── Deployment Controls ─────────────────────────────────────── -->
        <section class="deploy-section card" aria-labelledby="deploy-heading">
          <div class="card__header">
            <h2 class="card__title" id="deploy-heading">Deployment Controls</h2>
            <span class="card__meta">{{ activeCount }}/{{ agents.length }} active</span>
          </div>
          <ul class="deploy-list" role="list" aria-label="Agent deployment controls">
            <li
              v-for="agent in agents"
              :key="agent.id"
              class="deploy-row"
              :class="`deploy-row--${agent.status}`"
            >
              <div class="deploy-row__identity">
                <span class="deploy-dot" :class="`deploy-dot--${agent.status}`" aria-hidden="true"></span>
                <div class="deploy-row__info">
                  <span class="deploy-row__name">{{ agent.name }}</span>
                  <span class="deploy-row__role">{{ agent.role }}</span>
                </div>
              </div>

              <div class="deploy-row__stats">
                <span class="deploy-row__uptime">{{ agent.uptime }} uptime</span>
              </div>

              <button
                type="button"
                class="deploy-toggle deploy-toggle--inline"
                role="switch"
                :aria-checked="agent.active"
                :aria-label="`${agent.active ? 'Deactivate' : 'Activate'} ${agent.name} agent`"
                @click="toggleAgent(agent)"
              >
                <span class="deploy-toggle__track" aria-hidden="true">
                  <span class="deploy-toggle__thumb"></span>
                </span>
                <span class="deploy-toggle__label">{{ agent.active ? 'Active' : 'Standby' }}</span>
              </button>
            </li>
          </ul>
        </section>

        <!-- ── Activity Log ────────────────────────────────────────────── -->
        <section class="activity-section card" aria-labelledby="activity-heading">
          <div class="card__header">
            <h2 class="card__title" id="activity-heading">Activity Log</h2>
            <span class="card__meta">{{ filteredLog.length }} entries</span>
          </div>

          <!-- Filter chips -->
          <div class="activity-filters" role="group" aria-label="Filter activity by type">
            <button
              v-for="filter in activityFilters"
              :key="filter.value"
              type="button"
              class="filter-chip"
              :class="{ 'filter-chip--active': activeFilter === filter.value }"
              :aria-pressed="activeFilter === filter.value"
              @click="setFilter(filter.value)"
            >
              {{ filter.label }}
            </button>
          </div>

          <!-- Log entries — stagger via CSS custom property -->
          <ul class="log-list" role="list" aria-label="Agent activity entries">
            <li
              v-for="(entry, index) in filteredLog"
              :key="entry.id"
              class="log-entry"
              :class="`log-entry--${entry.type}`"
              :style="{ '--log-delay': `${index * 30}ms` }"
              :aria-label="`${agentName(entry.agentId)}: ${entry.message}, ${entry.at}`"
            >
              <span class="log-dot" :class="`log-dot--${entry.type}`" aria-hidden="true"></span>
              <div class="log-body">
                <span class="log-agent">{{ agentName(entry.agentId) }}</span>
                <span class="log-type-badge" :class="`log-type-badge--${entry.type}`">{{ entry.type }}</span>
                <span class="log-message">{{ entry.message }}</span>
              </div>
              <span class="log-time">{{ entry.at }}</span>
            </li>
          </ul>
        </section>

      </div><!-- /body-inner -->
    </main>
  </div>
</template>

<style scoped>
/* ── Reset ────────────────────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* ── Visually hidden ──────────────────────────────────────────────────── */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* ── Page root — mount fade ────────────────────────────────────────────── */
.page {
  min-height: 100vh;
  background-color: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  display: flex;
  flex-direction: column;
  opacity: 0;
  overflow-x: hidden;
  transition: opacity var(--duration-normal) var(--easing);
}

.page.is-mounted {
  opacity: 1;
}

/* ── Page header ─────────────────────────────────────────────────────── */
.page-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
  box-shadow: var(--shadow-md);
}

.page-header__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 calc(var(--space-unit) * 6);
  height: calc(var(--space-unit) * 16);
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 6);
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .page-header__inner {
    height: auto;
    padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
    gap: calc(var(--space-unit) * 3);
  }
}

.page-header__brand {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 2);
  flex-shrink: 0;
}

.brand-word {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
}

.brand-sep {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  color: var(--brand-muted);
}

.brand-sub {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--brand-text);
}

.page-header__stats {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
}

.hdr-stat {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
}

.hdr-stat__dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  flex-shrink: 0;
}
.hdr-stat__dot--active  { background-color: var(--brand-primary);   }
.hdr-stat__dot--standby { background-color: var(--brand-secondary); }

.hdr-stat__val {
  font-family: var(--font-mono);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
}

.hdr-stat__lbl {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.hdr-sep {
  width: 1px;
  height: calc(var(--space-unit) * 4);
  background-color: var(--brand-border);
  flex-shrink: 0;
}

.page-header__time {
  margin-left: auto;
}

.hdr-time {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-muted);
  letter-spacing: 0.05em;
}

/* ── Body ────────────────────────────────────────────────────────────── */
.page-body {
  flex: 1;
}

.body-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 6);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
}

@media (max-width: 768px) {
  .body-inner {
    padding: calc(var(--space-unit) * 4);
    gap: calc(var(--space-unit) * 5);
  }
}

/* ── Card base ───────────────────────────────────────────────────────── */
.card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
}

.card__title {
  font-family: var(--font-heading);
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--brand-text);
  margin: 0;
}

.card__meta {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

/* ════════════════════════════════════════════════════════════════════════
   SPOTLIGHT + TABS SECTION
   ════════════════════════════════════════════════════════════════════════ */
.spotlight-section {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

/* ── Tablist ─────────────────────────────────────────────────────────── */
.agent-tabs {
  display: flex;
  gap: 0;
  background: linear-gradient(180deg, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 95%, var(--brand-primary)));
  border-bottom: 1px solid var(--brand-border);
  overflow-x: auto;
}

.agent-tab {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 0.75);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  text-align: left;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  transition:
    color var(--duration-fast) var(--easing),
    border-color var(--duration-fast) var(--easing),
    background-color var(--duration-fast) var(--easing);
  flex-shrink: 0;
  margin-bottom: -1px;
  min-width: calc(var(--space-unit) * 28);
}

.agent-tab:hover:not(.agent-tab--selected) {
  color: var(--brand-text);
  background-color: color-mix(in srgb, var(--brand-surface) 40%, transparent);
}

.agent-tab:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

.agent-tab--selected {
  color: var(--brand-primary);
  border-bottom-color: var(--brand-primary);
  background-color: color-mix(in srgb, var(--brand-primary) 5%, transparent);
}

/* Tab dot indicators */
.agent-tab__dot {
  width: calc(var(--space-unit) * 1.5);
  height: calc(var(--space-unit) * 1.5);
  border-radius: 50%;
  flex-shrink: 0;
  align-self: flex-start;
  margin-top: calc(var(--space-unit) * 0.5);
}

.agent-tab__dot--active  { background-color: var(--brand-primary);   }
.agent-tab__dot--standby { background-color: var(--brand-secondary); }
.agent-tab__dot--offline { background-color: var(--brand-error);     }

.agent-tab__name {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  line-height: 1;
}

.agent-tab__role {
  font-family: var(--font-body);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  white-space: nowrap;
}

/* ── Spotlight panel ─────────────────────────────────────────────────── */
.spotlight-panel {
  padding: calc(var(--space-unit) * 10) calc(var(--space-unit) * 8);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
  border-radius: 0;
  background: linear-gradient(145deg, var(--brand-surface), color-mix(in srgb, var(--brand-surface) 85%, var(--brand-bg)));
  transition:
    box-shadow var(--duration-slow) var(--easing),
    border-color var(--duration-slow) var(--easing);
  outline: none;
}

.spotlight-panel:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -4px;
}

/* Active agent panel — glow-pulse animation */
.spotlight--active {
  animation: glow-pulse 3s var(--easing) infinite;
}

/* Offline panel — dimmed border only, no card opacity */
.spotlight-panel--offline {
  border-top: 1px solid color-mix(in srgb, var(--brand-error) 25%, transparent);
}

@media (max-width: 768px) {
  .spotlight-panel {
    padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 4);
  }
}

/* ── Spotlight hero row (icon + identity + toggle) ───────────────────── */
.spotlight-hero {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 6);
}

.spotlight-hero__left {
  flex-shrink: 0;
}

/* Large status icon */
.spotlight-icon {
  font-size: 2.5rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(var(--space-unit) * 18);
  height: calc(var(--space-unit) * 18);
  border-radius: var(--radius-md);
  border: 1px solid var(--brand-border);
  background-color: var(--brand-bg-secondary);
  transition:
    color var(--duration-normal) var(--easing),
    border-color var(--duration-normal) var(--easing);
}

.spotlight-icon--active  { color: var(--brand-primary);   border-color: color-mix(in srgb, var(--brand-primary) 35%, transparent); }
.spotlight-icon--standby { color: var(--brand-secondary); border-color: color-mix(in srgb, var(--brand-secondary) 35%, transparent); }
.spotlight-icon--offline { color: color-mix(in srgb, var(--brand-error) 60%, transparent); }

.spotlight-hero__main {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 4);
  flex-wrap: wrap;
}

.spotlight-identity {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.spotlight-identity__top {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  flex-wrap: wrap;
}

.spotlight-name {
  font-family: var(--font-heading);
  font-size: 2.75rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  margin: 0;
  transition: color var(--duration-normal) var(--easing);
}

.spotlight-name--active  { color: var(--brand-primary);   }
.spotlight-name--standby { color: var(--brand-secondary); }
.spotlight-name--offline { color: color-mix(in srgb, var(--brand-text) 50%, transparent); }

/* Active status dot — dot-pulse animation */
.spotlight-status-dot {
  width: calc(var(--space-unit) * 3);
  height: calc(var(--space-unit) * 3);
  border-radius: 50%;
  flex-shrink: 0;
}

.spotlight-status-dot--active {
  background-color: var(--brand-primary);
  animation: dot-pulse 2s var(--easing) infinite;
}

.spotlight-status-dot--standby {
  background-color: var(--brand-secondary);
}

.spotlight-status-dot--offline {
  background-color: var(--brand-error);
}

.spotlight-badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
}

.spotlight-badge--active  { background-color: var(--brand-primary);   }
.spotlight-badge--standby { background-color: var(--brand-secondary); }
.spotlight-badge--offline { background-color: var(--brand-error);     }

.spotlight-role {
  font-family: var(--font-body);
  font-size: 1.0625rem;
  color: var(--brand-muted);
  margin: 0;
  line-height: 1.5;
}

/* ── Deployment toggle (hero) ─────────────────────────────────────────── */
.deploy-toggle {
  display: inline-flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  background: none;
  border: none;
  cursor: pointer;
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  border-radius: var(--radius-sm);
  color: var(--brand-text);
  font-family: var(--font-body);
  transition: background-color var(--duration-fast) var(--easing);
}

.deploy-toggle:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.deploy-toggle:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 50%, var(--brand-bg-secondary));
}

/* Toggle track */
.deploy-toggle__track {
  width: calc(var(--space-unit) * 10);
  height: calc(var(--space-unit) * 6);
  border-radius: calc(var(--space-unit) * 3);
  background-color: var(--brand-muted);
  position: relative;
  transition: background-color var(--duration-normal) var(--easing);
  flex-shrink: 0;
}

[aria-checked="true"] .deploy-toggle__track {
  background-color: color-mix(in srgb, var(--brand-primary) 30%, transparent);
  border: 1px solid var(--brand-primary);
}

/* Toggle thumb */
.deploy-toggle__thumb {
  position: absolute;
  top: calc(var(--space-unit) * 0.75);
  left: calc(var(--space-unit) * 0.75);
  width: calc(var(--space-unit) * 4.5);
  height: calc(var(--space-unit) * 4.5);
  border-radius: 50%;
  background-color: var(--brand-primary);
  transition: transform var(--duration-normal) var(--easing);
}

[aria-checked="true"] .deploy-toggle__thumb {
  transform: translateX(calc(var(--space-unit) * 4));
}

/* Toggle label */
.deploy-toggle__label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
  transition: color var(--duration-normal) var(--easing);
}

[aria-checked="true"] .deploy-toggle__label {
  color: var(--brand-primary);
}

/* ── Spotlight stats row ──────────────────────────────────────────────── */
.spotlight-stats {
  display: flex;
  align-items: stretch;
  gap: 0;
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--brand-border);
  overflow: hidden;
}

.spotlight-stat {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.75);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  flex-shrink: 0;
}

.spotlight-stat--last-action {
  flex: 1;
  min-width: 0;
}

.spotlight-stat-divider {
  width: 1px;
  background-color: var(--brand-border);
  flex-shrink: 0;
}

.spotlight-stat__val {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--brand-primary);
  line-height: 1;
}

.spotlight-stat__val--threats {
  color: var(--brand-accent);
}

.spotlight-stat__val--action {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.spotlight-stat__lbl {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

@media (max-width: 768px) {
  .spotlight-stats {
    flex-direction: column;
  }
  .spotlight-stat-divider {
    width: auto;
    height: 1px;
  }
}

/* ── Spotlight lower (sparkline + config) ────────────────────────────── */
.spotlight-lower {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 6);
}

@media (max-width: 768px) {
  .spotlight-lower {
    grid-template-columns: 1fr;
  }
}

/* Sparkline */
.spotlight-sparkline-wrap {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.spotlight-sparkline-label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.spotlight-sparkline {
  width: 100%;
  height: calc(var(--space-unit) * 14);
}

/* Sparkline fill */
.sparkline-area {
  opacity: 0.3;
}

/* Sparkline stroke by status */
.sparkline-line--active  { stroke: var(--brand-primary);   }
.sparkline-line--standby { stroke: var(--brand-secondary); }
.sparkline-line--offline { stroke: color-mix(in srgb, var(--brand-error) 60%, transparent); }

/* Config summary */
.spotlight-config {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.spotlight-config__heading {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin: 0;
}

.spotlight-config__list {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
  margin: 0;
}

.config-entry {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 2) 0;
  border-bottom: 1px solid var(--brand-border);
}

.config-entry:last-child {
  border-bottom: none;
}

.config-entry__key {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: var(--brand-muted);
}

.config-entry__val {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
  text-align: right;
}

/* ════════════════════════════════════════════════════════════════════════
   PERFORMANCE METRICS SECTION
   ════════════════════════════════════════════════════════════════════════ */
.metrics-grid {
  padding: calc(var(--space-unit) * 6);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: calc(var(--space-unit) * 8);
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
    padding: calc(var(--space-unit) * 4);
    gap: calc(var(--space-unit) * 6);
  }
}

.metric-group {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 4);
}

.metric-group__heading {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin: 0;
  padding-bottom: calc(var(--space-unit) * 2);
  border-bottom: 1px solid var(--brand-border);
}

/* Bar rows */
.metric-bars {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.metric-bar-row {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 18) 1fr calc(var(--space-unit) * 14);
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  transition: opacity var(--duration-normal) var(--easing);
}

.metric-bar-row--dimmed {
  opacity: 0.45;
}

.metric-bar-row__name {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: var(--brand-muted);
  white-space: nowrap;
}

.metric-bar-track {
  height: calc(var(--space-unit) * 1.5);
  background-color: color-mix(in srgb, var(--brand-border) 80%, transparent);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.metric-bar-fill {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--duration-slow) var(--easing);
}

.metric-bar-fill--active  { background-color: var(--brand-primary);   }
.metric-bar-fill--standby { background-color: var(--brand-secondary); }
.metric-bar-fill--offline { background-color: color-mix(in srgb, var(--brand-error) 50%, transparent); }

.metric-bar-row__val {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
  text-align: right;
  white-space: nowrap;
}

/* List metric items (FPR) */
.metric-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.metric-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 1.5) 0;
  border-bottom: 1px solid var(--brand-border);
  transition: opacity var(--duration-normal) var(--easing);
}

.metric-item:last-child {
  border-bottom: none;
}

.metric-item--dimmed {
  opacity: 0.45;
}

.metric-item__name {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: var(--brand-muted);
}

.metric-item__val {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
}

.val--good { color: var(--brand-primary);   }
.val--mid  { color: var(--brand-secondary); }
.val--high { color: var(--brand-accent);    }

/* ════════════════════════════════════════════════════════════════════════
   DEPLOYMENT CONTROLS SECTION
   ════════════════════════════════════════════════════════════════════════ */
.deploy-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.deploy-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
  transition: background-color var(--duration-fast) var(--easing);
}

.deploy-row:last-child {
  border-bottom: none;
}

.deploy-row:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 60%, var(--brand-bg-secondary));
}

.deploy-row__identity {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.deploy-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.deploy-dot--active  { background-color: var(--brand-primary);   }
.deploy-dot--standby { background-color: var(--brand-secondary); }
.deploy-dot--offline { background-color: var(--brand-error);     }

.deploy-row__info {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.deploy-row__name {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
}

.deploy-row__role {
  font-family: var(--font-body);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

.deploy-row__stats {
  flex: 1;
  text-align: right;
}

.deploy-row__uptime {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
}

/* ── Inline deploy toggle (deploy-section rows) ───────────────────────── */
.deploy-toggle--inline {
  flex-shrink: 0;
}

/* ════════════════════════════════════════════════════════════════════════
   ACTIVITY LOG SECTION
   ════════════════════════════════════════════════════════════════════════ */
.activity-filters {
  display: flex;
  flex-wrap: wrap;
  gap: calc(var(--space-unit) * 2);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
}

.filter-chip {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 1.5) calc(var(--space-unit) * 3);
  border-radius: var(--radius-sm);
  border: 1px solid var(--brand-border);
  background-color: var(--brand-surface);
  color: var(--brand-text);
  cursor: pointer;
  transition:
    background-color var(--duration-fast) var(--easing),
    color var(--duration-fast) var(--easing),
    border-color var(--duration-fast) var(--easing);
}

.filter-chip:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.filter-chip:hover:not(.filter-chip--active) {
  background-color: color-mix(in srgb, var(--brand-surface) 70%, var(--brand-secondary));
  border-color: var(--brand-secondary);
}

.filter-chip--active {
  background-color: var(--brand-primary);
  color: var(--brand-bg);
  border-color: var(--brand-primary);
}

/* Log list */
.log-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

/* Log entry — animation uses CSS custom property stagger */
.log-entry {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 3) 1fr auto;
  align-items: start;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
  /* log-enter animation with per-entry stagger */
  animation: log-enter var(--duration-normal) var(--easing) both;
  animation-delay: var(--log-delay, 0ms);
  transition: background-color var(--duration-fast) var(--easing);
}

.log-entry:last-child {
  border-bottom: none;
}

.log-entry:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 60%, var(--brand-bg-secondary));
}

/* Log severity dot */
.log-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  margin-top: calc(var(--space-unit) * 1.25);
  flex-shrink: 0;
}

.log-dot--detection { background-color: var(--brand-error);     }
.log-dot--response  { background-color: var(--brand-accent);    }
.log-dot--scan      { background-color: var(--brand-secondary); }
.log-dot--config    { background-color: var(--brand-muted);     }

.log-body {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
  min-width: 0;
}

.log-agent {
  font-family: var(--font-heading);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
}

.log-type-badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.5) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
  align-self: flex-start;
}

.log-type-badge--detection { background-color: var(--brand-error);     }
.log-type-badge--response  { background-color: var(--brand-accent);    }
.log-type-badge--scan      { background-color: var(--brand-secondary); }
.log-type-badge--config    { background-color: var(--brand-muted);     }

.log-message {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: var(--brand-text);
  line-height: 1.5;
}

.log-time {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);
  white-space: nowrap;
  padding-top: calc(var(--space-unit) * 1.25);
  flex-shrink: 0;
}

/* ════════════════════════════════════════════════════════════════════════
   KEYFRAMES
   ════════════════════════════════════════════════════════════════════════ */

/* Glow breathe — active spotlight panel outer shadow pulses 8%↔15% */
@keyframes glow-pulse {
  0%, 100% {
    box-shadow:
      0 0 0 1px var(--brand-primary),
      0 0 16px color-mix(in srgb, var(--brand-primary) 20%, transparent),
      0 0 32px color-mix(in srgb, var(--brand-primary) 8%, transparent);
  }
  50% {
    box-shadow:
      0 0 0 1px var(--brand-primary),
      0 0 20px color-mix(in srgb, var(--brand-primary) 28%, transparent),
      0 0 40px color-mix(in srgb, var(--brand-primary) 15%, transparent);
  }
}

/* Active status dot pulse — gentle scale breath */
@keyframes dot-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(0.85);
  }
}

/* Log entry entrance — stagger via var(--log-delay) */
@keyframes log-enter {
  from {
    opacity: 0;
    transform: translateY(-6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ════════════════════════════════════════════════════════════════════════
   ACCESSIBILITY — reduced-motion guard (always last rule)
   ════════════════════════════════════════════════════════════════════════ */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
</style>

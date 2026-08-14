<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/agents/v3-agent-spotlight-tabs-radar-drilldown
// Fork of v3-agent-spotlight-tabs.
// Change: replace the tablist + tabpanels with an interactive pentagon radar chart
//         comparing all 4 agents across 5 dimensions, plus a click-to-drill-down
//         detail panel below the radar.
// Preserved verbatim: sticky header, metrics card, deployment controls, activity log.

// ── Types ──────────────────────────────────────────────────────────────────
interface RadarScores {
  throughput: number      // 0-100
  uptime: number          // 0-100
  responseTime: number    // 0-100 (inverted — lower ms = higher score)
  taskCompletion: number  // 0-100
  coverage: number        // 0-100 (direct from agent.coverage)
}

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
  radarScores: RadarScores
}

interface ActivityEntry {
  id: number
  agentId: string
  type: 'detection' | 'response' | 'scan' | 'config'
  message: string
  at: string
}

// ── Agent data ─────────────────────────────────────────────────────────────
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
    radarScores: { throughput: 82, uptime: 99, responseTime: 78, taskCompletion: 71, coverage: 94 },
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
      { key: 'Sampling rate',   value: '100%'      },
      { key: 'Baseline window', value: '7d'        },
      { key: 'Sensitivity',     value: 'High'      },
      { key: 'Protocol',        value: 'HTTP/gRPC' },
    ],
    radarScores: { throughput: 61, uptime: 98, responseTime: 72, taskCompletion: 65, coverage: 88 },
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
    radarScores: { throughput: 44, uptime: 97, responseTime: 88, taskCompletion: 95, coverage: 97 },
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
    radarScores: { throughput: 28, uptime: 90, responseTime: 55, taskCompletion: 48, coverage: 82 },
  },
])

// ── Activity log ───────────────────────────────────────────────────────────
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

// ── Radar selection state ──────────────────────────────────────────────────
const selectedId = ref<string | null>(null)
const isDrillOpen = ref(false)

const selectedAgent = computed(() =>
  agents.value.find(a => a.id === selectedId.value) ?? null
)

function selectRadarAgent(agentId: string) {
  if (selectedId.value === agentId) {
    // Toggle off — click same agent collapses panel
    selectedId.value = null
    isDrillOpen.value = false
  } else {
    selectedId.value = agentId
    isDrillOpen.value = true
  }
}

// Arrow-key nav on the radar container (NOT tablist pattern)
function handleRadarKeydown(event: KeyboardEvent) {
  const ids = agents.value.map(a => a.id)
  const currentIdx = selectedId.value ? ids.indexOf(selectedId.value) : -1
  let targetIdx: number | null = null

  if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
    event.preventDefault()
    targetIdx = (currentIdx + 1) % ids.length
  } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
    event.preventDefault()
    targetIdx = (currentIdx - 1 + ids.length) % ids.length
  } else if (event.key === 'Escape') {
    event.preventDefault()
    selectedId.value = null
    isDrillOpen.value = false
  }

  if (targetIdx !== null) {
    selectRadarAgent(ids[targetIdx])
  }
}

// ── Deployment toggle ──────────────────────────────────────────────────────
function toggleAgent(agent: Agent) {
  agent.active = !agent.active
  agent.status = agent.active ? 'active' : 'standby'
}

// ── Activity filter ────────────────────────────────────────────────────────
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

// ── Radar geometry ─────────────────────────────────────────────────────────
const RADAR_CX = 200
const RADAR_CY = 200
const RADAR_MAX_R = 160
const RADAR_AXES = 5
const RADAR_RINGS = 4

const radarAxes = [
  { key: 'throughput'     as keyof RadarScores, label: 'Throughput'      },
  { key: 'uptime'         as keyof RadarScores, label: 'Uptime'          },
  { key: 'responseTime'   as keyof RadarScores, label: 'Response Time'   },
  { key: 'taskCompletion' as keyof RadarScores, label: 'Task Completion' },
  { key: 'coverage'       as keyof RadarScores, label: 'Coverage'        },
] as const

function axisAngle(i: number): number {
  // Start at top (−π/2), go clockwise
  return (i / RADAR_AXES) * 2 * Math.PI - Math.PI / 2
}

function axisPoint(score: number, axisIndex: number): { x: number; y: number } {
  const angle = axisAngle(axisIndex)
  const r = (score / 100) * RADAR_MAX_R
  return {
    x: RADAR_CX + r * Math.cos(angle),
    y: RADAR_CY + r * Math.sin(angle),
  }
}

function ringPoint(axisIndex: number, ringFraction: number): { x: number; y: number } {
  const angle = axisAngle(axisIndex)
  const r = ringFraction * RADAR_MAX_R
  return { x: RADAR_CX + r * Math.cos(angle), y: RADAR_CY + r * Math.sin(angle) }
}

function ringPath(ringFraction: number): string {
  return Array.from({ length: RADAR_AXES }, (_, i) => {
    const pt = ringPoint(i, ringFraction)
    return `${i === 0 ? 'M' : 'L'}${pt.x.toFixed(1)},${pt.y.toFixed(1)}`
  }).join(' ') + ' Z'
}

function agentPolygonPath(agentId: string): string {
  const agent = agents.value.find(a => a.id === agentId)
  if (!agent) return ''
  return radarAxes.map((ax, i) => {
    const pt = axisPoint(agent.radarScores[ax.key], i)
    return `${i === 0 ? 'M' : 'L'}${pt.x.toFixed(1)},${pt.y.toFixed(1)}`
  }).join(' ') + ' Z'
}

function agentVertices(agentId: string): Array<{ x: number; y: number; axisLabel: string; score: number }> {
  const agent = agents.value.find(a => a.id === agentId)
  if (!agent) return []
  return radarAxes.map((ax, i) => {
    const score = agent.radarScores[ax.key]
    const pt = axisPoint(score, i)
    return { x: pt.x, y: pt.y, axisLabel: ax.label, score }
  })
}

function axisLabelPos(axisIndex: number): { x: number; y: number } {
  const angle = axisAngle(axisIndex)
  const r = RADAR_MAX_R + 28
  return { x: RADAR_CX + r * Math.cos(angle), y: RADAR_CY + r * Math.sin(angle) }
}

// ── Radar polygon entrance stagger delays ─────────────────────────────────
// Assigned semantically by agent role: sentinel (dimmest) draws first,
// then scanner, monitor, responder build up the full comparison.
const polygonDelay: Record<string, string> = {
  sentinel:  '0ms',
  scanner:   '80ms',
  monitor:   '160ms',
  responder: '240ms',
}

// ── Helpers ────────────────────────────────────────────────────────────────
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

// ── Computed stats ─────────────────────────────────────────────────────────
const activeCount      = computed(() => agents.value.filter(a => a.status === 'active').length)
const standbyCount     = computed(() => agents.value.filter(a => a.status === 'standby').length)
const maxResponseTime  = computed(() => Math.max(...agents.value.map(a => a.responseTime)))

// ── Live clock ─────────────────────────────────────────────────────────────
const liveTime = ref('')
let clockInterval: ReturnType<typeof setInterval> | null = null

function updateClock() {
  const now = new Date()
  liveTime.value = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

// ── Mount ──────────────────────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  updateClock()
  clockInterval = setInterval(updateClock, 1000)
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
    <h1 class="sr-only">Aegis Agent Management — Radar Comparison</h1>

    <!-- ── Page header ──────────────────────────────────────────────────── -->
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

    <!-- ── Body ─────────────────────────────────────────────────────────── -->
    <main class="page-body">
      <div class="body-inner">

        <!-- ── Radar + Drilldown spotlight section ───────────────────────── -->
        <section class="spotlight-section" aria-labelledby="radar-section-heading">
          <h2 id="radar-section-heading" class="sr-only">Agent Comparison Radar</h2>

          <!-- Radar area: header + SVG + legend -->
          <div
            class="radar-area"
            tabindex="0"
            role="group"
            aria-label="Agent performance radar — use arrow keys to select agents, Enter or click to drill down"
            @keydown="handleRadarKeydown"
          >
            <!-- Radar header -->
            <div class="radar-header">
              <span class="radar-title">Agent Performance Comparison</span>
              <span class="radar-subtitle">5 dimensions · 4 agents · click to drill down</span>
            </div>

            <!-- Radar + legend side by side on wide, stacked on narrow -->
            <div class="radar-body">

              <!-- SVG pentagon radar — aria-hidden; accessible text via legend + drilldown -->
              <svg
                class="radar-chart"
                viewBox="0 0 400 400"
                aria-hidden="true"
                preserveAspectRatio="xMidYMid meet"
              >
                <!-- Background rings (25 / 50 / 75 / 100 %) -->
                <path
                  v-for="ring in [0.25, 0.5, 0.75, 1.0]"
                  :key="ring"
                  :d="ringPath(ring)"
                  class="radar-ring"
                  fill="none"
                />

                <!-- Axis lines from centre to outer ring -->
                <line
                  v-for="(ax, i) in radarAxes"
                  :key="`axis-line-${ax.key}`"
                  :x1="RADAR_CX" :y1="RADAR_CY"
                  :x2="ringPoint(i, 1.0).x" :y2="ringPoint(i, 1.0).y"
                  class="radar-axis-line"
                />

                <!-- Axis labels (outside outer ring) -->
                <text
                  v-for="(ax, i) in radarAxes"
                  :key="`lbl-${ax.key}`"
                  :x="axisLabelPos(i).x"
                  :y="axisLabelPos(i).y"
                  class="radar-axis-label"
                  text-anchor="middle"
                  dominant-baseline="middle"
                >{{ ax.label }}</text>

                <!-- Ring percentage labels at top axis -->
                <text
                  v-for="ring in [0.25, 0.5, 0.75]"
                  :key="`ring-pct-${ring}`"
                  :x="RADAR_CX + 4"
                  :y="RADAR_CY - ring * RADAR_MAX_R + 4"
                  class="radar-ring-label"
                  text-anchor="start"
                  dominant-baseline="middle"
                >{{ Math.round(ring * 100) }}</text>

                <!-- Agent polygons — dimmer agents first (z-order: sentinel behind, then monitor, scanner, responder) -->
                <g v-for="agent in [...agents].reverse()" :key="`poly-group-${agent.id}`">
                  <!-- Filled polygon — radar-enter stagger via --polygon-delay CSS custom property -->
                  <path
                    :d="agentPolygonPath(agent.id)"
                    :class="[
                      'radar-polygon',
                      `radar-polygon--${agent.id}`,
                      { 'radar-polygon--selected': selectedId === agent.id },
                      { 'radar-polygon--dimmed': selectedId !== null && selectedId !== agent.id },
                    ]"
                    :style="{ '--polygon-delay': polygonDelay[agent.id] ?? '0ms' }"
                    @click="selectRadarAgent(agent.id)"
                  />
                  <!-- Invisible enlarged hit-target circles at each vertex -->
                  <!-- NOTE: tabindex/role/aria-label omitted — SVG is aria-hidden="true";
                       these are pointer-only hit enlargers. Keyboard + AT access via legend buttons. -->
                  <circle
                    v-for="(vertex, vi) in agentVertices(agent.id)"
                    :key="`node-${agent.id}-${vi}`"
                    :cx="vertex.x"
                    :cy="vertex.y"
                    r="10"
                    class="radar-node"
                    @click.stop="selectRadarAgent(agent.id)"
                  />
                </g>

                <!-- Visible vertex dots on selected agent (rendered last, on top) -->
                <g v-if="selectedId" aria-hidden="true">
                  <circle
                    v-for="(vertex, vi) in agentVertices(selectedId)"
                    :key="`sel-dot-${vi}`"
                    :cx="vertex.x"
                    :cy="vertex.y"
                    r="4"
                    :class="['radar-vertex-dot', `radar-vertex-dot--${selectedId}`]"
                  />
                </g>
              </svg>

              <!-- Agent legend — always visible, aria-pressed toggles for keyboard users -->
              <ul class="radar-legend" role="list" aria-label="Agents on radar — click to select">
                <li v-for="agent in agents" :key="`legend-${agent.id}`">
                  <button
                    type="button"
                    class="radar-legend-btn"
                    :class="{ 'radar-legend-btn--selected': selectedId === agent.id }"
                    :aria-pressed="selectedId === agent.id"
                    :aria-label="`${agent.name}, ${agent.role}. ${selectedId === agent.id ? 'Selected — click to close' : 'Click to view detail'}.`"
                    @click="selectRadarAgent(agent.id)"
                  >
                    <span class="radar-legend-dot" :class="`radar-legend-dot--${agent.id}`" aria-hidden="true"></span>
                    <div class="radar-legend-text">
                      <span class="radar-legend-name">{{ agent.name }}</span>
                      <span class="radar-legend-role">{{ agent.role }}</span>
                    </div>
                    <span
                      class="radar-legend-status-dot"
                      :class="`radar-legend-status-dot--${agent.status}`"
                      aria-hidden="true"
                    ></span>
                  </button>
                </li>
              </ul>
            </div>
          </div><!-- /radar-area -->

          <!-- ── Drilldown panel — max-height + opacity transition (no transition-delay bug) -->
          <div
            class="agent-spotlight"
            :class="{ 'is-open': isDrillOpen }"
            role="region"
            :aria-label="selectedAgent ? `${selectedAgent.name} detail` : 'Agent detail'"
            aria-live="polite"
          >
            <template v-if="selectedAgent">

              <!-- Close button -->
              <div class="spotlight-close-row">
                <span class="spotlight-close-label">
                  {{ selectedAgent.name }} — Detail View
                </span>
                <button
                  type="button"
                  class="spotlight-close-btn"
                  :aria-label="`Close ${selectedAgent.name} detail panel`"
                  @click="selectRadarAgent(selectedAgent.id)"
                >
                  ✕
                </button>
              </div>

              <!-- Panel hero: icon + identity + deploy toggle -->
              <div class="spotlight-hero">
                <div class="spotlight-hero__left">
                  <span class="spotlight-icon" :class="`spotlight-icon--${selectedAgent.status}`" aria-hidden="true">
                    {{ selectedAgent.icon }}
                  </span>
                </div>
                <div class="spotlight-hero__main">
                  <div class="spotlight-identity">
                    <div class="spotlight-identity__top">
                      <h3 class="spotlight-name" :class="`spotlight-name--${selectedAgent.status}`">
                        {{ selectedAgent.name }}
                      </h3>
                      <span
                        class="spotlight-status-dot"
                        :class="`spotlight-status-dot--${selectedAgent.status}`"
                        aria-hidden="true"
                      ></span>
                      <span
                        class="spotlight-badge"
                        :class="`spotlight-badge--${selectedAgent.status}`"
                        :aria-label="`Status: ${selectedAgent.status}`"
                      >{{ selectedAgent.status.toUpperCase() }}</span>
                    </div>
                    <p class="spotlight-role">{{ selectedAgent.role }}</p>
                  </div>

                  <button
                    type="button"
                    class="deploy-toggle"
                    role="switch"
                    :aria-checked="selectedAgent.active"
                    :aria-label="`${selectedAgent.active ? 'Deactivate' : 'Activate'} ${selectedAgent.name} agent`"
                    @click="toggleAgent(selectedAgent)"
                  >
                    <span class="deploy-toggle__track" aria-hidden="true">
                      <span class="deploy-toggle__thumb"></span>
                    </span>
                    <span class="deploy-toggle__label">
                      {{ selectedAgent.active ? 'Active' : 'Standby' }}
                    </span>
                  </button>
                </div>
              </div>

              <!-- Stats row -->
              <div class="spotlight-stats" aria-label="Agent statistics">
                <div class="spotlight-stat">
                  <span class="spotlight-stat__val">{{ selectedAgent.uptime }}</span>
                  <span class="spotlight-stat__lbl">Uptime</span>
                </div>
                <div class="spotlight-stat-divider" aria-hidden="true"></div>
                <div class="spotlight-stat">
                  <span class="spotlight-stat__val spotlight-stat__val--threats">{{ selectedAgent.neutralized }}</span>
                  <span class="spotlight-stat__lbl">Neutralized</span>
                </div>
                <div class="spotlight-stat-divider" aria-hidden="true"></div>
                <div class="spotlight-stat spotlight-stat--last-action">
                  <span class="spotlight-stat__val spotlight-stat__val--action">{{ selectedAgent.lastAction }}</span>
                  <span class="spotlight-stat__lbl">Last action · {{ selectedAgent.lastActionAt }}</span>
                </div>
              </div>

              <!-- Radar dimension scores row -->
              <div class="radar-scores" aria-label="Radar dimension scores for this agent">
                <div
                  v-for="ax in radarAxes"
                  :key="`score-${ax.key}`"
                  class="radar-score-cell"
                >
                  <span class="radar-score-val">{{ selectedAgent.radarScores[ax.key] }}</span>
                  <span class="radar-score-bar-track" aria-hidden="true">
                    <span
                      class="radar-score-bar-fill"
                      :class="`radar-score-bar-fill--${selectedAgent.id}`"
                      :style="{ width: `${selectedAgent.radarScores[ax.key]}%` }"
                    ></span>
                  </span>
                  <span class="radar-score-lbl">{{ ax.label }}</span>
                </div>
              </div>

              <!-- Config entries -->
              <div class="spotlight-config" aria-label="Agent configuration summary">
                <h3 class="spotlight-config__heading">Configuration</h3>
                <dl class="spotlight-config__list">
                  <div
                    v-for="entry in selectedAgent.configEntries"
                    :key="entry.key"
                    class="config-entry"
                  >
                    <dt class="config-entry__key">{{ entry.key }}</dt>
                    <dd class="config-entry__val">{{ entry.value }}</dd>
                  </div>
                </dl>
              </div>

            </template>
          </div><!-- /agent-spotlight drilldown -->

        </section><!-- /spotlight-section -->

        <!-- ── Performance Metrics ─────────────────────────────────────── -->
        <section class="metrics-section card" aria-labelledby="metrics-heading">
          <div class="card__header">
            <h2 class="card__title" id="metrics-heading">Performance Metrics</h2>
          </div>
          <div class="metrics-grid">

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

          </div>
        </section>

        <!-- ── Deployment Controls ────────────────────────────────────── -->
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

        <!-- ── Activity Log ───────────────────────────────────────────── -->
        <section class="activity-section card" aria-labelledby="activity-heading">
          <div class="card__header">
            <h2 class="card__title" id="activity-heading">Activity Log</h2>
            <span class="card__meta">{{ filteredLog.length }} entries</span>
          </div>

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
/* ── Reset ─────────────────────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* ── Visually hidden ────────────────────────────────────────────────────── */
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

/* ── Page root — mount fade ─────────────────────────────────────────────── */
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

/* ── Page header ────────────────────────────────────────────────────────── */
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

.hdr-stat__dot--active  {
  background-color: var(--brand-primary);
  animation: dot-pulse 1.5s var(--easing) infinite;
}
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

/* ── Body ───────────────────────────────────────────────────────────────── */
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

/* ── Card base ──────────────────────────────────────────────────────────── */
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

/* ═══════════════════════════════════════════════════════════════════════════
   SPOTLIGHT / RADAR SECTION
   ═══════════════════════════════════════════════════════════════════════════ */
.spotlight-section {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
}

/* ── Radar area container ───────────────────────────────────────────────── */
.radar-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 5);
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 8);
  outline: none;
  background: linear-gradient(150deg, var(--brand-surface), color-mix(in srgb, var(--brand-surface) 85%, var(--brand-bg)));
  /* Entrance: fade + slide up from 16px, 80ms delay lets page opacity settle first */
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity var(--duration-slow) var(--easing),
    transform var(--duration-slow) var(--easing);
  transition-delay: 80ms;
}

.is-mounted .radar-area {
  opacity: 1;
  transform: translateY(0);
}

.radar-area:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -4px;
}

@media (max-width: 768px) {
  .radar-area {
    padding: calc(var(--space-unit) * 4);
  }
}

/* Radar header row */
.radar-header {
  width: 100%;
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 3);
  flex-wrap: wrap;
}

.radar-title {
  font-family: var(--font-heading);
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--brand-text);
}

.radar-subtitle {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Radar SVG + legend side-by-side */
.radar-body {
  width: 100%;
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 8);
  flex-wrap: wrap;
  justify-content: center;
}

.radar-chart {
  width: 100%;
  max-width: calc(var(--space-unit) * 100);
  height: auto;
  flex-shrink: 0;
}

@media (min-width: 768px) {
  .radar-chart {
    width: calc(var(--space-unit) * 90);
    flex-shrink: 0;
  }
}

/* ── Radar SVG elements ─────────────────────────────────────────────────── */
.radar-ring {
  stroke: var(--brand-border);
  stroke-width: 0.75;
}

.radar-axis-line {
  stroke: var(--brand-border);
  stroke-width: 0.75;
}

.radar-axis-label {
  font-family: var(--font-mono);
  font-size: 11px;
  fill: var(--brand-muted);
  pointer-events: none;
  user-select: none;
}

.radar-ring-label {
  font-family: var(--font-mono);
  font-size: 8px;
  fill: var(--brand-border);
  pointer-events: none;
  user-select: none;
}

/* Agent polygon fills and strokes */
.radar-polygon {
  fill-opacity: 0.12;
  stroke-width: 1.5;
  cursor: pointer;
  /* Entrance stagger: fade in from opacity 0, delay from --polygon-delay CSS custom property */
  animation: radar-enter var(--duration-slow) var(--easing) both;
  animation-delay: var(--polygon-delay, 0ms);
  transition:
    fill-opacity var(--duration-normal) var(--easing),
    stroke-width var(--duration-normal) var(--easing),
    filter var(--duration-normal) var(--easing),
    opacity var(--duration-normal) var(--easing);
}

/* Hover brightening — tactile affordance that polygons are clickable */
.radar-polygon:hover:not(.radar-polygon--selected):not(.radar-polygon--sentinel) {
  fill-opacity: 0.18;
  stroke-width: 2;
}

/* Sentinel hover: lift its special opacity rather than fill-opacity */
.radar-polygon--sentinel:hover:not(.radar-polygon--selected) {
  opacity: 0.55;
  stroke-width: 2;
}

.radar-polygon--scanner   {
  fill: var(--brand-primary);
  stroke: var(--brand-primary);
}
.radar-polygon--monitor   {
  fill: var(--brand-secondary);
  stroke: var(--brand-secondary);
}
.radar-polygon--responder {
  fill: var(--brand-accent);
  stroke: var(--brand-accent);
}
.radar-polygon--sentinel  {
  fill: var(--brand-text);
  stroke: var(--brand-text);
  opacity: 0.4;
  stroke-dasharray: 4 3;
}

/* Selected state — brighter fill, thicker stroke, glow */
.radar-polygon--selected {
  fill-opacity: 0.25;
  stroke-width: 2.5;
}

.radar-polygon--scanner.radar-polygon--selected {
  filter: drop-shadow(0 0 6px var(--brand-primary));
}
.radar-polygon--monitor.radar-polygon--selected {
  filter: drop-shadow(0 0 6px var(--brand-secondary));
}
.radar-polygon--responder.radar-polygon--selected {
  filter: drop-shadow(0 0 6px var(--brand-accent));
}
.radar-polygon--sentinel.radar-polygon--selected {
  filter: drop-shadow(0 0 4px var(--brand-text));
  opacity: 0.7;
}

/* Dimmed when another is selected */
.radar-polygon--dimmed {
  fill-opacity: 0.04;
  opacity: 0.35;
}

/* Hit-target circles — invisible, large enough to click easily */
.radar-node {
  fill: transparent;
  cursor: pointer;
  stroke: none;
}

.radar-node:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* Visible vertex dots on selected agent */
.radar-vertex-dot {
  transition: opacity var(--duration-fast) var(--easing);
  pointer-events: none;
}

.radar-vertex-dot--scanner   { fill: var(--brand-primary);   }
.radar-vertex-dot--monitor   { fill: var(--brand-secondary); }
.radar-vertex-dot--responder { fill: var(--brand-accent);    }
.radar-vertex-dot--sentinel  { fill: var(--brand-text);      }

/* ── Radar legend ────────────────────────────────────────────────────────── */
.radar-legend {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
  min-width: calc(var(--space-unit) * 44);
}

@media (max-width: 768px) {
  .radar-legend {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    min-width: unset;
  }
}

.radar-legend-btn {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2.5);
  padding: calc(var(--space-unit) * 2.5) calc(var(--space-unit) * 3.5);
  background: none;
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  width: 100%;
  text-align: left;
  transition:
    background-color var(--duration-fast) var(--easing),
    border-color var(--duration-fast) var(--easing),
    color var(--duration-fast) var(--easing);
}

.radar-legend-btn:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.radar-legend-btn:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 60%, var(--brand-bg-secondary));
  color: var(--brand-text);
  border-color: color-mix(in srgb, var(--brand-border) 150%, var(--brand-text));
}

.radar-legend-btn--selected {
  background-color: color-mix(in srgb, var(--brand-surface) 40%, var(--brand-bg-secondary));
  color: var(--brand-text);
  border-color: var(--brand-text);
}

.radar-legend-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.radar-legend-dot--scanner   { background-color: var(--brand-primary);   }
.radar-legend-dot--monitor   { background-color: var(--brand-secondary); }
.radar-legend-dot--responder { background-color: var(--brand-accent);    }
.radar-legend-dot--sentinel  {
  background-color: color-mix(in srgb, var(--brand-text) 40%, transparent);
  outline: 1px dashed var(--brand-text);
  outline-offset: 2px;
}

.radar-legend-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
  min-width: 0;
}

.radar-legend-name {
  font-family: var(--font-heading);
  font-size: 0.875rem;
  font-weight: 700;
  line-height: 1;
}

.radar-legend-role {
  font-family: var(--font-body);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.radar-legend-status-dot {
  width: calc(var(--space-unit) * 1.5);
  height: calc(var(--space-unit) * 1.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.radar-legend-status-dot--active  {
  background-color: var(--brand-primary);
  animation: dot-pulse 1.5s var(--easing) infinite;
}
.radar-legend-status-dot--standby { background-color: var(--brand-secondary); }
.radar-legend-status-dot--offline { background-color: var(--brand-error);     }

/* ── Drilldown panel — max-height + opacity transition ──────────────────── */
/* No compound transition-delay selectors — each property transitioned independently */
.agent-spotlight {
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  transition:
    max-height var(--duration-slow) var(--easing),
    opacity var(--duration-normal) var(--easing);
  border-top: 1px solid transparent;
  transition-property: max-height, opacity, border-top-color;
}

.agent-spotlight.is-open {
  max-height: 1000px;
  opacity: 1;
  border-top-color: var(--brand-border);
}

/* Close row at top of drilldown */
.spotlight-close-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 8);
  border-bottom: 1px solid var(--brand-border);
  background-color: var(--brand-bg-secondary);
}

.spotlight-close-label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.spotlight-close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(var(--space-unit) * 7);
  height: calc(var(--space-unit) * 7);
  border-radius: var(--radius-sm);
  background: none;
  border: 1px solid var(--brand-border);
  cursor: pointer;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  transition:
    background-color var(--duration-fast) var(--easing),
    color var(--duration-fast) var(--easing),
    border-color var(--duration-fast) var(--easing);
}

.spotlight-close-btn:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.spotlight-close-btn:hover {
  background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);
  border-color: var(--brand-error);
  color: var(--brand-error);
}

/* Drilldown content entrance — staggered fade+slide when panel opens */
.agent-spotlight.is-open .spotlight-hero {
  animation: drill-enter var(--duration-normal) var(--easing) both;
  animation-delay: 80ms;
}

.agent-spotlight.is-open .spotlight-stats {
  animation: drill-enter var(--duration-normal) var(--easing) both;
  animation-delay: 140ms;
}

.agent-spotlight.is-open .radar-scores {
  animation: drill-enter var(--duration-normal) var(--easing) both;
  animation-delay: 200ms;
}

/* Spotlight hero inside drilldown */
.spotlight-hero {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 6);
  padding: calc(var(--space-unit) * 8) calc(var(--space-unit) * 8) 0;
}

.spotlight-hero__left {
  flex-shrink: 0;
}

.spotlight-icon {
  font-size: 2rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(var(--space-unit) * 16);
  height: calc(var(--space-unit) * 16);
  border-radius: var(--radius-md);
  border: 1px solid var(--brand-border);
  background-color: var(--brand-bg-secondary);
  transition:
    color var(--duration-normal) var(--easing),
    border-color var(--duration-normal) var(--easing);
}

.spotlight-icon--active  {
  color: var(--brand-primary);
  border-color: color-mix(in srgb, var(--brand-primary) 35%, transparent);
}
.spotlight-icon--standby {
  color: var(--brand-secondary);
  border-color: color-mix(in srgb, var(--brand-secondary) 35%, transparent);
}
.spotlight-icon--offline {
  color: color-mix(in srgb, var(--brand-error) 60%, transparent);
}

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
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0;
  transition: color var(--duration-normal) var(--easing);
}

.spotlight-name--active  { color: var(--brand-primary);   }
.spotlight-name--standby { color: var(--brand-secondary); }
.spotlight-name--offline { color: color-mix(in srgb, var(--brand-text) 50%, transparent); }

.spotlight-status-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.spotlight-status-dot--active  {
  background-color: var(--brand-primary);
  animation: dot-pulse 1.5s var(--easing) infinite;
}
.spotlight-status-dot--standby { background-color: var(--brand-secondary); }
.spotlight-status-dot--offline { background-color: var(--brand-error);     }

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
  font-size: 0.9375rem;
  color: var(--brand-muted);
  margin: 0;
  line-height: 1.5;
}

/* Deployment toggle */
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

.deploy-toggle--inline {
  flex-shrink: 0;
}

/* Spotlight stats row */
.spotlight-stats {
  display: flex;
  align-items: stretch;
  gap: 0;
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--brand-border);
  overflow: hidden;
  margin: calc(var(--space-unit) * 6) calc(var(--space-unit) * 8);
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
  font-size: 1.125rem;
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
  font-size: 0.5625rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

@media (max-width: 768px) {
  .spotlight-stats {
    flex-direction: column;
    margin: calc(var(--space-unit) * 4) calc(var(--space-unit) * 4);
  }
  .spotlight-stat-divider {
    width: auto;
    height: 1px;
  }
}

/* ── Radar dimension scores (inside drilldown) ──────────────────────────── */
.radar-scores {
  display: flex;
  gap: calc(var(--space-unit) * 3);
  padding: 0 calc(var(--space-unit) * 8) calc(var(--space-unit) * 6);
  flex-wrap: wrap;
}

.radar-score-cell {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
  min-width: calc(var(--space-unit) * 22);
  flex: 1;
}

.radar-score-val {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--brand-primary);
  line-height: 1;
}

.radar-score-bar-track {
  display: block;
  height: calc(var(--space-unit) * 1.5);
  background-color: color-mix(in srgb, var(--brand-border) 80%, transparent);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.radar-score-bar-fill {
  display: block;
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--duration-slow) var(--easing);
}

/* Agent-tinted fill colors for score bars */
.radar-score-bar-fill--scanner   { background-color: var(--brand-primary);   }
.radar-score-bar-fill--monitor   { background-color: var(--brand-secondary); }
.radar-score-bar-fill--responder { background-color: var(--brand-accent);    }
.radar-score-bar-fill--sentinel  {
  background-color: color-mix(in srgb, var(--brand-text) 50%, transparent);
}

.radar-score-lbl {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 500;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

@media (max-width: 768px) {
  .radar-scores {
    padding: 0 calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
  }
}

/* Config summary inside drilldown */
.spotlight-config {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
  padding: 0 calc(var(--space-unit) * 8) calc(var(--space-unit) * 8);
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

@media (max-width: 768px) {
  .spotlight-hero {
    padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 4) 0;
  }
  .spotlight-config {
    padding: 0 calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
  }
}

/* ═══════════════════════════════════════════════════════════════════════════
   PERFORMANCE METRICS SECTION
   ═══════════════════════════════════════════════════════════════════════════ */
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

/* ═══════════════════════════════════════════════════════════════════════════
   DEPLOYMENT CONTROLS SECTION
   ═══════════════════════════════════════════════════════════════════════════ */
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

/* ═══════════════════════════════════════════════════════════════════════════
   ACTIVITY LOG SECTION
   ═══════════════════════════════════════════════════════════════════════════ */
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

.log-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.log-entry {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 3) 1fr auto;
  align-items: start;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
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

/* ═══════════════════════════════════════════════════════════════════════════
   KEYFRAMES
   ═══════════════════════════════════════════════════════════════════════════ */

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

/* Radar polygon entrance — opacity fade, stagger via --polygon-delay */
@keyframes radar-enter {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Active status dot heartbeat pulse — applied to all --active dot variants */
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

/* Drilldown panel content entrance — fade + subtle slide up 8px */
@keyframes drill-enter {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ═══════════════════════════════════════════════════════════════════════════
   ACCESSIBILITY — reduced-motion guard (always last rule)
   ═══════════════════════════════════════════════════════════════════════════ */
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

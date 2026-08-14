<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/agents/v3-agent-spotlight-tabs-line-performance
// Fork of v3-agent-spotlight-tabs.
// Change: replace hero spotlight panel with a real-time multi-series line chart.
// Chart sits ABOVE the agent tabs. Tabs remain below for agent switching.
// Preserved verbatim: sticky header, metrics card, deployment controls, activity log.

// ── Types ──────────────────────────────────────────────────────────────────
interface ChartPoint {
  t: number       // 0-29 — rolling window index
  rps: number     // requests per second
  latency: number // ms
  errRate: number // 0–100 (percentage)
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
  chartData: ChartPoint[]
}

interface ActivityEntry {
  id: number
  agentId: string
  type: 'detection' | 'response' | 'scan' | 'config'
  message: string
  at: string
}

// ── Chart seed helpers ─────────────────────────────────────────────────────
function rand(min: number, max: number): number {
  return min + Math.random() * (max - min)
}

function seedChart(
  rpsRange: [number, number],
  latRange: [number, number],
  errRange: [number, number]
): ChartPoint[] {
  return Array.from({ length: 30 }, (_, t) => ({
    t,
    rps:     rand(rpsRange[0], rpsRange[1]),
    latency: rand(latRange[0],  latRange[1]),
    errRate: rand(errRange[0],  errRange[1]),
  }))
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
    chartData: seedChart([40, 90], [150, 250], [0, 3]),
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
    chartData: seedChart([20, 50], [180, 300], [1, 5]),
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
    chartData: seedChart([10, 30], [100, 180], [0, 2]),
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
      { key: 'Sweep interval',  value: '5m'        },
      { key: 'Perimeter scope', value: 'All zones' },
      { key: 'Alert on',        value: 'Unknown IPs'},
      { key: 'Mode',            value: 'Passive'   },
    ],
    chartData: seedChart([5, 15], [250, 400], [0, 8]),
  },
])

// ── Selected tab state ─────────────────────────────────────────────────────
const selectedId = ref('scanner')

const selectedAgent = computed(() => agents.value.find(a => a.id === selectedId.value)!)

function selectAgent(id: string) {
  selectedId.value = id
  // Bump key so Vue <Transition mode="out-in"> cross-fades chart SVG
  chartKey.value++
}

// ── Tab keyboard navigation (WCAG 2.1 AA — roving tabindex, Arrow/Home/End) ─
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

const filteredLog = computed(() =>
  activeFilter.value === 'all'
    ? activityLog
    : activityLog.filter(e => e.type === activeFilter.value)
)

// ── SVG chart geometry ─────────────────────────────────────────────────────
// viewBox="0 0 600 200"  preserveAspectRatio="none"
// Plot area: x 48–580 (left 48px for Y labels), y 12–172 (bottom 28px for X axis)
// plotW = 532, plotH = 160
const PLOT_X0  = 48
const PLOT_X1  = 580
const PLOT_Y0  = 12
const PLOT_Y1  = 172
const PLOT_W   = PLOT_X1 - PLOT_X0  // 532
const PLOT_H   = PLOT_Y1 - PLOT_Y0  // 160

function seriesPath(values: number[], min: number, max: number): string {
  const range = max - min || 1
  return values.map((v, i) => {
    const x = PLOT_X0 + (i / (values.length - 1)) * PLOT_W
    const y = PLOT_Y0 + PLOT_H - ((v - min) / range) * PLOT_H
    return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`
  }).join(' ')
}

function areaPath(linePath: string): string {
  return `${linePath} L${PLOT_X1},${PLOT_Y1} L${PLOT_X0},${PLOT_Y1} Z`
}

// ── Chart computed values for the selected agent ───────────────────────────
const chartPoints = computed(() => selectedAgent.value.chartData)

const rpsValues     = computed(() => chartPoints.value.map(p => p.rps))
const latValues     = computed(() => chartPoints.value.map(p => p.latency))
const errValues     = computed(() => chartPoints.value.map(p => p.errRate))

const rpsMin     = computed(() => Math.min(...rpsValues.value))
const rpsMax     = computed(() => Math.max(...rpsValues.value))
const latMin     = computed(() => Math.min(...latValues.value))
const latMax     = computed(() => Math.max(...latValues.value))
const errMin     = computed(() => Math.min(...errValues.value))
const errMax     = computed(() => Math.max(...errValues.value))

const rpsLinePath = computed(() => seriesPath(rpsValues.value, rpsMin.value, rpsMax.value))
const latLinePath = computed(() => seriesPath(latValues.value, latMin.value, latMax.value))
const errLinePath = computed(() => seriesPath(errValues.value, errMin.value, errMax.value))

const rpsAreaPath = computed(() => areaPath(rpsLinePath.value))
const latAreaPath = computed(() => areaPath(latLinePath.value))
const errAreaPath = computed(() => areaPath(errLinePath.value))

// Y-axis label values (4 grid lines at y=52,92,132,172 → top→bottom = max→min)
const rpsYLabels = computed(() => {
  const range = rpsMax.value - rpsMin.value || 1
  return [1, 0.667, 0.333, 0].map(frac =>
    (rpsMin.value + frac * range).toFixed(0)
  )
})

// X-axis: 6 evenly spaced time ticks
const xTicks = computed(() => {
  const n = 6
  return Array.from({ length: n }, (_, i) => {
    const frac = i / (n - 1)
    const x = PLOT_X0 + frac * PLOT_W
    const label = `T-${(30 - Math.round(frac * 29)).toString().padStart(2, '0')}`
    return { x, label }
  })
})

// Accessible latest values
const latestRps     = computed(() => chartPoints.value[chartPoints.value.length - 1]?.rps.toFixed(1)    ?? '0')
const latestLatency = computed(() => chartPoints.value[chartPoints.value.length - 1]?.latency.toFixed(0) ?? '0')
const latestErrRate = computed(() => chartPoints.value[chartPoints.value.length - 1]?.errRate.toFixed(2)  ?? '0')

// ── Chart cross-fade key — incremented on tab change to trigger Transition ──
const chartKey = ref(0)

// ── Readout flash — toggled on each data tick to trigger val-flash animation ─
const readoutFlash = ref(false)

// ── Live chart update (2s tick, 30-point rolling window) ───────────────────
let chartTick: ReturnType<typeof setInterval> | null = null

const rpsRanges: Record<string, [number, number]>     = { scanner: [40,90], monitor: [20,50], responder: [10,30], sentinel: [5,15]   }
const latRanges: Record<string, [number, number]>     = { scanner: [150,250], monitor: [180,300], responder: [100,180], sentinel: [250,400] }
const errRanges: Record<string, [number, number]>     = { scanner: [0,3], monitor: [1,5], responder: [0,2], sentinel: [0,8] }

function pushChartPoint(agent: Agent) {
  const id = agent.id
  const newPoint: ChartPoint = {
    t:       (agent.chartData[agent.chartData.length - 1].t + 1) % 30,
    rps:     rand(rpsRanges[id][0], rpsRanges[id][1]),
    latency: rand(latRanges[id][0], latRanges[id][1]),
    errRate: rand(errRanges[id][0], errRanges[id][1]),
  }
  agent.chartData = [...agent.chartData.slice(1), newPoint]
  // Toggle flash class for live readout values
  readoutFlash.value = !readoutFlash.value
}

// ── Helpers ────────────────────────────────────────────────────────────────
function agentName(id: string): string {
  return agents.value.find(a => a.id === id)?.name ?? id
}

function fprLabel(rate: number): string {
  return (rate * 100).toFixed(1) + '%'
}

// ── Computed stats ─────────────────────────────────────────────────────────
const activeCount   = computed(() => agents.value.filter(a => a.status === 'active').length)
const standbyCount  = computed(() => agents.value.filter(a => a.status === 'standby').length)
const maxResponseTime = computed(() => Math.max(...agents.value.map(a => a.responseTime)))

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
  chartTick = setInterval(() => {
    agents.value.forEach(agent => pushChartPoint(agent))
  }, 2000)
  // nextTick is mandatory — ensures opacity:0 is painted before transition fires
  nextTick(() => { isMounted.value = true })
})

onUnmounted(() => {
  if (clockInterval !== null) {
    clearInterval(clockInterval)
    clockInterval = null
  }
  if (chartTick !== null) {
    clearInterval(chartTick)
    chartTick = null
  }
})
</script>

<template>
  <div class="page" :class="{ 'is-mounted': isMounted }">
    <h1 class="sr-only">Aegis Agent Management — Live Performance</h1>

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

        <!-- ── Chart + Tabs spotlight section ───────────────────────────── -->
        <section class="spotlight-section" aria-label="Agent performance spotlight">

          <!-- 1. Chart area (top) -->
          <div class="chart-area">

            <!-- Chart header: agent identity + legend -->
            <div class="chart-header">
              <div class="chart-identity">
                <h2 class="chart-agent-name" :class="`chart-agent-name--${selectedAgent.status}`">
                  {{ selectedAgent.name }}
                </h2>
                <span
                  class="spotlight-badge"
                  :class="`spotlight-badge--${selectedAgent.status}`"
                  :aria-label="`Status: ${selectedAgent.status}`"
                >{{ selectedAgent.status.toUpperCase() }}</span>
                <p class="chart-agent-role">{{ selectedAgent.role }}</p>
              </div>

              <div class="chart-legend" aria-label="Chart series legend">
                <div class="legend-item">
                  <span class="legend-dot legend-dot--rps" aria-hidden="true"></span>
                  <span class="legend-label">REQ/S</span>
                </div>
                <div class="legend-item">
                  <span class="legend-dot legend-dot--lat" aria-hidden="true"></span>
                  <span class="legend-label">LATENCY</span>
                </div>
                <div class="legend-item">
                  <span class="legend-dot legend-dot--err" aria-hidden="true"></span>
                  <span class="legend-label">ERR RATE</span>
                </div>
              </div>
            </div>

            <!-- Accessible screen-reader summary -->
            <p class="sr-only">
              Showing requests/sec, latency, and error rate for {{ selectedAgent.name }}.
              Current: {{ latestRps }} req/s, {{ latestLatency }}ms latency, {{ latestErrRate }}% error rate.
            </p>

            <!-- SVG line chart — aria-hidden, sr-only text above provides accessible alternative -->
            <!-- chart-fade Transition: opacity cross-fade when selected agent key changes -->
            <Transition name="chart-fade" mode="out-in">
            <div class="chart-svg-wrap" :key="chartKey">
              <svg
                class="chart-svg"
                viewBox="0 0 600 200"
                preserveAspectRatio="none"
                aria-hidden="true"
              >
                <!-- Grid lines at y=52,92,132,172 -->
                <line x1="48" y1="52"  x2="580" y2="52"  class="chart-grid" />
                <line x1="48" y1="92"  x2="580" y2="92"  class="chart-grid" />
                <line x1="48" y1="132" x2="580" y2="132" class="chart-grid" />
                <line x1="48" y1="172" x2="580" y2="172" class="chart-grid" />

                <!-- Y-axis labels (top→bottom = max→min, using rps scale for reference) -->
                <text
                  v-for="(label, i) in rpsYLabels"
                  :key="`y-label-${i}`"
                  :x="44"
                  :y="[52, 92, 132, 172][i] + 3"
                  text-anchor="end"
                  class="chart-axis-label"
                >{{ label }}</text>

                <!-- X-axis tick labels -->
                <text
                  v-for="tick in xTicks"
                  :key="`x-tick-${tick.label}`"
                  :x="tick.x"
                  y="192"
                  text-anchor="middle"
                  class="chart-x-label"
                >{{ tick.label }}</text>

                <!-- Defs: gradient fills for each series (8% opacity) -->
                <defs>
                  <linearGradient id="grad-rps" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%"   class="grad-stop-rps"  stop-opacity="0.18" />
                    <stop offset="100%" class="grad-stop-rps"  stop-opacity="0.02" />
                  </linearGradient>
                  <linearGradient id="grad-lat" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%"   class="grad-stop-lat"  stop-opacity="0.18" />
                    <stop offset="100%" class="grad-stop-lat"  stop-opacity="0.02" />
                  </linearGradient>
                  <linearGradient id="grad-err" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%"   class="grad-stop-err"  stop-opacity="0.18" />
                    <stop offset="100%" class="grad-stop-err"  stop-opacity="0.02" />
                  </linearGradient>
                </defs>

                <!-- Area fills -->
                <path :d="rpsAreaPath" fill="url(#grad-rps)" class="chart-area-fill" />
                <path :d="latAreaPath" fill="url(#grad-lat)" class="chart-area-fill" />
                <path :d="errAreaPath" fill="url(#grad-err)" class="chart-area-fill" />

                <!-- Line series -->
                <path
                  :d="rpsLinePath"
                  class="chart-line chart-line--rps"
                  fill="none"
                  stroke-width="1.75"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  :d="latLinePath"
                  class="chart-line chart-line--lat"
                  fill="none"
                  stroke-width="1.75"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  :d="errLinePath"
                  class="chart-line chart-line--err"
                  fill="none"
                  stroke-width="1.75"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            </Transition>

            <!-- Live current value readout bar -->
            <div class="chart-readout" aria-label="Current metric values">
              <div class="readout-item">
                <span class="readout-val readout-val--rps" :class="{ 'readout-val--flashing': readoutFlash }">{{ latestRps }}</span>
                <span class="readout-unit">REQ/S</span>
              </div>
              <span class="readout-sep" aria-hidden="true"></span>
              <div class="readout-item">
                <span class="readout-val readout-val--lat" :class="{ 'readout-val--flashing': readoutFlash }">{{ latestLatency }}</span>
                <span class="readout-unit">MS LAT</span>
              </div>
              <span class="readout-sep" aria-hidden="true"></span>
              <div class="readout-item">
                <span class="readout-val readout-val--err" :class="{ 'readout-val--flashing': readoutFlash }">{{ latestErrRate }}</span>
                <span class="readout-unit">% ERR</span>
              </div>
            </div>
          </div><!-- /chart-area -->

          <!-- 2. Agent tabs (below chart) -->
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

          <!-- Hidden tabpanel stubs for ARIA completeness — v-show keeps DOM/aria refs intact -->
          <div
            v-for="agent in agents"
            :key="`panel-${agent.id}`"
            role="tabpanel"
            :id="`panel-${agent.id}`"
            :aria-labelledby="`tab-${agent.id}`"
            tabindex="0"
            class="sr-panel"
            v-show="selectedId === agent.id"
          >
            <!-- Panel content is fully represented by the chart above -->
            <span class="sr-only">Performance chart shown above for {{ agent.name }}.</span>
          </div>

        </section><!-- /spotlight-section -->

        <!-- ── Performance Metrics ─────────────────────────────────────── -->
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
                class="deploy-toggle"
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
   SPOTLIGHT SECTION — CHART ABOVE · TABS BELOW
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

/* ── Chart area ─────────────────────────────────────────────────────────── */
.chart-area {
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 8);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 5);
  background: linear-gradient(160deg, var(--brand-surface), color-mix(in srgb, var(--brand-surface) 80%, var(--brand-bg)));
  border-bottom: 1px solid var(--brand-border);
  /* Entrance: slide up + fade in after page mount. 80ms delay lets page fade complete first. */
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity var(--duration-slow) var(--easing),
    transform var(--duration-slow) var(--easing);
  transition-delay: 80ms;
}

.is-mounted .chart-area {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 768px) {
  .chart-area {
    padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 4);
  }
}

/* Chart header: identity left, legend right */
.chart-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 4);
  flex-wrap: wrap;
}

.chart-identity {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  flex-wrap: wrap;
}

.chart-agent-name {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
  transition: color var(--duration-normal) var(--easing);
}

.chart-agent-name--active  { color: var(--brand-primary);   }
.chart-agent-name--standby { color: var(--brand-secondary); }
.chart-agent-name--offline { color: color-mix(in srgb, var(--brand-text) 55%, transparent); }

/* Status badge */
.spotlight-badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
  flex-shrink: 0;
}

.spotlight-badge--active  { background-color: var(--brand-primary);   }
.spotlight-badge--standby { background-color: var(--brand-secondary); }
.spotlight-badge--offline { background-color: var(--brand-error);     }

.chart-agent-role {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--brand-muted);
  margin: 0;
}

/* Legend */
.chart-legend {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 5);
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.legend-dot {
  width: calc(var(--space-unit) * 3);
  height: calc(var(--space-unit) * 3);
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-dot--rps { background-color: var(--brand-primary);   }
.legend-dot--lat { background-color: var(--brand-secondary); }
.legend-dot--err { background-color: var(--brand-accent);    }

.legend-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-text);
}

/* Chart SVG wrapper — preserves aspect ratio on narrow screens */
.chart-svg-wrap {
  width: 100%;
  overflow: hidden;
  border-radius: var(--radius-sm);
}

.chart-svg {
  width: 100%;
  height: calc(var(--space-unit) * 50);
  display: block;
}

@media (max-width: 768px) {
  .chart-svg {
    height: calc(var(--space-unit) * 38);
  }
}

/* Chart grid lines */
.chart-grid {
  stroke: var(--brand-border);
  stroke-dasharray: 4 4;
  stroke-width: 1;
}

/* Axis labels (SVG text elements — class-driven styling) */
.chart-axis-label {
  font-family: var(--font-mono);
  font-size: 9px;
  fill: var(--brand-muted);
}

.chart-x-label {
  font-family: var(--font-mono);
  font-size: 8px;
  fill: var(--brand-muted);
}

/* Gradient stop colors (CSS class on SVG stop elements) */
.grad-stop-rps { stop-color: var(--brand-primary);   }
.grad-stop-lat { stop-color: var(--brand-secondary); }
.grad-stop-err { stop-color: var(--brand-accent);    }

/* Area fills opacity controlled at stop level above; clip is handled by Z close */
.chart-area-fill {
  /* opacity handled by stop-opacity in the gradient defs */
}

/* Line series */
.chart-line--rps { stroke: var(--brand-primary);   }
.chart-line--lat { stroke: var(--brand-secondary); }
.chart-line--err { stroke: var(--brand-accent);    }

/* Live readout bar — below chart SVG */
.chart-readout {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  background-color: var(--brand-bg-secondary);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 5);
  flex-wrap: wrap;
}

.readout-item {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 1.5);
}

.readout-val {
  font-family: var(--font-mono);
  font-size: 1.375rem;
  font-weight: 700;
  line-height: 1;
}

.readout-val--rps { color: var(--brand-primary);   }
.readout-val--lat { color: var(--brand-secondary); }
.readout-val--err { color: var(--brand-accent);    }

/* Flash class toggled on every data tick via readoutFlash boolean */
.readout-val--flashing {
  animation: val-flash var(--duration-normal) var(--easing);
}

.readout-unit {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.readout-sep {
  width: 1px;
  height: calc(var(--space-unit) * 6);
  background-color: var(--brand-border);
  flex-shrink: 0;
}

/* ── Agent tab list (below chart) ───────────────────────────────────────── */
.agent-tabs {
  display: flex;
  gap: 0;
  background: linear-gradient(180deg, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 95%, var(--brand-primary)));
  overflow-x: auto;
  scrollbar-width: none;
}

.agent-tabs::-webkit-scrollbar {
  display: none;
}

.agent-tab {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 0.75);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  background: none;
  border: none;
  border-top: 2px solid transparent;
  cursor: pointer;
  text-align: left;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  transition:
    color var(--duration-fast) var(--easing),
    border-color var(--duration-fast) var(--easing),
    background-color var(--duration-fast) var(--easing);
  flex-shrink: 0;
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
  border-top-color: var(--brand-primary);
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

.agent-tab__dot--active  {
  background-color: var(--brand-primary);
  animation: dot-pulse 1.5s var(--easing) infinite;
}
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

/* ARIA tabpanel stubs — not visible, only serve ARIA integrity */
.sr-panel {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
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

/* Metric list items (FPR) */
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

/* Deployment toggle (switch) */
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
  flex-shrink: 0;
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

/* Log list */
.log-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

/* Log entry — stagger animation via CSS custom property */
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

/* ═══════════════════════════════════════════════════════════════════════════
   KEYFRAMES
   ═══════════════════════════════════════════════════════════════════════════ */

/* Chart SVG area cross-fade — Vue <Transition name="chart-fade" mode="out-in"> */
.chart-fade-enter-active,
.chart-fade-leave-active {
  transition: opacity var(--duration-fast) var(--easing);
}

.chart-fade-enter-from,
.chart-fade-leave-to {
  opacity: 0;
}

/* Active status dot heartbeat pulse */
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

/* Readout value brief flash — triggers on every 2s data tick */
@keyframes val-flash {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}

/* Log entry stagger entrance */
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

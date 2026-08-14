<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/agents/v1-grid-roster-log
// Layout: sticky header · 2×2 agent card grid · lower-row (metrics | controls) · activity log

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
    sparkline: [12,18,15,22,31,28,45,38,52,47,61,55,48,63,71,58,44,67,72,69,81,76,88,83],
    responseTime: 187, falsePositiveRate: 0.02, coverage: 94,
  },
  {
    id: 'monitor', name: 'Monitor', role: 'Traffic analysis',
    icon: '◈', status: 'active', active: true,
    uptime: '99.91%', neutralized: 87,
    lastAction: 'Detected anomalous request pattern on llm-worker-07',
    lastActionAt: '14s ago',
    sparkline: [8,12,19,14,23,28,33,41,36,44,38,51,47,55,49,62,57,64,71,68,74,78,72,81],
    responseTime: 203, falsePositiveRate: 0.035, coverage: 88,
  },
  {
    id: 'responder', name: 'Responder', role: 'Threat containment',
    icon: '◉', status: 'active', active: true,
    uptime: '99.85%', neutralized: 203,
    lastAction: 'Isolated orchestrator-02 from network segment',
    lastActionAt: '34s ago',
    sparkline: [22,31,28,41,38,52,47,61,55,48,63,71,58,44,67,72,69,81,76,88,83,91,86,94],
    responseTime: 142, falsePositiveRate: 0.018, coverage: 97,
  },
  {
    id: 'sentinel', name: 'Sentinel', role: 'Perimeter watch',
    icon: '◇', status: 'standby', active: false,
    uptime: '98.40%', neutralized: 56,
    lastAction: 'Completed perimeter sweep — no anomalies',
    lastActionAt: '4m ago',
    sparkline: [5,8,6,9,7,11,8,14,10,12,9,16,13,11,15,12,18,14,17,13,19,16,21,18],
    responseTime: 312, falsePositiveRate: 0.041, coverage: 82,
  },
])

// ── Activity log data ─────────────────────────────────────────────────
const activityLog: ActivityEntry[] = [
  { id: 1,  agentId: 'scanner',   type: 'detection', message: 'Flagged CVE-2024-4891 on api-gateway-01 — severity CRITICAL (9.8)', at: '2s ago'   },
  { id: 2,  agentId: 'monitor',   type: 'detection', message: 'Anomalous request pattern detected on llm-worker-07 — 4× baseline rate', at: '14s ago'  },
  { id: 3,  agentId: 'responder', type: 'response',  message: 'Isolated orchestrator-02 from network segment — clean proxy active', at: '34s ago'  },
  { id: 4,  agentId: 'scanner',   type: 'scan',      message: 'Full sweep of api-gateway cluster completed — 3 new fingerprints logged', at: '1m ago'   },
  { id: 5,  agentId: 'monitor',   type: 'detection', message: 'Token privilege escalation probe on auth-service — blocked at ingress', at: '2m ago'   },
  { id: 6,  agentId: 'sentinel',  type: 'scan',      message: 'Perimeter sweep completed — no anomalies detected across 12 endpoints', at: '4m ago'   },
  { id: 7,  agentId: 'responder', type: 'response',  message: 'Containment boundary restored for llm-worker-07 — traffic rerouted', at: '6m ago'   },
  { id: 8,  agentId: 'scanner',   type: 'detection', message: 'CVE-2024-3310 flagged on model-output-service — HIGH severity (8.9)', at: '8m ago'   },
  { id: 9,  agentId: 'monitor',   type: 'scan',      message: 'Baseline recalibrated for api-gateway cluster — 847 requests sampled', at: '12m ago'  },
  { id: 10, agentId: 'responder', type: 'config',    message: 'Response threshold updated: containment trigger reduced to 2 anomaly events', at: '18m ago'  },
  { id: 11, agentId: 'sentinel',  type: 'config',    message: 'Perimeter sweep interval adjusted to 4m from 6m — high-threat window active', at: '21m ago'  },
  { id: 12, agentId: 'scanner',   type: 'scan',      message: 'Scheduled vulnerability scan completed — fine-tune cluster clear', at: '29m ago'  },
  { id: 13, agentId: 'monitor',   type: 'detection', message: 'Unusual embedding query pattern on vector-store-01 — monitoring elevated', at: '34m ago'  },
  { id: 14, agentId: 'responder', type: 'response',  message: 'Patch deployment for CVE-2024-2208 verified — memory-store-01 secured', at: '42m ago'  },
  { id: 15, agentId: 'scanner',   type: 'config',    message: 'Signature database updated: 847 new patterns ingested', at: '1h ago'   },
]

// ── Filter state ──────────────────────────────────────────────────────
const filters = [
  { value: 'all',       label: 'All'       },
  { value: 'detection', label: 'Detection' },
  { value: 'response',  label: 'Response'  },
  { value: 'scan',      label: 'Scan'      },
  { value: 'config',    label: 'Config'    },
] as const

const activeFilter = ref<string>('all')

const filteredLog = computed(() =>
  activeFilter.value === 'all'
    ? activityLog
    : activityLog.filter(e => e.type === activeFilter.value)
)

// ── Config summary (static) ───────────────────────────────────────────
const configSummary = [
  { label: 'Scan Interval',       value: '60s'       },
  { label: 'Response Threshold',  value: '2 events'  },
  { label: 'Monitoring Window',   value: '5m rolling'},
  { label: 'Alert Escalation',    value: '< 30s'     },
]

// ── Helpers ───────────────────────────────────────────────────────────
function toggleAgent(agent: Agent) {
  agent.active = !agent.active
  agent.status = agent.active ? 'active' : 'standby'
}

function sparklinePath(values: number[]): string {
  return values.map((v, i) => {
    const x = (i / (values.length - 1)) * 120
    const y = 40 - (v / 100) * 40
    return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`
  }).join(' ')
}

function sparklineAreaPath(values: number[]): string {
  const line = sparklinePath(values)
  const lastX = 120
  return `${line} L${lastX},40 L0,40 Z`
}

function statusToken(status: Agent['status']): string {
  const map: Record<Agent['status'], string> = {
    active:  'var(--brand-primary)',
    standby: 'var(--brand-secondary)',
    offline: 'var(--brand-error)',
  }
  return map[status]
}

function logTypeToken(type: ActivityEntry['type']): string {
  const map: Record<ActivityEntry['type'], string> = {
    detection: 'log-dot--detection',
    response:  'log-dot--response',
    scan:      'log-dot--scan',
    config:    'log-dot--config',
  }
  return map[type]
}

function agentName(id: string): string {
  return agents.value.find(a => a.id === id)?.name ?? id
}

// ── Computed stats ────────────────────────────────────────────────────
const activeCount = computed(() => agents.value.filter(a => a.status === 'active').length)

// ── Live clock ────────────────────────────────────────────────────────
const liveTime = ref('')
let clockInterval: ReturnType<typeof setInterval> | null = null

function updateClock() {
  const now = new Date()
  liveTime.value = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

// ── Mount ─────────────────────────────────────────────────────────────
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
    <h1 class="sr-only">Aegis Agent Management</h1>

    <!-- ── Page header ───────────────────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Agents page header">
      <div class="page-header__inner">
        <div class="page-header__left">
          <span class="page-header__brand">AEGIS</span>
          <span class="page-header__sep" aria-hidden="true">/</span>
          <span class="page-header__title">Agent Management</span>
        </div>
        <div class="page-header__right">
          <span
            class="page-header__count"
            :aria-label="`${activeCount} of ${agents.length} agents active`"
          >
            <span class="page-header__count-val">{{ activeCount }}/{{ agents.length }}</span>
            <span class="page-header__count-label">Active</span>
          </span>
          <span class="page-header__divider" aria-hidden="true"></span>
          <span
            class="page-header__live-dot"
            aria-hidden="true"
          ></span>
          <span class="page-header__time" aria-label="Current time">{{ liveTime }}</span>
        </div>
      </div>
    </header>

    <!-- ── Page body ────────────────────────────────────────────────── -->
    <div class="page__body">

      <!-- ── Section 1: Agent roster 2×2 grid ─────────────────────── -->
      <section aria-labelledby="roster-heading">
        <h2 class="section-heading" id="roster-heading">Agent Roster</h2>
        <div class="agent-grid" role="list" aria-label="Agent roster">
          <article
            v-for="agent in agents"
            :key="agent.id"
            class="agent-card"
            :class="`agent-card--${agent.status}`"
            role="listitem"
            :aria-label="`${agent.name}: ${agent.status}, uptime ${agent.uptime}, ${agent.neutralized} threats neutralized`"
          >
            <!-- Card header row: icon + name + status badge + toggle -->
            <div class="agent-card__top">
              <div class="agent-card__identity">
                <span class="agent-card__icon" aria-hidden="true">{{ agent.icon }}</span>
                <div class="agent-card__name-wrap">
                  <span class="agent-card__name">{{ agent.name }}</span>
                  <span class="agent-card__role">{{ agent.role }}</span>
                </div>
              </div>
              <div class="agent-card__controls">
                <span
                  class="status-badge"
                  :class="`status-badge--${agent.status}`"
                >{{ agent.status.toUpperCase() }}</span>
                <span
                  class="status-dot"
                  :class="[`status-dot--${agent.status}`, { 'status-dot--pulse': agent.status === 'active' }]"
                  aria-hidden="true"
                ></span>
              </div>
            </div>

            <div class="agent-card__divider" aria-hidden="true"></div>

            <!-- Stats row: uptime | neutralized | last seen -->
            <div class="agent-card__stats" role="list" :aria-label="`${agent.name} statistics`">
              <div class="agent-stat" role="listitem">
                <span
                  class="agent-stat__val"
                  :class="`stat-val--${agent.status}`"
                  :aria-label="`Uptime ${agent.uptime}`"
                >{{ agent.uptime }}</span>
                <span class="agent-stat__label">Uptime</span>
              </div>
              <div class="agent-stat-divider" aria-hidden="true"></div>
              <div class="agent-stat" role="listitem">
                <span
                  class="agent-stat__val"
                  :class="`stat-val--${agent.status}`"
                  :aria-label="`${agent.neutralized} threats neutralized`"
                >{{ agent.neutralized }}</span>
                <span class="agent-stat__label">Neutralized</span>
              </div>
              <div class="agent-stat-divider" aria-hidden="true"></div>
              <div class="agent-stat" role="listitem">
                <span
                  class="agent-stat__val stat-val--ts"
                  :aria-label="`Last action ${agent.lastActionAt}`"
                >{{ agent.lastActionAt }}</span>
                <span class="agent-stat__label">Last Action</span>
              </div>
            </div>

            <div class="agent-card__divider" aria-hidden="true"></div>

            <!-- Sparkline SVG -->
            <div class="agent-card__sparkline-wrap">
              <svg
                class="sparkline"
                viewBox="0 0 120 40"
                aria-hidden="true"
                preserveAspectRatio="none"
              >
                <defs>
                  <linearGradient :id="`grad-${agent.id}`" x1="0" x2="0" y1="0" y2="1">
                    <stop
                      offset="0%"
                      :stop-color="statusToken(agent.status)"
                      stop-opacity="0.28"
                    />
                    <stop
                      offset="100%"
                      :stop-color="statusToken(agent.status)"
                      stop-opacity="0"
                    />
                  </linearGradient>
                </defs>
                <path
                  :d="sparklineAreaPath(agent.sparkline)"
                  :fill="`url(#grad-${agent.id})`"
                />
                <path
                  :d="sparklinePath(agent.sparkline)"
                  class="sparkline__line"
                  :class="`sparkline__line--${agent.status}`"
                  fill="none"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              <span class="sparkline-label">24h activity</span>
            </div>

            <div class="agent-card__divider" aria-hidden="true"></div>

            <!-- Last action text -->
            <p class="agent-card__last-action">{{ agent.lastAction }}</p>
          </article>
        </div>
      </section>

      <!-- ── Lower row: metrics | deployment controls ───────────────── -->
      <div class="lower-row">

        <!-- Section 2: Performance Metrics -->
        <section class="card" aria-labelledby="metrics-heading">
          <div class="card__header">
            <h2 class="card__title" id="metrics-heading">Performance Metrics</h2>
          </div>
          <div class="card__body">
            <table
              class="metrics-table"
              role="table"
              aria-label="Agent performance metrics"
            >
              <thead>
                <tr>
                  <th scope="col" class="metrics-th">Agent</th>
                  <th scope="col" class="metrics-th metrics-th--num">Response</th>
                  <th scope="col" class="metrics-th metrics-th--num">FP Rate</th>
                  <th scope="col" class="metrics-th metrics-th--bar">Coverage</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="agent in agents"
                  :key="agent.id"
                  class="metrics-row"
                  :class="`metrics-row--${agent.status}`"
                  :aria-label="`${agent.name}: ${agent.responseTime}ms response, ${(agent.falsePositiveRate * 100).toFixed(1)}% false positives, ${agent.coverage}% coverage`"
                >
                  <th scope="row" class="metrics-agent-name">
                    <span
                      class="metrics-dot"
                      :class="`metrics-dot--${agent.status}`"
                      aria-hidden="true"
                    ></span>
                    {{ agent.name }}
                  </th>
                  <td class="metrics-val" :class="`metrics-val--${agent.status}`">
                    {{ agent.responseTime }}ms
                  </td>
                  <td class="metrics-val" :class="`metrics-val--${agent.status}`">
                    {{ (agent.falsePositiveRate * 100).toFixed(1) }}%
                  </td>
                  <td class="metrics-coverage-cell">
                    <div class="coverage-bar-track">
                      <div
                        class="coverage-bar-fill"
                        :class="`coverage-bar--${agent.status}`"
                        :style="{ width: agent.coverage + '%' }"
                        role="presentation"
                      ></div>
                    </div>
                    <span
                      class="coverage-pct"
                      :class="`metrics-val--${agent.status}`"
                    >{{ agent.coverage }}%</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Section 3: Deployment Controls -->
        <section class="card" aria-labelledby="controls-heading">
          <div class="card__header">
            <h2 class="card__title" id="controls-heading">Deployment Controls</h2>
          </div>
          <div class="card__body">
            <ul class="control-list" role="list" aria-label="Agent deployment toggles">
              <li
                v-for="agent in agents"
                :key="agent.id"
                class="control-row"
                role="listitem"
              >
                <div class="control-row__info">
                  <span class="control-agent-name">{{ agent.name }}</span>
                  <span class="control-agent-role">{{ agent.role }}</span>
                </div>
                <button
                  type="button"
                  role="switch"
                  :aria-checked="agent.active"
                  :aria-label="`${agent.active ? 'Deactivate' : 'Activate'} ${agent.name} agent`"
                  class="agent-toggle"
                  :class="{ 'agent-toggle--on': agent.active }"
                  @click="toggleAgent(agent)"
                >
                  <span class="agent-toggle__track" aria-hidden="true">
                    <span class="agent-toggle__thumb"></span>
                  </span>
                  <span class="agent-toggle__label">{{ agent.active ? 'Active' : 'Standby' }}</span>
                </button>
              </li>
            </ul>

            <!-- Config summary -->
            <div class="config-summary" aria-label="System configuration summary">
              <h3 class="config-summary__title">System Config</h3>
              <dl class="config-grid">
                <div
                  v-for="item in configSummary"
                  :key="item.label"
                  class="config-item"
                >
                  <dt class="config-item__label">{{ item.label }}</dt>
                  <dd class="config-item__value">{{ item.value }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </section>

      </div><!-- /lower-row -->

      <!-- ── Section 4: Activity Log ──────────────────────────────── -->
      <section class="card activity-section" aria-labelledby="activity-heading">
        <div class="card__header activity-header">
          <h2 class="card__title" id="activity-heading">Activity Log</h2>
          <div
            class="filter-group"
            role="group"
            aria-label="Filter activity by type"
          >
            <button
              v-for="f in filters"
              :key="f.value"
              type="button"
              class="filter-chip"
              :class="{ 'filter-chip--active': activeFilter === f.value }"
              :aria-pressed="activeFilter === f.value"
              @click="activeFilter = f.value"
            >{{ f.label }}</button>
          </div>
        </div>

        <ul
          class="activity-list"
          role="list"
          aria-label="Agent activity feed"
          aria-live="polite"
        >
          <li
            v-for="(entry, index) in filteredLog"
            :key="entry.id"
            class="activity-entry"
            :style="{ '--entry-index': index }"
            :aria-label="`${agentName(entry.agentId)}: ${entry.message}, ${entry.at}`"
          >
            <span
              class="log-dot"
              :class="logTypeToken(entry.type)"
              aria-hidden="true"
            ></span>
            <span
              class="activity-entry__agent"
              :class="`entry-agent--${entry.agentId}`"
            >{{ agentName(entry.agentId) }}</span>
            <span class="activity-entry__message">{{ entry.message }}</span>
            <span class="activity-entry__ts">{{ entry.at }}</span>
          </li>
        </ul>
      </section>

    </div><!-- /page__body -->
  </div><!-- /page -->
</template>

<style scoped>
/* ── Reset ──────────────────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* ── Page root ──────────────────────────────────────────────────────── */
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  overflow-x: hidden;
  opacity: 0;
  transition: opacity var(--duration-normal) var(--easing);
}

.page.is-mounted {
  opacity: 1;
}

/* ── Screen-reader only ─────────────────────────────────────────────── */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: calc(var(--space-unit) * -0.5);
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* ── Page header ────────────────────────────────────────────────────── */
.page-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
  box-shadow: var(--shadow-md);
  padding: 0 calc(var(--space-unit) * 8);
}

.page-header__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  height: calc(var(--space-unit) * 14);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 4);
}

.page-header__left {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.page-header__brand {
  font-family: var(--font-mono);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
}

.page-header__sep {
  color: var(--brand-border);
  font-size: 1.25rem;
}

.page-header__title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  color: var(--brand-text);
}

.page-header__right {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.page-header__count {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: calc(var(--space-unit) * 0.5);
}

.page-header__count-val {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  color: var(--brand-primary);
  line-height: 1;
}

.page-header__count-label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.page-header__divider {
  width: 1px;
  height: calc(var(--space-unit) * 6);
  background-color: var(--brand-border);
}

.page-header__live-dot {
  width: calc(var(--space-unit) * 1.5);
  height: calc(var(--space-unit) * 1.5);
  border-radius: 50%;
  background-color: var(--brand-error);
  animation: pulse 1.5s var(--easing) infinite;
}

.page-header__time {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--brand-muted);
}

@media (max-width: 768px) {
  .page-header {
    padding: 0 calc(var(--space-unit) * 4);
  }
  .page-header__inner {
    height: auto;
    flex-wrap: wrap;
    padding: calc(var(--space-unit) * 3) 0;
    gap: calc(var(--space-unit) * 2);
  }
  .page-header__time {
    display: none;
  }
}

/* ── Page body ──────────────────────────────────────────────────────── */
.page__body {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 8);
  max-width: var(--container-max);
  width: 100%;
  margin: 0 auto;
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 8);
}

@media (max-width: 768px) {
  .page__body {
    padding: calc(var(--space-unit) * 4);
    gap: calc(var(--space-unit) * 6);
  }
}

/* ── Section heading ────────────────────────────────────────────────── */
.section-heading {
  font-family: var(--font-heading);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin: 0 0 calc(var(--space-unit) * 4);
}

/* ── Agent grid ─────────────────────────────────────────────────────── */
.agent-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: calc(var(--space-unit) * 6);
}

@media (max-width: 768px) {
  .agent-grid {
    grid-template-columns: 1fr;
  }
}

/* ── Agent card base ────────────────────────────────────────────────── */
.agent-card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 5);
  display: flex;
  flex-direction: column;
  gap: 0;
  transition:
    box-shadow var(--duration-normal) var(--easing),
    border-color var(--duration-normal) var(--easing);
}

/* Active: enhanced white glow — no hardcoded rgba */
.agent-card--active {
  border-color: color-mix(in srgb, var(--brand-primary) 40%, transparent);
  background: linear-gradient(145deg, color-mix(in srgb, var(--brand-primary) 5%, var(--brand-surface)), var(--brand-surface));
  box-shadow:
    0 0 0 1px var(--brand-primary),
    0 0 20px color-mix(in srgb, var(--brand-primary) 30%, transparent),
    0 0 40px color-mix(in srgb, var(--brand-primary) 15%, transparent);
}

/* Standby: blue tint */
.agent-card--standby {
  border-color: color-mix(in srgb, var(--brand-secondary) 35%, transparent);
}

/* Offline: red tint, text dimmed */
.agent-card--offline {
  border-color: color-mix(in srgb, var(--brand-error) 30%, transparent);
}

.agent-card--offline .agent-card__name {
  color: color-mix(in srgb, var(--brand-text) 55%, transparent);
}

.agent-card--offline .agent-card__role {
  color: color-mix(in srgb, var(--brand-muted) 70%, transparent);
}

.agent-card--offline .agent-card__last-action {
  color: color-mix(in srgb, var(--brand-text) 45%, transparent);
}

/* ── Card top row ───────────────────────────────────────────────────── */
.agent-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 3);
  padding-bottom: calc(var(--space-unit) * 4);
}

.agent-card__identity {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 3);
  flex: 1;
  min-width: 0;
}

.agent-card__icon {
  font-size: 1.5rem;
  line-height: 1;
  flex-shrink: 0;
  margin-top: calc(var(--space-unit) * 0.5);
}

.agent-card__name-wrap {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
  min-width: 0;
}

.agent-card__name {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--brand-text);
  line-height: 1.2;
}

.agent-card__role {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
}

.agent-card__controls {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  flex-shrink: 0;
}

/* ── Status badge ───────────────────────────────────────────────────── */
.status-badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
}

.status-badge--active  { background-color: var(--brand-primary);   }
.status-badge--standby { background-color: var(--brand-secondary); }
.status-badge--offline { background-color: var(--brand-error);     }

/* ── Status dot ─────────────────────────────────────────────────────── */
.status-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
  transition: background-color var(--duration-normal) var(--easing);
}

.status-dot--active  { background-color: var(--brand-primary);   }
.status-dot--standby { background-color: var(--brand-secondary); }
.status-dot--offline { background-color: var(--brand-error);     }

.status-dot--pulse {
  animation: pulse 2s var(--easing) infinite;
}

/* ── Card divider ───────────────────────────────────────────────────── */
.agent-card__divider {
  height: 1px;
  background-color: var(--brand-border);
  margin: 0 calc(var(--space-unit) * -5);
}

/* ── Stats row ──────────────────────────────────────────────────────── */
.agent-card__stats {
  display: flex;
  align-items: center;
  padding: calc(var(--space-unit) * 4) 0;
  gap: 0;
}

.agent-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  flex: 1;
}

.agent-stat-divider {
  width: 1px;
  height: calc(var(--space-unit) * 7);
  background-color: var(--brand-border);
  flex-shrink: 0;
}

.agent-stat__val {
  font-family: var(--font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1;
}

.stat-val--active  { color: var(--brand-primary);   }
.stat-val--standby { color: var(--brand-secondary); }
.stat-val--offline { color: var(--brand-error);     }
.stat-val--ts      { color: color-mix(in srgb, var(--brand-text) 70%, transparent); font-size: 0.9375rem; }

.agent-stat__label {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── Sparkline ──────────────────────────────────────────────────────── */
.agent-card__sparkline-wrap {
  padding: calc(var(--space-unit) * 4) 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1.5);
}

.sparkline {
  width: 100%;
  height: calc(var(--space-unit) * 10);
  display: block;
}

.sparkline__line--active  { stroke: var(--brand-primary);   }
.sparkline__line--standby { stroke: var(--brand-secondary); }
.sparkline__line--offline { stroke: color-mix(in srgb, var(--brand-error) 60%, transparent); }

.sparkline-label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── Last action text ───────────────────────────────────────────────── */
.agent-card__last-action {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  line-height: 1.5;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  margin: 0;
  padding-top: calc(var(--space-unit) * 3);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ── Lower row ──────────────────────────────────────────────────────── */
.lower-row {
  display: grid;
  grid-template-columns: 55fr 45fr;
  gap: calc(var(--space-unit) * 6);
}

@media (max-width: 768px) {
  .lower-row {
    grid-template-columns: 1fr;
  }
}

/* ── Card base ──────────────────────────────────────────────────────── */
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
  flex-wrap: wrap;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  background-color: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
}

.card__title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: var(--brand-text);
  margin: 0;
}

.card__body {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
}

/* ── Metrics table ──────────────────────────────────────────────────── */
.metrics-table {
  width: 100%;
  border-collapse: collapse;
}

.metrics-th {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
  padding: 0 0 calc(var(--space-unit) * 3);
  text-align: left;
  border-bottom: 1px solid var(--brand-border);
}

.metrics-th--num {
  text-align: right;
}

.metrics-th--bar {
  text-align: right;
  min-width: calc(var(--space-unit) * 24);
}

.metrics-row {
  border-bottom: 1px solid color-mix(in srgb, var(--brand-border) 60%, transparent);
}

.metrics-row:last-child {
  border-bottom: none;
}

.metrics-agent-name {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
  padding: calc(var(--space-unit) * 3) 0;
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  text-align: left;
}

.metrics-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  flex-shrink: 0;
}

.metrics-dot--active  { background-color: var(--brand-primary);   }
.metrics-dot--standby { background-color: var(--brand-secondary); }
.metrics-dot--offline { background-color: var(--brand-error);     }

.metrics-val {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  text-align: right;
  padding: calc(var(--space-unit) * 3) 0 calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
}

.metrics-val--active  { color: var(--brand-primary);   }
.metrics-val--standby { color: var(--brand-secondary); }
.metrics-val--offline { color: var(--brand-error);     }

.metrics-coverage-cell {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) 0 calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
}

.coverage-bar-track {
  flex: 1;
  height: calc(var(--space-unit) * 1.5);
  background-color: color-mix(in srgb, var(--brand-border) 60%, transparent);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.coverage-bar-fill {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--duration-slow) var(--easing);
}

.coverage-bar--active  { background-color: var(--brand-primary);   }
.coverage-bar--standby { background-color: var(--brand-secondary); }
.coverage-bar--offline { background-color: var(--brand-error);     }

.coverage-pct {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Deployment controls ────────────────────────────────────────────── */
.control-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.control-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 4) 0;
  border-bottom: 1px solid color-mix(in srgb, var(--brand-border) 60%, transparent);
}

.control-row:last-child {
  border-bottom: none;
}

.control-row__info {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
  flex: 1;
  min-width: 0;
}

.control-agent-name {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  color: var(--brand-text);
}

.control-agent-role {
  font-family: var(--font-body);
  font-size: 0.75rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
}

/* ── Agent toggle ───────────────────────────────────────────────────── */
.agent-toggle {
  display: inline-flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  background: none;
  border: none;
  cursor: pointer;
  padding: calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-text);
  font-family: var(--font-body);
  flex-shrink: 0;
  transition: background-color var(--duration-fast) var(--easing);
}

.agent-toggle:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.agent-toggle:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 60%, var(--brand-bg-secondary));
}

.agent-toggle__track {
  width: calc(var(--space-unit) * 10);
  height: calc(var(--space-unit) * 6);
  border-radius: calc(var(--space-unit) * 3);
  background-color: var(--brand-muted);
  position: relative;
  flex-shrink: 0;
  border: 1px solid transparent;
  transition:
    background-color var(--duration-normal) var(--easing),
    border-color var(--duration-normal) var(--easing);
}

.agent-toggle--on .agent-toggle__track {
  background-color: color-mix(in srgb, var(--brand-primary) 20%, transparent);
  border-color: var(--brand-primary);
}

.agent-toggle__thumb {
  position: absolute;
  top: calc(var(--space-unit) * 0.75);
  left: calc(var(--space-unit) * 0.75);
  width: calc(var(--space-unit) * 4);
  height: calc(var(--space-unit) * 4);
  border-radius: 50%;
  background-color: var(--brand-primary);
  transition: transform var(--duration-normal) var(--easing);
}

.agent-toggle--on .agent-toggle__thumb {
  transform: translateX(calc(var(--space-unit) * 4));
}

.agent-toggle__label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
  transition: color var(--duration-normal) var(--easing);
  min-width: calc(var(--space-unit) * 12);
}

.agent-toggle--on .agent-toggle__label {
  color: var(--brand-primary);
}

/* ── Config summary ─────────────────────────────────────────────────── */
.config-summary {
  margin-top: calc(var(--space-unit) * 4);
  padding-top: calc(var(--space-unit) * 4);
  border-top: 1px solid var(--brand-border);
}

.config-summary__title {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin: 0 0 calc(var(--space-unit) * 3);
}

.config-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  margin: 0;
}

.config-item {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.config-item__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.config-item__value {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-text);
  margin: 0;
}

/* ── Activity log ───────────────────────────────────────────────────── */
.activity-section {
  /* inherits .card */
}

.activity-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: calc(var(--space-unit) * 3);
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: calc(var(--space-unit) * 2);
}

.filter-chip {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
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
  color: var(--brand-text);
}

.filter-chip--active {
  background-color: var(--brand-primary);
  color: var(--brand-bg);
  border-color: var(--brand-primary);
}

.activity-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.activity-entry {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 2.5) auto 1fr auto;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 6);
  border-bottom: 1px solid color-mix(in srgb, var(--brand-border) 50%, transparent);
  animation: entry-slide-in var(--duration-normal) var(--easing) both;
  animation-delay: calc(var(--entry-index, 0) * 25ms);
}

.activity-entry:last-child {
  border-bottom: none;
}

.log-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.log-dot--detection { background-color: var(--brand-error);     }
.log-dot--response  { background-color: var(--brand-secondary); }
.log-dot--scan      { background-color: var(--brand-accent);    }
.log-dot--config    { background-color: var(--brand-muted);     }

.activity-entry__agent {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  white-space: nowrap;
  flex-shrink: 0;
}

.entry-agent--scanner   { background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);     color: var(--brand-error);     }
.entry-agent--monitor   { background-color: color-mix(in srgb, var(--brand-accent) 15%, transparent);    color: var(--brand-accent);    }
.entry-agent--responder { background-color: color-mix(in srgb, var(--brand-secondary) 15%, transparent); color: var(--brand-secondary); }
.entry-agent--sentinel  { background-color: color-mix(in srgb, var(--brand-primary) 12%, transparent);   color: var(--brand-primary);   }

.activity-entry__message {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.activity-entry__ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Keyframes ──────────────────────────────────────────────────────── */
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.85); }
}

@keyframes entry-slide-in {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Reduced motion ─────────────────────────────────────────────────── */
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

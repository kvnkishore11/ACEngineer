<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/agents/v2-expandable-list-sidebar
// Layout: expandable agent list (main) + sticky metrics/deploy sidebar

// ── Types ────────────────────────────────────────────────────────
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
  agentName: string
  type: 'detection' | 'response' | 'scan' | 'config'
  message: string
  at: string
}

// ── Agent data ───────────────────────────────────────────────────
const agents = reactive<Agent[]>([
  {
    id: 'scanner', name: 'Scanner', role: 'Vulnerability scanning', icon: '⬡',
    status: 'active', active: true, uptime: '99.97%', neutralized: 142,
    lastAction: 'Flagged CVE-2024-4891 on api-gateway-01', lastActionAt: '2s ago',
    sparkline: [12, 18, 15, 22, 31, 28, 45, 38, 52, 47, 61, 55, 48, 63, 71, 58, 44, 67, 72, 69, 81, 76, 88, 83],
    responseTime: 187, falsePositiveRate: 0.02, coverage: 94,
    configEntries: [
      { key: 'Scan depth',       value: 'Deep'       },
      { key: 'Interval',         value: '60s'        },
      { key: 'CVE feed',         value: 'NVD + MITRE' },
      { key: 'Alert threshold',  value: 'HIGH'       },
    ],
  },
  {
    id: 'monitor', name: 'Monitor', role: 'Traffic analysis', icon: '◈',
    status: 'active', active: true, uptime: '99.91%', neutralized: 87,
    lastAction: 'Detected anomalous request pattern on llm-worker-07', lastActionAt: '14s ago',
    sparkline: [8, 12, 19, 14, 23, 28, 33, 41, 36, 44, 38, 51, 47, 55, 49, 62, 57, 64, 71, 68, 74, 78, 72, 81],
    responseTime: 203, falsePositiveRate: 0.035, coverage: 88,
    configEntries: [
      { key: 'Sampling rate',   value: '100%'      },
      { key: 'Baseline window', value: '7d'         },
      { key: 'Sensitivity',     value: 'High'       },
      { key: 'Protocol',        value: 'HTTP/gRPC'  },
    ],
  },
  {
    id: 'responder', name: 'Responder', role: 'Threat containment', icon: '◉',
    status: 'active', active: true, uptime: '99.85%', neutralized: 203,
    lastAction: 'Isolated orchestrator-02 from network segment', lastActionAt: '34s ago',
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
    id: 'sentinel', name: 'Sentinel', role: 'Perimeter watch', icon: '◇',
    status: 'standby', active: false, uptime: '98.40%', neutralized: 56,
    lastAction: 'Completed perimeter sweep — no anomalies', lastActionAt: '4m ago',
    sparkline: [5, 8, 6, 9, 7, 11, 8, 14, 10, 12, 9, 16, 13, 11, 15, 12, 18, 14, 17, 13, 19, 16, 21, 18],
    responseTime: 312, falsePositiveRate: 0.041, coverage: 82,
    configEntries: [
      { key: 'Sweep interval',  value: '5m'          },
      { key: 'Perimeter scope', value: 'All zones'   },
      { key: 'Alert on',        value: 'Unknown IPs' },
      { key: 'Mode',            value: 'Passive'     },
    ],
  },
])

// ── Activity log ─────────────────────────────────────────────────
const activityLog: ActivityEntry[] = [
  { id: 1,  agentId: 'scanner',   agentName: 'Scanner',   type: 'detection', message: 'CVE-2024-4891 flagged on api-gateway-01 — CRITICAL',                   at: '2s ago'  },
  { id: 2,  agentId: 'monitor',   agentName: 'Monitor',   type: 'detection', message: 'Anomalous request pattern on llm-worker-07 — 47 req/s above baseline', at: '14s ago' },
  { id: 3,  agentId: 'responder', agentName: 'Responder', type: 'response',  message: 'Isolated orchestrator-02 from network segment — circuit breaker on',   at: '34s ago' },
  { id: 4,  agentId: 'scanner',   agentName: 'Scanner',   type: 'scan',      message: 'Deep scan completed on fine-tune-03 — 0 new vulnerabilities',           at: '2m ago'  },
  { id: 5,  agentId: 'monitor',   agentName: 'Monitor',   type: 'scan',      message: 'Baseline recalculated for api-gateway cluster — 7d window',             at: '4m ago'  },
  { id: 6,  agentId: 'sentinel',  agentName: 'Sentinel',  type: 'scan',      message: 'Perimeter sweep complete — no anomalies detected',                      at: '4m ago'  },
  { id: 7,  agentId: 'responder', agentName: 'Responder', type: 'response',  message: 'Token #7f3a revoked — privilege escalation attempt blocked',            at: '8m ago'  },
  { id: 8,  agentId: 'scanner',   agentName: 'Scanner',   type: 'detection', message: 'CVE-2024-4887 flagged on llm-worker-02 — HIGH severity',                at: '11m ago' },
  { id: 9,  agentId: 'monitor',   agentName: 'Monitor',   type: 'config',    message: 'Sensitivity threshold updated: MEDIUM → HIGH — auto-adjusted',          at: '18m ago' },
  { id: 10, agentId: 'scanner',   agentName: 'Scanner',   type: 'config',    message: 'CVE feed refreshed — 14 new entries from NVD',                          at: '22m ago' },
  { id: 11, agentId: 'responder', agentName: 'Responder', type: 'response',  message: 'Containment lifted on fine-tune-03 — cleared and restored',             at: '31m ago' },
  { id: 12, agentId: 'sentinel',  agentName: 'Sentinel',  type: 'scan',      message: 'Perimeter sweep #47 initiated — covering 12 zones',                    at: '35m ago' },
]

// ── Row expand state ─────────────────────────────────────────────
const openRows = reactive<Record<string, boolean>>({
  scanner: true, monitor: false, responder: false, sentinel: false,
})

function toggleRow(id: string) {
  openRows[id] = !openRows[id]
}

// ── Deploy toggle ────────────────────────────────────────────────
function toggleAgent(id: string) {
  const agent = agents.find(a => a.id === id)
  if (!agent) return
  agent.active = !agent.active
  agent.status = agent.active ? 'active' : 'standby'
}

// ── Activity filter ──────────────────────────────────────────────
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

// ── Derived from log per agent (last 3) ──────────────────────────
function agentRecentActions(agentId: string): ActivityEntry[] {
  return activityLog.filter(e => e.agentId === agentId).slice(0, 3)
}

// ── Metrics helpers ──────────────────────────────────────────────
const maxResponseTime = computed(() => Math.max(...agents.map(a => a.responseTime)))

function fprColorClass(rate: number): string {
  if (rate < 0.02) return 'fpr--good'
  if (rate <= 0.04) return 'fpr--mid'
  return 'fpr--high'
}

// ── Sparkline ────────────────────────────────────────────────────
function sparklinePoints(data: number[]): string {
  const maxVal = Math.max(...data)
  const minVal = Math.min(...data)
  const range = maxVal - minVal || 1
  return data.map((v, i) => {
    const x = (i / (data.length - 1)) * 120
    const y = 40 - ((v - minVal) / range) * 36 + 2
    return `${x.toFixed(1)},${y.toFixed(1)}`
  }).join(' ')
}

// ── Mount ────────────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  nextTick(() => { isMounted.value = true })
})

onUnmounted(() => {
  // no intervals used — defensive hook present
})
</script>

<template>
  <div class="page" :class="{ 'is-mounted': isMounted }" aria-label="Aegis Agent Management — Expandable List View">
    <h1 class="sr-only">Aegis Agent Management</h1>

    <!-- ── Page header ─────────────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Agent management page header">
      <div class="page-header__inner">
        <div class="page-header__brand">
          <span class="brand-word">AEGIS</span>
          <span class="brand-sep" aria-hidden="true">/</span>
          <span class="brand-sub">Agent Management</span>
        </div>
        <div class="page-header__stats" aria-label="Agent status summary">
          <span class="hdr-stat">
            <span class="hdr-stat__dot hdr-stat__dot--active" aria-hidden="true"></span>
            <span class="hdr-stat__val">{{ agents.filter(a => a.status === 'active').length }}</span>
            <span class="hdr-stat__lbl">Active</span>
          </span>
          <span class="hdr-sep" aria-hidden="true"></span>
          <span class="hdr-stat">
            <span class="hdr-stat__dot hdr-stat__dot--standby" aria-hidden="true"></span>
            <span class="hdr-stat__val">{{ agents.filter(a => a.status === 'standby').length }}</span>
            <span class="hdr-stat__lbl">Standby</span>
          </span>
          <span class="hdr-sep" aria-hidden="true"></span>
          <span class="hdr-stat">
            <span class="hdr-stat__dot hdr-stat__dot--offline" aria-hidden="true"></span>
            <span class="hdr-stat__val">{{ agents.filter(a => a.status === 'offline').length }}</span>
            <span class="hdr-stat__lbl">Offline</span>
          </span>
        </div>
      </div>
    </header>

    <!-- ── Body grid ───────────────────────────────────────────── -->
    <main class="page-body">
      <div class="body-grid">

        <!-- ── Main column ───────────────────────────────────── -->
        <div class="main-col">

          <!-- Agent List -->
          <section class="card section-agents" aria-labelledby="agents-heading">
            <div class="card__header">
              <h2 class="card__title" id="agents-heading">Agent Roster</h2>
              <span class="card__meta">{{ agents.length }} agents — click row to expand</span>
            </div>

            <div class="agent-list" role="list">
              <div
                v-for="agent in agents"
                :key="agent.id"
                class="agent-row"
                :class="[`agent-row--${agent.status}`, { 'is-open': openRows[agent.id] }]"
                role="listitem"
              >
                <!-- Row trigger -->
                <button
                  type="button"
                  class="agent-row__trigger"
                  :id="`trigger-${agent.id}`"
                  :aria-expanded="openRows[agent.id]"
                  :aria-controls="`detail-${agent.id}`"
                  :aria-label="`${agent.name}: ${agent.status}, ${agent.role}. ${openRows[agent.id] ? 'Collapse' : 'Expand'} for details.`"
                  @click="toggleRow(agent.id)"
                >
                  <span class="row-chevron" aria-hidden="true">›</span>

                  <span class="row-icon" aria-hidden="true">{{ agent.icon }}</span>

                  <span class="row-identity">
                    <span class="row-name" :class="{ 'row-name--offline': agent.status === 'offline' }">
                      {{ agent.name }}
                    </span>
                    <span class="row-role" :class="{ 'row-role--offline': agent.status === 'offline' }">
                      {{ agent.role }}
                    </span>
                  </span>

                  <span class="row-status" aria-hidden="true">
                    <span class="status-dot" :class="`status-dot--${agent.status}`"></span>
                    <span class="status-badge" :class="`status-badge--${agent.status}`">
                      {{ agent.status }}
                    </span>
                  </span>

                  <span class="row-uptime" aria-hidden="true">
                    <span class="row-stat-val">{{ agent.uptime }}</span>
                    <span class="row-stat-lbl">Uptime</span>
                  </span>

                  <span class="row-neutralized" aria-hidden="true">
                    <span class="row-stat-val">{{ agent.neutralized }}</span>
                    <span class="row-stat-lbl">Neutralized</span>
                  </span>

                  <span class="row-ts" aria-hidden="true">{{ agent.lastActionAt }}</span>
                </button>

                <!-- Expandable detail -->
                <div
                  class="agent-row__detail"
                  :id="`detail-${agent.id}`"
                  role="region"
                  :aria-labelledby="`trigger-${agent.id}`"
                >
                  <div class="detail-inner">

                    <!-- Sparkline -->
                    <div class="detail-sparkline">
                      <span class="detail-section-label">Activity — last 24h</span>
                      <svg
                        class="sparkline"
                        viewBox="0 0 120 40"
                        aria-hidden="true"
                        preserveAspectRatio="none"
                      >
                        <polyline
                          class="sparkline__line"
                          :class="`sparkline__line--${agent.status}`"
                          :points="sparklinePoints(agent.sparkline)"
                          fill="none"
                          stroke-width="1.5"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>
                    </div>

                    <!-- Config grid -->
                    <div class="detail-config">
                      <span class="detail-section-label">Configuration</span>
                      <dl class="config-grid">
                        <div
                          v-for="entry in agent.configEntries"
                          :key="entry.key"
                          class="config-entry"
                        >
                          <dt class="config-key">{{ entry.key }}</dt>
                          <dd class="config-val">{{ entry.value }}</dd>
                        </div>
                      </dl>
                    </div>

                    <!-- Last action detail -->
                    <div class="detail-last-action">
                      <span class="detail-section-label">Last action</span>
                      <p class="last-action-text">{{ agent.lastAction }}</p>
                      <span class="last-action-ts">{{ agent.lastActionAt }}</span>
                    </div>

                    <!-- Recent activity -->
                    <div class="detail-recent" v-if="agentRecentActions(agent.id).length">
                      <span class="detail-section-label">Recent activity</span>
                      <ul class="recent-list" aria-label="Recent activity for this agent">
                        <li
                          v-for="entry in agentRecentActions(agent.id)"
                          :key="entry.id"
                          class="recent-entry"
                          :class="`recent-entry--${entry.type}`"
                        >
                          <span class="recent-type">{{ entry.type }}</span>
                          <span class="recent-msg">{{ entry.message }}</span>
                          <span class="recent-ts">{{ entry.at }}</span>
                        </li>
                      </ul>
                    </div>

                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Activity Log -->
          <section class="card section-activity" aria-labelledby="activity-heading">
            <div class="card__header">
              <h2 class="card__title" id="activity-heading">Activity Log</h2>
              <span class="card__meta">{{ filteredLog.length }} entries</span>
            </div>

            <div class="activity-body">
              <!-- Filter chips -->
              <div
                role="group"
                aria-label="Filter activity by type"
                class="filter-group"
              >
                <button
                  v-for="f in activityFilters"
                  :key="f.value"
                  type="button"
                  class="filter-chip"
                  :class="{ 'filter-chip--active': activeFilter === f.value }"
                  :aria-pressed="activeFilter === f.value"
                  @click="setFilter(f.value)"
                >
                  {{ f.label }}
                </button>
              </div>

              <!-- Entries -->
              <ul class="activity-list" aria-label="Activity log entries">
                <li
                  v-for="entry in filteredLog"
                  :key="entry.id"
                  class="activity-entry"
                  :class="`activity-entry--${entry.type}`"
                  :aria-label="`${entry.agentName}: ${entry.message}, ${entry.at}`"
                >
                  <span class="entry-type-badge" :class="`entry-type-badge--${entry.type}`">
                    {{ entry.type }}
                  </span>
                  <div class="entry-body">
                    <span class="entry-agent">{{ entry.agentName }}</span>
                    <span class="entry-msg">{{ entry.message }}</span>
                  </div>
                  <span class="entry-ts">{{ entry.at }}</span>
                </li>
              </ul>

              <p v-if="filteredLog.length === 0" class="activity-empty">
                No entries matching the current filter.
              </p>
            </div>
          </section>

        </div><!-- /main-col -->

        <!-- ── Sidebar ────────────────────────────────────────── -->
        <aside class="sidebar" aria-label="Performance metrics and deployment controls">

          <!-- Response Times -->
          <section class="card sidebar-card" aria-labelledby="rt-heading">
            <div class="card__header">
              <h2 class="card__title card__title--sm" id="rt-heading">Response Times</h2>
            </div>
            <div class="metric-body">
              <ul class="metric-list" aria-label="Agent response times in milliseconds">
                <li
                  v-for="agent in agents"
                  :key="agent.id"
                  class="metric-row"
                  :aria-label="`${agent.name}: ${agent.responseTime} milliseconds`"
                >
                  <span class="metric-label" :class="{ 'metric-label--offline': agent.status === 'offline' }">
                    {{ agent.name }}
                  </span>
                  <div class="metric-bar-wrap" aria-hidden="true">
                    <div
                      class="metric-bar"
                      :class="`metric-bar--${agent.status}`"
                      :style="{ width: `${(agent.responseTime / maxResponseTime) * 100}%` }"
                    ></div>
                  </div>
                  <span class="metric-val" :class="`metric-val--${agent.status}`">
                    {{ agent.responseTime }}<span class="metric-unit">ms</span>
                  </span>
                </li>
              </ul>
            </div>
          </section>

          <!-- False Positive Rate -->
          <section class="card sidebar-card" aria-labelledby="fpr-heading">
            <div class="card__header">
              <h2 class="card__title card__title--sm" id="fpr-heading">False Positive Rate</h2>
            </div>
            <div class="metric-body">
              <ul class="metric-list" aria-label="Agent false positive rates">
                <li
                  v-for="agent in agents"
                  :key="agent.id"
                  class="metric-row"
                  :aria-label="`${agent.name}: ${(agent.falsePositiveRate * 100).toFixed(1)}% false positive rate`"
                >
                  <span class="metric-label" :class="{ 'metric-label--offline': agent.status === 'offline' }">
                    {{ agent.name }}
                  </span>
                  <span
                    class="fpr-val"
                    :class="fprColorClass(agent.falsePositiveRate)"
                  >
                    {{ (agent.falsePositiveRate * 100).toFixed(1) }}%
                  </span>
                </li>
              </ul>
            </div>
          </section>

          <!-- Coverage -->
          <section class="card sidebar-card" aria-labelledby="cov-heading">
            <div class="card__header">
              <h2 class="card__title card__title--sm" id="cov-heading">Coverage</h2>
            </div>
            <div class="metric-body">
              <ul class="metric-list" aria-label="Agent coverage percentages">
                <li
                  v-for="agent in agents"
                  :key="agent.id"
                  class="metric-row"
                  :aria-label="`${agent.name}: ${agent.coverage}% coverage`"
                >
                  <span class="metric-label" :class="{ 'metric-label--offline': agent.status === 'offline' }">
                    {{ agent.name }}
                  </span>
                  <div class="metric-bar-wrap" aria-hidden="true">
                    <div
                      class="metric-bar"
                      :class="`metric-bar--${agent.status}`"
                      :style="{ width: `${agent.coverage}%` }"
                    ></div>
                  </div>
                  <span class="metric-val" :class="`metric-val--${agent.status}`">
                    {{ agent.coverage }}<span class="metric-unit">%</span>
                  </span>
                </li>
              </ul>
            </div>
          </section>

          <!-- Deployment Controls -->
          <section class="card sidebar-card" aria-labelledby="deploy-heading">
            <div class="card__header">
              <h2 class="card__title card__title--sm" id="deploy-heading">Deployment</h2>
            </div>
            <div class="deploy-body">
              <ul class="deploy-list" aria-label="Agent deployment controls">
                <li
                  v-for="agent in agents"
                  :key="agent.id"
                  class="deploy-row"
                >
                  <button
                    type="button"
                    class="agent-toggle"
                    role="switch"
                    :aria-checked="agent.active"
                    :aria-label="`${agent.active ? 'Deactivate' : 'Activate'} ${agent.name}`"
                    @click="toggleAgent(agent.id)"
                  >
                    <span class="agent-toggle__track" aria-hidden="true">
                      <span class="agent-toggle__thumb"></span>
                    </span>
                    <span class="agent-toggle__label">{{ agent.name }}</span>
                    <span class="agent-toggle__status">
                      {{ agent.active ? 'Active' : 'Standby' }}
                    </span>
                  </button>
                </li>
              </ul>
            </div>
          </section>

        </aside><!-- /sidebar -->

      </div><!-- /body-grid -->
    </main>
  </div>
</template>

<style scoped>
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* ── Root ─────────────────────────────────────────────────────── */
.page {
  min-height: 100vh;
  background-color: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  opacity: 0;
  transition: opacity var(--duration-normal) var(--easing);
}

.page.is-mounted {
  opacity: 1;
}

/* ── SR-only ──────────────────────────────────────────────────── */
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

/* ── Page header ──────────────────────────────────────────────── */
.page-header {
  background: linear-gradient(
    to right,
    var(--brand-bg-secondary),
    color-mix(in srgb, var(--brand-bg-secondary) 85%, var(--brand-surface))
  );
  border-bottom: 1px solid var(--brand-border);
  position: sticky;
  top: 0;
  z-index: 50;
}

.page-header__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 6);
  flex-wrap: wrap;
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
  color: var(--brand-border);
}

.brand-sub {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.page-header__stats {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  margin-left: auto;
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
.hdr-stat__dot--offline { background-color: var(--brand-error);     }

.hdr-stat__val {
  font-family: var(--font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brand-text);
}

.hdr-stat__lbl {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.hdr-sep {
  width: 1px;
  height: calc(var(--space-unit) * 5);
  background-color: var(--brand-border);
  flex-shrink: 0;
}

/* ── Body grid ────────────────────────────────────────────────── */
.page-body {
  flex: 1;
}

.body-grid {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 6);
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: calc(var(--space-unit) * 6);
  align-items: start;
}

/* ── Main column ──────────────────────────────────────────────── */
.main-col {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
  min-width: 0;
}

/* ── Sidebar ──────────────────────────────────────────────────── */
.sidebar {
  position: sticky;
  top: calc(var(--space-unit) * 20);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 4);
}

/* ── Card base ────────────────────────────────────────────────── */
.card {
  background: linear-gradient(135deg, var(--brand-surface) 0%, color-mix(in srgb, var(--brand-surface) 85%, var(--brand-bg)) 100%);
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
  background-color: var(--brand-bg-secondary);
  gap: calc(var(--space-unit) * 2);
  flex-wrap: wrap;
}

.card__title {
  font-family: var(--font-heading);
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--brand-text);
  margin: 0;
}

.card__title--sm {
  font-size: 0.8125rem;
}

.card__meta {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

/* ── Agent list ───────────────────────────────────────────────── */
.agent-list {
  /* no padding — rows are flush */
}

/* ── Agent row ────────────────────────────────────────────────── */
.agent-row {
  border-bottom: 1px solid var(--brand-border);
  border-left: 3px solid var(--brand-border);
  transition: border-left-color var(--duration-normal) var(--easing);
}

.agent-row:last-child {
  border-bottom: none;
}

.agent-row--active  { border-left-color: var(--brand-primary);   }
.agent-row--standby { border-left-color: var(--brand-secondary); }
.agent-row--offline { border-left-color: var(--brand-error);     }

/* Row trigger */
.agent-row__trigger {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6) 1fr auto auto auto auto;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  width: 100%;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
  background: none;
  border: none;
  color: var(--brand-text);
  cursor: pointer;
  text-align: left;
  transition: background-color var(--duration-fast) var(--easing);
}

.agent-row__trigger:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 60%, var(--brand-bg-secondary));
}

.agent-row__trigger:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

.row-chevron {
  font-size: 1.125rem;
  color: var(--brand-muted);
  transition: transform var(--duration-normal) var(--easing);
  display: inline-block;
  line-height: 1;
  justify-self: center;
}

.is-open .row-chevron {
  transform: rotate(90deg);
}

.row-icon {
  font-size: 1.25rem;
  line-height: 1;
  justify-self: center;
}

.row-identity {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
  min-width: 0;
}

.row-name {
  font-family: var(--font-heading);
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--brand-text);
  white-space: nowrap;
  transition: color var(--duration-normal) var(--easing);
}

.row-name--offline {
  color: color-mix(in srgb, var(--brand-text) 55%, transparent);
}

.row-role {
  font-size: 0.6875rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  white-space: nowrap;
  transition: color var(--duration-normal) var(--easing);
}

.row-role--offline {
  color: color-mix(in srgb, var(--brand-text) 40%, transparent);
}

/* Status dot + badge */
.row-status {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  flex-shrink: 0;
}

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

.status-badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
  flex-shrink: 0;
  transition: background-color var(--duration-normal) var(--easing);
}

.status-badge--active  { background-color: var(--brand-primary);   }
.status-badge--standby { background-color: var(--brand-secondary); }
.status-badge--offline { background-color: var(--brand-error);     }

/* Row stat (uptime, neutralized) */
.row-uptime,
.row-neutralized {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: calc(var(--space-unit) * 0.25);
  flex-shrink: 0;
}

.row-stat-val {
  font-family: var(--font-mono);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
  line-height: 1;
}

.row-stat-lbl {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 500;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.row-ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  flex-shrink: 0;
  white-space: nowrap;
}

/* ── Expandable detail ────────────────────────────────────────── */
.agent-row__detail {
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--duration-slow) var(--easing);
}

.is-open .agent-row__detail {
  max-height: 9999px;
}

.detail-inner {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: calc(var(--space-unit) * 5);
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  background-color: color-mix(in srgb, var(--brand-bg-secondary) 60%, var(--brand-surface));
  border-top: 1px solid var(--brand-border);
}

.detail-section-label {
  display: block;
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin-bottom: calc(var(--space-unit) * 2);
}

/* Sparkline */
.detail-sparkline {
  grid-column: 1 / -1;
}

.sparkline {
  display: block;
  width: 100%;
  height: calc(var(--space-unit) * 10);
}

.sparkline__line--active  { stroke: var(--brand-primary);   }
.sparkline__line--standby { stroke: var(--brand-secondary); }
.sparkline__line--offline { stroke: color-mix(in srgb, var(--brand-error) 60%, transparent); }

/* Config grid */
.config-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
  margin: 0;
}

.config-entry {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.config-key {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.config-val {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
}

/* Last action */
.detail-last-action {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.last-action-text {
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--brand-text);
  margin: 0;
}

.last-action-ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
}

/* Recent activity */
.detail-recent {
  grid-column: 1 / -1;
}

.recent-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.recent-entry {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-sm);
  border-left: 2px solid transparent;
}

.recent-entry--detection { border-left-color: var(--brand-error);     }
.recent-entry--response  { border-left-color: var(--brand-secondary); }
.recent-entry--scan      { border-left-color: var(--brand-accent);    }
.recent-entry--config    { border-left-color: var(--brand-muted);     }

.recent-type {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
  flex-shrink: 0;
}

.recent-msg {
  font-size: 0.75rem;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-ts {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);
  flex-shrink: 0;
}

/* ── Activity log ─────────────────────────────────────────────── */
.activity-body {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 4);
}

/* Filter chips */
.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: calc(var(--space-unit) * 2);
}

.filter-chip {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
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

.filter-chip:hover:not(.filter-chip--active) {
  background-color: color-mix(in srgb, var(--brand-surface) 70%, var(--brand-secondary));
  border-color: var(--brand-secondary);
}

.filter-chip--active {
  background-color: var(--brand-primary);
  color: var(--brand-bg);
  border-color: var(--brand-primary);
}

.filter-chip:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* Activity entries */
.activity-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.activity-entry {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  border-left: 3px solid transparent;
  transition: background-color var(--duration-fast) var(--easing);
}

.activity-entry:hover {
  background-color: color-mix(in srgb, var(--brand-bg-secondary) 70%, var(--brand-surface));
}

.activity-entry--detection { border-left-color: var(--brand-error);     }
.activity-entry--response  { border-left-color: var(--brand-secondary); }
.activity-entry--scan      { border-left-color: var(--brand-accent);    }
.activity-entry--config    { border-left-color: var(--brand-muted);     }

.entry-type-badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
  flex-shrink: 0;
}

.entry-type-badge--detection { background-color: var(--brand-error);     }
.entry-type-badge--response  { background-color: var(--brand-secondary); }
.entry-type-badge--scan      { background-color: var(--brand-accent);    }
.entry-type-badge--config    { background-color: var(--brand-muted);     }

.entry-body {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
  min-width: 0;
}

.entry-agent {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--brand-text);
}

.entry-msg {
  font-size: 0.8125rem;
  color: color-mix(in srgb, var(--brand-text) 85%, transparent);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.entry-ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  flex-shrink: 0;
  white-space: nowrap;
}

.activity-empty {
  font-size: 0.875rem;
  color: var(--brand-muted);
  text-align: center;
  padding: calc(var(--space-unit) * 6) 0;
  margin: 0;
}

/* ── Sidebar cards ────────────────────────────────────────────── */
.sidebar-card {
  /* inherits .card */
}

.metric-body {
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
}

.metric-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.metric-row {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 18) 1fr auto;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.metric-label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--brand-text);
  white-space: nowrap;
  transition: color var(--duration-normal) var(--easing);
}

.metric-label--offline {
  color: color-mix(in srgb, var(--brand-text) 45%, transparent);
}

.metric-bar-wrap {
  height: calc(var(--space-unit) * 1.5);
  background-color: color-mix(in srgb, var(--brand-primary) 10%, transparent);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.metric-bar {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--duration-slow) var(--easing);
}

.metric-bar--active  { background-color: var(--brand-primary);   }
.metric-bar--standby { background-color: var(--brand-secondary); }
.metric-bar--offline { background-color: color-mix(in srgb, var(--brand-error) 50%, transparent); }

.metric-val {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  white-space: nowrap;
  line-height: 1;
}

.metric-val--active  { color: var(--brand-primary);   }
.metric-val--standby { color: var(--brand-secondary); }
.metric-val--offline { color: color-mix(in srgb, var(--brand-error) 60%, transparent); }

.metric-unit {
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--brand-muted);
  margin-left: calc(var(--space-unit) * 0.5);
}

/* False positive rate */
.fpr-val {
  font-family: var(--font-mono);
  font-size: 0.9375rem;
  font-weight: 700;
  line-height: 1;
  margin-left: auto;
}

.fpr--good { color: var(--brand-primary);   }
.fpr--mid  { color: var(--brand-secondary); }
.fpr--high { color: var(--brand-accent);    }

/* FPR row override — label + value only */
.metric-row:has(.fpr-val) {
  grid-template-columns: 1fr auto;
}

/* ── Deployment toggles ───────────────────────────────────────── */
.deploy-body {
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
}

.deploy-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.deploy-row {
  /* container */
}

.agent-toggle {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  background: none;
  border: none;
  cursor: pointer;
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-text);
  font-family: var(--font-body);
  width: 100%;
  transition: background-color var(--duration-fast) var(--easing);
}

.agent-toggle:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 60%, var(--brand-bg-secondary));
}

.agent-toggle:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.agent-toggle__track {
  width: calc(var(--space-unit) * 10);
  height: calc(var(--space-unit) * 6);
  border-radius: calc(var(--space-unit) * 3);
  background-color: var(--brand-muted);
  position: relative;
  flex-shrink: 0;
  transition:
    background-color var(--duration-normal) var(--easing),
    border-color var(--duration-normal) var(--easing);
  border: 1px solid transparent;
}

[aria-checked="true"] .agent-toggle__track {
  background-color: color-mix(in srgb, var(--brand-primary) 20%, transparent);
  border-color: var(--brand-primary);
}

.agent-toggle__thumb {
  position: absolute;
  top: calc(var(--space-unit) * 0.75);
  left: calc(var(--space-unit) * 0.75);
  width: calc(var(--space-unit) * 4.5);
  height: calc(var(--space-unit) * 4.5);
  border-radius: 50%;
  background-color: var(--brand-primary);
  transition: transform var(--duration-normal) var(--easing);
}

[aria-checked="true"] .agent-toggle__thumb {
  transform: translateX(calc(var(--space-unit) * 4));
}

.agent-toggle__label {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  flex: 1;
  text-align: left;
  color: var(--brand-text);
}

.agent-toggle__status {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 500;
  color: var(--brand-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  transition: color var(--duration-normal) var(--easing);
}

[aria-checked="true"] .agent-toggle__status {
  color: var(--brand-primary);
}

/* ── Focus baseline ───────────────────────────────────────────── */
:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* ── Responsive ───────────────────────────────────────────────── */
@media (max-width: 768px) {
  .page-header__inner {
    padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
    gap: calc(var(--space-unit) * 3);
  }

  .page-header__stats {
    margin-left: 0;
    gap: calc(var(--space-unit) * 3);
  }

  .body-grid {
    grid-template-columns: 1fr;
    padding: calc(var(--space-unit) * 4);
    gap: calc(var(--space-unit) * 4);
  }

  .sidebar {
    position: static;
  }

  .agent-row__trigger {
    grid-template-columns: calc(var(--space-unit) * 4) calc(var(--space-unit) * 5) 1fr auto;
    padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  }

  /* Hide uptime, neutralized, timestamp on mobile — identity + status sufficient */
  .row-uptime,
  .row-neutralized,
  .row-ts {
    display: none;
  }

  .detail-inner {
    grid-template-columns: 1fr;
    padding: calc(var(--space-unit) * 4);
  }

  .detail-sparkline {
    grid-column: 1;
  }

  .detail-recent {
    grid-column: 1;
  }

  .metric-row {
    grid-template-columns: calc(var(--space-unit) * 14) 1fr auto;
  }
}

/* ── Reduced-motion ───────────────────────────────────────────── */
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

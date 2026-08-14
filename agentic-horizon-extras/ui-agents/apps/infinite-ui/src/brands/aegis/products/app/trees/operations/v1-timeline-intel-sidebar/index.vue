<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/operations/v1-timeline-intel-sidebar
// Layout: 60/40 grid — timeline-centric main column, sticky intel + containment sidebar

// ── Types ─────────────────────────────────────────────────────────
interface TimelineNode {
  id: number
  stage: 'DETECTION' | 'INVESTIGATION' | 'CONTAINMENT' | 'RESOLUTION'
  agent: string
  action: string
  timestamp: string
  duration?: string
  active?: boolean
}

interface AttackPattern {
  name: string
  count: number
  pct: number
  stage: 'DETECTION' | 'INVESTIGATION' | 'CONTAINMENT' | 'RESOLUTION'
}

interface RiskSystem {
  name: string
  score: number
  status: 'critical' | 'high' | 'medium' | 'low' | 'secured'
}

interface Vuln {
  id: string
  name: string
  score: number
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  affectedSystems: number
  detectedAt: string
  status: 'OPEN' | 'IN_PROGRESS' | 'PATCHED' | 'MITIGATED'
}

interface ContainedSystem {
  name: string
  isolatedAt: string
  reason: string
  status: 'ISOLATED' | 'MONITORING' | 'CLEARED'
}

interface RespondingAgent {
  name: string
  task: string
  since: string
  status: 'active' | 'idle'
}

// ── Timeline data ──────────────────────────────────────────────────
const timelineNodes = ref<TimelineNode[]>([
  {
    id: 1,
    stage: 'DETECTION',
    agent: 'Scanner',
    action: 'Identified anomalous prompt injection pattern across 3 API endpoints. Signature match: PIA-7734. Confidence 97%.',
    timestamp: '14:23:07',
    duration: '0m 12s',
  },
  {
    id: 2,
    stage: 'INVESTIGATION',
    agent: 'Monitor',
    action: 'Cross-referencing call patterns against baseline. Correlating with 4 prior incidents in 6h window. Escalating severity to CRITICAL.',
    timestamp: '14:23:19',
    duration: '2m 41s',
  },
  {
    id: 3,
    stage: 'CONTAINMENT',
    agent: 'Responder',
    action: 'Isolating api-gateway-01 from production traffic. Rerouting requests through clean proxy. Blocking originating IP range.',
    timestamp: '14:26:00',
    duration: '1m 05s',
    active: true,
  },
  {
    id: 4,
    stage: 'RESOLUTION',
    agent: 'Sentinel',
    action: 'Awaiting containment confirmation. Patch package queued for deployment. System restoration pending security clearance.',
    timestamp: '—',
  },
])

// ── Attack patterns data ───────────────────────────────────────────
const attackPatterns = ref<AttackPattern[]>([
  { name: 'Prompt Injection',     count: 47, pct: 38, stage: 'DETECTION'     },
  { name: 'Data Exfiltration',    count: 31, pct: 25, stage: 'INVESTIGATION' },
  { name: 'Privilege Escalation', count: 28, pct: 23, stage: 'CONTAINMENT'   },
  { name: 'Model Poisoning',      count: 17, pct: 14, stage: 'RESOLUTION'    },
])

// ── Risk systems data ──────────────────────────────────────────────
const riskSystems = ref<RiskSystem[]>([
  { name: 'api-gateway-01',  score: 95, status: 'critical' },
  { name: 'orchestrator-02', score: 82, status: 'critical' },
  { name: 'llm-worker-07',   score: 78, status: 'high'     },
  { name: 'fine-tune-03',    score: 67, status: 'high'     },
  { name: 'api-gateway-02',  score: 45, status: 'medium'   },
  { name: 'auth-service',    score: 41, status: 'medium'   },
  { name: 'vector-store-01', score: 22, status: 'low'      },
  { name: 'agent-runner-05', score: 8,  status: 'secured'  },
])

// ── Vulnerability data ─────────────────────────────────────────────
const vulns = ref<Vuln[]>([
  { id: 'CVE-2024-8821', name: 'Prompt injection via system role override',      score: 9.8, severity: 'CRITICAL', affectedSystems: 3, detectedAt: '14m ago',  status: 'IN_PROGRESS' },
  { id: 'CVE-2024-7734', name: 'Context window token boundary bypass',           score: 8.2, severity: 'HIGH',     affectedSystems: 7, detectedAt: '1h ago',   status: 'OPEN'        },
  { id: 'CVE-2024-6619', name: 'Agent tool schema manipulation',                 score: 7.6, severity: 'HIGH',     affectedSystems: 4, detectedAt: '2h ago',   status: 'IN_PROGRESS' },
  { id: 'CVE-2024-5502', name: 'Embedding store enumeration exploit',            score: 6.1, severity: 'MEDIUM',   affectedSystems: 2, detectedAt: '3h ago',   status: 'OPEN'        },
  { id: 'CVE-2024-4481', name: 'Privilege escalation via delegated token',       score: 5.4, severity: 'MEDIUM',   affectedSystems: 5, detectedAt: '5h ago',   status: 'MITIGATED'   },
  { id: 'CVE-2024-3310', name: 'Model output exfiltration via side channel',     score: 8.9, severity: 'HIGH',     affectedSystems: 6, detectedAt: '6h ago',   status: 'OPEN'        },
  { id: 'CVE-2024-2208', name: 'Memory store injection via crafted query',       score: 7.1, severity: 'HIGH',     affectedSystems: 3, detectedAt: '8h ago',   status: 'PATCHED'     },
  { id: 'CVE-2024-1105', name: 'Rate limiter bypass via request fragmentation',  score: 3.2, severity: 'LOW',      affectedSystems: 1, detectedAt: '12h ago',  status: 'PATCHED'     },
])

// ── Containment data ───────────────────────────────────────────────
const containedSystems = ref<ContainedSystem[]>([
  { name: 'api-gateway-01', isolatedAt: '14:26:00', reason: 'Prompt injection campaign', status: 'ISOLATED'   },
  { name: 'llm-worker-07',  isolatedAt: '14:22:44', reason: 'Exfiltration attempt',      status: 'MONITORING' },
  { name: 'fine-tune-03',   isolatedAt: '13:41:12', reason: 'Model poisoning probe',     status: 'CLEARED'    },
])

const respondingAgents = ref<RespondingAgent[]>([
  { name: 'Responder', task: 'Isolating api-gateway-01 from prod traffic', since: '1m ago',  status: 'active' },
  { name: 'Monitor',   task: 'Correlating exfiltration attempt patterns',  since: '14m ago', status: 'active' },
  { name: 'Scanner',   task: 'Scanning fine-tune cluster for anomalies',   since: '32m ago', status: 'idle'   },
])

// ── Helpers ────────────────────────────────────────────────────────
function severityBand(score: number): string {
  if (score >= 9.0) return 'critical'
  if (score >= 7.0) return 'high'
  if (score >= 4.0) return 'medium'
  return 'low'
}

function stageClass(stage: TimelineNode['stage']): string {
  const map: Record<TimelineNode['stage'], string> = {
    DETECTION:     'detection',
    INVESTIGATION: 'investigation',
    CONTAINMENT:   'containment',
    RESOLUTION:    'resolution',
  }
  return map[stage]
}

function vulnStatusClass(status: Vuln['status']): string {
  const map: Record<Vuln['status'], string> = {
    OPEN:        'status--open',
    IN_PROGRESS: 'status--in-progress',
    PATCHED:     'status--patched',
    MITIGATED:   'status--mitigated',
  }
  return map[status]
}

function containmentStatusClass(status: ContainedSystem['status']): string {
  const map: Record<ContainedSystem['status'], string> = {
    ISOLATED:   'containment--isolated',
    MONITORING: 'containment--monitoring',
    CLEARED:    'containment--cleared',
  }
  return map[status]
}

// ── Computed stats ─────────────────────────────────────────────────
const riskCounts = computed(() => ({
  critical: riskSystems.value.filter(s => s.status === 'critical').length,
  high:     riskSystems.value.filter(s => s.status === 'high').length,
  medium:   riskSystems.value.filter(s => s.status === 'medium').length,
  secured:  riskSystems.value.filter(s => s.status === 'low' || s.status === 'secured').length,
}))

const activeStage = computed(() => {
  const active = timelineNodes.value.find(n => n.active)
  return active ? stageClass(active.stage) : 'containment'
})

// ── Live clock ─────────────────────────────────────────────────────
const liveTime = ref('')
let clockInterval: ReturnType<typeof setInterval> | null = null

function updateClock() {
  const now = new Date()
  liveTime.value = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

// ── Mount ──────────────────────────────────────────────────────────
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
    <h1 class="sr-only">Aegis Operations Intelligence</h1>

    <!-- ── Page header ──────────────────────────────────────────── -->
    <header class="page-header" role="banner">
      <div class="page-header__inner">
        <div class="page-header__left">
          <span class="page-header__brand">AEGIS</span>
          <span class="page-header__separator" aria-hidden="true">/</span>
          <span class="page-header__title">Operations Intelligence</span>
        </div>
        <div class="page-header__right">
          <span class="page-header__live-label" aria-hidden="true">●</span>
          <span class="page-header__time" aria-label="Current time">{{ liveTime }}</span>
          <span class="page-header__incident-badge" :class="`incident-badge--${activeStage}`">
            ACTIVE INCIDENT
          </span>
        </div>
      </div>
    </header>

    <!-- ── Body: 60/40 grid ─────────────────────────────────────── -->
    <div class="page__body">

      <!-- ── LEFT MAIN ─────────────────────────────────────────── -->
      <main class="page__main">

        <!-- Section 1: Incident Response Timeline -->
        <section class="card" aria-labelledby="timeline-heading">
          <div class="card__header">
            <h2 class="card__title" id="timeline-heading">Incident Response Timeline</h2>
            <span class="card__meta">INC-2024-0047 — Prompt Injection Campaign</span>
          </div>

          <div class="timeline" role="list" aria-label="Incident response stages">
            <div
              v-for="(node, index) in timelineNodes"
              :key="node.id"
              class="timeline-node"
              :class="[`timeline-node--${stageClass(node.stage)}`, { 'timeline-node--active': node.active, 'timeline-node--pending': !node.duration && !node.active }]"
              role="listitem"
              :aria-label="`${node.stage} stage: ${node.agent} — ${node.action}`"
            >
              <!-- connector line above (all but first) -->
              <div
                v-if="index > 0"
                class="timeline-connector"
                aria-hidden="true"
              ></div>

              <div class="timeline-node__body">
                <!-- Left: dot -->
                <div class="timeline-node__dot-wrap" aria-hidden="true">
                  <span
                    class="timeline-node__dot"
                    :class="[`dot--${stageClass(node.stage)}`, { 'dot--pulse': node.active }]"
                  ></span>
                </div>

                <!-- Right: card content -->
                <div class="timeline-node__card">
                  <div class="timeline-node__top">
                    <span
                      class="stage-badge"
                      :class="`stage-badge--${stageClass(node.stage)}`"
                    >{{ node.stage }}</span>
                    <span class="timeline-node__agent">{{ node.agent }}</span>
                    <span class="timeline-node__spacer" aria-hidden="true"></span>
                    <span class="timeline-node__ts" :aria-label="`Timestamp: ${node.timestamp}`">{{ node.timestamp }}</span>
                    <span v-if="node.duration" class="timeline-node__duration" :aria-label="`Duration: ${node.duration}`">{{ node.duration }}</span>
                  </div>
                  <p class="timeline-node__action">{{ node.action }}</p>
                  <div v-if="node.active" class="timeline-node__active-indicator" aria-label="In progress">
                    <span class="active-dot" aria-hidden="true"></span>
                    <span class="active-label">In progress</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Section 2: Attack Pattern Categories -->
        <section class="card" aria-labelledby="patterns-heading">
          <div class="card__header">
            <h2 class="card__title" id="patterns-heading">Attack Pattern Categories</h2>
            <span class="card__meta">Last 24 hours — {{ attackPatterns.reduce((s, p) => s + p.count, 0) }} total events</span>
          </div>

          <div class="patterns-list" role="list" aria-label="Attack pattern frequency">
            <div
              v-for="pattern in attackPatterns"
              :key="pattern.name"
              class="pattern-row"
              role="listitem"
            >
              <div class="pattern-row__header">
                <span class="pattern-row__name">{{ pattern.name }}</span>
                <span
                  class="pattern-row__count"
                  :class="`count--${stageClass(pattern.stage)}`"
                  :aria-label="`${pattern.count} events`"
                >{{ pattern.count }}</span>
                <span
                  class="pattern-row__pct"
                  :aria-label="`${pattern.pct}% of total`"
                >{{ pattern.pct }}%</span>
              </div>
              <div
                class="pattern-bar-track"
                :class="`bar-track--${stageClass(pattern.stage)}`"
                role="presentation"
              >
                <div
                  class="pattern-bar-fill"
                  :class="`bar-fill--${stageClass(pattern.stage)}`"
                  :style="{ width: pattern.pct + '%' }"
                  :aria-label="`${pattern.pct}% frequency`"
                ></div>
              </div>
            </div>
          </div>
        </section>

        <!-- Section 3: Risk Overview -->
        <section class="card" aria-labelledby="risk-heading">
          <div class="card__header">
            <h2 class="card__title" id="risk-heading">Risk Overview</h2>
            <span class="card__meta">{{ riskSystems.length }} systems monitored</span>
          </div>

          <div class="risk-body">
            <!-- Risk summary pills -->
            <div class="risk-summary" role="list" aria-label="Risk summary by severity">
              <div class="risk-pill risk-pill--critical" role="listitem" :aria-label="`${riskCounts.critical} critical systems`">
                <span class="risk-pill__count">{{ riskCounts.critical }}</span>
                <span class="risk-pill__label">Critical</span>
              </div>
              <div class="risk-pill risk-pill--high" role="listitem" :aria-label="`${riskCounts.high} high risk systems`">
                <span class="risk-pill__count">{{ riskCounts.high }}</span>
                <span class="risk-pill__label">High</span>
              </div>
              <div class="risk-pill risk-pill--medium" role="listitem" :aria-label="`${riskCounts.medium} medium risk systems`">
                <span class="risk-pill__count">{{ riskCounts.medium }}</span>
                <span class="risk-pill__label">Medium</span>
              </div>
              <div class="risk-pill risk-pill--secured" role="listitem" :aria-label="`${riskCounts.secured} secured systems`">
                <span class="risk-pill__count">{{ riskCounts.secured }}</span>
                <span class="risk-pill__label">Secured</span>
              </div>
            </div>

            <!-- Spectrum bar + system dots -->
            <div class="risk-spectrum-wrap">
              <div class="risk-spectrum" aria-hidden="true">
                <span
                  v-for="sys in riskSystems"
                  :key="sys.name"
                  class="risk-system-dot"
                  :class="`risk-dot--${sys.status}`"
                  :style="{ left: sys.score + '%' }"
                  :title="sys.name"
                ></span>
              </div>
              <div class="risk-spectrum-labels" aria-hidden="true">
                <span class="risk-spectrum-label risk-spectrum-label--left">Critical</span>
                <span class="risk-spectrum-label risk-spectrum-label--right">Secured</span>
              </div>
            </div>

            <!-- System list -->
            <ul class="risk-system-list" role="list" aria-label="System risk scores">
              <li
                v-for="sys in riskSystems"
                :key="sys.name"
                class="risk-system-row"
                :aria-label="`${sys.name}: risk score ${sys.score}, status ${sys.status}`"
              >
                <span
                  class="risk-system-dot-inline"
                  :class="`risk-dot--${sys.status}`"
                  aria-hidden="true"
                ></span>
                <span class="risk-system-name">{{ sys.name }}</span>
                <span
                  class="risk-system-score"
                  :class="`score--${sys.status}`"
                >{{ sys.score }}</span>
                <div class="risk-bar-track">
                  <div
                    class="risk-bar-fill"
                    :class="`risk-bar--${sys.status}`"
                    :style="{ width: sys.score + '%' }"
                    role="presentation"
                  ></div>
                </div>
              </li>
            </ul>
          </div>
        </section>

      </main>

      <!-- ── RIGHT SIDEBAR ──────────────────────────────────────── -->
      <aside class="sidebar" aria-label="Threat intelligence and containment status">

        <!-- Section 4: Threat Intelligence — Vulnerability Cards -->
        <section aria-labelledby="vuln-heading">
          <div class="card__header card__header--flat">
            <h2 class="card__title" id="vuln-heading">Threat Intelligence</h2>
            <span
              class="card__meta"
              :aria-label="`${vulns.length} vulnerabilities tracked`"
            >{{ vulns.length }} CVEs</span>
          </div>

          <ul class="vuln-list" role="list" aria-label="Vulnerability entries">
            <li
              v-for="vuln in vulns"
              :key="vuln.id"
              class="vuln-card"
              :class="`vuln-card--${severityBand(vuln.score)}`"
              :aria-label="`${vuln.id}: ${vuln.name}, score ${vuln.score}, ${vuln.affectedSystems} affected systems, detected ${vuln.detectedAt}, status ${vuln.status}`"
            >
              <div class="vuln-card__top">
                <div class="vuln-card__ids">
                  <span class="vuln-card__cve-id">{{ vuln.id }}</span>
                  <span
                    class="vuln-card__score"
                    :class="`vuln-score--${severityBand(vuln.score)}`"
                  >{{ vuln.score.toFixed(1) }}</span>
                </div>
                <span
                  class="vuln-status-badge"
                  :class="vulnStatusClass(vuln.status)"
                >{{ vuln.status.replace('_', ' ') }}</span>
              </div>
              <p class="vuln-card__name">{{ vuln.name }}</p>
              <div class="vuln-card__meta">
                <span
                  class="vuln-meta-item"
                  :aria-label="`${vuln.affectedSystems} affected systems`"
                >
                  <span class="vuln-meta-item__value" aria-hidden="true">{{ vuln.affectedSystems }}</span>
                  <span class="vuln-meta-item__label" aria-hidden="true">systems</span>
                </span>
                <span
                  class="vuln-meta-item vuln-meta-item--ts"
                  :aria-label="`Detected ${vuln.detectedAt}`"
                >{{ vuln.detectedAt }}</span>
              </div>
            </li>
          </ul>
        </section>

        <!-- Section 5: Containment Status -->
        <section class="card" aria-labelledby="containment-heading">
          <div class="card__header">
            <h2 class="card__title" id="containment-heading">Containment Status</h2>
          </div>

          <!-- Isolated systems -->
          <div class="containment-group">
            <h3 class="containment-group__title">Isolated Systems</h3>
            <ul class="containment-list" role="list" aria-label="Isolated systems">
              <li
                v-for="sys in containedSystems"
                :key="sys.name"
                class="containment-row"
                :aria-label="`${sys.name}: ${sys.status}, isolated at ${sys.isolatedAt}, reason: ${sys.reason}`"
              >
                <div class="containment-row__top">
                  <span class="containment-row__name">{{ sys.name }}</span>
                  <span
                    class="containment-badge"
                    :class="containmentStatusClass(sys.status)"
                  >{{ sys.status }}</span>
                </div>
                <div class="containment-row__bottom">
                  <span class="containment-row__reason">{{ sys.reason }}</span>
                  <span class="containment-row__ts">{{ sys.isolatedAt }}</span>
                </div>
              </li>
            </ul>
          </div>

          <div class="containment-divider" aria-hidden="true"></div>

          <!-- Responding agents -->
          <div class="containment-group">
            <h3 class="containment-group__title">Responding Agents</h3>
            <ul class="containment-list" role="list" aria-label="Responding agents">
              <li
                v-for="agent in respondingAgents"
                :key="agent.name"
                class="agent-row"
                :class="`agent-row--${agent.status}`"
                :aria-label="`${agent.name}: ${agent.status}, task — ${agent.task}, since ${agent.since}`"
              >
                <div class="agent-row__left">
                  <span
                    class="agent-status-dot"
                    :class="`agent-dot--${agent.status}`"
                    aria-hidden="true"
                  ></span>
                  <div class="agent-row__info">
                    <span class="agent-row__name">{{ agent.name }}</span>
                    <span class="agent-row__task">{{ agent.task }}</span>
                  </div>
                </div>
                <span class="agent-row__since">{{ agent.since }}</span>
              </li>
            </ul>
          </div>
        </section>

      </aside>
    </div><!-- /page__body -->
  </div><!-- /page -->
</template>

<style scoped>
/* ── Reset ────────────────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* ── Page root ────────────────────────────────────────────────────── */
.page {
  min-height: 100vh;
  background-color: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  display: grid;
  grid-template-rows: auto 1fr;
  overflow-x: hidden;
  opacity: 0;
  transition: opacity var(--duration-normal) var(--easing);
}

.page.is-mounted {
  opacity: 1;
}

/* ── Screen-reader only ───────────────────────────────────────────── */
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

/* ── Page header ──────────────────────────────────────────────────── */
.page-header {
  background-color: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
  padding: 0 calc(var(--space-unit) * 6);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-md);
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

.page-header__separator {
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

.page-header__live-label {
  font-size: 0.625rem;
  color: var(--brand-error);
  animation: pulse 1.5s var(--easing) infinite;
}

.page-header__time {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--brand-muted);
}

.page-header__incident-badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: calc(var(--space-unit) * 1) calc(var(--space-unit) * 2.5);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
}

.incident-badge--detection    { background-color: var(--brand-error);     }
.incident-badge--investigation { background-color: var(--brand-accent);   }
.incident-badge--containment  { background-color: var(--brand-secondary); }
.incident-badge--resolution   { background-color: var(--brand-primary);   }

/* Mobile header */
@media (max-width: 768px) {
  .page-header__inner {
    height: auto;
    flex-wrap: wrap;
    padding: calc(var(--space-unit) * 3) 0;
    gap: calc(var(--space-unit) * 2);
  }
  .page-header__incident-badge {
    display: none;
  }
}

/* ── Page body grid ───────────────────────────────────────────────── */
.page__body {
  max-width: var(--container-max);
  width: 100%;
  margin: 0 auto;
  padding: calc(var(--space-unit) * 6);
  display: grid;
  grid-template-columns: 60fr 40fr;
  gap: calc(var(--space-unit) * 6);
  align-items: start;
}

@media (max-width: 768px) {
  .page__body {
    grid-template-columns: 1fr;
    padding: calc(var(--space-unit) * 4);
    gap: calc(var(--space-unit) * 4);
  }
}

/* ── Main column ──────────────────────────────────────────────────── */
.page__main {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
.sidebar {
  background: linear-gradient(180deg, var(--brand-bg-secondary), var(--brand-bg));
  position: sticky;
  top: calc(var(--space-unit) * 20);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
  max-height: calc(100vh - calc(var(--space-unit) * 24));
  overflow-y: auto;
}

@media (max-width: 768px) {
  .sidebar {
    position: static;
    max-height: none;
    overflow-y: visible;
  }
}

/* ── Card base ────────────────────────────────────────────────────── */
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
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
  background: linear-gradient(90deg, color-mix(in srgb, var(--brand-accent) 6%, var(--brand-bg-secondary)), var(--brand-bg-secondary));
}

.card__header--flat {
  background-color: transparent;
  border-bottom: 1px solid var(--brand-border);
  padding: calc(var(--space-unit) * 4) 0 calc(var(--space-unit) * 3);
}

.card__title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: var(--brand-text);
  margin: 0;
}

.card__meta {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  white-space: nowrap;
}

/* ── Stage badges ─────────────────────────────────────────────────── */
.stage-badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
  flex-shrink: 0;
}

.stage-badge--detection    { background-color: var(--brand-error);     }
.stage-badge--investigation { background-color: var(--brand-accent);   }
.stage-badge--containment  { background-color: var(--brand-secondary); }
.stage-badge--resolution   { background-color: var(--brand-primary);   }

/* ── Timeline ─────────────────────────────────────────────────────── */
.timeline {
  padding: calc(var(--space-unit) * 6);
  display: flex;
  flex-direction: column;
}

.timeline-node {
  position: relative;
}

.timeline-connector {
  width: calc(var(--space-unit) * 3);
  height: calc(var(--space-unit) * 5);
  margin-left: calc(var(--space-unit) * 1.5);
  border-left: 2px dashed var(--brand-border);
}

.timeline-node__body {
  display: flex;
  gap: calc(var(--space-unit) * 4);
  align-items: flex-start;
}

.timeline-node__dot-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  padding-top: calc(var(--space-unit) * 1.5);
}

.timeline-node__dot {
  width: calc(var(--space-unit) * 3);
  height: calc(var(--space-unit) * 3);
  border-radius: 50%;
  flex-shrink: 0;
}

.dot--detection    { background-color: var(--brand-error);     }
.dot--investigation { background-color: var(--brand-accent);   }
.dot--containment  { background-color: var(--brand-secondary); }
.dot--resolution   { background-color: var(--brand-primary);   }

.dot--pulse {
  animation: pulse 1.5s var(--easing) infinite;
}

.timeline-node__card {
  flex: 1;
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
  border: 1px solid var(--brand-border);
}

/* Stage-specific card styling */
.timeline-node--detection .timeline-node__card {
  background-color: color-mix(in srgb, var(--brand-error) 8%, var(--brand-surface));
  border-left: 3px solid var(--brand-error);
}
.timeline-node--investigation .timeline-node__card {
  background-color: color-mix(in srgb, var(--brand-accent) 8%, var(--brand-surface));
  border-left: 3px solid var(--brand-accent);
}
.timeline-node--containment .timeline-node__card {
  background-color: color-mix(in srgb, var(--brand-secondary) 8%, var(--brand-surface));
  border-left: 3px solid var(--brand-secondary);
}
.timeline-node--resolution .timeline-node__card {
  background-color: color-mix(in srgb, var(--brand-primary) 8%, var(--brand-surface));
  border-left: 3px solid var(--brand-primary);
}

.timeline-node--active .timeline-node__card {
  box-shadow: var(--shadow-lg);
}

.timeline-node--pending {
  opacity: 0.5;
}

.timeline-node__top {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  margin-bottom: calc(var(--space-unit) * 3);
  flex-wrap: wrap;
}

.timeline-node__agent {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
}

.timeline-node__spacer {
  flex: 1;
}

.timeline-node__ts {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

.timeline-node__duration {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  padding: calc(var(--space-unit) * 0.5) calc(var(--space-unit) * 2);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-sm);
}

.timeline-node__action {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  line-height: 1.6;
  color: var(--brand-text);
  margin: 0;
}

.timeline-node__active-indicator {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  margin-top: calc(var(--space-unit) * 3);
  padding-top: calc(var(--space-unit) * 3);
  border-top: 1px solid var(--brand-border);
}

.active-dot {
  width: calc(var(--space-unit) * 1.5);
  height: calc(var(--space-unit) * 1.5);
  border-radius: 50%;
  background-color: var(--brand-secondary);
  animation: pulse 1.5s var(--easing) infinite;
}

.active-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-secondary);
}

/* ── Attack patterns ──────────────────────────────────────────────── */
.patterns-list {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 5);
}

.pattern-row__header {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 3);
  margin-bottom: calc(var(--space-unit) * 2);
}

.pattern-row__name {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--brand-text);
  flex: 1;
}

.pattern-row__count {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  line-height: 1;
}

.count--detection    { color: var(--brand-error);     }
.count--investigation { color: var(--brand-accent);   }
.count--containment  { color: var(--brand-secondary); }
.count--resolution   { color: var(--brand-primary);   }

.pattern-row__pct {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  min-width: calc(var(--space-unit) * 7);
  text-align: right;
}

.pattern-bar-track {
  height: calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.bar-track--detection    { background-color: color-mix(in srgb, var(--brand-error)     15%, transparent); }
.bar-track--investigation { background-color: color-mix(in srgb, var(--brand-accent)   15%, transparent); }
.bar-track--containment  { background-color: color-mix(in srgb, var(--brand-secondary) 15%, transparent); }
.bar-track--resolution   { background-color: color-mix(in srgb, var(--brand-primary)   15%, transparent); }

.pattern-bar-fill {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--duration-slow) var(--easing);
}

.bar-fill--detection    { background-color: var(--brand-error);     }
.bar-fill--investigation { background-color: var(--brand-accent);   }
.bar-fill--containment  { background-color: var(--brand-secondary); }
.bar-fill--resolution   { background-color: var(--brand-primary);   }

/* ── Risk overview ────────────────────────────────────────────────── */
.risk-body {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 5);
}

.risk-summary {
  display: flex;
  gap: calc(var(--space-unit) * 3);
  flex-wrap: wrap;
}

.risk-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
  border-radius: var(--radius-md);
  flex: 1;
  min-width: calc(var(--space-unit) * 14);
}

.risk-pill--critical {
  background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-error) 35%, transparent);
}
.risk-pill--high {
  background-color: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-accent) 35%, transparent);
}
.risk-pill--medium {
  background-color: color-mix(in srgb, var(--brand-secondary) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-secondary) 35%, transparent);
}
.risk-pill--secured {
  background-color: color-mix(in srgb, var(--brand-primary) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-primary) 25%, transparent);
}

.risk-pill__count {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brand-text);
}

.risk-pill__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Spectrum bar */
.risk-spectrum-wrap {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1.5);
}

.risk-spectrum {
  position: relative;
  height: calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  background: linear-gradient(
    to right,
    var(--brand-error),
    var(--brand-accent) 40%,
    var(--brand-secondary) 70%,
    var(--brand-primary)
  );
  overflow: visible;
}

.risk-system-dot {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  border: 2px solid var(--brand-bg);
  cursor: default;
  transition: transform var(--duration-fast) var(--easing);
}

.risk-system-dot:hover {
  transform: translate(-50%, -50%) scale(1.4);
  z-index: 1;
}

.risk-dot--critical { background-color: var(--brand-error);     }
.risk-dot--high     { background-color: var(--brand-accent);    }
.risk-dot--medium   { background-color: var(--brand-secondary); }
.risk-dot--low      { background-color: var(--brand-primary);   }
.risk-dot--secured  { background-color: var(--brand-primary);   }

.risk-spectrum-labels {
  display: flex;
  justify-content: space-between;
}

.risk-spectrum-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* System list */
.risk-system-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2.5);
}

.risk-system-row {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 2.5) 1fr auto calc(var(--space-unit) * 20);
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.risk-system-dot-inline {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.risk-system-name {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.risk-system-score {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  line-height: 1;
  text-align: right;
  white-space: nowrap;
}

.score--critical { color: var(--brand-error);     }
.score--high     { color: var(--brand-accent);    }
.score--medium   { color: var(--brand-secondary); }
.score--low      { color: var(--brand-primary);   }
.score--secured  { color: var(--brand-primary);   }

.risk-bar-track {
  height: calc(var(--space-unit) * 1.5);
  background-color: color-mix(in srgb, var(--brand-border) 60%, transparent);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.risk-bar-fill {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--duration-slow) var(--easing);
}

.risk-bar--critical { background-color: var(--brand-error);     }
.risk-bar--high     { background-color: var(--brand-accent);    }
.risk-bar--medium   { background-color: var(--brand-secondary); }
.risk-bar--low      { background-color: var(--brand-primary);   }
.risk-bar--secured  { background-color: var(--brand-primary);   }

/* ── Vulnerability cards ──────────────────────────────────────────── */
.vuln-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.vuln-card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 4);
  transition: background-color var(--duration-fast) var(--easing);
}

.vuln-card:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 80%, var(--brand-bg-secondary));
}

.vuln-card--critical { border-left: 3px solid var(--brand-error);     }
.vuln-card--high     { border-left: 3px solid var(--brand-accent);    }
.vuln-card--medium   { border-left: 3px solid var(--brand-secondary); }
.vuln-card--low      { border-left: 3px solid var(--brand-primary);   }

.vuln-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 3);
  margin-bottom: calc(var(--space-unit) * 2);
}

.vuln-card__ids {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.vuln-card__cve-id {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--brand-text);
}

.vuln-card__score {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
}

.vuln-score--critical { color: var(--brand-error);     }
.vuln-score--high     { color: var(--brand-accent);    }
.vuln-score--medium   { color: var(--brand-secondary); }
.vuln-score--low      { color: var(--brand-primary);   }

.vuln-status-badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
  white-space: nowrap;
  flex-shrink: 0;
}

.status--open        { background-color: var(--brand-error);     }
.status--in-progress { background-color: var(--brand-accent);    }
.status--patched     { background-color: var(--brand-primary);   }
.status--mitigated   { background-color: var(--brand-primary);   }

.vuln-card__name {
  font-family: var(--font-body);
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 2.5);
}

.vuln-card__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 3);
}

.vuln-meta-item {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
}

.vuln-meta-item__value {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
}

.vuln-meta-item__label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
}

.vuln-meta-item--ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
}

/* ── Containment status ───────────────────────────────────────────── */
.containment-group {
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
}

.containment-group__title {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin: 0 0 calc(var(--space-unit) * 3);
}

.containment-divider {
  height: 1px;
  background-color: var(--brand-border);
  margin: 0 calc(var(--space-unit) * 6);
}

.containment-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.containment-row {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1.5);
  padding: calc(var(--space-unit) * 3);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--brand-border);
}

.containment-row__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 2);
}

.containment-row__name {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
}

.containment-badge {
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

.containment--isolated   { background-color: var(--brand-error);     }
.containment--monitoring { background-color: var(--brand-secondary); }
.containment--cleared    { background-color: var(--brand-primary);   }

.containment-row__bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 2);
}

.containment-row__reason {
  font-family: var(--font-body);
  font-size: 0.75rem;
  color: var(--brand-muted);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.containment-row__ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  white-space: nowrap;
}

/* ── Responding agents ────────────────────────────────────────────── */
.agent-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--brand-border);
}

.agent-row__left {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 2.5);
  flex: 1;
  min-width: 0;
}

.agent-status-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: calc(var(--space-unit) * 1);
}

.agent-dot--active { background-color: var(--brand-error); animation: pulse 1.5s var(--easing) infinite; }
.agent-dot--idle   { background-color: var(--brand-secondary); }

.agent-row__info {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
  min-width: 0;
}

.agent-row__name {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
}

.agent-row__task {
  font-family: var(--font-body);
  font-size: 0.75rem;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.agent-row__since {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Keyframes ────────────────────────────────────────────────────── */
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.85); }
}

/* ── Reduced motion ───────────────────────────────────────────────── */
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

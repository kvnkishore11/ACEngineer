<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/dashboard/v3-split-panel
// Layout: 55/45 split grid — left pane (sticky stats bar + scrollable threat feed)
//         right pane (defense posture gauge + agent team status + active incidents)
// "Mission control" variant — two live independently-scrolling panes

// ── Types ────────────────────────────────────────────────────────
interface ThreatEntry {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  system: string
  ts: string
  isNew?: boolean
}

interface Agent {
  name: string
  role: string
  status: 'active' | 'idle' | 'offline' | 'responding'
  uptime: string
  neutralized: number
}

interface Incident {
  id: number
  title: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  openedAt: string
  status: 'active' | 'resolved'
}

// ── Mock data ────────────────────────────────────────────────────
const posturePercent = ref(83)

const threats = ref<ThreatEntry[]>([
  { id: 1,  name: 'Prompt Injection — GPT-4 endpoint',  severity: 'CRITICAL', system: 'api-gateway-01',   ts: '0s ago',  isNew: true  },
  { id: 2,  name: 'Data Exfiltration attempt',           severity: 'HIGH',     system: 'llm-worker-07',   ts: '12s ago', isNew: true  },
  { id: 3,  name: 'Privilege Escalation — Agent token',  severity: 'CRITICAL', system: 'orchestrator-02', ts: '34s ago'               },
  { id: 4,  name: 'Model Poisoning probe',               severity: 'HIGH',     system: 'fine-tune-03',    ts: '1m ago'                },
  { id: 5,  name: 'Unusual API call pattern',            severity: 'MEDIUM',   system: 'api-gateway-02',  ts: '2m ago'                },
  { id: 6,  name: 'Repeated auth failure',               severity: 'MEDIUM',   system: 'auth-service',    ts: '3m ago'                },
  { id: 7,  name: 'Unrecognized tool invocation',        severity: 'LOW',      system: 'agent-runner-05', ts: '4m ago'                },
  { id: 8,  name: 'Context window overflow probe',       severity: 'MEDIUM',   system: 'llm-worker-02',   ts: '6m ago'                },
  { id: 9,  name: 'Rate limit bypass attempt',           severity: 'HIGH',     system: 'rate-limiter-01', ts: '8m ago'                },
  { id: 10, name: 'Jailbreak attempt — system prompt',   severity: 'CRITICAL', system: 'llm-worker-04',   ts: '9m ago'                },
  { id: 11, name: 'Anomalous embedding query',           severity: 'MEDIUM',   system: 'vector-store-01', ts: '11m ago'               },
  { id: 12, name: 'Memory store enumeration probe',      severity: 'HIGH',     system: 'memory-svc-02',   ts: '14m ago'               },
])

const agents: Agent[] = [
  { name: 'Scanner',   role: 'Vulnerability scanning',  status: 'active',     uptime: '99.97%', neutralized: 142 },
  { name: 'Monitor',   role: 'Traffic analysis',         status: 'responding', uptime: '99.91%', neutralized: 87  },
  { name: 'Responder', role: 'Threat containment',       status: 'active',     uptime: '99.85%', neutralized: 203 },
  { name: 'Sentinel',  role: 'Perimeter watch',          status: 'idle',       uptime: '98.40%', neutralized: 56  },
  { name: 'Analyst',   role: 'Behavioral correlation',   status: 'active',     uptime: '99.72%', neutralized: 119 },
  { name: 'Patcher',   role: 'Remediation automation',   status: 'offline',    uptime: '94.10%', neutralized: 33  },
]

const incidents = ref<Incident[]>([
  { id: 1, title: 'Prompt injection campaign — api-gateway cluster',  severity: 'CRITICAL', openedAt: '14 min ago', status: 'active'   },
  { id: 2, title: 'Exfiltration attempt — llm-worker-07',             severity: 'HIGH',     openedAt: '22 min ago', status: 'active'   },
  { id: 3, title: 'Token privilege escalation — orchestrator-02',     severity: 'CRITICAL', openedAt: '41 min ago', status: 'active'   },
  { id: 4, title: 'Model poisoning probe — fine-tune cluster',         severity: 'HIGH',     openedAt: '1h ago',     status: 'active'   },
  { id: 5, title: 'Anomalous call pattern — api-gateway-02',          severity: 'MEDIUM',   openedAt: '2h ago',     status: 'resolved' },
])

const sparklinePath = 'M0,40 L10,38 L20,42 L30,35 L40,30 L50,28 L60,22 L70,25 L80,18 L90,15 L100,12'

// ── Computed ──────────────────────────────────────────────────────
const activeIncidents = computed(() => incidents.value.filter(i => i.status === 'active'))

const threatCounts = computed(() => ({
  total:    threats.value.length,
  critical: threats.value.filter(t => t.severity === 'CRITICAL').length,
  high:     threats.value.filter(t => t.severity === 'HIGH').length,
}))

const agentCounts = computed(() => ({
  online:     agents.filter(a => a.status !== 'offline').length,
  total:      agents.length,
  responding: agents.filter(a => a.status === 'responding').length,
}))

const severityCounts = computed(() => ({
  CRITICAL: activeIncidents.value.filter(i => i.severity === 'CRITICAL').length,
  HIGH:     activeIncidents.value.filter(i => i.severity === 'HIGH').length,
  MEDIUM:   activeIncidents.value.filter(i => i.severity === 'MEDIUM').length,
}))

// ── SVG gauge math ────────────────────────────────────────────────
const gaugeRadius       = 90
const gaugeCircumference = 2 * Math.PI * gaugeRadius
const gaugeDashOffset   = computed(() =>
  gaugeCircumference * (1 - posturePercent.value / 100)
)

// ── Mount reveal ─────────────────────────────────────────────────
const isMounted = ref(false)

// ── CSS-only live dot — no JS interval for the blink ─────────────
// Live dot uses @keyframes pulse (CSS-only). Only JS intervals used
// are for simulating incoming threats (cleared in onUnmounted).

let threatSimInterval: ReturnType<typeof setInterval> | null = null
let newThreatTimeout: ReturnType<typeof setTimeout> | null  = null

onMounted(() => {
  // nextTick ensures initial opacity:0 is painted before transition fires
  nextTick(() => {
    isMounted.value = true
  })

  // Simulate an incoming critical threat after 3s to demonstrate threat-enter animation
  newThreatTimeout = setTimeout(() => {
    const newThreat: ThreatEntry = {
      id: 13,
      name: 'Tool chain hijack — agent-runner-01',
      severity: 'CRITICAL',
      system: 'agent-runner-01',
      ts: 'just now',
      isNew: true,
    }
    threats.value.unshift(newThreat)
    // Clear isNew flag after animation completes
    threatSimInterval = setInterval(() => {
      threats.value.forEach(t => { t.isNew = false })
      if (threatSimInterval !== null) {
        clearInterval(threatSimInterval)
        threatSimInterval = null
      }
    }, 500)
  }, 3000)
})

onUnmounted(() => {
  if (threatSimInterval !== null) {
    clearInterval(threatSimInterval)
    threatSimInterval = null
  }
  if (newThreatTimeout !== null) {
    clearTimeout(newThreatTimeout)
    newThreatTimeout = null
  }
})
</script>

<template>
  <div
    class="dashboard"
    :class="{ 'is-mounted': isMounted }"
    aria-label="Aegis Security Operations Center — Mission Control"
  >
    <h1 class="sr-only">Aegis Security Operations Center</h1>

    <!-- ── Split panel root ───────────────────────────────────── -->
    <div class="split-panel">

      <!-- ════════════════════════════════════════════════════════
           LEFT PANE: Quick Stats Bar (sticky) + Threat Feed
           ════════════════════════════════════════════════════════ -->
      <section class="pane pane--left" aria-label="Threat monitoring pane">

        <!-- A: Quick Stats Bar — sticky within left pane -->
        <header class="stats-bar" role="region" aria-label="Quick stats">
          <div class="stats-bar__brand">
            <span class="stats-bar__logo">AEGIS</span>
            <span class="stats-bar__sub">SOC</span>
          </div>

          <div class="stats-bar__items">
            <div class="stat-item">
              <span
                class="stat-item__value"
                :class="threatCounts.critical > 0 ? 'stat--critical' : 'stat--neutral'"
                :aria-label="`${threatCounts.critical} critical threats`"
              >{{ threatCounts.critical }}</span>
              <span class="stat-item__label">Critical</span>
            </div>
            <div class="stat-divider" aria-hidden="true"></div>
            <div class="stat-item">
              <span
                class="stat-item__value stat--threat"
                :aria-label="`${threatCounts.total} total threats`"
              >{{ threatCounts.total }}</span>
              <span class="stat-item__label">Threats</span>
            </div>
            <div class="stat-divider" aria-hidden="true"></div>
            <div class="stat-item">
              <span class="stat-item__value stat--secured" aria-label="Mean response time">187ms</span>
              <span class="stat-item__label">Response</span>
            </div>
            <div class="stat-divider" aria-hidden="true"></div>
            <div class="stat-item">
              <span
                class="stat-item__value stat--online"
                :aria-label="`${agentCounts.online} of ${agentCounts.total} agents online`"
              >{{ agentCounts.online }}/{{ agentCounts.total }}</span>
              <span class="stat-item__label">Agents</span>
            </div>
          </div>

          <div class="stats-bar__live">
            <!-- CSS-only pulse — no JS interval for visual blink -->
            <span class="live-dot" aria-hidden="true"></span>
            <span class="stats-bar__live-text">LIVE</span>
          </div>
        </header>

        <!-- B: Real-Time Threat Feed — scrollable body -->
        <div class="threat-feed" role="region" aria-label="Real-time threat feed">
          <div class="threat-feed__header">
            <h2 class="threat-feed__title">Threat Feed</h2>
            <span class="threat-feed__count" :aria-label="`${threats.length} detections`">
              {{ threats.length }} detections
            </span>
          </div>

          <!-- Table header -->
          <div class="feed-cols feed-cols--head" aria-hidden="true">
            <span>Severity</span>
            <span>Threat</span>
            <span>System</span>
            <span>Time</span>
          </div>

          <ul class="threat-list" role="list" aria-label="Recent threat detections">
            <li
              v-for="(threat, i) in threats"
              :key="threat.id"
              class="threat-row"
              :class="[
                `threat-row--${threat.severity.toLowerCase()}`,
                { 'threat-row--new': threat.isNew }
              ]"
              :style="{ '--stagger-delay': `${i * 20}ms` }"
              :aria-label="`${threat.severity}: ${threat.name} on ${threat.system}, ${threat.ts}`"
            >
              <div class="threat-row__severity">
                <span
                  class="severity-dot"
                  :class="`severity-dot--${threat.severity.toLowerCase()}`"
                  aria-hidden="true"
                ></span>
                <span class="badge" :class="`badge--${threat.severity.toLowerCase()}`">
                  {{ threat.severity }}
                </span>
              </div>
              <span class="threat-row__name">{{ threat.name }}</span>
              <span class="threat-row__system">{{ threat.system }}</span>
              <span class="threat-row__ts">{{ threat.ts }}</span>
            </li>
          </ul>
        </div>

      </section><!-- /pane--left -->

      <!-- ════════════════════════════════════════════════════════
           RIGHT PANE: Gauge + Agent Status + Incidents
           ════════════════════════════════════════════════════════ -->
      <section class="pane pane--right" aria-label="Command status pane">

        <!-- C: Defense Posture Gauge -->
        <div class="card gauge-card" aria-label="Defense posture gauge">
          <div class="card__header">
            <h2 class="card__title">Defense Posture</h2>
            <span class="gauge-card__badge" aria-label="83% systems secured">
              <span class="gauge-card__badge-dot" aria-hidden="true"></span>
              Secured
            </span>
          </div>

          <div class="gauge-card__body">
            <div class="gauge-wrap" :aria-label="`${posturePercent}% systems secured`">
              <svg class="gauge-svg" viewBox="0 0 220 220" aria-hidden="true">
                <defs>
                  <linearGradient id="v3GaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <!-- Fixed brand gradient order: error → accent → primary (red → crimson → white) -->
                    <stop offset="0%"   stop-color="var(--brand-error)"   />
                    <stop offset="40%"  stop-color="var(--brand-accent)"  />
                    <stop offset="100%" stop-color="var(--brand-primary)" />
                  </linearGradient>
                </defs>
                <circle
                  class="gauge-track"
                  cx="110" cy="110"
                  :r="gaugeRadius"
                  fill="none"
                  stroke-width="14"
                />
                <circle
                  class="gauge-fill"
                  cx="110" cy="110"
                  :r="gaugeRadius"
                  fill="none"
                  stroke="url(#v3GaugeGrad)"
                  stroke-width="14"
                  stroke-linecap="round"
                  :stroke-dasharray="gaugeCircumference"
                  :stroke-dashoffset="gaugeDashOffset"
                  transform="rotate(-90 110 110)"
                />
              </svg>
              <div class="gauge-center" aria-hidden="true">
                <span class="gauge-center__pct">{{ posturePercent }}%</span>
                <span class="gauge-center__label">Systems Secured</span>
                <span class="gauge-center__count">847 / 1,024</span>
              </div>
            </div>

            <div class="gauge-card__meta">
              <div class="gauge-meta-stat">
                <span class="gauge-meta-stat__val">+4.2%</span>
                <span class="gauge-meta-stat__lbl">vs. 24h ago</span>
              </div>
              <div class="gauge-meta-stat">
                <span class="gauge-meta-stat__val gauge-meta-stat__val--threat">17</span>
                <span class="gauge-meta-stat__lbl">Unsecured</span>
              </div>
              <div class="gauge-meta-stat">
                <span class="gauge-meta-stat__val">2h 14m</span>
                <span class="gauge-meta-stat__lbl">Longest Open</span>
              </div>
            </div>
          </div>
        </div>

        <!-- D: Agent Team Status Panel -->
        <div class="card agents-card" role="region" aria-label="Agent team status">
          <div class="card__header">
            <h2 class="card__title">Agent Teams</h2>
            <span class="agents-card__summary">
              {{ agentCounts.online }}/{{ agentCounts.total }} online
              <span v-if="agentCounts.responding > 0" class="agents-card__responding">
                · {{ agentCounts.responding }} responding
              </span>
            </span>
          </div>

          <ul class="agents-list" role="list" aria-label="Individual agent status">
            <li
              v-for="agent in agents"
              :key="agent.name"
              class="agent-row"
              :class="`agent-row--${agent.status}`"
              role="listitem"
              :aria-label="`${agent.name}: ${agent.status}, uptime ${agent.uptime}, ${agent.neutralized} threats neutralized`"
            >
              <div class="agent-row__left">
                <span
                  class="agent-dot"
                  :class="`agent-dot--${agent.status}`"
                  aria-hidden="true"
                ></span>
                <div class="agent-info">
                  <span class="agent-info__name">{{ agent.name }}</span>
                  <span class="agent-info__role">{{ agent.role }}</span>
                </div>
              </div>
              <div class="agent-row__right">
                <div class="agent-stat">
                  <span
                    class="agent-stat__val"
                    :class="{
                      'agent-stat__val--offline':    agent.status === 'offline',
                      'agent-stat__val--responding': agent.status === 'responding',
                      'agent-stat__val--active':     agent.status === 'active',
                      'agent-stat__val--idle':       agent.status === 'idle',
                    }"
                  >{{ agent.uptime }}</span>
                  <span class="agent-stat__lbl">Uptime</span>
                </div>
                <div class="agent-stat">
                  <span class="agent-stat__val agent-stat__val--neutral">{{ agent.neutralized }}</span>
                  <span class="agent-stat__lbl">Neutralized</span>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- E: Active Incidents Summary -->
        <div class="card incidents-card" role="region" aria-label="Active incidents summary">
          <div class="card__header">
            <h2 class="card__title">Active Incidents</h2>
            <span
              class="incidents-card__count-badge"
              :class="activeIncidents.length > 0 ? 'count-badge--threat' : 'count-badge--clear'"
              :aria-label="`${activeIncidents.length} open incidents`"
            >{{ activeIncidents.length }}</span>
          </div>

          <div class="incidents-overview">
            <div class="incidents-hero">
              <span
                class="incidents-hero__count"
                :class="activeIncidents.length > 0 ? 'hero-count--threat' : 'hero-count--secured'"
              >{{ activeIncidents.length }}</span>
              <div class="incidents-hero__detail">
                <span class="incidents-hero__label">Open Incidents</span>
                <svg class="sparkline" viewBox="0 0 100 50" aria-hidden="true" preserveAspectRatio="none">
                  <path
                    class="sparkline__path"
                    :d="sparklinePath"
                    fill="none"
                    stroke-width="2"
                    stroke-linecap="round"
                  />
                </svg>
              </div>
            </div>

            <div class="sev-pills" role="list" aria-label="Incidents by severity">
              <div class="sev-pill sev-pill--critical" role="listitem">
                <span class="sev-pill__count">{{ severityCounts.CRITICAL }}</span>
                <span class="sev-pill__lbl">Critical</span>
              </div>
              <div class="sev-pill sev-pill--high" role="listitem">
                <span class="sev-pill__count">{{ severityCounts.HIGH }}</span>
                <span class="sev-pill__lbl">High</span>
              </div>
              <div class="sev-pill sev-pill--medium" role="listitem">
                <span class="sev-pill__count">{{ severityCounts.MEDIUM }}</span>
                <span class="sev-pill__lbl">Medium</span>
              </div>
            </div>
          </div>

          <ul
            v-if="activeIncidents.length > 0"
            class="incident-list"
            role="list"
            aria-label="Open incident details"
          >
            <li
              v-for="inc in activeIncidents"
              :key="inc.id"
              class="incident-row"
              :class="`incident-row--${inc.severity.toLowerCase()}`"
              :aria-label="`${inc.severity}: ${inc.title}, opened ${inc.openedAt}`"
            >
              <span class="inc-badge" :class="`inc-badge--${inc.severity.toLowerCase()}`">
                {{ inc.severity }}
              </span>
              <span class="inc-title">{{ inc.title }}</span>
              <span class="inc-time">{{ inc.openedAt }}</span>
            </li>
          </ul>

          <div v-else class="incidents-clear" aria-label="No active incidents — systems secured">
            <span class="incidents-clear__text">All clear — no active incidents</span>
          </div>
        </div>

      </section><!-- /pane--right -->
    </div><!-- /split-panel -->
  </div>
</template>

<style scoped>
/* ── Reset ────────────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* ── Accessibility utilities ─────────────────────────────────── */
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

/* ── Dashboard root — mount fade ─────────────────────────────── */
.dashboard {
  height: 100vh;
  overflow: hidden;
  background-color: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  opacity: 0;
  transition: opacity var(--duration-normal) var(--easing);
}

.dashboard.is-mounted {
  opacity: 1;
}

/* ── Split panel grid — the structural differentiator vs v1/v2 ── */
.split-panel {
  display: grid;
  grid-template-columns: 55fr 45fr;
  height: 100%;
  max-width: var(--container-max);
  margin: 0 auto;
}

@media (max-width: 768px) {
  .dashboard {
    height: auto;
    overflow: visible;
  }

  .split-panel {
    grid-template-columns: 1fr;
    height: auto;
  }
}

/* ── Pane base ────────────────────────────────────────────────── */
.pane {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.pane--left {
  border-right: 1px solid var(--brand-border);
  overflow: hidden;
}

.pane--right {
  overflow-y: auto;
  padding: calc(var(--space-unit) * 5);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 5);
}

@media (max-width: 768px) {
  .pane--left,
  .pane--right {
    overflow: visible;
  }

  .pane--left {
    border-right: none;
    border-bottom: 1px solid var(--brand-border);
  }
}

/* ════════════════════════════════════════════════════════════════
   LEFT PANE: A — Quick Stats Bar (sticky within pane)
   ════════════════════════════════════════════════════════════════ */
.stats-bar {
  position: sticky;
  top: 0;
  z-index: 10;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  padding: 0 calc(var(--space-unit) * 5);
  height: calc(var(--space-unit) * 14);
  background: linear-gradient(180deg, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 90%, var(--brand-bg)));
  border-bottom: 1px solid var(--brand-border);
  box-shadow: var(--shadow-md);
}

.stats-bar__brand {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 1.5);
  flex-shrink: 0;
}

.stats-bar__logo {
  font-family: var(--font-mono);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
}

.stats-bar__sub {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.stats-bar__items {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  flex: 1;
}

.stat-divider {
  width: 1px;
  height: calc(var(--space-unit) * 5);
  background-color: var(--brand-border);
  flex-shrink: 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.stat-item__value {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1;
}

/* Semantic stat color classes */
.stat--critical { color: var(--brand-error);     }
.stat--threat   { color: var(--brand-accent);    }
.stat--secured  { color: var(--brand-primary);   }
.stat--online   { color: var(--brand-secondary); }
.stat--neutral  { color: var(--brand-text);      }

.stat-item__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.stats-bar__live {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
  flex-shrink: 0;
}

/* CSS-only live dot — uses @keyframes pulse, no JS interval */
.live-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  background-color: var(--brand-error);
  animation: pulse 1.5s var(--easing) infinite;
  flex-shrink: 0;
}

.stats-bar__live-text {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--brand-error);
}

/* ════════════════════════════════════════════════════════════════
   LEFT PANE: B — Real-Time Threat Feed (scrollable body)
   ════════════════════════════════════════════════════════════════ */
.threat-feed {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.threat-feed__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
  flex-shrink: 0;
}

.threat-feed__title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: var(--brand-text);
  margin: 0;
}

.threat-feed__count {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

/* Feed column header */
.feed-cols {
  display: grid;
  grid-template-columns: 100px 1fr 150px 70px;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 2.5) calc(var(--space-unit) * 5);
  flex-shrink: 0;
}

.feed-cols--head {
  background-color: var(--brand-bg-secondary);
  border-top: 1px solid var(--brand-border);
  border-bottom: 1px solid var(--brand-border);
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Threat list */
.threat-list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
}

.threat-row {
  display: grid;
  grid-template-columns: 100px 1fr 150px 70px;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 5);
  border-bottom: 1px solid var(--brand-border);
  /* threat-enter fires on initial render; stagger via CSS custom property */
  animation: threat-enter var(--duration-normal) var(--easing) both;
  animation-delay: var(--stagger-delay, 0ms);
  transition: background-color var(--duration-fast) var(--easing);
  cursor: default;
}

.threat-row:last-child {
  border-bottom: none;
}

.threat-row:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 80%, var(--brand-accent));
}

/* New incoming threat rows re-animate on prepend */
.threat-row--new {
  animation: threat-enter var(--duration-normal) var(--easing) both;
  animation-delay: 0ms;
}

/* Severity row left-border accent */
.threat-row--critical {
  border-left: 3px solid var(--brand-error);
}

.threat-row--high {
  border-left: 3px solid var(--brand-accent);
}

.threat-row--medium {
  border-left: 3px solid color-mix(in srgb, var(--brand-accent) 50%, transparent);
}

.threat-row--low {
  border-left: 3px solid var(--brand-secondary);
}

/* Severity dot + badge combo */
.threat-row__severity {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
}

.severity-dot {
  width: calc(var(--space-unit) * 1.5);
  height: calc(var(--space-unit) * 1.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.severity-dot--critical {
  background-color: var(--brand-error);
  animation: pulse 1.5s var(--easing) infinite;
}

.severity-dot--high {
  background-color: var(--brand-accent);
}

.severity-dot--medium {
  background-color: var(--brand-secondary);
}

.severity-dot--low {
  background-color: var(--brand-secondary);
}

/* Severity badges */
.badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  flex-shrink: 0;
  white-space: nowrap;
}

.badge--critical { background-color: var(--brand-error);  color: var(--brand-bg); }
.badge--high     { background-color: var(--brand-accent); color: var(--brand-bg); }
.badge--medium   {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text);
}
.badge--low      { background-color: var(--brand-secondary); color: var(--brand-bg); }

.threat-row__name {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.threat-row__system {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.threat-row__ts {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);
  white-space: nowrap;
  text-align: right;
}

/* ════════════════════════════════════════════════════════════════
   Card base (right pane shared)
   ════════════════════════════════════════════════════════════════ */
.card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  flex-shrink: 0;
}

.card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
  border-bottom: 1px solid var(--brand-border);
}

.card__title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--brand-text);
  margin: 0;
}

/* ════════════════════════════════════════════════════════════════
   RIGHT PANE: C — Defense Posture Gauge
   ════════════════════════════════════════════════════════════════ */
.gauge-card__badge {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-primary);
}

.gauge-card__badge-dot {
  width: calc(var(--space-unit) * 1.5);
  height: calc(var(--space-unit) * 1.5);
  border-radius: 50%;
  background-color: var(--brand-primary);
  /* CSS-only pulse on secured state dot */
  animation: pulse 2s var(--easing) infinite;
}

.gauge-card__body {
  padding: calc(var(--space-unit) * 5);
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 6);
}

.gauge-wrap {
  position: relative;
  width: 180px;
  height: 180px;
  flex-shrink: 0;
}

.gauge-svg {
  width: 100%;
  height: 100%;
}

.gauge-track {
  stroke: var(--brand-border);
}

.gauge-fill {
  transition: stroke-dashoffset var(--duration-slow) var(--easing);
}

.gauge-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 0.75);
}

.gauge-center__pct {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brand-primary);
}

.gauge-center__label {
  font-family: var(--font-body);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
  text-align: center;
}

.gauge-center__count {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-text);
}

.gauge-card__meta {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 4);
}

.gauge-meta-stat {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.gauge-meta-stat__val {
  font-family: var(--font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--brand-primary);
}

.gauge-meta-stat__val--threat {
  color: var(--brand-accent);
}

.gauge-meta-stat__lbl {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ════════════════════════════════════════════════════════════════
   RIGHT PANE: D — Agent Team Status Panel
   ════════════════════════════════════════════════════════════════ */
.agents-card__summary {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
}

.agents-card__responding {
  color: var(--brand-accent);
}

.agents-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.agent-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 5);
  border-bottom: 1px solid var(--brand-border);
  transition: background-color var(--duration-fast) var(--easing);
}

.agent-row:last-child {
  border-bottom: none;
}

.agent-row:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 60%, var(--brand-bg-secondary));
}

.agent-row__left {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

/* Agent status dots */
.agent-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

/* ACTIVE = white/secured */
.agent-dot--active { background-color: var(--brand-primary); }
/* IDLE = blue/supporting */
.agent-dot--idle { background-color: var(--brand-secondary); }
/* OFFLINE = red/down */
.agent-dot--offline { background-color: var(--brand-error); }
/* RESPONDING = crimson + pulse (active threat response) */
.agent-dot--responding {
  background-color: var(--brand-accent);
  animation: pulse 1.5s var(--easing) infinite;
}

.agent-info {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.agent-info__name {
  font-family: var(--font-heading);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
}

.agent-info__role {
  font-family: var(--font-body);
  font-size: 0.6875rem;
  color: var(--brand-muted);
}

.agent-row__right {
  display: flex;
  gap: calc(var(--space-unit) * 5);
}

.agent-stat {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: calc(var(--space-unit) * 0.5);
}

.agent-stat__val {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  line-height: 1;
}

/* Uptime value semantic colors */
.agent-stat__val--active     { color: var(--brand-primary);   }
.agent-stat__val--idle       { color: var(--brand-secondary); }
.agent-stat__val--offline    { color: var(--brand-error);     }
.agent-stat__val--responding { color: var(--brand-accent);    }
.agent-stat__val--neutral    { color: var(--brand-text);      }

.agent-stat__lbl {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ════════════════════════════════════════════════════════════════
   RIGHT PANE: E — Active Incidents Summary
   ════════════════════════════════════════════════════════════════ */
.incidents-card__count-badge {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2.5);
  border-radius: var(--radius-sm);
}

.count-badge--threat {
  background-color: color-mix(in srgb, var(--brand-accent) 20%, transparent);
  color: var(--brand-accent);
  border: 1px solid color-mix(in srgb, var(--brand-accent) 40%, transparent);
}

.count-badge--clear {
  background-color: color-mix(in srgb, var(--brand-primary) 15%, transparent);
  color: var(--brand-primary);
  border: 1px solid color-mix(in srgb, var(--brand-primary) 30%, transparent);
}

.incidents-overview {
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 5);
  border-bottom: 1px solid var(--brand-border);
}

.incidents-hero {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  flex-shrink: 0;
}

.incidents-hero__count {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.hero-count--threat   { color: var(--brand-accent);  }
/* white = all clear / secured */
.hero-count--secured  { color: var(--brand-primary); }

.incidents-hero__detail {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.incidents-hero__label {
  font-family: var(--font-body);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--brand-muted);
}

.sparkline {
  width: 80px;
  height: 36px;
}

.sparkline__path {
  stroke: var(--brand-accent);
}

/* Severity pills */
.sev-pills {
  display: flex;
  gap: calc(var(--space-unit) * 2);
  margin-left: auto;
}

.sev-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 0.75);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  border-radius: var(--radius-md);
  min-width: calc(var(--space-unit) * 12);
}

.sev-pill--critical {
  background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-error) 40%, transparent);
}

.sev-pill--high {
  background-color: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-accent) 40%, transparent);
}

.sev-pill--medium {
  background-color: color-mix(in srgb, var(--brand-secondary) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-secondary) 30%, transparent);
}

.sev-pill__count {
  font-family: var(--font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--brand-text);
  line-height: 1;
}

.sev-pill__lbl {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Incident list rows */
.incident-list {
  list-style: none;
  margin: 0;
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 5);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1.5);
}

.incident-row {
  display: grid;
  grid-template-columns: 80px 1fr auto;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 2.5) calc(var(--space-unit) * 3);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  border-left: 3px solid transparent;
  transition: background-color var(--duration-fast) var(--easing);
}

.incident-row--critical { border-left-color: var(--brand-error);     }
.incident-row--high     { border-left-color: var(--brand-accent);    }
.incident-row--medium   { border-left-color: var(--brand-secondary); }
/* resolved state: white left-border = secured */
.incident-row--resolved { border-left-color: var(--brand-primary);   }

.incident-row:hover {
  background-color: color-mix(in srgb, var(--brand-bg-secondary) 70%, var(--brand-surface));
}

.inc-badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  text-align: center;
}

.inc-badge--critical { background-color: var(--brand-error);  color: var(--brand-bg); }
.inc-badge--high     { background-color: var(--brand-accent); color: var(--brand-bg); }
.inc-badge--medium   {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text);
}

.inc-title {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--brand-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.inc-time {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);
  white-space: nowrap;
}

/* All clear state — white = secured brand narrative */
.incidents-clear {
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.incidents-clear__text {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--brand-primary);
  letter-spacing: 0.03em;
}

/* ════════════════════════════════════════════════════════════════
   KEYFRAMES — all brand token timing and easing
   ════════════════════════════════════════════════════════════════ */

/* Pulse — CRITICAL dots, RESPONDING agent dot, secured badge dot */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(0.85);
  }
}

/* Threat row entrance — fires on initial render and on new prepended rows */
@keyframes threat-enter {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ════════════════════════════════════════════════════════════════
   ACCESSIBILITY — reduced-motion guard (always last rule)
   ════════════════════════════════════════════════════════════════ */
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

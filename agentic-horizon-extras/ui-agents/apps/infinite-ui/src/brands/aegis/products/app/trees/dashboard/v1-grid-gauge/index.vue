<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/dashboard/v1-grid-gauge
// Layout: sticky stats bar top, left col gauge hero (~35%), right col threat feed + incidents + agents (2×2 grid)

// ── Types ────────────────────────────────────────────────────────
interface ThreatEntry {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  system: string
  ts: string
}

interface Agent {
  name: string
  role: string
  status: 'active' | 'idle' | 'offline'
  uptime: string
  neutralized: number
}

interface Incident {
  id: number
  title: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  openedAt: string
}

// ── Static data ──────────────────────────────────────────────────
const posturePercent = ref(83)

const threats = ref<ThreatEntry[]>([
  { id: 1,  name: 'Prompt Injection — GPT-4 endpoint',  severity: 'CRITICAL', system: 'api-gateway-01',   ts: '0s ago'  },
  { id: 2,  name: 'Data Exfiltration attempt',           severity: 'HIGH',     system: 'llm-worker-07',   ts: '12s ago' },
  { id: 3,  name: 'Privilege Escalation — Agent token',  severity: 'CRITICAL', system: 'orchestrator-02', ts: '34s ago' },
  { id: 4,  name: 'Model Poisoning probe',               severity: 'HIGH',     system: 'fine-tune-03',    ts: '1m ago'  },
  { id: 5,  name: 'Unusual API call pattern',            severity: 'MEDIUM',   system: 'api-gateway-02',  ts: '2m ago'  },
  { id: 6,  name: 'Repeated auth failure',               severity: 'MEDIUM',   system: 'auth-service',    ts: '3m ago'  },
  { id: 7,  name: 'Unrecognized tool invocation',        severity: 'LOW',      system: 'agent-runner-05', ts: '4m ago'  },
  { id: 8,  name: 'Context window overflow probe',       severity: 'MEDIUM',   system: 'llm-worker-02',   ts: '6m ago'  },
  { id: 9,  name: 'Rate limit bypass attempt',           severity: 'HIGH',     system: 'rate-limiter-01', ts: '8m ago'  },
  { id: 10, name: 'Jailbreak attempt — system prompt',   severity: 'CRITICAL', system: 'llm-worker-04',   ts: '9m ago'  },
])

const agents: Agent[] = [
  { name: 'Scanner',   role: 'Vulnerability scanning',  status: 'active',  uptime: '99.97%', neutralized: 142 },
  { name: 'Monitor',   role: 'Traffic analysis',         status: 'active',  uptime: '99.91%', neutralized: 87  },
  { name: 'Responder', role: 'Threat containment',       status: 'active',  uptime: '99.85%', neutralized: 203 },
  { name: 'Sentinel',  role: 'Perimeter watch',          status: 'idle',    uptime: '98.40%', neutralized: 56  },
]

const incidents = ref<Incident[]>([
  { id: 1, title: 'Prompt injection campaign — api-gateway cluster',   severity: 'CRITICAL', openedAt: '14 min ago' },
  { id: 2, title: 'Exfiltration attempt — llm-worker-07',              severity: 'HIGH',     openedAt: '22 min ago' },
  { id: 3, title: 'Token privilege escalation — orchestrator-02',      severity: 'CRITICAL', openedAt: '41 min ago' },
  { id: 4, title: 'Model poisoning probe — fine-tune cluster',          severity: 'HIGH',     openedAt: '1h ago'     },
  { id: 5, title: 'Anomalous call pattern — api-gateway-02',           severity: 'MEDIUM',   openedAt: '2h ago'     },
])

// Sparkline SVG points (24h history, descending trend)
const sparklinePath = 'M0,40 L10,38 L20,42 L30,35 L40,30 L50,28 L60,22 L70,25 L80,18 L90,15 L100,12'

// ── Computed ──────────────────────────────────────────────────────
const severityCounts = computed(() => ({
  CRITICAL: incidents.value.filter(i => i.severity === 'CRITICAL').length,
  HIGH:     incidents.value.filter(i => i.severity === 'HIGH').length,
  MEDIUM:   incidents.value.filter(i => i.severity === 'MEDIUM').length,
}))

// SVG arc gauge
const gaugeRadius = 90
const gaugeCircumference = 2 * Math.PI * gaugeRadius
const gaugeDashOffset = computed(() =>
  gaugeCircumference * (1 - posturePercent.value / 100)
)

// ── Live pulse for feed header ─────────────────────────────────
const pulseVisible = ref(true)
let pulseInterval: ReturnType<typeof setInterval> | null = null

// ── Mount ────────────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  nextTick(() => { isMounted.value = true })
  pulseInterval = setInterval(() => {
    pulseVisible.value = !pulseVisible.value
  }, 800)
})

onUnmounted(() => {
  if (pulseInterval !== null) clearInterval(pulseInterval)
})
</script>

<template>
  <div class="dashboard" :class="{ 'is-mounted': isMounted }" aria-label="Aegis Security Operations Dashboard">
    <h1 class="sr-only">Aegis Security Operations Dashboard</h1>

    <!-- ── A: Quick Stats Bar ─────────────────────────────────── -->
    <header class="stats-bar" role="banner" aria-label="Quick stats">
      <div class="stats-bar__inner">
        <div class="stats-bar__brand">
          <span class="stats-bar__logo-label">AEGIS</span>
          <span class="stats-bar__sub">Platform</span>
        </div>
        <div class="stats-bar__items">
          <div class="stat-item">
            <span class="stat-item__value stat-item__value--threat" aria-label="Total threats today">247</span>
            <span class="stat-item__label">Threats Today</span>
          </div>
          <div class="stat-divider" aria-hidden="true"></div>
          <div class="stat-item">
            <span class="stat-item__value stat-item__value--secured" aria-label="Mean response time">187ms</span>
            <span class="stat-item__label">Mean Response</span>
          </div>
          <div class="stat-divider" aria-hidden="true"></div>
          <div class="stat-item">
            <span class="stat-item__value stat-item__value--online" aria-label="Agents online">3/4</span>
            <span class="stat-item__label">Agents Online</span>
          </div>
        </div>
        <div class="stats-bar__time">
          <span class="stats-bar__timestamp">Live — updated just now</span>
        </div>
      </div>
    </header>

    <!-- ── Main layout: left gauge | right content ───────────── -->
    <main class="dashboard__main">

      <!-- LEFT: Gauge hero -->
      <aside class="gauge-pane" aria-label="Defense posture gauge">
        <div class="gauge-card">
          <div class="gauge-card__header">
            <h2 class="gauge-card__title">Defense Posture</h2>
            <span class="gauge-card__live-badge" :class="{ 'is-pulse': pulseVisible }" aria-hidden="true"></span>
          </div>

          <!-- SVG Ring Gauge -->
          <div class="gauge-ring-wrap" :aria-label="`${posturePercent}% systems secured`">
            <svg class="gauge-ring" viewBox="0 0 220 220" aria-hidden="true">
              <defs>
                <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%"   stop-color="var(--brand-error)"  />
                  <stop offset="40%"  stop-color="var(--brand-accent)" />
                  <stop offset="100%" stop-color="var(--brand-primary)"/>
                </linearGradient>
              </defs>
              <!-- Track -->
              <circle
                class="gauge-track"
                cx="110" cy="110"
                :r="gaugeRadius"
                fill="none"
                stroke-width="14"
              />
              <!-- Fill arc -->
              <circle
                class="gauge-fill"
                cx="110" cy="110"
                :r="gaugeRadius"
                fill="none"
                stroke="url(#gaugeGrad)"
                stroke-width="14"
                stroke-linecap="round"
                :stroke-dasharray="gaugeCircumference"
                :stroke-dashoffset="gaugeDashOffset"
                transform="rotate(-90 110 110)"
              />
            </svg>
            <!-- Center readout -->
            <div class="gauge-center">
              <span class="gauge-center__pct">{{ posturePercent }}%</span>
              <span class="gauge-center__label">Systems Secured</span>
              <span class="gauge-center__count">847 / 1,024 systems</span>
            </div>
          </div>

          <div class="gauge-card__footer">
            <span class="gauge-card__status-text">Posture trending upward vs. 24h ago</span>
          </div>
        </div>
      </aside>

      <!-- RIGHT: content column -->
      <div class="content-pane">

        <!-- B: Threat Feed -->
        <section class="card threat-feed" aria-label="Real-time threat feed">
          <div class="card__header">
            <div class="card__header-left">
              <span
                class="live-dot"
                :class="{ 'is-pulse': pulseVisible }"
                aria-hidden="true"
              ></span>
              <h2 class="card__title">Threat Feed</h2>
            </div>
            <span class="card__count">{{ threats.length }} detections</span>
          </div>

          <ul class="threat-list" role="list" aria-label="Recent threat detections">
            <li
              v-for="threat in threats"
              :key="threat.id"
              class="threat-row"
              :class="`threat-row--${threat.severity.toLowerCase()}`"
            >
              <span class="threat-row__badge" :class="`badge--${threat.severity.toLowerCase()}`">
                {{ threat.severity }}
              </span>
              <span class="threat-row__name">{{ threat.name }}</span>
              <span class="threat-row__system">{{ threat.system }}</span>
              <span class="threat-row__ts">{{ threat.ts }}</span>
            </li>
          </ul>
        </section>

        <!-- Bottom row: D incidents + C agents -->
        <div class="bottom-row">

          <!-- D: Active Incidents Summary -->
          <section class="card incidents-card" aria-label="Active incidents summary">
            <div class="card__header">
              <h2 class="card__title">Active Incidents</h2>
              <span class="card__timestamp">Updated just now</span>
            </div>

            <div class="incidents-hero">
              <span
                class="incidents-hero__count"
                :class="incidents.length > 0 ? 'count--threat' : 'count--secured'"
                :aria-label="`${incidents.length} open incidents`"
              >{{ incidents.length }}</span>
              <span class="incidents-hero__label">Open</span>

              <!-- Sparkline SVG -->
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

            <div class="severity-pills" role="list" aria-label="Incidents by severity">
              <div class="severity-pill severity-pill--critical" role="listitem">
                <span class="severity-pill__count">{{ severityCounts.CRITICAL }}</span>
                <span class="severity-pill__label">Critical</span>
              </div>
              <div class="severity-pill severity-pill--high" role="listitem">
                <span class="severity-pill__count">{{ severityCounts.HIGH }}</span>
                <span class="severity-pill__label">High</span>
              </div>
              <div class="severity-pill severity-pill--medium" role="listitem">
                <span class="severity-pill__count">{{ severityCounts.MEDIUM }}</span>
                <span class="severity-pill__label">Medium</span>
              </div>
            </div>
          </section>

          <!-- C: Agent Team Status -->
          <section class="card agents-card" aria-label="Agent team status">
            <div class="card__header">
              <h2 class="card__title">Agent Teams</h2>
            </div>

            <div class="agents-grid" role="list">
              <div
                v-for="agent in agents"
                :key="agent.name"
                class="agent-row"
                :class="`agent-row--${agent.status}`"
                role="listitem"
                :aria-label="`${agent.name}: ${agent.status}, uptime ${agent.uptime}`"
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
                      :class="agent.status === 'offline' ? 'stat-offline' : 'stat-active'"
                    >{{ agent.uptime }}</span>
                    <span class="agent-stat__lbl">Uptime</span>
                  </div>
                  <div class="agent-stat">
                    <span class="agent-stat__val stat-neutral">{{ agent.neutralized }}</span>
                    <span class="agent-stat__lbl">Neutralized</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

        </div><!-- /bottom-row -->
      </div><!-- /content-pane -->
    </main>
  </div>
</template>

<style scoped>
/* ── Reset & base ─────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
}

.dashboard {
  min-height: 100vh;
  background-color: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  display: flex;
  overflow-x: hidden;
  flex-direction: column;
  opacity: 0;
  transition: opacity var(--duration-normal) var(--easing);
}

.dashboard.is-mounted {
  opacity: 1;
}

/* ── A: Stats bar ─────────────────────────────────────────────── */
.stats-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: linear-gradient(180deg, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 85%, var(--brand-bg)));
  border-bottom: 1px solid var(--brand-border);
  box-shadow: var(--shadow-md);
  padding: 0 calc(var(--space-unit) * 6);
}

.stats-bar__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  height: calc(var(--space-unit) * 14);
  display: flex;
  overflow-x: hidden;
  align-items: center;
  gap: calc(var(--space-unit) * 8);
}

.stats-bar__brand {
  display: flex;
  overflow-x: hidden;
  align-items: baseline;
  gap: calc(var(--space-unit) * 2);
  flex-shrink: 0;
}

.stats-bar__logo-label {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
}

.stats-bar__sub {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.stats-bar__items {
  display: flex;
  overflow-x: hidden;
  align-items: center;
  gap: calc(var(--space-unit) * 6);
  flex: 1;
}

.stat-divider {
  width: 1px;
  height: calc(var(--space-unit) * 6);
  background-color: var(--brand-border);
}

.stat-item {
  display: flex;
  overflow-x: hidden;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.stat-item__value {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1;
}

.stat-item__value--threat  { color: var(--brand-accent);    }
.stat-item__value--secured { color: var(--brand-primary);   }
.stat-item__value--online  { color: var(--brand-secondary); }

.stat-item__label {
  font-family: var(--font-body);
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.stats-bar__time {
  margin-left: auto;
}

.stats-bar__timestamp {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

/* ── Main grid layout ─────────────────────────────────────────── */
.dashboard__main {
  max-width: var(--container-max);
  width: 100%;
  margin: 0 auto;
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 6);
  display: grid;
  grid-template-columns: 35% 1fr;
  gap: calc(var(--space-unit) * 6);
  align-items: start;
}

@media (max-width: 768px) {
  .dashboard__main {
    grid-template-columns: 1fr;
    padding: calc(var(--space-unit) * 4);
  }

  .stats-bar__inner {
    height: auto;
    flex-wrap: wrap;
    gap: calc(var(--space-unit) * 2);
    padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  }

  .stats-bar__items {
    flex-wrap: wrap;
    gap: calc(var(--space-unit) * 2);
  }


  .stats-bar__time {
    display: none;
  }
}

/* ── Gauge pane ───────────────────────────────────────────────── */
.gauge-pane {
  position: sticky;
  top: calc(var(--space-unit) * 20);
}

.gauge-card {
  background: linear-gradient(145deg, color-mix(in srgb, var(--brand-primary) 6%, var(--brand-surface)), var(--brand-surface));
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 6);
  box-shadow: var(--shadow-lg);
  display: flex;
  overflow-x: hidden;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
}

.gauge-card__header {
  display: flex;
  overflow-x: hidden;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.gauge-card__title {
  font-family: var(--font-heading);
  font-size: 1.0625rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--brand-text);
  margin: 0;
}

.gauge-card__live-badge {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  background-color: var(--brand-primary);
  transition: opacity var(--duration-fast) var(--easing);
}

.gauge-card__live-badge.is-pulse {
  opacity: 0.3;
}

/* SVG ring */
.gauge-ring-wrap {
  position: relative;
  width: 220px;
  height: 220px;
  flex-shrink: 0;
}

.gauge-ring {
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
  overflow-x: hidden;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 1);
}

.gauge-center__pct {
  font-family: var(--font-mono);
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brand-primary);
}

.gauge-center__label {
  font-family: var(--font-body);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.gauge-center__count {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--brand-text);
}

.gauge-card__footer {
  width: 100%;
  padding-top: calc(var(--space-unit) * 3);
  border-top: 1px solid var(--brand-border);
}

.gauge-card__status-text {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: var(--brand-muted);
  text-align: center;
  display: block;
}

/* ── Content pane ─────────────────────────────────────────────── */
.content-pane {
  display: flex;
  overflow-x: hidden;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
}

/* ── Card base ────────────────────────────────────────────────── */
.card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.card__header {
  display: flex;
  overflow-x: hidden;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
}

.card__header-left {
  display: flex;
  overflow-x: hidden;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.card__title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: var(--brand-text);
  margin: 0;
}

.card__count,
.card__timestamp {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

/* ── B: Live dot ──────────────────────────────────────────────── */
.live-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  background-color: var(--brand-error);
  flex-shrink: 0;
  transition: opacity var(--duration-fast) var(--easing);
}

.live-dot.is-pulse {
  opacity: 0.25;
}

/* ── B: Threat list ───────────────────────────────────────────── */
.threat-list {
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: calc(var(--space-unit) * 45);
  overflow-y: auto;
}

.threat-row {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
  transition: background-color var(--duration-fast) var(--easing);
  cursor: default;
}

.threat-row:last-child {
  border-bottom: none;
}

.threat-row:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 80%, var(--brand-accent));
}

/* Severity badges */
.threat-row__badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.badge--critical {
  background-color: var(--brand-error);
  color: var(--brand-bg);
}

.badge--high {
  background-color: var(--brand-accent);
  color: var(--brand-bg);
}

.badge--medium {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text);
}

.badge--low {
  background-color: var(--brand-secondary);
  color: var(--brand-bg);
}

.threat-row__name {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.threat-row__system {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  white-space: nowrap;
}

.threat-row__ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Bottom row: incidents + agents ──────────────────────────── */
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 6);
}

@media (max-width: 768px) {
  .bottom-row {
    grid-template-columns: 1fr;
  }
}

/* ── D: Incidents card ────────────────────────────────────────── */
.incidents-hero {
  display: flex;
  overflow-x: hidden;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
}

.incidents-hero__count {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.count--threat   { color: var(--brand-accent); }
.count--secured  { color: var(--brand-primary); }

.incidents-hero__label {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--brand-muted);
  margin-right: auto;
}

.sparkline {
  width: 100px;
  height: 50px;
  flex-shrink: 0;
}

.sparkline__path {
  stroke: var(--brand-accent);
}

.severity-pills {
  display: flex;
  overflow-x: hidden;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  border-top: 1px solid var(--brand-border);
}

.severity-pill {
  display: flex;
  overflow-x: hidden;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
  border-radius: var(--radius-md);
  flex: 1;
}

.severity-pill--critical {
  background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-error) 40%, transparent);
}

.severity-pill--high {
  background-color: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-accent) 40%, transparent);
}

.severity-pill--medium {
  background-color: color-mix(in srgb, var(--brand-secondary) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-secondary) 30%, transparent);
}

.severity-pill__count {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--brand-text);
  line-height: 1;
}

.severity-pill__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── C: Agents card ───────────────────────────────────────────── */
.agents-grid {
  padding: calc(var(--space-unit) * 3) 0;
}

.agent-row {
  display: flex;
  overflow-x: hidden;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 6);
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
  overflow-x: hidden;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.agent-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.agent-dot--active  { background-color: var(--brand-primary);   }
.agent-dot--idle    { background-color: var(--brand-secondary);  }
.agent-dot--offline { background-color: var(--brand-error);      }

.agent-info {
  display: flex;
  overflow-x: hidden;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.agent-info__name {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
}

.agent-info__role {
  font-family: var(--font-body);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

.agent-row__right {
  display: flex;
  overflow-x: hidden;
  gap: calc(var(--space-unit) * 5);
}

.agent-stat {
  display: flex;
  overflow-x: hidden;
  flex-direction: column;
  align-items: flex-end;
  gap: calc(var(--space-unit) * 0.5);
}

.agent-stat__val {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  line-height: 1;
}

.stat-active  { color: var(--brand-primary);  }
.stat-offline { color: var(--brand-error);    }
.stat-neutral { color: var(--brand-text);     }

.agent-stat__lbl {
  font-family: var(--font-mono);
  font-size: 0.6125rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── Screen-reader only ──────────────────────────────────────── */
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

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/dashboard/v2-feed-header
// Layout: sticky header (stats + compact gauge ring), then full-width sections stacked vertically

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

// ── Data ─────────────────────────────────────────────────────────
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

// Sparkline SVG
const sparklinePath = 'M0,40 L10,38 L20,42 L30,35 L40,30 L50,28 L60,22 L70,25 L80,18 L90,15 L100,12'

// ── Gauge math ────────────────────────────────────────────────────
const gaugeRadius     = 90
const gaugeCircumference = 2 * Math.PI * gaugeRadius
const gaugeDashOffset = computed(() =>
  gaugeCircumference * (1 - posturePercent.value / 100)
)

// Compact header gauge (40px, r=17)
const miniRadius         = 17
const miniCircumference  = 2 * Math.PI * miniRadius
const miniDashOffset     = computed(() =>
  miniCircumference * (1 - posturePercent.value / 100)
)

// ── Severity counts ───────────────────────────────────────────────
const severityCounts = computed(() => ({
  CRITICAL: incidents.value.filter(i => i.severity === 'CRITICAL').length,
  HIGH:     incidents.value.filter(i => i.severity === 'HIGH').length,
  MEDIUM:   incidents.value.filter(i => i.severity === 'MEDIUM').length,
}))

// ── Pulse ─────────────────────────────────────────────────────────
const pulseVisible = ref(true)
let pulseInterval: ReturnType<typeof setInterval> | null = null

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
  <div class="dashboard" :class="{ 'is-mounted': isMounted }" aria-label="Aegis Security Operations Dashboard — Feed View">
    <h1 class="sr-only">Aegis Security Operations Dashboard</h1>

    <!-- ── Sticky header: stats + compact gauge ring ──────────── -->
    <header class="sticky-header" role="banner" aria-label="Stats header">
      <div class="sticky-header__inner">

        <div class="sticky-header__brand">
          <span class="brand-word">AEGIS</span>
          <span class="brand-sub">Platform</span>
        </div>

        <!-- 3 quick stats -->
        <div class="hdr-stats">
          <div class="hdr-stat">
            <span class="hdr-stat__val hdr-stat__val--threat">247</span>
            <span class="hdr-stat__lbl">Threats Today</span>
          </div>
          <div class="hdr-divider" aria-hidden="true"></div>
          <div class="hdr-stat">
            <span class="hdr-stat__val hdr-stat__val--secured">187ms</span>
            <span class="hdr-stat__lbl">Mean Response</span>
          </div>
          <div class="hdr-divider" aria-hidden="true"></div>
          <div class="hdr-stat">
            <span class="hdr-stat__val hdr-stat__val--online">3/4</span>
            <span class="hdr-stat__lbl">Agents Online</span>
          </div>
        </div>

        <!-- Compact gauge ring (40px) -->
        <div class="mini-gauge" :aria-label="`${posturePercent}% systems secured`">
          <svg class="mini-gauge__svg" viewBox="0 0 42 42" aria-hidden="true">
            <defs>
              <linearGradient id="miniGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%"   stop-color="var(--brand-error)"   />
                <stop offset="40%"  stop-color="var(--brand-accent)"  />
                <stop offset="100%" stop-color="var(--brand-primary)" />
              </linearGradient>
            </defs>
            <circle class="mini-track" cx="21" cy="21" :r="miniRadius" fill="none" stroke-width="3" />
            <circle
              class="mini-fill"
              cx="21" cy="21"
              :r="miniRadius"
              fill="none"
              stroke="url(#miniGrad)"
              stroke-width="3"
              stroke-linecap="round"
              :stroke-dasharray="miniCircumference"
              :stroke-dashoffset="miniDashOffset"
              transform="rotate(-90 21 21)"
            />
          </svg>
          <span class="mini-gauge__pct">{{ posturePercent }}%</span>
        </div>

      </div>
    </header>

    <!-- ── Scrollable body ─────────────────────────────────────── -->
    <main class="dashboard__body">
      <div class="body__inner">

        <!-- A: Large gauge card (full-width, centered) -->
        <section class="card gauge-section" aria-label="Defense posture gauge">
          <div class="card__header">
            <h2 class="card__title">Defense Posture</h2>
            <span
              class="live-badge"
              :class="{ 'is-pulse': pulseVisible }"
              aria-hidden="true"
            ></span>
          </div>

          <div class="gauge-section__body">
            <div class="gauge-wrap" :aria-label="`${posturePercent}% systems secured`">
              <svg class="gauge-svg" viewBox="0 0 220 220" aria-hidden="true">
                <defs>
                  <linearGradient id="gaugeGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%"   stop-color="var(--brand-error)"   />
                    <stop offset="40%"  stop-color="var(--brand-accent)"  />
                    <stop offset="100%" stop-color="var(--brand-primary)" />
                  </linearGradient>
                </defs>
                <circle class="gauge-track" cx="110" cy="110" :r="gaugeRadius" fill="none" stroke-width="16" />
                <circle
                  class="gauge-fill"
                  cx="110" cy="110"
                  :r="gaugeRadius"
                  fill="none"
                  stroke="url(#gaugeGrad2)"
                  stroke-width="16"
                  stroke-linecap="round"
                  :stroke-dasharray="gaugeCircumference"
                  :stroke-dashoffset="gaugeDashOffset"
                  transform="rotate(-90 110 110)"
                />
              </svg>
              <div class="gauge-center" aria-hidden="true">
                <span class="gauge-center__pct">{{ posturePercent }}%</span>
                <span class="gauge-center__lbl">Systems Secured</span>
                <span class="gauge-center__count">847 / 1,024 systems</span>
              </div>
            </div>

            <div class="gauge-section__meta">
              <p class="gauge-meta__desc">
                Current defense posture is <strong>strong</strong>. 3 of 4 agent teams are actively neutralizing threats.
                Sentinel is on standby — coverage maintained at full-spectrum.
              </p>
              <div class="gauge-meta__stats">
                <div class="meta-stat">
                  <span class="meta-stat__val">+4.2%</span>
                  <span class="meta-stat__lbl">vs. 24h ago</span>
                </div>
                <div class="meta-stat">
                  <span class="meta-stat__val meta-stat__val--threat">17</span>
                  <span class="meta-stat__lbl">Unsecured systems</span>
                </div>
                <div class="meta-stat">
                  <span class="meta-stat__val">2h 14m</span>
                  <span class="meta-stat__lbl">Longest open incident</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- B: Threat Feed (full-width, scrollable) -->
        <section class="card threat-feed-section" aria-label="Real-time threat feed">
          <div class="card__header">
            <div class="card__header-left">
              <span
                class="live-dot"
                :class="{ 'is-pulse': pulseVisible }"
                aria-hidden="true"
              ></span>
              <h2 class="card__title">Threat Feed</h2>
            </div>
            <span class="card__meta">{{ threats.length }} detections in last 10 min</span>
          </div>

          <ul class="feed-table" role="list" aria-label="Recent threat detections">
            <!-- Header row -->
            <li class="feed-table__head" role="presentation" aria-hidden="true">
              <span>Severity</span>
              <span>Threat</span>
              <span>System</span>
              <span>Time</span>
            </li>
            <li
              v-for="threat in threats"
              :key="threat.id"
              class="feed-table__row"
            >
              <span class="badge" :class="`badge--${threat.severity.toLowerCase()}`">
                {{ threat.severity }}
              </span>
              <span class="feed-row__name">{{ threat.name }}</span>
              <span class="feed-row__system">{{ threat.system }}</span>
              <span class="feed-row__ts">{{ threat.ts }}</span>
            </li>
          </ul>
        </section>

        <!-- C: Agent team status — 4-col horizontal row -->
        <section class="card agents-section" aria-label="Agent team status">
          <div class="card__header">
            <h2 class="card__title">Agent Teams</h2>
            <span class="card__meta">3 active · 1 standby</span>
          </div>

          <div class="agents-row" role="list">
            <div
              v-for="agent in agents"
              :key="agent.name"
              class="agent-card"
              :class="`agent-card--${agent.status}`"
              role="listitem"
              :aria-label="`${agent.name}: ${agent.status}`"
            >
              <div class="agent-card__top">
                <span class="agent-dot" :class="`agent-dot--${agent.status}`" aria-hidden="true"></span>
                <span class="agent-card__name">{{ agent.name }}</span>
              </div>
              <span class="agent-card__role">{{ agent.role }}</span>
              <div class="agent-card__metrics">
                <div class="agent-metric">
                  <span
                    class="agent-metric__val"
                    :class="agent.status === 'offline' ? 'val--offline' : 'val--active'"
                  >{{ agent.uptime }}</span>
                  <span class="agent-metric__lbl">Uptime</span>
                </div>
                <div class="agent-metric">
                  <span class="agent-metric__val val--neutral">{{ agent.neutralized }}</span>
                  <span class="agent-metric__lbl">Neutralized</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- D: Active incidents summary -->
        <section class="card incidents-section" aria-label="Active incidents summary">
          <div class="card__header">
            <h2 class="card__title">Active Incidents</h2>
            <span class="card__meta">Last updated just now</span>
          </div>

          <div class="incidents-body">
            <!-- Hero count + sparkline -->
            <div class="incidents-hero">
              <span
                class="incidents-hero__count"
                :class="incidents.length > 0 ? 'count--threat' : 'count--secured'"
                :aria-label="`${incidents.length} open incidents`"
              >{{ incidents.length }}</span>
              <span class="incidents-hero__label">Open Incidents</span>

              <svg class="sparkline" viewBox="0 0 100 50" aria-hidden="true" preserveAspectRatio="none">
                <path class="sparkline__path" :d="sparklinePath" fill="none" stroke-width="2" stroke-linecap="round" />
              </svg>
            </div>

            <!-- Severity breakdown -->
            <div class="severity-strip" role="list" aria-label="By severity">
              <div class="sev-item sev-item--critical" role="listitem">
                <span class="sev-item__count">{{ severityCounts.CRITICAL }}</span>
                <span class="sev-item__lbl">Critical</span>
              </div>
              <div class="sev-item sev-item--high" role="listitem">
                <span class="sev-item__count">{{ severityCounts.HIGH }}</span>
                <span class="sev-item__lbl">High</span>
              </div>
              <div class="sev-item sev-item--medium" role="listitem">
                <span class="sev-item__count">{{ severityCounts.MEDIUM }}</span>
                <span class="sev-item__lbl">Medium</span>
              </div>
            </div>

            <!-- Incident list -->
            <ul class="incident-list" role="list" aria-label="Open incidents">
              <li
                v-for="inc in incidents"
                :key="inc.id"
                class="incident-row"
                :class="`incident-row--${inc.severity.toLowerCase()}`"
              >
                <span class="inc-badge" :class="`inc-badge--${inc.severity.toLowerCase()}`">
                  {{ inc.severity }}
                </span>
                <span class="inc-title">{{ inc.title }}</span>
                <span class="inc-time">{{ inc.openedAt }}</span>
              </li>
            </ul>
          </div>
        </section>

      </div><!-- /body__inner -->
    </main>
  </div>
</template>

<style scoped>
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
  flex-direction: column;
  opacity: 0;
  transition: opacity var(--duration-normal) var(--easing);
}

.dashboard.is-mounted {
  opacity: 1;
}

/* ── Sticky header ────────────────────────────────────────────── */
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: linear-gradient(
    to right,
    var(--brand-bg-secondary),
    color-mix(in srgb, var(--brand-bg-secondary) 85%, var(--brand-surface))
  );
  border-bottom: 1px solid var(--brand-border);
  box-shadow: var(--shadow-md);
}

.sticky-header__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 calc(var(--space-unit) * 6);
  height: calc(var(--space-unit) * 16);
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 8);
}

.sticky-header__brand {
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

.brand-sub {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Header stats */
.hdr-stats {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 5);
  flex: 1;
}

.hdr-divider {
  width: 1px;
  height: calc(var(--space-unit) * 5);
  background-color: var(--brand-border);
  flex-shrink: 0;
}

.hdr-stat {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.hdr-stat__val {
  font-family: var(--font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1;
}

.hdr-stat__val--threat  { color: var(--brand-accent);    }
.hdr-stat__val--secured { color: var(--brand-primary);   }
.hdr-stat__val--online  { color: var(--brand-secondary); }

.hdr-stat__lbl {
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Mini gauge */
.mini-gauge {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  flex-shrink: 0;
}

.mini-gauge__svg {
  width: 40px;
  height: 40px;
}

.mini-track {
  stroke: var(--brand-border);
}

.mini-fill {
  transition: stroke-dashoffset var(--duration-slow) var(--easing);
}

.mini-gauge__pct {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-primary);
}

/* ── Body ─────────────────────────────────────────────────────── */
.dashboard__body {
  flex: 1;
  overflow-y: auto;
}

.body__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 6);
  display: flex;
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
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
}

.card__header-left {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.card__title {
  font-family: var(--font-heading);
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--brand-text);
  margin: 0;
}

.card__meta {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

/* Live badge/dot */
.live-badge {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  background-color: var(--brand-primary);
  transition: opacity var(--duration-fast) var(--easing);
}

.live-badge.is-pulse { opacity: 0.3; }

.live-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  background-color: var(--brand-error);
  flex-shrink: 0;
  transition: opacity var(--duration-fast) var(--easing);
}

.live-dot.is-pulse { opacity: 0.25; }

/* ── A: Gauge section ─────────────────────────────────────────── */
.gauge-section__body {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 10);
  padding: calc(var(--space-unit) * 8) calc(var(--space-unit) * 10);
}

@media (max-width: 768px) {
  .gauge-section__body {
    flex-direction: column;
    padding: calc(var(--space-unit) * 6);
  }
}

.gauge-wrap {
  position: relative;
  width: 260px;
  height: 260px;
  flex-shrink: 0;
  /* Soft ambient glow behind gauge */
  filter: drop-shadow(0 0 24px color-mix(in srgb, var(--brand-primary) 8%, transparent));
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
  gap: calc(var(--space-unit) * 1);
}

.gauge-center__pct {
  font-family: var(--font-mono);
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brand-primary);
}

.gauge-center__lbl {
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.gauge-center__count {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--brand-text);
}

.gauge-section__meta {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
}

.gauge-meta__desc {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: var(--brand-text);
  margin: 0;
}

.gauge-meta__desc strong {
  color: var(--brand-primary);
  font-weight: 700;
}

.gauge-meta__stats {
  display: flex;
  gap: calc(var(--space-unit) * 8);
}

.meta-stat {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.meta-stat__val {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--brand-primary);
}

.meta-stat__val--threat {
  color: var(--brand-accent);
}

.meta-stat__lbl {
  font-size: 0.75rem;
  letter-spacing: 0.04em;
  color: var(--brand-muted);
}

/* ── B: Threat feed table ─────────────────────────────────────── */
.feed-table {
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 420px;
  overflow-y: auto;
}

.feed-table__head {
  display: grid;
  grid-template-columns: 100px 1fr 160px 80px;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 6);
  background: linear-gradient(to right, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 80%, var(--brand-surface)));
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
  border-bottom: 1px solid var(--brand-border);
}

.feed-table__row {
  display: grid;
  grid-template-columns: 100px 1fr 160px 80px;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 3.5) calc(var(--space-unit) * 6);
  border-bottom: 1px solid var(--brand-border);
  transition: background-color var(--duration-fast) var(--easing);
  cursor: default;
}

.feed-table__row:last-child {
  border-bottom: none;
}

.feed-table__row:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 80%, var(--brand-accent));
}

.badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  text-align: center;
}

.badge--critical { background-color: var(--brand-error);  color: var(--brand-bg);   }
.badge--high     { background-color: var(--brand-accent); color: var(--brand-bg);   }
.badge--medium   {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text);
}
.badge--low      { background-color: var(--brand-secondary); color: var(--brand-bg); }

.feed-row__name {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.feed-row__system {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

.feed-row__ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  text-align: right;
}

/* ── C: Agents 4-col ──────────────────────────────────────────── */
.agents-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: calc(var(--space-unit) * 1);
}

@media (max-width: 768px) {
  .agents-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

.agent-card {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 5);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
  border-right: 1px solid var(--brand-border);
}

.agent-card:last-child {
  border-right: none;
}

.agent-card__top {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2.5);
}

.agent-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.agent-dot--active  { background-color: var(--brand-primary);  }
.agent-dot--idle    { background-color: var(--brand-secondary); }
.agent-dot--offline { background-color: var(--brand-error);     }

.agent-card__name {
  font-family: var(--font-heading);
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--brand-text);
}

.agent-card__role {
  font-size: 0.75rem;
  color: var(--brand-muted);
  line-height: 1.4;
}

.agent-card__metrics {
  display: flex;
  gap: calc(var(--space-unit) * 5);
  margin-top: auto;
}

.agent-metric {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.agent-metric__val {
  font-family: var(--font-mono);
  font-size: 0.9375rem;
  font-weight: 700;
  line-height: 1;
}

.val--active  { color: var(--brand-primary);  }
.val--offline { color: var(--brand-error);    }
.val--neutral { color: var(--brand-text);     }

.agent-metric__lbl {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── D: Incidents section ─────────────────────────────────────── */
.incidents-body {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 5);
}

.incidents-hero {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
}

.incidents-hero__count {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.count--threat   { color: var(--brand-accent);  }
.count--secured  { color: var(--brand-primary); }

.incidents-hero__label {
  font-size: 0.875rem;
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

/* Severity strip */
.severity-strip {
  display: flex;
  gap: calc(var(--space-unit) * 4);
}

.sev-item {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
  border-radius: var(--radius-md);
}

.sev-item--critical {
  background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-error) 35%, transparent);
}
.sev-item--high {
  background-color: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-accent) 35%, transparent);
}
.sev-item--medium {
  background-color: color-mix(in srgb, var(--brand-secondary) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-secondary) 30%, transparent);
}

.sev-item__count {
  font-family: var(--font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--brand-text);
}

.sev-item__lbl {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Incident list */
.incident-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.incident-row {
  display: grid;
  grid-template-columns: 90px 1fr auto;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  border-left: 3px solid transparent;
  transition: background-color var(--duration-fast) var(--easing);
}

.incident-row--critical { border-left-color: var(--brand-error);  }
.incident-row--high     { border-left-color: var(--brand-accent); }
.incident-row--medium   { border-left-color: var(--brand-secondary); }

.incident-row:hover {
  background-color: color-mix(in srgb, var(--brand-bg-secondary) 70%, var(--brand-surface));
}

.inc-badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
}

.inc-badge--critical { background-color: var(--brand-error);  color: var(--brand-bg); }
.inc-badge--high     { background-color: var(--brand-accent); color: var(--brand-bg); }
.inc-badge--medium   {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text);
}

.inc-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--brand-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.inc-time {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  white-space: nowrap;
}

/* ── Focus styles ────────────────────────────────────────────── */
:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* ── Screen-reader only ───────────────────────────────────────── */
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

/* ── Responsive: header mobile ────────────────────────────────── */
@media (max-width: 768px) {
  .sticky-header__inner {
    flex-wrap: wrap;
    height: auto;
    gap: calc(var(--space-unit) * 3);
    padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  }
  .mini-gauge {
    margin-left: 0;
  }
}

/* ── Responsive: feed table mobile ────────────────────────────── */
@media (max-width: 640px) {
  .feed-table__head {
    display: none;
  }
  .feed-table__row {
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto;
    gap: calc(var(--space-unit) * 1);
  }
  .feed-row__system,
  .feed-row__ts {
    grid-column: 2;
    font-size: 0.6875rem;
    color: var(--brand-muted);
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

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/mobile/dashboard/v2-scroll-feed-bar
// Layout: compact header + mini gauge → horizontal-snap threat cards
//         → agent strip → full gauge → incidents → fixed bottom nav
// CRITICAL: --space-unit = 0.375rem on mobile (not 0.5rem)

// ── Types ────────────────────────────────────────────────────────
interface Threat {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  system: string
  ts: string
}

interface Agent {
  id: string
  name: string
  status: 'active' | 'standby' | 'offline'
}

interface Incident {
  id: number
  title: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  status: 'active' | 'contained' | 'resolved'
  ts: string
}

// ── Static data ──────────────────────────────────────────────────
const threats: Threat[] = [
  { id: 1, name: 'Prompt injection via system prompt',  severity: 'CRITICAL', system: 'api-gateway-01',   ts: '2s'  },
  { id: 2, name: 'Data exfiltration attempt',           severity: 'HIGH',     system: 'llm-worker-07',   ts: '14s' },
  { id: 3, name: 'Privilege escalation — agent token',  severity: 'CRITICAL', system: 'orchestrator-02', ts: '34s' },
  { id: 4, name: 'Model poisoning probe',               severity: 'HIGH',     system: 'fine-tune-03',    ts: '1m'  },
  { id: 5, name: 'Anomalous API call pattern',          severity: 'MEDIUM',   system: 'api-gateway-02',  ts: '2m'  },
  { id: 6, name: 'Rate limit bypass attempt',           severity: 'MEDIUM',   system: 'rate-limiter-01', ts: '3m'  },
  { id: 7, name: 'Repeated auth failure probe',         severity: 'HIGH',     system: 'auth-service',    ts: '4m'  },
  { id: 8, name: 'Context window overflow probe',       severity: 'MEDIUM',   system: 'llm-worker-02',   ts: '6m'  },
]

const agents: Agent[] = [
  { id: 'scanner',   name: 'Scanner',   status: 'active'  },
  { id: 'monitor',   name: 'Monitor',   status: 'active'  },
  { id: 'responder', name: 'Responder', status: 'active'  },
  { id: 'sentinel',  name: 'Sentinel',  status: 'standby' },
]

const incidents: Incident[] = [
  { id: 1, title: 'Prompt injection — api-gateway cluster',    severity: 'CRITICAL', status: 'active',    ts: '14m ago' },
  { id: 2, title: 'Exfiltration attempt — llm-worker-07',      severity: 'HIGH',     status: 'contained', ts: '22m ago' },
  { id: 3, title: 'Token privilege escalation',                severity: 'CRITICAL', status: 'active',    ts: '41m ago' },
  { id: 4, title: 'Model poisoning probe — fine-tune cluster', severity: 'HIGH',     status: 'contained', ts: '1h ago'  },
  { id: 5, title: 'Anomalous call pattern — api-gateway-02',   severity: 'MEDIUM',   status: 'resolved',  ts: '2h ago'  },
]

// ── Gauge math ───────────────────────────────────────────────────
const posturePercent = ref(83)

// Full gauge: r=80, viewBox 200×200
const gaugeCircumference = 2 * Math.PI * 80
const gaugeDashOffset = computed(() =>
  gaugeCircumference * (1 - posturePercent.value / 100)
)

// Mini header gauge: r=15, viewBox 40×40
const miniCircumference = 2 * Math.PI * 15
const miniDashOffset = computed(() =>
  miniCircumference * (1 - posturePercent.value / 100)
)

// ── Active agents count ──────────────────────────────────────────
const activeAgentCount = computed(() => agents.filter(a => a.status === 'active').length)

// ── Critical threats count ───────────────────────────────────────
const criticalCount = computed(() => threats.filter(t => t.severity === 'CRITICAL').length)

// ── Bottom nav ───────────────────────────────────────────────────
const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: '⬡' },
  { id: 'alerts',    label: 'Alerts',    icon: '◈' },
  { id: 'agents',    label: 'Agents',    icon: '◉' },
  { id: 'settings',  label: 'Settings',  icon: '◇' },
]
const activeTab = ref('dashboard')

// ── Mount + live dot ─────────────────────────────────────────────
const isMounted = ref(false)
let clockInterval: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  nextTick(() => { isMounted.value = true })
  // clockInterval reserved for future live updates — hook in place
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
    <h1 class="sr-only">Aegis Mobile Command Center</h1>

    <!-- ── Compact header ────────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Dashboard status">
      <div class="header-brand">
        <span class="brand-word">AEGIS</span>
        <span class="brand-sep" aria-hidden="true">/</span>
        <span class="brand-sub">SOC</span>
        <span class="live-dot" aria-hidden="true"></span>
        <span class="live-label">LIVE</span>
      </div>

      <div class="header-status" aria-label="Agent count and defense posture">
        <span class="header-agents">
          <span class="header-agents__count">{{ activeAgentCount }}</span>
          <span class="header-agents__label">/{{ agents.length }} agents</span>
        </span>

        <!-- Mini gauge ring -->
        <div class="mini-gauge" :aria-label="`${posturePercent}% systems secured`">
          <svg
            viewBox="0 0 40 40"
            aria-hidden="true"
            class="mini-gauge__svg"
          >
            <circle
              cx="20" cy="20" r="15"
              fill="none" stroke-width="3"
              class="mini-gauge__track"
            />
            <circle
              cx="20" cy="20" r="15"
              fill="none" stroke-width="3"
              class="mini-gauge__arc"
              :stroke-dasharray="miniCircumference"
              :stroke-dashoffset="miniDashOffset"
              stroke-linecap="round"
              transform="rotate(-90 20 20)"
            />
            <text x="20" y="24" text-anchor="middle" class="mini-gauge__text">{{ posturePercent }}</text>
          </svg>
        </div>
      </div>
    </header>

    <!-- ── Page content ──────────────────────────────────────── -->
    <div class="page__content">

      <!-- ── Section 1: Threat feed (horizontal scroll) ──────── -->
      <section class="feed-section" aria-labelledby="feed-heading">
        <div class="feed-header">
          <h2 id="feed-heading" class="section-title">Threat Feed</h2>
          <div class="feed-meta">
            <span class="crit-badge" v-if="criticalCount > 0" :aria-label="`${criticalCount} critical threats`">
              {{ criticalCount }} CRIT
            </span>
            <span class="feed-count">{{ threats.length }} active</span>
          </div>
        </div>

        <!-- Horizontal snap-scroll — scroll-snap on this container, NOT the page root -->
        <div
          class="feed-scroll"
          role="list"
          aria-label="Active threat detections, swipe to see more"
        >
          <article
            v-for="threat in threats"
            :key="threat.id"
            class="threat-card"
            :class="`threat-card--${threat.severity.toLowerCase()}`"
            role="listitem"
            :aria-label="`${threat.severity}: ${threat.name}, ${threat.system}, ${threat.ts} ago`"
          >
            <div class="threat-card__header">
              <span class="sev-pill" :class="`sev-pill--${threat.severity.toLowerCase()}`">
                {{ threat.severity }}
              </span>
              <span class="threat-card__ts">{{ threat.ts }}</span>
            </div>
            <p class="threat-card__name">{{ threat.name }}</p>
            <p class="threat-card__system">{{ threat.system }}</p>
          </article>
        </div>

        <!-- Scroll indicator dots -->
        <div class="feed-dots" aria-hidden="true">
          <span
            v-for="(threat, i) in threats"
            :key="threat.id"
            class="feed-dot"
            :class="{ 'feed-dot--first': i === 0 }"
          ></span>
        </div>
      </section>

      <!-- ── Section 2: Agent status strip ────────────────────── -->
      <section class="agent-section" aria-labelledby="agents-heading">
        <h2 id="agents-heading" class="sr-only">Agent Status</h2>
        <div class="agent-strip" role="list" aria-label="Agent team status">
          <div
            v-for="agent in agents"
            :key="agent.id"
            class="agent-indicator"
            :class="`agent-indicator--${agent.status}`"
            role="listitem"
            :aria-label="`${agent.name}: ${agent.status}`"
          >
            <div class="agent-dot-wrap" aria-hidden="true">
              <span class="agent-dot" :class="`agent-dot--${agent.status}`"></span>
            </div>
            <span class="agent-label">{{ agent.name }}</span>
          </div>
        </div>
      </section>

      <!-- ── Section 3: Full defense posture gauge ─────────────── -->
      <section class="gauge-section" aria-labelledby="posture-heading">
        <div class="gauge-header">
          <h2 id="posture-heading" class="section-title">Defense Posture</h2>
          <span class="gauge-trend">↑ 2% since yesterday</span>
        </div>

        <div class="gauge-wrap">
          <svg
            class="gauge-svg"
            viewBox="0 0 200 200"
            aria-hidden="true"
          >
            <defs>
              <linearGradient id="gaugeGradV2" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%"   stop-color="var(--brand-error)"   />
                <stop offset="40%"  stop-color="var(--brand-accent)"  />
                <stop offset="100%" stop-color="var(--brand-primary)" />
              </linearGradient>
            </defs>
            <circle
              cx="100" cy="100" r="80"
              fill="none" stroke-width="12"
              class="gauge-track"
            />
            <circle
              cx="100" cy="100" r="80"
              fill="none" stroke-width="12"
              stroke="url(#gaugeGradV2)"
              stroke-linecap="round"
              :stroke-dasharray="gaugeCircumference"
              :stroke-dashoffset="gaugeDashOffset"
              transform="rotate(-90 100 100)"
              class="gauge-arc"
            />
          </svg>

          <div class="gauge-center" :aria-label="`${posturePercent}% systems secured`">
            <span class="gauge-center__pct">{{ posturePercent }}%</span>
            <span class="gauge-center__label">Secured</span>
          </div>
        </div>

        <!-- Stats below gauge -->
        <div class="gauge-stats">
          <div class="gauge-stat">
            <span class="gauge-stat__val gauge-stat__val--threat">{{ criticalCount }}</span>
            <span class="gauge-stat__lbl">Critical</span>
          </div>
          <div class="gauge-stat-sep" aria-hidden="true"></div>
          <div class="gauge-stat">
            <span class="gauge-stat__val gauge-stat__val--secured">{{ activeAgentCount }}/4</span>
            <span class="gauge-stat__lbl">Agents</span>
          </div>
          <div class="gauge-stat-sep" aria-hidden="true"></div>
          <div class="gauge-stat">
            <span class="gauge-stat__val gauge-stat__val--secured">187ms</span>
            <span class="gauge-stat__lbl">Response</span>
          </div>
        </div>
      </section>

      <!-- ── Section 4: Recent incidents ──────────────────────── -->
      <section class="incidents-section" aria-labelledby="incidents-heading">
        <div class="incidents-header">
          <h2 id="incidents-heading" class="section-title">Recent Incidents</h2>
          <span class="incidents-count" :aria-label="`${incidents.length} open incidents`">
            {{ incidents.length }}
          </span>
        </div>

        <ul class="incidents-list" role="list" aria-label="Recent security incidents">
          <li
            v-for="inc in incidents"
            :key="inc.id"
            class="inc-row"
            :aria-label="`${inc.severity} incident: ${inc.title}, ${inc.status}, ${inc.ts}`"
          >
            <span
              class="inc-dot"
              :class="`inc-dot--${inc.status}`"
              aria-hidden="true"
            ></span>
            <div class="inc-body">
              <p class="inc-title">{{ inc.title }}</p>
              <div class="inc-meta">
                <span class="inc-sev" :class="`inc-sev--${inc.severity.toLowerCase()}`">
                  {{ inc.severity }}
                </span>
                <span class="inc-sep" aria-hidden="true">·</span>
                <span class="inc-ts">{{ inc.ts }}</span>
              </div>
            </div>
            <span class="inc-status-badge" :class="`inc-status-badge--${inc.status}`">
              {{ inc.status }}
            </span>
          </li>
        </ul>
      </section>

    </div><!-- /page__content -->

    <!-- ── Fixed bottom nav ──────────────────────────────────── -->
    <nav class="bottom-nav" aria-label="Main navigation">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="nav-tab"
        :class="{ 'nav-tab--active': activeTab === tab.id }"
        :aria-pressed="activeTab === tab.id"
        :aria-label="tab.label"
        @click="activeTab = tab.id"
      >
        <span class="nav-tab__icon" aria-hidden="true">{{ tab.icon }}</span>
        <span class="nav-tab__label">{{ tab.label }}</span>
      </button>
    </nav>

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
  max-width: var(--container-max);
  margin: 0 auto;
  min-height: 100vh;
  background-color: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  overflow-x: hidden;   /* page root only — feed-scroll uses overflow-x: auto */
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

/* ── Page content — clears fixed bottom nav ───────────────────── */
.page__content {
  padding-bottom: calc(
    calc(var(--space-unit) * 12)
    + env(safe-area-inset-bottom)
    + calc(var(--space-unit) * 4)
  );
}

/* ── Section title ────────────────────────────────────────────── */
.section-title {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.015em;
  color: var(--brand-text);
  margin: 0;
}

/* ── Page header ──────────────────────────────────────────────── */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 4);
  background: linear-gradient(to right, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 85%, var(--brand-surface)));
  border-bottom: 1px solid var(--brand-border);
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
}

.brand-word {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
}

.brand-sep {
  color: var(--brand-border);
  font-weight: 300;
}

.brand-sub {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.live-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  background-color: var(--brand-error);
  animation: live-pulse 1.5s var(--easing) infinite;
  flex-shrink: 0;
}

.live-label {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--brand-error);
}

.header-status {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.header-agents {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 0.5);
}

.header-agents__count {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--brand-primary);
  line-height: 1;
}

.header-agents__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  color: var(--brand-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Mini gauge */
.mini-gauge {
  flex-shrink: 0;
}

.mini-gauge__svg {
  width: calc(var(--space-unit) * 11);
  height: calc(var(--space-unit) * 11);
  display: block;
}

.mini-gauge__track {
  stroke: var(--brand-border);
}

.mini-gauge__arc {
  stroke: var(--brand-primary);
  transition: stroke-dashoffset var(--duration-slow) var(--easing);
}

.mini-gauge__text {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  fill: var(--brand-primary);
}

/* ── Threat feed ──────────────────────────────────────────────── */
.feed-section {
  padding-top: calc(var(--space-unit) * 4);
}

.feed-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 calc(var(--space-unit) * 4);
  margin-bottom: calc(var(--space-unit) * 3);
}

.feed-meta {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.crit-badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  padding: calc(var(--space-unit) * 0.5) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  background-color: var(--brand-error);
  color: var(--brand-bg);
}

.feed-count {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);
}

/* Horizontal scroll container — scroll-snap lives here, NOT on .page */
.feed-scroll {
  display: flex;
  gap: calc(var(--space-unit) * 3);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x mandatory;
  scroll-padding-left: calc(var(--space-unit) * 4);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4) calc(var(--space-unit) * 4);
  scrollbar-width: none;
}

.feed-scroll::-webkit-scrollbar {
  display: none;
}

/* Threat cards snap individually */
.threat-card {
  scroll-snap-align: start;
  flex-shrink: 0;
  width: calc(100% - calc(var(--space-unit) * 10));
  min-width: 240px;
  background-color: var(--brand-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: calc(var(--space-unit) * 4);
  border-left: 3px solid transparent;
}

.threat-card--critical { border-left-color: var(--brand-error);  }
.threat-card--high     { border-left-color: var(--brand-accent); }
.threat-card--medium   { border-left-color: color-mix(in srgb, var(--brand-accent) 50%, transparent); }
.threat-card--low      { border-left-color: var(--brand-secondary); }

.threat-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: calc(var(--space-unit) * 2);
}

.threat-card__ts {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);
}

.threat-card__name {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 1.5) 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.threat-card__system {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  margin: 0;
}

/* Severity pills */
.sev-pill {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  line-height: 1;
}

.sev-pill--critical { background-color: var(--brand-error);   color: var(--brand-bg); }
.sev-pill--high     { background-color: var(--brand-accent);  color: var(--brand-bg); }
.sev-pill--medium   {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text);
}
.sev-pill--low      { background-color: var(--brand-secondary); color: var(--brand-bg); }

/* Scroll indicator dots (decorative) */
.feed-dots {
  display: flex;
  justify-content: center;
  gap: calc(var(--space-unit) * 1);
  padding-bottom: calc(var(--space-unit) * 2);
}

.feed-dot {
  width: calc(var(--space-unit) * 1.5);
  height: calc(var(--space-unit) * 1.5);
  border-radius: 50%;
  background-color: color-mix(in srgb, var(--brand-border) 80%, transparent);
}

.feed-dot--first {
  background-color: var(--brand-primary);
}

/* ── Agent status strip ───────────────────────────────────────── */
.agent-section {
  background-color: var(--brand-bg-secondary);
  border-top: 1px solid var(--brand-border);
  border-bottom: 1px solid var(--brand-border);
}

.agent-strip {
  display: flex;
  justify-content: space-around;
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 2);
}

.agent-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
  min-width: calc(var(--space-unit) * 12);
  cursor: default;
}

.agent-dot-wrap {
  width: calc(var(--space-unit) * 8);
  height: calc(var(--space-unit) * 8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: color-mix(in srgb, var(--brand-border) 60%, transparent);
  transition: background-color var(--duration-normal) var(--easing);
}

.agent-indicator--active .agent-dot-wrap {
  background-color: color-mix(in srgb, var(--brand-primary) 10%, transparent);
}

.agent-dot {
  width: calc(var(--space-unit) * 5);
  height: calc(var(--space-unit) * 5);
  border-radius: 50%;
  transition: background-color var(--duration-normal) var(--easing);
}

.agent-dot--active  {
  background-color: var(--brand-primary);
  animation: agent-pulse 2s var(--easing) infinite;
}
.agent-dot--standby { background-color: var(--brand-secondary); }
.agent-dot--offline { background-color: var(--brand-error);     }

.agent-label {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

/* ── Full gauge section ───────────────────────────────────────── */
.gauge-section {
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 4);
  background: radial-gradient(
    ellipse 80% 60% at 50% 50%,
    color-mix(in srgb, var(--brand-primary) 4%, transparent),
    transparent 70%
  );
}

.gauge-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: calc(var(--space-unit) * 4);
}

.gauge-trend {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  color: var(--brand-primary);
}

.gauge-wrap {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: calc(var(--space-unit) * 53);
  margin: 0 auto;
}

.gauge-svg {
  width: 100%;
  max-width: calc(var(--space-unit) * 53);
}

.gauge-track {
  stroke: var(--brand-border);
}

.gauge-arc {
  transition: stroke-dashoffset var(--duration-slow) var(--easing);
}

.gauge-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 0.5);
}

.gauge-center__pct {
  font-family: var(--font-mono);
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brand-primary);
}

.gauge-center__label {
  font-family: var(--font-body);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Gauge stats below ring */
.gauge-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 4);
  margin-top: calc(var(--space-unit) * 5);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
}

.gauge-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 0.5);
}

.gauge-stat__val {
  font-family: var(--font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1;
}

.gauge-stat__val--threat  { color: var(--brand-error);   }
.gauge-stat__val--secured { color: var(--brand-primary); }

.gauge-stat__lbl {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.gauge-stat-sep {
  width: 1px;
  height: calc(var(--space-unit) * 8);
  background-color: var(--brand-border);
  flex-shrink: 0;
}

/* ── Incidents section ────────────────────────────────────────── */
.incidents-section {
  padding: calc(var(--space-unit) * 5) 0;
}

.incidents-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 calc(var(--space-unit) * 4);
  margin-bottom: calc(var(--space-unit) * 3);
}

.incidents-count {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-accent);
  background-color: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
}

.incidents-list {
  list-style: none;
  margin: 0;
  padding: 0;
  background-color: var(--brand-surface);
  border-top: 1px solid var(--brand-border);
}

.inc-row {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  border-bottom: 1px solid var(--brand-border);
}

.inc-row:last-child {
  border-bottom: none;
}

.inc-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: calc(var(--space-unit) * 1);
}

.inc-dot--active    { background-color: var(--brand-error);     }
.inc-dot--contained { background-color: var(--brand-secondary); }
.inc-dot--resolved  { background-color: var(--brand-primary);   }

.inc-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.inc-title {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
  line-height: 1.4;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.inc-meta {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.inc-sev {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.inc-sev--critical { color: var(--brand-error);     }
.inc-sev--high     { color: var(--brand-accent);    }
.inc-sev--medium   { color: var(--brand-secondary); }

.inc-sep {
  color: var(--brand-border);
  font-size: 0.6875rem;
}

.inc-ts {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  color: var(--brand-muted);
}

.inc-status-badge {
  font-family: var(--font-mono);
  font-size: 0.5rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.5) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  flex-shrink: 0;
  align-self: center;
  color: var(--brand-bg);
}

.inc-status-badge--active    { background-color: var(--brand-error);     }
.inc-status-badge--contained { background-color: var(--brand-secondary); }
.inc-status-badge--resolved  { background-color: var(--brand-primary);   }

/* ── Fixed bottom nav ─────────────────────────────────────────── */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background-color: var(--brand-bg-secondary);
  border-top: 1px solid var(--brand-border);
  display: flex;
  align-items: stretch;
  padding-bottom: env(safe-area-inset-bottom);
  max-width: var(--container-max);
  margin: 0 auto;
}

.nav-tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 1);
  min-height: calc(var(--space-unit) * 12);
  background: none;
  border: none;
  cursor: pointer;
  color: color-mix(in srgb, var(--brand-text) 55%, transparent);
  transition: color var(--duration-fast) var(--easing);
  -webkit-tap-highlight-color: transparent;
  padding: calc(var(--space-unit) * 2) 0;
}

.nav-tab:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

.nav-tab--active {
  color: var(--brand-primary);
}

.nav-tab__icon {
  font-size: 1.25rem;
  line-height: 1;
}

.nav-tab__label {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

/* ── Focus baseline ───────────────────────────────────────────── */
:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* ── Keyframes ────────────────────────────────────────────────── */
@keyframes agent-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: none;
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
    box-shadow: 0 0 calc(var(--space-unit) * 2) color-mix(in srgb, var(--brand-primary) 30%, transparent);
  }
}

@keyframes live-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
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

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/mobile/dashboard/v1-gauge-card-stack
// Variant: Gauge hero at top → agent strip → stacked threat cards → incidents → fixed bottom nav
// CRITICAL: --space-unit = 0.375rem (mobile override, NOT 0.5rem)

// ── Types ─────────────────────────────────────────────────────────────
interface Agent {
  id: string
  name: string
  status: 'active' | 'standby' | 'offline'
}

interface ThreatEntry {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  system: string
  ts: string
}

interface Incident {
  id: string
  title: string
  status: 'active' | 'investigating' | 'contained' | 'resolved'
  time: string
}

interface Tab {
  id: string
  label: string
  icon: string
}

// ── Agent data ─────────────────────────────────────────────────────────
const agents: Agent[] = [
  { id: 'scanner',   name: 'Scanner',   status: 'active'  },
  { id: 'monitor',   name: 'Monitor',   status: 'active'  },
  { id: 'responder', name: 'Responder', status: 'active'  },
  { id: 'sentinel',  name: 'Sentinel',  status: 'standby' },
]

// ── Threat data ────────────────────────────────────────────────────────
const threats: ThreatEntry[] = [
  { id: 1, name: 'Prompt injection — GPT-4 endpoint', severity: 'CRITICAL', system: 'api-gateway-01',   ts: '2s ago'  },
  { id: 2, name: 'Data exfiltration attempt',          severity: 'HIGH',     system: 'llm-worker-07',   ts: '14s ago' },
  { id: 3, name: 'Privilege escalation probe',         severity: 'CRITICAL', system: 'orchestrator-02', ts: '41s ago' },
  { id: 4, name: 'Model poisoning signal detected',    severity: 'HIGH',     system: 'fine-tune-03',    ts: '2m ago'  },
  { id: 5, name: 'Unusual API call pattern',           severity: 'MEDIUM',   system: 'api-gateway-02',  ts: '3m ago'  },
  { id: 6, name: 'Rate limiter bypass attempt',        severity: 'MEDIUM',   system: 'rate-limiter-01', ts: '5m ago'  },
]

// ── Incident data ──────────────────────────────────────────────────────
const incidents: Incident[] = [
  { id: 'INC-001', title: 'Prompt injection campaign — api-gateway cluster',   status: 'active',        time: '14m ago' },
  { id: 'INC-002', title: 'Exfiltration attempt — llm-worker-07',              status: 'investigating', time: '22m ago' },
  { id: 'INC-003', title: 'Token privilege escalation — orchestrator-02',      status: 'contained',     time: '41m ago' },
  { id: 'INC-004', title: 'Model poisoning probe — fine-tune cluster',         status: 'resolved',      time: '1h ago'  },
]

// ── Navigation tabs ────────────────────────────────────────────────────
const tabs: Tab[] = [
  { id: 'dashboard', label: 'Dashboard', icon: '⬡' },
  { id: 'alerts',    label: 'Alerts',    icon: '◉' },
  { id: 'agents',    label: 'Agents',    icon: '◈' },
  { id: 'settings',  label: 'Settings',  icon: '◇' },
]

const activeTab = ref('dashboard')

// ── Gauge ──────────────────────────────────────────────────────────────
const posturePercent = ref(83)
const circumference = 2 * Math.PI * 80 // r=80 → ≈502.65

const dashOffset = computed(() =>
  circumference * (1 - posturePercent.value / 100)
)

// ── Computed counts ────────────────────────────────────────────────────
const activeAgentCount = computed(() =>
  agents.filter(a => a.status === 'active').length
)

const activeIncidentCount = computed(() =>
  incidents.filter(i => i.status === 'active' || i.status === 'investigating').length
)

// ── Live clock ─────────────────────────────────────────────────────────
const liveTime = ref('')
let clockInterval: ReturnType<typeof setInterval> | null = null

function updateClock() {
  const now = new Date()
  liveTime.value = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
}

// ── Mount ──────────────────────────────────────────────────────────────
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
    <h1 class="sr-only">Aegis Mobile Command Center</h1>

    <!-- ── Page header (sticky) ───────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Mobile security dashboard header">
      <span class="page-header__brand">AEGIS SOC</span>
      <div class="page-header__right">
        <div class="page-header__status" aria-hidden="true">
          <span
            v-for="agent in agents"
            :key="agent.id"
            class="hdr-dot"
            :class="`hdr-dot--${agent.status}`"
          ></span>
          <span class="hdr-online">{{ activeAgentCount }}/{{ agents.length }}</span>
        </div>
        <span class="page-header__time" aria-label="Current time">{{ liveTime }}</span>
      </div>
    </header>

    <!-- ── Scrollable content ─────────────────────────────────────── -->
    <div class="page__content">

      <!-- ── Section 1: Defense Posture Gauge ──────────────────────── -->
      <section class="gauge-section" aria-labelledby="gauge-heading">
        <h2 id="gauge-heading" class="sr-only">Defense Posture</h2>
        <div class="gauge-wrap">
          <svg
            class="gauge-ring"
            viewBox="0 0 200 200"
            aria-hidden="true"
            preserveAspectRatio="xMidYMid meet"
          >
            <defs>
              <linearGradient id="gaugeGradV1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%"   stop-color="var(--brand-error)"   />
                <stop offset="40%"  stop-color="var(--brand-accent)"  />
                <stop offset="100%" stop-color="var(--brand-primary)" />
              </linearGradient>
            </defs>
            <!-- Track ring -->
            <circle
              cx="100" cy="100" r="80"
              fill="none"
              stroke="var(--brand-border)"
              stroke-width="12"
            />
            <!-- Arc fill — starts at top (-90 deg rotation) -->
            <circle
              cx="100" cy="100" r="80"
              fill="none"
              stroke="url(#gaugeGradV1)"
              stroke-width="12"
              stroke-linecap="round"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="dashOffset"
              transform="rotate(-90 100 100)"
            />
          </svg>
          <!-- Center readout — decorative, aria-hidden, data surfaces in sr-only paragraph -->
          <div class="gauge-center" aria-hidden="true">
            <span class="gauge-center__pct">{{ posturePercent }}%</span>
            <span class="gauge-center__label">Systems Secured</span>
          </div>
        </div>
        <!-- Accessible text version of gauge value -->
        <p class="gauge-accessible-label">
          <span class="sr-only">Defense posture: {{ posturePercent }}% systems secured</span>
          <span aria-hidden="true">Defense posture: {{ posturePercent }}% secured</span>
        </p>
      </section>

      <!-- ── Section 2: Agent Status Strip ─────────────────────────── -->
      <section class="agent-section" aria-labelledby="agents-heading">
        <h2 id="agents-heading" class="sr-only">Agent Team Status</h2>
        <div
          class="agent-strip"
          role="list"
          :aria-label="`${activeAgentCount} of ${agents.length} agents active`"
        >
          <div
            v-for="agent in agents"
            :key="agent.id"
            class="agent-indicator"
            :class="`agent-indicator--${agent.status}`"
            role="listitem"
            :aria-label="`${agent.name}: ${agent.status}`"
          >
            <div class="agent-dot-wrap" aria-hidden="true">
              <span
                class="agent-dot"
                :class="`agent-dot--${agent.status}`"
              ></span>
            </div>
            <span class="agent-label">{{ agent.name }}</span>
          </div>
        </div>
      </section>

      <!-- ── Section 3: Threat Feed (stacked cards) ─────────────────── -->
      <section class="feed-section" aria-labelledby="feed-heading">
        <div class="section-header">
          <h2 id="feed-heading" class="section-title">Threat Feed</h2>
          <span class="live-badge" aria-hidden="true">● LIVE</span>
        </div>
        <div class="threat-list" role="list" aria-label="Recent threat detections">
          <article
            v-for="threat in threats"
            :key="threat.id"
            class="threat-card"
            :class="`threat-card--${threat.severity.toLowerCase()}`"
            role="listitem"
            :aria-label="`${threat.severity} severity: ${threat.name}, system ${threat.system}, detected ${threat.ts}`"
          >
            <div class="threat-card__header">
              <span
                class="sev-pill"
                :class="`sev-pill--${threat.severity.toLowerCase()}`"
              >{{ threat.severity }}</span>
              <span class="threat-card__ts">{{ threat.ts }}</span>
            </div>
            <p class="threat-card__name">{{ threat.name }}</p>
            <p class="threat-card__system">{{ threat.system }}</p>
          </article>
        </div>
      </section>

      <!-- ── Section 4: Recent Incidents ───────────────────────────── -->
      <section class="incidents-section" aria-labelledby="incidents-heading">
        <div class="section-header">
          <h2 id="incidents-heading" class="section-title">Recent Incidents</h2>
          <span
            class="incident-count"
            :aria-label="`${activeIncidentCount} active incidents`"
          >{{ activeIncidentCount }} active</span>
        </div>
        <ul class="incident-list" role="list" aria-label="Recent security incidents">
          <li
            v-for="inc in incidents"
            :key="inc.id"
            class="incident-row"
            role="listitem"
          >
            <span
              class="incident-dot"
              :class="`incident-dot--${inc.status}`"
              aria-hidden="true"
            ></span>
            <div class="incident-body">
              <span class="incident-id">{{ inc.id }}</span>
              <span class="incident-title">{{ inc.title }}</span>
            </div>
            <span class="incident-time">{{ inc.time }}</span>
          </li>
        </ul>
      </section>

    </div><!-- /page__content -->

    <!-- ── Section 5: Fixed Bottom Nav ───────────────────────────────── -->
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
/* NOTE: --space-unit = 0.375rem for mobile (NOT 0.5rem like app/site) */
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-width: var(--container-max);
  margin: 0 auto;
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

/* ── Scrollable content area ────────────────────────────────────────── */
.page__content {
  flex: 1;
  overflow-y: auto;
  /* Clear fixed bottom nav + iOS safe area + breathing room */
  padding-bottom: calc(
    calc(var(--space-unit) * 12) +
    env(safe-area-inset-bottom, 0px) +
    calc(var(--space-unit) * 4)
  );
}

/* ── Page header ────────────────────────────────────────────────────── */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 4);
  background: linear-gradient(180deg, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 85%, var(--brand-bg)));
  border-bottom: 1px solid var(--brand-border);
  position: sticky;
  top: 0;
  z-index: 50;
}

.page-header__brand {
  font-family: var(--font-heading);
  font-size: 1.0625rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--brand-primary);
}

.page-header__right {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.page-header__status {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
}

.hdr-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  flex-shrink: 0;
}

.hdr-dot--active  { background-color: var(--brand-primary);   }
.hdr-dot--standby { background-color: var(--brand-secondary); }
.hdr-dot--offline { background-color: var(--brand-error);     }

.hdr-online {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

.page-header__time {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

/* ── Section 1: Gauge ───────────────────────────────────────────────── */
.gauge-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 4) calc(var(--space-unit) * 4);
  background: radial-gradient(ellipse 70% 50% at 50% 0%, color-mix(in srgb, var(--brand-primary) 5%, transparent), transparent);
}

.gauge-wrap {
  position: relative;
  width: 100%;
  max-width: calc(var(--space-unit) * 53);
}

/* SVG fills the wrapper; height is intrinsic from viewBox */
.gauge-ring {
  width: 100%;
  height: auto;
  display: block;
}

.gauge-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  pointer-events: none;
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
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.gauge-accessible-label {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  text-align: center;
  margin-top: calc(var(--space-unit) * 2);
}

/* ── Section 2: Agent strip ─────────────────────────────────────────── */
.agent-section {
  background: linear-gradient(180deg, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 80%, var(--brand-bg)));
  border-top: 1px solid var(--brand-border);
  border-bottom: 1px solid var(--brand-border);
}

.agent-strip {
  display: flex;
  justify-content: space-around;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 2);
}

.agent-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
  min-width: calc(var(--space-unit) * 12);
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

.agent-dot--active  { background-color: var(--brand-primary);   animation: pulse 2s var(--easing) infinite; }
.agent-dot--standby { background-color: var(--brand-secondary); }
.agent-dot--offline { background-color: var(--brand-error);     }

.agent-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

/* ── Shared section header ──────────────────────────────────────────── */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: calc(var(--space-unit) * 3);
}

.section-title {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin: 0;
}

/* ── Section 3: Threat feed ─────────────────────────────────────────── */
.feed-section {
  padding: calc(var(--space-unit) * 4);
}

.live-badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  color: var(--brand-error);
  letter-spacing: 0.06em;
}

.threat-list {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.threat-card {
  background-color: var(--brand-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: calc(var(--space-unit) * 4);
  border-left: 3px solid transparent;
  transition: box-shadow var(--duration-fast) var(--easing);
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
  font-size: 0.6875rem;
  color: var(--brand-muted);
}

.threat-card__name {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 700;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 1);
  line-height: 1.4;
}

.threat-card__system {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  margin: 0;
}

/* ── Severity pills ─────────────────────────────────────────────────── */
.sev-pill {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  line-height: 1;
}

.sev-pill--critical { background-color: var(--brand-error);   color: var(--brand-bg); }
.sev-pill--high     { background-color: var(--brand-accent);  color: var(--brand-bg); }
.sev-pill--medium   { background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent); color: var(--brand-text); }
.sev-pill--low      { background-color: var(--brand-secondary); color: var(--brand-bg); }

/* ── Section 4: Incidents ───────────────────────────────────────────── */
.incidents-section {
  padding: calc(var(--space-unit) * 4);
  padding-top: calc(var(--space-unit) * 2);
}

.incident-count {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-accent);
}

.incident-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
}

.incident-row {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) 0;
  border-bottom: 1px solid var(--brand-border);
}

.incident-row:last-child {
  border-bottom: none;
}

.incident-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  flex-shrink: 0;
}

.incident-dot--active        { background-color: var(--brand-error);     }
.incident-dot--investigating { background-color: var(--brand-accent);    }
.incident-dot--contained     { background-color: var(--brand-secondary); }
.incident-dot--resolved      { background-color: var(--brand-primary);   }

.incident-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
  min-width: 0;
}

.incident-id {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  color: var(--brand-muted);
  letter-spacing: 0.06em;
}

.incident-title {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.incident-time {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  flex-shrink: 0;
}

/* ── Section 5: Bottom nav ──────────────────────────────────────────── */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  max-width: var(--container-max);
  margin: 0 auto;
  background-color: var(--brand-bg-secondary);
  border-top: 1px solid var(--brand-border);
  display: flex;
  align-items: stretch;
  padding-bottom: env(safe-area-inset-bottom, 0px);
  box-shadow: 0 -1px 0 var(--brand-border);
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
  transition:
    color var(--duration-fast) var(--easing),
    background-color var(--duration-fast) var(--easing);
  /* Remove iOS tap flash */
  -webkit-tap-highlight-color: transparent;
}

.nav-tab:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

.nav-tab:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 50%, transparent);
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
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

/* ── Keyframes ──────────────────────────────────────────────────────── */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.75;
    transform: scale(1.1);
    box-shadow: 0 0 8px color-mix(in srgb, var(--brand-primary) 30%, transparent);
  }
}

/* ── Reduced motion (LAST RULE) ─────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
  .agent-dot--active {
    animation: none;
  }
}
</style>

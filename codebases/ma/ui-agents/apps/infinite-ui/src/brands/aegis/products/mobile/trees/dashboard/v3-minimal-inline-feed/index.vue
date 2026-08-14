<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/mobile/dashboard/v3-minimal-inline-feed
// Layout: sticky header → oversized 240×240 gauge hero (no card wrapper) →
//         agent strip → flat inline threat rows (no cards) → incidents → fixed bottom nav
//
// Variant differentiator:
//   v1 (gauge-card-stack): centered gauge, then stacked card-style threat entries
//   v2 (scroll-feed-bar):  compact header + mini-gauge, horizontal-scroll snap cards
//   v3 (this one): oversized gauge fills the top, everything below is minimal/flat — no
//                  card chrome, just rows. Maximum data density, minimum visual noise.
//
// CRITICAL: --space-unit = 0.375rem (mobile override — NOT 0.5rem)
//   * 1 = 0.375rem (6px)    * 4 = 1.5rem (24px)    * 8 = 3rem (48px — min touch target)
//   * 2 = 0.75rem  (12px)   * 6 = 2.25rem (36px)   * 12 = 4.5rem (72px — nav height)
//   * 3 = 1.125rem (18px)   * 16 = 6rem (96px)

// ── Types ─────────────────────────────────────────────────────────
interface ThreatEntry {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  system: string
  ts: string
}

interface Incident {
  id: number
  title: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  openedAt: string
}

interface Agent {
  id: string
  name: string
  status: 'active' | 'standby' | 'offline'
}

// ── Gauge math ─────────────────────────────────────────────────────
// v3 uses oversized 240×240 SVG, r=100
const posturePercent = ref(83)
const gaugeRadius = 100
const gaugeCircumference = 2 * Math.PI * gaugeRadius  // 628.318
const gaugeDashOffset = computed(() =>
  gaugeCircumference * (1 - posturePercent.value / 100)
)

// ── Agent data ─────────────────────────────────────────────────────
const agents: Agent[] = [
  { id: 'scanner',   name: 'Scanner',   status: 'active'  },
  { id: 'monitor',   name: 'Monitor',   status: 'active'  },
  { id: 'responder', name: 'Responder', status: 'active'  },
  { id: 'sentinel',  name: 'Sentinel',  status: 'standby' },
]

// ── Threat data ─────────────────────────────────────────────────────
const threats = ref<ThreatEntry[]>([
  { id: 1,  name: 'Prompt Injection',          severity: 'CRITICAL', system: 'api-gateway-01',    ts: '2s ago'   },
  { id: 2,  name: 'Data Exfiltration',          severity: 'HIGH',     system: 'llm-worker-07',    ts: '14s ago'  },
  { id: 3,  name: 'Token Privilege Escalation', severity: 'CRITICAL', system: 'orchestrator-02',  ts: '34s ago'  },
  { id: 4,  name: 'Model Poisoning Probe',      severity: 'HIGH',     system: 'fine-tune-03',     ts: '1m ago'   },
  { id: 5,  name: 'Unusual API Call Pattern',   severity: 'MEDIUM',   system: 'api-gateway-02',   ts: '2m ago'   },
  { id: 6,  name: 'Repeated Auth Failure',      severity: 'MEDIUM',   system: 'auth-service',     ts: '3m ago'   },
  { id: 7,  name: 'Tool Invocation Anomaly',    severity: 'LOW',      system: 'agent-runner-05',  ts: '4m ago'   },
  { id: 8,  name: 'Context Overflow Probe',     severity: 'MEDIUM',   system: 'llm-worker-02',    ts: '6m ago'   },
  { id: 9,  name: 'Rate Limit Bypass',          severity: 'HIGH',     system: 'rate-limiter-01',  ts: '8m ago'   },
  { id: 10, name: 'Jailbreak Attempt',          severity: 'CRITICAL', system: 'llm-worker-04',    ts: '9m ago'   },
  { id: 11, name: 'Embedding Query Probe',      severity: 'MEDIUM',   system: 'vector-store-01',  ts: '11m ago'  },
  { id: 12, name: 'Memory Store Enumeration',   severity: 'HIGH',     system: 'memory-svc-02',    ts: '14m ago'  },
])

const showAllThreats = ref(false)
const visibleThreats = computed(() =>
  showAllThreats.value ? threats.value : threats.value.slice(0, 6)
)

// ── Incident data ───────────────────────────────────────────────────
const incidents = ref<Incident[]>([
  { id: 1, title: 'Prompt injection campaign',  severity: 'CRITICAL', openedAt: '14m' },
  { id: 2, title: 'Exfiltration attempt',        severity: 'HIGH',     openedAt: '22m' },
  { id: 3, title: 'Token privilege escalation',  severity: 'CRITICAL', openedAt: '41m' },
  { id: 4, title: 'Model poisoning probe',        severity: 'HIGH',     openedAt: '1h'  },
  { id: 5, title: 'Anomalous API call pattern',  severity: 'MEDIUM',   openedAt: '2h'  },
])

// ── Bottom nav ──────────────────────────────────────────────────────
const activeTab = ref('dashboard')
const navTabs = [
  { id: 'dashboard', label: 'Dashboard', icon: '⬡' },
  { id: 'alerts',    label: 'Alerts',    icon: '◈' },
  { id: 'agents',    label: 'Agents',    icon: '◉' },
  { id: 'settings',  label: 'Settings',  icon: '◇' },
]

// ── Live clock ──────────────────────────────────────────────────────
function formatTime(): string {
  return new Date().toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  })
}
const currentTime = ref(formatTime())
let clockInterval: ReturnType<typeof setInterval> | null = null

// ── Mount/unmount ───────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  nextTick(() => {
    isMounted.value = true
  })
  clockInterval = setInterval(() => {
    currentTime.value = formatTime()
  }, 1000)
})

onUnmounted(() => {
  if (clockInterval) {
    clearInterval(clockInterval)
    clockInterval = null
  }
})
</script>

<template>
  <div
    class="page"
    :class="{ 'is-mounted': isMounted }"
    aria-label="Aegis Mobile Security Command Center"
  >
    <!-- ── SR-only page title ─────────────────────────────────── -->
    <h1 class="sr-only">Aegis Mobile Command Center</h1>

    <!-- ── Sticky page header ────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Command center header">
      <div class="page-header__left">
        <span class="page-header__logo">AEGIS SOC</span>
      </div>
      <div class="page-header__right">
        <span class="live-dot" aria-hidden="true"></span>
        <span
          class="page-header__time"
          aria-label="Current time"
          role="timer"
        >{{ currentTime }}</span>
      </div>
    </header>

    <!-- ── Scrollable content ────────────────────────────────── -->
    <main class="page__content" role="main" id="main-content">

      <!-- ══════════════════════════════════════
           SECTION 1 — Defense Posture Gauge
           Oversized 240×240 — v3's hero element
           ══════════════════════════════════════ -->
      <section
        class="gauge-section"
        aria-labelledby="gauge-heading"
      >
        <div class="gauge-hero">
          <svg
            class="gauge-svg"
            viewBox="0 0 240 240"
            aria-hidden="true"
          >
            <defs>
              <linearGradient id="gaugeGradV3Mobile" x1="0%" y1="0%" x2="100%" y2="0%">
                <!-- gradient order: error(danger) → accent(risk) → primary(secured) -->
                <stop offset="0%"   stop-color="var(--brand-error)"   />
                <stop offset="40%"  stop-color="var(--brand-accent)"  />
                <stop offset="100%" stop-color="var(--brand-primary)" />
              </linearGradient>
            </defs>
            <!-- Track ring -->
            <circle
              class="gauge-track"
              cx="120" cy="120"
              :r="gaugeRadius"
              fill="none"
              stroke-width="16"
            />
            <!-- Filled arc — rotated to start at top -->
            <circle
              class="gauge-fill"
              cx="120" cy="120"
              :r="gaugeRadius"
              fill="none"
              stroke="url(#gaugeGradV3Mobile)"
              stroke-width="16"
              stroke-linecap="round"
              :stroke-dasharray="gaugeCircumference"
              :stroke-dashoffset="gaugeDashOffset"
              transform="rotate(-90 120 120)"
            />
          </svg>

          <!-- Centered text readout — absolutely positioned over SVG -->
          <div
            class="gauge-center"
            :aria-label="`${posturePercent}% systems secured`"
          >
            <span class="gauge-center__pct" id="gauge-heading">{{ posturePercent }}%</span>
            <span class="gauge-center__label">Systems Secured</span>
            <span class="gauge-center__count">847 / 1,024 systems</span>
          </div>
        </div>
      </section>

      <!-- ══════════════════════════════════════
           SECTION 2 — Agent Status Strip
           ══════════════════════════════════════ -->
      <section
        class="agent-section"
        aria-labelledby="agents-section-label"
      >
        <span id="agents-section-label" class="sr-only">Agent team status</span>
        <div class="agent-strip" role="list" aria-label="Agent operational status">
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

      <!-- ══════════════════════════════════════
           SECTION 3 — Threat Intel (inline rows)
           v3 differentiator: no card wrappers,
           just flat rows for maximum density
           ══════════════════════════════════════ -->
      <section
        class="threats-section"
        aria-labelledby="threats-heading"
      >
        <div class="section-header-row">
          <h2 id="threats-heading" class="section-title">Threat Intel</h2>
          <span
            class="section-count"
            :aria-label="`${threats.length} active threats`"
          >{{ threats.length }} active</span>
        </div>

        <ul
          class="threat-rows"
          role="list"
          aria-label="Active threat detections"
        >
          <li
            v-for="threat in visibleThreats"
            :key="threat.id"
            class="threat-row"
            :class="`threat-row--${threat.severity.toLowerCase()}`"
            role="listitem"
            :aria-label="`${threat.severity}: ${threat.name} on ${threat.system}, ${threat.ts}`"
          >
            <span
              class="threat-row__dot"
              :class="`threat-dot--${threat.severity.toLowerCase()}`"
              aria-hidden="true"
            ></span>
            <span
              class="sev-pill"
              :class="`sev-pill--${threat.severity.toLowerCase()}`"
            >{{ threat.severity }}</span>
            <span class="threat-row__name">{{ threat.name }}</span>
            <span class="threat-row__ts">{{ threat.ts }}</span>
          </li>
        </ul>

        <button
          v-if="threats.length > 6"
          type="button"
          class="show-more-btn"
          :aria-expanded="showAllThreats"
          @click="showAllThreats = !showAllThreats"
        >
          {{ showAllThreats ? 'Show less' : `Show all ${threats.length} threats` }}
        </button>
      </section>

      <!-- ══════════════════════════════════════
           SECTION 4 — Recent Incidents
           ══════════════════════════════════════ -->
      <section
        class="incidents-section"
        aria-labelledby="incidents-heading"
      >
        <div class="section-header-row">
          <h2 id="incidents-heading" class="section-title">Recent Incidents</h2>
          <span
            class="section-count section-count--threat"
            :aria-label="`${incidents.length} open incidents`"
          >{{ incidents.length }} open</span>
        </div>

        <ul
          class="incident-rows"
          role="list"
          aria-label="Recent security incidents"
        >
          <li
            v-for="inc in incidents"
            :key="inc.id"
            class="incident-row"
            role="listitem"
            :aria-label="`${inc.severity} incident: ${inc.title}, opened ${inc.openedAt} ago`"
          >
            <span
              class="incident-row__dot"
              :class="`inc-dot--${inc.severity.toLowerCase()}`"
              aria-hidden="true"
            ></span>
            <span class="incident-row__title">{{ inc.title }}</span>
            <span class="incident-row__time">{{ inc.openedAt }}</span>
          </li>
        </ul>
      </section>

    </main>

    <!-- ── Fixed bottom navigation ───────────────────────────── -->
    <nav class="bottom-nav" aria-label="Main navigation">
      <button
        v-for="tab in navTabs"
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
/* ── Reset ────────────────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* ── SR-only utility ──────────────────────────────────────────────── */
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

/* ── Page root ────────────────────────────────────────────────────── */
/* --space-unit on mobile = 0.375rem — all calc() values are tighter  */
.page {
  max-width: var(--container-max);   /* 428px */
  margin: 0 auto;
  min-height: 100vh;
  background-color: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  opacity: 0;
  transition: opacity var(--duration-normal) var(--easing);
}

.page.is-mounted {
  opacity: 1;
}

/* ── Scrollable content — clears fixed nav + iOS safe area ───────── */
.page__content {
  flex: 1;
  overflow-y: auto;
  /* nav height (72px) + safe area + breathing room */
  padding-bottom: calc(
    calc(var(--space-unit) * 12) +
    env(safe-area-inset-bottom) +
    calc(var(--space-unit) * 4)
  );
}

/* ── Sticky page header ───────────────────────────────────────────── */
.page-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: linear-gradient(180deg, var(--brand-bg), color-mix(in srgb, var(--brand-bg) 97%, var(--brand-primary)));
  border-bottom: 1px solid var(--brand-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  flex-shrink: 0;
}

.page-header__left {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.page-header__logo {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--brand-primary);
}

.page-header__right {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.live-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  background-color: var(--brand-error);
  flex-shrink: 0;
  animation: pulse 1.5s var(--easing) infinite;
}

.page-header__time {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);   /* caption context — acceptable */
}

/* ── Gauge section ────────────────────────────────────────────────── */
/* v3: gauge floats directly in a padded section, NO card wrapper     */
.gauge-section {
  display: flex;
  justify-content: center;
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 4);
  background: linear-gradient(180deg, color-mix(in srgb, var(--brand-bg) 92%, var(--brand-accent)), var(--brand-bg));
}

.gauge-hero {
  position: relative;
  width: 100%;
  /* max-width: 384px — fits comfortably within 428px minus padding */
  max-width: calc(var(--space-unit) * 64);
  display: flex;
  justify-content: center;
}

.gauge-svg {
  width: 100%;
  height: auto;
  display: block;
}

.gauge-track {
  stroke: var(--brand-border);
}

.gauge-fill {
  transition: stroke-dashoffset var(--duration-slow) var(--easing);
}

/* Readout centered absolutely over the SVG */
.gauge-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 0.5);
  pointer-events: none;
}

.gauge-center__pct {
  font-family: var(--font-mono);
  font-size: 2.5rem;           /* mobile h1 scale — updated */
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
  color: var(--brand-muted);   /* caption context — OK */
}

.gauge-center__count {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
}

/* ── Agent status strip ───────────────────────────────────────────── */
.agent-section {
  background-color: var(--brand-bg-secondary);
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
  min-width: calc(var(--space-unit) * 12);  /* 72px — touch-target width */
}

/* Dot container — 48px touch target */
.agent-dot-wrap {
  width: calc(var(--space-unit) * 8);    /* 3rem = 48px */
  height: calc(var(--space-unit) * 8);   /* 3rem = 48px — WCAG 2.5.5 min */
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

.agent-indicator--offline .agent-dot-wrap {
  background-color: color-mix(in srgb, var(--brand-error) 10%, transparent);
}

/* Inner coloured dot */
.agent-dot {
  width: calc(var(--space-unit) * 5);    /* 1.875rem ≈ 30px */
  height: calc(var(--space-unit) * 5);
  border-radius: 50%;
  transition: background-color var(--duration-normal) var(--easing);
}

.agent-dot--active {
  background-color: var(--brand-primary);
  animation: pulse 2s var(--easing) infinite;
}

.agent-dot--standby {
  background-color: var(--brand-secondary);
}

.agent-dot--offline {
  background-color: var(--brand-error);
}

/* Agent name label */
.agent-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

/* ── Threat intel section ─────────────────────────────────────────── */
.threats-section {
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 4) 0;
}

.section-header-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: calc(var(--space-unit) * 3);
}

.section-title {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-text);
  margin: 0;
}

.section-count {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-accent);   /* active/threat count = crimson */
}

.section-count--threat {
  color: var(--brand-accent);
}

/* Threat rows — flat list, no card chrome (v3 differentiator) */
.threat-rows {
  list-style: none;
  padding: 0;
  margin: 0;
}

.threat-row {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 3) auto 1fr auto;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  padding: calc(var(--space-unit) * 2.5) 0;
  border-bottom: 1px solid var(--brand-border);
  min-height: calc(var(--space-unit) * 8);  /* 48px — WCAG 2.5.5 touch */
}

.threat-row:last-child {
  border-bottom: none;
}

/* Severity dot (left column) */
.threat-row__dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.threat-dot--critical {
  background-color: var(--brand-error);
}
.threat-dot--high {
  background-color: var(--brand-accent);
}
.threat-dot--medium {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
}
.threat-dot--low {
  background-color: var(--brand-secondary);
}

/* Severity pill badge */
/* All badge text uses --brand-bg for contrast:
   error: 5.33:1 ✅  accent: 4.74:1 ✅  secondary: 5.78:1 ✅ */
.sev-pill {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.5) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  white-space: nowrap;
  flex-shrink: 0;
  line-height: 1.4;
}

.sev-pill--critical {
  background-color: var(--brand-error);
  color: var(--brand-bg);
}

.sev-pill--high {
  background-color: var(--brand-accent);
  color: var(--brand-bg);
}

.sev-pill--medium {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text);   /* 7.44:1 on this mixed bg ✅ */
}

.sev-pill--low {
  background-color: var(--brand-secondary);
  color: var(--brand-bg);
}

.threat-row__name {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.threat-row__ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);   /* timestamp — caption context ✅ */
  white-space: nowrap;
  flex-shrink: 0;
}

/* Show all / show less toggle */
.show-more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: calc(var(--space-unit) * 3) 0;
  background: none;
  border: none;
  border-top: 1px solid var(--brand-border);
  color: var(--brand-secondary);
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  cursor: pointer;
  min-height: calc(var(--space-unit) * 8);  /* 48px touch target */
  transition: color var(--duration-fast) var(--easing);
}

.show-more-btn:hover {
  color: var(--brand-primary);
}

.show-more-btn:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

/* ── Incidents section ────────────────────────────────────────────── */
.incidents-section {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 4);
}

.incident-rows {
  list-style: none;
  padding: 0;
  margin: 0;
}

.incident-row {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 2.5) 1fr auto;
  align-items: center;
  gap: calc(var(--space-unit) * 2.5);
  padding: calc(var(--space-unit) * 3) 0;
  border-bottom: 1px solid var(--brand-border);
  min-height: calc(var(--space-unit) * 8);  /* 48px touch target */
}

.incident-row:last-child {
  border-bottom: none;
}

.incident-row__dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.inc-dot--critical {
  background-color: var(--brand-error);
}
.inc-dot--high {
  background-color: var(--brand-accent);
}
.inc-dot--medium {
  background-color: var(--brand-secondary);
}

.incident-row__title {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.incident-row__time {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);   /* timestamp — caption ✅ */
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Fixed bottom navigation ──────────────────────────────────────── */
/* max-width + margin: 0 auto mirrors the .page container             */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: var(--container-max);
  margin: 0 auto;
  z-index: 100;
  background-color: var(--brand-bg-secondary);
  border-top: 1px solid var(--brand-border);
  display: flex;
  align-items: stretch;
  /* iOS home indicator safe area */
  padding-bottom: env(safe-area-inset-bottom);
}

.nav-tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 1);
  /* 72px — WCAG 2.5.5 large target */
  min-height: calc(var(--space-unit) * 12);
  background: none;
  border: none;
  cursor: pointer;
  color: color-mix(in srgb, var(--brand-text) 50%, transparent);
  font-family: var(--font-body);
  padding: calc(var(--space-unit) * 2) 0;
  transition:
    color var(--duration-fast) var(--easing),
    background-color var(--duration-fast) var(--easing);
  /* Removes iOS tap highlight flash */
  -webkit-tap-highlight-color: transparent;
}

.nav-tab:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

.nav-tab:hover:not(.nav-tab--active) {
  color: color-mix(in srgb, var(--brand-text) 75%, transparent);
  background-color: color-mix(in srgb, var(--brand-surface) 40%, transparent);
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

/* ── Keyframe animations ──────────────────────────────────────────── */
/* Active agent dots and live header dot */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
    box-shadow: 0 0 6px color-mix(in srgb, var(--brand-primary) 30%, transparent);
  }
}

/* ── Reduced motion — FINAL CSS rule (double guard) ──────────────── */
@media (prefers-reduced-motion: reduce) {
  .agent-dot--active,
  .live-dot {
    animation: none !important;
  }

  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
</style>

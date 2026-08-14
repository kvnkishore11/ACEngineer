<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

// aegis/mobile/alerts/v3-timeline-floating-filters
// Layout: sticky page header → sticky floating filter bar → inline alert stream →
//         resolved history → fixed bottom nav
//
// Variant differentiator:
//   v1 (stacked-swipe-cards): full alert cards with swipe hint strips behind them
//   v2 (severity-accordions): four collapsible groups, no separate filter bar
//   v3 (this one): timeline-first reading flow. Compact inline rows (no card chrome).
//                  Sticky filter bar floats while scrolling. Maximum info density.
//
// CRITICAL: --space-unit = 0.375rem (mobile override — NOT 0.5rem)
//   * 8  = 3rem = 48px (min touch target)
//   * 12 = 4.5rem = 72px (bottom nav height)
//   * 21 = 7.875rem ≈ 84px (filter bar sticky top, below page header)

// ── Types ──────────────────────────────────────────────────────────
interface Alert {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  system: string
  ts: string
  desc: string
  status: 'active' | 'acknowledged'
}

interface ResolvedAlert {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  resolvedBy: string
  ttResolve: string
  resolvedAt: string
}

// ── Active alerts data ─────────────────────────────────────────────
const alerts = ref<Alert[]>([
  {
    id: 1,
    name: 'Prompt Injection',
    severity: 'CRITICAL',
    system: 'api-gateway-01',
    ts: '2s',
    desc: 'System prompt override detected in ingress traffic',
    status: 'active',
  },
  {
    id: 2,
    name: 'Data Exfiltration',
    severity: 'HIGH',
    system: 'llm-worker-07',
    ts: '14s',
    desc: 'Unusual volume of outbound API calls to unknown endpoint',
    status: 'active',
  },
  {
    id: 3,
    name: 'Token Privilege Escalation',
    severity: 'CRITICAL',
    system: 'orchestrator-02',
    ts: '34s',
    desc: 'Agent token used to access restricted configuration endpoint',
    status: 'active',
  },
  {
    id: 4,
    name: 'Model Poisoning Probe',
    severity: 'HIGH',
    system: 'fine-tune-03',
    ts: '1m',
    desc: 'Adversarial input pattern targeting fine-tuning pipeline',
    status: 'active',
  },
  {
    id: 5,
    name: 'Unusual API Pattern',
    severity: 'MEDIUM',
    system: 'api-gateway-02',
    ts: '2m',
    desc: 'Request frequency exceeds behavioral baseline by 340%',
    status: 'active',
  },
  {
    id: 6,
    name: 'Auth Failure Cluster',
    severity: 'MEDIUM',
    system: 'auth-service',
    ts: '3m',
    desc: 'Repeated authentication failures from single IP subnet',
    status: 'acknowledged',
  },
  {
    id: 7,
    name: 'Context Overflow Probe',
    severity: 'CRITICAL',
    system: 'llm-worker-02',
    ts: '4m',
    desc: 'Payload crafted to exceed context window boundary',
    status: 'active',
  },
])

// ── Resolved alert history data ────────────────────────────────────
const resolvedAlerts = ref<ResolvedAlert[]>([
  { id: 101, name: 'Jailbreak Attempt',       severity: 'CRITICAL', resolvedBy: 'Responder', ttResolve: '2m 14s', resolvedAt: '8m ago'  },
  { id: 102, name: 'Rate Limit Bypass',        severity: 'HIGH',     resolvedBy: 'Scanner',   ttResolve: '1m 44s', resolvedAt: '14m ago' },
  { id: 103, name: 'Embedding Query Probe',    severity: 'MEDIUM',   resolvedBy: 'Monitor',   ttResolve: '4m 07s', resolvedAt: '22m ago' },
  { id: 104, name: 'Memory Store Enumeration', severity: 'HIGH',     resolvedBy: 'Scanner',   ttResolve: '3m 31s', resolvedAt: '38m ago' },
])

// ── Filter state ───────────────────────────────────────────────────
const activeFilter = ref('all')

// Counts computed from live data
const filterCounts = computed(() => ({
  all:      alerts.value.length,
  critical: alerts.value.filter(a => a.severity === 'CRITICAL').length,
  high:     alerts.value.filter(a => a.severity === 'HIGH').length,
  medium:   alerts.value.filter(a => a.severity === 'MEDIUM').length,
}))

const filterDefs = [
  { id: 'all',      label: 'All'      },
  { id: 'critical', label: 'Critical' },
  { id: 'high',     label: 'High'     },
  { id: 'medium',   label: 'Medium'   },
]

const filteredAlerts = computed(() =>
  activeFilter.value === 'all'
    ? alerts.value
    : alerts.value.filter(a => a.severity.toLowerCase() === activeFilter.value)
)

// Three-tier count color: CRITICAL → error, HIGH → accent, else → primary
const countColorClass = computed(() => {
  if (alerts.value.some(a => a.severity === 'CRITICAL')) return 'count--error'
  if (alerts.value.some(a => a.severity === 'HIGH'))     return 'count--accent'
  return 'count--primary'
})

// ── Bottom nav ─────────────────────────────────────────────────────
const activeTab = ref('alerts')
const navTabs = [
  { id: 'dashboard', label: 'Dashboard', icon: '⬡' },
  { id: 'alerts',    label: 'Alerts',    icon: '◈' },
  { id: 'agents',    label: 'Agents',    icon: '◉' },
  { id: 'settings',  label: 'Settings',  icon: '◇' },
]

// ── Live clock ─────────────────────────────────────────────────────
function formatTime(): string {
  return new Date().toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  })
}
const currentTime = ref(formatTime())
let clockInterval: ReturnType<typeof setInterval> | null = null

// ── Mount ──────────────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  isMounted.value = true
  clockInterval = setInterval(() => {
    currentTime.value = formatTime()
  }, 60_000)
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
    aria-label="Aegis Mobile Alerts"
  >
    <!-- ── SR-only page title ────────────────────────────────── -->
    <h1 class="sr-only">Aegis Mobile Alerts</h1>

    <!-- ── Sticky page header ───────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Alerts command header">
      <div class="page-header__top">
        <span class="page-header__brand">AEGIS ALERTS</span>
        <div class="page-header__meta">
          <span class="live-dot" aria-hidden="true"></span>
          <span class="page-header__time" aria-label="Current time">{{ currentTime }}</span>
        </div>
      </div>
      <div class="page-header__count">
        <span
          class="alert-count"
          :class="countColorClass"
          :aria-label="`${alerts.length} active alerts`"
        >{{ alerts.length }}</span>
        <span class="alert-count__label">Active Alerts</span>
      </div>
    </header>

    <!-- ── Sticky floating filter bar ───────────────────────── -->
    <!-- position: sticky (NOT fixed) — stays in flow, no padding-top needed below -->
    <div
      class="filter-bar-wrap"
      role="group"
      aria-label="Filter alerts by severity"
    >
      <div class="filter-bar">
        <button
          v-for="f in filterDefs"
          :key="f.id"
          type="button"
          class="filter-pill"
          :class="[
            `filter-pill--${f.id}`,
            { 'filter-pill--active': activeFilter === f.id },
          ]"
          :aria-pressed="activeFilter === f.id"
          @click="activeFilter = f.id"
        >
          {{ f.label }}
          <span class="filter-pill__badge" aria-hidden="true">
            {{ filterCounts[f.id as keyof typeof filterCounts] }}
          </span>
        </button>
      </div>
    </div>

    <!-- ── Scrollable main content ──────────────────────────── -->
    <main id="main-content" class="page-content" role="main">

      <!-- ══════════════════════════════════
           ACTIVE ALERTS — inline rows
           v3 differentiator: no card chrome,
           just compact left-bar + text rows
           ══════════════════════════════════ -->
      <section
        class="alerts-section"
        aria-labelledby="active-heading"
      >
        <div class="section-divider">
          <span id="active-heading" class="section-divider__label">Active</span>
          <span
            class="section-divider__count"
            :class="countColorClass"
            aria-hidden="true"
          >{{ filteredAlerts.length }}</span>
        </div>

        <div
          class="alert-stream"
          role="list"
          aria-label="Active security alerts"
        >
          <!-- Alert rows — inline, no card shells -->
          <div
            v-for="alert in filteredAlerts"
            :key="alert.id"
            class="alert-row"
            :class="`alert-row--${alert.severity.toLowerCase()}`"
            role="listitem"
            :aria-label="`${alert.severity} alert: ${alert.name} on ${alert.system}, ${alert.ts} ago. ${alert.desc}`"
          >
            <!-- Left: severity bar + timestamp column -->
            <div class="alert-row__left" aria-hidden="true">
              <div
                class="alert-row__bar"
                :class="`alert-bar--${alert.severity.toLowerCase()}`"
              ></div>
              <span class="alert-row__ts">{{ alert.ts }}</span>
            </div>

            <!-- Right: body content -->
            <div class="alert-row__body">
              <div class="alert-row__top">
                <span
                  class="sev-pill"
                  :class="`sev-pill--${alert.severity.toLowerCase()}`"
                >{{ alert.severity }}</span>
                <span class="alert-row__name">{{ alert.name }}</span>
              </div>
              <span class="alert-row__system">{{ alert.system }}</span>
              <p class="alert-row__desc">{{ alert.desc }}</p>
            </div>
          </div>

          <!-- Empty state when filter yields no results -->
          <p
            v-if="filteredAlerts.length === 0"
            class="empty-state"
            aria-live="polite"
          >
            No {{ activeFilter === 'all' ? '' : activeFilter }} alerts
          </p>
        </div>
      </section>

      <!-- ══════════════════════════════════
           RESOLVED HISTORY
           Dimmed white/muted contrast vs
           active crimson bars above
           ══════════════════════════════════ -->
      <section
        class="history-section"
        aria-labelledby="history-heading"
      >
        <div class="section-divider">
          <span id="history-heading" class="section-divider__label">Resolved</span>
          <span class="section-divider__count section-divider__count--resolved" aria-hidden="true">
            {{ resolvedAlerts.length }}
          </span>
        </div>

        <!-- ol = ordered list — chronological history -->
        <ol
          class="history-list"
          role="list"
          aria-label="Resolved alert history"
        >
          <li
            v-for="entry in resolvedAlerts"
            :key="entry.id"
            class="history-entry"
            :aria-label="`Resolved: ${entry.name}, resolved by ${entry.resolvedBy} in ${entry.ttResolve}, ${entry.resolvedAt}`"
          >
            <!-- Track: white dot + vertical connector line (via ::after) -->
            <div class="history-entry__track" aria-hidden="true">
              <span class="history-dot"></span>
            </div>

            <!-- Body: time + name, then meta (agent · TTR) -->
            <div class="history-entry__body">
              <div class="history-entry__top">
                <span class="history-entry__time">{{ entry.resolvedAt }}</span>
                <span class="history-entry__name">{{ entry.name }}</span>
              </div>
              <p class="history-entry__meta">
                <span class="history-entry__agent">{{ entry.resolvedBy }}</span>
                <span class="history-entry__sep" aria-hidden="true"> · </span>
                <span class="history-entry__ttr">{{ entry.ttResolve }}</span>
              </p>
            </div>
          </li>
        </ol>
      </section>

    </main>

    <!-- ── Fixed bottom navigation ──────────────────────────── -->
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
/* --space-unit on mobile = 0.375rem — all spacing is 25% tighter    */
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

/* ── Main content — clears fixed nav + iOS safe area ─────────────── */
.page-content {
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
  z-index: 30;
  background: linear-gradient(180deg, var(--brand-bg), color-mix(in srgb, var(--brand-bg) 96%, var(--brand-accent)));
  border-bottom: 1px solid var(--brand-border);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  flex-shrink: 0;
}

.page-header__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: calc(var(--space-unit) * 2);
}

.page-header__brand {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--brand-primary);
}

.page-header__meta {
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
  animation: blink 1.5s var(--easing) infinite;
}

.page-header__time {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);    /* timestamp — caption context ✅ */
}

.page-header__count {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 2);
}

/* Alert count number — three-tier color logic */
/* contrast: error 5.33:1, accent 4.74:1, primary 17.39:1 — all AA ✅ */
.alert-count {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.count--error   { color: var(--brand-error);   }
.count--accent  { color: var(--brand-accent);  }
.count--primary { color: var(--brand-primary); }

.alert-count__label {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 400;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

/* ── Sticky floating filter bar ───────────────────────────────────── */
/* position: sticky keeps element in flow — no extra content padding   */
/* needed below. This is v3's defining structural element.              */
.filter-bar-wrap {
  position: sticky;
  top: calc(var(--space-unit) * 21);  /* 7.875rem ≈ 84px — just below header */
  z-index: 20;
  background: linear-gradient(180deg, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 95%, var(--brand-primary)));
  border-bottom: 1px solid var(--brand-border);
  box-shadow: 0 calc(var(--space-unit) * 1) calc(var(--space-unit) * 4)
              color-mix(in srgb, var(--brand-bg) 60%, transparent);
  flex-shrink: 0;
}

/* Filter bar itself — overflow-x: auto (NOT hidden) for horizontal scroll */
.filter-bar {
  display: flex;
  gap: calc(var(--space-unit) * 2);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  padding: calc(var(--space-unit) * 2.5) calc(var(--space-unit) * 4);
}

.filter-bar::-webkit-scrollbar {
  display: none;
}

/* Filter pill buttons */
.filter-pill {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
  padding: calc(var(--space-unit) * 1.5) calc(var(--space-unit) * 3);
  border-radius: var(--radius-md);
  border: none;
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  cursor: pointer;
  min-height: calc(var(--space-unit) * 8);  /* 48px — WCAG 2.5.5 min ✅ */
  transition:
    background-color var(--duration-fast) var(--easing),
    color var(--duration-fast) var(--easing);
  -webkit-tap-highlight-color: transparent;
}

.filter-pill:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* Inactive pill states — tinted background, brand-text color */
.filter-pill--all {
  background-color: var(--brand-surface);
  color: var(--brand-text);
}
.filter-pill--critical {
  background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);
  color: var(--brand-text);
}
.filter-pill--high {
  background-color: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  color: var(--brand-text);
}
.filter-pill--medium {
  background-color: color-mix(in srgb, var(--brand-secondary) 15%, transparent);
  color: var(--brand-text);
}

/* Active pill states — solid token background, brand-bg text */
/* Contrast verified: all=17.39:1, critical=5.33:1, high=4.74:1       */
.filter-pill--active.filter-pill--all {
  background-color: var(--brand-primary);
  color: var(--brand-bg);
}
.filter-pill--active.filter-pill--critical {
  background-color: var(--brand-error);
  color: var(--brand-bg);
}
.filter-pill--active.filter-pill--high {
  background-color: var(--brand-accent);
  color: var(--brand-bg);
}
/* medium active: color-mix bg → use brand-text (7.90:1) not brand-bg */
.filter-pill--active.filter-pill--medium {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text);
}

.filter-pill__badge {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  background-color: color-mix(in srgb, var(--brand-bg) 40%, transparent);
  padding: 0 calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  min-width: calc(var(--space-unit) * 4);
  text-align: center;
  line-height: calc(var(--space-unit) * 4);
}

/* ── Section divider ──────────────────────────────────────────────── */
.section-divider {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4)
           calc(var(--space-unit) * 1);
}

/* Horizontal rule after the label+count */
.section-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: var(--brand-border);
}

.section-divider__label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.section-divider__count {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
}

/* Resolved count in primary (white = secured) */
.section-divider__count--resolved {
  color: var(--brand-primary);
}

/* ── Alert stream — inline rows (v3 defining feature) ─────────────── */
/* No card chrome. Just a flat list of rows with a severity bar left.  */
.alert-stream {
  padding: calc(var(--space-unit) * 2) 0;
}

.alert-row {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  border-bottom: 1px solid var(--brand-border);
  min-height: calc(var(--space-unit) * 8);  /* 48px touch target ✅ */
  transition: background-color var(--duration-fast) var(--easing);
}

.alert-row:last-child {
  border-bottom: none;
}

.alert-row:active {
  background-color: color-mix(in srgb, var(--brand-surface) 50%, transparent);
}

/* Left column: severity indicator bar + timestamp */
.alert-row__left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  flex-shrink: 0;
  padding-top: calc(var(--space-unit) * 0.5);
}

/* Vertical severity bar — the left-marker for this row */
.alert-row__bar {
  width: calc(var(--space-unit) * 0.75);
  min-height: calc(var(--space-unit) * 8);  /* stretches with row height */
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.alert-bar--critical {
  background-color: var(--brand-error);
}
.alert-bar--high {
  background-color: var(--brand-accent);
}
.alert-bar--medium {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
}

.alert-row__ts {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  color: var(--brand-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

/* Right column: content body */
.alert-row__body {
  flex: 1;
  min-width: 0;
}

.alert-row__top {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  margin-bottom: calc(var(--space-unit) * 1);
  flex-wrap: wrap;
}

.alert-row__name {
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.alert-row__system {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);  /* system name — caption context ✅ */
  display: block;
  margin-bottom: calc(var(--space-unit) * 1);
}

.alert-row__desc {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  line-height: 1.4;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  margin: 0;
  /* Two-line clamp for compact density */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ── Severity pills ───────────────────────────────────────────────── */
/* All badge text uses --brand-bg for contrast:
   critical (error): 5.33:1 ✅  high (accent): 4.74:1 ✅
   medium: 7.90:1 on color-mix bg ✅                                   */
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
  color: var(--brand-text);
}

/* ── Empty filter state ───────────────────────────────────────────── */
.empty-state {
  padding: calc(var(--space-unit) * 8) calc(var(--space-unit) * 4);
  text-align: center;
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--brand-muted);
  margin: 0;
}

/* ── Alert history section ────────────────────────────────────────── */
.history-section {
  padding-bottom: calc(var(--space-unit) * 4);
}

/* ol: ordered list — chronological history */
.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.history-entry {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  border-bottom: 1px solid var(--brand-border);
  min-height: calc(var(--space-unit) * 8);  /* 48px touch ✅ */
}

.history-entry:last-child {
  border-bottom: none;
}

/* Track: dot + vertical connector via ::after */
.history-entry__track {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  padding-top: calc(var(--space-unit) * 0.75);
}

.history-entry__track::after {
  content: '';
  flex: 1;
  width: 1px;
  background-color: var(--brand-border);
  margin-top: calc(var(--space-unit) * 1);
  min-height: calc(var(--space-unit) * 4);
}

.history-entry:last-child .history-entry__track::after {
  display: none;
}

/* White dot = resolved = Aegis promise kept */
.history-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  background-color: var(--brand-primary);
  flex-shrink: 0;
}

.history-entry__body {
  flex: 1;
  min-width: 0;
}

.history-entry__top {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 2);
  margin-bottom: calc(var(--space-unit) * 1);
}

.history-entry__time {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);  /* timestamp — caption ✅ */
  flex-shrink: 0;
}

/* Dimmed vs active crimson bars above — `color-mix` NOT `opacity` */
.history-entry__name {
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.history-entry__meta {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);  /* caption context ✅ */
  margin: 0;
}

.history-entry__sep {
  color: var(--brand-border);
}

/* ── Fixed bottom navigation ──────────────────────────────────────── */
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
  padding-bottom: env(safe-area-inset-bottom);
}

.nav-tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 1);
  min-height: calc(var(--space-unit) * 12);   /* 72px — WCAG 2.5.5 ✅ */
  background: none;
  border: none;
  cursor: pointer;
  color: color-mix(in srgb, var(--brand-text) 50%, transparent);
  font-family: var(--font-body);
  padding: calc(var(--space-unit) * 2) 0;
  transition:
    color var(--duration-fast) var(--easing),
    background-color var(--duration-fast) var(--easing);
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

/* ── Animation ────────────────────────────────────────────────────── */
@keyframes blink {
  0%, 100% { opacity: 1;   }
  50%       { opacity: 0.3; }
}

/* ── Reduced motion — FINAL CSS rule ──────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
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

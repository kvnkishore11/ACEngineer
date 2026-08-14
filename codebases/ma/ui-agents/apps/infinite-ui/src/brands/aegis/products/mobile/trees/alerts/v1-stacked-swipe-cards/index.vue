<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'

// aegis/mobile/alerts/v1-stacked-swipe-cards
// Variant: Stacked alert cards with swipe hints + sticky filter bar
// CRITICAL: --space-unit = 0.375rem (mobile override, NOT 0.5rem)

// ── Types ──────────────────────────────────────────────────────────────
interface Alert {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  system: string
  ts: string
  desc: string
  status: 'active' | 'acknowledged' | 'escalated'
}

interface ResolvedAlert {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  resolvedBy: string
  ttResolve: string
  resolvedAt: string
}

interface NavTab {
  id: string
  label: string
  icon: string
}

// ── Active alerts ──────────────────────────────────────────────────────
const alerts = ref<Alert[]>([
  { id: 1, name: 'Prompt injection via system role override',    severity: 'CRITICAL', system: 'api-gateway-01',   ts: '2s ago',  desc: 'Detected malicious system prompt injection targeting GPT-4 endpoint.',         status: 'active'       },
  { id: 2, name: 'Data exfiltration from LLM worker',           severity: 'HIGH',     system: 'llm-worker-07',   ts: '14s ago', desc: 'Unusual outbound data volume detected from inference worker.',                 status: 'active'       },
  { id: 3, name: 'Token privilege escalation detected',         severity: 'CRITICAL', system: 'orchestrator-02', ts: '41s ago', desc: 'Agent token used to access out-of-scope resource endpoint.',                  status: 'active'       },
  { id: 4, name: 'Model poisoning signal in fine-tune cluster', severity: 'CRITICAL', system: 'fine-tune-03',    ts: '1m ago',  desc: 'Adversarial data pattern detected in training batch upload.',                 status: 'acknowledged' },
  { id: 5, name: 'Unusual API call pattern detected',           severity: 'MEDIUM',   system: 'api-gateway-02',  ts: '2m ago',  desc: 'Request frequency anomaly deviating from established baseline.',              status: 'active'       },
  { id: 6, name: 'Rate limiter bypass attempt',                 severity: 'HIGH',     system: 'rate-limiter-01', ts: '3m ago',  desc: 'Coordinated request fragmentation evading per-IP rate limits.',               status: 'escalated'    },
  { id: 7, name: 'Context window overflow probe',               severity: 'MEDIUM',   system: 'llm-worker-02',   ts: '5m ago',  desc: 'Repeated maximum-length prompts probing context boundary behavior.',           status: 'active'       },
])

// ── Resolved alerts ────────────────────────────────────────────────────
const resolvedAlerts: ResolvedAlert[] = [
  { id: 101, name: 'Jailbreak attempt via roleplay prompt',    severity: 'CRITICAL', resolvedBy: 'Responder', ttResolve: '1m 47s', resolvedAt: '8m ago'  },
  { id: 102, name: 'Memory store enumeration probe',           severity: 'HIGH',     resolvedBy: 'Scanner',   ttResolve: '4m 12s', resolvedAt: '15m ago' },
  { id: 103, name: 'Embedding query side-channel attempt',     severity: 'HIGH',     resolvedBy: 'Monitor',   ttResolve: '2m 33s', resolvedAt: '22m ago' },
  { id: 104, name: 'Repeated auth failure — API key rotation', severity: 'MEDIUM',   resolvedBy: 'Sentinel',  ttResolve: '8m 05s', resolvedAt: '31m ago' },
]

// ── Filter state ───────────────────────────────────────────────────────
const activeFilter = ref('all')

const criticalCount = computed(() => alerts.value.filter(a => a.severity === 'CRITICAL').length)
const highCount     = computed(() => alerts.value.filter(a => a.severity === 'HIGH').length)
const mediumCount   = computed(() => alerts.value.filter(a => a.severity === 'MEDIUM').length)

const filters = computed(() => [
  { id: 'all',      label: 'All',      count: alerts.value.length },
  { id: 'critical', label: 'Critical', count: criticalCount.value },
  { id: 'high',     label: 'High',     count: highCount.value     },
  { id: 'medium',   label: 'Medium',   count: mediumCount.value   },
])

const filteredAlerts = computed(() =>
  activeFilter.value === 'all'
    ? alerts.value
    : alerts.value.filter(a => a.severity.toLowerCase() === activeFilter.value)
)

// ── Three-tier count color ─────────────────────────────────────────────
const alertCountColor = computed(() => {
  if (alerts.value.some(a => a.severity === 'CRITICAL')) return 'error'
  if (alerts.value.some(a => a.severity === 'HIGH'))     return 'accent'
  return 'primary'
})

// ── Navigation ─────────────────────────────────────────────────────────
const navTabs: NavTab[] = [
  { id: 'dashboard', label: 'Dashboard', icon: '⬡' },
  { id: 'alerts',    label: 'Alerts',    icon: '◉' },
  { id: 'agents',    label: 'Agents',    icon: '◈' },
  { id: 'settings',  label: 'Settings',  icon: '◇' },
]
const activeTab = ref('alerts') // Alerts is active on this page

// ── Alert actions ──────────────────────────────────────────────────────
function acknowledgeAlert(id: number) {
  const alert = alerts.value.find(a => a.id === id)
  if (alert) alert.status = 'acknowledged'
}

function escalateAlert(id: number) {
  const alert = alerts.value.find(a => a.id === id)
  if (alert) alert.status = 'escalated'
}

// ── Mount ──────────────────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  nextTick(() => { isMounted.value = true })
})
</script>

<template>
  <div class="page" :class="{ 'is-mounted': isMounted }">
    <h1 class="sr-only">Aegis Mobile Alerts</h1>

    <!-- ── Sticky page header ─────────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Alerts page header">
      <div class="page-header__inner">
        <span class="page-header__back" aria-hidden="true">←</span>
        <span class="page-header__brand">AEGIS ALERTS</span>
        <span class="page-header__live" aria-hidden="true">● LIVE</span>
      </div>
    </header>

    <!-- ── Scrollable content ─────────────────────────────────────── -->
    <div class="page__content">

      <!-- Alert count bar -->
      <div
        class="alert-count-bar"
        role="status"
        :aria-label="`${alerts.length} active alerts`"
      >
        <span
          class="alert-count__num"
          :class="`alert-count__num--${alertCountColor}`"
        >{{ alerts.length }}</span>
        <span class="alert-count__label">Active Alerts</span>
      </div>

      <!-- ── Section 1: Severity filter bar (sticky) ───────────────── -->
      <div
        class="filter-section"
        role="group"
        aria-label="Filter alerts by severity"
      >
        <div class="filter-bar">
          <button
            v-for="f in filters"
            :key="f.id"
            type="button"
            class="filter-pill"
            :class="[`filter-pill--${f.id}`, { 'filter-pill--active': activeFilter === f.id }]"
            :aria-pressed="activeFilter === f.id"
            @click="activeFilter = f.id"
          >
            {{ f.label }}
            <span class="filter-pill__badge" aria-hidden="true">{{ f.count }}</span>
          </button>
        </div>
      </div>

      <!-- ── Section 2: Active alert cards ─────────────────────────── -->
      <section class="cards-section" aria-labelledby="active-alerts-heading">
        <h2 id="active-alerts-heading" class="sr-only">Active Alerts</h2>
        <div
          class="alert-list"
          role="list"
          :aria-label="`${filteredAlerts.length} active alerts displayed`"
        >
          <div
            v-for="alert in filteredAlerts"
            :key="alert.id"
            class="alert-card-wrap"
            role="listitem"
          >
            <!-- Swipe affordance strips — decorative only, aria-hidden -->
            <div class="swipe-hint swipe-hint--left" aria-hidden="true">
              <span class="swipe-hint__icon">✓</span>
              <span class="swipe-hint__label">Ack</span>
            </div>
            <div class="swipe-hint swipe-hint--right" aria-hidden="true">
              <span class="swipe-hint__icon">↑</span>
              <span class="swipe-hint__label">Esc</span>
            </div>

            <!-- The actual alert card -->
            <article
              class="alert-card"
              :class="[`alert-card--${alert.severity.toLowerCase()}`, `alert-card--${alert.status}`]"
              :aria-label="`${alert.severity} alert: ${alert.name}, ${alert.system}, ${alert.ts}`"
            >
              <div class="alert-card__header">
                <span
                  class="sev-pill"
                  :class="`sev-pill--${alert.severity.toLowerCase()}`"
                >{{ alert.severity }}</span>
                <span class="alert-card__ts">{{ alert.ts }}</span>
              </div>
              <p class="alert-card__name">{{ alert.name }}</p>
              <p class="alert-card__system">{{ alert.system }}</p>
              <p class="alert-card__desc">{{ alert.desc }}</p>
              <div class="alert-card__actions">
                <button
                  type="button"
                  class="action-btn action-btn--ack"
                  :aria-label="`Acknowledge alert: ${alert.name}`"
                  @click="acknowledgeAlert(alert.id)"
                >✓ Acknowledge</button>
                <button
                  type="button"
                  class="action-btn action-btn--esc"
                  :aria-label="`Escalate alert: ${alert.name}`"
                  @click="escalateAlert(alert.id)"
                >↑ Escalate</button>
              </div>
            </article>
          </div>

          <!-- Empty state when filter has no results -->
          <div
            v-if="filteredAlerts.length === 0"
            class="empty-state"
            role="status"
          >
            <span class="empty-state__icon" aria-hidden="true">◉</span>
            <p class="empty-state__text">No {{ activeFilter }} alerts</p>
          </div>
        </div>
      </section>

      <!-- ── Section 3: Alert history (resolved) ───────────────────── -->
      <section class="history-section" aria-labelledby="history-heading">
        <div class="history-header">
          <h2 id="history-heading" class="section-title">Alert History</h2>
          <span class="history-count">{{ resolvedAlerts.length }} resolved</span>
        </div>
        <ol class="history-timeline" role="list">
          <li
            v-for="ra in resolvedAlerts"
            :key="ra.id"
            class="history-entry"
            role="listitem"
            :aria-label="`Resolved: ${ra.name}, resolved by ${ra.resolvedBy} in ${ra.ttResolve}`"
          >
            <div class="history-entry__track" aria-hidden="true">
              <span class="history-dot"></span>
            </div>
            <div class="history-entry__body">
              <p class="history-entry__name">{{ ra.name }}</p>
              <p class="history-entry__meta">
                <span class="history-entry__agent">{{ ra.resolvedBy }}</span>
                <span class="history-entry__sep" aria-hidden="true"> · </span>
                <span class="history-entry__ttr">{{ ra.ttResolve }}</span>
                <span class="history-entry__sep" aria-hidden="true"> · </span>
                <span class="history-entry__time">{{ ra.resolvedAt }}</span>
              </p>
            </div>
          </li>
        </ol>
      </section>

    </div><!-- /page__content -->

    <!-- ── Section 4: Fixed Bottom Nav ──────────────────────────────── -->
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

/* ── Scrollable content ─────────────────────────────────────────────── */
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

/* ── Page header (sticky) ───────────────────────────────────────────── */
.page-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: linear-gradient(180deg, var(--brand-bg-secondary), color-mix(in srgb, var(--brand-bg-secondary) 85%, var(--brand-bg)));
  border-bottom: 1px solid var(--brand-border);
}

.page-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 4);
}

.page-header__back {
  font-family: var(--font-body);
  font-size: 1.125rem;
  color: color-mix(in srgb, var(--brand-text) 60%, transparent);
}

.page-header__brand {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--brand-primary);
}

.page-header__live {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--brand-error);
}

/* ── Alert count bar ────────────────────────────────────────────────── */
.alert-count-bar {
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 4) calc(var(--space-unit) * 2);
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 2);
}

.alert-count__num {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

/* Three-tier token logic */
.alert-count__num--error   { color: var(--brand-error);   }
.alert-count__num--accent  { color: var(--brand-accent);  }
.alert-count__num--primary { color: var(--brand-primary); }

.alert-count__label {
  font-family: var(--font-heading);
  font-size: 1.0625rem;
  font-weight: 700;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

/* ── Filter section (sticky below header) ───────────────────────────── */
.filter-section {
  position: sticky;
  top: calc(var(--space-unit) * 14);
  z-index: 20;
  background: linear-gradient(180deg, var(--brand-bg), color-mix(in srgb, var(--brand-bg) 90%, var(--brand-bg-secondary)));
  border-bottom: 1px solid var(--brand-border);
}

/* Filter bar — horizontal scroll allowed, never hidden */
.filter-bar {
  display: flex;
  gap: calc(var(--space-unit) * 2);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
}

.filter-bar::-webkit-scrollbar {
  display: none;
}

/* Filter pills */
.filter-pill {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  border-radius: var(--radius-md);
  border: none;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  cursor: pointer;
  min-height: calc(var(--space-unit) * 8);
  transition:
    background-color var(--duration-fast) var(--easing),
    color var(--duration-fast) var(--easing);
}

.filter-pill:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* Inactive filter pill states */
.filter-pill--all      { background-color: var(--brand-surface); color: var(--brand-text); }
.filter-pill--critical { background-color: color-mix(in srgb, var(--brand-error)     20%, transparent); color: var(--brand-text); }
.filter-pill--high     { background-color: color-mix(in srgb, var(--brand-accent)    20%, transparent); color: var(--brand-text); }
.filter-pill--medium   { background-color: color-mix(in srgb, var(--brand-secondary) 20%, transparent); color: var(--brand-text); }

/* Active filter pill states */
.filter-pill--active.filter-pill--all      { background-color: var(--brand-primary); color: var(--brand-bg); }
.filter-pill--active.filter-pill--critical { background-color: var(--brand-error);   color: var(--brand-bg); }
.filter-pill--active.filter-pill--high     { background-color: var(--brand-accent);  color: var(--brand-bg); }
.filter-pill--active.filter-pill--medium   { background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent); color: var(--brand-text); }

/* Count badge on pill */
.filter-pill__badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  background-color: color-mix(in srgb, var(--brand-bg) 30%, transparent);
  padding: 0 calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  min-width: calc(var(--space-unit) * 5);
  text-align: center;
  line-height: 1.6;
}

/* ── Cards section ──────────────────────────────────────────────────── */
.cards-section {
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

/* Card wrapper clips the swipe hints behind */
.alert-card-wrap {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

/* Swipe hint strips — decorative, pointer-events: none, aria-hidden */
.swipe-hint {
  position: absolute;
  top: 0;
  bottom: 0;
  width: calc(var(--space-unit) * 16);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 1);
  pointer-events: none;
  z-index: 0;
}

.swipe-hint--left {
  left: 0;
  background-color: color-mix(in srgb, var(--brand-primary) 20%, transparent);
}

.swipe-hint--right {
  right: 0;
  background-color: color-mix(in srgb, var(--brand-error) 20%, transparent);
}

.swipe-hint__icon {
  font-size: 1.25rem;
}

.swipe-hint__label {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.swipe-hint--left .swipe-hint__icon,
.swipe-hint--left .swipe-hint__label  { color: var(--brand-primary); }
.swipe-hint--right .swipe-hint__icon,
.swipe-hint--right .swipe-hint__label { color: var(--brand-error);   }

/* Alert card — sits on top of swipe hints (z-index: 1) */
.alert-card {
  background-color: var(--brand-surface);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 4);
  position: relative;
  z-index: 1;
  border-left: 3px solid transparent;
  box-shadow: var(--shadow-md);
}

/* Unresolved = crimson left border for all active severities */
.alert-card--critical,
.alert-card--high,
.alert-card--medium {
  border-left-color: var(--brand-accent);
}

/* Status modifier: acknowledged / escalated — dimmed name */
.alert-card--acknowledged .alert-card__name,
.alert-card--escalated    .alert-card__name {
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

.alert-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: calc(var(--space-unit) * 2);
}

.alert-card__ts {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
}

.alert-card__name {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 700;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 1);
  line-height: 1.3;
}

.alert-card__system {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  margin: 0 0 calc(var(--space-unit) * 2);
}

.alert-card__desc {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  line-height: 1.4;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  margin: 0 0 calc(var(--space-unit) * 3);
}

/* Action buttons row */
.alert-card__actions {
  display: flex;
  gap: calc(var(--space-unit) * 2);
}

.action-btn {
  flex: 1;
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  border-radius: var(--radius-sm);
  border: none;
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  cursor: pointer;
  min-height: calc(var(--space-unit) * 8);
  transition: background-color var(--duration-fast) var(--easing);
}

.action-btn:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.action-btn--ack {
  background-color: color-mix(in srgb, var(--brand-primary) 15%, transparent);
  color: var(--brand-primary);
}

.action-btn--ack:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 25%, transparent);
}

.action-btn--esc {
  background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);
  color: var(--brand-error);
}

.action-btn--esc:hover {
  background-color: color-mix(in srgb, var(--brand-error) 25%, transparent);
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

/* ── Empty state ────────────────────────────────────────────────────── */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 10) calc(var(--space-unit) * 4);
  text-align: center;
}

.empty-state__icon {
  font-size: 2rem;
  color: var(--brand-primary);
  opacity: 0.4;
}

.empty-state__text {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  margin: 0;
}

/* ── Alert history ──────────────────────────────────────────────────── */
.history-section {
  padding: calc(var(--space-unit) * 4);
  border-top: 1px solid var(--brand-border);
  background: linear-gradient(180deg, color-mix(in srgb, var(--brand-bg) 90%, var(--brand-bg-secondary)), var(--brand-bg));
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: calc(var(--space-unit) * 3);
}

.section-title {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  margin: 0;
}

.history-count {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-primary);
}

.history-timeline {
  list-style: none;
  padding: 0;
  margin: 0;
}

.history-entry {
  display: flex;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 2.5) 0;
  position: relative;
}

/* Vertical connector track */
.history-entry__track {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  padding-top: calc(var(--space-unit) * 0.5);
}

.history-entry__track::after {
  content: '';
  flex: 1;
  width: 1px;
  background-color: var(--brand-border);
  margin-top: calc(var(--space-unit) * 1);
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

.history-entry__name {
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  margin: 0 0 calc(var(--space-unit) * 1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-entry__meta {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  margin: 0;
}

.history-entry__agent {
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

/* ── Bottom nav ─────────────────────────────────────────────────────── */
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

/* ── Reduced motion (LAST RULE) ─────────────────────────────────────── */
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

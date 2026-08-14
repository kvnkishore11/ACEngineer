<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/mobile/alerts/v2-severity-accordions
// Layout: page header → 4 collapsible accordion groups (Critical/High/Medium/Resolved)
// CRITICAL: --space-unit = 0.375rem on mobile (not 0.5rem)
// CRITICAL: accordion header bg MUST be var(--brand-bg) not var(--brand-bg-secondary)
//           --brand-accent on --brand-bg-secondary = 4.47:1 (FAIL AA)
//           --brand-accent on --brand-bg           = 4.74:1 (PASS AA)

// ── Types ────────────────────────────────────────────────────────
interface Alert {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  system: string
  ts: string
  desc: string
  status: 'active' | 'acknowledged' | 'resolved'
}

interface ResolvedAlert {
  id: number
  name: string
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM'
  resolvedBy: string
  ttResolve: string
  resolvedAt: string
}

// ── Data ─────────────────────────────────────────────────────────
const alerts = ref<Alert[]>([
  { id: 1, name: 'Prompt injection via system prompt',    severity: 'CRITICAL', system: 'api-gateway-01',   ts: '2s ago',  desc: 'Adversarial payload in system prompt field bypasses guardrails.',         status: 'active'       },
  { id: 2, name: 'Agent token privilege escalation',      severity: 'CRITICAL', system: 'orchestrator-02', ts: '34s ago', desc: 'Token claims elevated agent tier without authorization.',               status: 'active'       },
  { id: 3, name: 'Context window injection attempt',      severity: 'CRITICAL', system: 'llm-worker-04',   ts: '1m ago',  desc: 'Crafted input designed to overflow and corrupt model context.',        status: 'acknowledged' },
  { id: 4, name: 'Data exfiltration via embedding query', severity: 'HIGH',     system: 'llm-worker-07',   ts: '14s ago', desc: 'Repeated similarity searches retrieving sensitive training data.',     status: 'active'       },
  { id: 5, name: 'Model poisoning probe — fine-tune',     severity: 'HIGH',     system: 'fine-tune-03',    ts: '3m ago',  desc: 'Suspicious fine-tune job submitted with adversarial training pairs.',  status: 'active'       },
  { id: 6, name: 'Rate limit bypass via fragmentation',   severity: 'MEDIUM',   system: 'rate-limiter-01', ts: '2m ago',  desc: 'Request fragmentation evading per-user rate limit enforcement.',       status: 'active'       },
  { id: 7, name: 'Anomalous API call pattern',            severity: 'MEDIUM',   system: 'api-gateway-02',  ts: '4m ago',  desc: 'Statistically anomalous API call sequence from consumer token 7f3a.', status: 'active'       },
])

const resolvedAlerts: ResolvedAlert[] = [
  { id: 101, name: 'Jailbreak attempt — system prompt',   severity: 'CRITICAL', resolvedBy: 'Responder', ttResolve: '2m 14s', resolvedAt: '8m ago'  },
  { id: 102, name: 'Repeated auth failure — brute force', severity: 'HIGH',     resolvedBy: 'Monitor',   ttResolve: '0m 47s', resolvedAt: '12m ago' },
  { id: 103, name: 'Unvalidated tool invocation',         severity: 'MEDIUM',   resolvedBy: 'Scanner',   ttResolve: '4m 31s', resolvedAt: '18m ago' },
  { id: 104, name: 'Memory store enumeration probe',      severity: 'HIGH',     resolvedBy: 'Scanner',   ttResolve: '1m 22s', resolvedAt: '25m ago' },
]

// ── Computed groupings ───────────────────────────────────────────
const criticalAlerts = computed(() => alerts.value.filter(a => a.severity === 'CRITICAL'))
const highAlerts     = computed(() => alerts.value.filter(a => a.severity === 'HIGH'))
const mediumAlerts   = computed(() => alerts.value.filter(a => a.severity === 'MEDIUM'))
const activeCount    = computed(() => alerts.value.filter(a => a.status !== 'resolved').length)

const alertCountColorClass = computed(() => {
  if (alerts.value.some(a => a.severity === 'CRITICAL')) return 'count--error'
  if (alerts.value.some(a => a.severity === 'HIGH'))     return 'count--accent'
  return 'count--primary'
})

// ── Accordion state ──────────────────────────────────────────────
const openSections = reactive<Record<string, boolean>>({
  critical: false,
  high:     false,
  medium:   false,
  resolved: false,
})

function toggleSection(id: string) {
  openSections[id] = !openSections[id]
}

// ── Bottom nav ───────────────────────────────────────────────────
const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: '⬡' },
  { id: 'alerts',    label: 'Alerts',    icon: '◈' },
  { id: 'agents',    label: 'Agents',    icon: '◉' },
  { id: 'settings',  label: 'Settings',  icon: '◇' },
]
const activeTab = ref('alerts')

// ── Mount ────────────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  nextTick(() => { isMounted.value = true })
  // Open highest-severity section that has alerts by default
  if (criticalAlerts.value.length > 0)      openSections.critical = true
  else if (highAlerts.value.length > 0)     openSections.high     = true
  else if (mediumAlerts.value.length > 0)   openSections.medium   = true
})

onUnmounted(() => {
  // No intervals used — defensive hook present
})
</script>

<template>
  <div class="page" :class="{ 'is-mounted': isMounted }">
    <h1 class="sr-only">Aegis Mobile Alerts</h1>

    <!-- ── Page header ─────────────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Alerts page header">
      <div class="page-header__inner">
        <div class="header-brand">
          <span class="brand-word">AEGIS</span>
          <span class="brand-sep" aria-hidden="true">/</span>
          <span class="brand-sub">Alerts</span>
        </div>
        <div class="header-count" :aria-label="`${activeCount} active alerts`">
          <span class="count-num" :class="alertCountColorClass">{{ activeCount }}</span>
          <span class="count-label">Active</span>
        </div>
      </div>
    </header>

    <!-- ── Main content ────────────────────────────────────────── -->
    <main class="page__content">

      <!-- ── CRITICAL accordion ─────────────────────────────────── -->
      <section class="accord-group" aria-labelledby="toggle-critical">
        <button
          type="button"
          class="accord-toggle accord-toggle--critical"
          id="toggle-critical"
          :aria-expanded="openSections.critical"
          aria-controls="panel-critical"
          @click="toggleSection('critical')"
        >
          <div class="accord-toggle__left">
            <span class="accord-dot accord-dot--critical" aria-hidden="true"></span>
            <span class="accord-toggle__label">Critical</span>
            <span
              class="accord-toggle__count"
              :aria-label="`${criticalAlerts.length} critical alerts`"
            >{{ criticalAlerts.length }}</span>
          </div>
          <span
            class="accord-chevron"
            :class="{ 'accord-chevron--open': openSections.critical }"
            aria-hidden="true"
          >›</span>
        </button>

        <div
          class="accord-panel"
          id="panel-critical"
          role="region"
          aria-labelledby="toggle-critical"
          :class="{ 'accord-panel--open': openSections.critical }"
        >
          <div class="accord-panel__inner">
            <article
              v-for="alert in criticalAlerts"
              :key="alert.id"
              class="alert-card"
              :class="alert.status === 'resolved' ? 'alert-card--resolved' : 'alert-card--unresolved'"
              :aria-label="`${alert.severity} alert: ${alert.name}, ${alert.system}`"
            >
              <div class="alert-card__header">
                <span class="sev-pill" :class="`sev-pill--${alert.severity.toLowerCase()}`">
                  {{ alert.severity }}
                </span>
                <span class="alert-card__ts">{{ alert.ts }}</span>
              </div>
              <h3 class="alert-card__name"
                  :class="{ 'alert-card__name--resolved': alert.status === 'resolved' }">
                {{ alert.name }}
              </h3>
              <p class="alert-card__system">{{ alert.system }}</p>
              <p class="alert-card__desc"
                 :class="{ 'alert-card__desc--resolved': alert.status === 'resolved' }">
                {{ alert.desc }}
              </p>
              <div class="alert-card__actions">
                <button
                  type="button"
                  class="action-btn action-btn--ack"
                  :aria-label="`Acknowledge: ${alert.name}`"
                >✓ Acknowledge</button>
                <button
                  type="button"
                  class="action-btn action-btn--esc"
                  :aria-label="`Escalate: ${alert.name}`"
                >↑ Escalate</button>
              </div>
            </article>
            <p v-if="criticalAlerts.length === 0" class="accord-empty">No critical alerts.</p>
          </div>
        </div>
      </section>

      <!-- ── HIGH accordion ──────────────────────────────────────── -->
      <section class="accord-group" aria-labelledby="toggle-high">
        <button
          type="button"
          class="accord-toggle accord-toggle--high"
          id="toggle-high"
          :aria-expanded="openSections.high"
          aria-controls="panel-high"
          @click="toggleSection('high')"
        >
          <div class="accord-toggle__left">
            <span class="accord-dot accord-dot--high" aria-hidden="true"></span>
            <span class="accord-toggle__label">High</span>
            <span
              class="accord-toggle__count"
              :aria-label="`${highAlerts.length} high severity alerts`"
            >{{ highAlerts.length }}</span>
          </div>
          <span
            class="accord-chevron"
            :class="{ 'accord-chevron--open': openSections.high }"
            aria-hidden="true"
          >›</span>
        </button>

        <div
          class="accord-panel"
          id="panel-high"
          role="region"
          aria-labelledby="toggle-high"
          :class="{ 'accord-panel--open': openSections.high }"
        >
          <div class="accord-panel__inner">
            <article
              v-for="alert in highAlerts"
              :key="alert.id"
              class="alert-card"
              :class="alert.status === 'resolved' ? 'alert-card--resolved' : 'alert-card--unresolved'"
              :aria-label="`${alert.severity} alert: ${alert.name}, ${alert.system}`"
            >
              <div class="alert-card__header">
                <span class="sev-pill" :class="`sev-pill--${alert.severity.toLowerCase()}`">
                  {{ alert.severity }}
                </span>
                <span class="alert-card__ts">{{ alert.ts }}</span>
              </div>
              <h3 class="alert-card__name"
                  :class="{ 'alert-card__name--resolved': alert.status === 'resolved' }">
                {{ alert.name }}
              </h3>
              <p class="alert-card__system">{{ alert.system }}</p>
              <p class="alert-card__desc"
                 :class="{ 'alert-card__desc--resolved': alert.status === 'resolved' }">
                {{ alert.desc }}
              </p>
              <div class="alert-card__actions">
                <button
                  type="button"
                  class="action-btn action-btn--ack"
                  :aria-label="`Acknowledge: ${alert.name}`"
                >✓ Acknowledge</button>
                <button
                  type="button"
                  class="action-btn action-btn--esc"
                  :aria-label="`Escalate: ${alert.name}`"
                >↑ Escalate</button>
              </div>
            </article>
            <p v-if="highAlerts.length === 0" class="accord-empty">No high severity alerts.</p>
          </div>
        </div>
      </section>

      <!-- ── MEDIUM accordion ─────────────────────────────────────── -->
      <section class="accord-group" aria-labelledby="toggle-medium">
        <button
          type="button"
          class="accord-toggle accord-toggle--medium"
          id="toggle-medium"
          :aria-expanded="openSections.medium"
          aria-controls="panel-medium"
          @click="toggleSection('medium')"
        >
          <div class="accord-toggle__left">
            <span class="accord-dot accord-dot--medium" aria-hidden="true"></span>
            <span class="accord-toggle__label">Medium</span>
            <span
              class="accord-toggle__count"
              :aria-label="`${mediumAlerts.length} medium severity alerts`"
            >{{ mediumAlerts.length }}</span>
          </div>
          <span
            class="accord-chevron"
            :class="{ 'accord-chevron--open': openSections.medium }"
            aria-hidden="true"
          >›</span>
        </button>

        <div
          class="accord-panel"
          id="panel-medium"
          role="region"
          aria-labelledby="toggle-medium"
          :class="{ 'accord-panel--open': openSections.medium }"
        >
          <div class="accord-panel__inner">
            <article
              v-for="alert in mediumAlerts"
              :key="alert.id"
              class="alert-card"
              :class="alert.status === 'resolved' ? 'alert-card--resolved' : 'alert-card--unresolved'"
              :aria-label="`${alert.severity} alert: ${alert.name}, ${alert.system}`"
            >
              <div class="alert-card__header">
                <span class="sev-pill" :class="`sev-pill--${alert.severity.toLowerCase()}`">
                  {{ alert.severity }}
                </span>
                <span class="alert-card__ts">{{ alert.ts }}</span>
              </div>
              <h3 class="alert-card__name"
                  :class="{ 'alert-card__name--resolved': alert.status === 'resolved' }">
                {{ alert.name }}
              </h3>
              <p class="alert-card__system">{{ alert.system }}</p>
              <p class="alert-card__desc"
                 :class="{ 'alert-card__desc--resolved': alert.status === 'resolved' }">
                {{ alert.desc }}
              </p>
              <div class="alert-card__actions">
                <button
                  type="button"
                  class="action-btn action-btn--ack"
                  :aria-label="`Acknowledge: ${alert.name}`"
                >✓ Acknowledge</button>
                <button
                  type="button"
                  class="action-btn action-btn--esc"
                  :aria-label="`Escalate: ${alert.name}`"
                >↑ Escalate</button>
              </div>
            </article>
            <p v-if="mediumAlerts.length === 0" class="accord-empty">No medium severity alerts.</p>
          </div>
        </div>
      </section>

      <!-- ── RESOLVED accordion (alert history) ──────────────────── -->
      <section class="accord-group accord-group--resolved" aria-labelledby="toggle-resolved">
        <button
          type="button"
          class="accord-toggle accord-toggle--resolved"
          id="toggle-resolved"
          :aria-expanded="openSections.resolved"
          aria-controls="panel-resolved"
          @click="toggleSection('resolved')"
        >
          <div class="accord-toggle__left">
            <span class="accord-dot accord-dot--resolved" aria-hidden="true"></span>
            <span class="accord-toggle__label">Resolved</span>
            <span
              class="accord-toggle__count"
              :aria-label="`${resolvedAlerts.length} resolved alerts`"
            >{{ resolvedAlerts.length }}</span>
          </div>
          <span
            class="accord-chevron"
            :class="{ 'accord-chevron--open': openSections.resolved }"
            aria-hidden="true"
          >›</span>
        </button>

        <div
          class="accord-panel"
          id="panel-resolved"
          role="region"
          aria-labelledby="toggle-resolved"
          :class="{ 'accord-panel--open': openSections.resolved }"
        >
          <div class="accord-panel__inner">
            <ol class="history-list" role="list" aria-label="Resolved alert history">
              <li
                v-for="r in resolvedAlerts"
                :key="r.id"
                class="history-entry"
                :aria-label="`Resolved: ${r.name}, by ${r.resolvedBy} in ${r.ttResolve}`"
              >
                <div class="history-entry__track" aria-hidden="true">
                  <span class="history-dot"></span>
                  <span class="history-connector"></span>
                </div>
                <div class="history-entry__body">
                  <p class="history-entry__name">{{ r.name }}</p>
                  <p class="history-entry__meta">
                    <span class="history-entry__agent">{{ r.resolvedBy }}</span>
                    <span aria-hidden="true"> · </span>
                    <span class="history-entry__ttr">{{ r.ttResolve }}</span>
                    <span aria-hidden="true"> · </span>
                    <span class="history-entry__when">{{ r.resolvedAt }}</span>
                  </p>
                </div>
              </li>
            </ol>
          </div>
        </div>
      </section>

    </main><!-- /page__content -->

    <!-- ── Fixed bottom nav ──────────────────────────────────────── -->
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

/* ── Page content — clears fixed bottom nav ───────────────────── */
.page__content {
  padding-bottom: calc(
    calc(var(--space-unit) * 12)
    + env(safe-area-inset-bottom)
    + calc(var(--space-unit) * 4)
  );
}

/* ── Page header ──────────────────────────────────────────────── */
.page-header {
  background-color: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
  position: sticky;
  top: 0;
  z-index: 50;
}

.page-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: calc(var(--space-unit) * 4);
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

.header-count {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 1);
}

.count-num {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.count--error   { color: var(--brand-error);   }
.count--accent  { color: var(--brand-accent);  }
.count--primary { color: var(--brand-primary); }

.count-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── Accordion group container ────────────────────────────────── */
.accord-group {
  border-bottom: 1px solid var(--brand-border);
}

.accord-group--resolved {
  /* slight visual separation for resolved section */
}

/* ── Accordion toggle ─────────────────────────────────────────── */
/* CRITICAL: background MUST be var(--brand-bg), NOT var(--brand-bg-secondary)
   --brand-accent on --brand-bg-secondary = 4.47:1 (FAILS AA)
   --brand-accent on --brand-bg           = 4.74:1 (PASSES AA) */
.accord-toggle {
  width: 100%;
  min-height: calc(var(--space-unit) * 12);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 calc(var(--space-unit) * 4);
  background: linear-gradient(to right, var(--brand-bg), color-mix(in srgb, var(--brand-bg) 90%, var(--brand-surface)));
  border: none;
  border-bottom: 1px solid var(--brand-border);
  cursor: pointer;
  transition: background-color var(--duration-fast) var(--easing);
  -webkit-tap-highlight-color: transparent;
}

.accord-toggle:hover {
  background-color: color-mix(in srgb, var(--brand-bg) 85%, var(--brand-surface));
}

.accord-toggle:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

/* Severity-specific label colors — all verified at 4.74:1+ on var(--brand-bg) */
.accord-toggle--critical .accord-toggle__label { color: var(--brand-error);     } /* 5.03:1 ✅ */
.accord-toggle--high     .accord-toggle__label { color: var(--brand-accent);    } /* 4.74:1 ✅ */
.accord-toggle--medium   .accord-toggle__label { color: var(--brand-secondary); } /* 5.45:1 ✅ */
.accord-toggle--resolved .accord-toggle__label { color: var(--brand-primary);   } /* 17.39:1 ✅ */

.accord-toggle__left {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2.5);
}

/* Severity dots */
.accord-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
}

.accord-dot--critical { background-color: var(--brand-error);     }
.accord-dot--high     { background-color: var(--brand-accent);    }
.accord-dot--medium   { background-color: var(--brand-secondary); }
.accord-dot--resolved { background-color: var(--brand-primary);   }

.accord-toggle__label {
  font-family: var(--font-heading);
  font-size: 1.0625rem;
  font-weight: 700;
  /* color set by severity modifier class above */
}

/* Count badge */
.accord-toggle__count {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  padding: calc(var(--space-unit) * 0.5) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  background-color: color-mix(in srgb, var(--brand-surface) 60%, transparent);
  color: var(--brand-text);
  min-width: calc(var(--space-unit) * 5);
  text-align: center;
}

/* Chevron */
.accord-chevron {
  font-size: 1.125rem;
  color: var(--brand-muted);
  transition: transform var(--duration-normal) var(--easing);
  display: inline-block;
  flex-shrink: 0;
}

.accord-chevron--open {
  transform: rotate(90deg);
}

/* ── Accordion panel ──────────────────────────────────────────── */
.accord-panel {
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--duration-slow) var(--easing);
  background-color: var(--brand-bg-secondary);
}

.accord-panel--open {
  max-height: 9999px;
}

.accord-panel__inner {
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.accord-empty {
  font-size: 0.875rem;
  color: var(--brand-muted);
  text-align: center;
  padding: calc(var(--space-unit) * 4) 0;
  margin: 0;
}

/* ── Alert card ───────────────────────────────────────────────── */
.alert-card {
  background-color: var(--brand-surface);
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 4);
  border-left: 3px solid transparent;
  box-shadow: var(--shadow-sm);
}

.alert-card--unresolved { border-left-color: var(--brand-accent);  }
.alert-card--resolved   { border-left-color: var(--brand-primary); }

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
  font-family: var(--font-heading);
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 1) 0;
  line-height: 1.4;
  transition: color var(--duration-normal) var(--easing);
}

.alert-card__name--resolved {
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
}

.alert-card__system {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  margin: 0 0 calc(var(--space-unit) * 2) 0;
}

.alert-card__desc {
  font-size: 0.875rem;
  line-height: 1.5;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  margin: 0 0 calc(var(--space-unit) * 3) 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color var(--duration-normal) var(--easing);
}

.alert-card__desc--resolved {
  color: color-mix(in srgb, var(--brand-text) 55%, transparent);
}

/* Action buttons */
.alert-card__actions {
  display: flex;
  gap: calc(var(--space-unit) * 2);
}

.action-btn {
  flex: 1;
  min-height: calc(var(--space-unit) * 8);
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background-color var(--duration-fast) var(--easing);
  -webkit-tap-highlight-color: transparent;
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

/* ── Severity pills ───────────────────────────────────────────── */
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

.sev-pill--critical { background-color: var(--brand-error);  color: var(--brand-bg); } /* 5.33:1 ✅ */
.sev-pill--high     { background-color: var(--brand-accent); color: var(--brand-bg); } /* 4.74:1 ✅ */
.sev-pill--medium   {
  background-color: color-mix(in srgb, var(--brand-accent) 50%, transparent);
  color: var(--brand-text); /* 7.90:1 ✅ on this semi-transparent bg */
}

/* ── Alert history (resolved panel) ──────────────────────────── */
.history-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.history-entry {
  display: flex;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) 0;
  border-bottom: 1px solid var(--brand-border);
}

.history-entry:last-child {
  border-bottom: none;
}

.history-entry__track {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  padding-top: calc(var(--space-unit) * 0.5);
}

.history-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  background-color: var(--brand-primary);
  flex-shrink: 0;
}

.history-connector {
  flex: 1;
  width: 1px;
  background-color: var(--brand-border);
  margin-top: calc(var(--space-unit) * 1);
  min-height: calc(var(--space-unit) * 4);
}

.history-entry:last-child .history-connector {
  display: none;
}

.history-entry__body {
  flex: 1;
  min-width: 0;
}

.history-entry__name {
  font-size: 0.875rem;
  font-weight: 500;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  margin: 0 0 calc(var(--space-unit) * 1) 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-entry__meta {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  margin: 0;
}

.history-entry__agent {
  font-weight: 700;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
}

.history-entry__ttr {
  color: var(--brand-primary);
  font-weight: 700;
}

.history-entry__when {
  color: var(--brand-muted);
}

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

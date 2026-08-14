<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, useTemplateRef } from 'vue'

// ── Types ────────────────────────────────────────────────────────────────────

interface LogEntry {
  id: number
  time: string
  source: 'DEPLOY' | 'STAGING' | 'PROD' | 'CI/CD' | 'ERROR' | 'MIGRATION' | 'MONITOR'
  severity: 'INFO' | 'WARN' | 'ERROR'
  message: string
}

interface ChatMessage {
  id: number
  agent: keyof typeof agents
  time: string
  isAlert: boolean
  message: string
}

interface Agent {
  color: string
  icon: string
  status: 'online' | 'busy' | 'idle'
  label: string
}

// ── Agent definitions ────────────────────────────────────────────────────────

const agents: Record<string, Agent> = {
  Scanner:        { color: '#6e7fff', icon: '◎', status: 'online', label: 'Scanner'         },
  Monitor:        { color: '#2ED573', icon: '♡', status: 'online', label: 'Monitor'         },
  Responder:      { color: '#FF6B35', icon: '⬡', status: 'busy',   label: 'Responder'       },
  Sentinel:       { color: '#FF4757', icon: '△', status: 'busy',   label: 'Sentinel'        },
  PackageMonitor: { color: '#9B59B6', icon: '⬡', status: 'idle',   label: 'Package Monitor' },
  SQLSpecialist:  { color: '#3498DB', icon: '◈', status: 'online', label: 'SQL Specialist'  },
  DeployChecker:  { color: '#FFA502', icon: '⬆', status: 'idle',   label: 'Deploy Checker'  },
}

const agentList = Object.entries(agents).map(([key, val]) => ({ key, ...val }))

// ── Log data ─────────────────────────────────────────────────────────────────

const logEntries: LogEntry[] = [
  { id: 1,  time: '14:23:01', source: 'DEPLOY',    severity: 'INFO',  message: 'v2.4.1 deployed to staging cluster-02' },
  { id: 2,  time: '14:22:47', source: 'STAGING',   severity: 'WARN',  message: 'Memory usage at 78% on pod-api-03' },
  { id: 3,  time: '14:22:33', source: 'ERROR',     severity: 'ERROR', message: 'Database connection pool exhausted (retry 3/5)' },
  { id: 4,  time: '14:22:15', source: 'PROD',      severity: 'INFO',  message: 'Health check passed - all services nominal' },
  { id: 5,  time: '14:21:58', source: 'CI/CD',     severity: 'INFO',  message: 'Build #847 completed in 4m 32s' },
  { id: 6,  time: '14:21:44', source: 'MIGRATION', severity: 'INFO',  message: 'Schema migration v3.2.1 applied to users table' },
  { id: 7,  time: '14:21:30', source: 'DEPLOY',    severity: 'INFO',  message: 'Canary release: 10% traffic on v2.4.1' },
  { id: 8,  time: '14:21:12', source: 'ERROR',     severity: 'WARN',  message: 'Elevated latency on /api/v2/search endpoint' },
  { id: 9,  time: '14:20:55', source: 'MONITOR',   severity: 'INFO',  message: 'Auto-scaling triggered: +2 instances' },
  { id: 10, time: '14:20:41', source: 'STAGING',   severity: 'INFO',  message: 'Integration tests passing (142/142)' },
  { id: 11, time: '14:20:28', source: 'PROD',      severity: 'INFO',  message: 'Cache hit ratio: 94.2%' },
  { id: 12, time: '14:20:15', source: 'CI/CD',     severity: 'WARN',  message: 'Build #846 had 2 flaky tests (auto-retried)' },
  { id: 13, time: '14:20:02', source: 'DEPLOY',    severity: 'INFO',  message: 'Rollback completed for v2.4.0' },
  { id: 14, time: '14:19:48', source: 'ERROR',     severity: 'ERROR', message: 'Failed to process webhook: timeout after 30s' },
  { id: 15, time: '14:19:35', source: 'STAGING',   severity: 'INFO',  message: 'Load test results: 12,450 RPS sustained' },
]

// ── Chat data ─────────────────────────────────────────────────────────────────

const chatMessages: ChatMessage[] = [
  { id: 1,  agent: 'Scanner',        time: '14:22:55', isAlert: false, message: 'Detected 3 new vulnerabilities in dependencies: lodash@4.17.20, express@4.16.0, ws@7.4.3' },
  { id: 2,  agent: 'Monitor',        time: '14:22:40', isAlert: false, message: 'All systems nominal. CPU at 34%, memory at 52%.' },
  { id: 3,  agent: 'Responder',      time: '14:22:20', isAlert: false, message: '@Scanner can you prioritize CVE-2024-31337? It\'s critical.' },
  { id: 4,  agent: 'Sentinel',       time: '14:22:05', isAlert: true,  message: 'ALERT: Unusual login pattern detected from IP 192.168.1.105' },
  { id: 5,  agent: 'PackageMonitor', time: '14:21:50', isAlert: false, message: '@Monitor new version available: react@18.3.0 - shall I schedule update?' },
  { id: 6,  agent: 'SQLSpecialist',  time: '14:21:30', isAlert: false, message: 'Migration complete. Indexes rebuilt on orders table. Query performance improved 40%.' },
  { id: 7,  agent: 'DeployChecker',  time: '14:21:10', isAlert: false, message: '@Responder deployment to prod requires your approval.' },
  { id: 8,  agent: 'Scanner',        time: '14:20:50', isAlert: false, message: 'Acknowledged @Responder. CVE prioritized and remediation queued.' },
  { id: 9,  agent: 'Monitor',        time: '14:20:35', isAlert: false, message: '@PackageMonitor proceed with react update during maintenance window.' },
  { id: 10, agent: 'Sentinel',       time: '14:20:15', isAlert: true,  message: 'Flagging incident #4471 — potential security breach attempt.' },
  { id: 11, agent: 'SQLSpecialist',  time: '14:19:58', isAlert: false, message: '@Sentinel I\'m seeing suspicious query patterns in logs. Sharing data now.' },
  { id: 12, agent: 'Responder',      time: '14:19:40', isAlert: false, message: 'Acknowledged. @Sentinel @SQLSpecialist isolate affected systems.' },
]

// ── Filter state ──────────────────────────────────────────────────────────────

type FilterValue = 'ALL' | 'DEPLOY' | 'STAGING' | 'PROD' | 'CI/CD' | 'ERROR' | 'MIGRATION' | 'MONITOR'
const filterOptions: FilterValue[] = ['ALL', 'DEPLOY', 'STAGING', 'PROD', 'CI/CD', 'ERROR', 'MIGRATION', 'MONITOR']
const activeFilter = ref<FilterValue>('ALL')

const filteredEntries = computed<LogEntry[]>(() => {
  if (activeFilter.value === 'ALL') return logEntries
  return logEntries.filter(e => e.source === activeFilter.value)
})

// ── Scroll containers ─────────────────────────────────────────────────────────

const logScrollEl  = useTemplateRef<HTMLElement>('logScroll')
const chatScrollEl = useTemplateRef<HTMLElement>('chatScroll')
const logPaused    = ref(false)
const chatPaused   = ref(false)

// ── Live clock ────────────────────────────────────────────────────────────────

function formatClock(d: Date): string {
  return d.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
}
const liveClock = ref<string>(formatClock(new Date()))

// ── Intervals ─────────────────────────────────────────────────────────────────

let clockInterval:   ReturnType<typeof setInterval> | null = null
let scrollInterval:  ReturnType<typeof setInterval> | null = null

onMounted(() => {
  clockInterval = setInterval(() => {
    liveClock.value = formatClock(new Date())
  }, 1000)

  scrollInterval = setInterval(() => {
    if (!logPaused.value && logScrollEl.value) {
      logScrollEl.value.scrollTop = logScrollEl.value.scrollHeight
    }
    if (!chatPaused.value && chatScrollEl.value) {
      chatScrollEl.value.scrollTop = chatScrollEl.value.scrollHeight
    }
  }, 500)
})

onUnmounted(() => {
  if (clockInterval !== null) { clearInterval(clockInterval); clockInterval = null }
  if (scrollInterval !== null) { clearInterval(scrollInterval); scrollInterval = null }
})

// ── @mention rendering ────────────────────────────────────────────────────────

/**
 * Replace @AgentName tokens with styled spans.
 * Only known agent names are matched — no XSS surface.
 */
function renderMessage(msg: string): string {
  const knownAgents = Object.keys(agents)
  // Escape msg first so any HTML-like content in mock data is safe
  const escaped = msg
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')

  return escaped.replace(/@([A-Za-z]+)/g, (_, name: string) => {
    const match = knownAgents.find(k => k.toLowerCase() === name.toLowerCase())
    if (!match) return `@${name}`
    const color = agents[match].color
    return `<span class="mention" style="background:${color}22;color:${color};border-radius:4px;padding:1px 5px;font-size:0.8125rem">@${match}</span>`
  })
}

// ── Source badge CSS class helpers ────────────────────────────────────────────

function sourceBadgeClass(source: LogEntry['source']): string {
  return `badge--${source.toLowerCase().replace('/', '-')}`
}

function severityClass(severity: LogEntry['severity']): string {
  return `severity--${severity.toLowerCase()}`
}

function presenceClass(status: Agent['status']): string {
  return `presence--${status}`
}
</script>

<template>
  <div class="gp-root" role="application" aria-label="Aegis Agent Stream — Glassmorphism Panel">

    <!-- Ambient background blobs -->
    <div class="gp-ambient" aria-hidden="true">
      <div class="gp-ambient__blob gp-ambient__blob--cyan"></div>
      <div class="gp-ambient__blob gp-ambient__blob--purple"></div>
    </div>

    <!-- ── Sticky header ───────────────────────────────────────────────────── -->
    <header class="gp-header" role="banner">
      <div class="gp-header__left">
        <span class="gp-header__hex" aria-hidden="true">⬡</span>
        <h1 class="gp-header__title">AGENT STREAM</h1>
      </div>
      <time class="gp-header__clock" :datetime="liveClock" aria-live="off" aria-atomic="true">
        {{ liveClock }}
      </time>
    </header>

    <!-- ── Split body ─────────────────────────────────────────────────────── -->
    <div class="gp-body">

      <!-- ── LEFT: Activity Log ───────────────────────────────────────────── -->
      <section class="gp-log-panel" aria-label="Activity log">

        <!-- Filter toolbar -->
        <div class="gp-filter-bar" role="toolbar" aria-label="Filter activity log by source">
          <button
            v-for="f in filterOptions"
            :key="f"
            type="button"
            class="gp-filter-btn"
            :class="{ 'gp-filter-btn--active': activeFilter === f }"
            :aria-pressed="activeFilter === f"
            @click="activeFilter = f"
          >{{ f }}</button>
        </div>

        <!-- Log scroll container -->
        <div
          ref="logScroll"
          class="gp-log-scroll"
          role="log"
          aria-label="Scrollable activity log entries"
          aria-live="polite"
          @mouseenter="logPaused = true"
          @mouseleave="logPaused = false"
        >
          <div
            v-for="(entry, index) in filteredEntries"
            :key="entry.id"
            class="gp-entry-wrap"
            :class="`gp-entry-wrap--${entry.source.toLowerCase().replace('/', '-')}`"
            :style="{ animationDelay: index * 150 + 'ms', animation: 'card-enter 0.5s ease both' }"
          >
            <div class="gp-entry">
              <time class="gp-entry__time">{{ entry.time }}</time>
              <span
                class="gp-entry__badge"
                :class="sourceBadgeClass(entry.source)"
                :aria-label="`Source: ${entry.source}`"
              >{{ entry.source }}</span>
              <span
                class="gp-entry__dot"
                :class="severityClass(entry.severity)"
                :aria-label="`Severity: ${entry.severity}`"
                role="img"
              ></span>
              <span class="gp-entry__msg">{{ entry.message }}</span>
            </div>
          </div>

          <!-- Empty state -->
          <p v-if="filteredEntries.length === 0" class="gp-log-empty" role="status">
            No entries match the selected filter.
          </p>
        </div>
      </section>

      <!-- ── RIGHT: Agent Chat ─────────────────────────────────────────────── -->
      <section class="gp-chat-panel" aria-label="Agent communication feed">

        <!-- Agent presence bar -->
        <div class="gp-presence-bar" role="list" aria-label="Agent presence status">
          <div
            v-for="ag in agentList"
            :key="ag.key"
            class="gp-presence-agent"
            :class="presenceClass(ag.status)"
            role="listitem"
            :aria-label="`${ag.label}: ${ag.status}`"
            :title="`${ag.label} — ${ag.status}`"
          >
            <div
              class="gp-presence-avatar"
              :style="{
                background: ag.color + '22',
                borderColor: ag.color,
                boxShadow: ag.status === 'online'
                  ? `0 0 10px ${ag.color}66`
                  : ag.status === 'busy'
                    ? `0 0 10px ${ag.color}88`
                    : 'none'
              }"
            >
              <span class="gp-presence-icon" :style="{ color: ag.color }" aria-hidden="true">{{ ag.icon }}</span>
            </div>
            <span
              class="gp-presence-dot"
              :style="{
                background: ag.status === 'online' ? '#2ED573' : ag.status === 'busy' ? '#FFA502' : '#5a5a72'
              }"
              aria-hidden="true"
            ></span>
          </div>
        </div>

        <!-- Chat scroll container -->
        <div
          ref="chatScroll"
          class="gp-chat-scroll"
          role="log"
          aria-label="Agent message stream"
          aria-live="polite"
          @mouseenter="chatPaused = true"
          @mouseleave="chatPaused = false"
        >
          <article
            v-for="(msg, index) in chatMessages"
            :key="msg.id"
            class="gp-bubble"
            :class="{ 'gp-bubble--alert': msg.isAlert }"
            :style="{ animationDelay: index * 200 + 'ms', animation: 'bubble-enter 0.5s ease both' }"
            :aria-label="`${agents[msg.agent].label} at ${msg.time}${msg.isAlert ? ' — ALERT' : ''}`"
          >
            <!-- Avatar -->
            <div
              class="gp-bubble__avatar"
              :style="{
                background: agents[msg.agent].color + '22',
                borderColor: agents[msg.agent].color,
                boxShadow: `0 2px 10px ${agents[msg.agent].color}33`
              }"
              aria-hidden="true"
            >
              <span :style="{ color: agents[msg.agent].color }">{{ agents[msg.agent].icon }}</span>
            </div>

            <!-- Content -->
            <div class="gp-bubble__content">
              <div class="gp-bubble__meta">
                <span
                  class="gp-bubble__name"
                  :style="{ color: agents[msg.agent].color }"
                >{{ agents[msg.agent].label }}</span>
                <time class="gp-bubble__time">{{ msg.time }}</time>
              </div>

              <!-- Alert badge -->
              <div v-if="msg.isAlert" class="gp-alert-badge" aria-hidden="true">⚠ ALERT</div>

              <!-- Message with @mentions rendered via v-html (sanitized by renderMessage) -->
              <p
                class="gp-bubble__text"
                v-html="renderMessage(msg.message)"
              ></p>
            </div>
          </article>
        </div>
      </section>

    </div>
  </div>
</template>

<style scoped>
/* ── CSS custom properties ────────────────────────────────────────────────── */
.gp-root {
  --brand-bg:           #0a0a0f;
  --brand-bg-secondary: #12121a;
  --brand-surface:      #1a1a2e;
  --brand-primary:      #f0f0f5;
  --brand-secondary:    #6e7fff;
  --brand-accent:       #e63946;
  --brand-text:         #e8e8ed;
  --brand-muted:        #5a5a72;
  --brand-border:       #2a2a3e;
  --brand-error:        #ff2d2d;
  --brand-success:      #f0f0f5;
  --brand-warning:      #e63946;
  --font-heading:       'Play', sans-serif;
  --font-body:          'Play', sans-serif;
  --font-mono:          'Play', sans-serif;
  --duration-fast:      150ms;
  --duration-normal:    350ms;
  --duration-slow:      600ms;
  --easing:             cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --radius-sm:          0.5rem;
  --radius-md:          1rem;
  --radius-lg:          1.5rem;
  --space-unit:         0.5rem;
}

/* ── Reset ────────────────────────────────────────────────────────────────── */
.gp-root *,
.gp-root *::before,
.gp-root *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* ── Root container ───────────────────────────────────────────────────────── */
.gp-root {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background-color: var(--brand-bg);
  background-image:
    radial-gradient(ellipse 60% 40% at 15% 20%, rgba(110, 127, 255, 0.07) 0%, transparent 70%),
    radial-gradient(ellipse 50% 35% at 85% 75%, rgba(155, 89, 182, 0.06) 0%, transparent 70%);
  font-family: var(--font-body);
  color: var(--brand-text);
}

/* ── Ambient background blobs ─────────────────────────────────────────────── */
.gp-ambient {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.gp-ambient__blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.12;
  animation: float-bg 8s ease-in-out infinite;
}

.gp-ambient__blob--cyan {
  width: 500px;
  height: 500px;
  top: -120px;
  left: -80px;
  background: radial-gradient(circle, rgba(110, 127, 255, 1) 0%, transparent 70%);
  animation-delay: 0s;
}

.gp-ambient__blob--purple {
  width: 400px;
  height: 400px;
  bottom: -100px;
  right: -60px;
  background: radial-gradient(circle, rgba(155, 89, 182, 1) 0%, transparent 70%);
  animation-delay: 4s;
}

/* ── Header ───────────────────────────────────────────────────────────────── */
.gp-header {
  position: relative;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
  padding: 0 calc(var(--space-unit) * 4);
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}

.gp-header__left {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.gp-header__hex {
  font-size: 1.1rem;
  color: var(--brand-secondary);
  text-shadow: 0 0 14px rgba(110, 127, 255, 0.7);
}

.gp-header__title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--brand-primary);
  text-shadow: 0 0 20px rgba(110, 127, 255, 0.4);
}

.gp-header__clock {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  color: var(--brand-secondary);
  letter-spacing: 0.05em;
  opacity: 0.9;
}

/* ── Body split grid ──────────────────────────────────────────────────────── */
.gp-body {
  position: relative;
  z-index: 10;
  display: grid;
  grid-template-columns: 60fr 40fr;
  flex: 1;
  overflow: hidden;
  min-height: 0;
}

/* ── Left panel: Activity Log ─────────────────────────────────────────────── */
.gp-log-panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: rgba(26, 26, 46, 0.4);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
}

/* ── Filter bar ───────────────────────────────────────────────────────────── */
.gp-filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  background: rgba(10, 10, 15, 0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
}

.gp-filter-btn {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  background: transparent;
  color: rgba(232, 232, 237, 0.5);
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 400;
  letter-spacing: 0.06em;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  cursor: pointer;
  transition: all var(--duration-fast) var(--easing);
}

.gp-filter-btn:hover {
  color: var(--brand-primary);
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.04);
}

.gp-filter-btn--active {
  background: rgba(110, 127, 255, 0.25);
  border-color: rgba(110, 127, 255, 0.5);
  color: var(--brand-primary);
  box-shadow: 0 0 8px rgba(110, 127, 255, 0.2);
}

.gp-filter-btn:focus-visible {
  outline: 2px solid var(--brand-secondary);
  outline-offset: 3px;
}

/* ── Log scroll container ─────────────────────────────────────────────────── */
.gp-log-scroll {
  flex: 1;
  overflow-y: auto;
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  scrollbar-width: thin;
  scrollbar-color: rgba(110, 127, 255, 0.3) transparent;
}

.gp-log-scroll::-webkit-scrollbar {
  width: 4px;
}

.gp-log-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.gp-log-scroll::-webkit-scrollbar-thumb {
  background: rgba(110, 127, 255, 0.3);
  border-radius: 2px;
}

/* ── Log entry gradient-border wrapper ────────────────────────────────────── */
.gp-entry-wrap {
  border-radius: 10px;
  margin-bottom: calc(var(--space-unit) * 2);
  padding: 1px;
}

/* Gradient border per source */
.gp-entry-wrap--deploy    { background: linear-gradient(135deg, rgba(110, 127, 255, 0.4), rgba(110, 127, 255, 0.08)); }
.gp-entry-wrap--staging   { background: linear-gradient(135deg, rgba(255, 165, 2, 0.35),  rgba(255, 165, 2, 0.06));  }
.gp-entry-wrap--prod      { background: linear-gradient(135deg, rgba(46, 213, 115, 0.35), rgba(46, 213, 115, 0.06)); }
.gp-entry-wrap--error     { background: linear-gradient(135deg, rgba(255, 45, 45, 0.45),  rgba(255, 45, 45, 0.08));  }
.gp-entry-wrap--ci-cd     { background: linear-gradient(135deg, rgba(110, 127, 255, 0.28), rgba(110, 127, 255, 0.05)); }
.gp-entry-wrap--migration { background: linear-gradient(135deg, rgba(138, 43, 226, 0.38), rgba(138, 43, 226, 0.06)); }
.gp-entry-wrap--monitor   { background: linear-gradient(135deg, rgba(0, 217, 255, 0.32),  rgba(0, 217, 255, 0.05));  }

/* Inner entry card */
.gp-entry {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1.5);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  background: rgba(18, 18, 26, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 9px;
}

/* ── Log entry fields ─────────────────────────────────────────────────────── */
.gp-entry__time {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: rgba(90, 90, 114, 0.85);
  min-width: 70px;
  flex-shrink: 0;
  letter-spacing: 0.02em;
}

.gp-entry__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  padding: 2px 8px;
  flex-shrink: 0;
  white-space: nowrap;
}

/* Badge variants */
.badge--deploy    { background: linear-gradient(135deg, rgba(110, 127, 255, 0.5), rgba(110, 127, 255, 0.2)); color: #a5b0ff; border: 1px solid rgba(110, 127, 255, 0.4); }
.badge--staging   { background: linear-gradient(135deg, rgba(255, 165, 2, 0.4),   rgba(255, 165, 2, 0.15));  color: #FFD066; border: 1px solid rgba(255, 165, 2, 0.35);  }
.badge--prod      { background: linear-gradient(135deg, rgba(46, 213, 115, 0.4),  rgba(46, 213, 115, 0.15)); color: #7FFFAA; border: 1px solid rgba(46, 213, 115, 0.35); }
.badge--error     { background: linear-gradient(135deg, rgba(255, 45, 45, 0.5),   rgba(255, 45, 45, 0.2));   color: #FF8080; border: 1px solid rgba(255, 45, 45, 0.4);   }
.badge--ci-cd     { background: linear-gradient(135deg, rgba(110, 127, 255, 0.3), rgba(110, 127, 255, 0.1)); color: #9aadff; border: 1px solid rgba(110, 127, 255, 0.3); }
.badge--migration { background: linear-gradient(135deg, rgba(138, 43, 226, 0.4),  rgba(138, 43, 226, 0.15)); color: #D4AAFF; border: 1px solid rgba(138, 43, 226, 0.35); }
.badge--monitor   { background: linear-gradient(135deg, rgba(0, 217, 255, 0.35),  rgba(0, 217, 255, 0.12));  color: #80F0FF; border: 1px solid rgba(0, 217, 255, 0.3);   }

/* ── Severity dot ─────────────────────────────────────────────────────────── */
.gp-entry__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.severity--info  { background: var(--brand-secondary); box-shadow: 0 0 6px rgba(110, 127, 255, 0.6); }
.severity--warn  { background: var(--brand-warning);   box-shadow: 0 0 6px color-mix(in srgb, var(--brand-warning) 60%, transparent);   }
.severity--error { background: var(--brand-error);     box-shadow: 0 0 6px rgba(255, 45, 45, 0.7);   }

/* ── Entry message ────────────────────────────────────────────────────────── */
.gp-entry__msg {
  font-size: 0.8125rem;
  color: var(--brand-text);
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

/* Empty state */
.gp-log-empty {
  text-align: center;
  color: var(--brand-muted);
  font-size: 0.875rem;
  padding: calc(var(--space-unit) * 8);
}

/* ── Right panel: Agent Chat ──────────────────────────────────────────────── */
.gp-chat-panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: rgba(18, 18, 26, 0.5);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-left: 1px solid rgba(255, 255, 255, 0.06);
}

/* ── Presence bar ─────────────────────────────────────────────────────────── */
.gp-presence-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: calc(var(--space-unit) * 3);
  height: 64px;
  padding: 0 calc(var(--space-unit) * 3);
  background: rgba(10, 10, 15, 0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.gp-presence-agent {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  position: relative;
}

.gp-presence-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1.5px solid;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  transition: box-shadow var(--duration-normal) var(--easing);
}

.gp-presence--busy .gp-presence-avatar {
  animation: presence-pulse 2s ease-in-out infinite;
}

.gp-presence-icon {
  line-height: 1;
  font-style: normal;
}

.gp-presence-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.gp-presence--busy .gp-presence-dot {
  animation: dot-pulse 2s ease-in-out infinite;
}

/* ── Chat scroll container ────────────────────────────────────────────────── */
.gp-chat-scroll {
  flex: 1;
  overflow-y: auto;
  padding: calc(var(--space-unit) * 2.5) calc(var(--space-unit) * 3);
  scrollbar-width: thin;
  scrollbar-color: rgba(110, 127, 255, 0.25) transparent;
}

.gp-chat-scroll::-webkit-scrollbar {
  width: 4px;
}

.gp-chat-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.gp-chat-scroll::-webkit-scrollbar-thumb {
  background: rgba(110, 127, 255, 0.25);
  border-radius: 2px;
}

/* ── Chat bubble ──────────────────────────────────────────────────────────── */
.gp-bubble {
  display: flex;
  gap: calc(var(--space-unit) * 2.5);
  margin-bottom: calc(var(--space-unit) * 2.5);
  padding: calc(var(--space-unit) * 2.5) calc(var(--space-unit) * 3);
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: box-shadow var(--duration-normal) var(--easing);
}

.gp-bubble:hover {
  background: rgba(26, 26, 46, 0.75);
}

/* Alert bubble overrides */
.gp-bubble--alert {
  border-color: rgba(255, 45, 45, 0.4);
  background: rgba(255, 45, 45, 0.06);
  animation: alert-glow 2s ease-in-out infinite;
}

/* ── Bubble avatar ────────────────────────────────────────────────────────── */
.gp-bubble__avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1.5px solid;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
  margin-top: 2px;
}

/* ── Bubble content ───────────────────────────────────────────────────────── */
.gp-bubble__content {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
  flex: 1;
  min-width: 0;
}

.gp-bubble__meta {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 2);
}

.gp-bubble__name {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

.gp-bubble__time {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  flex-shrink: 0;
}

/* ── Alert badge ──────────────────────────────────────────────────────────── */
.gp-alert-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--brand-error);
  background: rgba(255, 45, 45, 0.12);
  border: 1px solid rgba(255, 45, 45, 0.35);
  border-radius: 4px;
  padding: 2px 7px;
  width: fit-content;
}

/* ── Message text ─────────────────────────────────────────────────────────── */
.gp-bubble__text {
  font-size: 0.875rem;
  color: var(--brand-text);
  line-height: 1.55;
  word-break: break-word;
}

/* ── Keyframe animations ──────────────────────────────────────────────────── */
@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateX(-12px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@keyframes bubble-enter {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes alert-glow {
  0%, 100% {
    box-shadow: 0 0 8px rgba(255, 45, 45, 0.2);
  }
  50% {
    box-shadow: 0 0 22px rgba(255, 45, 45, 0.55);
  }
}

@keyframes presence-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.75;
    transform: scale(0.96);
  }
}

@keyframes dot-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(0.85);
  }
}

@keyframes float-bg {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

/* ── Responsive ────────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .gp-body {
    grid-template-columns: 1fr;
    grid-template-rows: 50vh 50vh;
    overflow-y: auto;
  }

  .gp-root {
    height: auto;
    min-height: 100vh;
    overflow: visible;
  }

  .gp-log-panel,
  .gp-chat-panel {
    border-right: none;
    border-left: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }

  .gp-presence-bar {
    gap: calc(var(--space-unit) * 2);
  }

  .gp-filter-bar {
    gap: calc(var(--space-unit) * 0.75);
  }

  .gp-filter-btn {
    font-size: 0.5625rem;
    padding: 2px 6px;
  }

  .gp-entry__msg {
    font-size: 0.75rem;
  }

  .gp-header__title {
    font-size: 0.875rem;
    letter-spacing: 0.1em;
  }
}

@media (max-width: 480px) {
  .gp-entry__time {
    display: none;
  }

  .gp-bubble__time {
    display: none;
  }
}

/* ── Reduced motion ───────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>

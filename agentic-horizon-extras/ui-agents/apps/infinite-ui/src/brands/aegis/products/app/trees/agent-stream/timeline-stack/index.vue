<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

// ── Mock Data ──────────────────────────────────────────────────────────────

interface LogEntry {
  id: number
  time: string
  source: string
  severity: string
  message: string
}

interface Agent {
  id: string
  name: string
  role: string
  color: string
  icon: string
  presence: string
}

interface ChatMessage {
  id: number
  agentId: string
  time: string
  text: string
  isAlert: boolean
}

const logEntries: LogEntry[] = [
  { id: 1,  time: '14:23', source: 'DEPLOY',    severity: 'INFO',  message: 'v2.4.1 deployed to staging cluster-02' },
  { id: 2,  time: '14:22', source: 'STAGING',   severity: 'WARN',  message: 'Memory usage at 78% on pod-api-03' },
  { id: 3,  time: '14:22', source: 'ERROR',     severity: 'ERROR', message: 'Database connection pool exhausted (retry 3/5)' },
  { id: 4,  time: '14:22', source: 'PROD',      severity: 'INFO',  message: 'Health check passed - all services nominal' },
  { id: 5,  time: '14:21', source: 'CI/CD',     severity: 'INFO',  message: 'Build #847 completed in 4m 32s' },
  { id: 6,  time: '14:21', source: 'MIGRATION', severity: 'INFO',  message: 'Schema migration v3.2.1 applied to users table' },
  { id: 7,  time: '14:21', source: 'DEPLOY',    severity: 'INFO',  message: 'Canary release: 10% traffic on v2.4.1' },
  { id: 8,  time: '14:21', source: 'ERROR',     severity: 'WARN',  message: 'Elevated latency on /api/v2/search endpoint' },
  { id: 9,  time: '14:20', source: 'MONITOR',   severity: 'INFO',  message: 'Auto-scaling triggered: +2 instances' },
  { id: 10, time: '14:20', source: 'STAGING',   severity: 'INFO',  message: 'Integration tests passing (142/142)' },
  { id: 11, time: '14:20', source: 'PROD',      severity: 'INFO',  message: 'Cache hit ratio: 94.2%' },
  { id: 12, time: '14:20', source: 'CI/CD',     severity: 'WARN',  message: 'Build #846 had 2 flaky tests (auto-retried)' },
  { id: 13, time: '14:19', source: 'DEPLOY',    severity: 'INFO',  message: 'Rollback completed for v2.4.0' },
  { id: 14, time: '14:19', source: 'ERROR',     severity: 'ERROR', message: 'Failed to process webhook: timeout after 30s' },
  { id: 15, time: '14:19', source: 'STAGING',   severity: 'INFO',  message: 'Load test results: 12,450 RPS sustained' },
]

const agents: Agent[] = [
  { id: 'scanner',   name: 'Scanner',  role: 'Vulnerability', color: '#00D9FF', icon: 'scan',     presence: 'online' },
  { id: 'monitor',   name: 'Monitor',  role: 'Observability', color: '#2ED573', icon: 'activity', presence: 'online' },
  { id: 'responder', name: 'Responder',role: 'Incident Resp', color: '#FF6B35', icon: 'shield',   presence: 'busy'   },
  { id: 'sentinel',  name: 'Sentinel', role: 'Threat Intel',  color: '#FF4757', icon: 'alert',    presence: 'busy'   },
  { id: 'pkgmon',    name: 'Pkg Mon',  role: 'Dependencies',  color: '#7B61FF', icon: 'package',  presence: 'idle'   },
  { id: 'sqlspec',   name: 'SQL Spec', role: 'Database',      color: '#3498DB', icon: 'database', presence: 'online' },
  { id: 'deploychk', name: 'Deploy',   role: 'Deployments',   color: '#FFA502', icon: 'rocket',   presence: 'idle'   },
]

const chatMessages: ChatMessage[] = [
  { id: 1,  agentId: 'scanner',   time: '14:21', text: 'Detected 3 new vulnerabilities in dependencies: lodash@4.17.20, express@4.16.0, ws@7.4.3', isAlert: false },
  { id: 2,  agentId: 'monitor',   time: '14:21', text: 'All systems nominal. CPU at 34%, memory at 52%.', isAlert: false },
  { id: 3,  agentId: 'responder', time: '14:21', text: "@Scanner can you prioritize CVE-2024-31337? It's critical.", isAlert: false },
  { id: 4,  agentId: 'sentinel',  time: '14:20', text: 'ALERT: Unusual login pattern detected from IP 192.168.1.105', isAlert: true },
  { id: 5,  agentId: 'pkgmon',    time: '14:20', text: '@Monitor new version available: react@18.3.0 - shall I schedule update?', isAlert: false },
  { id: 6,  agentId: 'sqlspec',   time: '14:20', text: 'Migration complete. Indexes rebuilt on orders table. Query performance improved 40%.', isAlert: false },
  { id: 7,  agentId: 'deploychk', time: '14:20', text: '@Responder deployment to prod requires your approval', isAlert: false },
  { id: 8,  agentId: 'scanner',   time: '14:19', text: 'Acknowledged @Responder. CVE prioritized and remediation queued.', isAlert: false },
  { id: 9,  agentId: 'monitor',   time: '14:19', text: '@Package Monitor proceed with react update during maintenance window', isAlert: false },
  { id: 10, agentId: 'sentinel',  time: '14:19', text: 'Flagging incident #4471 — potential security breach attempt', isAlert: true },
  { id: 11, agentId: 'sqlspec',   time: '14:19', text: "@Sentinel I'm seeing suspicious query patterns in logs. Sharing data now.", isAlert: false },
  { id: 12, agentId: 'responder', time: '14:18', text: 'Acknowledged. @Sentinel @SQL Specialist isolate affected systems.', isAlert: false },
]

// ── Icon Paths ─────────────────────────────────────────────────────────────

const iconPaths: Record<string, string> = {
  scan:     'M3 3h3v3H3zM8 3h3v3H8zM3 8h3v3H3zM10 10h3v3h-3zM10 1v3h3V1zM1 10v3h3v-3z',
  activity: 'M22 12h-4l-3 9L9 3l-3 9H2',
  shield:   'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z',
  alert:    'M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0zM12 9v4M12 17h.01',
  package:  'M16.5 9.4l-9-5.19M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16zM3.27 6.96L12 12.01l8.73-5.05M12 22.08V12',
  database: 'M12 2C6.48 2 2 3.79 2 6v12c0 2.21 4.48 4 10 4s10-1.79 10-4V6c0-2.21-4.48-4-10-4zM2 12c0 1.1 3.58 2 8 2s8-.9 8-2M2 18c0 1.1 3.58 2 8 2s8-.9 8-2M2 6c0 1.1 3.58 2 8 2s8-.9 8-2',
  rocket:   'M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 00-2.91-.09zM12 15l-3-3a22 22 0 012-3.95A12.88 12.88 0 0122 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 01-4 2zM9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0M15 19v-5s3.03-.55 4-2c1.08-1.62 0-5 0-5',
}

// ── Source / Severity Helpers ──────────────────────────────────────────────

const sourceColors: Record<string, string> = {
  'DEPLOY':    '#3498DB',
  'STAGING':   '#FFA502',
  'PROD':      '#2ED573',
  'ERROR':     '#FF4757',
  'CI/CD':     '#7B61FF',
  'MIGRATION': '#00D9FF',
  'MONITOR':   '#FF6B35',
}

function severityBorderColor(severity: string): string {
  if (severity === 'ERROR') return 'var(--brand-error)'
  if (severity === 'WARN')  return 'var(--brand-warning)'
  return 'var(--brand-secondary)'
}

function severityDotColor(severity: string): string {
  if (severity === 'ERROR') return 'var(--brand-error)'
  if (severity === 'WARN')  return 'var(--brand-warning)'
  return 'var(--brand-success)'
}

function presenceColor(presence: string): string {
  if (presence === 'online') return 'var(--brand-success)'
  if (presence === 'busy')   return 'var(--brand-warning)'
  return 'var(--brand-muted)'
}

// ── Agent Lookup ───────────────────────────────────────────────────────────

const agentById = (id: string): Agent | undefined => agents.find(a => a.id === id)

// ── @mention Parser ────────────────────────────────────────────────────────

interface TextPart {
  type: 'text' | 'mention'
  value: string
}

function parseMessage(text: string): TextPart[] {
  const parts: TextPart[] = []
  const regex = /@([\w][\w\s]*?)(?=\s|$|[.,!?])/g
  let last = 0
  let match: RegExpExecArray | null
  while ((match = regex.exec(text)) !== null) {
    if (match.index > last) {
      parts.push({ type: 'text', value: text.slice(last, match.index) })
    }
    parts.push({ type: 'mention', value: match[0] })
    last = match.index + match[0].length
  }
  if (last < text.length) {
    parts.push({ type: 'text', value: text.slice(last) })
  }
  return parts
}

// ── Filter State ───────────────────────────────────────────────────────────

const filters = ['ALL', 'DEPLOY', 'STAGING', 'PROD', 'ERROR', 'CI/CD', 'MIGRATION', 'MONITOR']
const activeFilter = ref<string>('ALL')

// ── Live Feed State ────────────────────────────────────────────────────────

const visibleEntries = ref<LogEntry[]>([...logEntries])
const entryIndex = ref<number>(logEntries.length)
const isPaused = ref<boolean>(false)
const logContainer = ref<HTMLElement | null>(null)

let scrollInterval: ReturnType<typeof setInterval> | null = null

const filteredLog = computed<LogEntry[]>(() =>
  activeFilter.value === 'ALL'
    ? visibleEntries.value
    : visibleEntries.value.filter(e => e.source === activeFilter.value)
)

function startFeed(): void {
  scrollInterval = setInterval(() => {
    if (isPaused.value) return
    const base = logEntries[entryIndex.value % logEntries.length]
    const next: LogEntry = { ...base, id: Date.now() }
    visibleEntries.value = [next, ...visibleEntries.value.slice(0, 19)]
    entryIndex.value++
    nextTick(() => {
      if (logContainer.value && !isPaused.value) {
        logContainer.value.scrollTop = 0
      }
    })
  }, 3500)
}

// ── Clock ──────────────────────────────────────────────────────────────────

const currentTime = ref<string>('')

function formatTime(d: Date): string {
  return d.toTimeString().slice(0, 8)
}

let clockInterval: ReturnType<typeof setInterval> | null = null

function startClock(): void {
  currentTime.value = formatTime(new Date())
  clockInterval = setInterval(() => {
    currentTime.value = formatTime(new Date())
  }, 1000)
}

// ── Lifecycle ──────────────────────────────────────────────────────────────

onMounted(() => {
  startClock()
  startFeed()
})

onUnmounted(() => {
  if (scrollInterval) { clearInterval(scrollInterval); scrollInterval = null }
  if (clockInterval)  { clearInterval(clockInterval);  clockInterval = null }
})
</script>

<template>
  <div class="timeline-stack">

    <!-- ── Sticky Header ─────────────────────────────────────────── -->
    <header class="stream-header" role="banner">
      <div class="stream-header__inner">

        <!-- Presence Bar -->
        <div class="presence-bar" role="list" aria-label="Agent presence status">
          <div
            v-for="agent in agents"
            :key="agent.id"
            class="presence-item"
            role="listitem"
            :style="{ '--agent-color': agent.color, '--presence-color': presenceColor(agent.presence) }"
          >
            <div
              class="presence-avatar"
              :title="`${agent.name} — ${agent.presence}`"
            >
              <svg
                viewBox="0 0 24 24"
                width="12"
                height="12"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path :d="iconPaths[agent.icon]" />
              </svg>
            </div>
            <span class="presence-name">{{ agent.name }}</span>
          </div>
        </div>

        <!-- Title Row -->
        <div class="stream-title-row">
          <span class="stream-overline" aria-hidden="true">AEGIS</span>
          <h1 class="stream-title">AGENT STREAM</h1>
          <div class="stream-clock" aria-live="polite" aria-label="Current time">{{ currentTime }}</div>
        </div>

      </div>
    </header>

    <!-- ── Split Body ────────────────────────────────────────────── -->
    <main class="stream-body">

      <!-- LEFT: Timeline Log -->
      <section class="log-panel" aria-label="Activity log timeline">

        <!-- Filter Strip -->
        <div class="filter-strip" role="group" aria-label="Filter log by source">
          <button
            v-for="f in filters"
            :key="f"
            type="button"
            class="filter-chip"
            :class="{ 'filter-chip--active': activeFilter === f }"
            :aria-pressed="activeFilter === f"
            @click="activeFilter = f"
          >{{ f }}</button>
        </div>

        <!-- Timeline Container -->
        <div
          ref="logContainer"
          class="timeline-container"
          role="log"
          aria-live="polite"
          aria-label="Live activity log — hover to pause"
          tabindex="0"
          @mouseenter="isPaused = true"
          @mouseleave="isPaused = false"
        >
          <div
            v-for="(entry, index) in filteredLog"
            :key="entry.id"
            class="timeline-row"
            :style="{ animationDelay: `${index * 80}ms` }"
          >
            <!-- Timeline dot (on the vertical line) -->
            <div
              class="timeline-dot"
              :style="{ background: severityDotColor(entry.severity) }"
              :aria-label="`${entry.severity} severity`"
            ></div>

            <!-- Card -->
            <article
              class="timeline-card"
              :style="{
                borderLeftColor: severityBorderColor(entry.severity),
                '--source-color': sourceColors[entry.source] ?? 'var(--brand-muted)',
              }"
            >
              <div class="card-meta">
                <span class="card-time">{{ entry.time }}</span>
                <span class="source-badge">{{ entry.source }}</span>
                <span
                  class="severity-label"
                  :class="`severity--${entry.severity.toLowerCase()}`"
                >{{ entry.severity }}</span>
              </div>
              <p class="card-message">{{ entry.message }}</p>
            </article>
          </div>

          <!-- Pause indicator -->
          <div v-if="isPaused" class="pause-indicator" aria-live="polite">
            ⏸ Paused — move cursor away to resume
          </div>
        </div>

      </section>

      <!-- RIGHT: Agent Chat Feed -->
      <section class="chat-panel" aria-label="Agent communication feed">

        <div
          class="chat-feed"
          role="log"
          aria-live="polite"
          aria-label="Agent chat messages"
        >
          <article
            v-for="(msg, index) in chatMessages"
            :key="msg.id"
            class="chat-card"
            :class="{ 'chat-card--alert': msg.isAlert }"
            :style="{
              '--agent-color': agentById(msg.agentId)?.color ?? 'var(--brand-muted)',
              animationDelay: `${index * 150}ms`,
            }"
          >
            <div class="chat-card__header">
              <div
                class="chat-avatar"
                :aria-label="agentById(msg.agentId)?.name"
              >
                <svg
                  viewBox="0 0 24 24"
                  width="14"
                  height="14"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  aria-hidden="true"
                >
                  <path :d="iconPaths[agentById(msg.agentId)?.icon ?? 'shield']" />
                </svg>
              </div>
              <div class="chat-agent-info">
                <span class="chat-agent-name">{{ agentById(msg.agentId)?.name }}</span>
                <span class="chat-role-badge">{{ agentById(msg.agentId)?.role }}</span>
              </div>
              <span class="chat-time">{{ msg.time }}</span>
            </div>

            <p class="chat-message">
              <template
                v-for="(part, pi) in parseMessage(msg.text)"
                :key="pi"
              >
                <span v-if="part.type === 'mention'" class="mention">{{ part.value }}</span>
                <template v-else>{{ part.value }}</template>
              </template>
            </p>
          </article>
        </div>

      </section>

    </main>
  </div>
</template>

<style scoped>
/* ── CSS Custom Properties ───────────────────────────────────────────────── */
:root {
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
  --brand-warning:      #e63946;
  --brand-success:      #f0f0f5;
  --font-heading:       'Play', sans-serif;
  --font-body:          'Play', sans-serif;
  --font-mono:          'Play', sans-serif;
  --space-unit:         0.5rem;
  --radius-sm:          0.5rem;
  --radius-md:          1rem;
  --radius-lg:          1.5rem;
  --duration-fast:      150ms;
  --duration-normal:    350ms;
  --duration-slow:      600ms;
  --easing:             cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --shadow-sm:          0 1px 3px rgba(0, 0, 0, 0.6), 0 1px 2px rgba(0, 0, 0, 0.4);
  --shadow-md:          0 6px 16px rgba(0, 0, 0, 0.6), 0 2px 6px rgba(0, 0, 0, 0.4);
  --shadow-lg:          0 20px 40px rgba(0, 0, 0, 0.7), 0 8px 16px rgba(0, 0, 0, 0.5);
}

/* ── Root Layout ─────────────────────────────────────────────────────────── */
.timeline-stack {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--brand-bg);
  color: var(--brand-text);
  font-family: var(--font-body);
  overflow: hidden;
}

/* ── Sticky Header ───────────────────────────────────────────────────────── */
.stream-header {
  position: sticky;
  top: 0;
  z-index: 20;
  background: color-mix(in srgb, var(--brand-bg) 88%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--brand-border);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
  flex-shrink: 0;
}

.stream-header__inner {
  max-width: 1400px;
  margin: 0 auto;
}

/* ── Presence Bar ────────────────────────────────────────────────────────── */
.presence-bar {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: calc(var(--space-unit) * 4);
  padding-bottom: calc(var(--space-unit) * 2);
  border-bottom: 1px solid var(--brand-border);
  margin-bottom: calc(var(--space-unit) * 2);
  overflow-x: auto;
  scrollbar-width: none;
}

.presence-bar::-webkit-scrollbar {
  display: none;
}

.presence-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  flex-shrink: 0;
}

.presence-avatar {
  width: calc(var(--space-unit) * 7);
  height: calc(var(--space-unit) * 7);
  border-radius: 50%;
  background: color-mix(in srgb, var(--agent-color) 15%, transparent);
  border: 1.5px solid var(--agent-color);
  box-shadow: 0 0 0 2.5px var(--presence-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--agent-color);
  transition: box-shadow var(--duration-normal) var(--easing);
}

.presence-name {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  color: var(--brand-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: center;
  white-space: nowrap;
}

/* ── Stream Title Row ────────────────────────────────────────────────────── */
.stream-title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 3);
}

.stream-overline {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--brand-muted);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.stream-title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--brand-primary);
  margin: 0;
}

.stream-clock {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  margin-left: auto;
  letter-spacing: 0.06em;
}

/* ── Split Body ──────────────────────────────────────────────────────────── */
.stream-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  flex: 1;
  overflow: hidden;
  min-height: 0;
}

/* ── Log Panel (LEFT) ────────────────────────────────────────────────────── */
.log-panel {
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--brand-border);
  overflow: hidden;
}

/* ── Filter Strip ────────────────────────────────────────────────────────── */
.filter-strip {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 1);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  border-bottom: 1px solid var(--brand-border);
  flex-shrink: 0;
  overflow-x: auto;
  scrollbar-width: none;
}

.filter-strip::-webkit-scrollbar {
  display: none;
}

.filter-chip {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 1) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  border: 1px solid var(--brand-border);
  background: transparent;
  color: var(--brand-muted);
  cursor: pointer;
  white-space: nowrap;
  transition: all var(--duration-normal) var(--easing);
}

.filter-chip--active {
  background: color-mix(in srgb, var(--brand-secondary) 18%, transparent);
  border-color: var(--brand-secondary);
  color: var(--brand-secondary);
}

.filter-chip:hover:not(.filter-chip--active) {
  border-color: color-mix(in srgb, var(--brand-primary) 40%, transparent);
  color: var(--brand-text);
}

.filter-chip:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 2px;
}

/* ── Timeline Container ──────────────────────────────────────────────────── */
.timeline-container {
  flex: 1;
  overflow-y: auto;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 4) calc(var(--space-unit) * 4) calc(var(--space-unit) * 5);
  position: relative;
  scrollbar-width: thin;
  scrollbar-color: var(--brand-border) transparent;
  outline: none;
}

.timeline-container:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

/* Vertical connector line via ::before pseudo */
.timeline-container::before {
  content: '';
  position: absolute;
  left: calc(var(--space-unit) * 5 + 4px);
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--brand-border);
  pointer-events: none;
}

/* ── Timeline Rows ───────────────────────────────────────────────────────── */
.timeline-row {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 3);
  margin-bottom: calc(var(--space-unit) * 3);
  position: relative;
  animation: slideInLeft var(--duration-slow) var(--easing) both;
}

.timeline-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: calc(var(--space-unit) * 2);
  position: relative;
  z-index: 1;
  box-shadow: 0 0 8px currentColor;
}

/* ── Timeline Card ───────────────────────────────────────────────────────── */
.timeline-card {
  flex: 1;
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-left-width: 3px;
  border-radius: var(--radius-sm);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--duration-normal) var(--easing),
              border-color var(--duration-normal) var(--easing);
}

.timeline-card:hover {
  box-shadow: var(--shadow-md);
}

.card-meta {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  margin-bottom: calc(var(--space-unit) * 1);
  flex-wrap: wrap;
}

.card-time {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--brand-muted);
  letter-spacing: 0.04em;
}

.source-badge {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.5) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  background: color-mix(in srgb, var(--source-color, var(--brand-muted)) 14%, transparent);
  color: var(--source-color, var(--brand-muted));
  border: 1px solid color-mix(in srgb, var(--source-color, var(--brand-muted)) 28%, transparent);
}

.severity-label {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.severity--info  { color: var(--brand-secondary); }
.severity--warn  { color: var(--brand-warning); }
.severity--error { color: var(--brand-error); }

.card-message {
  font-size: 0.8125rem;
  color: var(--brand-text);
  margin: 0;
  line-height: 1.5;
}

/* ── Pause Indicator ─────────────────────────────────────────────────────── */
.pause-indicator {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--brand-muted);
  text-align: center;
  padding: calc(var(--space-unit) * 2);
  letter-spacing: 0.06em;
  animation: fadeUp var(--duration-normal) var(--easing) both;
}

/* ── Chat Panel (RIGHT) ──────────────────────────────────────────────────── */
.chat-panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--brand-bg-secondary);
}

.chat-feed {
  flex: 1;
  overflow-y: auto;
  padding: calc(var(--space-unit) * 3);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2.5);
  scrollbar-width: thin;
  scrollbar-color: var(--brand-border) transparent;
}

/* ── Chat Card ───────────────────────────────────────────────────────────── */
.chat-card {
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 3);
  box-shadow: var(--shadow-sm);
  animation: fadeUp var(--duration-slow) var(--easing) both;
  transition: box-shadow var(--duration-normal) var(--easing);
}

.chat-card--alert {
  box-shadow: 0 0 16px color-mix(in srgb, var(--brand-error) 28%, transparent),
              0 0 0 1px color-mix(in srgb, var(--brand-error) 50%, transparent);
}

.chat-card__header {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  margin-bottom: calc(var(--space-unit) * 2);
}

.chat-avatar {
  width: calc(var(--space-unit) * 9);
  height: calc(var(--space-unit) * 9);
  border-radius: 50%;
  background: color-mix(in srgb, var(--agent-color, var(--brand-muted)) 14%, transparent);
  border: 1.5px solid var(--agent-color, var(--brand-border));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--agent-color, var(--brand-text));
  flex-shrink: 0;
}

.chat-agent-info {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.chat-agent-name {
  font-family: var(--font-heading);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--agent-color, var(--brand-text));
  line-height: 1;
}

.chat-role-badge {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.5) calc(var(--space-unit) * 1.5);
  border-radius: var(--radius-sm);
  background: color-mix(in srgb, var(--agent-color, var(--brand-muted)) 10%, transparent);
  color: var(--agent-color, var(--brand-muted));
  display: inline-block;
}

.chat-time {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--brand-muted);
  margin-left: auto;
  letter-spacing: 0.03em;
  flex-shrink: 0;
}

.chat-message {
  font-size: 0.8125rem;
  color: var(--brand-text);
  margin: 0;
  line-height: 1.6;
}

.mention {
  color: var(--brand-secondary);
  background: color-mix(in srgb, var(--brand-secondary) 10%, transparent);
  border-radius: var(--radius-sm);
  padding: 0 calc(var(--space-unit) * 1);
  font-size: 0.85em;
  font-weight: 500;
}

/* ── Keyframe Animations ─────────────────────────────────────────────────── */
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ── Reduced Motion ──────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .timeline-row,
  .timeline-card,
  .chat-card,
  .pause-indicator {
    animation: none !important;
    transition: none !important;
  }
}

/* ── Responsive: Mobile ──────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .timeline-stack {
    height: auto;
    overflow: visible;
  }

  .stream-body {
    grid-template-columns: 1fr;
    overflow: visible;
    min-height: 0;
  }

  .log-panel {
    border-right: none;
    border-bottom: 1px solid var(--brand-border);
    min-height: 50vh;
  }

  .chat-panel {
    min-height: 50vh;
  }

  .stream-title-row {
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .stream-clock {
    margin-left: 0;
    width: 100%;
  }

  .presence-bar {
    gap: calc(var(--space-unit) * 2);
    justify-content: flex-start;
  }
}
</style>

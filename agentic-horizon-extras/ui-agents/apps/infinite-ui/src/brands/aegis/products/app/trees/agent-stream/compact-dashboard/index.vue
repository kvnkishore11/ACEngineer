<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

// ─── Data ────────────────────────────────────────────────────────────────────

const logEntries = [
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

const agentDefs: Record<string, { name: string; colorVar: string; role: string }> = {
  scanner:        { name: 'Scanner',        colorVar: '--agent-scanner',        role: 'Vuln Scanner' },
  monitor:        { name: 'Monitor',        colorVar: '--agent-monitor',        role: 'Sys Monitor' },
  responder:      { name: 'Responder',      colorVar: '--agent-responder',      role: 'Incident Resp.' },
  sentinel:       { name: 'Sentinel',       colorVar: '--agent-sentinel',       role: 'Security' },
  packageMonitor: { name: 'Pkg Monitor',    colorVar: '--agent-package-monitor', role: 'Packages' },
  sqlSpecialist:  { name: 'SQL Specialist', colorVar: '--agent-sql-specialist', role: 'Database' },
  deployChecker:  { name: 'Deploy Checker', colorVar: '--agent-deploy-checker', role: 'Deployments' },
}

const presenceStates: Record<string, 'online' | 'busy' | 'idle'> = {
  scanner:        'online',
  monitor:        'online',
  responder:      'busy',
  sentinel:       'busy',
  packageMonitor: 'idle',
  sqlSpecialist:  'online',
  deployChecker:  'idle',
}

const chatMessages = [
  { id: 1,  agent: 'scanner',        time: '14:23:05', message: "Detected 3 new vulnerabilities in dependencies: lodash@4.17.20, express@4.16.0, ws@7.4.3", flagged: false },
  { id: 2,  agent: 'monitor',        time: '14:22:51', message: "All systems nominal. CPU at 34%, memory at 52%.", flagged: false },
  { id: 3,  agent: 'responder',      time: '14:22:44', message: "@Scanner can you prioritize CVE-2024-31337? It's critical.", flagged: false },
  { id: 4,  agent: 'sentinel',       time: '14:22:38', message: "ALERT: Unusual login pattern detected from IP 192.168.1.105", flagged: true },
  { id: 5,  agent: 'packageMonitor', time: '14:22:20', message: "@Monitor new version available: react@18.3.0 - shall I schedule update?", flagged: false },
  { id: 6,  agent: 'sqlSpecialist',  time: '14:22:05', message: "Migration complete. Indexes rebuilt on orders table. Query performance improved 40%.", flagged: false },
  { id: 7,  agent: 'deployChecker',  time: '14:21:50', message: "@Responder deployment to prod requires your approval", flagged: false },
  { id: 8,  agent: 'scanner',        time: '14:21:35', message: "Acknowledged @Responder. CVE prioritized and remediation queued.", flagged: false },
  { id: 9,  agent: 'monitor',        time: '14:21:18', message: "@Package Monitor proceed with react update during maintenance window", flagged: false },
  { id: 10, agent: 'sentinel',       time: '14:21:02', message: "Flagging incident #4471 — potential security breach attempt", flagged: true },
  { id: 11, agent: 'sqlSpecialist',  time: '14:20:48', message: "@Sentinel I'm seeing suspicious query patterns in logs. Sharing data now.", flagged: false },
  { id: 12, agent: 'responder',      time: '14:20:35', message: "Acknowledged. @Sentinel @SQL Specialist isolate affected systems.", flagged: false },
]

const filterSources = ['ALL', 'DEPLOY', 'STAGING', 'PROD', 'ERROR', 'CI/CD', 'MIGRATION', 'MONITOR']

// ─── State ───────────────────────────────────────────────────────────────────

const activeFilter = ref<string>('ALL')
const isPaused = ref<boolean>(false)
const liveTime = ref<string>('')
const logScrollRef = ref<HTMLElement | null>(null)
const chatScrollRef = ref<HTMLElement | null>(null)

// ─── Computed ────────────────────────────────────────────────────────────────

const filteredLog = computed(() =>
  activeFilter.value === 'ALL'
    ? logEntries
    : logEntries.filter(e => e.source === activeFilter.value)
)

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatTime(): string {
  const now = new Date()
  return now.toTimeString().slice(0, 8)
}

function toggleFilter(source: string) {
  activeFilter.value = source
}

function pauseScroll() { isPaused.value = true }
function resumeScroll() { isPaused.value = false }

function sourceBadgeClass(source: string): string {
  return 'badge-' + source.toLowerCase().replace('/', '-')
}

function parseMessage(text: string): Array<{ type: 'text' | 'mention'; value: string }> {
  const parts: Array<{ type: 'text' | 'mention'; value: string }> = []
  const regex = /@[\w\s]+?(?=\s@|\s[^@\w]|$)/g
  let last = 0
  let match: RegExpExecArray | null
  // simpler split approach
  const segments = text.split(/(@\w+(?:\s\w+)?)/g)
  for (const seg of segments) {
    if (seg.startsWith('@')) {
      parts.push({ type: 'mention', value: seg })
    } else if (seg.length > 0) {
      parts.push({ type: 'text', value: seg })
    }
  }
  void last
  void match
  return parts
}

function scrollToBottom(el: HTMLElement | null) {
  if (el) el.scrollTop = el.scrollHeight
}

// ─── Lifecycle ───────────────────────────────────────────────────────────────

let timer: ReturnType<typeof setInterval>

onMounted(() => {
  liveTime.value = formatTime()
  timer = setInterval(() => { liveTime.value = formatTime() }, 1000)
  nextTick(() => {
    scrollToBottom(logScrollRef.value)
    scrollToBottom(chatScrollRef.value)
  })
})

onUnmounted(() => clearInterval(timer))

watch(filteredLog, async () => {
  if (!isPaused.value) {
    await nextTick()
    scrollToBottom(logScrollRef.value)
  }
})

const agentKeys = Object.keys(agentDefs)
</script>

<template>
  <div class="stream-root">

    <!-- ── Sticky Header ── -->
    <header class="stream-header">
      <h1 class="stream-title">AGENT STREAM</h1>
      <span class="stream-clock" aria-live="off">{{ liveTime }}</span>
    </header>

    <!-- ── Content Grid ── -->
    <div class="content-grid">

      <!-- ════════════════ LEFT: Activity Log ════════════════ -->
      <section class="log-column" aria-label="Activity Log">

        <!-- Filter Bar -->
        <div class="filter-bar" role="toolbar" aria-label="Filter activity log by source">
          <button
            v-for="src in filterSources"
            :key="src"
            type="button"
            class="filter-pill"
            :class="{ active: activeFilter === src }"
            :aria-pressed="activeFilter === src"
            @click="toggleFilter(src)"
          >{{ src }}</button>
        </div>

        <!-- Log Scroll Area -->
        <div
          class="log-scroll"
          ref="logScrollRef"
          @mouseenter="pauseScroll"
          @mouseleave="resumeScroll"
        >
          <div
            v-for="(entry, index) in filteredLog"
            :key="entry.id"
            class="log-row"
            :class="[`severity-${entry.severity.toLowerCase()}`, index % 2 === 0 ? 'row-even' : '']"
            :style="{ '--row-index': index }"
          >
            <span class="log-time">{{ entry.time }}</span>
            <span class="log-badge" :class="sourceBadgeClass(entry.source)">{{ entry.source }}</span>
            <span class="severity-dot" :class="`dot-${entry.severity.toLowerCase()}`"></span>
            <span class="log-sev-label">{{ entry.severity }}</span>
            <span class="log-msg">{{ entry.message }}</span>
          </div>
        </div>

      </section>

      <!-- ════════════════ RIGHT: Agent Chat ════════════════ -->
      <section class="chat-column" aria-label="Agent Chat">

        <!-- Presence Bar -->
        <div class="presence-bar">
          <div
            v-for="agentKey in agentKeys"
            :key="agentKey"
            class="presence-agent"
            :title="`${agentDefs[agentKey].name} — ${presenceStates[agentKey]}`"
          >
            <span class="agent-icon-wrap" :class="`agent-${agentKey}`">
              <!-- Scanner: radar -->
              <svg v-if="agentKey === 'scanner'" viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true">
                <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="8" cy="8" r="2" fill="currentColor"/>
                <line x1="8" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              <!-- Monitor: activity line -->
              <svg v-else-if="agentKey === 'monitor'" viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true">
                <polyline points="2,8 5,4 8,12 11,6 14,8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <!-- Responder: shield -->
              <svg v-else-if="agentKey === 'responder'" viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true">
                <path d="M8 2L2 5v4c0 3.3 2.5 6 6 7 3.5-1 6-3.7 6-7V5L8 2z" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              <!-- Sentinel: alert triangle -->
              <svg v-else-if="agentKey === 'sentinel'" viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true">
                <path d="M8 2L1 14h14L8 2z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
                <line x1="8" y1="7" x2="8" y2="10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="8" cy="12.5" r="0.8" fill="currentColor"/>
              </svg>
              <!-- Package Monitor: box -->
              <svg v-else-if="agentKey === 'packageMonitor'" viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true">
                <rect x="2" y="7" width="12" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/>
                <polyline points="0.5,7 8,2 15.5,7" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
                <line x1="8" y1="7" x2="8" y2="14" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              <!-- SQL Specialist: database cylinders -->
              <svg v-else-if="agentKey === 'sqlSpecialist'" viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true">
                <ellipse cx="8" cy="4" rx="5" ry="2" stroke="currentColor" stroke-width="1.5"/>
                <path d="M3 4v4c0 1.1 2.2 2 5 2s5-.9 5-2V4" stroke="currentColor" stroke-width="1.5"/>
                <path d="M3 8v4c0 1.1 2.2 2 5 2s5-.9 5-2V8" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              <!-- Deploy Checker: rocket -->
              <svg v-else viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true">
                <path d="M8 1c0 0 5 2.5 5 8.5H3C3 3.5 8 1 8 1z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
                <rect x="5" y="9" width="6" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/>
                <line x1="5" y1="10" x2="3.5" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <line x1="11" y1="10" x2="12.5" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </span>
            <span class="presence-dot" :class="`presence-${presenceStates[agentKey]}`"></span>
          </div>
        </div>

        <!-- Chat Messages -->
        <div class="chat-scroll" ref="chatScrollRef">
          <div
            v-for="(msg, index) in chatMessages"
            :key="msg.id"
            class="chat-card"
            :class="{ 'alert-card': msg.flagged }"
            :style="{ '--msg-index': index }"
          >
            <div v-if="msg.flagged" class="alert-label">⚠ FLAGGED</div>

            <div class="chat-inner">
              <!-- Agent Avatar -->
              <div class="agent-avatar" :class="`agent-${msg.agent}`">
                <!-- Scanner -->
                <svg v-if="msg.agent === 'scanner'" viewBox="0 0 16 16" width="13" height="13" fill="none" aria-hidden="true">
                  <circle cx="8" cy="8" r="6" stroke="white" stroke-width="1.5"/>
                  <circle cx="8" cy="8" r="2" fill="white"/>
                  <line x1="8" y1="8" x2="14" y2="8" stroke="white" stroke-width="1.5"/>
                </svg>
                <!-- Monitor -->
                <svg v-else-if="msg.agent === 'monitor'" viewBox="0 0 16 16" width="13" height="13" fill="none" aria-hidden="true">
                  <polyline points="2,8 5,4 8,12 11,6 14,8" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <!-- Responder -->
                <svg v-else-if="msg.agent === 'responder'" viewBox="0 0 16 16" width="13" height="13" fill="none" aria-hidden="true">
                  <path d="M8 2L2 5v4c0 3.3 2.5 6 6 7 3.5-1 6-3.7 6-7V5L8 2z" stroke="white" stroke-width="1.5"/>
                </svg>
                <!-- Sentinel -->
                <svg v-else-if="msg.agent === 'sentinel'" viewBox="0 0 16 16" width="13" height="13" fill="none" aria-hidden="true">
                  <path d="M8 2L1 14h14L8 2z" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
                  <line x1="8" y1="7" x2="8" y2="10" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
                  <circle cx="8" cy="12.5" r="0.8" fill="white"/>
                </svg>
                <!-- Package Monitor -->
                <svg v-else-if="msg.agent === 'packageMonitor'" viewBox="0 0 16 16" width="13" height="13" fill="none" aria-hidden="true">
                  <rect x="2" y="7" width="12" height="7" rx="1" stroke="white" stroke-width="1.5"/>
                  <polyline points="0.5,7 8,2 15.5,7" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
                  <line x1="8" y1="7" x2="8" y2="14" stroke="white" stroke-width="1.5"/>
                </svg>
                <!-- SQL Specialist -->
                <svg v-else-if="msg.agent === 'sqlSpecialist'" viewBox="0 0 16 16" width="13" height="13" fill="none" aria-hidden="true">
                  <ellipse cx="8" cy="4" rx="5" ry="2" stroke="white" stroke-width="1.5"/>
                  <path d="M3 4v4c0 1.1 2.2 2 5 2s5-.9 5-2V4" stroke="white" stroke-width="1.5"/>
                  <path d="M3 8v4c0 1.1 2.2 2 5 2s5-.9 5-2V8" stroke="white" stroke-width="1.5"/>
                </svg>
                <!-- Deploy Checker -->
                <svg v-else viewBox="0 0 16 16" width="13" height="13" fill="none" aria-hidden="true">
                  <path d="M8 1c0 0 5 2.5 5 8.5H3C3 3.5 8 1 8 1z" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
                  <rect x="5" y="9" width="6" height="4" rx="1" stroke="white" stroke-width="1.5"/>
                  <line x1="5" y1="10" x2="3.5" y2="13" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
                  <line x1="11" y1="10" x2="12.5" y2="13" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </div>

              <!-- Message Body -->
              <div class="msg-body">
                <div class="msg-header-row">
                  <span class="agent-name" :class="`agent-${msg.agent}`">{{ agentDefs[msg.agent].name }}</span>
                  <span class="role-badge" :class="`agent-${msg.agent}`">{{ agentDefs[msg.agent].role }}</span>
                  <span class="msg-time">{{ msg.time }}</span>
                </div>
                <div class="msg-text">
                  <template v-for="(part, pi) in parseMessage(msg.message)" :key="pi">
                    <span v-if="part.type === 'mention'" class="mention">{{ part.value }}</span>
                    <span v-else>{{ part.value }}</span>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>

      </section>
    </div>
  </div>
</template>

<style scoped>
/* ── Agent color tokens (component-scoped, outside brand system) ──────────── */
.stream-root {
  /* Agent identity colors — sourced from component design spec */
  --agent-scanner:         #00D9FF;
  --agent-monitor:         #2ED573;
  --agent-responder:       #FF6B35;
  --agent-sentinel:        #FF4757;
  --agent-package-monitor: #7B61FF;
  --agent-sql-specialist:  #3498DB;
  --agent-deploy-checker:  #FFA502;

  /* Source badge colors — per-source design identity */
  --source-deploy:    #3498DB;
  --source-staging:   #FFA502;
  --source-prod:      #2ED573;
  --source-error:     #FF4757;
  --source-cicd:      #7B61FF;
  --source-migration: #00D9FF;
  --source-monitor:   #FF6B35;
}

/* ── Root Shell ─────────────────────────────────────────────────────────────── */
.stream-root {
  height: 100vh;
  display: grid;
  grid-template-rows: 36px 1fr;
  background: var(--brand-bg);
  font-family: var(--font-body);
  color: var(--brand-text);
  overflow: hidden;
  box-sizing: border-box;
}

/* ── Header ─────────────────────────────────────────────────────────────────── */
.stream-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  background: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
  z-index: 20;
}

.stream-title {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--brand-primary);
  margin: 0;
}

.stream-clock {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--brand-muted);
  letter-spacing: 0.06em;
}

/* ── Content Grid ───────────────────────────────────────────────────────────── */
.content-grid {
  display: grid;
  grid-template-columns: 55fr 45fr;
  overflow: hidden;
  min-height: 0;
}

/* ── Log Column ─────────────────────────────────────────────────────────────── */
.log-column {
  display: grid;
  grid-template-rows: 32px 1fr;
  border-right: 1px solid var(--brand-border);
  overflow: hidden;
  min-height: 0;
}

/* ── Filter Bar ─────────────────────────────────────────────────────────────── */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0 0.625rem;
  background: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
  overflow-x: auto;
  scrollbar-width: none;
  flex-shrink: 0;
}

.filter-bar::-webkit-scrollbar { display: none; }

.filter-pill {
  font-family: var(--font-mono);
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 2px 7px;
  border-radius: 3px;
  border: 1px solid var(--brand-border);
  background: transparent;
  color: var(--brand-muted);
  cursor: pointer;
  white-space: nowrap;
  transition: color var(--duration-fast) var(--easing),
              background var(--duration-fast) var(--easing),
              border-color var(--duration-fast) var(--easing);
  line-height: 1;
}

.filter-pill:hover {
  color: var(--brand-text);
  border-color: var(--brand-muted);
}

.filter-pill.active {
  background: var(--brand-primary);
  border-color: var(--brand-primary);
  color: var(--brand-bg);
}

.filter-pill:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 2px;
}

/* ── Log Scroll ─────────────────────────────────────────────────────────────── */
.log-scroll {
  overflow-y: auto;
  min-height: 0;
  scrollbar-width: thin;
  scrollbar-color: var(--brand-border) transparent;
}

.log-scroll::-webkit-scrollbar { width: 4px; }
.log-scroll::-webkit-scrollbar-track { background: transparent; }
.log-scroll::-webkit-scrollbar-thumb { background: var(--brand-border); border-radius: 2px; }
.log-scroll::-webkit-scrollbar-thumb:hover { background: var(--brand-muted); }

/* ── Log Row ────────────────────────────────────────────────────────────────── */
.log-row {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.22rem 0.75rem;
  min-height: 26px;
  cursor: default;
  animation: logEnter 0.3s var(--easing) both;
  animation-delay: calc(var(--row-index, 0) * 80ms);
  transition: background var(--duration-fast) var(--easing);
}

.log-row.row-even { background: color-mix(in srgb, var(--brand-text) 2%, transparent); }
.log-row:hover    { background: color-mix(in srgb, var(--brand-primary) 4%, transparent); }

/* ── Timestamp ──────────────────────────────────────────────────────────────── */
.log-time {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--brand-muted);
  flex-shrink: 0;
  width: 5.25rem;
  white-space: nowrap;
}

/* ── Source Badges ──────────────────────────────────────────────────────────── */
.log-badge {
  font-family: var(--font-mono);
  font-size: 0.58rem;
  font-weight: 500;
  padding: 1px 5px;
  border-radius: 3px;
  white-space: nowrap;
  flex-shrink: 0;
  letter-spacing: 0.02em;
}

.badge-deploy    { background: color-mix(in srgb, var(--source-deploy)    22%, transparent); color: var(--source-deploy);    border: 1px solid color-mix(in srgb, var(--source-deploy)    38%, transparent); }
.badge-staging   { background: color-mix(in srgb, var(--source-staging)   18%, transparent); color: var(--source-staging);   border: 1px solid color-mix(in srgb, var(--source-staging)   32%, transparent); }
.badge-prod      { background: color-mix(in srgb, var(--source-prod)      18%, transparent); color: var(--source-prod);      border: 1px solid color-mix(in srgb, var(--source-prod)      32%, transparent); }
.badge-error     { background: color-mix(in srgb, var(--source-error)     18%, transparent); color: var(--source-error);     border: 1px solid color-mix(in srgb, var(--source-error)     32%, transparent); }
.badge-ci-cd     { background: color-mix(in srgb, var(--source-cicd)      18%, transparent); color: var(--source-cicd);      border: 1px solid color-mix(in srgb, var(--source-cicd)      32%, transparent); }
.badge-migration { background: color-mix(in srgb, var(--source-migration) 13%, transparent); color: var(--source-migration); border: 1px solid color-mix(in srgb, var(--source-migration) 26%, transparent); }
.badge-monitor   { background: color-mix(in srgb, var(--source-monitor)   18%, transparent); color: var(--source-monitor);   border: 1px solid color-mix(in srgb, var(--source-monitor)   32%, transparent); }

/* ── Severity Dot ───────────────────────────────────────────────────────────── */
.severity-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-info  { background: var(--brand-muted); }
.dot-warn  { background: var(--brand-warning); }
.dot-error { background: var(--brand-error); }

/* ── Severity Label ─────────────────────────────────────────────────────────── */
.log-sev-label {
  font-family: var(--font-mono);
  font-size: 0.58rem;
  color: var(--brand-muted);
  flex-shrink: 0;
  width: 2.8rem;
  letter-spacing: 0.03em;
}

.log-row.severity-warn  .log-sev-label { color: var(--brand-warning); }
.log-row.severity-error .log-sev-label { color: var(--brand-error); }

/* ── Log Message ────────────────────────────────────────────────────────────── */
.log-msg {
  font-size: 0.74rem;
  color: var(--brand-text);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1;
}

.log-row.severity-error .log-msg { color: color-mix(in srgb, var(--brand-error)   70%, var(--brand-text)); }
.log-row.severity-warn  .log-msg { color: color-mix(in srgb, var(--brand-warning) 70%, var(--brand-text)); }

/* ── Chat Column ────────────────────────────────────────────────────────────── */
.chat-column {
  display: grid;
  grid-template-rows: 40px 1fr;
  overflow: hidden;
  min-height: 0;
}

/* ── Presence Bar ───────────────────────────────────────────────────────────── */
.presence-bar {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0 0.75rem;
  background: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
  overflow-x: auto;
  scrollbar-width: none;
}

.presence-bar::-webkit-scrollbar { display: none; }

.presence-agent {
  display: flex;
  align-items: center;
  gap: 2px;
  cursor: default;
  flex-shrink: 0;
}

.agent-icon-wrap {
  display: flex;
  align-items: center;
  line-height: 0;
}

.presence-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Agent color classes — icon color in presence bar */
.agent-icon-wrap.agent-scanner        { color: var(--agent-scanner); }
.agent-icon-wrap.agent-monitor        { color: var(--agent-monitor); }
.agent-icon-wrap.agent-responder      { color: var(--agent-responder); }
.agent-icon-wrap.agent-sentinel       { color: var(--agent-sentinel); }
.agent-icon-wrap.agent-packageMonitor { color: var(--agent-package-monitor); }
.agent-icon-wrap.agent-sqlSpecialist  { color: var(--agent-sql-specialist); }
.agent-icon-wrap.agent-deployChecker  { color: var(--agent-deploy-checker); }

.presence-online { background: var(--brand-success); }
.presence-idle   { background: var(--brand-muted); }
.presence-busy {
  background: var(--brand-error);
  animation: busyPulse 1.5s ease-in-out infinite;
}

/* ── Chat Scroll ────────────────────────────────────────────────────────────── */
.chat-scroll {
  overflow-y: auto;
  min-height: 0;
  padding: 0.25rem 0;
  scrollbar-width: thin;
  scrollbar-color: var(--brand-border) transparent;
}

.chat-scroll::-webkit-scrollbar { width: 4px; }
.chat-scroll::-webkit-scrollbar-track { background: transparent; }
.chat-scroll::-webkit-scrollbar-thumb { background: var(--brand-border); border-radius: 2px; }
.chat-scroll::-webkit-scrollbar-thumb:hover { background: var(--brand-muted); }

/* ── Chat Card ──────────────────────────────────────────────────────────────── */
.chat-card {
  position: relative;
  margin: 0.2rem 0.5rem;
  padding: 0.45rem 0.6rem;
  border-radius: var(--radius-sm);
  background: var(--brand-surface);
  animation: msgEnter 0.3s var(--easing) both;
  animation-delay: calc(var(--msg-index, 0) * 120ms);
  transition: background var(--duration-fast) var(--easing);
}

.chat-card:hover { background: color-mix(in srgb, var(--brand-surface) 90%, var(--brand-bg)); }

/* ── Alert Card ─────────────────────────────────────────────────────────────── */
.alert-card {
  border-left: 3px solid var(--brand-error);
  background: color-mix(in srgb, var(--brand-error) 6%, transparent);
}

.alert-card:hover { background: color-mix(in srgb, var(--brand-error) 9%, transparent); }

.alert-label {
  position: absolute;
  top: 0.35rem;
  right: 0.5rem;
  font-family: var(--font-mono);
  font-size: 0.58rem;
  font-weight: 700;
  color: var(--brand-error);
  letter-spacing: 0.06em;
  pointer-events: none;
}

/* ── Chat Inner ─────────────────────────────────────────────────────────────── */
.chat-inner {
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
}

/* ── Agent Avatar ───────────────────────────────────────────────────────────── */
.agent-avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 0;
}

/* Agent background colors on avatar circles */
.agent-avatar.agent-scanner        { background: var(--agent-scanner); }
.agent-avatar.agent-monitor        { background: var(--agent-monitor); }
.agent-avatar.agent-responder      { background: var(--agent-responder); }
.agent-avatar.agent-sentinel       { background: var(--agent-sentinel); }
.agent-avatar.agent-packageMonitor { background: var(--agent-package-monitor); }
.agent-avatar.agent-sqlSpecialist  { background: var(--agent-sql-specialist); }
.agent-avatar.agent-deployChecker  { background: var(--agent-deploy-checker); }

/* Agent text/border colors on name + role badge */
.agent-name.agent-scanner,        .role-badge.agent-scanner        { color: var(--agent-scanner);         border-color: var(--agent-scanner); }
.agent-name.agent-monitor,        .role-badge.agent-monitor        { color: var(--agent-monitor);         border-color: var(--agent-monitor); }
.agent-name.agent-responder,      .role-badge.agent-responder      { color: var(--agent-responder);       border-color: var(--agent-responder); }
.agent-name.agent-sentinel,       .role-badge.agent-sentinel       { color: var(--agent-sentinel);        border-color: var(--agent-sentinel); }
.agent-name.agent-packageMonitor, .role-badge.agent-packageMonitor { color: var(--agent-package-monitor); border-color: var(--agent-package-monitor); }
.agent-name.agent-sqlSpecialist,  .role-badge.agent-sqlSpecialist  { color: var(--agent-sql-specialist);  border-color: var(--agent-sql-specialist); }
.agent-name.agent-deployChecker,  .role-badge.agent-deployChecker  { color: var(--agent-deploy-checker);  border-color: var(--agent-deploy-checker); }

/* ── Message Body ───────────────────────────────────────────────────────────── */
.msg-body {
  flex: 1;
  min-width: 0;
}

.msg-header-row {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  margin-bottom: 0.2rem;
  flex-wrap: wrap;
}

.agent-name {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
  white-space: nowrap;
  /* color set per-agent via .agent-{key} class */
}

.role-badge {
  font-family: var(--font-mono);
  font-size: 0.55rem;
  font-weight: 400;
  padding: 0px 4px;
  border-radius: 3px;
  border: 1px solid;
  opacity: 0.8;
  white-space: nowrap;
  letter-spacing: 0.02em;
  /* color + border-color set per-agent via .agent-{key} class */
}

.msg-time {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  color: var(--brand-muted);
  margin-left: auto;
  white-space: nowrap;
}

.msg-text {
  font-size: 0.76rem;
  line-height: 1.45;
  color: var(--brand-text);
  word-break: break-word;
}

/* ── @mentions ──────────────────────────────────────────────────────────────── */
.mention {
  display: inline;
  background: color-mix(in srgb, var(--brand-primary) 12%, transparent);
  color: var(--brand-primary);
  border-radius: 3px;
  padding: 0 3px;
  font-size: 0.74rem;
  font-weight: 700;
}

/* ── Keyframes ──────────────────────────────────────────────────────────────── */
@keyframes logEnter {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}

@keyframes msgEnter {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes busyPulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.25; }
}

/* ── Reduced Motion ─────────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .log-row,
  .chat-card,
  .presence-busy {
    animation: none !important;
    transition: none !important;
  }
}
</style>

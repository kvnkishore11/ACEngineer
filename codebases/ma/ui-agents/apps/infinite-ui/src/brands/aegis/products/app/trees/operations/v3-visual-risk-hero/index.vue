<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/app/operations/v3-visual-risk-hero
// Layout: large full-width risk overview hero (always visible) +
//         4 accordion sections below. Containment open by default.
// Variant differentiator: the hero IS the page identity — it dominates
// the viewport before any section is expanded. v1 is timeline-centric,
// v2 is table-heavy; v3 is purely visual-first.

// ── Types ─────────────────────────────────────────────────────────
interface RiskSystem {
  id: number
  name: string
  riskScore: number   // 0–100, maps to left% position on spectrum
  severity: 'critical' | 'high' | 'medium' | 'secured'
}

interface ContainedSystem {
  id: number
  name: string
  isolatedAt: string
  reason: string
  status: 'ISOLATED' | 'MONITORING' | 'CLEARED'
}

interface RespondingAgent {
  name: string
  task: string
  since: string
  status: 'active' | 'monitoring'
}

interface Vuln {
  id: string
  name: string
  score: number
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  affectedSystems: number
  detectedAt: string
  status: 'OPEN' | 'IN_PROGRESS' | 'PATCHED' | 'MITIGATED'
}

interface TimelineNode {
  stage: 'DETECTION' | 'INVESTIGATION' | 'CONTAINMENT' | 'RESOLUTION'
  agent: string
  action: string
  timestamp: string
  duration: string | null
}

interface AttackPattern {
  name: string
  count: number
  pct: number
  colorVar: string
}

// ── Section accordion state ────────────────────────────────────────
const sections = reactive({
  containment: true,   // open by default — user requirement
  intel:       false,
  timeline:    false,
  patterns:    false,
})

// ── Risk systems data (20 systems) ────────────────────────────────
const riskSystems: RiskSystem[] = [
  { id: 1,  name: 'api-gateway-01',      riskScore: 94, severity: 'critical' },
  { id: 2,  name: 'orchestrator-02',     riskScore: 87, severity: 'critical' },
  { id: 3,  name: 'llm-worker-04',       riskScore: 91, severity: 'critical' },
  { id: 4,  name: 'fine-tune-03',        riskScore: 82, severity: 'critical' },
  { id: 5,  name: 'llm-worker-07',       riskScore: 73, severity: 'high'     },
  { id: 6,  name: 'api-gateway-02',      riskScore: 66, severity: 'high'     },
  { id: 7,  name: 'rate-limiter-01',     riskScore: 71, severity: 'high'     },
  { id: 8,  name: 'log-aggregator',      riskScore: 68, severity: 'high'     },
  { id: 9,  name: 'llm-worker-02',       riskScore: 55, severity: 'medium'   },
  { id: 10, name: 'auth-service',        riskScore: 48, severity: 'medium'   },
  { id: 11, name: 'vector-db-01',        riskScore: 43, severity: 'medium'   },
  { id: 12, name: 'agent-runner-05',     riskScore: 37, severity: 'medium'   },
  { id: 13, name: 'plugin-sandbox',      riskScore: 31, severity: 'medium'   },
  { id: 14, name: 'cache-layer-01',      riskScore: 21, severity: 'secured'  },
  { id: 15, name: 'object-store-02',     riskScore: 18, severity: 'secured'  },
  { id: 16, name: 'scheduler-01',        riskScore: 14, severity: 'secured'  },
  { id: 17, name: 'pkg-registry-mirror', riskScore: 12, severity: 'secured'  },
  { id: 18, name: 'llm-worker-01',       riskScore: 9,  severity: 'secured'  },
  { id: 19, name: 'static-cdn',          riskScore: 6,  severity: 'secured'  },
  { id: 20, name: 'monitoring-db-01',    riskScore: 4,  severity: 'secured'  },
]

// ── Risk counts (derived) ─────────────────────────────────────────
const riskCounts = computed(() => ({
  critical: riskSystems.filter(s => s.severity === 'critical').length,
  high:     riskSystems.filter(s => s.severity === 'high').length,
  medium:   riskSystems.filter(s => s.severity === 'medium').length,
  secured:  riskSystems.filter(s => s.severity === 'secured').length,
}))

// ── Containment data ───────────────────────────────────────────────
const containedSystems: ContainedSystem[] = [
  {
    id: 1,
    name: 'api-gateway-01',
    isolatedAt: '14 min ago',
    reason: 'Prompt injection vector detected in ingress traffic',
    status: 'ISOLATED',
  },
  {
    id: 2,
    name: 'llm-worker-04',
    isolatedAt: '9 min ago',
    reason: 'Jailbreak attempt against system prompt',
    status: 'MONITORING',
  },
  {
    id: 3,
    name: 'orchestrator-02',
    isolatedAt: '41 min ago',
    reason: 'Privilege escalation on agent token resolved',
    status: 'CLEARED',
  },
]

const respondingAgents: RespondingAgent[] = [
  {
    name: 'Responder',
    task: 'Isolating api-gateway-01 from service mesh',
    since: '2 min ago',
    status: 'active',
  },
  {
    name: 'Scanner',
    task: 'Sweeping llm-worker cluster for residual payloads',
    since: '7 min ago',
    status: 'active',
  },
  {
    name: 'Monitor',
    task: 'Passive traffic observation on rate-limiter-01',
    since: '14 min ago',
    status: 'monitoring',
  },
]

// ── Vulnerability data (8 CVE-style entries) ───────────────────────
const vulns: Vuln[] = [
  {
    id: 'CVE-2024-4891',
    name: 'Prompt injection via system prompt override',
    score: 9.4,
    severity: 'CRITICAL',
    affectedSystems: 3,
    detectedAt: '14 min ago',
    status: 'IN_PROGRESS',
  },
  {
    id: 'CVE-2024-4782',
    name: 'Privilege escalation via agent token reuse',
    score: 9.1,
    severity: 'CRITICAL',
    affectedSystems: 1,
    detectedAt: '41 min ago',
    status: 'IN_PROGRESS',
  },
  {
    id: 'CVE-2024-4665',
    name: 'Model poisoning probe — fine-tune endpoint',
    score: 8.7,
    severity: 'HIGH',
    affectedSystems: 2,
    detectedAt: '1h ago',
    status: 'OPEN',
  },
  {
    id: 'CVE-2024-4601',
    name: 'Data exfiltration via malformed tool call',
    score: 8.2,
    severity: 'HIGH',
    affectedSystems: 1,
    detectedAt: '2h ago',
    status: 'OPEN',
  },
  {
    id: 'CVE-2024-4490',
    name: 'Context window overflow probe — token budget',
    score: 6.5,
    severity: 'MEDIUM',
    affectedSystems: 4,
    detectedAt: '3h ago',
    status: 'PATCHED',
  },
  {
    id: 'CVE-2024-4423',
    name: 'Unverified plugin execution in sandbox',
    score: 5.8,
    severity: 'MEDIUM',
    affectedSystems: 1,
    detectedAt: '4h ago',
    status: 'MITIGATED',
  },
  {
    id: 'CVE-2024-4311',
    name: 'Repeated auth failure — service account abuse',
    score: 5.1,
    severity: 'MEDIUM',
    affectedSystems: 2,
    detectedAt: '5h ago',
    status: 'PATCHED',
  },
  {
    id: 'CVE-2024-4200',
    name: 'Unrecognized tool invocation — agent-runner',
    score: 3.2,
    severity: 'LOW',
    affectedSystems: 1,
    detectedAt: '8h ago',
    status: 'MITIGATED',
  },
]

// ── Timeline data ──────────────────────────────────────────────────
const timeline: TimelineNode[] = [
  {
    stage: 'DETECTION',
    agent: 'Scanner',
    action: 'Identified prompt injection payload in api-gateway-01 ingress traffic. Pattern matched known jailbreak vector from threat intelligence database.',
    timestamp: '14:23:07',
    duration: null,
  },
  {
    stage: 'INVESTIGATION',
    agent: 'Monitor',
    action: 'Correlated attack signature across 3 API gateway nodes. Identified source IP range and payload variant family. Confirmed active campaign, not isolated probe.',
    timestamp: '14:25:41',
    duration: '2m 34s',
  },
  {
    stage: 'CONTAINMENT',
    agent: 'Responder',
    action: 'Isolated api-gateway-01 from service mesh. Rate-limited source IP range. Deployed updated WAF ruleset to all gateway nodes. Lateral movement blocked.',
    timestamp: '14:28:19',
    duration: '2m 38s',
  },
  {
    stage: 'RESOLUTION',
    agent: 'Patcher',
    action: 'Applied security patch to all affected gateway nodes. Verified payload rejection across full request corpus. Restored full service mesh connectivity.',
    timestamp: '14:51:03',
    duration: '22m 44s',
  },
]

// ── Attack patterns data ───────────────────────────────────────────
const attackPatterns: AttackPattern[] = [
  { name: 'Prompt Injection',     count: 47, pct: 38, colorVar: '--brand-error'     },
  { name: 'Data Exfiltration',    count: 31, pct: 25, colorVar: '--brand-accent'    },
  { name: 'Privilege Escalation', count: 28, pct: 23, colorVar: '--brand-secondary' },
  { name: 'Model Poisoning',      count: 17, pct: 14, colorVar: '--brand-primary'   },
]

// ── Token helpers ──────────────────────────────────────────────────
function severityToken(score: number): string {
  if (score >= 9) return 'var(--brand-error)'
  if (score >= 7) return 'var(--brand-accent)'
  if (score >= 4) return 'var(--brand-secondary)'
  return 'var(--brand-primary)'
}

function stageToken(stage: string): string {
  const map: Record<string, string> = {
    DETECTION:     'var(--brand-error)',
    INVESTIGATION: 'var(--brand-accent)',
    CONTAINMENT:   'var(--brand-secondary)',
    RESOLUTION:    'var(--brand-primary)',
  }
  return map[stage] ?? 'var(--brand-muted)'
}

function containmentToken(status: ContainedSystem['status']): string {
  if (status === 'ISOLATED')   return 'var(--brand-error)'
  if (status === 'MONITORING') return 'var(--brand-secondary)'
  return 'var(--brand-primary)'
}

function remediationToken(status: Vuln['status']): string {
  if (status === 'OPEN')       return 'var(--brand-error)'
  if (status === 'IN_PROGRESS') return 'var(--brand-accent)'
  return 'var(--brand-primary)'
}

function riskSystemToken(severity: RiskSystem['severity']): string {
  if (severity === 'critical') return 'var(--brand-error)'
  if (severity === 'high')     return 'var(--brand-accent)'
  if (severity === 'medium')   return 'var(--brand-secondary)'
  return 'var(--brand-primary)'
}

// ── Mount ─────────────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  nextTick(() => {
    isMounted.value = true
  })
})

// No setInterval in this component — no cleanup needed
onUnmounted(() => {
  // intentionally empty — no timers to clear
})
</script>

<template>
  <div
    class="page"
    :class="{ 'is-mounted': isMounted }"
    aria-label="Aegis Security Operations and Intelligence — Visual Risk Overview"
  >
    <!-- ── SR-only page title (heading hierarchy anchor) ────────── -->
    <h1 class="sr-only">Aegis Security Operations and Intelligence</h1>

    <!-- ── Page header ──────────────────────────────────────────── -->
    <header class="page-header" role="region" aria-label="Operations page header">
      <div class="page-inner page-header__inner">
        <div class="page-header__brand">
          <span class="page-header__logo">AEGIS</span>
          <span class="page-header__sep" aria-hidden="true">/</span>
          <span class="page-header__product">OPERATIONS</span>
        </div>
        <div class="page-header__meta" aria-label="Risk summary">
          <span class="page-header__live-dot" aria-hidden="true"></span>
          <span class="page-header__live-label">Live</span>
        </div>
      </div>
    </header>

    <!-- ── Main content ─────────────────────────────────────────── -->
    <main class="page-main" role="main">
      <div class="page-inner">

        <!-- ══════════════════════════════════════════════
             RISK OVERVIEW HERO — always visible, dominant
             ══════════════════════════════════════════════ -->
        <section class="risk-hero" aria-label="Risk overview">
          <div class="risk-hero__header">
            <span class="risk-hero__title">Risk Overview</span>
            <span class="risk-hero__subtitle">{{ riskSystems.length }} systems monitored</span>
          </div>

          <!-- Spectrum gradient bar -->
          <div
            class="risk-spectrum-wrap"
            role="img"
            aria-label="Risk spectrum from critical (red) to secured (white)"
          >
            <div class="risk-spectrum" aria-hidden="true"></div>

            <!-- System dots positioned along the spectrum -->
            <div class="risk-dots-row" aria-hidden="true">
              <div
                v-for="sys in riskSystems"
                :key="sys.id"
                class="risk-dot"
                :class="`risk-dot--${sys.severity}`"
                :style="{ left: (100 - sys.riskScore) + '%' }"
                :title="sys.name"
              ></div>
            </div>

            <!-- Axis labels -->
            <div class="risk-axis" aria-hidden="true">
              <span class="risk-axis__label risk-axis__label--left">Critical</span>
              <span class="risk-axis__label risk-axis__label--right">Secured</span>
            </div>
          </div>

          <!-- System list — accessible, uses aria-label on each item -->
          <ul class="risk-system-list sr-only" aria-label="System risk levels">
            <li
              v-for="sys in riskSystems"
              :key="sys.id"
            >{{ sys.name }}: {{ sys.severity }}, risk score {{ sys.riskScore }}</li>
          </ul>

          <!-- Summary count pills -->
          <div class="risk-summary" role="list" aria-label="Risk distribution by severity">
            <div class="risk-pill risk-pill--critical" role="listitem">
              <span
                class="risk-pill__count"
                :aria-label="`${riskCounts.critical} critical systems`"
              >{{ riskCounts.critical }}</span>
              <span class="risk-pill__label">Critical</span>
            </div>
            <div class="risk-pill risk-pill--high" role="listitem">
              <span
                class="risk-pill__count"
                :aria-label="`${riskCounts.high} high-risk systems`"
              >{{ riskCounts.high }}</span>
              <span class="risk-pill__label">High</span>
            </div>
            <div class="risk-pill risk-pill--medium" role="listitem">
              <span
                class="risk-pill__count"
                :aria-label="`${riskCounts.medium} medium-risk systems`"
              >{{ riskCounts.medium }}</span>
              <span class="risk-pill__label">Medium</span>
            </div>
            <div class="risk-pill risk-pill--secured" role="listitem">
              <span
                class="risk-pill__count"
                :aria-label="`${riskCounts.secured} secured systems`"
              >{{ riskCounts.secured }}</span>
              <span class="risk-pill__label">Secured</span>
            </div>
          </div>
        </section>

        <!-- ══════════════════════════════════════════════
             ACCORDION SECTIONS
             ══════════════════════════════════════════════ -->
        <div class="accordions" role="list" aria-label="Operations detail sections">

          <!-- ── 1. Containment Status (open by default) ──────── -->
          <section
            class="expand-section"
            :class="{ 'is-open': sections.containment }"
            role="listitem"
            aria-label="Containment status section"
          >
            <button
              type="button"
              class="expand-toggle"
              id="toggle-containment"
              :aria-expanded="sections.containment"
              aria-controls="panel-containment"
              @click="sections.containment = !sections.containment"
            >
              <span class="expand-toggle__icon" aria-hidden="true">›</span>
              <span class="expand-toggle__label">Containment Status</span>
              <span class="expand-toggle__count" aria-hidden="true">
                {{ containedSystems.filter(s => s.status === 'ISOLATED').length }} isolated
                · {{ respondingAgents.filter(a => a.status === 'active').length }} responding
              </span>
            </button>
            <div
              id="panel-containment"
              class="expand-panel"
              role="region"
              aria-labelledby="toggle-containment"
            >
              <div class="expand-panel__inner">
                <div class="containment-grid">

                  <!-- A: Isolated systems -->
                  <div class="containment-col">
                    <h2 class="subsection-title">Isolated Systems</h2>
                    <ul class="contained-list" role="list" aria-label="Isolated systems">
                      <li
                        v-for="sys in containedSystems"
                        :key="sys.id"
                        class="contained-row"
                        :class="`contained-row--${sys.status.toLowerCase()}`"
                        role="listitem"
                        :aria-label="`${sys.name}: ${sys.status}, isolated ${sys.isolatedAt}`"
                      >
                        <div class="contained-row__body">
                          <span class="contained-name">{{ sys.name }}</span>
                          <span class="contained-reason">{{ sys.reason }}</span>
                          <span class="contained-time">{{ sys.isolatedAt }}</span>
                        </div>
                        <span
                          class="stage-badge"
                          :style="{ backgroundColor: containmentToken(sys.status) }"
                        >{{ sys.status }}</span>
                      </li>
                    </ul>
                  </div>

                  <!-- B: Responding agents -->
                  <div class="containment-col">
                    <h2 class="subsection-title">Responding Agents</h2>
                    <ul class="agent-list" role="list" aria-label="Active responding agents">
                      <li
                        v-for="agent in respondingAgents"
                        :key="agent.name"
                        class="agent-row"
                        :class="`agent-row--${agent.status}`"
                        role="listitem"
                        :aria-label="`${agent.name}: ${agent.task}, since ${agent.since}`"
                      >
                        <span
                          class="agent-status-dot"
                          :class="`agent-dot--${agent.status}`"
                          aria-hidden="true"
                        ></span>
                        <div class="agent-body">
                          <span class="agent-name">{{ agent.name }}</span>
                          <span class="agent-task">{{ agent.task }}</span>
                          <span class="agent-since">{{ agent.since }}</span>
                        </div>
                      </li>
                    </ul>
                  </div>

                </div><!-- /containment-grid -->
              </div>
            </div>
          </section>

          <!-- ── 2. Threat Intelligence (collapsed) ───────────── -->
          <section
            class="expand-section"
            :class="{ 'is-open': sections.intel }"
            role="listitem"
            aria-label="Threat intelligence section"
          >
            <button
              type="button"
              class="expand-toggle"
              id="toggle-intel"
              :aria-expanded="sections.intel"
              aria-controls="panel-intel"
              @click="sections.intel = !sections.intel"
            >
              <span class="expand-toggle__icon" aria-hidden="true">›</span>
              <span class="expand-toggle__label">Threat Intelligence</span>
              <span class="expand-toggle__count" aria-hidden="true">
                {{ vulns.filter(v => v.status === 'OPEN' || v.status === 'IN_PROGRESS').length }} active ·
                {{ vulns.length }} total CVEs
              </span>
            </button>
            <div
              id="panel-intel"
              class="expand-panel"
              role="region"
              aria-labelledby="toggle-intel"
            >
              <div class="expand-panel__inner">
                <ul class="vuln-grid" role="list" aria-label="Vulnerability entries">
                  <li
                    v-for="vuln in vulns"
                    :key="vuln.id"
                    class="vuln-card"
                    role="listitem"
                    :aria-label="`${vuln.id}: ${vuln.name}, score ${vuln.score}, ${vuln.affectedSystems} affected systems, status ${vuln.status}`"
                    :style="{ borderLeftColor: severityToken(vuln.score) }"
                  >
                    <div class="vuln-card__top">
                      <div class="vuln-card__id-row">
                        <span class="vuln-id">{{ vuln.id }}</span>
                        <span
                          class="stage-badge vuln-status-badge"
                          :style="{ backgroundColor: remediationToken(vuln.status) }"
                        >{{ vuln.status }}</span>
                      </div>
                      <span
                        class="vuln-score"
                        :style="{ color: severityToken(vuln.score) }"
                        :aria-label="`Severity score ${vuln.score} out of 10`"
                      >{{ vuln.score }}</span>
                    </div>

                    <p class="vuln-name">{{ vuln.name }}</p>

                    <div class="vuln-meta">
                      <span
                        class="vuln-meta__item"
                        :aria-label="`${vuln.affectedSystems} affected systems`"
                      >
                        <span class="vuln-meta__value">{{ vuln.affectedSystems }}</span>
                        <span class="vuln-meta__label">Systems</span>
                      </span>
                      <span class="vuln-meta__item">
                        <span class="vuln-meta__value">{{ vuln.detectedAt }}</span>
                        <span class="vuln-meta__label">Detected</span>
                      </span>
                      <span class="vuln-meta__item">
                        <span class="vuln-meta__value vuln-sev-label">{{ vuln.severity }}</span>
                        <span class="vuln-meta__label">Severity</span>
                      </span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </section>

          <!-- ── 3. Incident Response Timeline (collapsed) ──────── -->
          <section
            class="expand-section"
            :class="{ 'is-open': sections.timeline }"
            role="listitem"
            aria-label="Incident response timeline section"
          >
            <button
              type="button"
              class="expand-toggle"
              id="toggle-timeline"
              :aria-expanded="sections.timeline"
              aria-controls="panel-timeline"
              @click="sections.timeline = !sections.timeline"
            >
              <span class="expand-toggle__icon" aria-hidden="true">›</span>
              <span class="expand-toggle__label">Incident Response Timeline</span>
              <span class="expand-toggle__count" aria-hidden="true">
                {{ timeline.length }} stages · Active incident
              </span>
            </button>
            <div
              id="panel-timeline"
              class="expand-panel"
              role="region"
              aria-labelledby="toggle-timeline"
            >
              <div class="expand-panel__inner">
                <div class="timeline-incident-label">
                  <span class="timeline-incident-id">INC-2024-0047</span>
                  <span class="timeline-incident-desc">Prompt injection campaign — api-gateway cluster</span>
                </div>

                <ol class="timeline" role="list" aria-label="Incident response stages">
                  <li
                    v-for="(node, idx) in timeline"
                    :key="node.stage"
                    class="timeline-node"
                    :class="`timeline-node--${node.stage.toLowerCase()}`"
                    role="listitem"
                    :aria-label="`${node.stage} stage: ${node.agent} — ${node.action}`"
                  >
                    <!-- Left: dot + connector -->
                    <div class="timeline-node__track" aria-hidden="true">
                      <div
                        class="timeline-dot"
                        :style="{ backgroundColor: stageToken(node.stage) }"
                      ></div>
                      <div
                        v-if="idx < timeline.length - 1"
                        class="timeline-connector"
                      ></div>
                    </div>

                    <!-- Right: content card -->
                    <div
                      class="timeline-card"
                      :style="{ borderLeftColor: stageToken(node.stage) }"
                    >
                      <div class="timeline-card__header">
                        <span
                          class="stage-badge"
                          :style="{ backgroundColor: stageToken(node.stage) }"
                        >{{ node.stage }}</span>
                        <span class="timeline-agent">{{ node.agent }}</span>
                        <div class="timeline-times">
                          <span
                            class="timeline-ts"
                            :aria-label="`Timestamp ${node.timestamp}`"
                          >{{ node.timestamp }}</span>
                          <span
                            v-if="node.duration"
                            class="timeline-dur"
                            :aria-label="`Duration ${node.duration}`"
                          >+{{ node.duration }}</span>
                        </div>
                      </div>
                      <p class="timeline-action">{{ node.action }}</p>
                    </div>
                  </li>
                </ol>
              </div>
            </div>
          </section>

          <!-- ── 4. Attack Pattern Categories (collapsed) ───────── -->
          <section
            class="expand-section"
            :class="{ 'is-open': sections.patterns }"
            role="listitem"
            aria-label="Attack pattern categories section"
          >
            <button
              type="button"
              class="expand-toggle"
              id="toggle-patterns"
              :aria-expanded="sections.patterns"
              aria-controls="panel-patterns"
              @click="sections.patterns = !sections.patterns"
            >
              <span class="expand-toggle__icon" aria-hidden="true">›</span>
              <span class="expand-toggle__label">Attack Pattern Categories</span>
              <span class="expand-toggle__count" aria-hidden="true">
                {{ attackPatterns.reduce((s, p) => s + p.count, 0) }} total detections
              </span>
            </button>
            <div
              id="panel-patterns"
              class="expand-panel"
              role="region"
              aria-labelledby="toggle-patterns"
            >
              <div class="expand-panel__inner">
                <ul class="patterns-list" role="list" aria-label="Attack vector frequency breakdown">
                  <li
                    v-for="pattern in attackPatterns"
                    :key="pattern.name"
                    class="pattern-row"
                    role="listitem"
                    :aria-label="`${pattern.name}: ${pattern.count} detections, ${pattern.pct}% of total`"
                  >
                    <span class="pattern-name">{{ pattern.name }}</span>
                    <div
                      class="pattern-track"
                      :aria-label="`${pattern.pct}% of attack patterns`"
                      aria-hidden="true"
                    >
                      <div
                        class="pattern-bar"
                        :style="{
                          width: pattern.pct + '%',
                          backgroundColor: `var(${pattern.colorVar})`,
                        }"
                      ></div>
                    </div>
                    <span class="pattern-pct">{{ pattern.pct }}%</span>
                    <span
                      class="pattern-count"
                      :aria-label="`${pattern.count} detections`"
                    >{{ pattern.count }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </section>

        </div><!-- /accordions -->
      </div><!-- /page-inner -->
    </main>
  </div>
</template>

<style scoped>
/* ── Reset ────────────────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* ── Page root ────────────────────────────────────────────────────── */
.page {
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

/* ── Layout wrapper ───────────────────────────────────────────────── */
.page-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 calc(var(--space-unit) * 6);
}

/* ── Page header ──────────────────────────────────────────────────── */
.page-header {
  background-color: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
  position: sticky;
  top: 0;
  z-index: 20;
}

.page-header__inner {
  height: calc(var(--space-unit) * 14);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-header__brand {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.page-header__logo {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
}

.page-header__sep {
  font-family: var(--font-mono);
  color: var(--brand-border);
}

.page-header__product {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.page-header__meta {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.page-header__live-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  background-color: var(--brand-error);
  animation: pulse 1.5s var(--easing) infinite;
}

.page-header__live-label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── Main ─────────────────────────────────────────────────────────── */
.page-main {
  padding: calc(var(--space-unit) * 6) 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 4);
}

/* ── Risk Hero ────────────────────────────────────────────────────── */
.risk-hero {
  background: linear-gradient(160deg, var(--brand-surface), color-mix(in srgb, var(--brand-surface) 80%, var(--brand-accent) 4%));
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: calc(var(--space-unit) * 8);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 5);
}

.risk-hero__header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 4);
}

.risk-hero__title {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.risk-hero__subtitle {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

/* Spectrum gradient bar + dots container */
.risk-spectrum-wrap {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.risk-spectrum {
  width: 100%;
  height: calc(var(--space-unit) * 3);
  border-radius: var(--radius-sm);
  background: linear-gradient(
    to right,
    var(--brand-error),
    var(--brand-accent) 35%,
    var(--brand-secondary) 65%,
    var(--brand-primary)
  );
}

/* System dots row — relative container, dots use absolute % left */
.risk-dots-row {
  position: relative;
  height: calc(var(--space-unit) * 4);
  width: 100%;
}

.risk-dot {
  position: absolute;
  width: calc(var(--space-unit) * 3);
  height: calc(var(--space-unit) * 3);
  border-radius: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid var(--brand-bg-secondary);
  transition: transform var(--duration-fast) var(--easing);
}

.risk-dot:hover {
  transform: translate(-50%, -50%) scale(1.4);
  z-index: 2;
}

.risk-dot--critical { background-color: var(--brand-error);     }
.risk-dot--high     { background-color: var(--brand-accent);    }
.risk-dot--medium   { background-color: var(--brand-secondary); }
.risk-dot--secured  { background-color: var(--brand-primary);   }

/* Axis labels */
.risk-axis {
  display: flex;
  justify-content: space-between;
}

.risk-axis__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Summary pills */
.risk-summary {
  display: flex;
  flex-wrap: wrap;
  gap: calc(var(--space-unit) * 3);
}

.risk-pill {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
  border-radius: var(--radius-md);
  min-width: 0;
}

.risk-pill--critical {
  background-color: color-mix(in srgb, var(--brand-error) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-error) 40%, transparent);
}
.risk-pill--high {
  background-color: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-accent) 40%, transparent);
}
.risk-pill--medium {
  background-color: color-mix(in srgb, var(--brand-secondary) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-secondary) 40%, transparent);
}
.risk-pill--secured {
  background-color: color-mix(in srgb, var(--brand-primary) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-primary) 30%, transparent);
}

.risk-pill__count {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brand-text);
}

.risk-pill__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── Accordion container ──────────────────────────────────────────── */
.accordions {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

/* ── Expand section shell ─────────────────────────────────────────── */
.expand-section {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

/* ── Toggle button ────────────────────────────────────────────────── */
.expand-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 6);
  background-color: var(--brand-bg-secondary);
  border: none;
  border-bottom: 1px solid var(--brand-border);
  color: var(--brand-text);
  font-family: var(--font-body);
  font-size: 1rem;
  cursor: pointer;
  text-align: left;
  transition: background-color var(--duration-fast) var(--easing);
}

/* Closed state: no bottom border visible outside the button */
.expand-section:not(.is-open) .expand-toggle {
  border-bottom-color: transparent;
}

.expand-toggle:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 70%, var(--brand-bg-secondary));
}

.expand-toggle:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: -2px;
}

.expand-toggle__icon {
  font-size: 1rem;
  line-height: 1;
  color: var(--brand-muted);
  transition: transform var(--duration-normal) var(--easing);
  flex-shrink: 0;
}

.is-open .expand-toggle__icon {
  transform: rotate(90deg);
}

.expand-toggle__label {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  flex: 1;
  color: var(--brand-text);
}

.expand-toggle__count {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  flex-shrink: 0;
}

/* ── Panel collapse/expand ────────────────────────────────────────── */
.expand-panel {
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--duration-slow) var(--easing);
}

.is-open .expand-panel {
  max-height: 9999px;
}

.expand-panel__inner {
  padding: calc(var(--space-unit) * 6);
}

/* ── Shared stage badge ───────────────────────────────────────────── */
/* Text is always brand-bg for contrast on all colored backgrounds:
   brand-error: 5.33:1, brand-accent: 4.74:1, brand-secondary: 5.78:1,
   brand-primary: 17.39:1 — all pass WCAG AA. */
.stage-badge {
  display: inline-flex;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2);
  border-radius: var(--radius-sm);
  color: var(--brand-bg);
  flex-shrink: 0;
  white-space: nowrap;
}

/* ── Containment: two-col grid ────────────────────────────────────── */
.containment-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 8);
  align-items: start;
}

.subsection-title {
  font-family: var(--font-heading);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin: 0 0 calc(var(--space-unit) * 4);
}

/* Contained systems list */
.contained-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.contained-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  border-left: 3px solid transparent;
  transition: background-color var(--duration-fast) var(--easing);
}

.contained-row--isolated {
  border-left-color: var(--brand-error);
}
.contained-row--monitoring {
  border-left-color: var(--brand-secondary);
}
.contained-row--cleared {
  border-left-color: var(--brand-primary);
}

.contained-row__body {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
  min-width: 0;
  flex: 1;
}

.contained-name {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.contained-reason {
  font-family: var(--font-body);
  font-size: 0.75rem;
  color: var(--brand-text);
  line-height: 1.4;
}

.contained-time {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);
}

/* Responding agents list */
.agent-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.agent-row {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  background-color: var(--brand-bg-secondary);
  border-radius: var(--radius-md);
  transition: background-color var(--duration-fast) var(--easing);
}

.agent-status-dot {
  width: calc(var(--space-unit) * 2.5);
  height: calc(var(--space-unit) * 2.5);
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: calc(var(--space-unit) * 0.5);
}

.agent-dot--active {
  background-color: var(--brand-error);
  animation: pulse 1.5s var(--easing) infinite;
}

.agent-dot--monitoring {
  background-color: var(--brand-secondary);
}

.agent-body {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
  min-width: 0;
}

.agent-name {
  font-family: var(--font-heading);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-text);
}

.agent-task {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: var(--brand-text);
  line-height: 1.4;
}

.agent-since {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  color: var(--brand-muted);
}

/* ── Threat Intelligence: vuln cards grid ────────────────────────── */
.vuln-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: calc(var(--space-unit) * 4);
}

.vuln-card {
  background-color: var(--brand-bg-secondary);
  border: 1px solid var(--brand-border);
  border-left: 3px solid transparent;
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 4);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
  transition: background-color var(--duration-fast) var(--easing);
}

.vuln-card:hover {
  background-color: color-mix(in srgb, var(--brand-surface) 80%, var(--brand-bg-secondary));
}

.vuln-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 3);
}

.vuln-card__id-row {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.vuln-id {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--brand-text);
}

.vuln-status-badge {
  align-self: flex-start;
}

.vuln-score {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
  flex-shrink: 0;
}

.vuln-name {
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--brand-text);
  line-height: 1.5;
  margin: 0;
}

.vuln-meta {
  display: flex;
  gap: calc(var(--space-unit) * 5);
  border-top: 1px solid var(--brand-border);
  padding-top: calc(var(--space-unit) * 3);
}

.vuln-meta__item {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.vuln-meta__value {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
  line-height: 1;
}

.vuln-sev-label {
  font-size: 0.6875rem;
  letter-spacing: 0.05em;
}

.vuln-meta__label {
  font-family: var(--font-mono);
  font-size: 0.5625rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* ── Incident Timeline ────────────────────────────────────────────── */
.timeline-incident-label {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 3);
  margin-bottom: calc(var(--space-unit) * 6);
  padding-bottom: calc(var(--space-unit) * 4);
  border-bottom: 1px solid var(--brand-border);
}

.timeline-incident-id {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-accent);
}

.timeline-incident-desc {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--brand-text);
}

.timeline {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.timeline-node {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 4);
}

/* Left track: dot + vertical connector */
.timeline-node__track {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  width: calc(var(--space-unit) * 3);
}

.timeline-dot {
  width: calc(var(--space-unit) * 3);
  height: calc(var(--space-unit) * 3);
  border-radius: 50%;
  flex-shrink: 0;
  z-index: 1;
}

.timeline-connector {
  width: 2px;
  flex: 1;
  min-height: calc(var(--space-unit) * 8);
  background-color: var(--brand-border);
  margin: calc(var(--space-unit) * 1) 0;
}

/* Right card */
.timeline-card {
  flex: 1;
  background-color: var(--brand-bg-secondary);
  border: 1px solid var(--brand-border);
  border-left: 3px solid transparent;
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 4);
  margin-bottom: calc(var(--space-unit) * 4);
}

.timeline-card__header {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  margin-bottom: calc(var(--space-unit) * 3);
  flex-wrap: wrap;
}

.timeline-agent {
  font-family: var(--font-heading);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-text);
  flex: 1;
}

.timeline-times {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  flex-shrink: 0;
}

.timeline-ts {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
}

.timeline-dur {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
}

.timeline-action {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--brand-text);
  line-height: 1.6;
  margin: 0;
}

/* ── Attack Patterns ──────────────────────────────────────────────── */
.patterns-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 4);
}

.pattern-row {
  display: grid;
  grid-template-columns: calc(var(--space-unit) * 40) 1fr calc(var(--space-unit) * 10) calc(var(--space-unit) * 10);
  align-items: center;
  gap: calc(var(--space-unit) * 4);
}

.pattern-name {
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--brand-text);
  white-space: nowrap;
}

.pattern-track {
  height: calc(var(--space-unit) * 3);
  background-color: color-mix(in srgb, var(--brand-surface) 80%, transparent);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.pattern-bar {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--duration-slow) var(--easing);
}

.pattern-pct {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--brand-muted);
  text-align: right;
}

.pattern-count {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--brand-text);
  text-align: right;
}

/* ── Keyframe animations ──────────────────────────────────────────── */
@keyframes pulse {
  0%, 100% { opacity: 1;   transform: scale(1);    }
  50%       { opacity: 0.5; transform: scale(0.85); }
}

/* ── Responsive: ≤768px ───────────────────────────────────────────── */
@media (max-width: 768px) {
  .page-inner {
    padding: 0 calc(var(--space-unit) * 4);
  }

  .page-header__inner {
    height: auto;
    flex-wrap: wrap;
    padding: calc(var(--space-unit) * 3) 0;
    gap: calc(var(--space-unit) * 3);
  }

  .page-main {
    padding: calc(var(--space-unit) * 4) 0;
  }

  .risk-hero {
    padding: calc(var(--space-unit) * 4);
  }

  .risk-summary {
    gap: calc(var(--space-unit) * 2);
  }

  .risk-pill__count {
    font-size: 1.125rem;
  }

  .containment-grid {
    grid-template-columns: 1fr;
    gap: calc(var(--space-unit) * 6);
  }

  .vuln-grid {
    grid-template-columns: 1fr;
  }

  .expand-toggle {
    padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
    flex-wrap: wrap;
    gap: calc(var(--space-unit) * 2);
  }

  .expand-toggle__count {
    width: 100%;
    padding-left: calc(var(--space-unit) * 7);
  }

  .expand-panel__inner {
    padding: calc(var(--space-unit) * 4);
  }

  .pattern-row {
    grid-template-columns: 1fr auto;
    grid-template-rows: auto auto;
  }

  .pattern-name {
    grid-column: 1;
    grid-row: 1;
  }

  .pattern-count {
    grid-column: 2;
    grid-row: 1;
  }

  .pattern-track {
    grid-column: 1 / -1;
    grid-row: 2;
  }

  .pattern-pct {
    display: none;
  }

  .timeline-card__header {
    flex-wrap: wrap;
  }

  .timeline-agent {
    width: 100%;
  }
}

/* ── Reduced motion ───────────────────────────────────────────────── */
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

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

// aegis/site/landing/v2-asymmetric-bold
// Full scrollable marketing landing page — alternating left-right asymmetric sections

// ── Feature data ──────────────────────────────────────────────────
const features = [
  {
    id: 'scan',
    icon: '⬡',
    title: 'Preemptive Scanning',
    desc: 'The Scanner agent runs continuous deep scans across your production systems, identifying CVEs and misconfigurations before attackers can exploit them. Signatures updated in real time from NVD and MITRE feeds.',
  },
  {
    id: 'defense',
    icon: '◉',
    title: 'Hack-Time Defense',
    desc: 'The Responder agent activates the moment an attack is detected — isolating compromised nodes, revoking tokens, and engaging circuit breakers across the LLM inference path. Response times under 200ms.',
  },
  {
    id: 'roster',
    icon: '◈',
    title: 'Agent Roster',
    desc: 'Four specialized agents — Scanner, Monitor, Responder, and Sentinel — form an interlocking defense perimeter. Each runs 24/7 with independent uptime guarantees and automatic failover.',
  },
  {
    id: 'monitor',
    icon: '◇',
    title: 'Continuous Monitoring',
    desc: 'The Monitor and Sentinel agents watch every packet, request, and model inference for behavioral anomalies. No sleep schedules. No gaps. 99.99% uptime by design.',
  },
]

// ── Pricing tiers ─────────────────────────────────────────────────
const pricingTiers = [
  {
    id: 'starter',
    name: 'Starter',
    price: '$299',
    period: '/mo',
    tagline: 'For teams beginning to secure their agent infrastructure.',
    tokenClass: 'tier--starter',
    ctaClass: 'tier-cta--starter',
    features: [
      { text: 'Continuous monitoring',  included: true  },
      { text: 'Threat alerts & reports', included: true  },
      { text: 'Up to 5 agents',          included: true  },
      { text: 'Hack-time defense',       included: false },
      { text: 'Incident response',       included: false },
      { text: 'SLA guarantee',           included: false },
    ],
    cta: 'Get Started',
    ctaHref: '#signup',
    badge: null,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '$899',
    period: '/mo',
    tagline: 'Complete defense for production-grade agent systems.',
    tokenClass: 'tier--pro',
    ctaClass: 'tier-cta--pro',
    features: [
      { text: 'Everything in Starter', included: true  },
      { text: 'Hack-time defense',      included: true  },
      { text: 'Incident response',      included: true  },
      { text: 'Up to 25 agents',        included: true  },
      { text: 'Priority support',       included: true  },
      { text: 'SLA guarantee',          included: false },
    ],
    cta: 'Start Free Trial',
    ctaHref: '#signup',
    badge: 'RECOMMENDED',
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 'Custom',
    period: '',
    tagline: 'The full Aegis team for your most critical infrastructure.',
    tokenClass: 'tier--enterprise',
    ctaClass: 'tier-cta--enterprise',
    features: [
      { text: 'Everything in Pro',   included: true },
      { text: 'Unlimited agents',    included: true },
      { text: 'Sentinel deployment', included: true },
      { text: 'SLA guarantee',       included: true },
      { text: 'Dedicated support',   included: true },
      { text: 'Custom integrations', included: true },
    ],
    cta: 'Contact Sales',
    ctaHref: '#contact',
    badge: null,
  },
]

// ── Trust stats ───────────────────────────────────────────────────
const trustStats = [
  { value: '1.2M+',  label: 'Threats neutralized', tokenClass: 'stat--threat'  },
  { value: '99.99%', label: 'Uptime guarantee',     tokenClass: 'stat--secured' },
  { value: '10K+',   label: 'Agents protected',     tokenClass: 'stat--secured' },
  { value: '<200ms', label: 'Mean response time',   tokenClass: 'stat--secured' },
]

// ── Compliance badges ─────────────────────────────────────────────
const complianceBadges = [
  { label: 'SOC 2 Type II certified', name: 'SOC 2 Type II', icon: '◈' },
  { label: 'ISO 27001 certified',     name: 'ISO 27001',     icon: '◇' },
  { label: 'GDPR compliant',          name: 'GDPR',          icon: '⬡' },
]

// ── Testimonials ──────────────────────────────────────────────────
const testimonials = [
  {
    id: 1,
    quote: 'Aegis caught a prompt injection campaign we didn\'t even know existed. Response time was under 30 seconds.',
    name: 'Sarah Chen',
    role: 'Head of Platform Engineering, DataOps Inc.',
  },
  {
    id: 2,
    quote: 'We deployed all four agents in under an hour. The Scanner alone flagged 14 CVEs in our fine-tuning pipeline that our own tooling missed.',
    name: 'Marcus Webb',
    role: 'Principal Security Architect, NeuralStack',
  },
  {
    id: 3,
    quote: 'Enterprise SLA hit 99.99% uptime across all systems last quarter. The Responder\'s isolation speed is genuinely remarkable.',
    name: 'Priya Rajan',
    role: 'VP Engineering, AgentOps.ai',
  },
]

// ── Mount state ───────────────────────────────────────────────────
const isMounted = ref(false)

onMounted(() => {
  nextTick(() => { isMounted.value = true })
})

onUnmounted(() => {
  // no intervals or observers — defensive hook present
})
</script>

<template>
  <div class="page" :class="{ 'is-mounted': isMounted }">

    <!-- ── Skip link ─────────────────────────────────────────── -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <!-- ── Nav ───────────────────────────────────────────────── -->
    <nav class="site-nav" aria-label="Main navigation">
      <div class="nav-inner">
        <a href="/" class="nav-brand" aria-label="Aegis home">AEGIS</a>
        <ul class="nav-links" role="list">
          <li><a href="#features" class="nav-link">Features</a></li>
          <li><a href="#pricing" class="nav-link">Pricing</a></li>
          <li><a href="#trust" class="nav-link">Security</a></li>
        </ul>
        <a href="#signup" class="btn btn--primary nav-cta">Get Started</a>
      </div>
    </nav>

    <!-- ── Main ──────────────────────────────────────────────── -->
    <main id="main-content">

      <!-- ── Hero ────────────────────────────────────────────── -->
      <section class="hero" aria-label="Hero" id="hero">
        <div class="section-inner hero__inner">
          <div class="hero__content">
            <p class="hero__eyebrow">Security for AI-native systems</p>
            <h1 class="hero__headline">White Hat Agents.<br>Production&#8209;Grade Defense.</h1>
            <p class="hero__sub">Preemptive scanning and real-time response teams that never sleep — deployed across your entire agent infrastructure.</p>
            <div class="hero__ctas">
              <a href="#pricing" class="btn btn--primary btn--lg">Secure Your Agents</a>
              <a href="#features" class="btn btn--ghost btn--lg">See How It Works</a>
            </div>
            <div class="hero__proof">
              <span class="hero__proof-stat">
                <span class="hero__proof-val">1.2M+</span>
                <span class="hero__proof-lbl">threats neutralized</span>
              </span>
              <span class="hero__proof-sep" aria-hidden="true"></span>
              <span class="hero__proof-stat">
                <span class="hero__proof-val">99.99%</span>
                <span class="hero__proof-lbl">uptime</span>
              </span>
              <span class="hero__proof-sep" aria-hidden="true"></span>
              <span class="hero__proof-stat">
                <span class="hero__proof-val">10K+</span>
                <span class="hero__proof-lbl">agents protected</span>
              </span>
            </div>
          </div>

          <!-- Decorative threat visualization -->
          <div class="hero__visual" aria-hidden="true">
            <svg viewBox="0 0 480 480" class="hero__svg">
              <circle cx="240" cy="240" r="210" fill="none" stroke-width="1" class="threat-ring threat-ring--1"/>
              <circle cx="240" cy="240" r="160" fill="none" stroke-width="1" class="threat-ring threat-ring--2"/>
              <circle cx="240" cy="240" r="110" fill="none" stroke-width="1" class="threat-ring threat-ring--3"/>
              <circle cx="240" cy="240" r="60"  fill="none" stroke-width="1" class="threat-ring threat-ring--4"/>
              <!-- Agent dots positioned on rings -->
              <circle cx="240" cy="30"  r="5" class="agent-dot agent-dot--active"/>
              <circle cx="440" cy="240" r="5" class="agent-dot agent-dot--active"/>
              <circle cx="240" cy="450" r="5" class="agent-dot agent-dot--active"/>
              <circle cx="40"  cy="240" r="4" class="agent-dot agent-dot--standby"/>
              <!-- Core -->
              <circle cx="240" cy="240" r="10" class="threat-core"/>
              <circle cx="240" cy="240" r="10" class="threat-core-pulse"/>
              <!-- Crosshair lines -->
              <line x1="240" y1="0"   x2="240" y2="480" class="crosshair"/>
              <line x1="0"   y1="240" x2="480" y2="240" class="crosshair"/>
            </svg>
          </div>
        </div>
      </section>

      <!-- ── Features ─────────────────────────────────────────── -->
      <section class="features" aria-labelledby="features-heading" id="features">
        <div class="section-inner">
          <div class="features__header">
            <h2 id="features-heading" class="features__title">How Aegis Protects You</h2>
            <p class="features__sub">Four specialized agents. One unified defense perimeter.</p>
          </div>

          <div
            v-for="(feature, i) in features"
            :key="feature.id"
            class="feature-block"
            :class="{ 'feature-block--reverse': i % 2 !== 0 }"
          >
            <div class="feature-block__text">
              <div class="feature-icon" aria-hidden="true">{{ feature.icon }}</div>
              <h3 class="feature-block__heading">{{ feature.title }}</h3>
              <p class="feature-block__desc">{{ feature.desc }}</p>
            </div>
            <div class="feature-block__visual" aria-hidden="true">
              <!-- Decorative mini terminal / status panel per feature -->
              <div class="feature-visual-card">
                <div class="fvc__header">
                  <span class="fvc__dot fvc__dot--red"></span>
                  <span class="fvc__dot fvc__dot--yellow"></span>
                  <span class="fvc__dot fvc__dot--green"></span>
                  <span class="fvc__title">{{ feature.title }}</span>
                </div>
                <div class="fvc__rows">
                  <div class="fvc__row">
                    <span class="fvc__row-dot fvc__row-dot--active"></span>
                    <span class="fvc__row-label">Scanner</span>
                    <span class="fvc__row-val">ACTIVE</span>
                  </div>
                  <div class="fvc__row">
                    <span class="fvc__row-dot fvc__row-dot--active"></span>
                    <span class="fvc__row-label">Monitor</span>
                    <span class="fvc__row-val">ACTIVE</span>
                  </div>
                  <div class="fvc__row">
                    <span class="fvc__row-dot fvc__row-dot--active"></span>
                    <span class="fvc__row-label">Responder</span>
                    <span class="fvc__row-val">ACTIVE</span>
                  </div>
                  <div class="fvc__row">
                    <span class="fvc__row-dot fvc__row-dot--standby"></span>
                    <span class="fvc__row-label">Sentinel</span>
                    <span class="fvc__row-val">STANDBY</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Pricing ───────────────────────────────────────────── -->
      <section class="pricing" aria-labelledby="pricing-heading" id="pricing">
        <div class="section-inner">
          <div class="pricing__header">
            <h2 id="pricing-heading" class="pricing__title">Simple, Transparent Pricing</h2>
            <p class="pricing__sub">Start with what you need. Scale as your infrastructure grows.</p>
          </div>

          <div class="pricing-grid">
            <div
              v-for="tier in pricingTiers"
              :key="tier.id"
              class="pricing-card"
              :class="tier.tokenClass"
            >
              <div class="tier-top">
                <div class="tier-name-row">
                  <span class="tier-name">{{ tier.name }}</span>
                  <span v-if="tier.badge" class="tier-badge">{{ tier.badge }}</span>
                </div>
                <div class="tier-price-row">
                  <span class="tier-price">{{ tier.price }}</span>
                  <span v-if="tier.period" class="tier-period">{{ tier.period }}</span>
                </div>
                <p class="tier-tagline">{{ tier.tagline }}</p>
              </div>

              <ul class="tier-features" role="list" :aria-label="`${tier.name} plan features`">
                <li
                  v-for="feat in tier.features"
                  :key="feat.text"
                  class="feature-item"
                  :class="{ 'feature-item--excluded': !feat.included }"
                >
                  <span
                    class="feature-icon-mark"
                    :class="feat.included ? 'feature-check' : 'feature-cross'"
                    aria-hidden="true"
                  >{{ feat.included ? '✓' : '×' }}</span>
                  <span
                    class="feature-text"
                    :class="{ 'feature-text--excluded': !feat.included }"
                  >{{ feat.text }}</span>
                  <span class="sr-only">{{ feat.included ? 'Included' : 'Not included' }}</span>
                </li>
              </ul>

              <a
                :href="tier.ctaHref"
                class="tier-cta"
                :class="tier.ctaClass"
                :aria-label="`${tier.cta} — ${tier.name} plan`"
              >{{ tier.cta }}</a>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Trust ──────────────────────────────────────────────── -->
      <section class="trust" aria-labelledby="trust-heading" id="trust">
        <div class="section-inner">
          <div class="trust__header">
            <h2 id="trust-heading" class="trust__title">Trusted by Security Teams Worldwide</h2>
          </div>

          <div class="trust-inner">
            <!-- Left: stats + compliance -->
            <div class="trust-left">
              <div class="stats-grid">
                <div
                  v-for="stat in trustStats"
                  :key="stat.label"
                  class="stat-item"
                >
                  <span class="stat-value" :class="stat.tokenClass">{{ stat.value }}</span>
                  <span class="stat-label">{{ stat.label }}</span>
                </div>
              </div>

              <div class="compliance-row" role="list" aria-label="Compliance certifications">
                <div
                  v-for="badge in complianceBadges"
                  :key="badge.name"
                  class="compliance-badge"
                  role="listitem"
                  :aria-label="badge.label"
                >
                  <span class="compliance-icon" aria-hidden="true">{{ badge.icon }}</span>
                  <span class="compliance-label">{{ badge.name }}</span>
                </div>
              </div>
            </div>

            <!-- Right: testimonials -->
            <div class="testimonials-col">
              <figure
                v-for="t in testimonials"
                :key="t.id"
                class="testimonial"
              >
                <blockquote>
                  <p>&#8220;{{ t.quote }}&#8221;</p>
                </blockquote>
                <figcaption class="testimonial__meta">
                  <span class="testimonial__name">{{ t.name }}</span>
                  <span class="testimonial__role">{{ t.role }}</span>
                </figcaption>
              </figure>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Final CTA ──────────────────────────────────────────── -->
      <section class="cta-final" aria-labelledby="cta-final-heading">
        <div class="section-inner">
          <div class="cta-final__inner">
            <div class="cta-final__content">
              <p class="cta-final__overline">Ready when you are</p>
              <h2 id="cta-final-heading" class="cta-final__heading">
                Turn your systems white.<br>Start with Aegis today.
              </h2>
              <p class="cta-final__sub">Deploy in under 10 minutes. No credit card required for your first 14 days.</p>
            </div>
            <div class="cta-final__action">
              <a href="#signup" class="btn btn--primary btn--lg btn--cta-final">Get Started Free</a>
              <p class="cta-final__trust-note">SOC 2 Type II · ISO 27001 · GDPR</p>
            </div>
          </div>
        </div>
      </section>

    </main>

    <!-- ── Footer ────────────────────────────────────────────── -->
    <footer class="site-footer" role="contentinfo">
      <div class="footer-inner">
        <span class="footer-brand">AEGIS</span>
        <span class="footer-copy">© 2026 Aegis Security. All rights reserved.</span>
        <nav class="footer-nav" aria-label="Footer navigation">
          <a href="#" class="footer-link">Privacy</a>
          <a href="#" class="footer-link">Terms</a>
          <a href="#" class="footer-link">Contact</a>
        </nav>
      </div>
    </footer>

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

/* ── Skip link ────────────────────────────────────────────────── */
.skip-link {
  position: absolute;
  top: calc(var(--space-unit) * -20);
  left: 0;
  background-color: var(--brand-primary);
  color: var(--brand-bg);
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
  z-index: 9999;
  text-decoration: none;
  font-family: var(--font-body);
  font-weight: 700;
}

.skip-link:focus {
  top: 0;
}

/* ── Section inner ────────────────────────────────────────────── */
.section-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding-left: calc(var(--space-unit) * 6);
  padding-right: calc(var(--space-unit) * 6);
}

/* ── Navigation ───────────────────────────────────────────────── */
.site-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: color-mix(in srgb, var(--brand-bg) 90%, transparent);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--brand-border);
}

.nav-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 6);
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 6);
}

.nav-brand {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
  text-decoration: none;
  flex-shrink: 0;
}

.nav-brand:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.nav-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: calc(var(--space-unit) * 6);
  flex: 1;
}

.nav-link {
  font-size: 0.9375rem;
  font-weight: 500;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  text-decoration: none;
  transition: color var(--duration-fast) var(--easing);
}

.nav-link:hover {
  color: var(--brand-text);
}

.nav-link:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.nav-cta {
  margin-left: auto;
  flex-shrink: 0;
}

/* ── Buttons ──────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 6);
  border-radius: var(--radius-md);
  text-decoration: none;
  cursor: pointer;
  border: 1px solid transparent;
  transition:
    background-color var(--duration-fast) var(--easing),
    color var(--duration-fast) var(--easing),
    box-shadow var(--duration-fast) var(--easing),
    border-color var(--duration-fast) var(--easing);
}

.btn:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.btn--lg {
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 8);
  font-size: 1.0625rem;
}

.btn--primary {
  background-color: var(--brand-primary);
  color: var(--brand-bg);
  border-color: var(--brand-primary);
}

.btn--primary:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 85%, var(--brand-bg));
  box-shadow: 0 4px 16px color-mix(in srgb, var(--brand-primary) 20%, transparent);
}

.btn--ghost {
  background-color: transparent;
  color: var(--brand-primary);
  border-color: var(--brand-primary);
}

.btn--ghost:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 12%, transparent);
}

.btn--cta-final {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 10);
  font-size: 1.125rem;
  white-space: nowrap;
}

/* ── Hero ─────────────────────────────────────────────────────── */
.hero {
  min-height: 90vh;
  display: flex;
  align-items: center;
  background:
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 39px,
      color-mix(in srgb, var(--brand-accent) 5%, transparent) 40px
    ),
    radial-gradient(
      ellipse 100% 80% at 20% 50%,
      color-mix(in srgb, var(--brand-accent) 20%, var(--brand-bg)),
      color-mix(in srgb, var(--brand-error) 6%, var(--brand-bg)) 50%,
      var(--brand-bg) 80%
    );
  padding-top: calc(var(--space-unit) * 20);
  padding-bottom: calc(var(--space-unit) * 20);
}

.hero__inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 16);
  align-items: center;
}

.hero__content {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
}

.hero__eyebrow {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--brand-accent);
  margin: 0;
}

.hero__headline {
  font-family: var(--font-heading);
  font-size: clamp(3.5rem, 6vw, 5.5rem);
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1.02;
  color: var(--brand-text);
  margin: 0;
}

.hero__sub {
  font-size: 1.125rem;
  line-height: 1.7;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  max-width: 520px;
  margin: 0;
}

.hero__ctas {
  display: flex;
  gap: calc(var(--space-unit) * 4);
  flex-wrap: wrap;
  align-items: center;
}

.hero__proof {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  flex-wrap: wrap;
  padding-top: calc(var(--space-unit) * 4);
  border-top: 1px solid var(--brand-border);
}

.hero__proof-stat {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.hero__proof-val {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--brand-primary);
  line-height: 1;
}

.hero__proof-lbl {
  font-size: 0.75rem;
  color: var(--brand-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-family: var(--font-mono);
}

.hero__proof-sep {
  width: 1px;
  height: calc(var(--space-unit) * 8);
  background-color: var(--brand-border);
  flex-shrink: 0;
}

/* Hero SVG */
.hero__visual {
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero__svg {
  width: 100%;
  max-width: 440px;
  height: auto;
}

.threat-ring {
  stroke: color-mix(in srgb, var(--brand-accent) 25%, transparent);
}

.threat-ring--1 { animation: ring-breathe 4s var(--easing) infinite; }
.threat-ring--2 { animation: ring-breathe 4s 1.3s var(--easing) infinite; }
.threat-ring--3 { animation: ring-breathe 4s 2.6s var(--easing) infinite; }
.threat-ring--4 { animation: ring-breathe 4s 0.65s var(--easing) infinite; }

.agent-dot {
  filter: none;
}

.agent-dot--active  { fill: var(--brand-primary); }
.agent-dot--standby { fill: var(--brand-secondary); }

.threat-core {
  fill: var(--brand-accent);
}

.threat-core-pulse {
  fill: none;
  stroke: var(--brand-accent);
  stroke-width: 2;
  animation: pulse-out 2s var(--easing) infinite;
}

.crosshair {
  stroke: color-mix(in srgb, var(--brand-border) 50%, transparent);
  stroke-width: 1;
}

@keyframes ring-breathe {
  0%, 100% { opacity: 0.55; }
  50%       { opacity: 0.12; }
}

@keyframes pulse-out {
  0%   { r: 10; opacity: 0.8; }
  100% { r: 48; opacity: 0;   }
}

/* ── Features ─────────────────────────────────────────────────── */
.features {
  padding-top: calc(var(--space-unit) * 24);
  padding-bottom: calc(var(--space-unit) * 24);
}

.features__header {
  margin-bottom: calc(var(--space-unit) * 8);
}

.features__title {
  font-family: var(--font-heading);
  font-size: 3.25rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 3) 0;
}

.features__sub {
  font-size: 1.125rem;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  margin: 0;
}

/* Feature blocks — alternating layout */
.feature-block {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 16);
  align-items: center;
  padding: calc(var(--space-unit) * 16) 0;
  border-top: 1px solid var(--brand-border);
}

.feature-block--reverse {
  direction: rtl;
}

.feature-block--reverse > * {
  direction: ltr;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: calc(var(--space-unit) * 4);
}

.feature-block__heading {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 4) 0;
}

.feature-block__desc {
  font-size: 1.0625rem;
  line-height: 1.7;
  color: color-mix(in srgb, var(--brand-text) 75%, transparent);
  margin: 0;
}

/* Feature visual card (decorative) */
.feature-visual-card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.fvc__header {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  padding: calc(var(--space-unit) * 3) calc(var(--space-unit) * 4);
  background-color: var(--brand-bg-secondary);
  border-bottom: 1px solid var(--brand-border);
}

.fvc__dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  flex-shrink: 0;
}

.fvc__dot--red    { background-color: var(--brand-error);     }
.fvc__dot--yellow { background-color: var(--brand-accent);    }
.fvc__dot--green  { background-color: var(--brand-primary);   }

.fvc__title {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--brand-muted);
  margin-left: calc(var(--space-unit) * 2);
}

.fvc__rows {
  padding: calc(var(--space-unit) * 4);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.fvc__row {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.fvc__row-dot {
  width: calc(var(--space-unit) * 2);
  height: calc(var(--space-unit) * 2);
  border-radius: 50%;
  flex-shrink: 0;
}

.fvc__row-dot--active  { background-color: var(--brand-primary);   }
.fvc__row-dot--standby { background-color: var(--brand-secondary); }

.fvc__row-label {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--brand-text);
  flex: 1;
}

.fvc__row-val {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--brand-primary);
}

.fvc__row:last-child .fvc__row-val {
  color: var(--brand-secondary);
}

/* ── Pricing ──────────────────────────────────────────────────── */
.pricing {
  padding-top: calc(var(--space-unit) * 28);
  padding-bottom: calc(var(--space-unit) * 28);
  background: linear-gradient(
    180deg,
    var(--brand-bg-secondary) 0%,
    color-mix(in srgb, var(--brand-bg-secondary) 90%, var(--brand-surface)) 100%
  );
}

.pricing__header {
  margin-bottom: calc(var(--space-unit) * 12);
}

.pricing__title {
  font-family: var(--font-heading);
  font-size: 3.25rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 3) 0;
}

.pricing__sub {
  font-size: 1.0625rem;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  margin: 0;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: calc(var(--space-unit) * 6);
  align-items: start;
}

/* Pricing card */
.pricing-card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 8);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
}

/* Tier-specific treatment */
.tier--starter {
  border-color: color-mix(in srgb, var(--brand-accent) 40%, transparent);
}

.tier--pro {
  border: 2px solid var(--brand-secondary);
  box-shadow:
    0 0 0 1px var(--brand-secondary),
    0 0 24px color-mix(in srgb, var(--brand-secondary) 15%, transparent);
  background-color: color-mix(in srgb, var(--brand-secondary) 6%, var(--brand-surface));
}

.tier--enterprise {
  border-color: color-mix(in srgb, var(--brand-primary) 40%, transparent);
}

.tier-top {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.tier-name-row {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  flex-wrap: wrap;
}

.tier-name {
  font-family: var(--font-heading);
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--brand-text);
}

.tier-badge {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2.5);
  border-radius: var(--radius-sm);
  background-color: var(--brand-secondary);
  color: var(--brand-bg);
}

.tier-price-row {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 1);
}

.tier-price {
  font-family: var(--font-mono);
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brand-text);
}

.tier-period {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 500;
  color: var(--brand-muted);
}

.tier-tagline {
  font-size: 0.9375rem;
  line-height: 1.5;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  margin: 0;
}

/* Feature list */
.tier-features {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
  flex: 1;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.feature-icon-mark {
  font-size: 0.875rem;
  flex-shrink: 0;
  line-height: 1;
}

.feature-check { color: var(--brand-success); }
.feature-cross  { color: color-mix(in srgb, var(--brand-text) 35%, transparent); }

.feature-text {
  font-size: 0.9375rem;
  color: var(--brand-text);
  line-height: 1.4;
}

.feature-text--excluded {
  color: color-mix(in srgb, var(--brand-text) 45%, transparent);
}

/* Tier CTA links */
.tier-cta {
  display: block;
  text-align: center;
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 3.5) calc(var(--space-unit) * 6);
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-decoration: none;
  border: none;
  transition:
    background-color var(--duration-fast) var(--easing),
    box-shadow var(--duration-fast) var(--easing);
}

.tier-cta:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.tier-cta--starter {
  background-color: var(--brand-accent);
  color: var(--brand-bg);
}
.tier-cta--starter:hover {
  background-color: color-mix(in srgb, var(--brand-accent) 85%, var(--brand-bg));
}

.tier-cta--pro {
  background-color: var(--brand-secondary);
  color: var(--brand-bg);
}
.tier-cta--pro:hover {
  background-color: color-mix(in srgb, var(--brand-secondary) 85%, var(--brand-bg));
  box-shadow: 0 4px 16px color-mix(in srgb, var(--brand-secondary) 25%, transparent);
}

.tier-cta--enterprise {
  background-color: var(--brand-primary);
  color: var(--brand-bg);
}
.tier-cta--enterprise:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 85%, var(--brand-bg));
  box-shadow: 0 4px 16px color-mix(in srgb, var(--brand-primary) 20%, transparent);
}

/* ── Trust ────────────────────────────────────────────────────── */
.trust {
  padding-top: calc(var(--space-unit) * 24);
  padding-bottom: calc(var(--space-unit) * 24);
}

.trust__header {
  margin-bottom: calc(var(--space-unit) * 12);
}

.trust__title {
  font-family: var(--font-heading);
  font-size: 3.25rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--brand-text);
  margin: 0;
}

.trust-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 16);
  align-items: start;
}

.trust-left {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 10);
}

/* Stats grid */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 8);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
}

.stat-value {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.stat--threat  { color: var(--brand-accent); }
.stat--secured { color: var(--brand-primary); }

.stat-label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

/* Compliance row */
.compliance-row {
  display: flex;
  gap: calc(var(--space-unit) * 4);
  flex-wrap: wrap;
}

.compliance-badge {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  padding: calc(var(--space-unit) * 2.5) calc(var(--space-unit) * 4);
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-md);
}

.compliance-icon {
  font-size: 1.125rem;
  color: var(--brand-primary);
}

.compliance-label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--brand-text);
}

/* Testimonials */
.testimonials-col {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
}

.testimonial {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 7);
  margin: 0;
  border-left: 3px solid var(--brand-accent);
}

.testimonial blockquote {
  margin: 0 0 calc(var(--space-unit) * 4) 0;
  padding: 0;
}

.testimonial blockquote p {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--brand-text);
  margin: 0;
  font-style: italic;
}

.testimonial__meta {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 0.5);
}

.testimonial__name {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
}

.testimonial__role {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
}

/* ── Final CTA ────────────────────────────────────────────────── */
.cta-final {
  padding-top: calc(var(--space-unit) * 28);
  padding-bottom: calc(var(--space-unit) * 28);
  background:
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 39px,
      color-mix(in srgb, var(--brand-accent) 3%, transparent) 40px
    ),
    radial-gradient(
      ellipse 80% 60% at 50% 100%,
      color-mix(in srgb, var(--brand-accent) 10%, var(--brand-bg-secondary)),
      var(--brand-bg-secondary) 70%
    );
  border-top: 1px solid var(--brand-border);
}

.cta-final__inner {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: calc(var(--space-unit) * 16);
  align-items: center;
}

.cta-final__content {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.cta-final__overline {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-accent);
  margin: 0;
}

.cta-final__heading {
  font-family: var(--font-heading);
  font-size: 3.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.25;
  color: var(--brand-text);
  margin: 0;
}

.cta-final__sub {
  font-size: 1rem;
  line-height: 1.6;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  margin: 0;
  max-width: 480px;
}

.cta-final__action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  flex-shrink: 0;
}

.cta-final__trust-note {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  color: var(--brand-muted);
  text-align: center;
  margin: 0;
}

/* ── Footer ───────────────────────────────────────────────────── */
.site-footer {
  background-color: var(--brand-bg);
  border-top: 1px solid var(--brand-border);
  padding: calc(var(--space-unit) * 8) 0;
}

.footer-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 calc(var(--space-unit) * 6);
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 6);
  flex-wrap: wrap;
}

.footer-brand {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--brand-primary);
}

.footer-copy {
  font-size: 0.8125rem;
  color: var(--brand-muted);
  flex: 1;
}

.footer-nav {
  display: flex;
  gap: calc(var(--space-unit) * 5);
}

.footer-link {
  font-size: 0.8125rem;
  color: color-mix(in srgb, var(--brand-text) 60%, transparent);
  text-decoration: none;
  transition: color var(--duration-fast) var(--easing);
}

.footer-link:hover {
  color: var(--brand-text);
}

.footer-link:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* ── Focus baseline ───────────────────────────────────────────── */
:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

/* ── Responsive ───────────────────────────────────────────────── */
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .nav-cta {
    margin-left: auto;
  }

  .hero {
    min-height: auto;
    padding-top: calc(var(--space-unit) * 16);
    padding-bottom: calc(var(--space-unit) * 16);
  }

  .hero__inner {
    grid-template-columns: 1fr;
    gap: calc(var(--space-unit) * 10);
  }

  .hero__visual {
    order: -1;
  }

  .hero__svg {
    max-width: 280px;
    margin: 0 auto;
    display: block;
  }

  .features {
    padding-top: calc(var(--space-unit) * 16);
    padding-bottom: calc(var(--space-unit) * 16);
  }

  .feature-block {
    grid-template-columns: 1fr;
    gap: calc(var(--space-unit) * 8);
    padding: calc(var(--space-unit) * 10) 0;
  }

  .feature-block--reverse {
    direction: ltr;
  }

  .pricing {
    padding-top: calc(var(--space-unit) * 16);
    padding-bottom: calc(var(--space-unit) * 16);
  }

  .pricing-grid {
    grid-template-columns: 1fr;
  }

  .trust {
    padding-top: calc(var(--space-unit) * 16);
    padding-bottom: calc(var(--space-unit) * 16);
  }

  .trust-inner {
    grid-template-columns: 1fr;
    gap: calc(var(--space-unit) * 12);
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: calc(var(--space-unit) * 6);
  }

  .cta-final {
    padding-top: calc(var(--space-unit) * 16);
    padding-bottom: calc(var(--space-unit) * 16);
  }

  .cta-final__inner {
    grid-template-columns: 1fr;
    gap: calc(var(--space-unit) * 8);
  }

  .footer-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: calc(var(--space-unit) * 4);
  }

  .footer-copy {
    flex: none;
  }
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

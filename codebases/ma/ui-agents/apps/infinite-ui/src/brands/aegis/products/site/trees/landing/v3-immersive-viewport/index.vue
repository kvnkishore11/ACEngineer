<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// aegis/site/landing/v3-immersive-viewport
// Layout: Full-viewport sections (min-height: 100vh) with IntersectionObserver
// scroll-reveal. No scroll-snap — screen reader hostile.
// Variant differentiator:
//   v1 (centered-classic): centered hero, balanced 2×2 features, classic rhythm
//   v2 (asymmetric-bold): left-aligned, alternating left/right feature rows
//   v3 (this one): each section fills the viewport; scroll IS the narrative arc
//                  hero (threat) → features (defense) → pricing (tiers) →
//                  trust (proof) → CTA (resolution)

// ── Feature data ───────────────────────────────────────────────────
const features = [
  {
    id: 'scanning',
    icon: '⬡',
    heading: 'Preemptive Scanning',
    desc: 'Scanner continuously probes your systems for CVEs, misconfigurations, and injection vectors before attackers do. Every finding is prioritised by exploitability and blast radius.',
  },
  {
    id: 'defense',
    icon: '◉',
    heading: 'Hack-Time Defense',
    desc: 'When an attack fires, Responder engages in real time — isolating compromised nodes, deploying updated signatures, and restoring integrity in under 200ms.',
  },
  {
    id: 'roster',
    icon: '◈',
    heading: 'Agent Roster',
    desc: 'Four specialist agents — Scanner, Monitor, Responder, Sentinel — cover vulnerability scanning, traffic analysis, threat containment, and perimeter watch around the clock.',
  },
  {
    id: 'monitoring',
    icon: '◇',
    heading: 'Continuous Monitoring',
    desc: 'Monitor analyses every packet, API call, and model invocation against behavioural baselines. Sentinel watches the perimeter. Neither agent ever sleeps.',
  },
]

// ── Pricing data ───────────────────────────────────────────────────
const pricingTiers = [
  {
    id: 'starter',
    name: 'Starter',
    price: '$299',
    period: '/mo',
    tagline: 'Monitoring, alerts, up to 5 agents',
    badge: '',
    features: ['Vulnerability monitoring', 'Real-time alerts', 'Up to 5 agents', 'Email support', 'SOC 2 compliant'],
    missing: ['Hack-time defense', 'Incident response', 'SLA guarantee'],
    cta: 'Get Started',
    ctaHref: '#signup',
    tier: 'starter',
    highlighted: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '$899',
    period: '/mo',
    tagline: 'Full defense, incident response, 25 agents',
    badge: 'RECOMMENDED',
    features: ['Everything in Starter', 'Hack-time defense', 'Incident response', 'Up to 25 agents', 'Priority support', '99.99% uptime SLA'],
    missing: ['Unlimited agents', 'Custom SLA'],
    cta: 'Start Pro Trial',
    ctaHref: '#signup',
    tier: 'pro',
    highlighted: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 'Custom',
    period: '',
    tagline: 'Full team, unlimited agents, custom SLA',
    badge: '',
    features: ['Everything in Pro', 'Unlimited agents', 'Full Sentinel deployment', 'Custom SLA', 'Dedicated security team', 'On-prem option'],
    missing: [],
    cta: 'Contact Sales',
    ctaHref: '#contact',
    tier: 'enterprise',
    highlighted: false,
  },
]

// ── Trust data ─────────────────────────────────────────────────────
const stats = [
  { id: 'threats', value: '1.2M+',   label: 'Threats Neutralized', color: 'accent'  },
  { id: 'uptime',  value: '99.99%',  label: 'System Uptime',       color: 'primary' },
  { id: 'agents',  value: '10K+',    label: 'Agents Protected',     color: 'primary' },
  { id: 'resp',    value: '<200ms',  label: 'Response Time',        color: 'primary' },
]

const complianceBadges = [
  { id: 'soc2', label: 'SOC 2 Type II', icon: '◈' },
  { id: 'iso',  label: 'ISO 27001',     icon: '◉' },
  { id: 'gdpr', label: 'GDPR Ready',    icon: '◇' },
]

const testimonials = [
  {
    id: 't1',
    quote: "Aegis caught a prompt injection campaign we didn't know existed. Response time was under 30 seconds. Our on-call rotation went from 47 pages a week to zero.",
    name: 'Sarah Chen',
    role: 'Head of Platform Engineering',
    company: 'DataOps Inc.',
  },
  {
    id: 't2',
    quote: 'We deployed the full agent roster in a single afternoon. By morning, Scanner had found three critical CVEs in our API gateway that had been there for months.',
    name: 'Marcus Webb',
    role: 'Principal Security Engineer',
    company: 'Vertex Systems',
  },
  {
    id: 't3',
    quote: 'The red-to-white posture dashboard is the first thing my team checks every morning. Seeing that number climb toward 100% is genuinely motivating.',
    name: 'Priya Nair',
    role: 'VP of Engineering',
    company: 'CloudBase AI',
  },
]

// ── IntersectionObserver scroll-reveal ────────────────────────────
// JS-level prefers-reduced-motion check (double guard with CSS kill-switch)
const prefersReducedMotion = ref(false)
const revealEls = ref<Element[]>([])
let observer: IntersectionObserver | null = null

function collectReveal(el: Element | null) {
  if (el) revealEls.value.push(el)
}

onMounted(() => {
  prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  if (!prefersReducedMotion.value) {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible')
            observer?.unobserve(entry.target)  // fire once, then stop observing
          }
        })
      },
      { threshold: 0.12 }
    )
    revealEls.value.forEach(el => el && observer!.observe(el))
  }
})

onUnmounted(() => {
  observer?.disconnect()
  observer = null
})
</script>

<template>
  <div class="page" aria-label="Aegis Security — Immersive Landing Page">

    <!-- ── Skip link ───────────────────────────────────────────── -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <!-- ── Site navigation ────────────────────────────────────── -->
    <header class="site-nav">
      <div class="nav-inner">
        <a href="#" class="nav-logo" aria-label="Aegis — home">
          <span class="nav-logo__text">AEGIS</span>
          <span class="nav-logo__sub">Security</span>
        </a>
        <nav aria-label="Site navigation">
          <ul class="nav-links" role="list">
            <li><a href="#features" class="nav-link">Features</a></li>
            <li><a href="#pricing"  class="nav-link">Pricing</a></li>
            <li><a href="#trust"    class="nav-link">Trust</a></li>
            <li>
              <a href="#signup" class="nav-link nav-link--cta">Get Started</a>
            </li>
          </ul>
        </nav>
      </div>
    </header>

    <!-- ── Main content ───────────────────────────────────────── -->
    <main id="main-content" role="main">

      <!-- ══════════════════════════════════════════════
           SECTION 1 — HERO (100vh, crimson bloom bg)
           ══════════════════════════════════════════════ -->
      <section
        class="section hero"
        id="hero"
        aria-labelledby="hero-heading"
      >
        <div class="section-inner hero__inner">

          <div
            class="reveal hero__content"
            :ref="collectReveal"
          >
            <span class="hero__eyebrow">AI Security Platform</span>
            <h1 id="hero-heading" class="hero__headline">
              White Hat Agents.<br>
              Zero Compromises.
            </h1>
            <p class="hero__sub">
              Preemptive scanning, real-time defense, and always-on surveillance teams that neutralise threats before they become incidents.
            </p>
            <div class="hero__ctas">
              <a href="#signup"   class="btn btn-primary">Secure Your Agents</a>
              <a href="#features" class="btn btn-ghost">See How It Works</a>
            </div>
          </div>

          <!-- Decorative threat-network SVG — aria-hidden -->
          <div class="hero__visual" aria-hidden="true">
            <svg
              class="threat-graph"
              viewBox="0 0 400 300"
              aria-hidden="true"
              role="img"
            >
              <defs>
                <radialGradient id="core-grad-v3" cx="50%" cy="50%" r="50%">
                  <stop offset="0%"   stop-color="var(--brand-primary)" stop-opacity="0.8"/>
                  <stop offset="100%" stop-color="var(--brand-primary)" stop-opacity="0"/>
                </radialGradient>
              </defs>
              <!-- Threat nodes — outer ring, crimson -->
              <circle cx="40"  cy="60"  r="6" fill="var(--brand-accent)"    opacity="0.7"/>
              <circle cx="360" cy="80"  r="8" fill="var(--brand-accent)"    opacity="0.8"/>
              <circle cx="20"  cy="200" r="5" fill="var(--brand-error)"     opacity="0.6"/>
              <circle cx="380" cy="220" r="7" fill="var(--brand-accent)"    opacity="0.7"/>
              <circle cx="200" cy="20"  r="5" fill="var(--brand-accent)"    opacity="0.5"/>
              <circle cx="150" cy="280" r="6" fill="var(--brand-error)"     opacity="0.6"/>
              <!-- Connection lines -->
              <line x1="40"  y1="60"  x2="200" y2="150" stroke="var(--brand-accent)"    stroke-width="0.5" opacity="0.3"/>
              <line x1="360" y1="80"  x2="200" y2="150" stroke="var(--brand-accent)"    stroke-width="0.5" opacity="0.3"/>
              <line x1="20"  y1="200" x2="200" y2="150" stroke="var(--brand-error)"     stroke-width="0.5" opacity="0.2"/>
              <line x1="380" y1="220" x2="200" y2="150" stroke="var(--brand-accent)"    stroke-width="0.5" opacity="0.3"/>
              <line x1="200" y1="20"  x2="200" y2="150" stroke="var(--brand-secondary)" stroke-width="0.5" opacity="0.3"/>
              <line x1="150" y1="280" x2="200" y2="150" stroke="var(--brand-secondary)" stroke-width="0.5" opacity="0.3"/>
              <!-- Core — white secured center -->
              <circle cx="200" cy="150" r="30" fill="url(#core-grad-v3)"/>
              <circle cx="200" cy="150" r="16" fill="var(--brand-primary)" opacity="0.9"/>
              <!-- Agent guard ring -->
              <circle cx="200" cy="100" r="5" fill="var(--brand-secondary)"/>
              <circle cx="240" cy="170" r="5" fill="var(--brand-secondary)"/>
              <circle cx="160" cy="170" r="5" fill="var(--brand-secondary)"/>
              <circle cx="200" cy="200" r="5" fill="var(--brand-primary)"/>
            </svg>
          </div>

        </div>
      </section>

      <!-- ══════════════════════════════════════════════
           SECTION 2 — FEATURES (100vh, bg-secondary)
           ══════════════════════════════════════════════ -->
      <section
        class="section section-features"
        id="features"
        aria-labelledby="features-heading"
      >
        <div class="section-inner">

          <div class="reveal section-header" :ref="collectReveal">
            <h2 id="features-heading" class="section-heading">
              Four Agents. One Mission.
            </h2>
            <p class="section-sub">
              Every Aegis deployment ships with four specialised agents, each trained on a different attack surface.
            </p>
          </div>

          <div class="features-grid">
            <div
              v-for="(feat, i) in features"
              :key="feat.id"
              class="reveal feature-card"
              :ref="collectReveal"
              :style="{ transitionDelay: `${i * 80}ms` }"
            >
              <span class="feature-card__icon" aria-hidden="true">{{ feat.icon }}</span>
              <h3 class="feature-card__heading">{{ feat.heading }}</h3>
              <p class="feature-card__desc">{{ feat.desc }}</p>
            </div>
          </div>

        </div>
      </section>

      <!-- ══════════════════════════════════════════════
           SECTION 3 — PRICING (90vh, brand-bg)
           ══════════════════════════════════════════════ -->
      <section
        class="section section-pricing"
        id="pricing"
        aria-labelledby="pricing-heading"
      >
        <div class="section-inner">

          <div class="reveal section-header" :ref="collectReveal">
            <h2 id="pricing-heading" class="section-heading">
              Simple, Transparent Pricing
            </h2>
            <p class="section-sub">
              Start with monitoring. Scale to full defense. Enterprise teams get the full roster.
            </p>
          </div>

          <div class="pricing-grid">
            <div
              v-for="tier in pricingTiers"
              :key="tier.id"
              class="reveal pricing-card"
              :class="[
                `pricing-card--${tier.tier}`,
                { 'pricing-card--highlighted': tier.highlighted },
              ]"
              :ref="collectReveal"
            >
              <div class="pricing-card__header">
                <span
                  v-if="tier.badge"
                  class="tier-badge"
                >{{ tier.badge }}</span>
                <h3 class="tier-name">{{ tier.name }}</h3>
                <div class="tier-price" aria-label="Price">
                  <span class="tier-price__amount">{{ tier.price }}</span>
                  <span
                    v-if="tier.period"
                    class="tier-price__period"
                  >{{ tier.period }}</span>
                </div>
                <p class="tier-tagline">{{ tier.tagline }}</p>
              </div>

              <ul
                class="feature-list"
                role="list"
                :aria-label="`${tier.name} plan features`"
              >
                <li
                  v-for="f in tier.features"
                  :key="f"
                  class="feature-item feature-item--included"
                >
                  <span class="feature-check" aria-hidden="true">✓</span>
                  <span>{{ f }}</span>
                </li>
                <li
                  v-for="f in tier.missing"
                  :key="f"
                  class="feature-item feature-item--excluded"
                >
                  <span class="feature-cross" aria-hidden="true">—</span>
                  <span>{{ f }}</span>
                </li>
              </ul>

              <a
                :href="tier.ctaHref"
                class="tier-cta"
                :class="`tier-cta--${tier.tier}`"
                :aria-label="`${tier.cta} — ${tier.name} plan`"
              >{{ tier.cta }}</a>

            </div>
          </div>

        </div>
      </section>

      <!-- ══════════════════════════════════════════════
           SECTION 4 — TRUST (80vh, bg-secondary)
           ══════════════════════════════════════════════ -->
      <section
        class="section section-trust"
        id="trust"
        aria-labelledby="trust-heading"
      >
        <div class="section-inner">

          <div class="reveal section-header" :ref="collectReveal">
            <h2 id="trust-heading" class="section-heading">
              Trusted by Security Teams Worldwide
            </h2>
          </div>

          <!-- Stats -->
          <div
            class="stats-row"
            role="list"
            aria-label="Platform statistics"
          >
            <div
              v-for="stat in stats"
              :key="stat.id"
              class="reveal stat-item"
              :ref="collectReveal"
              role="listitem"
            >
              <span
                class="stat-item__value"
                :class="`stat-value--${stat.color}`"
              >{{ stat.value }}</span>
              <span class="stat-item__label">{{ stat.label }}</span>
            </div>
          </div>

          <!-- Compliance badges -->
          <div
            class="compliance-row"
            role="list"
            aria-label="Security certifications"
          >
            <div
              v-for="badge in complianceBadges"
              :key="badge.id"
              class="reveal compliance-card"
              :ref="collectReveal"
              role="listitem"
              :aria-label="badge.label"
            >
              <span class="compliance-card__icon" aria-hidden="true">{{ badge.icon }}</span>
              <span class="compliance-card__label">{{ badge.label }}</span>
            </div>
          </div>

          <!-- Testimonials — semantic figure/blockquote/figcaption pattern -->
          <div class="testimonials-grid">
            <figure
              v-for="t in testimonials"
              :key="t.id"
              class="reveal testimonial"
              :ref="collectReveal"
            >
              <blockquote>
                <p>{{ t.quote }}</p>
              </blockquote>
              <figcaption class="testimonial__author">
                <span class="testimonial__name">{{ t.name }}</span>
                <span class="testimonial__role">{{ t.role }}, {{ t.company }}</span>
              </figcaption>
            </figure>
          </div>

        </div>
      </section>

      <!-- ══════════════════════════════════════════════
           SECTION 5 — FINAL CTA (60vh, brand-bg + white bloom)
           ══════════════════════════════════════════════ -->
      <section
        class="section section-final-cta"
        id="signup"
        aria-labelledby="cta-final-heading"
      >
        <div class="section-inner">
          <div class="reveal cta-final-content" :ref="collectReveal">
            <h2 id="cta-final-heading" class="cta-final__heading">
              Ready to Turn Your Systems White?
            </h2>
            <p class="cta-final__sub">
              Join 10,000+ engineering teams that sleep soundly because Aegis never does.
            </p>
            <a href="#contact" class="btn btn-primary btn-large">
              Get Started — It's Free
            </a>
            <p class="cta-final__disclaimer">
              No credit card required. Full deployment in under 10 minutes.
            </p>
          </div>
        </div>
      </section>

    </main>

    <!-- ── Footer ──────────────────────────────────────────────── -->
    <footer class="site-footer">
      <div class="footer-inner">
        <span class="footer-brand">AEGIS</span>
        <span class="footer-copy">© 2026 Aegis Security. All rights reserved.</span>
        <nav aria-label="Footer navigation">
          <ul class="footer-links" role="list">
            <li><a href="#" class="footer-link">Privacy</a></li>
            <li><a href="#" class="footer-link">Terms</a></li>
            <li><a href="#" class="footer-link">Security</a></li>
          </ul>
        </nav>
      </div>
    </footer>

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
}

/* ── Skip link ────────────────────────────────────────────────────── */
.skip-link {
  position: absolute;
  top: calc(var(--space-unit) * -20);
  left: calc(var(--space-unit) * 4);
  background-color: var(--brand-primary);
  color: var(--brand-bg);            /* 17.39:1 PASS */
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
  border-radius: var(--radius-sm);
  z-index: 9999;
  text-decoration: none;
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 0.875rem;
  transition: top var(--duration-fast) var(--easing);
}

.skip-link:focus {
  top: calc(var(--space-unit) * 2);
}

/* ── Site navigation ──────────────────────────────────────────────── */
.site-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background-color: color-mix(in srgb, var(--brand-bg) 85%, transparent);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--brand-border);
}

.nav-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 calc(var(--space-unit) * 6);
  height: calc(var(--space-unit) * 16);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 6);
}

.nav-logo {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 2);
  text-decoration: none;
}

.nav-logo:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.nav-logo__text {
  font-family: var(--font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
}

.nav-logo__sub {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-muted);
}

.nav-links {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
}

.nav-link {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 500;
  color: color-mix(in srgb, var(--brand-text) 75%, transparent);
  text-decoration: none;
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 3);
  border-radius: var(--radius-sm);
  transition: color var(--duration-fast) var(--easing);
}

.nav-link:hover {
  color: var(--brand-text);
}

.nav-link:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.nav-link--cta {
  background-color: var(--brand-primary);
  color: var(--brand-bg);            /* 17.39:1 PASS */
  font-weight: 700;
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 5);
}

.nav-link--cta:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 85%, var(--brand-bg));
  color: var(--brand-bg);
}

/* ── Shared section layout ────────────────────────────────────────── */
.section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.section-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: calc(var(--space-unit) * 28) calc(var(--space-unit) * 6) calc(var(--space-unit) * 24);
  width: 100%;
}

.section-header {
  text-align: center;
  margin-bottom: calc(var(--space-unit) * 16);
}

.section-heading {
  font-family: var(--font-heading);
  font-size: 3.25rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--brand-primary);
  margin: 0 0 calc(var(--space-unit) * 4) 0;
  line-height: 1.1;
}

.section-sub {
  font-size: 1.125rem;
  line-height: 1.65;
  color: color-mix(in srgb, var(--brand-text) 75%, transparent);
  max-width: 640px;
  margin: 0 auto;
}

/* ── Scroll-reveal animation ──────────────────────────────────────── */
.reveal {
  opacity: 0;
  transform: translateY(calc(var(--space-unit) * 8));
  transition:
    opacity var(--duration-slow) var(--easing),
    transform var(--duration-slow) var(--easing);
}

.reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* ── SECTION 1 — HERO ─────────────────────────────────────────────── */
.hero {
  min-height: 100vh;
  /* Token-only crimson bloom background — zero rgba() */
  background:
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 39px,
      color-mix(in srgb, var(--brand-accent) 4%, transparent) 40px
    ),
    radial-gradient(
      ellipse 80% 50% at 50% 0%,
      color-mix(in srgb, var(--brand-accent) 20%, var(--brand-bg)),
      var(--brand-bg)
    );
  padding-top: calc(var(--space-unit) * 16);  /* clear fixed nav */
}

.hero__inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 12);
  align-items: center;
}

.hero__eyebrow {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--brand-accent);
  display: block;
  margin-bottom: calc(var(--space-unit) * 3);
}

.hero__headline {
  font-family: var(--font-heading);
  font-size: 5.5rem;
  font-weight: 700;
  letter-spacing: -0.05em;
  line-height: 1.02;
  color: var(--brand-primary);
  margin: 0 0 calc(var(--space-unit) * 4) 0;
}

.hero__sub {
  font-family: var(--font-body);
  font-size: 1.25rem;
  line-height: 1.65;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  max-width: 520px;
  margin: 0 0 calc(var(--space-unit) * 8) 0;
}

.hero__ctas {
  display: flex;
  gap: calc(var(--space-unit) * 4);
  flex-wrap: wrap;
}

.threat-graph {
  width: 100%;
  max-width: 400px;
  opacity: 0.85;
  display: block;
  margin: 0 auto;
}

/* ── CTA buttons — <a> elements for page/section navigation ───────── */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 8);
  border-radius: var(--radius-md);
  text-decoration: none;
  cursor: pointer;
  transition:
    background-color var(--duration-fast) var(--easing),
    color var(--duration-fast) var(--easing),
    box-shadow var(--duration-fast) var(--easing);
}

.btn:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.btn-primary {
  background-color: var(--brand-primary);
  color: var(--brand-bg);            /* 17.39:1 PASS */
  border: none;
}

.btn-primary:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 85%, var(--brand-bg));
  box-shadow: 0 4px 20px color-mix(in srgb, var(--brand-primary) 25%, transparent);
}

.btn-ghost {
  background-color: transparent;
  color: var(--brand-primary);       /* 17.39:1 on bg PASS */
  border: 1px solid var(--brand-primary);
}

.btn-ghost:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 12%, transparent);
}

.btn-large {
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 12);
  font-size: 1.125rem;
}

/* ── SECTION 2 — FEATURES ─────────────────────────────────────────── */
.section-features {
  min-height: 100vh;
  background-color: var(--brand-bg-secondary);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: calc(var(--space-unit) * 8);
}

.feature-card {
  background: linear-gradient(145deg, var(--brand-surface), color-mix(in srgb, var(--brand-surface) 90%, var(--brand-primary)));
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 8);
  transition:
    border-color var(--duration-normal) var(--easing),
    box-shadow var(--duration-normal) var(--easing);
}

.feature-card:hover {
  border-color: color-mix(in srgb, var(--brand-secondary) 40%, transparent);
  box-shadow: 0 0 24px color-mix(in srgb, var(--brand-secondary) 8%, transparent);
}

.feature-card__icon {
  font-size: 2rem;
  line-height: 1;
  display: block;
  margin-bottom: calc(var(--space-unit) * 4);
  color: var(--brand-secondary);
}

.feature-card__heading {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--brand-text);
  margin: 0 0 calc(var(--space-unit) * 3) 0;
}

.feature-card__desc {
  font-size: 0.9375rem;
  line-height: 1.65;
  color: color-mix(in srgb, var(--brand-text) 75%, transparent);
  margin: 0;
}

/* ── SECTION 3 — PRICING ──────────────────────────────────────────── */
.section-pricing {
  min-height: 90vh;
  background: linear-gradient(180deg, var(--brand-bg), color-mix(in srgb, var(--brand-bg) 95%, var(--brand-accent)));
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: calc(var(--space-unit) * 6);
  align-items: start;
}

.pricing-card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 8);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 6);
}

/* Tier accent top bars */
.pricing-card--starter   { border-top: 3px solid var(--brand-accent);    }
.pricing-card--pro       { border-top: 3px solid var(--brand-secondary);  border: 2px solid var(--brand-secondary); }
.pricing-card--enterprise { border-top: 3px solid var(--brand-primary);   }

/* Pro highlighted card — blue glow */
.pricing-card--highlighted {
  box-shadow:
    0 0 0 1px var(--brand-secondary),
    0 0 32px color-mix(in srgb, var(--brand-secondary) 12%, transparent);
  background-color: color-mix(in srgb, var(--brand-secondary) 6%, var(--brand-surface));
}

.pricing-card__header {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.tier-badge {
  display: inline-flex;
  align-self: flex-start;
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: calc(var(--space-unit) * 0.75) calc(var(--space-unit) * 2.5);
  border-radius: var(--radius-sm);
  background-color: var(--brand-secondary);
  color: var(--brand-bg);            /* 5.78:1 PASS */
}

.tier-name {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--brand-text);
  margin: 0;
}

.tier-price {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 1);
}

.tier-price__amount {
  font-family: var(--font-mono);
  font-size: 2.5rem;
  font-weight: 700;
  /* NOT brand-primary — CTA button owns the white; price in brand-text */
  color: var(--brand-text);
  line-height: 1;
}

.tier-price__period {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  color: var(--brand-muted);
}

.tier-tagline {
  font-size: 0.875rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  margin: 0;
  line-height: 1.4;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
  flex: 1;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: calc(var(--space-unit) * 2);
  font-size: 0.875rem;
  line-height: 1.4;
}

.feature-item--included { color: var(--brand-text); }
.feature-item--excluded { color: color-mix(in srgb, var(--brand-text) 35%, transparent); }

.feature-check {
  /* --brand-success = white = secured/included — valid semantic use */
  color: var(--brand-success);
  flex-shrink: 0;
  font-weight: 700;
}

.feature-cross {
  color: color-mix(in srgb, var(--brand-text) 35%, transparent);
  flex-shrink: 0;
}

/* Tier CTA links — all use brand-bg text, contrast verified per tier */
.tier-cta {
  display: block;
  text-align: center;
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: calc(var(--space-unit) * 3.5) calc(var(--space-unit) * 6);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--brand-bg);
  transition:
    background-color var(--duration-fast) var(--easing),
    box-shadow var(--duration-fast) var(--easing);
}

.tier-cta:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.tier-cta--starter    { background-color: var(--brand-accent);    }  /* 4.74:1 PASS */
.tier-cta--pro        { background-color: var(--brand-secondary);  }  /* 5.78:1 PASS */
.tier-cta--enterprise { background-color: var(--brand-primary);    }  /* 17.39:1 PASS */

.tier-cta--starter:hover    { background-color: color-mix(in srgb, var(--brand-accent)    90%, var(--brand-bg)); }
.tier-cta--pro:hover        { background-color: color-mix(in srgb, var(--brand-secondary) 90%, var(--brand-bg)); }
.tier-cta--enterprise:hover { background-color: color-mix(in srgb, var(--brand-primary)   90%, var(--brand-bg)); }

/* ── SECTION 4 — TRUST ────────────────────────────────────────────── */
.section-trust {
  min-height: 80vh;
  background-color: var(--brand-bg-secondary);
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: calc(var(--space-unit) * 6);
  margin-bottom: calc(var(--space-unit) * 16);
}

.stat-item {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 2);
}

.stat-item__value {
  font-family: var(--font-mono);
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
}

.stat-value--primary { color: var(--brand-primary); }
.stat-value--accent  { color: var(--brand-accent);  }  /* threats = crimson */

.stat-item__label {
  font-size: 0.875rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 500;
}

.compliance-row {
  display: flex;
  gap: calc(var(--space-unit) * 4);
  justify-content: center;
  margin-bottom: calc(var(--space-unit) * 16);
  flex-wrap: wrap;
}

.compliance-card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 6);
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
}

.compliance-card__icon {
  font-size: 1.25rem;
  line-height: 1;
  color: var(--brand-primary);
}

.compliance-card__label {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--brand-text);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: calc(var(--space-unit) * 6);
}

/* Testimonials — figure/blockquote/figcaption semantic pattern */
.testimonial {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 8);
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 5);
}

.testimonial blockquote {
  margin: 0;
  padding: 0;
  border: none;
}

.testimonial blockquote p {
  font-size: 0.9375rem;
  line-height: 1.65;
  color: color-mix(in srgb, var(--brand-text) 85%, transparent);
  margin: 0;
  font-style: italic;
}

.testimonial__author {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
  padding-top: calc(var(--space-unit) * 4);
  border-top: 1px solid var(--brand-border);
}

.testimonial__name {
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--brand-text);
}

.testimonial__role {
  font-size: 0.8125rem;
  color: color-mix(in srgb, var(--brand-text) 60%, transparent);
}

/* ── SECTION 5 — FINAL CTA ────────────────────────────────────────── */
.section-final-cta {
  min-height: 60vh;
  background:
    radial-gradient(
      ellipse 60% 60% at 50% 100%,
      color-mix(in srgb, var(--brand-primary) 8%, var(--brand-bg)),
      var(--brand-bg)
    );
}

.cta-final-content {
  text-align: center;
  max-width: 640px;
  margin: 0 auto;
}

.cta-final__heading {
  font-family: var(--font-heading);
  font-size: 2.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--brand-primary);
  margin: 0 0 calc(var(--space-unit) * 4) 0;
  line-height: 1.2;
}

.cta-final__sub {
  font-size: 1.0625rem;
  line-height: 1.65;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  margin: 0 0 calc(var(--space-unit) * 8) 0;
}

.cta-final__disclaimer {
  font-size: 0.8125rem;
  color: var(--brand-muted);
  margin: calc(var(--space-unit) * 4) 0 0 0;
}

/* ── Footer ───────────────────────────────────────────────────────── */
.site-footer {
  background-color: var(--brand-bg-secondary);
  border-top: 1px solid var(--brand-border);
  padding: calc(var(--space-unit) * 8) 0;
}

.footer-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 calc(var(--space-unit) * 6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 6);
  flex-wrap: wrap;
}

.footer-brand {
  font-family: var(--font-mono);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
}

.footer-copy {
  font-size: 0.8125rem;
  color: var(--brand-muted);
  flex: 1;
  text-align: center;
}

.footer-links {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: calc(var(--space-unit) * 4);
}

.footer-link {
  font-size: 0.8125rem;
  color: color-mix(in srgb, var(--brand-text) 55%, transparent);
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

/* ── Responsive: ≤768px ───────────────────────────────────────────── */
@media (max-width: 768px) {
  .nav-links { display: none; }  /* nav links hidden on mobile — logo only */

  .section-inner {
    padding: calc(var(--space-unit) * 20) calc(var(--space-unit) * 5) calc(var(--space-unit) * 16);
  }

  /* Hero */
  .hero__inner {
    grid-template-columns: 1fr;
    gap: calc(var(--space-unit) * 8);
  }

  .hero__visual { display: none; }  /* decorative SVG removed on mobile */

  .hero__headline {
    font-size: 2.5rem;
  }

  .hero__ctas {
    flex-direction: column;
    align-items: flex-start;
  }

  /* Features */
  .features-grid { grid-template-columns: 1fr; }

  /* Pricing */
  .pricing-grid { grid-template-columns: 1fr; }

  /* Trust */
  .stats-row { grid-template-columns: repeat(2, 1fr); }

  .testimonials-grid { grid-template-columns: 1fr; }

  /* Footer */
  .footer-inner {
    flex-direction: column;
    text-align: center;
    gap: calc(var(--space-unit) * 3);
  }

  .footer-copy { text-align: center; }
}

/* ── Reduced motion — CSS kill-switch (double guard with JS check) ── */
@media (prefers-reduced-motion: reduce) {
  .reveal {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
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

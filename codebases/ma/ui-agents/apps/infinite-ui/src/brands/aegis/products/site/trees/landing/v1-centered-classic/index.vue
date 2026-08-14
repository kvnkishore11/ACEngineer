<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

// aegis/site/landing/v1-centered-classic
// Full scrollable marketing landing page — centered classic layout
// Sections: Hero · Features · Pricing · Trust · Final CTA

const isMounted = ref(false)

onMounted(() => {
  nextTick(() => { isMounted.value = true })
})
</script>

<template>
  <!-- Skip link — WCAG 2.4.1 bypass blocks -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <div class="page" :class="{ 'is-mounted': isMounted }">

    <!-- ── Navigation ─────────────────────────────────────────────── -->
    <header class="site-nav">
      <nav class="site-nav__inner" aria-label="Main navigation">
        <a href="/" class="nav-brand">AEGIS</a>
        <ul class="nav-links" role="list">
          <li><a href="#features" class="nav-link">Features</a></li>
          <li><a href="#pricing" class="nav-link">Pricing</a></li>
          <li><a href="#signup" class="btn btn-sm btn-primary">Get Started</a></li>
        </ul>
      </nav>
    </header>

    <!-- ── Main content ───────────────────────────────────────────── -->
    <main id="main-content">

      <!-- ── Section 1: Hero ───────────────────────────────────────── -->
      <section class="hero" aria-label="Hero">
        <div class="hero__inner section-inner">
          <p class="hero__eyebrow" aria-hidden="true">Autonomous Agent Security</p>
          <h1 class="hero__headline">White Hat Agents.<br>Zero Blind Spots.</h1>
          <p class="hero__sub">Four autonomous agents — Scanner, Monitor, Responder, Sentinel — running preemptive and defensive operations around the clock so your production systems stay secured.</p>
          <div class="hero__cta-row">
            <a href="#signup" class="btn btn-primary">Secure Your Agents</a>
            <a href="#features" class="btn btn-ghost">See How It Works</a>
          </div>
          <!-- Subtle threat indicators -->
          <div class="hero__threat-strip" aria-hidden="true">
            <span class="hero__threat-item">PIA-7734 NEUTRALIZED</span>
            <span class="hero__threat-sep">·</span>
            <span class="hero__threat-item">CVE-2024-8821 CONTAINED</span>
            <span class="hero__threat-sep">·</span>
            <span class="hero__threat-item">847 SYSTEMS SECURED</span>
            <span class="hero__threat-sep">·</span>
            <span class="hero__threat-item">UPTIME 99.99%</span>
          </div>
        </div>
      </section>

      <!-- ── Section 2: Features ──────────────────────────────────── -->
      <section
        class="features"
        id="features"
        aria-labelledby="features-heading"
      >
        <div class="section-inner features__inner">
          <p class="eyebrow" aria-hidden="true">How it works</p>
          <h2 class="section-heading" id="features-heading">
            Four Agents. Full Coverage.
          </h2>
          <p class="section-sub">
            Scanner, Monitor, Responder, and Sentinel each own a distinct layer of your security posture. Together they form a coordinated defense that never sleeps.
          </p>

          <div class="feature-grid">

            <article class="feature-card" aria-label="Preemptive Scanning feature">
              <span class="feature-icon" aria-hidden="true">⬡</span>
              <h3 class="feature-title">Preemptive Scanning</h3>
              <p class="feature-desc">Scanner probes your infrastructure for vulnerabilities before attackers find them. CVE-pattern matching and anomaly detection run continuously across all endpoints.</p>
            </article>

            <article class="feature-card" aria-label="Hack-Time Defense feature">
              <span class="feature-icon" aria-hidden="true">◉</span>
              <h3 class="feature-title">Hack-Time Defense</h3>
              <p class="feature-desc">When an attack is in progress, Responder isolates affected systems in milliseconds. Real-time containment stops lateral movement before it starts.</p>
            </article>

            <article class="feature-card" aria-label="Agent Roster feature">
              <span class="feature-icon" aria-hidden="true">◈</span>
              <h3 class="feature-title">Agent Roster</h3>
              <p class="feature-desc">Scanner, Monitor, Responder, and Sentinel form a coordinated defensive team. Each agent has a distinct role — together they cover the full threat lifecycle.</p>
            </article>

            <article class="feature-card" aria-label="Continuous Monitoring feature">
              <span class="feature-icon" aria-hidden="true">◇</span>
              <h3 class="feature-title">Continuous Monitoring</h3>
              <p class="feature-desc">Monitor and Sentinel provide 24/7 traffic analysis and perimeter surveillance. Nothing enters or leaves your environment without being observed.</p>
            </article>

          </div>
        </div>
      </section>

      <!-- ── Section 3: Pricing ───────────────────────────────────── -->
      <section
        class="pricing"
        id="pricing"
        aria-labelledby="pricing-heading"
      >
        <div class="section-inner pricing__inner">
          <p class="eyebrow" aria-hidden="true">Pricing</p>
          <h2 class="section-heading" id="pricing-heading">
            Simple, Transparent Pricing
          </h2>
          <p class="section-sub">
            Start with monitoring. Scale to full defense. No hidden fees, no lock-in.
          </p>

          <div class="pricing-grid">

            <!-- Starter tier -->
            <div class="pricing-card pricing-card--starter" role="article" aria-label="Starter plan">
              <div class="pricing-card__head">
                <span class="tier-name">Starter</span>
                <div class="tier-price-row">
                  <span class="tier-price">$299</span>
                  <span class="tier-period">/mo</span>
                </div>
                <p class="tier-tagline">For teams getting started with agent-based security.</p>
              </div>
              <ul class="tier-features" aria-label="Starter plan features">
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Continuous monitoring
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Real-time alerts
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Up to 5 agents
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  SOC 2 II compliance
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Email support
                </li>
              </ul>
              <a href="#signup" class="tier-cta tier-cta--starter">Get Started with Starter</a>
            </div>

            <!-- Pro tier — highlighted -->
            <div class="pricing-card pricing-card--pro" role="article" aria-label="Pro plan, recommended">
              <div class="pricing-card__head">
                <span class="tier-badge">RECOMMENDED</span>
                <span class="tier-name">Pro</span>
                <div class="tier-price-row">
                  <span class="tier-price">$899</span>
                  <span class="tier-period">/mo</span>
                </div>
                <p class="tier-tagline">For production-grade security with incident response.</p>
              </div>
              <ul class="tier-features" aria-label="Pro plan features">
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Everything in Starter
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Hack-time defense active
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Incident response automation
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Up to 25 agents
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Priority support
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  SLA guarantee
                </li>
              </ul>
              <a href="#signup" class="tier-cta tier-cta--pro">Get Started with Pro</a>
            </div>

            <!-- Enterprise tier -->
            <div class="pricing-card pricing-card--enterprise" role="article" aria-label="Enterprise plan">
              <div class="pricing-card__head">
                <span class="tier-name">Enterprise</span>
                <div class="tier-price-row">
                  <span class="tier-price">Custom</span>
                </div>
                <p class="tier-tagline">For organizations that require absolute security.</p>
              </div>
              <ul class="tier-features" aria-label="Enterprise plan features">
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Everything in Pro
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Unlimited agents
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Sentinel deployment
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Custom SLA
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  Dedicated security team
                </li>
                <li class="tier-feature">
                  <span class="tier-feature__check" aria-hidden="true">✓</span>
                  On-prem deployment
                </li>
              </ul>
              <a href="#signup" class="tier-cta tier-cta--enterprise">Contact Sales</a>
            </div>

          </div><!-- /pricing-grid -->
        </div>
      </section>

      <!-- ── Section 4: Trust ─────────────────────────────────────── -->
      <section
        class="trust"
        aria-labelledby="trust-heading"
      >
        <div class="section-inner trust__inner">
          <p class="eyebrow" aria-hidden="true">Trusted by security teams</p>
          <h2 class="section-heading" id="trust-heading">
            Trusted by Security Teams Worldwide
          </h2>

          <!-- 4a: Stats row -->
          <div class="stats-row" role="list" aria-label="Key metrics">
            <div class="stat-item" role="listitem">
              <span class="stat-number stat-number--threat">1.2M+</span>
              <span class="stat-label">Threats Neutralized</span>
            </div>
            <div class="stat-item" role="listitem">
              <span class="stat-number stat-number--secured">99.99%</span>
              <span class="stat-label">Uptime</span>
            </div>
            <div class="stat-item" role="listitem">
              <span class="stat-number stat-number--secured">10K+</span>
              <span class="stat-label">Agents Protected</span>
            </div>
            <div class="stat-item" role="listitem">
              <!-- Vue auto-escapes < — safe, never use v-html for copy -->
              <span class="stat-number stat-number--secured">{{ '<200ms' }}</span>
              <span class="stat-label">Response Time</span>
            </div>
          </div>

          <!-- 4b: Compliance badges -->
          <div class="compliance-row" role="list" aria-label="Compliance certifications">
            <div class="compliance-card" role="listitem" aria-label="SOC 2 Type II certified">
              <span class="compliance-icon" aria-hidden="true">🛡</span>
              <span class="compliance-label">SOC 2 Type II</span>
            </div>
            <div class="compliance-card" role="listitem" aria-label="ISO 27001 certified">
              <span class="compliance-icon" aria-hidden="true">⬡</span>
              <span class="compliance-label">ISO 27001</span>
            </div>
            <div class="compliance-card" role="listitem" aria-label="GDPR compliant">
              <span class="compliance-icon" aria-hidden="true">◉</span>
              <span class="compliance-label">GDPR Compliant</span>
            </div>
          </div>

          <!-- 4c: Testimonials -->
          <div class="testimonials-grid" aria-label="Customer testimonials">

            <figure class="testimonial">
              <blockquote>
                <p>"Aegis caught a prompt injection campaign we didn't know existed. Response was under 30 seconds — the team didn't even have to intervene."</p>
              </blockquote>
              <figcaption>
                <span class="testimonial__name">Sarah Chen</span>
                <span class="testimonial__role">Head of Platform Engineering, DataOps Inc.</span>
              </figcaption>
            </figure>

            <figure class="testimonial">
              <blockquote>
                <p>"We moved from reactive firefighting to genuinely proactive security. Responder isolated a privilege escalation attempt before our on-call engineer even got the page."</p>
              </blockquote>
              <figcaption>
                <span class="testimonial__name">Marcus Webb</span>
                <span class="testimonial__role">VP Infrastructure, Cloudrise</span>
              </figcaption>
            </figure>

            <figure class="testimonial">
              <blockquote>
                <p>"The combination of Scanner and Sentinel gives us the coverage our compliance auditors have been asking for. Aegis made our SOC 2 audit a formality."</p>
              </blockquote>
              <figcaption>
                <span class="testimonial__name">Priya Sharma</span>
                <span class="testimonial__role">Staff Security Engineer, NeuralCore</span>
              </figcaption>
            </figure>

          </div><!-- /testimonials-grid -->
        </div>
      </section>

      <!-- ── Section 5: Final CTA ─────────────────────────────────── -->
      <section
        class="cta-final"
        id="signup"
        aria-labelledby="cta-final-heading"
      >
        <div class="cta-final__inner section-inner">
          <h2 class="cta-final__heading" id="cta-final-heading">
            Ready to Turn Your Systems White?
          </h2>
          <p class="cta-final__sub">
            Join thousands of engineering teams who trust Aegis to protect their production agents.
          </p>
          <a href="/signup" class="btn btn-primary btn-large">Get Started</a>
        </div>
      </section>

    </main>

    <!-- ── Footer ──────────────────────────────────────────────────── -->
    <footer class="site-footer" role="contentinfo">
      <div class="site-footer__inner section-inner">
        <span class="footer-brand">AEGIS</span>
        <span class="footer-tagline">Your agent security command center.</span>
        <span class="footer-copy">© 2024 Aegis Platform. All rights reserved.</span>
      </div>
    </footer>

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
.page {
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

/* ── Skip link ──────────────────────────────────────────────────────── */
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
  font-size: 0.875rem;
  font-weight: 700;
}

.skip-link:focus {
  top: 0;
}

/* ── Section shared ─────────────────────────────────────────────────── */
.section-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 calc(var(--space-unit) * 6);
}

.eyebrow {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--brand-accent);
  margin: 0 0 calc(var(--space-unit) * 3);
}

.section-heading {
  font-family: var(--font-heading);
  font-size: 3.25rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--brand-primary);
  margin: 0 0 calc(var(--space-unit) * 6);
  line-height: 1.1;
}

.section-sub {
  font-family: var(--font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  margin: 0 0 calc(var(--space-unit) * 12);
}

/* ── Navigation ─────────────────────────────────────────────────────── */
.site-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 200;
  background-color: color-mix(in srgb, var(--brand-bg) 90%, transparent);
  border-bottom: 1px solid var(--brand-border);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.site-nav__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 calc(var(--space-unit) * 6);
  height: calc(var(--space-unit) * 14);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: calc(var(--space-unit) * 4);
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
  align-items: center;
  gap: calc(var(--space-unit) * 6);
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 500;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  text-decoration: none;
  transition: color var(--duration-fast) var(--easing);
}

.nav-link:hover {
  color: var(--brand-primary);
}

.nav-link:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

@media (max-width: 640px) {
  .nav-links li:not(:last-child) {
    display: none;
  }
}

/* ── Buttons ─────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-decoration: none;
  border-radius: var(--radius-md);
  padding: calc(var(--space-unit) * 4) calc(var(--space-unit) * 8);
  cursor: pointer;
  border: none;
  transition:
    background-color var(--duration-fast) var(--easing),
    box-shadow var(--duration-fast) var(--easing),
    transform var(--duration-fast) var(--easing);
}

.btn:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.btn-sm {
  font-size: 0.875rem;
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 4);
}

.btn-large {
  font-size: 1.125rem;
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 12);
}

.btn-primary {
  background-color: var(--brand-primary);
  color: var(--brand-bg);
}

.btn-primary:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 85%, var(--brand-bg));
  box-shadow: 0 4px 16px color-mix(in srgb, var(--brand-primary) 20%, transparent);
}

.btn-ghost {
  background-color: transparent;
  color: var(--brand-primary);
  border: 1px solid var(--brand-primary);
}

.btn-ghost:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 12%, transparent);
}

/* ── Hero ────────────────────────────────────────────────────────────── */
.hero {
  min-height: 85vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: calc(var(--space-unit) * 14); /* nav height offset */
  background:
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 79px,
      color-mix(in srgb, var(--brand-accent) 3%, transparent) 80px
    ),
    radial-gradient(
      ellipse 100% 60% at 50% 0%,
      color-mix(in srgb, var(--brand-accent) 20%, var(--brand-bg)),
      color-mix(in srgb, var(--brand-error) 8%, var(--brand-bg)) 40%,
      var(--brand-bg)
    );
}

.hero__inner {
  text-align: center;
  max-width: 720px;
  padding-top: calc(var(--space-unit) * 12);
  padding-bottom: calc(var(--space-unit) * 12);
}

.hero__eyebrow {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--brand-accent);
  margin: 0 0 calc(var(--space-unit) * 4);
}

.hero__headline {
  font-family: var(--font-heading);
  font-size: 5.5rem;
  font-weight: 700;
  letter-spacing: -0.05em;
  line-height: 1.0;
  color: var(--brand-primary);
  margin: 0 0 calc(var(--space-unit) * 8);
}

.hero__sub {
  font-family: var(--font-body);
  font-size: 1.25rem;
  line-height: 1.7;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  max-width: 600px;
  margin: 0 auto calc(var(--space-unit) * 8);
}

.hero__cta-row {
  display: flex;
  gap: calc(var(--space-unit) * 4);
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: calc(var(--space-unit) * 12);
}

.hero__threat-strip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: calc(var(--space-unit) * 3);
  flex-wrap: wrap;
}

.hero__threat-item {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: color-mix(in srgb, var(--brand-text) 35%, transparent);
}

.hero__threat-sep {
  color: var(--brand-border);
  font-size: 0.75rem;
}

@media (max-width: 768px) {
  .hero__headline {
    font-size: 3.5rem;
  }
  .hero__sub {
    font-size: 1rem;
  }
  .hero__threat-strip {
    display: none;
  }
}

/* ── Features section ───────────────────────────────────────────────── */
.features {
  padding: calc(var(--space-unit) * 20) 0;
  background-color: var(--brand-bg);
}

.features__inner {
  text-align: center;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: calc(var(--space-unit) * 6);
  text-align: left;
  margin-top: calc(var(--space-unit) * 4);
}

.feature-card {
  background: linear-gradient(145deg, color-mix(in srgb, var(--brand-secondary) 4%, var(--brand-surface)), var(--brand-surface));
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 8);
  transition: border-color var(--duration-normal) var(--easing);
}

.feature-card:hover {
  border-color: color-mix(in srgb, var(--brand-primary) 30%, var(--brand-border));
}

.feature-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: calc(var(--space-unit) * 4);
  color: var(--brand-secondary);
}

.feature-title {
  font-family: var(--font-heading);
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--brand-primary);
  margin: 0 0 calc(var(--space-unit) * 3);
}

.feature-desc {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  line-height: 1.6;
  color: color-mix(in srgb, var(--brand-text) 80%, transparent);
  margin: 0;
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
}

/* ── Pricing section ────────────────────────────────────────────────── */
.pricing {
  padding: calc(var(--space-unit) * 20) 0;
  background-color: var(--brand-bg-secondary);
}

.pricing__inner {
  text-align: center;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: calc(var(--space-unit) * 6);
  align-items: start;
  text-align: left;
  margin-top: calc(var(--space-unit) * 4);
}

.pricing-card {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 8);
  display: flex;
  flex-direction: column;
}

.pricing-card--starter {
  border-top: 3px solid var(--brand-accent);
}

.pricing-card--pro {
  border: 2px solid var(--brand-secondary);
  background: linear-gradient(145deg, color-mix(in srgb, var(--brand-secondary) 12%, var(--brand-surface)), color-mix(in srgb, var(--brand-secondary) 4%, var(--brand-surface)));
  box-shadow:
    0 0 0 1px var(--brand-secondary),
    0 0 32px color-mix(in srgb, var(--brand-secondary) 20%, transparent),
    0 0 64px color-mix(in srgb, var(--brand-secondary) 8%, transparent);
}

.pricing-card--enterprise {
  border-top: 3px solid var(--brand-primary);
}

.pricing-card__head {
  margin-bottom: calc(var(--space-unit) * 6);
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
  display: inline-block;
  margin-bottom: calc(var(--space-unit) * 3);
}

.tier-name {
  display: block;
  font-family: var(--font-heading);
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--brand-text);
  margin-bottom: calc(var(--space-unit) * 3);
}

.tier-price-row {
  display: flex;
  align-items: baseline;
  gap: calc(var(--space-unit) * 1.5);
  margin-bottom: calc(var(--space-unit) * 3);
}

/* Price number in --brand-text, NOT --brand-primary (CTA button owns white) */
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
  color: var(--brand-muted);
}

.tier-tagline {
  font-family: var(--font-body);
  font-size: 0.875rem;
  line-height: 1.5;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  margin: 0;
}

.tier-features {
  list-style: none;
  padding: 0;
  margin: 0 0 calc(var(--space-unit) * 8);
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 3);
}

.tier-feature {
  display: flex;
  gap: calc(var(--space-unit) * 3);
  align-items: flex-start;
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--brand-text);
  line-height: 1.5;
}

/* brand-success = white (#f0f0f5) — valid here: white = secured/included */
.tier-feature__check {
  color: var(--brand-success);
  flex-shrink: 0;
  font-size: 1rem;
  line-height: 1.5;
}

.tier-cta {
  display: block;
  text-align: center;
  text-decoration: none;
  font-family: var(--font-heading);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: calc(var(--space-unit) * 3.5) calc(var(--space-unit) * 6);
  border-radius: var(--radius-md);
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
}

.tier-cta--enterprise {
  background-color: var(--brand-primary);
  color: var(--brand-bg);
}

.tier-cta--enterprise:hover {
  background-color: color-mix(in srgb, var(--brand-primary) 85%, var(--brand-bg));
}

@media (max-width: 768px) {
  .pricing-grid {
    grid-template-columns: 1fr;
  }
}

/* ── Trust section ──────────────────────────────────────────────────── */
.trust {
  padding: calc(var(--space-unit) * 20) 0;
  background-color: var(--brand-bg);
}

.trust__inner {
  text-align: center;
}

/* Stats row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: calc(var(--space-unit) * 6);
  margin-bottom: calc(var(--space-unit) * 16);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 2);
  padding: calc(var(--space-unit) * 6) calc(var(--space-unit) * 4);
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
}

.stat-number {
  font-family: var(--font-mono);
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
}

/* Threat count in crimson — these are the attacks */
.stat-number--threat  { color: var(--brand-accent);  }
/* Secured outcomes in white */
.stat-number--secured { color: var(--brand-primary);  }

.stat-label {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: color-mix(in srgb, var(--brand-text) 70%, transparent);
  text-align: center;
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Compliance badges */
.compliance-row {
  display: flex;
  gap: calc(var(--space-unit) * 4);
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: calc(var(--space-unit) * 16);
}

.compliance-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(var(--space-unit) * 3);
  padding: calc(var(--space-unit) * 5) calc(var(--space-unit) * 8);
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-md);
  min-width: calc(var(--space-unit) * 30);
}

.compliance-icon {
  font-size: 1.5rem;
  color: var(--brand-primary);
  display: block;
}

.compliance-label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-text);
}

/* Testimonials */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: calc(var(--space-unit) * 6);
  text-align: left;
}

@media (max-width: 768px) {
  .testimonials-grid {
    grid-template-columns: 1fr;
  }
  .compliance-row {
    flex-direction: column;
    align-items: center;
  }
}

.testimonial {
  background-color: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  padding: calc(var(--space-unit) * 7);
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 5);
}

.testimonial blockquote {
  margin: 0;
  padding: 0;
}

.testimonial blockquote p {
  font-family: var(--font-body);
  font-size: 0.9375rem;
  line-height: 1.7;
  color: color-mix(in srgb, var(--brand-text) 90%, transparent);
  margin: 0;
  font-style: italic;
}

.testimonial blockquote p::before {
  content: '"';
  font-size: 1.5rem;
  color: var(--brand-accent);
  font-style: normal;
  line-height: 0;
  vertical-align: -0.3em;
  margin-right: calc(var(--space-unit) * 1);
}

.testimonial figcaption {
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1);
  padding-top: calc(var(--space-unit) * 4);
  border-top: 1px solid var(--brand-border);
}

.testimonial__name {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  color: var(--brand-text);
}

.testimonial__role {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: color-mix(in srgb, var(--brand-text) 65%, transparent);
  line-height: 1.4;
}

/* ── Final CTA section ──────────────────────────────────────────────── */
.cta-final {
  padding: calc(var(--space-unit) * 20) 0;
  background-color: var(--brand-bg-secondary);
  border-top: 1px solid var(--brand-border);
}

.cta-final__inner {
  text-align: center;
}

.cta-final__heading {
  font-family: var(--font-heading);
  font-size: 3.25rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--brand-primary);
  margin: 0 0 calc(var(--space-unit) * 6);
}

.cta-final__sub {
  font-family: var(--font-body);
  font-size: 1.125rem;
  line-height: 1.6;
  color: color-mix(in srgb, var(--brand-text) 75%, transparent);
  margin: 0 auto calc(var(--space-unit) * 8);
  max-width: 520px;
}

/* ── Footer ─────────────────────────────────────────────────────────── */
.site-footer {
  background-color: var(--brand-bg);
  border-top: 1px solid var(--brand-border);
  padding: calc(var(--space-unit) * 10) 0;
}

.site-footer__inner {
  display: flex;
  align-items: center;
  gap: calc(var(--space-unit) * 4);
  flex-wrap: wrap;
}

.footer-brand {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--brand-primary);
  flex-shrink: 0;
}

.footer-tagline {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: color-mix(in srgb, var(--brand-text) 60%, transparent);
  flex: 1;
}

.footer-copy {
  font-family: var(--font-body);
  font-size: 0.75rem;
  color: var(--brand-muted);
  margin-left: auto;
}

@media (max-width: 640px) {
  .footer-copy {
    margin-left: 0;
    width: 100%;
  }
}

/* ── Reduced motion ─────────────────────────────────────────────────── */
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

<template>
  <section class="hero-centered">
    <div class="hero-content">
      <h1 class="hero-heading">Welcome to Acme Corp</h1>
      <p class="hero-subtext">
        Building the future, one prototype at a time. This is Variant A,
        a centered hero layout demonstrating brand token usage.
      </p>
      <button class="hero-cta">Get Started</button>
    </div>
  </section>
</template>

<style scoped>
.hero-centered {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--brand-bg);
  padding: calc(var(--space-unit) * 4);
}

.hero-content {
  text-align: center;
  max-width: var(--container-max);
}

.hero-heading {
  font-family: var(--font-heading);
  font-size: 3rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--brand-text);
  margin-bottom: calc(var(--space-unit) * 3);
  transition: color var(--duration-normal) var(--easing);
}

.hero-subtext {
  font-family: var(--font-body);
  font-size: 1.125rem;
  color: var(--brand-muted);
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto calc(var(--space-unit) * 4);
  transition: color var(--duration-normal) var(--easing);
}

.hero-cta {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  padding: calc(var(--space-unit) * 2) calc(var(--space-unit) * 5);
  background: var(--brand-primary);
  color: var(--brand-bg);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-normal) var(--easing);
  box-shadow: var(--shadow-md);
}

.hero-cta:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

@media (max-width: 768px) {
  .hero-heading {
    font-size: 2rem;
  }

  .hero-subtext {
    font-size: 1rem;
  }
}
</style>

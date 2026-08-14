<template>
  <section class="hero-split">
    <div class="split-container">
      <div class="split-text">
        <span class="overline">Acme Corp</span>
        <h1 class="split-heading">Design at the Speed of Thought</h1>
        <p class="split-body">
          Variant B demonstrates a split layout with text on the left and a visual
          placeholder on the right. All styles driven by brand tokens.
        </p>
        <div class="split-actions">
          <button class="btn-primary">Start Building</button>
          <button class="btn-secondary">Learn More</button>
        </div>
      </div>
      <div class="split-visual">
        <div class="visual-placeholder" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-split {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background-color: var(--brand-bg);
  padding: calc(var(--space-unit) * 4);
}

.split-container {
  max-width: var(--container-max);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--space-unit) * 8);
  align-items: center;
}

.overline {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--brand-primary);
  margin-bottom: calc(var(--space-unit) * 2);
  display: block;
}

.split-heading {
  font-family: var(--font-heading);
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--brand-text);
  margin-bottom: calc(var(--space-unit) * 3);
  line-height: 1.15;
  transition: color var(--duration-normal) var(--easing);
}

.split-body {
  font-family: var(--font-body);
  font-size: 1rem;
  color: var(--brand-muted);
  line-height: 1.6;
  margin-bottom: calc(var(--space-unit) * 4);
  transition: color var(--duration-normal) var(--easing);
}

.split-actions {
  display: flex;
  gap: calc(var(--space-unit) * 2);
}

.btn-primary {
  font-family: var(--font-body);
  font-size: 0.9rem;
  font-weight: 600;
  padding: calc(var(--space-unit) * 1.5) calc(var(--space-unit) * 4);
  background: var(--brand-primary);
  color: var(--brand-bg);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-normal) var(--easing);
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-secondary {
  font-family: var(--font-body);
  font-size: 0.9rem;
  font-weight: 600;
  padding: calc(var(--space-unit) * 1.5) calc(var(--space-unit) * 4);
  background: transparent;
  color: var(--brand-text);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-normal) var(--easing);
}

.btn-secondary:hover {
  border-color: var(--brand-primary);
  color: var(--brand-primary);
}

.visual-placeholder {
  width: 100%;
  aspect-ratio: 4/3;
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  background-image: linear-gradient(
    135deg,
    var(--brand-primary) 0%,
    var(--brand-secondary) 50%,
    var(--brand-accent) 100%
  );
  opacity: 0.3;
}

@media (max-width: 768px) {
  .split-container {
    grid-template-columns: 1fr;
  }

  .split-heading {
    font-size: 2rem;
  }
}
</style>

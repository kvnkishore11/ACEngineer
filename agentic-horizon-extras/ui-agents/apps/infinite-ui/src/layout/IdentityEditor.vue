<script setup lang="ts">
import { computed } from 'vue'
import { useBrandStore } from '../stores/brand'

const brandStore = useBrandStore()

const identity = computed(() => brandStore.config?.identity)

function updateIdentity(field: string, value: unknown) {
  brandStore.update({
    identity: {
      ...brandStore.config?.identity,
      [field]: value,
    },
  })
}

function parseCommaList(value: string): string[] {
  return value.split(',').map(s => s.trim()).filter(Boolean)
}
</script>

<template>
  <div class="editor-section">
    <h4 class="section-title">Identity</h4>

    <div class="field">
      <label class="field-label">Mission</label>
      <input
        type="text"
        :value="identity?.mission ?? ''"
        @input="updateIdentity('mission', ($event.target as HTMLInputElement).value)"
      />
    </div>

    <div class="field">
      <label class="field-label">Description</label>
      <textarea
        rows="3"
        :value="identity?.description ?? ''"
        @input="updateIdentity('description', ($event.target as HTMLTextAreaElement).value)"
      />
    </div>

    <div class="field">
      <label class="field-label">Keywords (comma-separated)</label>
      <input
        type="text"
        :value="(identity?.keywords ?? []).join(', ')"
        @input="updateIdentity('keywords', parseCommaList(($event.target as HTMLInputElement).value))"
      />
    </div>

    <div class="field">
      <label class="field-label">Voice</label>
      <input
        type="text"
        :value="identity?.voice ?? ''"
        @input="updateIdentity('voice', ($event.target as HTMLInputElement).value)"
      />
    </div>

    <div class="field">
      <label class="field-label">Avoid (comma-separated)</label>
      <input
        type="text"
        :value="(identity?.avoid ?? []).join(', ')"
        @input="updateIdentity('avoid', parseCommaList(($event.target as HTMLInputElement).value))"
      />
    </div>
  </div>
</template>

<style scoped>
.editor-section {
  border-top: 1px solid var(--brand-border);
  padding-top: calc(var(--space-unit) * 2);
  display: flex;
  flex-direction: column;
  gap: calc(var(--space-unit) * 1.5);
}

.section-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--brand-muted);
  letter-spacing: 0.05em;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--brand-muted);
  letter-spacing: 0.04em;
}

.field input,
.field textarea {
  width: 100%;
}

.field textarea {
  resize: vertical;
  min-height: 60px;
}
</style>

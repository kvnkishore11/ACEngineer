<script setup lang="ts">
import { computed } from 'vue'
import { useActivityStore } from '../stores/activity'
import { useCanvasStore } from '../stores/canvas'

const activityStore = useActivityStore()
const canvasStore = useCanvasStore()

const phaseColor = (phase: string) => {
  switch (phase) {
    case 'done': return 'var(--brand-success)'
    case 'failed': return 'var(--brand-error)'
    case 'generating': return 'var(--brand-accent)'
    case 'validating': return 'var(--brand-warning)'
    case 'scaffolding': return 'var(--brand-muted)'
    default: return 'var(--brand-muted)'
  }
}

const phaseIcon = (phase: string) => {
  switch (phase) {
    case 'done': return '\u2713'
    case 'failed': return '\u2717'
    case 'generating': return '\u25CB'
    case 'validating': return '\u25CB'
    case 'scaffolding': return '\u25CF'
    default: return '\u25CB'
  }
}

const doneCount = computed(() => activityStore.branches.filter(b => b.phase === 'done').length)
const totalCount = computed(() => activityStore.branches.length)
</script>

<template>
  <div v-if="activityStore.isActive" class="activity-panel">
    <div class="activity-header" @click="canvasStore.toggleActivityPanel()">
      <div class="activity-title-row">
        <span class="activity-pulse"></span>
        <span class="activity-title">{{ activityStore.pipeline }}</span>
        <span class="activity-count">{{ doneCount }}/{{ totalCount }}</span>
      </div>
      <p v-if="canvasStore.activityPanelOpen" class="activity-brief">{{ activityStore.brief }}</p>
    </div>
    <div v-if="canvasStore.activityPanelOpen" class="activity-branches">
      <div
        v-for="branch in activityStore.branches"
        :key="branch.slug"
        class="activity-branch"
      >
        <span class="branch-phase-icon" :style="{ color: phaseColor(branch.phase) }">{{ phaseIcon(branch.phase) }}</span>
        <span class="branch-slug">{{ branch.slug }}</span>
        <span class="branch-team">{{ branch.team }}</span>
        <span class="branch-phase" :style="{ color: phaseColor(branch.phase) }">{{ branch.phase }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.activity-panel {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 340px;
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  z-index: 100;
  overflow: hidden;
  font-family: var(--font-body);
}

.activity-header {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid var(--brand-border);
}

.activity-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.activity-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brand-accent);
  animation: pulse 1.5s ease-in-out infinite;
}

.activity-title {
  font-weight: 600;
  font-size: 0.8rem;
  color: var(--brand-text);
  text-transform: capitalize;
  flex: 1;
}

.activity-count {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--brand-muted);
  font-family: var(--font-mono);
}

.activity-brief {
  font-size: 0.7rem;
  color: var(--brand-muted);
  margin-top: 6px;
  line-height: 1.3;
}

.activity-branches {
  max-height: 240px;
  overflow-y: auto;
  padding: 8px 0;
}

.activity-branch {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  font-size: 0.75rem;
}

.activity-branch:hover {
  background: color-mix(in srgb, var(--brand-primary) 5%, transparent);
}

.branch-phase-icon {
  font-size: 0.7rem;
  width: 14px;
  text-align: center;
}

.branch-slug {
  color: var(--brand-text);
  font-weight: 500;
  font-family: var(--font-mono);
  flex: 1;
}

.branch-team {
  color: var(--brand-muted);
  font-size: 0.65rem;
}

.branch-phase {
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: capitalize;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.6; }
}
</style>

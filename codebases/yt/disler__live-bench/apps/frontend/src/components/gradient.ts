// Shared helper for computing gradient element IDs from a session id +
// metric key. Lives outside BarGradientDefs.vue so other components (notably
// GroupedBarChart) can call it without importing the SFC just for one fn.

export function gradientIdFor(sessionId: string, metricKey: string): string {
  return `grad-${sessionId}-${metricKey}`.replace(/[^a-zA-Z0-9_-]/g, '_')
}

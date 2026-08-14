<script setup lang="ts">
import type { TagDef } from '../schemas'

defineProps<{ tags: TagDef[] }>()
</script>

<template>
  <div class="tag-bar">
    <span
      v-for="tag in tags"
      :key="tag.name"
      class="tag-bar__tag"
    >
      <span v-if="tag.icons.length" class="tag-bar__icons">
        <img
          v-for="(icon, i) in tag.icons"
          :key="i"
          :src="icon"
          class="tag-bar__icon"
          :alt="tag.name"
        />
      </span>
      <span class="tag-bar__label">{{ tag.name }}</span>
    </span>
  </div>
</template>

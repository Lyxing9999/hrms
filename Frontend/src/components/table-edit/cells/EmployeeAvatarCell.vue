<script setup lang="ts">
import { computed } from "vue";
import { ElAvatar } from "element-plus";

const props = defineProps<{
  row: { photo_url?: string; full_name?: string };
}>();

const initial = computed(() =>
  (props.row?.full_name || "?").slice(0, 1).toUpperCase()
);
</script>

<template>
  <ElAvatar
    :size="32"
    :src="props.row.photo_url || undefined"
    @error="(e) => console.log('avatar load failed:', props.row.photo_url, e)"
  >
    {{ initial }}
  </ElAvatar>
</template>
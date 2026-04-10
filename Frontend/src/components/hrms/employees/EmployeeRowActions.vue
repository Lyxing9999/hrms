<script setup lang="ts">
import { computed } from "vue";
import { Delete, EditPen, RefreshLeft, View } from "@element-plus/icons-vue";
import BaseButton from "~/components/base/BaseButton.vue";

interface EmployeeTableRow {
  id: string;
  full_name: string;
  deleted_at: string | null;
}

const props = defineProps<{
  row: EmployeeTableRow;
  loading?: boolean;
}>();

const emit = defineEmits<{
  (e: "detail", row: EmployeeTableRow): void;
  (e: "assign-schedule", row: EmployeeTableRow): void;
  (e: "delete", row: EmployeeTableRow): void;
  (e: "restore", row: EmployeeTableRow): void;
}>();

const isDeleted = computed(() => !!props.row.deleted_at);
</script>

<template>
  <div class="row-actions">
    <BaseButton type="primary" link size="small" @click="emit('detail', row)">
      <template #iconPre>
        <el-icon><View /></el-icon>
      </template>
      Detail
    </BaseButton>

    <BaseButton
      type="warning"
      link
      size="small"
      @click="emit('assign-schedule', row)"
    >
      <template #iconPre>
        <el-icon><EditPen /></el-icon>
      </template>
      Assign Schedule
    </BaseButton>

    <BaseButton
      v-if="!isDeleted"
      type="danger"
      link
      size="small"
      :loading="loading"
      @click="emit('delete', row)"
    >
      <template #iconPre>
        <el-icon><Delete /></el-icon>
      </template>
      Delete
    </BaseButton>

    <BaseButton
      v-else
      type="success"
      link
      size="small"
      :loading="loading"
      @click="emit('restore', row)"
    >
      <template #iconPre>
        <el-icon><RefreshLeft /></el-icon>
      </template>
      Restore
    </BaseButton>
  </div>
</template>

<style scoped>
.row-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
</style>

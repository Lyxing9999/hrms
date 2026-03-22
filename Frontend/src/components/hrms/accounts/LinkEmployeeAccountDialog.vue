<script setup lang="ts">
import { computed, ref, watch } from "vue";
import {
  ElDialog,
  ElInput,
  ElButton,
  ElTable,
  ElTableColumn,
  ElEmpty,
} from "element-plus";
import type { HrEmployeeDTO } from "~/api/hr_admin/employees/dto";

const props = defineProps<{
  visible: boolean;
  loading?: boolean;
  employees: HrEmployeeDTO[];
  selectedAccountLabel?: string;
}>();

const emit = defineEmits<{
  (e: "update:visible", value: boolean): void;
  (e: "select", employee: HrEmployeeDTO): void;
  (e: "search", keyword: string): void;
  (e: "close"): void;
}>();

const keyword = ref("");

watch(
  () => props.visible,
  (v) => {
    if (!v) keyword.value = "";
  },
);

const filteredEmployees = computed(() => props.employees ?? []);

function closeDialog() {
  emit("update:visible", false);
  emit("close");
}

function handleSearch() {
  emit("search", keyword.value.trim());
}
</script>

<template>
  <ElDialog
    :model-value="visible"
    title="Link Employee"
    width="860px"
    @close="closeDialog"
  >
    <div class="space-y-4">
      <div class="text-sm text-gray-500">
        Selected account:
        <span class="font-medium text-gray-700">
          {{ selectedAccountLabel || "-" }}
        </span>
      </div>

      <div class="flex gap-2">
        <ElInput
          v-model="keyword"
          placeholder="Search employee by code, name, department..."
          clearable
          @keyup.enter="handleSearch"
        />
        <ElButton @click="handleSearch">Search</ElButton>
      </div>

      <ElTable
        v-if="filteredEmployees.length > 0"
        :data="filteredEmployees"
        v-loading="loading"
        height="420"
      >
        <ElTableColumn
          prop="employee_code"
          label="Employee Code"
          min-width="140"
        />
        <ElTableColumn prop="full_name" label="Full Name" min-width="180" />
        <ElTableColumn prop="department" label="Department" min-width="140" />
        <ElTableColumn prop="position" label="Position" min-width="140" />
        <ElTableColumn label="Operation" width="140" align="center">
          <template #default="{ row }">
            <ElButton type="primary" size="small" @click="emit('select', row)">
              Link
            </ElButton>
          </template>
        </ElTableColumn>
      </ElTable>

      <ElEmpty v-else description="No available employees" />
    </div>
  </ElDialog>
</template>

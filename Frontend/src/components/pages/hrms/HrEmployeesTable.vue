<script setup lang="ts">
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { ColumnConfig } from "~/components/types/tableEdit";
import type { EmployeeTableRow } from "~/modules/tables/columns/hr_admin/employeeColumns";

const props = defineProps<{
  rows: EmployeeTableRow[];
  columns: ColumnConfig<EmployeeTableRow>[];
  loading: boolean;
  hasFetchedOnce: boolean;
}>();
</script>

<template>
  <el-card>
    <SmartTable
      :data="rows"
      :columns="columns"
      :loading="loading"
      :has-fetched-once="hasFetchedOnce"
    >
      <template #employee_code="{ row }">
        {{ row.employee?.employee_code || "-" }}
      </template>

      <template #full_name="{ row }">
        {{ row.employee?.full_name || "-" }}
      </template>

      <template #department="{ row }">
        {{ row.employee?.department || "-" }}
      </template>

      <template #position="{ row }">
        {{ row.employee?.position || "-" }}
      </template>

      <template #employment_type="{ row }">
        <el-tag effect="plain">
          {{ row.employee?.employment_type || "-" }}
        </el-tag>
      </template>

      <template #basic_salary="{ row }">
        {{ row.employee?.basic_salary ?? 0 }}
      </template>

      <template #employee_status="{ row }">
        <el-tag
          :type="row.employee?.status === 'active' ? 'success' : 'warning'"
        >
          {{ row.employee?.status || "unknown" }}
        </el-tag>
      </template>

      <template #account_status="{ row }">
        <div class="account-cell">
          <el-tag :type="row.account ? 'success' : 'info'">
            {{ row.account ? row.account.status || "linked" : "not linked" }}
          </el-tag>

          <div v-if="row.account" class="account-meta">
            {{ row.account.email || row.account.username || row.account.id }}
          </div>
        </div>
      </template>

      <template #operation="slotProps">
        <slot name="operation" v-bind="slotProps" />
      </template>
    </SmartTable>
  </el-card>
</template>

<style scoped>
.account-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.account-meta {
  font-size: 12px;
  color: #909399;
}
</style>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import {
  ElRow,
  ElCol,
  ElInput,
  ElSelect,
  ElOption,
  ElTag,
  ElButton,
} from "element-plus";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import type { OvertimeRequestDTO } from "~/api/hr_admin/overtimeRequest";
import { overtimeColumns } from "~/modules/tables/columns/hr_admin/overtimeColumns";
import { useAuthStore } from "~/stores/authStore";
import dayjs from "dayjs";

const { $hrmsAdminService } = useNuxtApp();
const authStore = useAuthStore();

const q = ref("");
const yearFilter = ref<number>(dayjs().year());
const monthFilter = ref<number>(dayjs().month() + 1);
const statusFilter = ref<string | undefined>(undefined);

const isManager = computed(() => {
  const role = authStore.user?.role;
  return role === "manager" || role === "hr_admin" || role === "admin";
});

let fetchRequestsFn: ReturnType<typeof usePaginatedFetch> | null = null;

// For employees - get their own history
const createEmployeeHistoryFetch = () =>
  usePaginatedFetch<OvertimeRequestDTO, void>(
    async (_unusedFilter, page, size, signal) => {
      const res = await $hrmsAdminService().overtimeRequest.getMyRequests({
        status: statusFilter.value as any,
        year: yearFilter.value,
        month: monthFilter.value,
        signal,
      });

      return {
        items: (res ?? []) as OvertimeRequestDTO[],
        total: res.length ?? 0,
      };
    },
    { initialPage: 1 },
  );

// For managers - get team history
const createManagerHistoryFetch = () =>
  usePaginatedFetch<OvertimeRequestDTO, void>(
    async (_unusedFilter, page, size, signal) => {
      const res = await $hrmsAdminService().overtimeRequest.getTeamRequests({
        status: statusFilter.value as any,
        year: yearFilter.value,
        month: monthFilter.value,
        signal,
      });

      return {
        items: (res ?? []) as OvertimeRequestDTO[],
        total: res.length ?? 0,
      };
    },
    { initialPage: 1 },
  );

const {
  data: requests,
  error: tableError,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = isManager.value
  ? createManagerHistoryFetch()
  : createEmployeeHistoryFetch();

watch([statusFilter, yearFilter, monthFilter], () => {
  fetchPage(1);
});

// Status tag color
const getStatusTagType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: "warning",
    approved: "success",
    rejected: "danger",
    cancelled: "info",
  };
  return typeMap[status] || "";
};

// Generate year options
const yearOptions = computed(() => {
  const currentYear = dayjs().year();
  const years = [];
  for (let i = currentYear; i >= currentYear - 5; i--) {
    years.push(i);
  }
  return years;
});

// Generate month options
const monthOptions = [
  { label: "January", value: 1 },
  { label: "February", value: 2 },
  { label: "March", value: 3 },
  { label: "April", value: 4 },
  { label: "May", value: 5 },
  { label: "June", value: 6 },
  { label: "July", value: 7 },
  { label: "August", value: 8 },
  { label: "September", value: 9 },
  { label: "October", value: 10 },
  { label: "November", value: 11 },
  { label: "December", value: 12 },
];

// Initial load
await fetchPage(1);
</script>

<template>
  <OverviewHeader
    :title="isManager ? 'Team Overtime History' : 'Overtime History'"
    :description="
      isManager
        ? 'View team member overtime records'
        : 'View your overtime records'
    "
    :backPath="'/hr/overtime'"
  >
    <template #actions>
      <BaseButton
        plain
        :loading="initialLoading || fetching"
        class="!border-[color:var(--color-primary)] !text-[color:var(--color-primary)] hover:!bg-[var(--color-primary-light-7)]"
        @click="fetchPage(currentPage || 1)"
      >
        Refresh
      </BaseButton>
    </template>
  </OverviewHeader>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="6">
      <el-select v-model="yearFilter" placeholder="Select year">
        <el-option
          v-for="year in yearOptions"
          :key="year"
          :label="String(year)"
          :value="year"
        />
      </el-select>
    </el-col>
    <el-col :span="6">
      <el-select v-model="monthFilter" placeholder="Select month">
        <el-option
          v-for="month in monthOptions"
          :key="month.value"
          :label="month.label"
          :value="month.value"
        />
      </el-select>
    </el-col>
    <el-col :span="6">
      <el-select
        v-model="statusFilter"
        placeholder="Filter by status"
        clearable
      >
        <el-option label="Pending" value="pending" />
        <el-option label="Approved" value="approved" />
        <el-option label="Rejected" value="rejected" />
        <el-option label="Cancelled" value="cancelled" />
      </el-select>
    </el-col>
  </el-row>

  <SmartTable
    :columns="overtimeColumns"
    :data="requests"
    :loading="initialLoading || fetching"
    :total="totalRows"
    :page="currentPage"
    :page-size="pageSize"
    @page="goPage"
    @page-size="setPageSize"
  >
    <template #status="{ row }">
      <el-tag :type="getStatusTagType(row.status)" size="small">
        {{ row.status.charAt(0).toUpperCase() + row.status.slice(1) }}
      </el-tag>
    </template>

    <template #operation="{ row }">
      <el-space>
        <!-- View details -->
        <el-button type="info" size="small" link> View </el-button>
      </el-space>
    </template>
  </SmartTable>

  <el-row v-if="totalRows > 0" justify="end" class="m-4">
    <el-pagination
      :current-page="currentPage"
      :page-size="pageSize"
      :total="totalRows"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      background
      @current-change="goPage"
      @size-change="setPageSize"
    />
  </el-row>
</template>

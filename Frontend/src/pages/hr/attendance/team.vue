<script setup lang="ts">
import { ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { AttendanceDTO } from "~/api/hr_admin/attendance/dto";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";

const { $hrAttendanceService } = useNuxtApp();

const selectedDate = ref(new Date().toISOString().split("T")[0]);
const status = ref<string | undefined>(undefined);

// Table columns
const teamColumns = [
  { prop: "employee_id", label: "Employee", minWidth: 150 },
  {
    prop: "check_in_time",
    label: "Check In",
    width: 100,
    formatter: (row: any) => new Date(row.check_in_time).toLocaleTimeString(),
  },
  {
    prop: "check_out_time",
    label: "Check Out",
    width: 100,
    formatter: (row: any) =>
      row.check_out_time
        ? new Date(row.check_out_time).toLocaleTimeString()
        : "-",
  },
  {
    prop: "late_minutes",
    label: "Late",
    width: 80,
    formatter: (row: any) =>
      row.late_minutes > 0 ? `${row.late_minutes}m` : "-",
  },
  {
    prop: "early_leave_minutes",
    label: "Early Leave",
    width: 100,
    formatter: (row: any) =>
      row.early_leave_minutes > 0 ? `${row.early_leave_minutes}m` : "-",
  },
  { prop: "status", label: "Status", width: 120, slot: "status" },
  { prop: "notes", label: "Notes", minWidth: 200 },
];

// Fetch data
const {
  data: attendances,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = usePaginatedFetch<AttendanceDTO, void>(
  async (_unusedFilter, page, size, signal) => {
    const res = await $hrAttendanceService.getAttendances({
      page,
      limit: size,
      start_date: selectedDate.value,
      end_date: selectedDate.value,
      status: status.value,
      signal,
    });

    return {
      items: (res.items ?? []) as AttendanceDTO[],
      total: res.total ?? 0,
    };
  },
  { initialPage: 1 },
);

watch([selectedDate, status], () => {
  fetchPage(1);
});

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    checked_in: "primary",
    checked_out: "success",
    late: "warning",
    early_leave: "warning",
  };
  return map[status] || "info";
};

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    checked_in: "Checked In",
    checked_out: "Checked Out",
    late: "Late",
    early_leave: "Early Leave",
  };
  return map[status] || status;
};

// Stats
const stats = computed(() => {
  const total = attendances.value?.length || 0;
  const checkedOut =
    attendances.value?.filter((a) => a.check_out_time).length || 0;
  const late = attendances.value?.filter((a) => a.late_minutes > 0).length || 0;
  const earlyLeave =
    attendances.value?.filter((a) => a.early_leave_minutes > 0).length || 0;

  return { total, checkedOut, late, earlyLeave };
});

// Initial load
await fetchPage(1);
</script>

<template>
  <OverviewHeader
    :title="'Team Attendance'"
    :description="'Monitor team attendance and check-in status'"
    :backPath="'/hr/attendance'"
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

  <!-- Stats Cards -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="6">
      <el-card>
        <div class="text-center">
          <div class="text-2xl font-bold text-blue-600">{{ stats.total }}</div>
          <div class="text-sm text-gray-500">Total Present</div>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card>
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600">
            {{ stats.checkedOut }}
          </div>
          <div class="text-sm text-gray-500">Checked Out</div>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card>
        <div class="text-center">
          <div class="text-2xl font-bold text-orange-600">{{ stats.late }}</div>
          <div class="text-sm text-gray-500">Late Arrivals</div>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card>
        <div class="text-center">
          <div class="text-2xl font-bold text-red-600">
            {{ stats.earlyLeave }}
          </div>
          <div class="text-sm text-gray-500">Early Leaves</div>
        </div>
      </el-card>
    </el-col>
  </el-row>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="6">
      <el-date-picker
        v-model="selectedDate"
        type="date"
        placeholder="Select date"
        format="YYYY-MM-DD"
        value-format="YYYY-MM-DD"
        class="w-full"
      />
    </el-col>
    <el-col :span="4">
      <el-select
        v-model="status"
        placeholder="Filter by status"
        clearable
        @change="fetchPage(1)"
      >
        <el-option label="Checked In" value="checked_in" />
        <el-option label="Checked Out" value="checked_out" />
        <el-option label="Late" value="late" />
        <el-option label="Early Leave" value="early_leave" />
      </el-select>
    </el-col>
  </el-row>

  <SmartTable
    :columns="teamColumns"
    :data="attendances"
    :loading="initialLoading || fetching"
    :total="totalRows"
    :page="currentPage"
    :page-size="pageSize"
    @page="goPage"
    @page-size="setPageSize"
  >
    <template #status="{ row }">
      <el-tag :type="getStatusType(row.status)" size="small">
        {{ getStatusLabel(row.status) }}
      </el-tag>
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

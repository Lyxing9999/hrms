<script setup lang="ts">
import { ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { AttendanceDTO } from "~/api/hr_admin/attendance/dto";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { Calendar, Clock, ArrowLeft } from "@element-plus/icons-vue";

const { $hrAttendanceService } = useNuxtApp();

const start_date = ref("");
const end_date = ref("");
const status = ref<string | undefined>(undefined);

// Table columns
const attendanceColumns = [
  {
    prop: "check_in_time",
    label: "Date",
    width: 140,
    formatter: (row: any) =>
      new Date(row.check_in_time).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      }),
  },
  {
    prop: "check_in_time",
    label: "Check In",
    width: 100,
    formatter: (row: any) =>
      new Date(row.check_in_time).toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      }),
  },
  {
    prop: "check_out_time",
    label: "Check Out",
    width: 100,
    formatter: (row: any) =>
      row.check_out_time
        ? new Date(row.check_out_time).toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
          })
        : "-",
  },
  {
    prop: "late_minutes",
    label: "Late",
    width: 80,
    formatter: (row: any) =>
      row.late_minutes > 0 ? `${row.late_minutes} min` : "-",
  },
  {
    prop: "early_leave_minutes",
    label: "Early Leave",
    width: 110,
    formatter: (row: any) =>
      row.early_leave_minutes > 0 ? `${row.early_leave_minutes} min` : "-",
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
      start_date: start_date.value || undefined,
      end_date: end_date.value || undefined,
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

watch([start_date, end_date, status], () => {
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

// Initial load
await fetchPage(1);
</script>

<template>
  <div class="attendance-history">
    <!-- Header -->
    <div class="page-header">
      <nuxt-link to="/employee/check-in" class="back-link">
        <el-icon><ArrowLeft /></el-icon>
        Back to Check-In
      </nuxt-link>
      <h1 class="page-title">
        <el-icon :size="28"><Calendar /></el-icon>
        My Attendance History
      </h1>
      <p class="page-subtitle">View your check-in and check-out records</p>
    </div>

    <!-- Filters -->
    <el-card class="filter-card" shadow="hover">
      <el-row :gutter="16">
        <el-col :xs="24" :sm="8" :md="6">
          <el-date-picker
            v-model="start_date"
            type="date"
            placeholder="Start date"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            class="w-full"
            :prefix-icon="Calendar"
          />
        </el-col>
        <el-col :xs="24" :sm="8" :md="6">
          <el-date-picker
            v-model="end_date"
            type="date"
            placeholder="End date"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            class="w-full"
            :prefix-icon="Calendar"
          />
        </el-col>
        <el-col :xs="24" :sm="8" :md="6">
          <el-select
            v-model="status"
            placeholder="Filter by status"
            clearable
            class="w-full"
            @change="fetchPage(1)"
          >
            <el-option label="Checked In" value="checked_in" />
            <el-option label="Checked Out" value="checked_out" />
            <el-option label="Late" value="late" />
            <el-option label="Early Leave" value="early_leave" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="24" :md="6">
          <el-button
            type="primary"
            :loading="initialLoading || fetching"
            class="w-full"
            @click="fetchPage(currentPage || 1)"
          >
            <el-icon class="mr-2"><Clock /></el-icon>
            Refresh
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- Table -->
    <el-card class="table-card mt-4" shadow="hover">
      <SmartTable
        :columns="attendanceColumns"
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

      <el-row v-if="totalRows > 0" justify="end" class="pagination-row">
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

      <!-- Empty State -->
      <div v-if="!initialLoading && totalRows === 0" class="empty-state">
        <el-icon :size="64" class="empty-icon"><Calendar /></el-icon>
        <p class="empty-text">No attendance records found</p>
        <p class="empty-subtext">
          Your attendance history will appear here once you start checking in
        </p>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.attendance-history {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--el-color-primary);
  text-decoration: none;
  font-size: 14px;
  margin-bottom: 12px;
  transition: all 0.3s;
}

.back-link:hover {
  color: var(--el-color-primary-light-3);
  transform: translateX(-4px);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--el-text-color-primary);
}

.page-subtitle {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

.filter-card,
.table-card {
  border-radius: 12px;
}

.pagination-row {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.empty-state {
  text-align: center;
  padding: 64px 24px;
}

.empty-icon {
  color: var(--el-color-info-light-5);
  margin-bottom: 16px;
}

.empty-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.empty-subtext {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

.mt-4 {
  margin-top: 16px;
}

.mr-2 {
  margin-right: 8px;
}

.w-full {
  width: 100%;
}

@media (max-width: 768px) {
  .attendance-history {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }
}
</style>

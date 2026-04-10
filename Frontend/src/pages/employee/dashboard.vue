<script setup lang="ts">
import { computed, onActivated, onMounted, ref } from "vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import { hrmsAdminService } from "~/api/hr_admin";
import type { HrEmployeeDTO } from "~/api/hr_admin/employees/dto";
import type { AttendanceTodayDTO } from "~/api/hr_admin/attendance/dto";
import type { MyOvertimeSummaryDTO } from "~/api/hr_admin/overtime/dto";
import type {
  LeaveBalanceDTO,
  LeaveSummaryDTO,
} from "~/api/hr_admin/leave/dto";
import type { PayslipDTO } from "~/api/hr_admin/payroll/dto";
import { ROUTES } from "~/constants/routes";

definePageMeta({ layout: "default" });

const router = useRouter();
const hrService = hrmsAdminService();

const loading = ref(false);
const initialized = ref(false);

const employee = ref<HrEmployeeDTO | null>(null);
const attendanceToday = ref<AttendanceTodayDTO["item"]>(null);
const overtimeSummary = ref<MyOvertimeSummaryDTO | null>(null);
const leaveSummary = ref<LeaveSummaryDTO | null>(null);
const leaveBalance = ref<LeaveBalanceDTO | null>(null);
const payslips = ref<PayslipDTO[]>([]);

function toNumber(value?: number | string | null): number {
  const n = Number(value ?? 0);
  return Number.isFinite(n) ? n : 0;
}

function formatMoney(value?: number | null): string {
  const amount = toNumber(value);
  return amount.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function formatDate(value?: string | null): string {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "2-digit",
  });
}

function formatDateTime(value?: string | null): string {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatMonthLabel(month?: string | null): string {
  if (!month) return "-";
  const date = new Date(`${month}-01T00:00:00`);
  if (Number.isNaN(date.getTime())) return String(month);
  return date.toLocaleDateString("en-US", {
    month: "short",
    year: "2-digit",
  });
}

function statusTagType(
  status?: string | null,
): "success" | "warning" | "danger" | "info" {
  const key = String(status || "").toLowerCase();

  if (
    key === "approved" ||
    key === "paid" ||
    key === "checked_out" ||
    key === "present"
  ) {
    return "success";
  }

  if (
    key === "pending" ||
    key === "generated" ||
    key === "checked_in" ||
    key === "excused"
  ) {
    return "warning";
  }

  if (key === "rejected" || key === "absent" || key === "cancelled") {
    return "danger";
  }

  return "info";
}

function cssVar(name: string, fallback: string): string {
  if (typeof window === "undefined") return fallback;
  const value = getComputedStyle(document.documentElement)
    .getPropertyValue(name)
    .trim();
  return value || fallback;
}

function buildEmptyOption(text: string) {
  return {
    title: {
      text,
      left: "center",
      top: "center",
      textStyle: {
        fontSize: 14,
        fontWeight: 500,
        color: cssVar("--muted-color", "#94a3b8"),
      },
    },
  };
}

const attendanceLabel = computed(() => {
  const status = attendanceToday.value?.status;
  if (!status) return "No Attendance Yet";
  return String(status)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (m) => m.toUpperCase());
});

const pageNetSalary = computed(() =>
  payslips.value.reduce((sum, item) => sum + toNumber(item.net_salary), 0),
);

const payslipTrendRows = computed(() => {
  return [...payslips.value]
    .sort((a, b) => String(a.month || "").localeCompare(String(b.month || "")))
    .slice(-8);
});

const attendanceSummary = computed(() => ({
  status: attendanceLabel.value,
  date: formatDate(attendanceToday.value?.attendance_date),
  checkIn: formatDateTime(attendanceToday.value?.check_in_time),
  checkOut: formatDateTime(attendanceToday.value?.check_out_time),
  lateMinutes: toNumber(attendanceToday.value?.late_minutes),
  earlyLeaveMinutes: toNumber(attendanceToday.value?.early_leave_minutes),
}));

const overtimeCards = computed(() => {
  const ot = overtimeSummary.value;
  return {
    approvedHours: toNumber(ot?.approved_hours).toFixed(1),
    approvedPayment: formatMoney(ot?.approved_payment),
    pending: toNumber(ot?.pending_count),
    approved: toNumber(ot?.approved_count),
    rejected: toNumber(ot?.rejected_count),
    cancelled: toNumber(ot?.cancelled_count),
    total: toNumber(ot?.total_requests),
  };
});

const leaveCards = computed(() => {
  const leave = leaveSummary.value;
  const balance = leaveBalance.value;

  return {
    pending: toNumber(leave?.pending),
    approved: toNumber(leave?.approved),
    rejected: toNumber(leave?.rejected),
    cancelled: toNumber(leave?.cancelled),
    total: toNumber(leave?.total_requests),
    remaining: toNumber(balance?.remaining_days),
    used: toNumber(balance?.used_days),
    entitlement: toNumber(balance?.annual_entitlement),
  };
});

const requestCompositionOption = computed(() => {
  const ot = overtimeSummary.value;
  const leave = leaveSummary.value;

  if (!ot && !leave) return buildEmptyOption("No request summary available");

  const otData = [
    { name: "Pending", value: toNumber(ot?.pending_count) },
    { name: "Approved", value: toNumber(ot?.approved_count) },
    { name: "Rejected", value: toNumber(ot?.rejected_count) },
    { name: "Cancelled", value: toNumber(ot?.cancelled_count) },
  ];

  const leaveData = [
    { name: "Pending", value: toNumber(leave?.pending) },
    { name: "Approved", value: toNumber(leave?.approved) },
    { name: "Rejected", value: toNumber(leave?.rejected) },
    { name: "Cancelled", value: toNumber(leave?.cancelled) },
  ];

  const tooltipBg = cssVar("--chart-tooltip-bg", "rgba(15, 23, 42, 0.92)");
  const tooltipText = cssVar("--color-light", "#ffffff");
  const chartLabel = cssVar("--chart-label-color", "#64748b");
  const chartText = cssVar("--text-color", "#0f172a");
  const chartBorder = cssVar("--chart-border-color", "#ffffff");

  return {
    tooltip: {
      trigger: "item",
      confine: true,
      backgroundColor: tooltipBg,
      borderWidth: 0,
      textStyle: {
        color: tooltipText,
      },
      formatter: (params: any) => {
        return `
          <div style="min-width: 120px;">
            <div style="font-weight:600;margin-bottom:4px;">${params.seriesName}</div>
            <div>${params.name}: <strong>${params.value}</strong></div>
          </div>
        `;
      },
    },
    legend: {
      bottom: 0,
      icon: "circle",
      itemWidth: 10,
      itemHeight: 10,
      textStyle: {
        fontSize: 11,
        color: chartLabel,
      },
    },
    graphic: [
      {
        type: "text",
        left: "25%",
        top: "38%",
        style: {
          text: `OT\n${leaveCards.value.total || overtimeCards.value.total}`,
          textAlign: "center",
          fill: chartText,
          fontSize: 13,
          fontWeight: 700,
          lineHeight: 18,
        },
      },
      {
        type: "text",
        left: "73%",
        top: "38%",
        style: {
          text: `Leave\n${leaveCards.value.total}`,
          textAlign: "center",
          fill: chartText,
          fontSize: 13,
          fontWeight: 700,
          lineHeight: 18,
        },
      },
    ],
    series: [
      {
        name: "Overtime",
        type: "pie",
        center: ["25%", "42%"],
        radius: ["44%", "66%"],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 12,
          borderColor: chartBorder,
          borderWidth: 3,
        },
        label: { show: false },
        labelLine: { show: false },
        emphasis: {
          scale: true,
          scaleSize: 8,
        },
        data: otData,
      },
      {
        name: "Leave",
        type: "pie",
        center: ["75%", "42%"],
        radius: ["44%", "66%"],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 12,
          borderColor: chartBorder,
          borderWidth: 3,
        },
        label: { show: false },
        labelLine: { show: false },
        emphasis: {
          scale: true,
          scaleSize: 8,
        },
        data: leaveData,
      },
    ],
  };
});

const leaveBalanceAdvancedOption = computed(() => {
  const b = leaveBalance.value;
  if (!b) return buildEmptyOption("No leave balance available");

  const entitlement = toNumber(b.annual_entitlement);
  const used = toNumber(b.used_days);
  const remaining = toNumber(b.remaining_days);
  const safeEntitlement = Math.max(entitlement, 1);
  const tooltipBg = cssVar("--chart-tooltip-bg", "rgba(15, 23, 42, 0.92)");
  const tooltipText = cssVar("--color-light", "#ffffff");
  const chartLabel = cssVar("--chart-label-color", "#64748b");
  const chartGrid = cssVar("--chart-grid", "#e5e7eb");

  return {
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      confine: true,
      backgroundColor: tooltipBg,
      borderWidth: 0,
      textStyle: { color: tooltipText },
    },
    legend: {
      bottom: 0,
      textStyle: {
        color: chartLabel,
        fontSize: 11,
      },
    },
    grid: {
      top: 24,
      left: 42,
      right: 18,
      bottom: 40,
    },
    xAxis: {
      type: "category",
      axisTick: { show: false },
      axisLine: { lineStyle: { color: chartGrid } },
      axisLabel: { color: chartLabel },
      data: ["Entitlement", "Used", "Remaining"],
    },
    yAxis: [
      {
        type: "value",
        min: 0,
        minInterval: 1,
        name: "Days",
        nameTextStyle: { color: chartLabel },
        axisLabel: { color: chartLabel },
        splitLine: {
          lineStyle: { color: chartGrid },
        },
      },
      {
        type: "value",
        min: 0,
        max: 100,
        name: "%",
        nameTextStyle: { color: chartLabel },
        axisLabel: { color: chartLabel },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        name: "Days",
        type: "bar",
        barWidth: "40%",
        itemStyle: {
          borderRadius: [10, 10, 0, 0],
        },
        data: [entitlement, used, remaining],
      },
      {
        name: "Utilization %",
        type: "line",
        yAxisIndex: 1,
        smooth: true,
        symbol: "circle",
        symbolSize: 8,
        lineStyle: {
          width: 3,
        },
        data: [
          100,
          Number(((used / safeEntitlement) * 100).toFixed(1)),
          Number(((remaining / safeEntitlement) * 100).toFixed(1)),
        ],
      },
    ],
  };
});

const payrollTrendOption = computed(() => {
  if (!payslipTrendRows.value.length)
    return buildEmptyOption("No payroll trend data");

  const labels = payslipTrendRows.value.map((item) =>
    formatMonthLabel(item.month),
  );
  const net = payslipTrendRows.value.map((item) => toNumber(item.net_salary));
  const deduction = payslipTrendRows.value.map((item) =>
    toNumber(item.total_deductions),
  );
  const ot = payslipTrendRows.value.map((item) => toNumber(item.ot_payment));
  const tooltipBg = cssVar("--chart-tooltip-bg", "rgba(15, 23, 42, 0.92)");
  const tooltipText = cssVar("--color-light", "#ffffff");
  const chartLabel = cssVar("--chart-label-color", "#64748b");
  const chartGrid = cssVar("--chart-grid", "#e5e7eb");

  return {
    tooltip: {
      trigger: "axis",
      confine: true,
      backgroundColor: tooltipBg,
      borderWidth: 0,
      textStyle: { color: tooltipText },
    },
    legend: {
      bottom: 0,
      icon: "roundRect",
      itemWidth: 12,
      itemHeight: 8,
      textStyle: {
        color: chartLabel,
        fontSize: 11,
      },
    },
    grid: {
      top: 26,
      left: 44,
      right: 18,
      bottom: 42,
    },
    xAxis: {
      type: "category",
      data: labels,
      axisTick: { show: false },
      axisLine: { lineStyle: { color: chartGrid } },
      axisLabel: { color: chartLabel },
    },
    yAxis: {
      type: "value",
      name: "Amount",
      nameTextStyle: { color: chartLabel },
      axisLabel: { color: chartLabel },
      splitLine: {
        lineStyle: { color: chartGrid },
      },
    },
    series: [
      {
        name: "Net Salary",
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 8,
        lineStyle: { width: 3 },
        areaStyle: { opacity: 0.08 },
        data: net,
      },
      {
        name: "Deductions",
        type: "bar",
        barWidth: "22%",
        stack: "aux",
        itemStyle: {
          borderRadius: [8, 8, 0, 0],
        },
        data: deduction,
      },
      {
        name: "OT Payment",
        type: "bar",
        barWidth: "22%",
        stack: "aux",
        itemStyle: {
          borderRadius: [8, 8, 0, 0],
        },
        data: ot,
      },
    ],
  };
});

async function fetchDashboard() {
  loading.value = true;
  try {
    const [profile, today, otSummary, lSummary, lBalance, payslipData] =
      await Promise.all([
        hrService.employee.getMyEmployee(),
        hrService.attendance.getMyAttendanceToday(),
        hrService.overtimeRequest.getMyOvertimeSummary(),
        hrService.leaveRequest.getMySummary(),
        hrService.leaveRequest.getMyBalance(),
        hrService.payrollRun.listPayslips({ page: 1, limit: 8 }),
      ]);

    employee.value = profile;
    attendanceToday.value = today.item;
    overtimeSummary.value = otSummary;
    leaveSummary.value = lSummary;
    leaveBalance.value = lBalance;
    payslips.value = payslipData.items ?? [];
  } catch {
    // handled by service layer
  } finally {
    loading.value = false;
  }
}

async function ensureInitialLoad() {
  if (initialized.value) return;
  initialized.value = true;
  await fetchDashboard();
}

onMounted(() => {
  void ensureInitialLoad();
});

onActivated(() => {
  void fetchDashboard();
});
</script>

<template>
  <div class="employee-dashboard-page">
    <OverviewHeader
      title="Employee Dashboard"
      description="Personal insights across attendance, overtime, leave, and payroll"
      :backPath="ROUTES.EMPLOYEE.DASHBOARD"
    >
      <template #actions>
        <BaseButton plain :loading="loading" @click="fetchDashboard">
          Refresh
        </BaseButton>
        <BaseButton
          plain
          :disabled="loading"
          @click="router.push(ROUTES.EMPLOYEE.LEAVE_REQUEST)"
        >
          Request Leave
        </BaseButton>
      </template>
    </OverviewHeader>

    <el-row :gutter="16" class="section-row section-row--kpi">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card
          class="panel-card kpi-card kpi-card--employee"
          shadow="hover"
          v-loading="loading"
        >
          <p class="kpi-card__label">Employee</p>
          <p class="kpi-card__value">{{ employee?.full_name || "-" }}</p>
          <p class="kpi-card__hint">
            {{ employee?.employee_code || "No code" }}
          </p>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card
          class="panel-card kpi-card kpi-card--attendance"
          shadow="hover"
          v-loading="loading"
        >
          <p class="kpi-card__label">Today Attendance</p>
          <p class="kpi-card__value">{{ attendanceLabel }}</p>
          <p class="kpi-card__hint">
            In: {{ formatDateTime(attendanceToday?.check_in_time) }}
          </p>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card
          class="panel-card kpi-card kpi-card--overtime"
          shadow="hover"
          v-loading="loading"
        >
          <p class="kpi-card__label">Approved Overtime</p>
          <p class="kpi-card__value">{{ overtimeCards.approvedHours }} h</p>
          <p class="kpi-card__hint">
            Payment: {{ overtimeCards.approvedPayment }}
          </p>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card
          class="panel-card kpi-card kpi-card--leave"
          shadow="hover"
          v-loading="loading"
        >
          <p class="kpi-card__label">Leave Remaining</p>
          <p class="kpi-card__value">{{ leaveCards.remaining }} day(s)</p>
          <p class="kpi-card__hint">
            Used: {{ leaveCards.used }} / {{ leaveCards.entitlement }}
          </p>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="section-row">
      <el-col :xs="24" :lg="12">
        <el-card
          shadow="hover"
          class="panel-card dashboard-card"
          v-loading="loading"
        >
          <div class="card-top">
            <div>
              <div class="section-head">Request Status Comparison</div>
              <div class="section-sub">
                Overtime and leave requests in one compact visual
              </div>
            </div>
            <el-tag effect="plain" round>
              Total Requests: {{ overtimeCards.total + leaveCards.total }}
            </el-tag>
          </div>

          <ClientOnly>
            <div class="chart-box chart-box--standard">
              <VChart
                :option="requestCompositionOption"
                autoresize
                class="chart-view"
              />
            </div>
            <template #fallback>
              <div class="chart-fallback">Loading chart...</div>
            </template>
          </ClientOnly>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="12">
        <el-card
          shadow="hover"
          class="panel-card dashboard-card"
          v-loading="loading"
        >
          <div class="card-top">
            <div>
              <div class="section-head">Leave Utilization Analytics</div>
              <div class="section-sub">
                Entitlement, usage, and remaining balance
              </div>
            </div>
            <el-tag effect="plain" round>
              Remaining: {{ leaveCards.remaining }} day(s)
            </el-tag>
          </div>

          <ClientOnly>
            <div class="chart-box chart-box--standard">
              <VChart
                :option="leaveBalanceAdvancedOption"
                autoresize
                class="chart-view"
              />
            </div>
            <template #fallback>
              <div class="chart-fallback">Loading chart...</div>
            </template>
          </ClientOnly>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="section-row">
      <el-col :xs="24">
        <el-card
          shadow="hover"
          class="panel-card dashboard-card"
          v-loading="loading"
        >
          <div class="card-top">
            <div>
              <div class="section-head">Payroll Trend Analytics</div>
              <div class="section-sub">
                Net salary, deductions, and overtime payment by month
              </div>
            </div>
            <el-tag type="success" effect="plain" round>
              Page Net: {{ formatMoney(pageNetSalary) }}
            </el-tag>
          </div>

          <ClientOnly>
            <div class="chart-box chart-box--tall">
              <VChart
                :option="payrollTrendOption"
                autoresize
                class="chart-view"
              />
            </div>
            <template #fallback>
              <div class="chart-fallback">Loading chart...</div>
            </template>
          </ClientOnly>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="section-row">
      <el-col :xs="24" :lg="10">
        <el-card
          shadow="hover"
          v-loading="loading"
          class="panel-card dashboard-card h-full"
        >
          <div class="section-head">Today Snapshot</div>
          <div class="section-sub">Current attendance detail for today</div>

          <div class="summary-strip">
            <el-tag
              :type="statusTagType(attendanceToday?.status)"
              effect="plain"
              round
            >
              {{ attendanceSummary.status }}
            </el-tag>
            <el-tag effect="plain" round>
              {{ attendanceSummary.date }}
            </el-tag>
          </div>

          <div class="meta-grid">
            <div class="meta-card">
              <span class="meta-label">Check In</span>
              <span class="meta-value">{{ attendanceSummary.checkIn }}</span>
            </div>

            <div class="meta-card">
              <span class="meta-label">Check Out</span>
              <span class="meta-value">{{ attendanceSummary.checkOut }}</span>
            </div>

            <div class="meta-card">
              <span class="meta-label">Late Minutes</span>
              <span class="meta-value"
                >{{ attendanceSummary.lateMinutes }} min</span
              >
            </div>

            <div class="meta-card">
              <span class="meta-label">Early Leave</span>
              <span class="meta-value">
                {{ attendanceSummary.earlyLeaveMinutes }} min
              </span>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="14">
        <el-card
          shadow="hover"
          v-loading="loading"
          class="panel-card dashboard-card h-full"
        >
          <div class="card-top">
            <div>
              <div class="section-head">Payroll Snapshot</div>
              <div class="section-sub">Latest payroll records overview</div>
            </div>
            <el-tag effect="plain" round>
              Payslips: {{ payslips.length }}
            </el-tag>
          </div>

          <div class="table-wrap">
            <el-table
              :data="payslips.slice(0, 4)"
              size="small"
              border
              style="width: 100%"
            >
              <el-table-column prop="month" label="Month" width="110" />
              <el-table-column label="Net Salary" min-width="130">
                <template #default="{ row }">
                  {{ formatMoney(row.net_salary) }}
                </template>
              </el-table-column>
              <el-table-column label="Status" width="110">
                <template #default="{ row }">
                  <el-tag
                    :type="statusTagType(row.status)"
                    effect="plain"
                    round
                    size="small"
                  >
                    {{ String(row.status || "-").toUpperCase() }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="Created" min-width="160">
                <template #default="{ row }">
                  {{ formatDateTime(row.lifecycle?.created_at) }}
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card
      shadow="hover"
      v-loading="loading"
      class="panel-card dashboard-card section-row section-row--final"
    >
      <div class="card-top">
        <div>
          <div class="section-head">Recent Payslips</div>
          <div class="section-sub">
            Latest payroll records from the payslip list
          </div>
        </div>
        <el-tag effect="plain" round> GET /api/hrms/payroll/payslips </el-tag>
      </div>

      <div class="table-wrap">
        <el-table :data="payslips" border style="width: 100%" size="small">
          <el-table-column prop="month" label="Month" width="110" />
          <el-table-column label="Base Salary" min-width="130">
            <template #default="{ row }">
              {{ formatMoney(row.base_salary) }}
            </template>
          </el-table-column>
          <el-table-column label="OT" width="120">
            <template #default="{ row }">
              {{ formatMoney(row.ot_payment) }}
            </template>
          </el-table-column>
          <el-table-column label="Deductions" width="130">
            <template #default="{ row }">
              {{ formatMoney(row.total_deductions) }}
            </template>
          </el-table-column>
          <el-table-column label="Net Salary" min-width="140">
            <template #default="{ row }">
              {{ formatMoney(row.net_salary) }}
            </template>
          </el-table-column>
          <el-table-column label="Status" width="110">
            <template #default="{ row }">
              <el-tag
                :type="statusTagType(row.status)"
                effect="plain"
                round
                size="small"
              >
                {{ String(row.status || "-").toUpperCase() }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.employee-dashboard-page {
  padding: 20px;
  max-width: 1520px;
  margin: 0 auto;
}

.section-row {
  margin-bottom: 16px;
}

.section-row--final {
  margin-bottom: 0;
}

.panel-card {
  border-radius: 18px;
  border: 1px solid var(--border-color);
  background: var(--color-card);
  transition: border-color 0.22s ease, box-shadow 0.22s ease,
    transform 0.22s ease;
}

.panel-card:hover {
  border-color: color-mix(
    in srgb,
    var(--primary-color) 30%,
    var(--border-color)
  );
  box-shadow: 0 10px 24px
    color-mix(in srgb, var(--primary-color) 10%, transparent);
  transform: translateY(-1px);
}

.panel-card :deep(.el-card__body) {
  padding: 16px;
}

.dashboard-card {
  min-height: 100%;
}

.dashboard-card.h-full :deep(.el-card__body) {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.dashboard-card.h-full .table-wrap {
  flex: 1;
}

.kpi-card {
  --kpi-accent: var(--chart-2);
  position: relative;
  overflow: hidden;
  border-radius: 18px;
  min-height: 156px;
  background: #fff;
  border-color: color-mix(in srgb, var(--kpi-accent) 18%, var(--border-color));
}

.kpi-card::before {
  content: "";
  position: absolute;
  inset: 0;
  opacity: 1;
  background: radial-gradient(
      120% 80% at 100% 0%,
      color-mix(in srgb, var(--kpi-accent) 10%, transparent) 0%,
      transparent 60%
    ),
    linear-gradient(
      135deg,
      color-mix(in srgb, var(--kpi-accent) 7%, transparent),
      transparent 48%
    );
  pointer-events: none;
}

.kpi-card--employee::before {
  --kpi-accent: var(--chart-6);
}

.kpi-card--attendance::before {
  --kpi-accent: var(--chart-2);
}

.kpi-card--overtime::before {
  --kpi-accent: var(--button-warning-bg);
}

.kpi-card--leave::before {
  --kpi-accent: var(--chart-7);
}

.kpi-card__label {
  position: relative;
  margin: 0;
  font-size: 12px;
  color: var(--muted-color);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.kpi-card__value {
  position: relative;
  margin: 10px 0 4px;
  font-size: 30px;
  line-height: 1.08;
  font-weight: 800;
  color: var(--text-color);
}

.kpi-card__hint {
  position: relative;
  margin: 0;
  font-size: 12px;
  color: var(--muted-color);
}

.card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}

.section-head {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-color);
}

.section-sub {
  margin-top: 4px;
  font-size: 12px;
  color: var(--muted-color);
}

.chart-box {
  width: 100%;
}

.chart-box--standard {
  height: 300px;
}

.chart-box--tall {
  height: 360px;
}

.chart-view {
  width: 100%;
  height: 100%;
}

.chart-fallback {
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: var(--muted-color);
}

.table-wrap {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  scrollbar-gutter: stable;
  scrollbar-width: thin;
  scrollbar-color: color-mix(in srgb, var(--muted-color) 50%, transparent)
    transparent;
}

.table-wrap::-webkit-scrollbar {
  height: 8px;
  width: 8px;
}

.table-wrap::-webkit-scrollbar-thumb {
  background: color-mix(in srgb, var(--muted-color) 42%, transparent);
  border-radius: 999px;
}

.table-wrap::-webkit-scrollbar-thumb:hover {
  background: color-mix(in srgb, var(--muted-color) 62%, transparent);
}

.table-wrap :deep(.el-table) {
  min-width: 720px;
}

.summary-strip {
  margin-top: 8px;
  margin-bottom: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.meta-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.meta-card {
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 14px;
  background: linear-gradient(
    180deg,
    var(--color-card) 0%,
    color-mix(in srgb, var(--hover-bg) 28%, var(--color-card) 72%) 100%
  );
}

.meta-label {
  display: block;
  font-size: 12px;
  color: var(--muted-color);
}

.meta-value {
  display: block;
  margin-top: 4px;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-color);
}

@media (max-width: 768px) {
  .employee-dashboard-page {
    padding: 12px;
  }

  .panel-card :deep(.el-card__body) {
    padding: 14px;
  }

  .section-row {
    margin-bottom: 12px;
  }

  .kpi-card {
    min-height: 124px;
  }

  .kpi-card__value {
    font-size: 24px;
  }

  .card-top {
    flex-direction: column;
    align-items: stretch;
  }

  .chart-box--standard,
  .chart-box--tall {
    height: 250px;
  }

  .chart-fallback {
    min-height: 250px;
  }

  .meta-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 1280px) {
  .section-row--kpi {
    margin-bottom: 18px;
  }

  .chart-box--standard {
    height: 320px;
  }

  .chart-box--tall {
    height: 380px;
  }
}
</style>

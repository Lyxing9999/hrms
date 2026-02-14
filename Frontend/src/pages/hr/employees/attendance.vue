<script setup lang="ts">
import { computed, ref } from "vue";

type TabKey = "profile" | "reports" | "employee";

const tab = ref<TabKey>("employee");

const kpis = ref([
  { label: "Department", value: 20 },
  { label: "Employee", value: 200 },
  { label: "Presence", value: 131 },
  { label: "Leave", value: 18 },
]);

const leaveRequests = ref([
  { id: 1, name: "Lyyou San", role: "IT Support Officer", avatar: "https://i.pravatar.cc/80?img=5" },
  { id: 2, name: "Lyyou San", role: "IT Support Officer", avatar: "https://i.pravatar.cc/80?img=6" },
  { id: 3, name: "Lyyou San", role: "IT Support Officer", avatar: "https://i.pravatar.cc/80?img=7" },
]);

/** Calendar */
const calendarDate = ref(new Date());
const month = ref(calendarDate.value.getMonth()); // 0-11
const year = ref(calendarDate.value.getFullYear());

const monthOptions = [
  "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec",
].map((label, idx) => ({ label, value: idx }));

const yearOptions = computed(() => {
  const y = year.value;
  return Array.from({ length: 7 }, (_, i) => y - 3 + i).map((v) => ({ label: String(v), value: v }));
});

function syncCalendar() {
  calendarDate.value = new Date(year.value, month.value, 1);
}

function prevMonth() {
  const d = new Date(year.value, month.value - 1, 1);
  year.value = d.getFullYear();
  month.value = d.getMonth();
  syncCalendar();
}
function nextMonth() {
  const d = new Date(year.value, month.value + 1, 1);
  year.value = d.getFullYear();
  month.value = d.getMonth();
  syncCalendar();
}
</script>

<template>
  <div class="dash-page">
    <!-- Top bar -->
    <div class="dash-top">
      <div class="pill-tabs">
        <button class="pill" :class="{ active: tab === 'profile' }" @click="tab = 'profile'">
          Profile
        </button>
        <button class="pill" :class="{ active: tab === 'reports' }" @click="tab = 'reports'">
          Reports
        </button>
        <button class="pill" :class="{ active: tab === 'employee' }" @click="tab = 'employee'">
          Employee
        </button>
      </div>

      <el-button class="icon-btn" circle>
        <el-icon><Bell /></el-icon>
      </el-button>
    </div>

    <!-- KPI Row -->
    <el-row :gutter="16" class="kpi-row">
      <el-col v-for="k in kpis" :key="k.label" :xs="24" :sm="12" :md="6">
        <el-card class="app-card kpi-card is-always-shadow">
          <div class="kpi-title">{{ k.label }}</div>
          <div class="kpi-value">{{ k.value }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Row -->
    <el-row :gutter="16" class="charts-row">
      <el-col :xs="24" :md="8">
        <el-card class="app-card viz-card is-always-shadow">
          <div class="viz-box" />
        </el-card>
      </el-col>
      <el-col :xs="24" :md="8">
        <el-card class="app-card viz-card is-always-shadow">
          <div class="viz-box" />
        </el-card>
      </el-col>
      <el-col :xs="24" :md="8">
        <el-card class="app-card viz-card is-always-shadow">
          <div class="viz-box" />
        </el-card>
      </el-col>
    </el-row>

    <!-- Bottom Row: Leaves + Calendar -->
    <el-row :gutter="16" class="bottom-row">
      <el-col :xs="24" :md="16">
        <el-card class="app-card leave-panel is-always-shadow">
          <template #header>
            <div class="panel-title">Employee’s leave</div>
          </template>

          <div class="leave-grid">
            <div v-for="p in leaveRequests" :key="p.id" class="leave-card">
              <div class="leave-head">
                <img :src="p.avatar" class="avatar" alt="" />
                <div class="meta">
                  <div class="name">{{ p.name }}</div>
                  <div class="role">{{ p.role }}</div>
                </div>
              </div>
              <div class="leave-body" />
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="8">
        <el-card class="app-card calendar-panel is-always-shadow">
          <div class="cal-header">
            <el-button class="cal-nav" circle @click="prevMonth">
              <el-icon><ArrowLeft /></el-icon>
            </el-button>

            <div class="cal-selects">
              <el-select v-model="month" size="small" class="cal-select" @change="syncCalendar">
                <el-option v-for="m in monthOptions" :key="m.value" :label="m.label" :value="m.value" />
              </el-select>

              <el-select v-model="year" size="small" class="cal-select" @change="syncCalendar">
                <el-option v-for="y in yearOptions" :key="y.value" :label="y.label" :value="y.value" />
              </el-select>
            </div>

            <el-button class="cal-nav" circle @click="nextMonth">
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>

          <el-calendar v-model="calendarDate" class="cal-body">
            <!-- you can customize cells here later -->
          </el-calendar>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
/* Layout */
.dash-page {
  padding: 16px;
  background: var(--color-bg);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Top bar */
.dash-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.pill-tabs {
  display: inline-flex;
  gap: 10px;
  padding: 6px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--color-card) 85%, var(--color-primary) 15%);
  border: 1px solid var(--border-color);
}

.pill {
  border: 0;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 999px;
  font-weight: 650;
  font-size: 13px;
  color: var(--muted-color);
  background: transparent;
  transition: background-color var(--transition-base), color var(--transition-base);
}

.pill.active {
  color: var(--text-color);
  background: color-mix(in srgb, var(--color-primary) 40%, var(--color-card) 60%);
  border: 1px solid color-mix(in srgb, var(--border-color) 65%, var(--el-color-primary) 35%);
}

.icon-btn {
  border: 1px solid var(--border-color) !important;
  background: var(--color-card) !important;
  color: var(--text-color) !important;
}

/* KPI */
.kpi-row {
  margin-top: 4px;
}

.kpi-card {
  background: color-mix(in srgb, var(--color-card) 90%, var(--color-primary) 10%) !important;
  border: 1px solid color-mix(in srgb, var(--border-color) 65%, var(--color-primary) 35%) !important;
  border-radius: 16px !important;
}

.kpi-title {
  font-size: 16px;
  font-weight: 650;
  color: var(--text-color);
}

.kpi-value {
  margin-top: 10px;
  font-size: 56px;
  line-height: 1;
  font-weight: 750;
  color: color-mix(in srgb, var(--text-color) 25%, var(--muted-color) 75%);
}

/* Charts placeholders */
.viz-card {
  border-radius: 16px !important;
}

.viz-box {
  height: 220px;
  border-radius: 14px;
  background: color-mix(in srgb, var(--border-color) 35%, var(--color-card) 65%);
}

/* Bottom panels */
.leave-panel,
.calendar-panel {
  border-radius: 16px !important;
}

.panel-title {
  font-size: 28px;
  font-weight: 750;
  color: var(--text-color);
}

/* Leave cards */
.leave-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.leave-card {
  background: var(--color-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  overflow: hidden;
}

.leave-head {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-bottom: 1px solid color-mix(in srgb, var(--border-color) 75%, transparent);
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  object-fit: cover;
}

.meta .name {
  font-weight: 650;
  font-size: 13px;
  color: var(--text-color);
}
.meta .role {
  font-size: 11px;
  color: var(--muted-color);
}

.leave-body {
  height: 120px;
  background: color-mix(in srgb, var(--color-card) 92%, var(--color-primary) 8%);
}

/* Calendar */
.cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}

.cal-selects {
  display: flex;
  gap: 8px;
  align-items: center;
  flex: 1;
  justify-content: center;
}

.cal-select {
  width: 92px;
}

.cal-nav {
  border: 1px solid var(--border-color) !important;
  background: var(--color-card) !important;
}

.cal-body :deep(.el-calendar__header) {
  display: none; /* hide default header to match your screenshot */
}

.cal-body :deep(.el-calendar-table) {
  border-radius: 12px;
  overflow: hidden;
}

/* Responsive */
@media (max-width: 1024px) {
  .leave-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .leave-grid {
    grid-template-columns: 1fr;
  }
  .kpi-value {
    font-size: 44px;
  }
}
</style>
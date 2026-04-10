<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import { ElMessageBox } from "element-plus";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import { useMessage } from "~/composables/common/useMessage";
import type { ColumnConfig } from "~/components/types/tableEdit";
import type {
  WorkingScheduleCreateDTO,
  WorkingScheduleDTO,
  WorkingScheduleUpdateDTO,
} from "~/api/hr_admin/schedule";

type ScheduleFilter = "active" | "deleted" | "all";

type ScheduleFormModel = {
  name: string;
  start_time: string;
  end_time: string;
  working_days: number[];
  is_default: boolean;
};

const DAYS = [
  { label: "Mon", value: 0, fullLabel: "Monday" },
  { label: "Tue", value: 1, fullLabel: "Tuesday" },
  { label: "Wed", value: 2, fullLabel: "Wednesday" },
  { label: "Thu", value: 3, fullLabel: "Thursday" },
  { label: "Fri", value: 4, fullLabel: "Friday" },
  { label: "Sat", value: 5, fullLabel: "Saturday" },
  { label: "Sun", value: 6, fullLabel: "Sunday" },
] as const;

import { hrmsAdminService } from "~/api/hr_admin";

const scheduleService = hrmsAdminService().workingSchedule;

const schedules = ref<WorkingScheduleDTO[]>([]);
const loading = ref(false);
const dialogVisible = ref(false);
const dialogMode = ref<"create" | "edit">("create");
const saving = ref(false);
const submittingDefaultId = ref<string | null>(null);
const actionLoading = ref<Record<string, boolean>>({});
const currentScheduleId = ref<string>("");
const initialFormValues = ref<ScheduleFormModel | null>(null);

const q = ref("");
const filter = ref<ScheduleFilter>("active");
const page = ref(1);
const pageSize = ref(10);

const form = reactive<ScheduleFormModel>(getDefaultForm());

const tableColumns: ColumnConfig<WorkingScheduleDTO>[] = [
  {
    field: "name",
    label: "Schedule",
    minWidth: "220px",
  },
  {
    field: "start_time",
    label: "Shift",
    minWidth: "150px",
    useSlot: true,
    slotName: "shift",
  },
  {
    field: "working_days",
    label: "Working Days",
    minWidth: "220px",
    useSlot: true,
    slotName: "working_days",
  },
  {
    field: "total_hours_per_day",
    label: "Hours / Day",
    width: "120px",
    useSlot: true,
    slotName: "hours",
  },
  {
    field: "is_default",
    label: "Status",
    width: "140px",
    useSlot: true,
    slotName: "status",
  },
  {
    field: "lifecycle",
    label: "Updated",
    minWidth: "180px",
    useSlot: true,
    slotName: "updated_at",
  },
  {
    field: "id",
    label: "Actions",
    operation: true,
    minWidth: "220px",
    fixed: "right",
    useSlot: true,
    slotName: "operation",
  },
];
const daySummary = computed(() =>
  form.working_days
    .slice()
    .sort((a, b) => a - b)
    .map(
      (day) =>
        DAYS.find((item) => item.value === day)?.fullLabel ?? String(day),
    ),
);

const weekendDays = computed(() =>
  DAYS.filter((day) => !form.working_days.includes(day.value)).map(
    (day) => day.value,
  ),
);

const workingHours = computed(() => {
  try {
    const start = toMinutes(form.start_time);
    const end = toMinutes(form.end_time);

    // Validate minutes
    if (Number.isNaN(start) || Number.isNaN(end)) return 0;
    if (end <= start) return 0;

    // Calculate hours
    const totalMinutes = end - start;
    return Number((totalMinutes / 60).toFixed(2));
  } catch {
    return 0;
  }
});

const formError = computed(() => {
  // Name validation
  if (!form.name.trim()) return "Schedule name is required.";
  if (form.name.trim().length < 2)
    return "Schedule name must be at least 2 characters.";
  if (form.name.trim().length > 100)
    return "Schedule name cannot exceed 100 characters.";

  // Time validation
  if (!form.start_time || !form.end_time)
    return "Start and end time are required.";

  const startMin = toMinutes(form.start_time);
  const endMin = toMinutes(form.end_time);

  if (Number.isNaN(startMin) || Number.isNaN(endMin)) {
    return "Invalid time format.";
  }

  if (endMin <= startMin) {
    return "End time must be later than start time.";
  }

  // Working days validation
  if (!form.working_days || form.working_days.length === 0) {
    return "Select at least one working day.";
  }

  if (
    !form.working_days.every((d) => typeof d === "number" && d >= 0 && d <= 6)
  ) {
    return "Invalid working day values.";
  }

  return "";
});

const hasFormChanged = computed(() => {
  if (!initialFormValues.value) return false;
  return JSON.stringify(form) !== JSON.stringify(initialFormValues.value);
});

const summaryCards = computed(() => {
  const active = schedules.value.filter((item) => !item.lifecycle?.deleted_at);
  const deleted = schedules.value.filter((item) => item.lifecycle?.deleted_at);
  const defaultSchedule = active.find((item) => item.is_default);

  return [
    { label: "Total schedules", value: schedules.value.length },
    { label: "Active schedules", value: active.length },
    { label: "Deleted schedules", value: deleted.length },
    {
      label: "Default schedule",
      value: defaultSchedule?.name ?? "Not set",
    },
  ];
});

const filteredSchedules = computed(() => {
  const keyword = q.value.trim().toLowerCase();

  return schedules.value
    .filter((item) => {
      const isDeleted = Boolean(item.lifecycle?.deleted_at);
      if (filter.value === "active" && isDeleted) return false;
      if (filter.value === "deleted" && !isDeleted) return false;
      if (!keyword) return true;

      // Search across multiple fields
      const searchableText = [
        item.name,
        item.start_time,
        item.end_time,
        ...item.working_days.map(
          (day) => DAYS.find((entry) => entry.value === day)?.fullLabel ?? "",
        ),
      ]
        .join(" ")
        .toLowerCase();

      return searchableText.includes(keyword);
    })
    .sort((a, b) => {
      // Sort: default first, then by name
      if (a.is_default !== b.is_default) return a.is_default ? -1 : 1;
      return a.name.localeCompare(b.name);
    });
});

const totalRows = computed(() => filteredSchedules.value.length);

const pagedSchedules = computed(() => {
  const start = (page.value - 1) * pageSize.value;
  return filteredSchedules.value.slice(start, start + pageSize.value);
});

function getDefaultForm(): ScheduleFormModel {
  return {
    name: "",
    start_time: "09:00:00",
    end_time: "17:00:00",
    working_days: [0, 1, 2, 3, 4],
    is_default: false,
  };
}

function resetForm() {
  Object.assign(form, getDefaultForm());
  initialFormValues.value = null;
}

function fillForm(schedule: WorkingScheduleDTO) {
  const normalized = {
    name: schedule.name,
    start_time: normalizeTime(schedule.start_time),
    end_time: normalizeTime(schedule.end_time),
    working_days: [...schedule.working_days].sort((a, b) => a - b),
    is_default: schedule.is_default,
  };
  Object.assign(form, normalized);
  initialFormValues.value = { ...normalized };
}

/**
 * Ensures time is always in HH:MM:SS format
 * Handles HH:MM, HH:MM:SS formats
 */
function normalizeTime(value: string): string {
  if (!value) return "00:00:00";

  const trimmed = value.trim();
  const parts = trimmed.split(":");

  if (parts.length === 2) {
    const [hour, minute] = parts;
    return `${hour.padStart(2, "0")}:${minute.padStart(2, "0")}:00`;
  } else if (parts.length === 3) {
    const [hour, minute, second] = parts;
    return `${hour.padStart(2, "0")}:${minute.padStart(
      2,
      "0",
    )}:${second.padStart(2, "0")}`;
  }

  // Fallback: return as-is if already in correct format
  return value;
}

/**
 * Converts HH:MM:SS or HH:MM to total minutes
 */
function toMinutes(value: string): number {
  try {
    const [hour = "0", minute = "0"] = value.split(":");
    return Number(hour) * 60 + Number(minute);
  } catch {
    return 0;
  }
}

/**
 * Format shift time display (HH:MM - HH:MM)
 */
function formatShift(schedule: WorkingScheduleDTO): string {
  try {
    const start = schedule.start_time.slice(0, 5);
    const end = schedule.end_time.slice(0, 5);
    return `${start} - ${end}`;
  } catch {
    return "-";
  }
}

/**
 * Format working days for display
 */
function formatDays(days: number[]): string {
  return days
    .slice()
    .sort((a, b) => a - b)
    .map((day) => DAYS.find((item) => item.value === day)?.label ?? String(day))
    .join(", ");
}

/**
 * Format date/time for display using locale settings
 */
function formatDate(value?: string | null): string {
  if (!value) return "-";
  try {
    return new Intl.DateTimeFormat("en-GB", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(value));
  } catch {
    return "-";
  }
}

function buildPayload(): WorkingScheduleCreateDTO | WorkingScheduleUpdateDTO {
  return {
    name: form.name.trim(),
    start_time: normalizeTime(form.start_time),
    end_time: normalizeTime(form.end_time),
    working_days: [...form.working_days].sort((a, b) => a - b),
    weekend_days: [...weekendDays.value],
    total_hours_per_day: workingHours.value,
    is_default: form.is_default,
  };
}

async function loadSchedules() {
  loading.value = true;
  try {
    schedules.value = await scheduleService.getSchedules();
    if (
      (page.value - 1) * pageSize.value >= totalRows.value &&
      page.value > 1
    ) {
      page.value = Math.max(1, Math.ceil(totalRows.value / pageSize.value));
    }
  } catch (error: any) {
    console.error("Load schedules error:", error);
  } finally {
    loading.value = false;
  }
}

function openCreateDialog() {
  dialogMode.value = "create";
  currentScheduleId.value = "";
  resetForm();
  dialogVisible.value = true;
}

function openEditDialog(schedule: WorkingScheduleDTO) {
  dialogMode.value = "edit";
  currentScheduleId.value = schedule.id;
  fillForm(schedule);
  dialogVisible.value = true;
}

function closeDialog() {
  dialogVisible.value = false;
  currentScheduleId.value = "";
  resetForm();
}

async function submitForm() {
  if (formError.value) {
    return;
  }

  saving.value = true;
  try {
    const payload = buildPayload();
    if (dialogMode.value === "create") {
      await scheduleService.createSchedule(payload as WorkingScheduleCreateDTO);
      page.value = 1;
    } else {
      await scheduleService.updateSchedule(
        currentScheduleId.value,
        payload as WorkingScheduleUpdateDTO,
      );
    }

    closeDialog();
    await loadSchedules();
  } catch (error: any) {
    const errorMessage =
      error?.data?.message || error?.message || "Failed to save schedule.";
    console.error("Submit form error:", error);
  } finally {
    saving.value = false;
  }
}

async function confirmDelete(schedule: WorkingScheduleDTO) {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete "${schedule.name}"? This action can be undone.`,
      "Delete schedule",
      {
        type: "warning",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      },
    );

    actionLoading.value[schedule.id] = true;
    await scheduleService.softDeleteSchedule(schedule.id);

    await loadSchedules();
  } catch (error: any) {
    if (error !== "cancel") {
    }
  } finally {
    actionLoading.value[schedule.id] = false;
  }
}

async function confirmRestore(schedule: WorkingScheduleDTO) {
  try {
    await ElMessageBox.confirm(
      `Restore "${schedule.name}"?`,
      "Restore schedule",
      {
        type: "info",
        confirmButtonText: "Restore",
        cancelButtonText: "Cancel",
      },
    );

    actionLoading.value[schedule.id] = true;
    await scheduleService.restoreSchedule(schedule.id);

    await loadSchedules();
  } catch (error: any) {
    if (error !== "cancel") {
      const errorMessage =
        error?.data?.message || error?.message || "Failed to restore schedule.";
      console.error("Restore error:", error);
    }
  } finally {
    actionLoading.value[schedule.id] = false;
  }
}

async function setAsDefault(schedule: WorkingScheduleDTO) {
  // Guard: can't set deleted items or already default items as default
  if (schedule.is_default || schedule.lifecycle?.deleted_at) {
    return;
  }

  submittingDefaultId.value = schedule.id;
  try {
    await scheduleService.updateSchedule(schedule.id, { is_default: true });
    await loadSchedules();
  } catch (error: any) {
    const errorMessage =
      error?.data?.message ||
      error?.message ||
      "Failed to set default schedule.";
    console.error("Set default error:", error);
  } finally {
    submittingDefaultId.value = null;
  }
}

function onFilterChange() {
  // Reset to first page when filter changes
  page.value = 1;
}

// Lifecycle hooks
onMounted(async () => {
  await loadSchedules();
});

// Watch for prop changes in form to ensure data consistency
watch(
  () => form.working_days,
  () => {
    // working_days has changed, validation will re-run via computed
  },
);
</script>

<template>
  <div class="schedule-page">
    <OverviewHeader
      :title="'Working Schedules'"
      :description="'Create and manage employee working schedules based on the HRMS service layer.'"
      :backPath="'/hr/config'"
    >
      <template #actions>
        <div class="schedule-header-actions">
          <BaseButton
            plain
            :loading="loading"
            class="schedule-header-btn schedule-header-btn--refresh"
            @click="loadSchedules"
          >
            Refresh
          </BaseButton>

          <BaseButton
            type="primary"
            class="schedule-header-btn"
            :disabled="loading"
            @click="openCreateDialog"
          >
            Add Schedule
          </BaseButton>
        </div>
      </template>
    </OverviewHeader>

    <div class="schedule-summary-grid">
      <div
        v-for="item in summaryCards"
        :key="item.label"
        class="schedule-summary-card"
      >
        <div class="schedule-summary-label">{{ item.label }}</div>
        <div class="schedule-summary-value">{{ item.value }}</div>
      </div>
    </div>

    <div class="schedule-toolbar">
      <el-input
        v-model="q"
        clearable
        placeholder="Search schedules, days, or shift time"
        @input="onFilterChange"
        @clear="onFilterChange"
      >
        <template #prefix>
          <i class="el-icon-search" />
        </template>
      </el-input>

      <el-segmented
        v-model="filter"
        :options="[
          { label: 'Active', value: 'active' },
          { label: 'Deleted', value: 'deleted' },
          { label: 'All', value: 'all' },
        ]"
        @change="onFilterChange"
      />
    </div>

    <div class="schedule-table-card">
      <SmartTable
        :columns="tableColumns"
        :data="pagedSchedules"
        :loading="loading"
        :total="totalRows"
        :page="page"
        :page-size="pageSize"
        @page="page = $event"
        @page-size="pageSize = $event"
      >
        <template #shift="{ row }">
          <div class="schedule-shift">
            <div class="schedule-shift-time">
              {{ formatShift(row as WorkingScheduleDTO) }}
            </div>
            <div class="schedule-shift-subtext">
              {{
                (row as WorkingScheduleDTO).is_default
                  ? "Primary schedule"
                  : "Standard schedule"
              }}
            </div>
          </div>
        </template>

        <template #working_days="{ row }">
          <div class="schedule-days">
            {{ formatDays((row as WorkingScheduleDTO).working_days) }}
          </div>
        </template>

        <template #hours="{ row }">
          <span>{{
            Number(
              (row as WorkingScheduleDTO).total_hours_per_day || 0,
            ).toFixed(2)
          }}</span>
        </template>

        <template #status="{ row }">
          <el-space size="small">
            <el-tag
              :type="(row as WorkingScheduleDTO).lifecycle?.deleted_at ? 'danger' : 'success'"
              size="small"
            >
              {{
                (row as WorkingScheduleDTO).lifecycle?.deleted_at
                  ? "Deleted"
                  : "Active"
              }}
            </el-tag>
            <el-tag
              v-if="(row as WorkingScheduleDTO).is_default"
              type="warning"
              size="small"
            >
              Default
            </el-tag>
          </el-space>
        </template>

        <template #updated_at="{ row }">
          {{ formatDate((row as WorkingScheduleDTO).lifecycle?.updated_at) }}
        </template>

        <template #operation="{ row }">
          <el-space wrap>
            <el-button
              v-if="!(row as WorkingScheduleDTO).lifecycle?.deleted_at"
              type="primary"
              link
              size="small"
              @click="openEditDialog(row as WorkingScheduleDTO)"
            >
              Edit
            </el-button>

            <el-button
              v-if="!(row as WorkingScheduleDTO).lifecycle?.deleted_at && !(row as WorkingScheduleDTO).is_default"
              type="warning"
              link
              size="small"
              :loading="submittingDefaultId === (row as WorkingScheduleDTO).id"
              @click="setAsDefault(row as WorkingScheduleDTO)"
            >
              Set Default
            </el-button>

            <el-button
              v-if="(row as WorkingScheduleDTO).lifecycle?.deleted_at"
              type="success"
              link
              size="small"
              :loading="actionLoading[(row as WorkingScheduleDTO).id]"
              @click="confirmRestore(row as WorkingScheduleDTO)"
            >
              Restore
            </el-button>

            <el-button
              v-else
              type="danger"
              link
              size="small"
              :disabled="(row as WorkingScheduleDTO).is_default"
              :loading="actionLoading[(row as WorkingScheduleDTO).id]"
              @click="confirmDelete(row as WorkingScheduleDTO)"
            >
              Delete
            </el-button>
          </el-space>
        </template>
      </SmartTable>

      <div v-if="!loading && totalRows === 0" class="schedule-empty-state">
        <div class="schedule-empty-title">No schedules found</div>
        <div class="schedule-empty-text">
          Try changing the filter or create a new working schedule.
        </div>
      </div>
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="
        dialogMode === 'create'
          ? 'Add Working Schedule'
          : 'Edit Working Schedule'
      "
      width="720px"
      destroy-on-close
      @closed="closeDialog"
    >
      <div class="schedule-dialog-layout">
        <div class="schedule-form-panel">
          <el-form label-position="top">
            <el-form-item label="Schedule Name" required>
              <el-input
                v-model="form.name"
                maxlength="100"
                placeholder="Morning Shift, Office Hours, Weekend Team..."
              />
            </el-form-item>

            <div class="schedule-time-grid">
              <el-form-item label="Start Time" required>
                <el-time-select
                  v-model="form.start_time"
                  start="00:00"
                  step="00:30"
                  end="23:30"
                  format="HH:mm"
                  value-format="HH:mm:ss"
                  placeholder="Select start time"
                />
              </el-form-item>

              <el-form-item label="End Time" required>
                <el-time-select
                  v-model="form.end_time"
                  start="00:30"
                  step="00:30"
                  end="23:59"
                  format="HH:mm"
                  value-format="HH:mm:ss"
                  placeholder="Select end time"
                />
              </el-form-item>
            </div>

            <el-form-item label="Working Days" required>
              <div class="schedule-day-picker">
                <el-check-tag
                  v-for="day in DAYS"
                  :key="day.value"
                  :checked="form.working_days.includes(day.value)"
                  @change="
                    (checked: boolean) => {
                      form.working_days = checked
                        ? [...form.working_days, day.value].sort(
                            (a, b) => a - b,
                          )
                        : form.working_days.filter(
                            (value) => value !== day.value,
                          );
                    }
                  "
                >
                  {{ day.fullLabel }}
                </el-check-tag>
              </div>
            </el-form-item>

            <el-form-item label="Default Schedule">
              <el-switch v-model="form.is_default" />
            </el-form-item>
          </el-form>
        </div>

        <div class="schedule-preview-panel">
          <div class="schedule-preview-title">Backend-aligned preview</div>
          <div class="schedule-preview-item">
            <span>Shift</span>
            <strong
              >{{ form.start_time.slice(0, 5) }} -
              {{ form.end_time.slice(0, 5) }}</strong
            >
          </div>
          <div class="schedule-preview-item">
            <span>Working days</span>
            <strong>{{ daySummary.join(", ") || "-" }}</strong>
          </div>
          <div class="schedule-preview-item">
            <span>Weekend days</span>
            <strong>{{ formatDays(weekendDays) || "-" }}</strong>
          </div>
          <div class="schedule-preview-item">
            <span>Total hours / day</span>
            <strong>{{ workingHours.toFixed(2) }}</strong>
          </div>
          <div class="schedule-preview-note">
            This form sends `name`, `start_time`, `end_time`, `working_days`,
            `weekend_days`, `total_hours_per_day`, and `is_default` so it stays
            consistent with your current backend contract.
          </div>

          <el-alert
            v-if="formError"
            :title="formError"
            type="warning"
            :closable="false"
            show-icon
          />
        </div>
      </div>

      <template #footer>
        <el-space>
          <BaseButton plain @click="closeDialog">Cancel</BaseButton>
          <BaseButton type="primary" :loading="saving" @click="submitForm">
            {{ dialogMode === "create" ? "Create Schedule" : "Save Changes" }}
          </BaseButton>
        </el-space>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.schedule-page {
  display: grid;
  gap: 20px;
}

.schedule-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.schedule-header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 10px;
}

.schedule-header-btn {
  min-height: 36px;
  border-radius: 10px;
  font-weight: 650;
}

.schedule-header-btn--refresh {
  border-color: color-mix(
    in srgb,
    var(--border-color) 60%,
    var(--color-primary) 40%
  ) !important;
  color: color-mix(
    in srgb,
    var(--text-color) 82%,
    var(--color-primary) 18%
  ) !important;
  background: color-mix(
    in srgb,
    var(--color-card) 94%,
    var(--color-bg) 6%
  ) !important;
}

.schedule-header-btn--refresh:hover:not(.is-disabled):not([disabled]) {
  background: var(--hover-bg) !important;
  border-color: color-mix(
    in srgb,
    var(--border-color) 48%,
    var(--color-primary) 52%
  ) !important;
}

.schedule-summary-card {
  padding: 18px 20px;
  border: 1px solid var(--el-border-color-light);
  border-radius: 18px;
  background: linear-gradient(
      135deg,
      color-mix(in srgb, var(--el-color-primary) 6%, transparent),
      color-mix(in srgb, var(--button-success-bg) 10%, transparent)
    ),
    var(--color-card);
}

.schedule-summary-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--el-text-color-secondary);
  margin-bottom: 8px;
}

.schedule-summary-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--el-text-color-primary);
}

.schedule-toolbar {
  display: grid;
  grid-template-columns: minmax(260px, 420px) auto;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

.schedule-table-card {
  position: relative;
  padding: 8px;
  border: 1px solid var(--el-border-color-light);
  border-radius: 20px;
  background: var(--color-card);
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
}

.schedule-shift-time {
  font-weight: 600;
}

.schedule-shift-subtext {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.schedule-days {
  line-height: 1.5;
}

.schedule-empty-state {
  padding: 24px 16px 8px;
  text-align: center;
}

.schedule-empty-title {
  font-weight: 700;
  margin-bottom: 6px;
}

.schedule-empty-text {
  color: var(--el-text-color-secondary);
}

.schedule-dialog-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(280px, 1fr);
  gap: 20px;
}

.schedule-form-panel,
.schedule-preview-panel {
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 18px;
  padding: 18px;
  background: var(--color-card);
}

.schedule-preview-panel {
  background: radial-gradient(
      circle at top right,
      color-mix(in srgb, var(--button-warning-bg) 12%, transparent),
      transparent 42%
    ),
    linear-gradient(
      180deg,
      color-mix(in srgb, var(--button-warning-bg) 10%, var(--color-card) 90%),
      var(--color-card)
    );
}

.schedule-preview-title {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 16px;
}

.schedule-preview-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed var(--el-border-color);
}

.schedule-preview-item span {
  color: var(--el-text-color-secondary);
}

.schedule-preview-item strong {
  text-align: right;
}

.schedule-preview-note {
  margin: 16px 0;
  font-size: 13px;
  line-height: 1.6;
  color: var(--el-text-color-secondary);
}

.schedule-time-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.schedule-day-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

@media (max-width: 1024px) {
  .schedule-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .schedule-toolbar,
  .schedule-dialog-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .schedule-header-actions {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr;
  }

  .schedule-header-btn {
    width: 100%;
  }

  .schedule-summary-grid {
    grid-template-columns: 1fr;
  }

  .schedule-time-grid {
    grid-template-columns: 1fr;
  }
}
</style>

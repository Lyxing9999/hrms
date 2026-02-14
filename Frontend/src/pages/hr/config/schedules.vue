<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { WorkingScheduleDTO } from "~/api/hr_admin/schedule/schedule.dto";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { ElMessageBox } from "element-plus";
import { usePreferencesStore } from "~/stores/preferencesStore";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import { useFormCreate } from "~/composables/forms/useFormCreate";

const { $hrScheduleService } = useNuxtApp();

const detailLoading = ref<Record<string | number, boolean>>({});
const deleteLoading = ref<Record<string | number, boolean>>({});
const restoreLoading = ref<Record<string | number, boolean>>({});

const q = ref("");
const include_deleted = ref(false);
const deleted_only = ref(false);

// Table columns
const scheduleColumns = [
  { prop: "name", label: "Schedule Name", minWidth: 180 },
  { prop: "start_time", label: "Start Time", width: 120 },
  { prop: "end_time", label: "End Time", width: 120 },
  { 
    prop: "working_days", 
    label: "Working Days", 
    minWidth: 200,
    formatter: (row: any) => {
      const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
      return row.working_days.map((d: number) => days[d]).join(', ');
    }
  },
  { prop: "total_hours_per_day", label: "Hours/Day", width: 100 },
  { 
    prop: "is_default", 
    label: "Default", 
    width: 100,
    slot: "is_default"
  },
  { prop: "operation", label: "Actions", width: 200, fixed: "right", slot: "operation" },
];

// Fetch data
const {
  data: schedules,
  error: tableError,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = usePaginatedFetch<WorkingScheduleDTO, void>(
  async (_unusedFilter, page, size, signal) => {
    const keyword = q.value.trim();
    const res = await $hrScheduleService.getSchedules({
      q: keyword.length ? keyword : undefined,
      page,
      limit: size,
      include_deleted: include_deleted.value,
      deleted_only: deleted_only.value,
      signal,
    });

    return {
      items: (res.items ?? []) as WorkingScheduleDTO[],
      total: res.total ?? 0,
    };
  },
  { initialPage: 1 }
);

watch([q, include_deleted, deleted_only], () => {
  fetchPage(1);
});

// Form schema
const scheduleFormSchema = [
  {
    prop: "name",
    label: "Schedule Name",
    type: "input",
    required: true,
    placeholder: "e.g., Standard 9-5",
  },
  {
    prop: "start_time",
    label: "Start Time",
    type: "time",
    required: true,
    format: "HH:mm:ss",
  },
  {
    prop: "end_time",
    label: "End Time",
    type: "time",
    required: true,
    format: "HH:mm:ss",
  },
  {
    prop: "working_days",
    label: "Working Days",
    type: "checkbox-group",
    required: true,
    options: [
      { label: "Monday", value: 0 },
      { label: "Tuesday", value: 1 },
      { label: "Wednesday", value: 2 },
      { label: "Thursday", value: 3 },
      { label: "Friday", value: 4 },
      { label: "Saturday", value: 5 },
      { label: "Sunday", value: 6 },
    ],
  },
  {
    prop: "is_default",
    label: "Set as Default Schedule",
    type: "switch",
  },
];

// Create form
const {
  formDialogVisible: createFormVisible,
  formData: createFormData,
  schema: createFormSchema,
  saveForm: saveCreateForm,
  cancelForm: cancelCreateForm,
  openForm: openCreateForm,
  loading: createFormLoading,
} = useFormCreate(
  () => async (data: any) => {
    return await $hrScheduleService.createSchedule(data);
  },
  () => ({
    name: "",
    start_time: "09:00:00",
    end_time: "17:00:00",
    working_days: [0, 1, 2, 3, 4], // Mon-Fri
    is_default: false,
  }),
  () => scheduleFormSchema
);

const handleCreateSave = async (form: any) => {
  const created = await saveCreateForm(form);
  if (created) await fetchPage(1);
};

const createDialogKey = ref(0);

const handleOpenCreateForm = async () => {
  createDialogKey.value++;
  await openCreateForm({});
};

// Update form
const updateFormVisible = ref(false);
const updateFormData = ref<any>({});
const updateFormLoading = ref(false);
const currentScheduleId = ref<string>("");

const handleOpenUpdateForm = async (row: WorkingScheduleDTO) => {
  currentScheduleId.value = row.id;
  updateFormData.value = {
    name: row.name,
    start_time: row.start_time,
    end_time: row.end_time,
    working_days: row.working_days,
    is_default: row.is_default,
  };
  updateFormVisible.value = true;
};

const handleUpdateSave = async (form: any) => {
  updateFormLoading.value = true;
  try {
    await $hrScheduleService.updateSchedule(currentScheduleId.value, form);
    updateFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    updateFormLoading.value = false;
  }
};

// Delete
const handleSoftDeleteSchedule = async (row: WorkingScheduleDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to delete this schedule?",
      "Warning",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "warning" }
    );

    deleteLoading.value[row.id] = true;
    await $hrScheduleService.softDeleteSchedule(row.id);

    const page = currentPage.value || 1;
    await fetchPage(page);

    if (page > 1 && (schedules.value?.length ?? 0) === 0) {
      await fetchPage(page - 1);
    }
  } finally {
    deleteLoading.value[row.id] = false;
  }
};

// Restore
const handleRestoreSchedule = async (row: WorkingScheduleDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to restore this schedule?",
      "Confirm Restore",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "info" }
    );

    restoreLoading.value[row.id] = true;
    await $hrScheduleService.restoreSchedule(row.id);

    const page = currentPage.value || 1;
    await fetchPage(page);
  } finally {
    restoreLoading.value[row.id] = false;
  }
};

// Initial load
await fetchPage(1);
</script>

<template>
  <OverviewHeader
    :title="'Working Schedules'"
    :description="'Manage working hours and days for employees'"
    :backPath="'/hr/config'"
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

      <BaseButton
        type="primary"
        :disabled="initialLoading || fetching"
        @click="handleOpenCreateForm"
      >
        Add Schedule
      </BaseButton>
    </template>
  </OverviewHeader>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="6">
      <el-input
        v-model="q"
        placeholder="Search by name..."
        clearable
        @clear="fetchPage(1)"
      />
    </el-col>
    <el-col :span="4">
      <el-checkbox v-model="include_deleted" @change="fetchPage(1)">
        Include Deleted
      </el-checkbox>
    </el-col>
    <el-col :span="4">
      <el-checkbox v-model="deleted_only" @change="fetchPage(1)">
        Deleted Only
      </el-checkbox>
    </el-col>
  </el-row>

  <SmartTable
    :columns="scheduleColumns"
    :data="schedules"
    :loading="initialLoading || fetching"
    :total="totalRows"
    :page="currentPage"
    :page-size="pageSize"
    @page="goPage"
    @page-size="setPageSize"
  >
    <template #is_default="{ row }">
      <el-tag v-if="row.is_default" type="success" size="small">Default</el-tag>
      <span v-else class="text-gray-400">-</span>
    </template>

    <template #operation="{ row }">
      <el-space>
        <!-- Edit Button -->
        <el-button
          type="primary"
          size="small"
          link
          :loading="detailLoading[row.id]"
          @click="handleOpenUpdateForm(row as WorkingScheduleDTO)"
        >
          Edit
        </el-button>

        <!-- Restore Button (only for deleted schedules) -->
        <el-button
          v-if="row.lifecycle?.deleted_at"
          type="success"
          size="small"
          link
          :loading="restoreLoading[row.id]"
          @click="handleRestoreSchedule(row as WorkingScheduleDTO)"
        >
          Restore
        </el-button>

        <!-- Delete Button (only for non-deleted schedules) -->
        <el-button
          v-else
          type="danger"
          size="small"
          link
          :loading="deleteLoading[row.id]"
          @click="handleSoftDeleteSchedule(row as WorkingScheduleDTO)"
        >
          Delete
        </el-button>
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

  <!-- Create Schedule Dialog -->
  <SmartFormDialog
    :key="createDialogKey"
    v-model:visible="createFormVisible"
    :model-value="createFormData"
    :fields="createFormSchema"
    :width="'40%'"
    :loading="createFormLoading"
    :disabled="createFormLoading"
    title="Add Working Schedule"
    useElForm
    @save="handleCreateSave"
    @cancel="cancelCreateForm"
  />

  <!-- Update Schedule Dialog -->
  <SmartFormDialog
    v-model:visible="updateFormVisible"
    :model-value="updateFormData"
    :fields="scheduleFormSchema"
    :width="'40%'"
    :loading="updateFormLoading"
    :disabled="updateFormLoading"
    title="Update Working Schedule"
    useElForm
    @save="handleUpdateSave"
    @cancel="updateFormVisible = false"
  />
</template>

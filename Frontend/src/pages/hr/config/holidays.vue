<script setup lang="ts">
import { ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { PublicHolidayDTO } from "~/api/hr_admin/holiday/holiday.dto";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { ElMessageBox } from "element-plus";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import { useFormCreate } from "~/composables/forms/useFormCreate";

const { $hrHolidayService } = useNuxtApp();

const deleteLoading = ref<Record<string | number, boolean>>({});
const restoreLoading = ref<Record<string | number, boolean>>({});

const q = ref("");
const year = ref<number | undefined>(new Date().getFullYear());
const include_deleted = ref(false);
const deleted_only = ref(false);

// Table columns
const holidayColumns = [
  { prop: "name", label: "Holiday Name", minWidth: 200 },
  { prop: "name_kh", label: "Khmer Name", minWidth: 150 },
  { prop: "date", label: "Date", width: 120 },
  { prop: "is_paid", label: "Paid", width: 100, slot: "is_paid" },
  { prop: "description", label: "Description", minWidth: 200 },
  { prop: "operation", label: "Actions", width: 200, fixed: "right", slot: "operation" },
];

// Fetch data
const {
  data: holidays,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = usePaginatedFetch<PublicHolidayDTO, void>(
  async (_unusedFilter, page, size, signal) => {
    const keyword = q.value.trim();
    const res = await $hrHolidayService.getHolidays({
      q: keyword.length ? keyword : undefined,
      page,
      limit: size,
      year: year.value,
      include_deleted: include_deleted.value,
      deleted_only: deleted_only.value,
      signal,
    });

    return {
      items: (res.items ?? []) as PublicHolidayDTO[],
      total: res.total ?? 0,
    };
  },
  { initialPage: 1 }
);

watch([q, year, include_deleted, deleted_only], () => {
  fetchPage(1);
});

// Form schema
const holidayFormSchema = [
  {
    prop: "name",
    label: "Holiday Name",
    type: "input",
    required: true,
    placeholder: "e.g., New Year's Day",
  },
  {
    prop: "name_kh",
    label: "Khmer Name",
    type: "input",
    placeholder: "ឈ្មោះជាភាសាខ្មែរ",
  },
  {
    prop: "date",
    label: "Date",
    type: "date",
    required: true,
    format: "YYYY-MM-DD",
  },
  {
    prop: "is_paid",
    label: "Paid Holiday",
    type: "switch",
  },
  {
    prop: "description",
    label: "Description",
    type: "textarea",
    placeholder: "Optional description",
    rows: 3,
  },
];

// Create form
const {
  formDialogVisible: createFormVisible,
  formData: createFormData,
  saveForm: saveCreateForm,
  openForm: openCreateForm,
  loading: createFormLoading,
} = useFormCreate(
  () => async (data: any) => {
    return await $hrHolidayService.createHoliday(data);
  },
  () => ({
    name: "",
    name_kh: "",
    date: "",
    is_paid: true,
    description: "",
  }),
  () => holidayFormSchema
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
const currentHolidayId = ref<string>("");

const handleOpenUpdateForm = async (row: PublicHolidayDTO) => {
  currentHolidayId.value = row.id;
  updateFormData.value = {
    name: row.name,
    name_kh: row.name_kh || "",
    date: row.date,
    is_paid: row.is_paid,
    description: row.description || "",
  };
  updateFormVisible.value = true;
};

const handleUpdateSave = async (form: any) => {
  updateFormLoading.value = true;
  try {
    await $hrHolidayService.updateHoliday(currentHolidayId.value, form);
    updateFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    updateFormLoading.value = false;
  }
};

// Delete
const handleSoftDeleteHoliday = async (row: PublicHolidayDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to delete this holiday?",
      "Warning",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "warning" }
    );

    deleteLoading.value[row.id] = true;
    await $hrHolidayService.softDeleteHoliday(row.id);
    await fetchPage(currentPage.value || 1);
  } finally {
    deleteLoading.value[row.id] = false;
  }
};

// Restore
const handleRestoreHoliday = async (row: PublicHolidayDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to restore this holiday?",
      "Confirm Restore",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "info" }
    );

    restoreLoading.value[row.id] = true;
    await $hrHolidayService.restoreHoliday(row.id);
    await fetchPage(currentPage.value || 1);
  } finally {
    restoreLoading.value[row.id] = false;
  }
};

// Initial load
await fetchPage(1);
</script>

<template>
  <OverviewHeader
    :title="'Public Holidays'"
    :description="'Manage public holidays for payroll and leave calculations'"
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
        Add Holiday
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
      <el-input-number
        v-model="year"
        placeholder="Year"
        :min="2000"
        :max="2100"
        controls-position="right"
        @change="fetchPage(1)"
      />
    </el-col>
    <el-col :span="4">
      <el-checkbox v-model="include_deleted" @change="fetchPage(1)">
        Include Deleted
      </el-checkbox>
    </el-col>
  </el-row>

  <SmartTable
    :columns="holidayColumns"
    :data="holidays"
    :loading="initialLoading || fetching"
    :total="totalRows"
    :page="currentPage"
    :page-size="pageSize"
    @page="goPage"
    @page-size="setPageSize"
  >
    <template #is_paid="{ row }">
      <el-tag v-if="row.is_paid" type="success" size="small">Paid</el-tag>
      <el-tag v-else type="info" size="small">Unpaid</el-tag>
    </template>

    <template #operation="{ row }">
      <el-space>
        <el-button
          type="primary"
          size="small"
          link
          @click="handleOpenUpdateForm(row as PublicHolidayDTO)"
        >
          Edit
        </el-button>

        <el-button
          v-if="row.lifecycle?.deleted_at"
          type="success"
          size="small"
          link
          :loading="restoreLoading[row.id]"
          @click="handleRestoreHoliday(row as PublicHolidayDTO)"
        >
          Restore
        </el-button>

        <el-button
          v-else
          type="danger"
          size="small"
          link
          :loading="deleteLoading[row.id]"
          @click="handleSoftDeleteHoliday(row as PublicHolidayDTO)"
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

  <!-- Create Dialog -->
  <SmartFormDialog
    :key="createDialogKey"
    v-model:visible="createFormVisible"
    :model-value="createFormData"
    :fields="holidayFormSchema"
    :width="'40%'"
    :loading="createFormLoading"
    :disabled="createFormLoading"
    title="Add Public Holiday"
    useElForm
    @save="handleCreateSave"
  />

  <!-- Update Dialog -->
  <SmartFormDialog
    v-model:visible="updateFormVisible"
    :model-value="updateFormData"
    :fields="holidayFormSchema"
    :width="'40%'"
    :loading="updateFormLoading"
    :disabled="updateFormLoading"
    title="Update Public Holiday"
    useElForm
    @save="handleUpdateSave"
    @cancel="updateFormVisible = false"
  />
</template>

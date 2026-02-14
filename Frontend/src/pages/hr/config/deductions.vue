<script setup lang="ts">
import { ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { DeductionRuleDTO, DeductionType } from "~/api/hr_admin/deduction/deduction.dto";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { ElMessageBox } from "element-plus";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import { useFormCreate } from "~/composables/forms/useFormCreate";

const { $hrDeductionService } = useNuxtApp();

const deleteLoading = ref<Record<string | number, boolean>>({});
const restoreLoading = ref<Record<string | number, boolean>>({});

const type = ref<DeductionType | undefined>(undefined);
const is_active = ref<boolean | undefined>(undefined);
const include_deleted = ref(false);
const deleted_only = ref(false);

// Table columns
const deductionColumns = [
  { 
    prop: "type", 
    label: "Type", 
    width: 120,
    formatter: (row: any) => {
      const typeMap: Record<string, string> = {
        late: "Late",
        absent: "Absent",
        early_leave: "Early Leave"
      };
      return typeMap[row.type] || row.type;
    }
  },
  { prop: "min_minutes", label: "Min Minutes", width: 120 },
  { prop: "max_minutes", label: "Max Minutes", width: 120 },
  { 
    prop: "deduction_percentage", 
    label: "Deduction %", 
    width: 120,
    formatter: (row: any) => `${row.deduction_percentage}%`
  },
  { prop: "is_active", label: "Status", width: 100, slot: "is_active" },
  { prop: "operation", label: "Actions", width: 200, fixed: "right", slot: "operation" },
];

// Fetch data
const {
  data: deductions,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = usePaginatedFetch<DeductionRuleDTO, void>(
  async (_unusedFilter, page, size, signal) => {
    const res = await $hrDeductionService.getDeductions({
      page,
      limit: size,
      type: type.value,
      is_active: is_active.value,
      include_deleted: include_deleted.value,
      deleted_only: deleted_only.value,
      signal,
    });

    return {
      items: (res.items ?? []) as DeductionRuleDTO[],
      total: res.total ?? 0,
    };
  },
  { initialPage: 1 }
);

watch([type, is_active, include_deleted, deleted_only], () => {
  fetchPage(1);
});

// Form schema
const deductionFormSchema = [
  {
    prop: "type",
    label: "Deduction Type",
    type: "select",
    required: true,
    options: [
      { label: "Late", value: "late" },
      { label: "Absent", value: "absent" },
      { label: "Early Leave", value: "early_leave" },
    ],
  },
  {
    prop: "min_minutes",
    label: "Minimum Minutes",
    type: "number",
    required: true,
    placeholder: "e.g., 0",
    min: 0,
  },
  {
    prop: "max_minutes",
    label: "Maximum Minutes",
    type: "number",
    required: true,
    placeholder: "e.g., 30",
    min: 0,
  },
  {
    prop: "deduction_percentage",
    label: "Deduction Percentage",
    type: "number",
    required: true,
    placeholder: "e.g., 10",
    min: 0,
    max: 100,
    step: 0.01,
  },
  {
    prop: "is_active",
    label: "Active",
    type: "switch",
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
    return await $hrDeductionService.createDeduction(data);
  },
  () => ({
    type: "late" as DeductionType,
    min_minutes: 0,
    max_minutes: 30,
    deduction_percentage: 10,
    is_active: true,
  }),
  () => deductionFormSchema
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
const currentDeductionId = ref<string>("");

const handleOpenUpdateForm = async (row: DeductionRuleDTO) => {
  currentDeductionId.value = row.id;
  updateFormData.value = {
    type: row.type,
    min_minutes: row.min_minutes,
    max_minutes: row.max_minutes,
    deduction_percentage: row.deduction_percentage,
    is_active: row.is_active,
  };
  updateFormVisible.value = true;
};

const handleUpdateSave = async (form: any) => {
  updateFormLoading.value = true;
  try {
    await $hrDeductionService.updateDeduction(currentDeductionId.value, form);
    updateFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    updateFormLoading.value = false;
  }
};

// Delete
const handleSoftDeleteDeduction = async (row: DeductionRuleDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to delete this deduction rule?",
      "Warning",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "warning" }
    );

    deleteLoading.value[row.id] = true;
    await $hrDeductionService.softDeleteDeduction(row.id);
    await fetchPage(currentPage.value || 1);
  } finally {
    deleteLoading.value[row.id] = false;
  }
};

// Restore
const handleRestoreDeduction = async (row: DeductionRuleDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to restore this deduction rule?",
      "Confirm Restore",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "info" }
    );

    restoreLoading.value[row.id] = true;
    await $hrDeductionService.restoreDeduction(row.id);
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
    :title="'Deduction Rules'"
    :description="'Manage payroll deduction rules for late, absent, and early leave'"
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
        Add Rule
      </BaseButton>
    </template>
  </OverviewHeader>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="4">
      <el-select
        v-model="type"
        placeholder="Filter by type"
        clearable
        @change="fetchPage(1)"
      >
        <el-option label="Late" value="late" />
        <el-option label="Absent" value="absent" />
        <el-option label="Early Leave" value="early_leave" />
      </el-select>
    </el-col>
    <el-col :span="4">
      <el-select
        v-model="is_active"
        placeholder="Filter by status"
        clearable
        @change="fetchPage(1)"
      >
        <el-option label="Active" :value="true" />
        <el-option label="Inactive" :value="false" />
      </el-select>
    </el-col>
    <el-col :span="4">
      <el-checkbox v-model="include_deleted" @change="fetchPage(1)">
        Include Deleted
      </el-checkbox>
    </el-col>
  </el-row>

  <SmartTable
    :columns="deductionColumns"
    :data="deductions"
    :loading="initialLoading || fetching"
    :total="totalRows"
    :page="currentPage"
    :page-size="pageSize"
    @page="goPage"
    @page-size="setPageSize"
  >
    <template #is_active="{ row }">
      <el-tag v-if="row.is_active" type="success" size="small">Active</el-tag>
      <el-tag v-else type="info" size="small">Inactive</el-tag>
    </template>

    <template #operation="{ row }">
      <el-space>
        <el-button
          type="primary"
          size="small"
          link
          @click="handleOpenUpdateForm(row as DeductionRuleDTO)"
        >
          Edit
        </el-button>

        <el-button
          v-if="row.lifecycle?.deleted_at"
          type="success"
          size="small"
          link
          :loading="restoreLoading[row.id]"
          @click="handleRestoreDeduction(row as DeductionRuleDTO)"
        >
          Restore
        </el-button>

        <el-button
          v-else
          type="danger"
          size="small"
          link
          :loading="deleteLoading[row.id]"
          @click="handleSoftDeleteDeduction(row as DeductionRuleDTO)"
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
    :fields="deductionFormSchema"
    :width="'40%'"
    :loading="createFormLoading"
    :disabled="createFormLoading"
    title="Add Deduction Rule"
    useElForm
    @save="handleCreateSave"
  />

  <!-- Update Dialog -->
  <SmartFormDialog
    v-model:visible="updateFormVisible"
    :model-value="updateFormData"
    :fields="deductionFormSchema"
    :width="'40%'"
    :loading="updateFormLoading"
    :disabled="updateFormLoading"
    title="Update Deduction Rule"
    useElForm
    @save="handleUpdateSave"
    @cancel="updateFormVisible = false"
  />
</template>

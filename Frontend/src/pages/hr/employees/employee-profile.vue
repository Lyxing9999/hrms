<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import { useNuxtApp, useRouter } from "nuxt/app";
import { useMessage } from "~/composables/common/useMessage";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { ColumnConfig } from "~/components/types/tableEdit";
import type { HrEmployeeDTO, HrCreateEmployeeDTO } from "~/api/hr_admin/employee/employee.dto";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { ElInput, ElButton, ElAvatar } from "element-plus";

import { usePreferencesStore } from "~/stores/preferencesStore";
import ActionButtons from "~/components/buttons/ActionButtons.vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import { getEmployeeFormDataFlat, getEmployeeFormDataEditFlat, employeeToFormFlat } from "~/modules/forms/hr_admin/employee/";
import type { employeeToFormFlat as EmployeeToFormFlatType } from "~/modules/forms/hr_admin/employee/";
import { employeeFormSchema } from "~/modules/forms/hr_admin/employee/";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
const nuxtApp = useNuxtApp();
const $hrEmployeeService = nuxtApp.$hrEmployeeService;

import { employeeColumns } from "~/modules/tables/columns/hr_admin/employeeColumns";
import { useFormCreate } from "~/composables/forms/useFormCreate";

const detailLoading = ref<Record<string | number, boolean>>({});
const deleteLoading = ref<Record<string | number, boolean>>({});

const q = ref("");
const include_deleted = ref(false);
const deleted_only = ref(false);
import { useEmployeeCreateWithPhoto } from "~/modules/forms/hr_admin/employee/employee.service";


const {
  data: employees,
  error: tableError,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = usePaginatedFetch<HrEmployeeDTO, void>(
  async (_unusedFilter, page, size, signal) => {
    const keyword = q.value.trim(); 
    const res = await $hrEmployeeService.getEmployees({
      q: keyword.length ? keyword : undefined,
      page,
      limit: size,
      include_deleted: include_deleted.value,
      deleted_only: deleted_only.value,
      // if your service supports AbortSignal:
      signal,
    });

    return {
      items: (res.items ?? []) as HrEmployeeDTO[],
      total: res.total ?? 0,
    };
  },
  { initialPage: 1 }
);

watch([q, include_deleted, deleted_only], () => {
  fetchPage(1);
});


const handleCreateSave = async (form: employeeToFormFlat) => {
  const created = await saveCreateForm(form);
  if (created) await fetchPage(1);
};

// Update Employee
const updateFormVisible = ref(false);
const updateFormData = ref<any>({});
const updateFormLoading = ref(false);
const currentEmployeeId = ref<string>("");

const handleOpenUpdateForm = async (row: HrEmployeeDTO) => {
  currentEmployeeId.value = row.id;
  updateFormData.value = employeeToFormFlat(row);
  updateFormVisible.value = true;
};

const handleUpdateSave = async (form: any) => {
  updateFormLoading.value = true;
  try {
    await $hrEmployeeService.updateEmployee(currentEmployeeId.value, form);
    updateFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    updateFormLoading.value = false;
  }
};

// Restore Employee
const restoreLoading = ref<Record<string | number, boolean>>({});

const handleRestoreEmployee = async (row: HrEmployeeDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to restore this employee?",
      "Confirm Restore",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "info" }
    );

    restoreLoading.value[row.id] = true;
    await $hrEmployeeService.restoreEmployee(row.id);

    const page = currentPage.value || 1;
    await fetchPage(page);
  } finally {
    restoreLoading.value[row.id] = false;
  }
};


const {
  formDialogVisible: createFormVisible,
  formData: createFormData,
  schema: baseCreateFormSchema,
  saveForm: saveCreateForm,
  cancelForm: cancelCreateForm,
  openForm: openCreateForm,
  loading: createFormLoading,
} = useFormCreate(
  () => useEmployeeCreateWithPhoto($hrEmployeeService),      
  () => getEmployeeFormDataFlat(),     
  () => employeeFormSchema
);
// initial load
await fetchPage(1);

const createDialogKey = ref(0);

const departmentFilter = ref<string | null>(null);
const positionFilter = ref<string | null>(null);

const handleOpenCreateForm = async () => {
  createDialogKey.value++;
  
  const payload: any = {
    // prefill (optional)
    department: departmentFilter.value,
    position: positionFilter.value,

    // lock flags (optional — your SmartForm can read these)
    __lock_department: !!departmentFilter.value,
    __lock_position: !!positionFilter.value,
  };

  await openCreateForm(payload);
};

const openEmployeeDetail = async (row: HrEmployeeDTO) => {
  detailLoading.value[row.id] = true;
  try {
    // OPTION A: navigate to detail page (if you have it)
    // const router = useRouter();
    // router.push(`/hr/employees/${row.id}`);

    // Navigate to employee detail page
    // Note: Detail view functionality can be added here if needed
  } finally {
    detailLoading.value[row.id] = false;
  }
};

import { ElMessageBox } from "element-plus";
// (you already import element-plus stuff)

async function handleSoftDeleteEmployee(row: HrEmployeeDTO) {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to soft delete this employee?",
      "Warning",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "warning" }
    );

    deleteLoading.value[row.id] = true;

    await $hrEmployeeService.softDeleteEmployee(row.id);

    const page = currentPage.value || 1;
    await fetchPage(page);

    // if current page becomes empty, go back one page
    if (page > 1 && (employees.value?.length ?? 0) === 0) {
      await fetchPage(page - 1);
    }
  } finally {
    deleteLoading.value[row.id] = false;
  }
}

const router = useRouter();
</script>

<template>
  <OverviewHeader
    :title="'Employee Profile'"
    :description="'Manage employee profiles'"
    :backPath="'/hr/employees'"

    
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
    Add Employee
  </BaseButton>
</template>
    </OverviewHeader>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="6">
      <el-input
        v-model="q"
        placeholder="Search by name or code..."
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
    :columns="employeeColumns"
    :data="employees"
    :loading="initialLoading || fetching"
    :total="totalRows"
    :page="currentPage"
    :page-size="pageSize"
    @page="goPage"
    @page-size="setPageSize"
    
  >
  

<template #operation="{ row }">
  <el-space>
    <!-- Edit Button -->
    <el-button
      type="primary"
      size="small"
      link
      :loading="detailLoading[row.id]"
      @click="handleOpenUpdateForm(row as HrEmployeeDTO)"
    >
      Edit
    </el-button>

    <!-- Restore Button (only for deleted employees) -->
    <el-button
      v-if="row.lifecycle?.deleted_at"
      type="success"
      size="small"
      link
      :loading="restoreLoading[row.id]"
      @click="handleRestoreEmployee(row as HrEmployeeDTO)"
    >
      Restore
    </el-button>

    <!-- Delete Button (only for non-deleted employees) -->
    <el-button
      v-else
      type="danger"
      size="small"
      link
      :loading="deleteLoading[row.id]"
      @click="handleSoftDeleteEmployee(row as HrEmployeeDTO)"
    >
      Delete
    </el-button>
  </el-space>
</template>
<template #photo="{ row }">
  <el-avatar
    :size="48"
    :src="row.photo_url || undefined"
    class="cursor-pointer"
    @click.stop="router.push(`/hr/employees/${row.id}`)"
  >
    {{ (row.full_name || "?").slice(0, 1).toUpperCase() }}
  </el-avatar>
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
        @size-change="usePreferencesStore"
      />
    </el-row>




    

<SmartFormDialog
  :key="createDialogKey"
  v-model:visible="createFormVisible"
  :model-value="createFormData"
  :fields="baseCreateFormSchema"
  :width="'40%'"
  :loading="createFormLoading"
  :disabled="createFormLoading"
  title="Add Employee"
  useElForm
  @save="handleCreateSave"
  @cancel="cancelCreateForm"
/>

<!-- Update Employee Dialog -->
<SmartFormDialog
  v-model:visible="updateFormVisible"
  :model-value="updateFormData"
  :fields="baseCreateFormSchema"
  :width="'40%'"
  :loading="updateFormLoading"
  :disabled="updateFormLoading"
  title="Update Employee"
  useElForm
  @save="handleUpdateSave"
  @cancel="updateFormVisible = false"
/>
</template>
<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import { useNuxtApp } from "#app";
import { ElMessage, ElMessageBox } from "element-plus";

import type {
  HrCreateEmployeeDTO,
  HrUpdateEmployeeDTO,
  HrEmployeeDTO,
} from "~/api/hr_admin/employees/dto";

import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import ActionButtons from "~/components/buttons/ActionButtons.vue";

import {
  ElCard,
  ElInput,
  ElSelect,
  ElOption,
  ElInputNumber,
  ElButton,
  ElPagination,
} from "element-plus";

import { employeeColumns } from "~/modules/tables/columns/hr_admin/employeeColumns";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import type { Field } from "~/components/types/form";

// --- Nuxt app ---
const { $hrEmployeeService } = useNuxtApp();

// --- Dialog & form state ---
const dialogVisible = ref(false);
const isEdit = ref(false);
const editingEmployeeId = ref<string | null>(null);
const loadingForm = ref(false);
const dialogInitialLoading = ref(false);

const form = reactive<HrCreateEmployeeDTO>({
  employee_code: "",
  full_name: "",
  department: "",
  position: "",
  employment_type: "contract",
  basic_salary: 0,
  status: "active",
});

// --- Select options ---
const employmentTypeOptions = [
  { label: "Contract", value: "contract" },
  { label: "Permanent", value: "permanent" },
  { label: "Probation", value: "probation" },
];

const statusOptions = [
  { label: "Active", value: "active" },
  { label: "Inactive", value: "inactive" },
];

// --- Table paginated fetch ---
const {
  data: employees,
  fetchPage,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
} = usePaginatedFetch<HrEmployeeDTO, {}>(
  async (_, page, size) => {
    const res = await $hrEmployeeService.getEmployees({
      page,
      pageSize: size,
    });
    return {
      items: res.items,
      total: res.total,
    };
  },
  { initialPage: 1, pageSizeRef: 10 },
);

// --- Form fields ---
const employeeFields = computed<Field<HrCreateEmployeeDTO>[]>(() => [
  {
    key: "employee_code",
    label: "Employee Code",
    component: ElInput,
    componentProps: {
      placeholder: "Enter employee code",
      clearable: true,
    },
  },
  {
    key: "full_name",
    label: "Full Name",
    component: ElInput,
    componentProps: {
      placeholder: "Enter full name",
      clearable: true,
    },
  },
  {
    key: "department",
    label: "Department",
    component: ElInput,
    componentProps: {
      placeholder: "Enter department",
      clearable: true,
    },
  },
  {
    key: "position",
    label: "Position",
    component: ElInput,
    componentProps: {
      placeholder: "Enter position",
      clearable: true,
    },
  },
  {
    key: "employment_type",
    label: "Employment Type",
    component: ElSelect,
    componentProps: {
      placeholder: "Select employment type",
      clearable: true,
    },
    childComponent: ElOption,
    childComponentProps: {
      options: employmentTypeOptions,
      valueKey: "value",
      labelKey: "label",
    },
  },
  {
    key: "basic_salary",
    label: "Basic Salary",
    component: ElInputNumber,
    componentProps: {
      min: 0,
      step: 1,
      controlsPosition: "right",
      style: { width: "100%" },
    },
  },
  {
    key: "status",
    label: "Status",
    component: ElSelect,
    componentProps: {
      placeholder: "Select status",
      clearable: true,
    },
    childComponent: ElOption,
    childComponentProps: {
      options: statusOptions,
      valueKey: "value",
      labelKey: "label",
    },
  },
]);

// --- Dialog title ---
const dialogTitle = computed(() =>
  isEdit.value ? "Edit Employee" : "Create Employee",
);

// --- Utility ---
function resetForm() {
  form.employee_code = "";
  form.full_name = "";
  form.department = "";
  form.position = "";
  form.employment_type = "contract";
  form.basic_salary = 0;
  form.status = "active";
}

function fillForm(employee: Partial<HrEmployeeDTO>) {
  form.employee_code = employee.employee_code ?? "";
  form.full_name = employee.full_name ?? "";
  form.department = employee.department ?? "";
  form.position = employee.position ?? "";
  form.employment_type =
    (employee.employment_type as HrCreateEmployeeDTO["employment_type"]) ??
    "contract";
  form.basic_salary = employee.basic_salary ?? 0;
  form.status = (employee.status as HrCreateEmployeeDTO["status"]) ?? "active";
}

// --- Dialog actions ---
function openCreateDialog() {
  isEdit.value = false;
  editingEmployeeId.value = null;
  resetForm();
  dialogVisible.value = true;
}

async function openEditDialog(row: HrEmployeeDTO) {
  isEdit.value = true;
  editingEmployeeId.value = row.id;
  dialogVisible.value = true;
  dialogInitialLoading.value = true;

  try {
    // If you don't have getEmployeeById, replace this with: fillForm(row)
    const employee = await $hrEmployeeService.getEmployeeById(row.id);
    fillForm(employee);
  } catch {
    fillForm(row);
    ElMessage.warning("Could not load full employee detail, using row data.");
  } finally {
    dialogInitialLoading.value = false;
  }
}

function handleCancel() {
  dialogVisible.value = false;
  isEdit.value = false;
  editingEmployeeId.value = null;
  resetForm();
}

async function handleSave(payload: Partial<HrCreateEmployeeDTO>) {
  loadingForm.value = true;

  try {
    if (isEdit.value && editingEmployeeId.value) {
      const updatePayload: HrUpdateEmployeeDTO = {
        employee_code: payload.employee_code ?? form.employee_code,
        full_name: payload.full_name ?? form.full_name,
        department: payload.department ?? form.department,
        position: payload.position ?? form.position,
        employment_type: payload.employment_type ?? form.employment_type,
        basic_salary: payload.basic_salary ?? form.basic_salary,
        status: payload.status ?? form.status,
      };

      await $hrEmployeeService.updateEmployee(
        editingEmployeeId.value,
        updatePayload,
      );

      ElMessage.success("Employee updated successfully");
    } else {
      const createPayload: HrCreateEmployeeDTO = {
        employee_code: payload.employee_code ?? form.employee_code,
        full_name: payload.full_name ?? form.full_name,
        department: payload.department ?? form.department,
        position: payload.position ?? form.position,
        employment_type: payload.employment_type ?? form.employment_type,
        basic_salary: payload.basic_salary ?? form.basic_salary,
        status: payload.status ?? form.status,
      };

      await $hrEmployeeService.createEmployee(createPayload);
      ElMessage.success("Employee created successfully");
    }

    dialogVisible.value = false;
    resetForm();
    await fetchPage(currentPage.value || 1);
  } catch (error) {
    console.error(error);
    ElMessage.error(
      isEdit.value ? "Failed to update employee" : "Failed to create employee",
    );
  } finally {
    loadingForm.value = false;
  }
}

// --- Table actions ---
function onEditRow(row: HrEmployeeDTO) {
  openEditDialog(row);
}

async function onDeleteRow(row: HrEmployeeDTO) {
  try {
    await ElMessageBox.confirm(
      `Delete employee "${row.full_name}"?`,
      "Confirm Delete",
      {
        type: "warning",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      },
    );

    await $hrEmployeeService.deleteEmployee(row.id);
    ElMessage.success("Employee deleted successfully");

    await fetchPage(currentPage.value || 1);
  } catch (error: any) {
    if (error === "cancel" || error === "close") return;
    console.error(error);
    ElMessage.error("Failed to delete employee");
  }
}

// --- Per-row loading states (optional placeholder) ---
const deleteLoading = ref<Record<string, boolean>>({});
const detailLoading = ref<Record<string, boolean>>({});

// --- Load initial table ---
onMounted(async () => {
  await fetchPage(1);
});
</script>

<template>
  <div class="employee-page">
    <OverviewHeader
      title="Employee Management"
      description="Manage employees"
      showSearch
      showReset
      @refresh="fetchPage(1)"
    >
      <template #actions>
        <ElButton type="primary" @click="openCreateDialog">
          Create Employee
        </ElButton>
      </template>
    </OverviewHeader>

    <ElCard>
      <SmartTable
        :columns="employeeColumns"
        :data="employees"
        :loading="initialLoading"
      >
        <template #operation="{ row }">
          <ActionButtons
            :rowId="row.id"
            :detailContent="''"
            deleteContent="Delete this employee?"
            @detail="onEditRow(row)"
            @delete="onDeleteRow(row)"
            :deleteLoading="deleteLoading[row.id] ?? false"
            :detailLoading="detailLoading[row.id] ?? false"
          />
        </template>
      </SmartTable>

      <div class="pagination">
        <ElPagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="totalRows"
          layout="prev, pager, next"
          @current-change="fetchPage"
        />
      </div>
    </ElCard>

    <SmartFormDialog
      v-model:modelValue="form"
      v-model:visible="dialogVisible"
      :title="dialogTitle"
      :fields="employeeFields"
      :loading="loadingForm"
      :initialLoading="dialogInitialLoading"
      width="800px"
      @save="handleSave"
      @cancel="handleCancel"
    />
  </div>
</template>

<style scoped>
.employee-page {
  padding: 20px;
}

.pagination {
  margin-top: 10px;
  text-align: right;
}
</style>

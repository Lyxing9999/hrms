<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  CirclePlus,
  Delete,
  DocumentAdd,
  EditPen,
  Refresh,
  RefreshLeft,
  Search,
  User,
  View,
} from "@element-plus/icons-vue";

import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { ColumnConfig } from "~/components/types/tableEdit";

import { hrmsAdminService } from "~/api/hr_admin";
import type {
  HrCreateEmployeeDTO,
  HrEmployeeAccountDTO,
  HrEmployeeDTO,
  HrEmployeeWithAccountSummaryDTO,
  HrEmploymentType,
} from "~/api/hr_admin/employees/dto";
import { Role } from "~/api/types/enums/role.enum";
import type { SelectOptionDTO } from "~/api/types/common/select-option.type";
import { useHrEmployeeStore } from "~/stores/hrEmployeeStore";

definePageMeta({ layout: "default" });

type LifecycleFilter = "active" | "deleted" | "all";

interface EmployeeFormModel {
  employee_code: string;
  full_name: string;
  department: string;
  position: string;
  employment_type: HrEmploymentType;
  basic_salary: number | null;
  status: "active" | "inactive";
}

interface OnboardFormModel extends EmployeeFormModel {
  email: string;
  username: string;
  password: string;
  role: Role.EMPLOYEE | Role.MANAGER | Role.PAYROLL_MANAGER;
}

interface EmployeeTableRow {
  id: string;
  employee: HrEmployeeDTO;
  employee_code: string;
  full_name: string;
  department: string | null;
  position: string | null;
  employment_type: HrEmploymentType;
  basic_salary: number;
  status: "active" | "inactive";
  deleted_at: string | null;
  account: HrEmployeeAccountDTO | null;
}

const employeeStore = useHrEmployeeStore();
const scheduleService = hrmsAdminService().workingSchedule;
const { $api } = useNuxtApp();
const router = useRouter();

const loading = ref(false);
const tableRows = ref<EmployeeTableRow[]>([]);
const totalRows = ref(0);

const q = ref("");
const lifecycleFilter = ref<LifecycleFilter>("active");
const page = ref(1);
const pageSize = ref(10);

const createDialogVisible = ref(false);
const createSaving = ref(false);
const createForm = reactive<EmployeeFormModel>(getDefaultEmployeeForm());

const onboardDialogVisible = ref(false);
const onboardSaving = ref(false);
const onboardForm = reactive<OnboardFormModel>(getDefaultOnboardForm());

const assignDialogVisible = ref(false);
const assignSaving = ref(false);
const scheduleOptionsLoading = ref(false);
const scheduleOptions = ref<SelectOptionDTO[]>([]);
const assignRow = ref<EmployeeTableRow | null>(null);
const assignForm = reactive({
  schedule_id: "",
});

const rowLoading = ref<Record<string, boolean>>({});

const tableColumns: ColumnConfig<EmployeeTableRow>[] = [
  {
    field: "employee",
    label: "Employee",
    minWidth: "240px",
    useSlot: true,
    slotName: "employee",
  },
  {
    field: "employee_code",
    label: "Code",
    width: "130px",
    useSlot: true,
    slotName: "code",
  },
  {
    field: "department",
    label: "Department / Position",
    minWidth: "200px",
    useSlot: true,
    slotName: "department",
  },
  {
    field: "employment_type",
    label: "Employment",
    width: "140px",
    useSlot: true,
    slotName: "employment",
  },
  {
    field: "basic_salary",
    label: "Basic Salary",
    width: "140px",
    useSlot: true,
    slotName: "salary",
  },
  {
    field: "status",
    label: "Status",
    width: "120px",
    useSlot: true,
    slotName: "status",
  },
  {
    field: "account",
    label: "Account",
    minWidth: "180px",
    useSlot: true,
    slotName: "account",
  },
  {
    field: "id",
    label: "Actions",
    operation: true,
    fixed: "right",
    width: "330px",
    useSlot: true,
    slotName: "operation",
  },
];

const summaryCards = computed(() => {
  const active = tableRows.value.filter((item) => !item.deleted_at).length;
  const deleted = tableRows.value.filter((item) => !!item.deleted_at).length;
  const inactive = tableRows.value.filter(
    (item) => item.status === "inactive",
  ).length;
  const withAccount = tableRows.value.filter((item) => !!item.account).length;

  return [
    { label: "Total", value: totalRows.value },
    { label: "Active", value: active },
    { label: "Inactive", value: inactive },
    { label: "Deleted", value: deleted },
    { label: "With Account", value: withAccount },
  ];
});

function getDefaultEmployeeForm(): EmployeeFormModel {
  return {
    employee_code: "",
    full_name: "",
    department: "",
    position: "",
    employment_type: "permanent",
    basic_salary: null,
    status: "active",
  };
}

function getDefaultOnboardForm(): OnboardFormModel {
  return {
    ...getDefaultEmployeeForm(),
    email: "",
    username: "",
    password: "",
    role: Role.EMPLOYEE,
  };
}

function resetCreateForm() {
  Object.assign(createForm, getDefaultEmployeeForm());
}

function resetOnboardForm() {
  Object.assign(onboardForm, getDefaultOnboardForm());
}

function employeePayloadFromForm(form: EmployeeFormModel): HrCreateEmployeeDTO {
  return {
    employee_code: form.employee_code.trim(),
    full_name: form.full_name.trim(),
    department: form.department.trim() || null,
    position: form.position.trim() || null,
    employment_type: form.employment_type,
    basic_salary: Number(form.basic_salary ?? 0),
    status: form.status,
  };
}

function resolveAccount(
  row: HrEmployeeWithAccountSummaryDTO,
): HrEmployeeAccountDTO | null {
  return row.account ?? row.user ?? null;
}

function toTableRow(item: HrEmployeeWithAccountSummaryDTO): EmployeeTableRow {
  return {
    id: item.employee.id,
    employee: item.employee,
    employee_code: item.employee.employee_code,
    full_name: item.employee.full_name,
    department: item.employee.department ?? null,
    position: item.employee.position ?? null,
    employment_type: item.employee.employment_type,
    basic_salary: item.employee.basic_salary,
    status: item.employee.status,
    deleted_at: item.employee.lifecycle?.deleted_at ?? null,
    account: resolveAccount(item),
  };
}

function formatCurrency(value: number | null | undefined) {
  if (value == null) return "-";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(value);
}

function mapError(error: unknown, fallback: string) {
  const fromStore =
    employeeStore.getError("getEmployeesWithAccounts") ||
    employeeStore.getError("createEmployee") ||
    employeeStore.getError("onboardEmployee") ||
    employeeStore.getError("softDeleteEmployee") ||
    employeeStore.getError("restoreEmployee") ||
    employeeStore.getError("getEmployee");

  if (fromStore) return fromStore;

  if (error && typeof error === "object" && "response" in error) {
    const maybeResponse = error as {
      response?: { data?: { user_message?: string; message?: string } };
    };
    return (
      maybeResponse.response?.data?.user_message ||
      maybeResponse.response?.data?.message ||
      fallback
    );
  }

  if (error instanceof Error && error.message) return error.message;
  return fallback;
}

async function loadEmployees() {
  loading.value = true;
  try {
    const response = await employeeStore.getEmployeesWithAccounts({
      page: page.value,
      limit: pageSize.value,
      q: q.value.trim() || undefined,
      include_deleted: lifecycleFilter.value === "all" ? true : undefined,
      deleted_only: lifecycleFilter.value === "deleted" ? true : undefined,
      with_accounts: true,
    });

    tableRows.value = (response.items ?? []).map(toTableRow);
    totalRows.value = Number(response.total ?? 0);
  } catch (error) {
    ElMessage.error(mapError(error, "Failed to load employees"));
  } finally {
    loading.value = false;
  }
}

function applyFilterAndReload() {
  page.value = 1;
  loadEmployees();
}

function openCreateDialog() {
  resetCreateForm();
  createDialogVisible.value = true;
}

function openOnboardDialog() {
  resetOnboardForm();
  onboardDialogVisible.value = true;
}

async function submitCreate() {
  if (!createForm.employee_code.trim()) {
    ElMessage.warning("Employee code is required");
    return;
  }
  if (!createForm.full_name.trim()) {
    ElMessage.warning("Full name is required");
    return;
  }
  if (createForm.basic_salary == null || Number(createForm.basic_salary) < 0) {
    ElMessage.warning("Basic salary must be 0 or greater");
    return;
  }

  createSaving.value = true;
  try {
    await employeeStore.createEmployee(employeePayloadFromForm(createForm));
    ElMessage.success("Employee created successfully");
    createDialogVisible.value = false;
    await loadEmployees();
  } catch (error) {
    ElMessage.error(mapError(error, "Failed to create employee"));
  } finally {
    createSaving.value = false;
  }
}

async function submitOnboard() {
  if (!onboardForm.employee_code.trim()) {
    ElMessage.warning("Employee code is required");
    return;
  }
  if (!onboardForm.full_name.trim()) {
    ElMessage.warning("Full name is required");
    return;
  }
  if (!onboardForm.email.trim()) {
    ElMessage.warning("Email is required");
    return;
  }
  if (!onboardForm.password || onboardForm.password.length < 6) {
    ElMessage.warning("Password must be at least 6 characters");
    return;
  }
  if (
    onboardForm.basic_salary == null ||
    Number(onboardForm.basic_salary) < 0
  ) {
    ElMessage.warning("Basic salary must be 0 or greater");
    return;
  }

  onboardSaving.value = true;
  try {
    await employeeStore.onboardEmployee({
      employee: employeePayloadFromForm(onboardForm),
      email: onboardForm.email.trim(),
      password: onboardForm.password,
      username: onboardForm.username.trim() || undefined,
      role: onboardForm.role,
    });

    ElMessage.success("Employee onboarded successfully");
    onboardDialogVisible.value = false;
    await loadEmployees();
  } catch (error) {
    ElMessage.error(mapError(error, "Failed to onboard employee"));
  } finally {
    onboardSaving.value = false;
  }
}

async function openDetail(row: EmployeeTableRow) {
  await router.push(`/hr/employees/${row.id}`);
}

async function confirmDelete(row: EmployeeTableRow) {
  try {
    await ElMessageBox.confirm(
      `Soft delete ${row.full_name}?`,
      "Delete Employee",
      {
        type: "warning",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      },
    );

    rowLoading.value[row.id] = true;
    await employeeStore.softDeleteEmployee(row.id);
    ElMessage.success("Employee deleted successfully");
    await loadEmployees();
  } catch (error: unknown) {
    if (error === "cancel" || error === "close") return;
    ElMessage.error(mapError(error, "Failed to delete employee"));
  } finally {
    rowLoading.value[row.id] = false;
  }
}

async function confirmRestore(row: EmployeeTableRow) {
  try {
    await ElMessageBox.confirm(
      `Restore ${row.full_name}?`,
      "Restore Employee",
      {
        type: "info",
        confirmButtonText: "Restore",
        cancelButtonText: "Cancel",
      },
    );

    rowLoading.value[row.id] = true;
    await employeeStore.restoreEmployee(row.id);
    ElMessage.success("Employee restored successfully");
    await loadEmployees();
  } catch (error: unknown) {
    if (error === "cancel" || error === "close") return;
    ElMessage.error(mapError(error, "Failed to restore employee"));
  } finally {
    rowLoading.value[row.id] = false;
  }
}

async function loadScheduleOptions() {
  if (scheduleOptions.value.length) return;

  scheduleOptionsLoading.value = true;
  try {
    scheduleOptions.value = await scheduleService.getScheduleSelectOptions();
  } catch (error) {
    ElMessage.error(mapError(error, "Failed to load schedules"));
  } finally {
    scheduleOptionsLoading.value = false;
  }
}

async function openAssignScheduleDialog(row: EmployeeTableRow) {
  assignRow.value = row;
  assignForm.schedule_id = "";
  assignDialogVisible.value = true;
  await loadScheduleOptions();
}

async function submitAssignSchedule() {
  if (!assignRow.value) return;
  if (!assignForm.schedule_id) {
    ElMessage.warning("Please select a schedule");
    return;
  }

  assignSaving.value = true;
  try {
    if (!$api) {
      throw new Error("API client is unavailable");
    }

    await ($api as any).post(
      `/api/hrms/employees/${assignRow.value.id}/assign-schedule`,
      {
        schedule_id: assignForm.schedule_id,
      },
    );

    ElMessage.success("Schedule assigned successfully");
    assignDialogVisible.value = false;
  } catch (error) {
    ElMessage.error(mapError(error, "Failed to assign schedule"));
  } finally {
    assignSaving.value = false;
  }
}

function handlePageChange(value: number) {
  page.value = value;
  loadEmployees();
}

function handlePageSizeChange(value: number) {
  pageSize.value = value;
  page.value = 1;
  loadEmployees();
}

onMounted(() => {
  loadEmployees();
});
</script>

<template>
  <div class="employees-page">
    <OverviewHeader
      title="Employee Directory"
      description="Manage employee records, onboarding, and schedule assignment"
      @refresh="loadEmployees"
    >
      <template #actions>
        <div class="header-actions">
          <BaseButton type="primary" @click="openCreateDialog">
            <template #iconPre>
              <el-icon><CirclePlus /></el-icon>
            </template>
            Create Employee
          </BaseButton>

          <BaseButton type="success" plain @click="openOnboardDialog">
            <template #iconPre>
              <el-icon><DocumentAdd /></el-icon>
            </template>
            Onboard Employee
          </BaseButton>

          <BaseButton
            type="info"
            plain
            @click="router.push('/hr/employees/accounts')"
          >
            <template #iconPre>
              <el-icon><User /></el-icon>
            </template>
            Accounts
          </BaseButton>

          <BaseButton
            type="warning"
            plain
            @click="router.push('/hr/employees/archived')"
          >
            <template #iconPre>
              <el-icon><RefreshLeft /></el-icon>
            </template>
            Archived
          </BaseButton>

          <el-input
            v-model="q"
            clearable
            placeholder="Search by name, code, department"
            class="search-input"
            @keyup.enter="applyFilterAndReload"
            @clear="applyFilterAndReload"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>

          <el-radio-group
            v-model="lifecycleFilter"
            size="default"
            class="lifecycle-group"
            @change="applyFilterAndReload"
          >
            <el-radio-button label="active">Active</el-radio-button>
            <el-radio-button label="deleted">Deleted</el-radio-button>
            <el-radio-button label="all">All</el-radio-button>
          </el-radio-group>
        </div>
      </template>
    </OverviewHeader>

    <div class="summary-grid">
      <el-card v-for="card in summaryCards" :key="card.label" shadow="never">
        <div class="summary-label">{{ card.label }}</div>
        <div class="summary-value">{{ card.value }}</div>
      </el-card>
    </div>

    <el-card shadow="never" class="table-card">
      <SmartTable
        :columns="tableColumns"
        :data="tableRows"
        :loading="loading"
        :total="totalRows"
        :page="page"
        :page-size="pageSize"
        @page="handlePageChange"
        @page-size="handlePageSizeChange"
      >
        <template #employee="{ row }">
          <div
            class="employee-cell employee-cell--clickable"
            @click="openDetail(row as EmployeeTableRow)"
          >
            <el-avatar class="employee-avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div>
              <div class="employee-name">
                {{ (row as EmployeeTableRow).full_name }}
              </div>
              <div class="employee-meta">
                ID: {{ (row as EmployeeTableRow).id }}
              </div>
            </div>
          </div>
        </template>

        <template #code="{ row }">
          {{ (row as EmployeeTableRow).employee_code }}
        </template>

        <template #department="{ row }">
          <div class="department-cell">
            <div>{{ (row as EmployeeTableRow).department || "-" }}</div>
            <div class="employee-meta">
              {{ (row as EmployeeTableRow).position || "-" }}
            </div>
          </div>
        </template>

        <template #employment="{ row }">
          <el-tag effect="light" type="info">
            {{ (row as EmployeeTableRow).employment_type }}
          </el-tag>
        </template>

        <template #salary="{ row }">
          {{ formatCurrency((row as EmployeeTableRow).basic_salary) }}
        </template>

        <template #status="{ row }">
          <el-tag
            :type="(row as EmployeeTableRow).status === 'active' ? 'success' : 'warning'"
            effect="light"
          >
            {{ (row as EmployeeTableRow).status }}
          </el-tag>
        </template>

        <template #account="{ row }">
          <div class="account-cell">
            <template v-if="(row as EmployeeTableRow).account">
              <div>{{ (row as EmployeeTableRow).account?.email || "-" }}</div>
              <div class="employee-meta">
                {{ (row as EmployeeTableRow).account?.role || "-" }}
              </div>
            </template>
            <el-tag v-else type="info" effect="plain">No account</el-tag>
          </div>
        </template>

        <template #operation="{ row }">
          <div class="row-actions">
            <BaseButton
              type="primary"
              link
              size="small"
              @click="openDetail(row as EmployeeTableRow)"
            >
              <template #iconPre>
                <el-icon><View /></el-icon>
              </template>
              Detail
            </BaseButton>

            <BaseButton
              type="warning"
              link
              size="small"
              @click="openAssignScheduleDialog(row as EmployeeTableRow)"
            >
              <template #iconPre>
                <el-icon><EditPen /></el-icon>
              </template>
              Assign Schedule
            </BaseButton>

            <BaseButton
              v-if="!(row as EmployeeTableRow).deleted_at"
              type="danger"
              link
              size="small"
              :loading="rowLoading[(row as EmployeeTableRow).id]"
              @click="confirmDelete(row as EmployeeTableRow)"
            >
              <template #iconPre>
                <el-icon><Delete /></el-icon>
              </template>
              Delete
            </BaseButton>

            <BaseButton
              v-else
              type="success"
              link
              size="small"
              :loading="rowLoading[(row as EmployeeTableRow).id]"
              @click="confirmRestore(row as EmployeeTableRow)"
            >
              <template #iconPre>
                <el-icon><RefreshLeft /></el-icon>
              </template>
              Restore
            </BaseButton>
          </div>
        </template>
      </SmartTable>
    </el-card>

    <el-dialog
      v-model="createDialogVisible"
      title="Create Employee"
      width="720px"
    >
      <el-form label-position="top" class="dialog-form">
        <div class="form-grid">
          <el-form-item label="Employee Code" required>
            <el-input
              v-model="createForm.employee_code"
              placeholder="EMP-001"
            />
          </el-form-item>
          <el-form-item label="Full Name" required>
            <el-input
              v-model="createForm.full_name"
              placeholder="Employee full name"
            />
          </el-form-item>
          <el-form-item label="Department">
            <el-input
              v-model="createForm.department"
              placeholder="Department"
            />
          </el-form-item>
          <el-form-item label="Position">
            <el-input v-model="createForm.position" placeholder="Position" />
          </el-form-item>
          <el-form-item label="Employment Type">
            <el-select v-model="createForm.employment_type">
              <el-option label="Permanent" value="permanent" />
              <el-option label="Contract" value="contract" />
            </el-select>
          </el-form-item>
          <el-form-item label="Status">
            <el-select v-model="createForm.status">
              <el-option label="Active" value="active" />
              <el-option label="Inactive" value="inactive" />
            </el-select>
          </el-form-item>
          <el-form-item label="Basic Salary" required>
            <el-input-number
              v-model="createForm.basic_salary"
              :min="0"
              :step="10"
              :precision="2"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-actions">
          <BaseButton @click="createDialogVisible = false">Cancel</BaseButton>
          <BaseButton
            type="primary"
            :loading="createSaving"
            @click="submitCreate"
          >
            Create
          </BaseButton>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="onboardDialogVisible"
      title="Onboard Employee"
      width="760px"
    >
      <el-form label-position="top" class="dialog-form">
        <div class="form-grid">
          <el-form-item label="Employee Code" required>
            <el-input
              v-model="onboardForm.employee_code"
              placeholder="EMP-001"
            />
          </el-form-item>
          <el-form-item label="Full Name" required>
            <el-input
              v-model="onboardForm.full_name"
              placeholder="Employee full name"
            />
          </el-form-item>
          <el-form-item label="Department">
            <el-input
              v-model="onboardForm.department"
              placeholder="Department"
            />
          </el-form-item>
          <el-form-item label="Position">
            <el-input v-model="onboardForm.position" placeholder="Position" />
          </el-form-item>
          <el-form-item label="Employment Type">
            <el-select v-model="onboardForm.employment_type">
              <el-option label="Permanent" value="permanent" />
              <el-option label="Contract" value="contract" />
            </el-select>
          </el-form-item>
          <el-form-item label="Status">
            <el-select v-model="onboardForm.status">
              <el-option label="Active" value="active" />
              <el-option label="Inactive" value="inactive" />
            </el-select>
          </el-form-item>
          <el-form-item label="Basic Salary" required>
            <el-input-number
              v-model="onboardForm.basic_salary"
              :min="0"
              :step="10"
              :precision="2"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="Email" required>
            <el-input
              v-model="onboardForm.email"
              placeholder="employee@company.com"
            />
          </el-form-item>
          <el-form-item label="Username">
            <el-input
              v-model="onboardForm.username"
              placeholder="username (optional)"
            />
          </el-form-item>
          <el-form-item label="Password" required>
            <el-input
              v-model="onboardForm.password"
              type="password"
              show-password
            />
          </el-form-item>
          <el-form-item label="Role">
            <el-select v-model="onboardForm.role">
              <el-option label="Employee" :value="Role.EMPLOYEE" />
              <el-option label="Manager" :value="Role.MANAGER" />
              <el-option
                label="Payroll Manager"
                :value="Role.PAYROLL_MANAGER"
              />
            </el-select>
          </el-form-item>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-actions">
          <BaseButton @click="onboardDialogVisible = false">Cancel</BaseButton>
          <BaseButton
            type="success"
            :loading="onboardSaving"
            @click="submitOnboard"
          >
            Onboard
          </BaseButton>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="assignDialogVisible"
      title="Assign Working Schedule"
      width="520px"
    >
      <el-form label-position="top">
        <el-form-item label="Employee">
          <el-input :model-value="assignRow?.full_name || '-'" disabled />
        </el-form-item>

        <el-form-item label="Working Schedule" required>
          <el-select
            v-model="assignForm.schedule_id"
            placeholder="Select a schedule"
            :loading="scheduleOptionsLoading"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="option in scheduleOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-actions">
          <BaseButton @click="assignDialogVisible = false">Cancel</BaseButton>
          <BaseButton
            type="warning"
            :loading="assignSaving"
            @click="submitAssignSchedule"
          >
            <template #iconPre>
              <el-icon><Refresh /></el-icon>
            </template>
            Assign
          </BaseButton>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.employees-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.header-actions {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, auto));
  align-items: center;
  gap: 10px;
}

.search-input {
  min-width: 280px;
}

.lifecycle-group {
  width: fit-content;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
}

.summary-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.summary-value {
  margin-top: 6px;
  font-size: 24px;
  font-weight: 700;
  color: var(--el-text-color-primary);
}

.table-card {
  border: 1px solid color-mix(in srgb, var(--el-border-color) 75%, #ffffff 25%);
}

.employee-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.employee-cell--clickable {
  cursor: pointer;
}

.employee-avatar {
  background: color-mix(in srgb, var(--el-color-primary) 25%, #ffffff 75%);
  color: var(--el-color-primary);
}

.employee-name {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.employee-meta {
  margin-top: 2px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.department-cell,
.account-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.row-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.dialog-form {
  margin-top: 6px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 14px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.detail-item {
  padding: 12px;
  border-radius: 10px;
  border: 1px solid var(--el-border-color-lighter);
  background: color-mix(in srgb, var(--el-fill-color-light) 90%, #ffffff 10%);
}

.detail-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.detail-value {
  margin-top: 4px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

@media (max-width: 1200px) {
  .header-actions {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .summary-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .header-actions {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .search-input {
    grid-column: span 3;
    width: 100%;
  }

  .lifecycle-group {
    width: 100%;
  }

  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .form-grid,
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>

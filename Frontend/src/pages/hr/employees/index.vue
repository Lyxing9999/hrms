<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useNuxtApp } from "#app";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";

import type { ColumnConfig } from "~/components/table-edit/core/types";
import type { Field } from "~/components/types/form";
import { Role } from "~/api/types/enums/role.enum";

import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import ActionButtons from "~/components/buttons/ActionButtons.vue";
import ManageEmployeeAccountDialog from "~/components/hrms/employees/ManageEmployeeAccountDialog.vue";

import {
  ElCard,
  ElInput,
  ElSelect,
  ElOption,
  ElInputNumber,
  ElButton,
  ElPagination,
  ElDatePicker,
} from "element-plus";

/* ------------------------------------------------------------------
 * Frontend types aligned to backend Pydantic schemas
 * ------------------------------------------------------------------ */

type EmploymentType = "permanent" | "contract";
type SalaryType = "monthly" | "daily" | "hourly";
type EmployeeStatus = "active" | "inactive";

interface ContractSchema {
  start_date: string; // YYYY-MM-DD
  end_date: string;   // YYYY-MM-DD
  salary_type: SalaryType;
  rate: number;
  leave_policy_id?: string | null;
  pay_on_holiday?: boolean;
  pay_on_weekend?: boolean;
}

interface HrCreateEmployeeDTO {
  employee_code: string;
  full_name: string;
  department?: string | null;
  position?: string | null;
  employment_type: EmploymentType;
  basic_salary: number;
  contract?: ContractSchema | null;
  manager_user_id?: string | null;
  schedule_id?: string | null;
  status?: string;
  photo_url?: string | null;
}

interface HrUpdateEmployeeDTO {
  full_name?: string;
  department?: string | null;
  position?: string | null;
  employment_type?: EmploymentType;
  basic_salary?: number;
  contract?: ContractSchema | null;
  manager_user_id?: string | null;
  schedule_id?: string | null;
  status?: string;
  photo_url?: string | null;
}

interface HrEmployeeDTO {
  id: string;
  employee_code: string;
  full_name: string;
  department?: string | null;
  position?: string | null;
  employment_type: EmploymentType;
  basic_salary: number;
  contract?: ContractSchema | null;
  manager_user_id?: string | null;
  schedule_id?: string | null;
  status?: string;
  photo_url?: string | null;
}

interface HrEmployeeAccountDTO {
  id: string;
  email?: string | null;
  username?: string | null;
  role?: string;
  status?: string;
}

interface HrCreateEmployeeAccountDTO {
  email: string;
  password: string;
  username?: string | null;
  role: string;
}

type EmployeeTableRow = {
  id: string;
  employee: HrEmployeeDTO;
  account: HrEmployeeAccountDTO | null;
};

type EmployeeFormModel = {
  employee_code: string;
  full_name: string;
  department: string | null;
  position: string | null;
  employment_type: EmploymentType;
  basic_salary: number;
  status: string;
  start_date: string | null;
  end_date: string | null;
};

const employeeColumns: ColumnConfig<EmployeeTableRow>[] = [
  {
    field: "employee_code",
    label: "Employee Code",
    useSlot: true,
    slotName: "employee_code",
    minWidth: "140px",
  },
  {
    field: "full_name",
    label: "Full Name",
    useSlot: true,
    slotName: "full_name",
    minWidth: "180px",
  },
  {
    field: "department",
    label: "Department",
    useSlot: true,
    slotName: "department",
    minWidth: "160px",
  },
  {
    field: "position",
    label: "Position",
    useSlot: true,
    slotName: "position",
    minWidth: "160px",
  },
  {
    field: "employment_type",
    label: "Employment Type",
    useSlot: true,
    slotName: "employment_type",
    minWidth: "140px",
  },
  {
    field: "basic_salary",
    label: "Basic Salary",
    useSlot: true,
    slotName: "basic_salary",
    minWidth: "120px",
  },
  {
    field: "employee_status",
    label: "Employee Status",
    useSlot: true,
    slotName: "employee_status",
    minWidth: "140px",
  },
  {
    field: "account_status",
    label: "Account Status",
    useSlot: true,
    slotName: "account_status",
    minWidth: "220px",
  },
  {
    field: "id",
    operation: true,
    label: "Operation",
    inlineEditActive: false,
    align: "center",
    minWidth: "300px",
    smartProps: {},
  },
];

const { $hrEmployeeService } = useNuxtApp();

/* -----------------------------
 * Table data
 * ----------------------------- */
const rows = ref<EmployeeTableRow[]>([]);
const loadingTable = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const totalRows = ref(0);
const search = ref("");

/* -----------------------------
 * Employee dialog state
 * ----------------------------- */
const employeeDialogVisible = ref(false);
const isEdit = ref(false);
const editingEmployeeId = ref<string | null>(null);
const loadingEmployeeForm = ref(false);
const employeeDialogInitialLoading = ref(false);

const employeeForm = reactive<EmployeeFormModel>({
  employee_code: "",
  full_name: "",
  department: "",
  position: "",
  employment_type: "contract",
  basic_salary: 0,
  status: "active",
  start_date: "",
  end_date: "",
});

watch(
  () => employeeForm.employment_type,
  (newType) => {
    if (newType !== "contract") {
      employeeForm.start_date = "";
      employeeForm.end_date = "";
    }
  },
);

/* -----------------------------
 * Account state
 * ----------------------------- */
const manageAccountDialogVisible = ref(false);
const manageAccountDialogLoading = ref(false);
const accountActionLoading = ref(false);

const createAccountDialogVisible = ref(false);
const loadingCreateAccountForm = ref(false);

const selectedEmployee = ref<HrEmployeeDTO | null>(null);
const selectedAccount = ref<HrEmployeeAccountDTO | null>(null);

const createAccountForm = ref<HrCreateEmployeeAccountDTO>({
  username: "",
  email: "",
  password: "",
  role: Role.EMPLOYEE,
});

/* -----------------------------
 * Options
 * ----------------------------- */
const employmentTypeOptions = [
  { label: "Contract", value: "contract" },
  { label: "Permanent", value: "permanent" },
];

const statusOptions = [
  { label: "Active", value: "active" },
  { label: "Inactive", value: "inactive" },
];

const roleOptions = [
  { label: "Employee", value: Role.EMPLOYEE },
  { label: "Manager", value: Role.MANAGER },
  { label: "Payroll Manager", value: Role.PAYROLL_MANAGER },
  { label: "HR Admin", value: Role.HR_ADMIN },
];

/* -----------------------------
 * Helpers
 * ----------------------------- */
function normalizeNullableText(value?: string | null) {
  const trimmed = (value ?? "").trim();
  return trimmed.length ? trimmed : null;
}

function buildContractPayload(
  model: Pick<EmployeeFormModel, "start_date" | "end_date" | "basic_salary">,
): ContractSchema {
  return {
    start_date: model.start_date || "",
    end_date: model.end_date || "",
    salary_type: "monthly",
    rate: Number(model.basic_salary),
    pay_on_holiday: true,
    pay_on_weekend: false,
    leave_policy_id: null,
  };
}

function validateEmployeeFormBeforeSubmit(
  payload: Partial<EmployeeFormModel>,
): string | null {
  const employmentType =
    payload.employment_type ?? employeeForm.employment_type;
  const basicSalary = Number(payload.basic_salary ?? employeeForm.basic_salary);
  const startDate = payload.start_date ?? employeeForm.start_date;
  const endDate = payload.end_date ?? employeeForm.end_date;

  if (!String(payload.full_name ?? employeeForm.full_name).trim()) {
    return "Full name is required";
  }

  if (!isEdit.value && !String(payload.employee_code ?? employeeForm.employee_code).trim()) {
    return "Employee code is required";
  }

  if (basicSalary < 0) {
    return "Basic salary cannot be negative";
  }

  if (employmentType === "contract") {
    if (!startDate) return "Contract start date is required";
    if (!endDate) return "Contract end date is required";
    if (new Date(endDate) < new Date(startDate)) {
      return "Contract end date cannot be before start date";
    }
    if (basicSalary <= 0) {
      return "Contract salary/rate must be greater than 0";
    }
  }

  return null;
}

/* -----------------------------
 * Employee form fields
 * ----------------------------- */
const employeeFields = computed<Field<EmployeeFormModel>[]>(() => {
  const baseFields: Field<EmployeeFormModel>[] = [
    {
      key: "employee_code",
      label: "Employee Code",
      component: ElInput,
      componentProps: {
        placeholder: "Enter employee code",
        clearable: true,
        disabled: isEdit.value, // backend update schema does not support employee_code
      },
      formItemProps: {
        rules: [
          {
            required: !isEdit.value,
            message: "Employee code is required",
            trigger: "blur",
          },
        ],
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
      formItemProps: {
        rules: [
          {
            required: true,
            message: "Full name is required",
            trigger: "blur",
          },
        ],
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
        clearable: false,
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
        clearable: false,
      },
      childComponent: ElOption,
      childComponentProps: {
        options: statusOptions,
        valueKey: "value",
        labelKey: "label",
      },
    },
  ];

  if (employeeForm.employment_type === "contract") {
    baseFields.push(
      {
        key: "start_date",
        label: "Contract Start Date",
        component: ElDatePicker,
        componentProps: {
          type: "date",
          placeholder: "Select start date",
          style: { width: "100%" },
          clearable: true,
          valueFormat: "YYYY-MM-DD",
        },
        formItemProps: {
          rules: [
            {
              required: true,
              message: "Start date is required",
              trigger: "change",
            },
          ],
        },
      },
      {
        key: "end_date",
        label: "Contract End Date",
        component: ElDatePicker,
        componentProps: {
          type: "date",
          placeholder: "Select end date",
          style: { width: "100%" },
          clearable: true,
          valueFormat: "YYYY-MM-DD",
        },
        formItemProps: {
          rules: [
            {
              required: true,
              message: "End date is required",
              trigger: "change",
            },
            {
              validator: (_rule: unknown, value: string, callback: (err?: Error) => void) => {
                const start = employeeForm.start_date
                  ? new Date(employeeForm.start_date)
                  : null;
                const end = value ? new Date(value) : null;

                if (start && end && end < start) {
                  callback(new Error("End date cannot be before start date"));
                } else {
                  callback();
                }
              },
              trigger: "change",
            },
          ],
        },
      },
    );
  }

  return baseFields;
});

/* -----------------------------
 * Create account form fields
 * ----------------------------- */
const createAccountFields = computed<Field<HrCreateEmployeeAccountDTO>[]>(() => [
  {
    key: "email",
    label: "Email",
    component: ElInput,
    componentProps: {
      placeholder: "Enter email",
      clearable: true,
    },
    formItemProps: {
      rules: [
        { required: true, message: "Email is required", trigger: "blur" },
      ],
    },
  },
  {
    key: "username",
    label: "Username",
    component: ElInput,
    componentProps: {
      placeholder: "Enter username",
      clearable: true,
    },
  },
  {
    key: "password",
    label: "Password",
    component: ElInput,
    componentProps: {
      type: "password",
      showPassword: true,
      placeholder: "Enter password",
    },
    formItemProps: {
      rules: [
        { required: true, message: "Password is required", trigger: "blur" },
      ],
    },
  },
  {
    key: "role",
    label: "Role",
    component: ElSelect,
    componentProps: {
      placeholder: "Select role",
      clearable: false,
    },
    childComponent: ElOption,
    childComponentProps: {
      options: roleOptions,
      valueKey: "value",
      labelKey: "label",
    },
  },
]);

const employeeDialogTitle = computed(() =>
  isEdit.value ? "Edit Employee" : "Create Employee",
);

const createAccountDialogTitle = computed(() => {
  return selectedEmployee.value
    ? `Create Account - ${selectedEmployee.value.full_name}`
    : "Create Account";
});

function resetEmployeeForm() {
  employeeForm.employee_code = "";
  employeeForm.full_name = "";
  employeeForm.department = "";
  employeeForm.position = "";
  employeeForm.employment_type = "contract";
  employeeForm.basic_salary = 0;
  employeeForm.status = "active";
  employeeForm.start_date = "";
  employeeForm.end_date = "";
}

function fillEmployeeForm(employee: Partial<HrEmployeeDTO>) {
  employeeForm.employee_code = employee.employee_code ?? "";
  employeeForm.full_name = employee.full_name ?? "";
  employeeForm.department = employee.department ?? "";
  employeeForm.position = employee.position ?? "";
  employeeForm.employment_type = employee.employment_type ?? "contract";
  employeeForm.basic_salary = employee.basic_salary ?? 0;
  employeeForm.status = employee.status ?? "active";
  employeeForm.start_date = employee.contract?.start_date ?? "";
  employeeForm.end_date = employee.contract?.end_date ?? "";
}

function resetCreateAccountForm(employee?: HrEmployeeDTO | null) {
  createAccountForm.value = {
    username: employee?.full_name
      ? employee.full_name.toLowerCase().trim().replace(/\s+/g, ".")
      : "",
    email: "",
    password: "",
    role: Role.EMPLOYEE,
  };
}

function getAccountTagType(account: HrEmployeeAccountDTO | null) {
  if (!account) return "info";
  if (account.status === "active") return "success";
  if (account.status === "inactive") return "warning";
  return "danger";
}

function getEmployeeStatusTagType(status?: string | null) {
  return status === "active" ? "success" : "warning";
}

function mapRows(
  items: Array<{
    employee: HrEmployeeDTO;
    account?: HrEmployeeAccountDTO | null;
  }>,
): EmployeeTableRow[] {
  return items.map((item) => ({
    id: item.employee.id,
    employee: item.employee,
    account: item.account ?? null,
  }));
}

/* -----------------------------
 * Fetch
 * ----------------------------- */
async function fetchEmployees(page = currentPage.value) {
  loadingTable.value = true;

  try {
    const res = await $hrEmployeeService.getEmployeesWithAccounts({
      page,
      limit: pageSize.value,
      q: search.value.trim() || undefined,
    });

    rows.value = mapRows(res.items);
    totalRows.value = res.total;
    currentPage.value = page;
  } catch (error) {
    console.error(error);
    ElMessage.error("Failed to load employees");
  } finally {
    loadingTable.value = false;
  }
}

/* -----------------------------
 * Employee actions
 * ----------------------------- */
function openCreateEmployeeDialog() {
  isEdit.value = false;
  editingEmployeeId.value = null;
  resetEmployeeForm();
  employeeDialogVisible.value = true;
}

async function openEditEmployeeDialog(row: EmployeeTableRow) {
  isEdit.value = true;
  editingEmployeeId.value = row.employee.id;
  employeeDialogVisible.value = true;
  employeeDialogInitialLoading.value = true;

  try {
    const employee = await $hrEmployeeService.getEmployee(row.employee.id);
    fillEmployeeForm(employee);
  } catch {
    fillEmployeeForm(row.employee);
    ElMessage.warning("Could not load full employee detail, using row data.");
  } finally {
    employeeDialogInitialLoading.value = false;
  }
}

function handleCancelEmployeeForm() {
  employeeDialogVisible.value = false;
  isEdit.value = false;
  editingEmployeeId.value = null;
  resetEmployeeForm();
}

async function handleSaveEmployeeForm(payload: Partial<EmployeeFormModel>) {
  const validationError = validateEmployeeFormBeforeSubmit(payload);
  if (validationError) {
    ElMessage.error(validationError);
    return;
  }

  loadingEmployeeForm.value = true;

  try {
    const employmentType =
      payload.employment_type ?? employeeForm.employment_type;
    const basicSalary = Number(payload.basic_salary ?? employeeForm.basic_salary);

    if (isEdit.value && editingEmployeeId.value) {
      const updatePayload: HrUpdateEmployeeDTO = {
        full_name: (payload.full_name ?? employeeForm.full_name).trim(),
        department: normalizeNullableText(payload.department ?? employeeForm.department),
        position: normalizeNullableText(payload.position ?? employeeForm.position),
        employment_type: employmentType,
        basic_salary: basicSalary,
        status: payload.status ?? employeeForm.status,
        contract:
          employmentType === "contract"
            ? buildContractPayload({
                start_date: payload.start_date ?? employeeForm.start_date,
                end_date: payload.end_date ?? employeeForm.end_date,
                basic_salary: basicSalary,
              })
            : null,
      };

      await $hrEmployeeService.updateEmployee(
        editingEmployeeId.value,
        updatePayload,
      );

      ElMessage.success("Employee updated successfully");
    } else {
      const createPayload: HrCreateEmployeeDTO = {
        employee_code: (payload.employee_code ?? employeeForm.employee_code).trim(),
        full_name: (payload.full_name ?? employeeForm.full_name).trim(),
        department: normalizeNullableText(payload.department ?? employeeForm.department),
        position: normalizeNullableText(payload.position ?? employeeForm.position),
        employment_type: employmentType,
        basic_salary: basicSalary,
        status: payload.status ?? employeeForm.status,
        contract:
          employmentType === "contract"
            ? buildContractPayload({
                start_date: payload.start_date ?? employeeForm.start_date,
                end_date: payload.end_date ?? employeeForm.end_date,
                basic_salary: basicSalary,
              })
            : null,
      };

      await $hrEmployeeService.createEmployee(createPayload);
      ElMessage.success("Employee created successfully");
    }

    employeeDialogVisible.value = false;
    resetEmployeeForm();
    await fetchEmployees(currentPage.value);
  } catch (error) {
    console.error(error);
    ElMessage.error(
      isEdit.value ? "Failed to update employee" : "Failed to create employee",
    );
  } finally {
    loadingEmployeeForm.value = false;
  }
}

async function onDeleteRow(row: EmployeeTableRow) {
  try {
    await ElMessageBox.confirm(
      `Delete employee "${row.employee.full_name}"?`,
      "Confirm Delete",
      {
        type: "warning",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      },
    );

    await $hrEmployeeService.softDeleteEmployee(row.employee.id);
    ElMessage.success("Employee deleted successfully");
    await fetchEmployees(currentPage.value);
  } catch (error: unknown) {
    if (error === "cancel" || error === "close") return;
    console.error(error);
    ElMessage.error("Failed to delete employee");
  }
}

/* -----------------------------
 * Account actions
 * ----------------------------- */
async function openManageAccountDialog(row: EmployeeTableRow) {
  selectedEmployee.value = row.employee;
  selectedAccount.value = null;
  resetCreateAccountForm(row.employee);
  manageAccountDialogVisible.value = true;
  manageAccountDialogLoading.value = true;

  try {
    const account = await $hrEmployeeService.getEmployeeAccount(
      row.employee.id,
    );
    selectedAccount.value = account ?? null;
  } catch (error) {
    console.error(error);
    manageAccountDialogVisible.value = false;
    ElMessage.error("Failed to load linked account");
  } finally {
    manageAccountDialogLoading.value = false;
  }
}

function closeManageAccountDialog() {
  manageAccountDialogVisible.value = false;
  manageAccountDialogLoading.value = false;
  accountActionLoading.value = false;
  selectedAccount.value = null;
}

function openCreateAccountDialog() {
  manageAccountDialogVisible.value = false;
  createAccountDialogVisible.value = true;
}

function closeCreateAccountDialog() {
  createAccountDialogVisible.value = false;
  loadingCreateAccountForm.value = false;
  resetCreateAccountForm(selectedEmployee.value);
}

async function handleSaveCreateAccount(
  payload: Partial<HrCreateEmployeeAccountDTO>,
) {
  if (!selectedEmployee.value) return;

  const email = (payload.email ?? createAccountForm.value.email ?? "").trim();
  const password = payload.password ?? createAccountForm.value.password ?? "";

  if (!email) {
    ElMessage.error("Email is required");
    return;
  }

  if (!password || password.length < 6) {
    ElMessage.error("Password must be at least 6 characters");
    return;
  }

  loadingCreateAccountForm.value = true;

  try {
    const createPayload: HrCreateEmployeeAccountDTO = {
      email,
      username: normalizeNullableText(payload.username ?? createAccountForm.value.username),
      password,
      role: payload.role ?? createAccountForm.value.role,
    };

    const result = await $hrEmployeeService.createAccount(
      selectedEmployee.value.id,
      createPayload,
    );

    selectedAccount.value = result.user ?? null;
    createAccountDialogVisible.value = false;
    manageAccountDialogVisible.value = true;

    ElMessage.success("Account created successfully");
    await fetchEmployees(currentPage.value);
  } catch (error) {
    console.error(error);
    ElMessage.error("Failed to create account");
  } finally {
    loadingCreateAccountForm.value = false;
  }
}

async function handleSoftDeleteAccount() {
  if (!selectedEmployee.value) return;

  try {
    await ElMessageBox.confirm("Soft delete this linked account?", "Confirm", {
      type: "warning",
      confirmButtonText: "Soft Delete",
      cancelButtonText: "Cancel",
    });

    accountActionLoading.value = true;
    selectedAccount.value = await $hrEmployeeService.softDeleteEmployeeAccount(
      selectedEmployee.value.id,
    );
    ElMessage.success("Account soft deleted successfully");
    await fetchEmployees(currentPage.value);
  } catch (error: unknown) {
    if (error === "cancel" || error === "close") return;
    console.error(error);
    ElMessage.error("Failed to soft delete account");
  } finally {
    accountActionLoading.value = false;
  }
}

async function handleRestoreAccount() {
  if (!selectedEmployee.value) return;

  accountActionLoading.value = true;
  try {
    selectedAccount.value = await $hrEmployeeService.restoreEmployeeAccount(
      selectedEmployee.value.id,
    );
    ElMessage.success("Account restored successfully");
    await fetchEmployees(currentPage.value);
  } catch (error) {
    console.error(error);
    ElMessage.error("Failed to restore account");
  } finally {
    accountActionLoading.value = false;
  }
}

/* -----------------------------
 * Search & pagination
 * ----------------------------- */
async function handleSearch() {
  currentPage.value = 1;
  await fetchEmployees(1);
}

async function handleRefresh() {
  await fetchEmployees(currentPage.value);
}

/* -----------------------------
 * Row loading placeholders
 * ----------------------------- */
const deleteLoading = ref<Record<string, boolean>>({});
const detailLoading = ref<Record<string, boolean>>({});

/* -----------------------------
 * Init
 * ----------------------------- */
onMounted(async () => {
  await fetchEmployees(1);
});
</script>

<template>
  <div class="employee-page">
    <OverviewHeader
      title="Employee Management"
      description="Manage employees and linked login accounts"
      @refresh="handleRefresh"
    >
      <template #actions>
        <div class="header-actions">
          <ElInput
            v-model="search"
            placeholder="Search employees"
            clearable
            style="width: 240px"
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          />
          <ElButton @click="handleSearch">Search</ElButton>
          <ElButton type="primary" @click="openCreateEmployeeDialog">
            Create Employee
          </ElButton>
        </div>
      </template>
    </OverviewHeader>

    <ElCard>
      <SmartTable
        :columns="employeeColumns"
        :data="rows"
        :loading="loadingTable"
      >
        <template #employee_code="{ row }">
          {{ row.employee?.employee_code || "-" }}
        </template>

        <template #full_name="{ row }">
          {{ row.employee?.full_name || "-" }}
        </template>

        <template #department="{ row }">
          {{ row.employee?.department || "-" }}
        </template>

        <template #position="{ row }">
          {{ row.employee?.position || "-" }}
        </template>

        <template #employment_type="{ row }">
          <ElTag effect="plain">
            {{ row.employee?.employment_type || "-" }}
          </ElTag>
        </template>

        <template #basic_salary="{ row }">
          {{ row.employee?.basic_salary ?? 0 }}
        </template>

        <template #employee_status="{ row }">
          <ElTag :type="getEmployeeStatusTagType(row.employee?.status)">
            {{ row.employee?.status || "unknown" }}
          </ElTag>
        </template>

        <template #account_status="{ row }">
          <div class="account-cell">
            <ElTag :type="getAccountTagType(row.account ?? null)">
              {{ row.account ? row.account.status || "linked" : "not linked" }}
            </ElTag>

            <div v-if="row.account" class="account-meta">
              {{ row.account.email || row.account.username || row.account.id }}
            </div>
          </div>
        </template>

        <template #operation="{ row }">
          <div class="row-actions">
            <ActionButtons
              :rowId="row.id"
              :detailContent="''"
              deleteContent="Delete this employee?"
              @detail="openEditEmployeeDialog(row)"
              @delete="onDeleteRow(row)"
              :deleteLoading="deleteLoading[row.id] ?? false"
              :detailLoading="detailLoading[row.id] ?? false"
            />
            <ElButton size="small" @click="openManageAccountDialog(row)">
              Manage Account
            </ElButton>
          </div>
        </template>
      </SmartTable>

      <div class="pagination">
        <ElPagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="totalRows"
          layout="prev, pager, next"
          @current-change="fetchEmployees"
        />
      </div>
    </ElCard>

    <SmartFormDialog
      v-model:modelValue="employeeForm"
      v-model:visible="employeeDialogVisible"
      :title="employeeDialogTitle"
      :fields="employeeFields"
      :loading="loadingEmployeeForm"
      :initialLoading="employeeDialogInitialLoading"
      width="800px"
      @save="handleSaveEmployeeForm"
      @cancel="handleCancelEmployeeForm"
    />

    <ManageEmployeeAccountDialog
      v-model:visible="manageAccountDialogVisible"
      :employee="selectedEmployee"
      :account="selectedAccount"
      :loading="manageAccountDialogLoading"
      :actionLoading="accountActionLoading"
      @open-create-account="openCreateAccountDialog"
      @soft-delete-account="handleSoftDeleteAccount"
      @restore-account="handleRestoreAccount"
      @close="closeManageAccountDialog"
    />

    <SmartFormDialog
      v-model:modelValue="createAccountForm"
      v-model:visible="createAccountDialogVisible"
      :title="createAccountDialogTitle"
      :fields="createAccountFields"
      :loading="loadingCreateAccountForm"
      width="640px"
      @save="handleSaveCreateAccount"
      @cancel="closeCreateAccountDialog"
    />
  </div>
</template>

<style scoped>
.employee-page {
  padding: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.pagination {
  margin-top: 10px;
  text-align: right;
}

.row-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.account-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.account-meta {
  font-size: 12px;
  color: #909399;
}
</style>
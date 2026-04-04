<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import {
  ElButton,
  ElCard,
  ElCheckbox,
  ElDatePicker,
  ElDialog,
  ElDivider,
  ElForm,
  ElFormItem,
  ElInput,
  ElInputNumber,
  ElOption,
  ElPagination,
  ElSelect,
} from "element-plus";
import { Plus, Search } from "@element-plus/icons-vue";
import { Role } from "~/api/types/enums/role.enum";

import type { ColumnConfig } from "~/components/types/tableEdit";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import ActionButtons from "~/components/buttons/ActionButtons.vue";
import WorkingScheduleSelect from "~/components/selects/hr/WorkingScheduleSelect.vue";
import WorkLocationSelect from "~/components/selects/hr/WorkLocationSelect.vue";
import type { FormInstance } from "element-plus";

import { useHrEmployeeStore } from "~/stores/hrEmployeeStore";
import type {
  HrCreateEmployeeDTO,
  HrEmployeeContractDTO,
  HrEmployeeDTO,
  HrSalaryType,
  HrEmployeeStatus,
  HrEmploymentType,
  HrUpdateEmployeeDTO,
  ListEmployeesParams,
  HrEmployeeWithAccountSummaryDTO,
} from "~/api/hr_admin/employees/dto";

definePageMeta({ layout: "default" });

type HrEmployeeViewDTO = HrEmployeeDTO & {
  schedule_id?: string | null;
  work_location_id?: string | null;
  schedule_name?: string | null;
  work_location_name?: string | null;
  schedule?: {
    id?: string;
    name?: string | null;
    label?: string | null;
  } | null;
  location?: {
    id?: string;
    name?: string | null;
    label?: string | null;
  } | null;
};

type EmployeeScope = "active" | "all" | "deleted";

type EmployeeFormModel = {
  employee_code: string;
  full_name: string;
  department: string | null;
  position: string | null;
  employment_type: HrEmploymentType;
  schedule_id: string | null;
  work_location_id: string | null;
  basic_salary: number;
  status: HrEmployeeStatus;
  contract_salary_type: HrSalaryType;
  start_date: string | null;
  end_date: string | null;
};

type EmployeeTableRow = {
  id: string;
  employee_code: string;
  full_name: string;
  department: string | null;
  position: string | null;
  employment_type: HrEmploymentType;
  schedule: string;
  work_location: string;
  basic_salary: number;
  contract_range: string;
  employee_status: string;
  is_deleted: boolean;
  employee: HrEmployeeViewDTO;
};

const employeeStore = useHrEmployeeStore();

const rows = ref<EmployeeTableRow[]>([]);
const loadingTable = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const totalRows = ref(0);
const search = ref("");
const scope = ref<EmployeeScope>("active");

const employeeDialogVisible = ref(false);
const employeeDialogInitialLoading = ref(false);
const loadingEmployeeForm = computed(
  () =>
    employeeStore.isLoading("createEmployee") ||
    employeeStore.isLoading("updateEmployee") ||
    employeeStore.createFlowStatus.creatingEmployee ||
    employeeStore.createFlowStatus.creatingAccount,
);
const employeeFormRef = ref<FormInstance>();
const isEdit = ref(false);
const editingEmployeeId = ref<string | null>(null);

const deleteLoading = ref<Record<string, boolean>>({});
const detailLoading = ref<Record<string, boolean>>({});

const createLoginAccount = ref(false);
const createAccountForm = reactive({
  email: "",
  username: "",
  password: "",
  role: Role.EMPLOYEE,
});

const employeeForm = reactive<EmployeeFormModel>({
  employee_code: "",
  full_name: "",
  department: "",
  position: "",
  employment_type: "contract",
  schedule_id: null,
  work_location_id: null,
  basic_salary: 0,
  status: "active",
  contract_salary_type: "monthly",
  start_date: "",
  end_date: "",
});

const isContractEmployment = computed(
  () => employeeForm.employment_type === "contract",
);
const showContractFields = computed(
  () => employeeForm.employment_type === "contract",
);

const employeeDialogTitle = computed(() =>
  isEdit.value ? "Edit Employee" : "Create Employee",
);

const summary = computed(() => {
  const visibleTotal = rows.value.length;
  const active = rows.value.filter(
    (r) => !r.is_deleted && r.employee.status === "active",
  ).length;
  const inactive = rows.value.filter(
    (r) => !r.is_deleted && r.employee.status === "inactive",
  ).length;
  const deleted = rows.value.filter((r) => r.is_deleted).length;

  return {
    visibleTotal,
    active,
    inactive,
    deleted,
  };
});

const scopeOptions = [
  { label: "Active", value: "active" },
  { label: "All", value: "all" },
  { label: "Deleted", value: "deleted" },
];

const employmentTypeOptions = [
  { label: "Contract", value: "contract" },
  { label: "Permanent", value: "permanent" },
];

const statusOptions = [
  { label: "Active", value: "active" },
  { label: "Inactive", value: "inactive" },
];

const salaryTypeOptions = [
  { label: "Monthly", value: "monthly" },
  { label: "Daily", value: "daily" },
  { label: "Hourly", value: "hourly" },
];

const employeeColumns: ColumnConfig<EmployeeTableRow>[] = [
  {
    field: "employee_code",
    label: "Code",
    useSlot: true,
    slotName: "employee_code",
    minWidth: "130px",
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
    minWidth: "150px",
  },
  {
    field: "position",
    label: "Position",
    useSlot: true,
    slotName: "position",
    minWidth: "150px",
  },
  {
    field: "employment_type",
    label: "Type",
    useSlot: true,
    slotName: "employment_type",
    minWidth: "120px",
  },
  {
    field: "schedule",
    label: "Schedule",
    useSlot: true,
    slotName: "schedule",
    minWidth: "170px",
  },
  {
    field: "work_location",
    label: "Work Location",
    useSlot: true,
    slotName: "work_location",
    minWidth: "170px",
  },
  {
    field: "basic_salary",
    label: "Salary",
    useSlot: true,
    slotName: "basic_salary",
    minWidth: "130px",
  },
  {
    field: "contract_range",
    label: "Contract Range",
    useSlot: true,
    slotName: "contract_range",
    minWidth: "190px",
  },
  {
    field: "employee_status",
    label: "Status",
    useSlot: true,
    slotName: "employee_status",
    minWidth: "130px",
  },
  {
    field: "id",
    operation: true,
    label: "Operation",
    inlineEditActive: false,
    align: "center",
    minWidth: "220px",
    smartProps: {},
  },
];

function normalizeNullableText(value?: string | null) {
  const trimmed = (value ?? "").trim();
  return trimmed.length ? trimmed : null;
}

function normalizeEmploymentType(value?: string | null): HrEmploymentType {
  const v = String(value ?? "")
    .trim()
    .toLowerCase();
  return v === "permanent" ? "permanent" : "contract";
}

function normalizeEmployeeStatus(value?: string | null): HrEmployeeStatus {
  const v = String(value ?? "")
    .trim()
    .toLowerCase();
  return v === "inactive" ? "inactive" : "active";
}

function formatDateOnly(date: Date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function addMonths(date: Date, months: number) {
  const next = new Date(date);
  next.setMonth(next.getMonth() + months);
  return next;
}

function asDate(value?: string | null) {
  if (!value) return null;
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d;
}

function toIsoDateTimeString(value?: string | null) {
  const d = asDate(value);
  if (!d) return "";
  return new Date(
    Date.UTC(d.getFullYear(), d.getMonth(), d.getDate(), 0, 0, 0),
  ).toISOString();
}

function generateEmployeeCode() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, "0");
  const d = String(now.getDate()).padStart(2, "0");
  const rand = String(Math.floor(Math.random() * 900) + 100);
  return `EMP-${y}${m}${d}-${rand}`;
}

function buildContractPayload(
  model: Pick<
    EmployeeFormModel,
    "start_date" | "end_date" | "basic_salary" | "contract_salary_type"
  >,
): HrEmployeeContractDTO {
  return {
    start_date: toIsoDateTimeString(model.start_date),
    end_date: toIsoDateTimeString(model.end_date),
    salary_type: model.contract_salary_type,
    rate: Number(model.basic_salary),
  };
}

function getScheduleDisplay(employee: HrEmployeeViewDTO) {
  return (
    employee.schedule_name ??
    employee.schedule?.name ??
    employee.schedule?.label ??
    employee.schedule_id ??
    "-"
  );
}

function getLocationDisplay(employee: HrEmployeeViewDTO) {
  return (
    employee.work_location_name ??
    employee.location?.name ??
    employee.location?.label ??
    employee.work_location_id ??
    "-"
  );
}

function getContractRange(employee: HrEmployeeViewDTO) {
  if (employee.employment_type !== "contract") return "Permanent";
  if (!employee.contract?.start_date || !employee.contract?.end_date)
    return "-";
  return `${employee.contract.start_date} to ${employee.contract.end_date}`;
}

function getEmployeeStatusTagType(row: EmployeeTableRow) {
  if (row.is_deleted) return "danger";
  return row.employee.status === "active" ? "success" : "warning";
}

function getEmployeeStatusLabel(row: EmployeeTableRow) {
  if (row.is_deleted) return "deleted";
  return row.employee.status;
}

function mapRows(items: HrEmployeeWithAccountSummaryDTO[]): EmployeeTableRow[] {
  return items.map((item) => {
    const employee = item.employee;
    const isDeleted = Boolean(employee.lifecycle?.deleted_at);

    return {
      id: employee.id,
      employee_code: employee.employee_code,
      full_name: employee.full_name,
      department: employee.department ?? null,
      position: employee.position ?? null,
      employment_type: employee.employment_type,
      schedule: getScheduleDisplay(employee),
      work_location: getLocationDisplay(employee),
      basic_salary: employee.basic_salary,
      contract_range: getContractRange(employee),
      employee_status: employee.status,
      is_deleted: isDeleted,
      employee,
    };
  });
}

function resetAccountForm() {
  createAccountForm.email = "";
  createAccountForm.username = "";
  createAccountForm.password = "";
  createAccountForm.role = Role.EMPLOYEE;
}

function resetEmployeeForm() {
  employeeForm.employee_code = "";
  employeeForm.full_name = "";
  employeeForm.department = "";
  employeeForm.position = "";
  employeeForm.employment_type = "contract";
  employeeForm.schedule_id = null;
  employeeForm.work_location_id = null;
  employeeForm.basic_salary = 0;
  employeeForm.status = "active";
  employeeForm.contract_salary_type = "monthly";
  employeeForm.start_date = "";
  employeeForm.end_date = "";

  createLoginAccount.value = false;
  resetAccountForm();
}

function fillEmployeeForm(employee: Partial<HrEmployeeViewDTO>) {
  employeeForm.employee_code = employee.employee_code ?? "";
  employeeForm.full_name = employee.full_name ?? "";
  employeeForm.department = employee.department ?? "";
  employeeForm.position = employee.position ?? "";
  employeeForm.employment_type = normalizeEmploymentType(
    employee.employment_type,
  );
  employeeForm.schedule_id =
    employee.schedule_id ?? employee.schedule?.id ?? null;
  employeeForm.work_location_id =
    employee.work_location_id ?? employee.location?.id ?? null;
  employeeForm.basic_salary = employee.basic_salary ?? 0;
  employeeForm.status = normalizeEmployeeStatus(employee.status);
  employeeForm.contract_salary_type =
    employee.contract?.salary_type ?? "monthly";
  employeeForm.start_date = employee.contract?.start_date ?? "";
  employeeForm.end_date = employee.contract?.end_date ?? "";

  createLoginAccount.value = false;
  resetAccountForm();
}

function validateEmployeeFormBeforeSubmit(payload: Partial<EmployeeFormModel>) {
  const employmentType =
    payload.employment_type ?? employeeForm.employment_type;
  const basicSalary = Number(payload.basic_salary ?? employeeForm.basic_salary);
  const startDate = payload.start_date ?? employeeForm.start_date;
  const endDate = payload.end_date ?? employeeForm.end_date;

  if (!String(payload.full_name ?? employeeForm.full_name).trim()) {
    return "Full name is required";
  }

  if (
    !isEdit.value &&
    !String(payload.employee_code ?? employeeForm.employee_code).trim()
  ) {
    return "Employee code is required";
  }

  if (employmentType === "contract" && basicSalary <= 0) {
    return "Contract rate must be greater than 0";
  }

  if (employmentType !== "contract" && basicSalary < 0) {
    return "Basic salary cannot be negative";
  }

  if (employmentType === "contract") {
    if (!startDate) return "Contract start date is required";
    if (!endDate) return "Contract end date is required";
    if (new Date(endDate) < new Date(startDate))
      return "Contract end date cannot be before start date";
  }

  if (!isEdit.value && createLoginAccount.value) {
    if (!createAccountForm.email.trim()) return "Account email is required";
    if (!createAccountForm.password || createAccountForm.password.length < 6) {
      return "Account password must be at least 6 characters";
    }
  }

  return null;
}

const employeeFormRules = computed(() => ({
  employee_code: [
    {
      required: !isEdit.value,
      message: "Employee code is required",
      trigger: "blur",
    },
  ],
  full_name: [
    { required: true, message: "Full name is required", trigger: "blur" },
  ],
  basic_salary: [
    {
      validator: (
        _rule: unknown,
        value: number,
        callback: (err?: Error) => void,
      ) => {
        const salary = Number(value ?? 0);
        if (isContractEmployment.value && salary <= 0) {
          callback(new Error("Contract rate must be greater than 0"));
          return;
        }
        if (!isContractEmployment.value && salary < 0) {
          callback(new Error("Basic salary cannot be negative"));
          return;
        }
        callback();
      },
      trigger: ["blur", "change"],
    },
  ],
}));

async function submitEmployeeForm() {
  if (!employeeFormRef.value) {
    await handleSaveEmployeeForm();
    return;
  }

  try {
    const valid = await employeeFormRef.value.validate();
    if (valid !== false) {
      await handleSaveEmployeeForm();
    }
  } catch {
    // Keep form open for inline errors.
  }
}

async function fetchEmployees(page = currentPage.value) {
  loadingTable.value = true;
  try {
    const params: ListEmployeesParams = {
      page,
      limit: pageSize.value,
      q: search.value.trim() || undefined,
      include_deleted: scope.value === "all",
      deleted_only: scope.value === "deleted",
    };

    const res = await employeeStore.getEmployeesWithAccounts(params);
    rows.value = mapRows(res.items ?? []);
    totalRows.value = res.total ?? 0;
    currentPage.value = page;
  } catch (error) {
    console.error(error);
    ElMessage.error(
      employeeStore.getError("getEmployeesWithAccounts") ||
        "Failed to load employees",
    );
  } finally {
    loadingTable.value = false;
  }
}

function openCreateEmployeeDialog() {
  isEdit.value = false;
  editingEmployeeId.value = null;
  resetEmployeeForm();
  employeeForm.employee_code = generateEmployeeCode();
  employeeDialogVisible.value = true;
}

async function openEditEmployeeDialog(row: EmployeeTableRow) {
  const rowId = String(row.id);
  detailLoading.value[rowId] = true;
  isEdit.value = true;
  editingEmployeeId.value = row.employee.id;
  employeeDialogVisible.value = true;
  employeeDialogInitialLoading.value = true;

  try {
    const employee = await employeeStore.getEmployee(row.employee.id);
    fillEmployeeForm(employee as HrEmployeeViewDTO);
  } catch (error) {
    console.error(error);
    fillEmployeeForm(row.employee);
    ElMessage.warning("Could not load full employee details, using row data");
  } finally {
    detailLoading.value[rowId] = false;
    employeeDialogInitialLoading.value = false;
  }
}

function handleCancelEmployeeForm() {
  employeeDialogVisible.value = false;
  isEdit.value = false;
  editingEmployeeId.value = null;
  resetEmployeeForm();
  employeeStore.resetCreateFlowStatus();
}

async function handleSaveEmployeeForm() {
  const payload: Partial<EmployeeFormModel> = { ...employeeForm };
  const validationError = validateEmployeeFormBeforeSubmit(payload);
  if (validationError) {
    ElMessage.error(validationError);
    return;
  }

  try {
    const employmentType =
      payload.employment_type ?? employeeForm.employment_type;
    const basicSalary = Number(
      payload.basic_salary ?? employeeForm.basic_salary,
    );

    if (isEdit.value && editingEmployeeId.value) {
      const updatePayload: HrUpdateEmployeeDTO & {
        schedule_id?: string | null;
        work_location_id?: string | null;
      } = {
        full_name: (payload.full_name ?? employeeForm.full_name).trim(),
        department: normalizeNullableText(
          payload.department ?? employeeForm.department,
        ),
        position: normalizeNullableText(
          payload.position ?? employeeForm.position,
        ),
        employment_type: employmentType,
        schedule_id: normalizeNullableText(
          payload.schedule_id ?? employeeForm.schedule_id,
        ),
        work_location_id: normalizeNullableText(
          payload.work_location_id ?? employeeForm.work_location_id,
        ),
        basic_salary: basicSalary,
        status: payload.status ?? employeeForm.status,
        contract:
          employmentType === "contract"
            ? buildContractPayload({
                start_date: payload.start_date ?? employeeForm.start_date,
                end_date: payload.end_date ?? employeeForm.end_date,
                basic_salary: basicSalary,
                contract_salary_type:
                  payload.contract_salary_type ??
                  employeeForm.contract_salary_type,
              })
            : null,
      };

      await employeeStore.updateEmployee(
        editingEmployeeId.value,
        updatePayload,
      );
      ElMessage.success("Employee updated successfully");
    } else {
      const createPayload: HrCreateEmployeeDTO & {
        schedule_id?: string | null;
        work_location_id?: string | null;
      } = {
        employee_code: (
          payload.employee_code ?? employeeForm.employee_code
        ).trim(),
        full_name: (payload.full_name ?? employeeForm.full_name).trim(),
        department: normalizeNullableText(
          payload.department ?? employeeForm.department,
        ),
        position: normalizeNullableText(
          payload.position ?? employeeForm.position,
        ),
        employment_type: employmentType,
        schedule_id: normalizeNullableText(
          payload.schedule_id ?? employeeForm.schedule_id,
        ),
        work_location_id: normalizeNullableText(
          payload.work_location_id ?? employeeForm.work_location_id,
        ),
        basic_salary: basicSalary,
        status: payload.status ?? employeeForm.status,
        contract:
          employmentType === "contract"
            ? buildContractPayload({
                start_date: payload.start_date ?? employeeForm.start_date,
                end_date: payload.end_date ?? employeeForm.end_date,
                basic_salary: basicSalary,
                contract_salary_type:
                  payload.contract_salary_type ??
                  employeeForm.contract_salary_type,
              })
            : null,
      };

      if (createLoginAccount.value) {
        await employeeStore.createEmployeeWithAccount(createPayload, {
          email: createAccountForm.email.trim(),
          username:
            normalizeNullableText(createAccountForm.username) ?? undefined,
          password: createAccountForm.password,
          role: createAccountForm.role,
        });
        ElMessage.success("Employee and account created successfully");
      } else {
        await employeeStore.createEmployee(createPayload);
        ElMessage.success("Employee created successfully");
      }
    }

    employeeDialogVisible.value = false;
    resetEmployeeForm();
    await fetchEmployees(currentPage.value);
  } catch (error) {
    console.error(error);
    const actionError = isEdit.value
      ? employeeStore.getError("updateEmployee")
      : employeeStore.createFlowStatus.error ||
        employeeStore.getError("createEmployee");

    ElMessage.error(
      actionError ||
        (isEdit.value
          ? "Failed to update employee"
          : "Failed to create employee"),
    );
  }
}

async function handleToggleDelete(row: EmployeeTableRow) {
  const rowId = String(row.id);
  deleteLoading.value[rowId] = true;

  try {
    if (row.is_deleted) {
      await ElMessageBox.confirm(
        `Restore employee \"${row.employee.full_name}\"?`,
        "Confirm Restore",
        {
          type: "warning",
          confirmButtonText: "Restore",
          cancelButtonText: "Cancel",
        },
      );
      await employeeStore.restoreEmployee(row.employee.id);
      ElMessage.success("Employee restored successfully");
    } else {
      await ElMessageBox.confirm(
        `Delete employee \"${row.employee.full_name}\"?`,
        "Confirm Delete",
        {
          type: "warning",
          confirmButtonText: "Delete",
          cancelButtonText: "Cancel",
        },
      );
      await employeeStore.softDeleteEmployee(row.employee.id);
      ElMessage.success("Employee deleted successfully");
    }

    await fetchEmployees(currentPage.value);
  } catch (error: unknown) {
    if (error === "cancel" || error === "close") return;
    console.error(error);
    ElMessage.error(
      row.is_deleted
        ? "Failed to restore employee"
        : "Failed to delete employee",
    );
  } finally {
    deleteLoading.value[rowId] = false;
  }
}

async function handleSearch() {
  currentPage.value = 1;
  await fetchEmployees(1);
}

async function handleRefresh() {
  await fetchEmployees(currentPage.value);
}

watch(
  () => employeeForm.employment_type,
  (newType) => {
    if (newType !== "contract") {
      employeeForm.start_date = "";
      employeeForm.end_date = "";
      if (employeeForm.basic_salary < 0) {
        employeeForm.basic_salary = 0;
      }
      return;
    }

    if (!employeeForm.start_date) {
      employeeForm.start_date = formatDateOnly(new Date());
    }

    if (!employeeForm.end_date) {
      const base = new Date(employeeForm.start_date);
      employeeForm.end_date = formatDateOnly(addMonths(base, 1));
    }

    if (employeeForm.basic_salary <= 0) {
      employeeForm.basic_salary = 1;
    }
  },
);

watch(scope, async () => {
  await handleSearch();
});

onMounted(async () => {
  await fetchEmployees(1);
});
</script>

<template>
  <div class="employee-page">
    <OverviewHeader
      title="Employee Index"
      description="Main HR registry for employee records and onboarding"
      @refresh="handleRefresh"
    >
      <template #actions>
        <div class="header-actions">
          <ElInput
            v-model="search"
            placeholder="Search by code, name, department"
            clearable
            style="width: 280px"
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          />

          <ElSelect v-model="scope" style="width: 120px">
            <ElOption
              v-for="option in scopeOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </ElSelect>

          <ElButton :icon="Search" @click="handleSearch">Search</ElButton>
          <ElButton
            type="primary"
            :icon="Plus"
            @click="openCreateEmployeeDialog"
          >
            New Employee
          </ElButton>
        </div>
      </template>
    </OverviewHeader>

    <div class="summary-grid">
      <ElCard
        ><div class="summary-title">Visible</div>
        <div class="summary-value">{{ summary.visibleTotal }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Active</div>
        <div class="summary-value">{{ summary.active }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Inactive</div>
        <div class="summary-value">{{ summary.inactive }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Deleted</div>
        <div class="summary-value">{{ summary.deleted }}</div></ElCard
      >
    </div>

    <ElCard>
      <SmartTable
        :columns="employeeColumns"
        :data="rows"
        :loading="loadingTable"
      >
        <template #employee_code="{ row }">{{
          row.employee_code || "-"
        }}</template>
        <template #full_name="{ row }">{{ row.full_name || "-" }}</template>
        <template #department="{ row }">{{ row.department || "-" }}</template>
        <template #position="{ row }">{{ row.position || "-" }}</template>
        <template #employment_type="{ row }"
          ><ElTag effect="plain">{{
            row.employment_type || "-"
          }}</ElTag></template
        >
        <template #schedule="{ row }">{{ row.schedule || "-" }}</template>
        <template #work_location="{ row }">{{
          row.work_location || "-"
        }}</template>
        <template #basic_salary="{ row }">{{ row.basic_salary ?? 0 }}</template>
        <template #contract_range="{ row }">{{
          row.contract_range || "-"
        }}</template>
        <template #employee_status="{ row }"
          ><ElTag :type="getEmployeeStatusTagType(row)">{{
            getEmployeeStatusLabel(row)
          }}</ElTag></template
        >

        <template #operation="{ row }">
          <ActionButtons
            :row-id="row.id"
            :detail-content="'Edit this employee'"
            :delete-content="
              row.is_deleted
                ? 'Restore this employee?'
                : 'Delete this employee?'
            "
            :detail-loading="detailLoading[row.id] ?? false"
            :delete-loading="deleteLoading[row.id] ?? false"
            :detail-text="'Edit'"
            :delete-text="row.is_deleted ? 'Restore' : 'Delete'"
            :on-detail="() => openEditEmployeeDialog(row)"
            :on-delete="() => handleToggleDelete(row)"
          />
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

    <ElDialog
      v-model="employeeDialogVisible"
      :title="employeeDialogTitle"
      width="860px"
      top="6vh"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      @close="handleCancelEmployeeForm"
    >
      <div v-if="employeeDialogInitialLoading" class="p-4">
        <el-skeleton :rows="6" animated />
      </div>

      <ElForm
        v-else
        ref="employeeFormRef"
        :model="employeeForm"
        :rules="employeeFormRules"
        label-position="top"
      >
        <div class="form-row-grid">
          <ElFormItem label="Employee Code" prop="employee_code">
            <ElInput
              v-model="employeeForm.employee_code"
              placeholder="Enter employee code"
              :disabled="isEdit"
              clearable
            />
          </ElFormItem>
          <ElFormItem label="Full Name" prop="full_name">
            <ElInput
              v-model="employeeForm.full_name"
              placeholder="Enter full name"
              clearable
            />
          </ElFormItem>
        </div>

        <div class="form-row-grid">
          <ElFormItem label="Department"
            ><ElInput
              v-model="employeeForm.department"
              placeholder="Enter department"
              clearable
          /></ElFormItem>
          <ElFormItem label="Position"
            ><ElInput
              v-model="employeeForm.position"
              placeholder="Enter position"
              clearable
          /></ElFormItem>
        </div>

        <div class="form-row-grid">
          <ElFormItem label="Employment Type">
            <ElSelect
              v-model="employeeForm.employment_type"
              style="width: 100%"
            >
              <ElOption
                v-for="item in employmentTypeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </ElSelect>
          </ElFormItem>
          <ElFormItem label="Status">
            <ElSelect v-model="employeeForm.status" style="width: 100%">
              <ElOption
                v-for="item in statusOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </ElSelect>
          </ElFormItem>
        </div>

        <div class="form-row-grid">
          <ElFormItem label="Working Schedule"
            ><WorkingScheduleSelect
              v-model="employeeForm.schedule_id"
              clearable
          /></ElFormItem>
          <ElFormItem label="Work Location"
            ><WorkLocationSelect
              v-model="employeeForm.work_location_id"
              clearable
          /></ElFormItem>
        </div>

        <ElFormItem
          :label="
            employeeForm.employment_type === 'contract'
              ? 'Contract Rate'
              : 'Basic Salary'
          "
          prop="basic_salary"
        >
          <ElInputNumber
            v-model="employeeForm.basic_salary"
            :min="employeeForm.employment_type === 'contract' ? 1 : 0"
            :step="1"
            controls-position="right"
            style="width: 100%"
          />
        </ElFormItem>

        <template v-if="showContractFields">
          <div class="form-row-grid">
            <ElFormItem label="Contract Salary Type">
              <ElSelect
                v-model="employeeForm.contract_salary_type"
                style="width: 100%"
              >
                <ElOption
                  v-for="item in salaryTypeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </ElSelect>
            </ElFormItem>
            <div />
          </div>

          <div class="form-row-grid">
            <ElFormItem label="Contract Start Date" prop="start_date">
              <ElDatePicker
                v-model="employeeForm.start_date"
                type="date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </ElFormItem>
            <ElFormItem label="Contract End Date" prop="end_date">
              <ElDatePicker
                v-model="employeeForm.end_date"
                type="date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
                :disabled-date="(date: Date) => { const start = asDate(employeeForm.start_date); return !!start && date.getTime() < start.getTime(); }"
              />
            </ElFormItem>
          </div>
        </template>

        <template v-if="!isEdit">
          <ElDivider content-position="left">Optional Login Account</ElDivider>
          <ElCheckbox v-model="createLoginAccount"
            >Create employee login account now</ElCheckbox
          >

          <div v-if="createLoginAccount" class="account-create-grid">
            <ElFormItem label="Account Email">
              <ElInput
                v-model="createAccountForm.email"
                placeholder="employee@company.com"
                clearable
              />
            </ElFormItem>
            <ElFormItem label="Account Username">
              <ElInput
                v-model="createAccountForm.username"
                placeholder="Optional username"
                clearable
              />
            </ElFormItem>
            <ElFormItem label="Account Password">
              <ElInput
                v-model="createAccountForm.password"
                type="password"
                show-password
                placeholder="At least 6 characters"
              />
            </ElFormItem>
            <ElFormItem label="Account Role">
              <ElSelect v-model="createAccountForm.role" style="width: 100%">
                <ElOption label="Employee" :value="Role.EMPLOYEE" />
                <ElOption label="Manager" :value="Role.MANAGER" />
                <ElOption
                  label="Payroll Manager"
                  :value="Role.PAYROLL_MANAGER"
                />
              </ElSelect>
            </ElFormItem>
          </div>

          <div v-if="createLoginAccount" class="flow-status-text">
            Employee:
            {{
              employeeStore.createFlowStatus.employeeCreated
                ? "created"
                : employeeStore.createFlowStatus.creatingEmployee
                ? "creating..."
                : "pending"
            }}
            | Account:
            {{
              employeeStore.createFlowStatus.accountCreated
                ? "created"
                : employeeStore.createFlowStatus.creatingAccount
                ? "creating..."
                : "pending"
            }}
          </div>
        </template>
      </ElForm>

      <template #footer>
        <div class="flex justify-end gap-2">
          <ElButton @click="handleCancelEmployeeForm">Cancel</ElButton>
          <ElButton
            type="primary"
            :loading="loadingEmployeeForm"
            @click="submitEmployeeForm"
            >Save</ElButton
          >
        </div>
      </template>
    </ElDialog>
  </div>
</template>

<style scoped>
.employee-page {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.summary-title {
  font-size: 12px;
  color: #909399;
}

.summary-value {
  font-size: 24px;
  font-weight: 700;
  line-height: 1.1;
}

.pagination {
  margin-top: 12px;
  text-align: right;
}

.form-row-grid,
.account-create-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.flow-status-text {
  margin-top: 6px;
  font-size: 12px;
  color: #606266;
}

@media (max-width: 960px) {
  .summary-grid,
  .form-row-grid,
  .account-create-grid {
    grid-template-columns: 1fr;
  }
}
</style>

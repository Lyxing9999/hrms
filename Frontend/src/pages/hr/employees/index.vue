<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import {
  ElCard,
  ElInput,
  ElMessage,
  ElMessageBox,
  ElOption,
  ElPagination,
  ElSelect,
  ElTag,
} from "element-plus";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import EmployeeRowActions from "~/components/hrms/employees/EmployeeRowActions.vue";
import EmployeeOnboardDialog from "~/components/hrms/employees/EmployeeOnboardDialog.vue";
import { ROUTES } from "~/constants/routes";
import { useHrEmployeeStore } from "~/stores/hrEmployeeStore";
import { Role } from "~/api/types/enums/role.enum";
import type {
  HrCreateEmployeeDTO,
  HrEmployeeWithAccountSummaryDTO,
} from "~/api/hr_admin/employees/dto";
import type { ColumnConfig } from "~/components/types/tableEdit";

definePageMeta({ layout: "default" });

const router = useRouter();
const employeeStore = useHrEmployeeStore();

const loading = ref(false);
const hasFetchedOnce = ref(false);
const onboardVisible = ref(false);
const actionLoadingById = ref<Record<string, boolean>>({});

const filters = reactive({
  q: "",
  hasAccount: "" as "" | "yes" | "no",
  status: "" as "" | "active" | "inactive",
});

const sourceRows = ref<HrEmployeeWithAccountSummaryDTO[]>([]);
const page = ref(1);
const pageSize = ref(20);

type HrOnboardRole = Role.EMPLOYEE | Role.MANAGER | Role.PAYROLL_MANAGER;

type EmployeeTableRow = {
  id: string;
  employee_code: string;
  full_name: string;
  department: string;
  position: string;
  employment_type: string;
  basic_salary: number;
  employee_status: string;
  has_account: boolean;
  account_status: string;
  account_meta: string;
  deleted_at: string | null;
  raw: HrEmployeeWithAccountSummaryDTO;
};

const isDirty = computed(() => {
  return Boolean(filters.q || filters.hasAccount || filters.status);
});

const filteredSourceRows = computed(() => {
  const q = filters.q.trim().toLowerCase();
  return sourceRows.value.filter((row) => {
    const employee = row.employee;
    const account = row.account ?? row.user ?? null;

    const accountOk =
      filters.hasAccount === ""
        ? true
        : filters.hasAccount === "yes"
        ? Boolean(account)
        : !account;

    const statusOk =
      filters.status === ""
        ? true
        : String(employee.status || "").toLowerCase() === filters.status;

    const qOk =
      !q ||
      [
        employee.employee_code,
        employee.full_name,
        employee.department || "",
        employee.position || "",
        account?.email || "",
        account?.username || "",
      ]
        .join(" ")
        .toLowerCase()
        .includes(q);

    return accountOk && statusOk && qOk;
  });
});

const filteredRows = computed<EmployeeTableRow[]>(() => {
  return filteredSourceRows.value.map((row) => {
    const employee = row.employee;
    const account = row.account ?? row.user ?? null;
    return {
      id: employee.id,
      employee_code: employee.employee_code || "-",
      full_name: employee.full_name || "-",
      department: employee.department || "-",
      position: employee.position || "-",
      employment_type: employee.employment_type || "-",
      basic_salary: Number(employee.basic_salary || 0),
      employee_status: employee.status || "unknown",
      has_account: Boolean(account),
      account_status: account?.status || (account ? "linked" : "not linked"),
      account_meta: account?.email || account?.username || account?.id || "",
      deleted_at: employee.lifecycle?.deleted_at || null,
      raw: row,
    };
  });
});

const pagedRows = computed(() => {
  const start = (page.value - 1) * pageSize.value;
  return filteredRows.value.slice(start, start + pageSize.value);
});

const stats = computed(() => {
  const total = filteredRows.value.length;
  const active = filteredRows.value.filter(
    (r) => String(r.employee_status || "").toLowerCase() === "active",
  ).length;
  const linked = filteredRows.value.filter((r) => r.has_account).length;
  const noAccount = total - linked;

  return [
    { label: "Employees", value: total, helper: "Directory" },
    { label: "Active", value: active, helper: "Current workforce" },
    { label: "Linked Account", value: linked, helper: "Can login" },
    { label: "No Account", value: noAccount, helper: "Needs action" },
  ];
});

const columns: ColumnConfig<EmployeeTableRow>[] = [
  {
    field: "employee_code",
    label: "Code",
    minWidth: "120px",
    useSlot: true,
    slotName: "employee_code",
  },
  {
    field: "full_name",
    label: "Full Name",
    minWidth: "180px",
    useSlot: true,
    slotName: "full_name",
  },
  {
    field: "department",
    label: "Department",
    minWidth: "140px",
    useSlot: true,
    slotName: "department",
  },
  {
    field: "position",
    label: "Position",
    minWidth: "140px",
    useSlot: true,
    slotName: "position",
  },
  {
    field: "employment_type",
    label: "Type",
    width: "120px",
    useSlot: true,
    slotName: "employment_type",
  },
  {
    field: "basic_salary",
    label: "Basic Salary",
    width: "140px",
    useSlot: true,
    slotName: "basic_salary",
    align: "right",
  },
  {
    field: "employee_status",
    label: "Status",
    width: "120px",
    useSlot: true,
    slotName: "employee_status",
  },
  {
    field: "account_status",
    label: "Account",
    minWidth: "180px",
    useSlot: true,
    slotName: "account_status",
  },
  {
    field: "id",
    label: "Actions",
    operation: true,
    useSlot: true,
    slotName: "operation",
    fixed: "right",
    minWidth: "280px",
  },
];

async function fetchEmployees() {
  loading.value = true;
  try {
    const res = await employeeStore.getEmployeesWithAccounts({
      page: 1,
      limit: 400,
      include_deleted: false,
      with_accounts: true,
    });

    sourceRows.value = res.items ?? [];
    hasFetchedOnce.value = true;

    const maxPage = Math.max(
      1,
      Math.ceil(filteredSourceRows.value.length / pageSize.value),
    );
    if (page.value > maxPage) page.value = maxPage;
  } catch (error) {
    const message =
      (
        error as {
          response?: { data?: { user_message?: string; message?: string } };
        }
      )?.response?.data?.user_message ||
      (
        error as {
          response?: { data?: { user_message?: string; message?: string } };
        }
      )?.response?.data?.message ||
      (error as Error)?.message ||
      "Failed to load employees";
    ElMessage.error(message);
  } finally {
    loading.value = false;
  }
}

function resetFilters() {
  filters.q = "";
  filters.hasAccount = "";
  filters.status = "";
  page.value = 1;
}

function goDetail(row: EmployeeTableRow) {
  router.push(ROUTES.HR_ADMIN.EMPLOYEE_DETAIL(row.id));
}

function assignSchedule(row: EmployeeTableRow) {
  router.push(ROUTES.HR_ADMIN.EMPLOYEE_DETAIL(row.id));
}

async function deleteEmployee(row: EmployeeTableRow) {
  const id = row.id;
  try {
    await ElMessageBox.confirm(
      `Delete employee ${row.full_name}?`,
      "Confirm Delete",
      {
        type: "warning",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      },
    );

    actionLoadingById.value[id] = true;
    await employeeStore.softDeleteEmployee(id);
    ElMessage.success("Employee deleted");
    await fetchEmployees();
  } catch (error: unknown) {
    if (error === "cancel" || error === "close") return;
    ElMessage.error(
      (
        error as {
          response?: { data?: { user_message?: string; message?: string } };
        }
      )?.response?.data?.user_message ||
        (
          error as {
            response?: { data?: { user_message?: string; message?: string } };
          }
        )?.response?.data?.message ||
        (error as Error)?.message ||
        "Failed to delete employee",
    );
  } finally {
    actionLoadingById.value[id] = false;
  }
}

async function restoreEmployee(row: EmployeeTableRow) {
  const id = row.id;
  try {
    actionLoadingById.value[id] = true;
    await employeeStore.restoreEmployee(id);
    ElMessage.success("Employee restored");
    await fetchEmployees();
  } catch (error) {
    ElMessage.error(
      (
        error as {
          response?: { data?: { user_message?: string; message?: string } };
        }
      )?.response?.data?.user_message ||
        (
          error as {
            response?: { data?: { user_message?: string; message?: string } };
          }
        )?.response?.data?.message ||
        (error as Error)?.message ||
        "Failed to restore employee",
    );
  } finally {
    actionLoadingById.value[id] = false;
  }
}

async function submitOnboard(payload: {
  employee: HrCreateEmployeeDTO;
  account: {
    email: string;
    password: string;
    username?: string;
    role?: HrOnboardRole;
  };
}) {
  loading.value = true;
  try {
    await employeeStore.createEmployeeWithAccount(payload.employee, {
      email: payload.account.email,
      password: payload.account.password,
      username: payload.account.username,
      role: payload.account.role || Role.EMPLOYEE,
    });

    onboardVisible.value = false;
    ElMessage.success("Employee onboarded successfully");
    await fetchEmployees();
  } catch (error) {
    ElMessage.error(
      (
        error as {
          response?: { data?: { user_message?: string; message?: string } };
        }
      )?.response?.data?.user_message ||
        (
          error as {
            response?: { data?: { user_message?: string; message?: string } };
          }
        )?.response?.data?.message ||
        (error as Error)?.message ||
        "Failed to onboard employee",
    );
  } finally {
    loading.value = false;
  }
}

watch(
  () => [filters.q, filters.hasAccount, filters.status, pageSize.value],
  () => {
    page.value = 1;
  },
);

onMounted(() => {
  void fetchEmployees();
});
</script>

<template>
  <div class="hr-employee-page">
    <OverviewHeader
      title="HR Employee Directory"
      description="Manage employees and account onboarding with a single clean workflow."
      :backPath="ROUTES.HR_ADMIN.EMPLOYEES"
    >
      <template #actions>
        <BaseButton
          type="primary"
          :loading="loading"
          @click="onboardVisible = true"
        >
          Onboard Employee
        </BaseButton>
      </template>
    </OverviewHeader>

    <section class="toolbar-shell">
      <div class="toolbar-left">
        <BaseButton plain :loading="loading" @click="fetchEmployees"
          >Refresh</BaseButton
        >
        <BaseButton
          plain
          @click="router.push(ROUTES.HR_ADMIN.EMPLOYEE_ARCHIVED)"
          >Archived</BaseButton
        >
        <BaseButton
          plain
          @click="router.push(ROUTES.HR_ADMIN.EMPLOYEE_ACCOUNTS)"
          >Accounts</BaseButton
        >
      </div>

      <div class="toolbar-right">
        <ElInput
          v-model="filters.q"
          clearable
          placeholder="Search by code, name, department, account..."
          class="toolbar-search"
        />
        <ElSelect v-model="filters.hasAccount" class="toolbar-select">
          <ElOption label="All Accounts" value="" />
          <ElOption label="Has Account" value="yes" />
          <ElOption label="No Account" value="no" />
        </ElSelect>
        <ElSelect v-model="filters.status" class="toolbar-select">
          <ElOption label="All Status" value="" />
          <ElOption label="Active" value="active" />
          <ElOption label="Inactive" value="inactive" />
        </ElSelect>
        <BaseButton plain :disabled="!isDirty" @click="resetFilters"
          >Reset</BaseButton
        >
      </div>
    </section>

    <section class="summary-grid">
      <article v-for="item in stats" :key="item.label" class="summary-card">
        <span class="summary-label">{{ item.label }}</span>
        <strong class="summary-value">{{ item.value }}</strong>
        <small class="summary-note">{{ item.helper }}</small>
      </article>
    </section>

    <ElCard class="table-shell">
      <SmartTable
        :data="pagedRows"
        :columns="columns"
        :loading="loading"
        :has-fetched-once="hasFetchedOnce"
      >
        <template #employee_code="{ row }">
          {{ row.employee_code }}
        </template>

        <template #full_name="{ row }">
          {{ row.full_name }}
        </template>

        <template #department="{ row }">
          {{ row.department }}
        </template>

        <template #position="{ row }">
          {{ row.position }}
        </template>

        <template #employment_type="{ row }">
          <ElTag effect="plain">{{ row.employment_type }}</ElTag>
        </template>

        <template #basic_salary="{ row }">
          {{
            Number(row.basic_salary || 0).toLocaleString("en-US", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })
          }}
        </template>

        <template #employee_status="{ row }">
          <ElTag
            :type="row.employee_status === 'active' ? 'success' : 'warning'"
            effect="plain"
          >
            {{ row.employee_status }}
          </ElTag>
        </template>

        <template #account_status="{ row }">
          <div class="account-cell">
            <ElTag :type="row.has_account ? 'success' : 'info'" effect="plain">
              {{ row.account_status }}
            </ElTag>
            <small v-if="row.has_account" class="account-meta">
              {{ row.account_meta }}
            </small>
          </div>
        </template>

        <template #operation="{ row }">
          <EmployeeRowActions
            :row="{
              id: row.id,
              full_name: row.full_name,
              deleted_at: row.deleted_at,
            }"
            :loading="actionLoadingById[row.id]"
            @detail="goDetail(row)"
            @assign-schedule="assignSchedule(row)"
            @delete="deleteEmployee(row)"
            @restore="restoreEmployee(row)"
          />
        </template>
      </SmartTable>

      <div class="pagination-wrap">
        <ElPagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          background
          layout="total, sizes, prev, pager, next"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredRows.length"
        />
      </div>
    </ElCard>

    <EmployeeOnboardDialog
      v-model:visible="onboardVisible"
      :loading="loading"
      @submitted="submitOnboard"
    />
  </div>
</template>

<style scoped>
.hr-employee-page {
  padding: 16px;
  max-width: 1460px;
  margin: 0 auto;
}

.toolbar-shell {
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  border: 1px solid var(--border-color);
  border-radius: 14px;
  background: var(--color-card);
  padding: 12px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.toolbar-search {
  width: 320px;
}

.toolbar-select {
  width: 170px;
}

.summary-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.summary-card {
  border-radius: 14px;
  border: 1px solid var(--border-color);
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--color-primary-light-8) 100%, var(--color-card)) 0%,
    var(--color-card) 100%
  );
  padding: 12px;
}

.summary-label {
  display: block;
  color: var(--muted-color);
  font-size: 12px;
}

.summary-value {
  display: block;
  margin-top: 4px;
  color: var(--text-color);
  font-size: 26px;
  font-weight: 800;
}

.summary-note {
  display: block;
  margin-top: 2px;
  color: var(--muted-color);
  font-size: 11px;
}

.table-shell {
  margin-top: 12px;
  border: 1px solid var(--border-color);
}

.account-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.account-meta {
  color: var(--muted-color);
  font-size: 12px;
}

.pagination-wrap {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 1200px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 780px) {
  .toolbar-search,
  .toolbar-select {
    width: 100%;
  }

  .toolbar-right {
    width: 100%;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import {
  ElButton,
  ElCard,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElMessage,
  ElMessageBox,
  ElOption,
  ElPagination,
  ElRow,
  ElSelect,
  ElTag,
} from "element-plus";
import type { FormInstance } from "element-plus";

import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";

import {
  employeeAccountColumns,
  type HrEmployeeAccountRow,
} from "~/modules/tables/columns/hr_admin/employeeAccountColumns";

import type {
  HrCreateEmployeeAccountDTO,
  HrEmployeeAccountListItemDTO,
  HrEmployeeDTO,
  HrEmployeeWithAccountSummaryDTO,
} from "~/api/hr_admin/employees/dto";
import { Status } from "~/api/types/enums/status.enum";
import { Role } from "~/api/types/enums/role.enum";
import { useEmployeeAccountStatusInline } from "~/composables/features/hrms/useHrUserStatusInline";
import { useHrEmployeeStore } from "~/stores/hrEmployeeStore";

definePageMeta({ layout: "default" });

type AccountRoleFilter = "all" | "employee" | "manager" | "payroll_manager";

const employeeStore = useHrEmployeeStore();

const rows = ref<HrEmployeeAccountRow[]>([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const totalRows = ref(0);
const search = ref("");
const roleFilter = ref<AccountRoleFilter>("all");

const passwordResetSaving = ref<Record<string, boolean>>({});
const deleteAccountSaving = ref<Record<string, boolean>>({});
const employeesWithoutAccounts = ref<HrEmployeeDTO[]>([]);
const unlinkedAccounts = ref<HrEmployeeAccountListItemDTO[]>([]);

const createDialogVisible = ref(false);
const createFormRef = ref<FormInstance>();
const createSaving = ref(false);
const createCandidatesLoading = ref(false);
const createCandidates = ref<HrEmployeeDTO[]>([]);
const createForm = reactive<{
  employee_id: string;
  email: string;
  username: string;
  password: string;
  role: Role;
}>({
  employee_id: "",
  email: "",
  username: "",
  password: "",
  role: Role.MANAGER,
});

const managerStats = computed(() => {
  const employee = rows.value.filter((r) => r.role === "employee").length;
  const manager = rows.value.filter((r) => r.role === "manager").length;
  const payroll = rows.value.filter((r) => r.role === "payroll_manager").length;
  const suspended = rows.value.filter(
    (r) => String(r.status).toLowerCase() === Status.SUSPENDED,
  ).length;
  const noAccount = employeesWithoutAccounts.value.length;
  const unlinked = unlinkedAccounts.value.length;

  return {
    total: rows.value.length,
    employee,
    manager,
    payroll,
    suspended,
    noAccount,
    unlinked,
  };
});

const topEmployeesWithoutAccount = computed(() =>
  employeesWithoutAccounts.value.slice(0, 6),
);

const topUnlinkedAccounts = computed(() => unlinkedAccounts.value.slice(0, 6));

function normalizeRole(raw?: string | null): string {
  return String(raw ?? "")
    .trim()
    .toLowerCase();
}

function resolveLinkedState(item: Record<string, unknown>) {
  if (typeof item.is_linked === "boolean") return item.is_linked;
  if (typeof item.linked === "boolean") return item.linked;

  const employee = item.employee as Record<string, unknown> | undefined;
  if (employee && typeof employee.id !== "undefined") return true;

  return !!item.employee;
}

function roleAllowed(role: string) {
  if (roleFilter.value === "all") {
    return (
      role === "employee" || role === "manager" || role === "payroll_manager"
    );
  }
  return role === roleFilter.value;
}

function toManagerAccountRow(
  item: HrEmployeeWithAccountSummaryDTO,
): HrEmployeeAccountRow | null {
  const account = item.account ?? item.user ?? null;
  if (!account) return null;

  const role = normalizeRole(account.role);
  if (!roleAllowed(role)) return null;

  return {
    id: item.employee.id,
    user_id: account.id,
    account_name: item.employee.full_name ?? null,
    email: account.email ?? null,
    username: account.username ?? null,
    role,
    status: account.status ?? null,
    is_linked: resolveLinkedState(item as unknown as Record<string, unknown>),
  };
}

async function fetchManagerAccounts(page = currentPage.value) {
  loading.value = true;
  try {
    const res = await employeeStore.getEmployeesWithAccounts({
      page,
      limit: pageSize.value,
      q: search.value.trim() || undefined,
      with_accounts: true,
    });

    rows.value = (res.items ?? [])
      .map(toManagerAccountRow)
      .filter((row): row is HrEmployeeAccountRow => !!row);

    const accountItems = res.items ?? [];
    employeesWithoutAccounts.value = accountItems
      .filter((item) => !(item.account ?? item.user))
      .map((item) => item.employee);

    const linkedAccountIds = new Set(
      accountItems
        .map((item) => (item.account ?? item.user)?.id)
        .filter((id): id is string => typeof id === "string" && !!id.trim()),
    );

    const accountRes = await employeeStore.getEmployeeAccounts({
      page: 1,
      limit: 300,
      q: search.value.trim() || undefined,
    });

    unlinkedAccounts.value = (accountRes.items ?? []).filter((account) => {
      const role = normalizeRole(account.role);
      return roleAllowed(role) && !linkedAccountIds.has(account.id);
    });

    totalRows.value = rows.value.length;
    currentPage.value = page;
  } catch (error) {
    console.error(error);
    ElMessage.error(
      employeeStore.getError("getEmployeesWithAccounts") ||
        "Failed to load manager accounts",
    );
  } finally {
    loading.value = false;
  }
}

function createForEmployee(employeeId: string) {
  createForm.employee_id = employeeId;
  createDialogVisible.value = true;
}

function resetCreateForm() {
  createForm.employee_id = "";
  createForm.email = "";
  createForm.username = "";
  createForm.password = "";
  createForm.role = Role.MANAGER;
}

async function fetchCreateCandidates(keyword = "") {
  createCandidatesLoading.value = true;
  try {
    const res = await employeeStore.getEmployeesWithAccounts({
      page: 1,
      limit: 200,
      q: keyword.trim() || undefined,
      with_accounts: true,
    });

    createCandidates.value = (res.items ?? [])
      .filter((item) => !(item.account ?? item.user))
      .map((item) => item.employee);
  } catch (error) {
    console.error(error);
    ElMessage.error(
      employeeStore.getError("getEmployeesWithAccounts") ||
        "Failed to load available employees",
    );
  } finally {
    createCandidatesLoading.value = false;
  }
}

async function openCreateDialog() {
  resetCreateForm();
  createDialogVisible.value = true;
  await fetchCreateCandidates();
}

function closeCreateDialog() {
  createDialogVisible.value = false;
  resetCreateForm();
}

async function submitCreateAccount() {
  if (!createForm.employee_id) {
    ElMessage.error("Please select an employee");
    return;
  }
  if (!createForm.email.trim()) {
    ElMessage.error("Email is required");
    return;
  }
  if (!createForm.password || createForm.password.length < 6) {
    ElMessage.error("Password must be at least 6 characters");
    return;
  }

  const payload: HrCreateEmployeeAccountDTO = {
    email: createForm.email.trim(),
    username: createForm.username.trim() || undefined,
    password: createForm.password,
    role: createForm.role,
  };

  createSaving.value = true;
  try {
    await employeeStore.createAccount(createForm.employee_id, payload);
    ElMessage.success("Employee account created successfully");
    closeCreateDialog();
    await fetchManagerAccounts(currentPage.value);
  } catch (error) {
    console.error(error);
    ElMessage.error(
      employeeStore.getError("createAccount") || "Failed to create account",
    );
  } finally {
    createSaving.value = false;
  }
}

async function copyText(value: string) {
  if (!value) return false;
  try {
    await navigator.clipboard.writeText(value);
    return true;
  } catch {
    return false;
  }
}

async function handlePasswordReset(row: HrEmployeeAccountRow) {
  try {
    await ElMessageBox.confirm(
      `Reset password for ${row.account_name || row.email || row.id}?`,
      "Confirm Password Reset",
      {
        type: "warning",
        confirmButtonText: "Reset",
        cancelButtonText: "Cancel",
      },
    );

    const rowId = String(row.id);
    passwordResetSaving.value[rowId] = true;
    const resetResult = await employeeStore.requestEmployeeAccountPasswordReset(
      row.id,
    );

    const resetLink = resetResult?.reset_link?.trim() || "";
    if (!resetLink) {
      ElMessage.success("Password reset requested successfully");
      return;
    }

    try {
      await ElMessageBox.confirm(
        `Reset link:\n${resetLink}\n\nClick Copy to copy this link.`,
        "Password Reset Link",
        {
          type: "success",
          confirmButtonText: "Copy Link",
          cancelButtonText: "Close",
          distinguishCancelAndClose: true,
        },
      );

      const copied = await copyText(resetLink);
      if (copied) {
        ElMessage.success("Reset link copied");
      } else {
        ElMessage.warning("Could not copy automatically. Please copy manually");
      }
    } catch {
      // User closed the dialog.
    }
  } catch (error: any) {
    if (error === "cancel" || error === "close") return;
    console.error(error);
    ElMessage.error(
      employeeStore.getError("requestEmployeeAccountPasswordReset") ||
        "Failed to send password reset link",
    );
  } finally {
    passwordResetSaving.value[String(row.id)] = false;
  }
}

async function handleDeleteAccount(row: HrEmployeeAccountRow) {
  try {
    await ElMessageBox.confirm(
      `Delete account for ${row.account_name || row.email || row.id}?`,
      "Confirm Delete Account",
      {
        type: "warning",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      },
    );

    const rowId = String(row.id);
    deleteAccountSaving.value[rowId] = true;
    await employeeStore.softDeleteEmployeeAccount(row.id);
    ElMessage.success("Account deleted successfully");
    await fetchManagerAccounts(currentPage.value);
  } catch (error: any) {
    if (error === "cancel" || error === "close") return;
    console.error(error);
    ElMessage.error(
      employeeStore.getError("softDeleteEmployeeAccount") ||
        "Failed to delete account",
    );
  } finally {
    deleteAccountSaving.value[String(row.id)] = false;
  }
}

async function handleSearch() {
  currentPage.value = 1;
  await fetchManagerAccounts(1);
}

onMounted(async () => {
  await fetchManagerAccounts(1);
});

const { statusTagType, formatStatusLabel } = useEmployeeAccountStatusInline();
</script>

<template>
  <div class="manager-account-page">
    <OverviewHeader
      title="Employee Accounts"
      description="Control center for employee, manager, and payroll-manager access"
      @refresh="fetchManagerAccounts(currentPage)"
    >
      <template #actions>
        <div class="header-actions">
          <ElButton type="primary" @click="openCreateDialog">
            Create Employee Account
          </ElButton>

          <ElInput
            v-model="search"
            placeholder="Search by name, username, email"
            clearable
            style="width: 280px"
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          />

          <ElSelect
            v-model="roleFilter"
            style="width: 170px"
            @change="handleSearch"
          >
            <ElOption label="All Roles" value="all" />
            <ElOption label="Employee" value="employee" />
            <ElOption label="Manager" value="manager" />
            <ElOption label="Payroll Manager" value="payroll_manager" />
          </ElSelect>

          <ElButton @click="handleSearch">Search</ElButton>
        </div>
      </template>
    </OverviewHeader>

    <div class="summary-grid">
      <ElCard
        ><div class="summary-title">Visible Accounts</div>
        <div class="summary-value">{{ managerStats.total }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Employee</div>
        <div class="summary-value">{{ managerStats.employee }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Manager</div>
        <div class="summary-value">{{ managerStats.manager }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Payroll Manager</div>
        <div class="summary-value">{{ managerStats.payroll }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Suspended</div>
        <div class="summary-value">{{ managerStats.suspended }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Employees Without Account</div>
        <div class="summary-value">{{ managerStats.noAccount }}</div></ElCard
      >
      <ElCard
        ><div class="summary-title">Unlinked Accounts</div>
        <div class="summary-value">{{ managerStats.unlinked }}</div></ElCard
      >
    </div>

    <div class="insight-grid">
      <ElCard>
        <template #header>
          <div class="insight-title">Employees Without Account</div>
        </template>
        <div v-if="topEmployeesWithoutAccount.length === 0" class="empty-note">
          No employees without account.
        </div>
        <div v-else class="insight-list">
          <div
            v-for="employee in topEmployeesWithoutAccount"
            :key="employee.id"
            class="insight-row"
          >
            <div>
              <div class="row-main">{{ employee.full_name }}</div>
              <div class="row-sub">{{ employee.employee_code }}</div>
            </div>
            <ElButton
              size="small"
              type="primary"
              plain
              @click="createForEmployee(employee.id)"
            >
              Create Account
            </ElButton>
          </div>
        </div>
      </ElCard>

      <ElCard>
        <template #header>
          <div class="insight-title">Accounts Not Linked</div>
        </template>
        <div v-if="topUnlinkedAccounts.length === 0" class="empty-note">
          No unlinked accounts for selected roles.
        </div>
        <div v-else class="insight-list">
          <div
            v-for="account in topUnlinkedAccounts"
            :key="account.id"
            class="insight-row"
          >
            <div>
              <div class="row-main">
                {{ account.username || account.email || account.id }}
              </div>
              <div class="row-sub">
                {{ account.role || "-" }} | {{ account.status || "-" }}
              </div>
            </div>
            <ElTag type="warning" effect="plain">Not linked</ElTag>
          </div>
        </div>
      </ElCard>
    </div>

    <ElCard>
      <SmartTable
        :data="rows"
        :columns="employeeAccountColumns"
        :loading="loading"
        :has-fetched-once="true"
      >
        <template #role="{ row }">
          <ElTag
            :type="row.role === 'payroll_manager' ? 'warning' : 'primary'"
            effect="plain"
          >
            {{ row.role || "-" }}
          </ElTag>
        </template>

        <template #status="{ row }">
          <ElTag
            :type="statusTagType((row.status ?? Status.ACTIVE) as Status)"
            effect="plain"
            size="small"
          >
            {{ formatStatusLabel((row.status ?? Status.ACTIVE) as Status) }}
          </ElTag>
        </template>

        <template #operation="{ row }">
          <div class="operation-actions">
            <ElButton
              size="small"
              type="danger"
              plain
              :loading="deleteAccountSaving?.[String(row.id)] ?? false"
              @click="handleDeleteAccount(row)"
            >
              Delete
            </ElButton>
            <ElButton
              size="small"
              type="warning"
              plain
              :loading="passwordResetSaving?.[String(row.id)] ?? false"
              @click="handlePasswordReset(row)"
            >
              Reset / Copy Link
            </ElButton>
          </div>
        </template>
      </SmartTable>

      <ElRow v-if="totalRows > 0" justify="end" class="mt-6">
        <ElPagination
          :current-page="currentPage"
          :page-size="pageSize"
          :total="totalRows"
          layout="total, prev, pager, next, jumper"
          @current-change="fetchManagerAccounts"
        />
      </ElRow>
    </ElCard>

    <ElDialog
      v-model="createDialogVisible"
      title="Create Employee Account"
      width="640px"
      @close="closeCreateDialog"
    >
      <ElForm ref="createFormRef" label-position="top">
        <ElFormItem label="Employee">
          <ElSelect
            v-model="createForm.employee_id"
            filterable
            clearable
            :loading="createCandidatesLoading"
            placeholder="Select employee without account"
            style="width: 100%"
          >
            <ElOption
              v-for="employee in createCandidates"
              :key="employee.id"
              :label="`${employee.employee_code} - ${employee.full_name}`"
              :value="employee.id"
            />
          </ElSelect>
        </ElFormItem>

        <ElFormItem label="Email">
          <ElInput
            v-model="createForm.email"
            placeholder="employee@company.com"
            clearable
          />
        </ElFormItem>

        <ElFormItem label="Username">
          <ElInput
            v-model="createForm.username"
            placeholder="Optional username"
            clearable
          />
        </ElFormItem>

        <ElFormItem label="Password">
          <ElInput
            v-model="createForm.password"
            type="password"
            show-password
            placeholder="At least 6 characters"
          />
        </ElFormItem>

        <ElFormItem label="Role">
          <ElSelect v-model="createForm.role" style="width: 100%">
            <ElOption label="Employee" :value="Role.EMPLOYEE" />
            <ElOption label="Manager" :value="Role.MANAGER" />
            <ElOption label="Payroll Manager" :value="Role.PAYROLL_MANAGER" />
          </ElSelect>
        </ElFormItem>
      </ElForm>

      <template #footer>
        <div class="dialog-actions">
          <ElButton @click="closeCreateDialog">Cancel</ElButton>
          <ElButton
            type="primary"
            :loading="createSaving"
            @click="submitCreateAccount"
          >
            Create Account
          </ElButton>
        </div>
      </template>
    </ElDialog>
  </div>
</template>

<style scoped>
.manager-account-page {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.header-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.operation-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.insight-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.insight-title {
  font-weight: 600;
}

.insight-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.insight-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.row-main {
  font-weight: 600;
}

.row-sub,
.empty-note {
  font-size: 12px;
  color: #909399;
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

@media (max-width: 960px) {
  .summary-grid,
  .insight-grid {
    grid-template-columns: 1fr;
  }
}
</style>

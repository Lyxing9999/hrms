<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useNuxtApp } from "#app";
import {
  ElButton,
  ElCard,
  ElInput,
  ElMessage,
  ElMessageBox,
  ElPagination,
  ElRow,
} from "element-plus";

import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import LinkEmployeeAccountDialog from "~/components/hrms/accounts/LinkEmployeeAccountDialog.vue";

import { type HrEmployeeAccountRow } from "~/modules/tables/columns/hr_admin/employeeAccountColumns";

import { employeeColumns } from "~/modules/tables/columns/hr_admin/employeeColumns";

import type { HrEmployeeDTO } from "~/api/hr_admin/employees/dto";

definePageMeta({ layout: "default" });

const { $hrEmployeeService } = useNuxtApp();

/* account list */
const rows = ref<HrEmployeeAccountRow[]>([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const totalRows = ref(0);
const search = ref("");

/* link dialog */
const linkDialogVisible = ref(false);
const linkDialogLoading = ref(false);
const selectedAccount = ref<HrEmployeeAccountRow | null>(null);
const candidateEmployees = ref<HrEmployeeDTO[]>([]);

const selectedAccountLabel = computed(() => {
  if (!selectedAccount.value) return "";
  return (
    selectedAccount.value.email ||
    selectedAccount.value.username ||
    selectedAccount.value.id
  );
});

/* fetch account page */
async function fetchAccounts(page = currentPage.value) {
  loading.value = true;
  try {
    const res = await $hrEmployeeService.getEmployeeAccounts({
      page,
      limit: pageSize.value,
      q: search.value.trim() || undefined,
    });

    rows.value = res.items ?? [];
    totalRows.value = res.total ?? 0;
    currentPage.value = page;
  } catch (error) {
    console.error(error);
    ElMessage.error("Failed to load employee accounts");
  } finally {
    loading.value = false;
  }
}

/* open link dialog */
async function openLinkDialog(row: HrEmployeeAccountRow) {
  selectedAccount.value = row;
  linkDialogVisible.value = true;
  await fetchCandidateEmployees();
}

/* fetch unlinked employees for linking */
async function fetchCandidateEmployees(keyword = "") {
  linkDialogLoading.value = true;
  try {
    const res = await $hrEmployeeService.getEmployeesWithAccounts({
      page: 1,
      limit: 100,
      q: keyword || undefined,
    });

    const items = res.items ?? [];

    candidateEmployees.value = items
      .filter((item) => !item.account)
      .map((item) => item.employee)
      .filter(Boolean);
  } catch (error) {
    console.error(error);
    ElMessage.error("Failed to load employees for linking");
  } finally {
    linkDialogLoading.value = false;
  }
}

/* link account -> employee */
async function handleLinkEmployee(employee: HrEmployeeDTO) {
  console.log("handleLinkEmployee called");
  console.log("selectedAccount.value =", selectedAccount.value);
  console.log("employee =", employee);

  const account = selectedAccount.value;
  if (!account) {
    console.warn("No selected account");
    return;
  }

  try {
    await ElMessageBox.confirm(
      `Link account "${
        account.email || account.username || account.id
      }" to employee "${employee.full_name}"?`,
      "Confirm Link",
      {
        type: "warning",
        confirmButtonText: "Link",
        cancelButtonText: "Cancel",
      },
    );

    const payload = {
      user_id: account.id,
    };

    console.log("link payload =", payload);

    const result = await $hrEmployeeService.linkAccount(employee.id, payload);
    console.log("link result =", result);

    ElMessage.success("Account linked successfully");

    linkDialogVisible.value = false;
    selectedAccount.value = null;
    candidateEmployees.value = [];

    await fetchAccounts(currentPage.value);
  } catch (error: any) {
    if (error === "cancel" || error === "close") return;
    console.error("link failed =", error);
    ElMessage.error("Failed to link account");
  }
}
function handleCloseLinkDialog() {
  linkDialogVisible.value = false;
  selectedAccount.value = null;
  candidateEmployees.value = [];
}

/* search */
async function handleSearch() {
  currentPage.value = 1;
  await fetchAccounts(1);
}

onMounted(async () => {
  await fetchAccounts(1);
});
import { useEmployeeAccountStatusInline } from "../../../composables/features/hrms/useHrUserStatusInline";
import { Status } from "../../../api/types/enums/status.enum";
const {
  editingStatusRowId,
  statusDraft,
  statusSaving,
  statusTagType,
  formatStatusLabel,
  startEditStatus,
  cancelEditStatus,
  saveStatus,
} = useEmployeeAccountStatusInline();

function updateStatusDraft(val: Status) {
  statusDraft.value = val;
}
import InlineStatusCell from "../../../components/table-edit/cells/InlineStatusCell.vue";
const statusOptions = [
  { label: "Active", value: Status.ACTIVE },
  { label: "Inactive", value: Status.INACTIVE },
  { label: "Suspended", value: Status.SUSPENDED },
];
</script>

<template>
  <div class="p-4 space-y-6">
    <OverviewHeader
      title="Employee Accounts"
      description="Manage employee-role IAM accounts and link them to employees"
      @refresh="fetchAccounts(currentPage)"
    >
      <template #actions>
        <div class="flex gap-2 items-center flex-wrap">
          <ElInput
            v-model="search"
            placeholder="Search username or email"
            clearable
            style="width: 260px"
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          />
          <ElButton @click="handleSearch">Search</ElButton>
        </div>
      </template>
    </OverviewHeader>

    <ElCard>
      <SmartTable
        :data="rows"
        :columns="employeeColumns"
        :loading="loading"
        :has-fetched-once="true"
      >
        <template #status="{ row }">
          <InlineStatusCell
            :row-id="row.id"
            :value="(row.status ?? Status.ACTIVE) as Status"
            :editing-row-id="editingStatusRowId"
            :draft="statusDraft"
            :options="statusOptions"
            :tag-type="statusTagType"
            :format-label="formatStatusLabel"
            :loading="statusSaving?.[String(row.id)] ?? false"
            @start="startEditStatus(row)"
            @cancel="cancelEditStatus()"
            @save="(val) => saveStatus(row, val as Status)"
            @update:draft="(val) => updateStatusDraft(val as Status)"
          />
        </template>

        <template #operation="{ row }">
          <div class="flex gap-2 items-center">
            <ElButton size="small" type="primary" @click="openLinkDialog(row)">
              Link Employee
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
          @current-change="fetchAccounts"
        />
      </ElRow>
    </ElCard>

    <LinkEmployeeAccountDialog
      v-model:visible="linkDialogVisible"
      :loading="linkDialogLoading"
      :employees="candidateEmployees"
      :selectedAccountLabel="selectedAccountLabel"
      @search="fetchCandidateEmployees"
      @select="handleLinkEmployee"
      @close="handleCloseLinkDialog"
    />
  </div>
</template>

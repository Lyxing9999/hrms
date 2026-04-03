<script setup lang="ts">
import { ref, computed } from "vue";
import { useNuxtApp } from "nuxt/app";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import ActionButtons from "~/components/buttons/ActionButtons.vue";
import {
  ElCard,
  ElMessageBox,
  ElTag,
  ElButton,
  ElRow,
  ElCol,
  ElInput,
  ElSelect,
  ElOption,
} from "element-plus";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { useFormCreate } from "~/composables/forms/useFormCreate";
import type { OvertimeRequestDTO } from "~/api/hr_admin/overtimeRequest";
import { overtimeColumns } from "~/modules/tables/columns/hr_admin/overtimeColumns";
import {
  overtimeFormSchema,
  overtimeUpdateFormSchema,
  getOvertimeFormData,
  getOvertimeUpdateFormData,
} from "~/modules/forms/hr_admin/overtime/";
import { useAuthStore } from "~/stores/authStore";

const { $hrmsAdminService } = useNuxtApp();
const authStore = useAuthStore();

const deleteLoading = ref<Record<string | number, boolean>>({});
const actionLoading = ref<Record<string | number, boolean>>({});

const q = ref("");
const statusFilter = ref<string | undefined>("pending");

const {
  data: requests,
  error: tableError,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = usePaginatedFetch<OvertimeRequestDTO, void>(
  async (_unusedFilter, page, size, signal) => {
    const keyword = q.value.trim();
    const res = await $hrmsAdminService().overtimeRequest.getMyRequests({
      q: keyword.length ? keyword : undefined,
      status: statusFilter.value as any,
      signal,
    });

    return {
      items: (res ?? []) as OvertimeRequestDTO[],
      total: res.length ?? 0,
    };
  },
  { initialPage: 1 },
);

// Create Overtime Request Form
const {
  formDialogVisible: createFormVisible,
  formData: createFormData,
  schema: createFormSchema,
  saveForm: saveCreateForm,
  cancelForm: cancelCreateForm,
  openForm: openCreateForm,
  loading: createFormLoading,
} = useFormCreate(
  () => async (data: any) => {
    return await $hrmsAdminService().overtimeRequest.createRequest(data);
  },
  () => getOvertimeFormData(),
  () => overtimeFormSchema,
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

// Update Overtime Request Form
const updateFormVisible = ref(false);
const updateFormData = ref<any>({});
const updateFormLoading = ref(false);
const currentOvertimeId = ref<string>("");

const handleOpenUpdateForm = async (row: OvertimeRequestDTO) => {
  if (row.status !== "pending") {
    ElMessageBox.alert(
      "Only pending overtime requests can be updated",
      "Cannot Update",
      { type: "warning" },
    );
    return;
  }

  currentOvertimeId.value = row.id;
  updateFormData.value = getOvertimeUpdateFormData(row);
  updateFormVisible.value = true;
};

const handleUpdateSave = async (form: any) => {
  updateFormLoading.value = true;
  try {
    await $hrmsAdminService().overtimeRequest.updateRequest(
      currentOvertimeId.value,
      form,
    );
    updateFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    updateFormLoading.value = false;
  }
};

// Cancel Overtime Request
const handleCancelRequest = async (row: OvertimeRequestDTO) => {
  if (row.status !== "pending") {
    ElMessageBox.alert(
      "Only pending overtime requests can be cancelled",
      "Cannot Cancel",
      { type: "warning" },
    );
    return;
  }

  try {
    await ElMessageBox.confirm(
      "Are you sure you want to cancel this overtime request?",
      "Confirm Cancel",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "warning" },
    );

    actionLoading.value[row.id] = true;
    await $hrmsAdminService().overtimeRequest.cancelRequest(row.id);
    await fetchPage(currentPage.value || 1);
  } finally {
    actionLoading.value[row.id] = false;
  }
};

// Status tag color
const getStatusTagType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: "warning",
    approved: "success",
    rejected: "danger",
    cancelled: "info",
  };
  return typeMap[status] || "";
};

// Initial load
await fetchPage(1);
</script>

<template>
  <OverviewHeader
    :title="'My Overtime Requests'"
    :description="'Submit and manage your overtime requests'"
    :backPath="'/hr/overtime'"
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
        New Request
      </BaseButton>
    </template>
  </OverviewHeader>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="12">
      <el-input
        v-model="q"
        placeholder="Search by reason..."
        clearable
        @clear="fetchPage(1)"
      />
    </el-col>
    <el-col :span="12">
      <el-select
        v-model="statusFilter"
        placeholder="Filter by status"
        clearable
        @change="fetchPage(1)"
      >
        <el-option label="All" :value="undefined" />
        <el-option label="Pending" value="pending" />
        <el-option label="Approved" value="approved" />
        <el-option label="Rejected" value="rejected" />
        <el-option label="Cancelled" value="cancelled" />
      </el-select>
    </el-col>
  </el-row>

  <SmartTable
    :columns="overtimeColumns"
    :data="requests"
    :loading="initialLoading || fetching"
    :total="totalRows"
    :page="currentPage"
    :page-size="pageSize"
    @page="goPage"
    @page-size="setPageSize"
  >
    <template #status="{ row }">
      <el-tag :type="getStatusTagType(row.status)" size="small">
        {{ row.status.charAt(0).toUpperCase() + row.status.slice(1) }}
      </el-tag>
    </template>

    <template #operation="{ row }">
      <el-space>
        <!-- Edit (only pending) -->
        <el-button
          v-if="row.status === 'pending'"
          type="primary"
          size="small"
          link
          @click="handleOpenUpdateForm(row as OvertimeRequestDTO)"
        >
          Edit
        </el-button>

        <!-- Cancel (pending only) -->
        <el-button
          v-if="row.status === 'pending'"
          type="warning"
          size="small"
          link
          :loading="actionLoading[row.id]"
          @click="handleCancelRequest(row as OvertimeRequestDTO)"
        >
          Cancel
        </el-button>

        <!-- View details (read-only) -->
        <el-button type="info" size="small" link> View </el-button>
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

  <!-- Create Overtime Request Dialog -->
  <SmartFormDialog
    :key="createDialogKey"
    v-model:visible="createFormVisible"
    :model-value="createFormData"
    :fields="createFormSchema"
    :width="'50%'"
    :loading="createFormLoading"
    :disabled="createFormLoading"
    title="Submit Overtime Request"
    useElForm
    @save="handleCreateSave"
    @cancel="cancelCreateForm"
  />

  <!-- Update Overtime Request Dialog -->
  <SmartFormDialog
    v-model:visible="updateFormVisible"
    :model-value="updateFormData"
    :fields="overtimeUpdateFormSchema"
    :width="'50%'"
    :loading="updateFormLoading"
    :disabled="updateFormLoading"
    title="Update Overtime Request"
    useElForm
    @save="handleUpdateSave"
    @cancel="updateFormVisible = false"
  />
</template>

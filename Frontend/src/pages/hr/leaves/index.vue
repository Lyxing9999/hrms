<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { LeaveDTO } from "~/api/hr_admin/leave/leave.dto";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { ElTag, ElButton, ElMessageBox } from "element-plus";
import { usePreferencesStore } from "~/stores/preferencesStore";
import ActionButtons from "~/components/buttons/ActionButtons.vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import { leaveColumns } from "~/modules/tables/columns/hr_admin/leaveColumns";
import {
  getLeaveFormData,
  getLeaveUpdateFormData,
  leaveFormSchema,
  leaveReviewFormSchema,
} from "~/modules/forms/hr_admin/leave/";
import { useFormCreate } from "~/composables/forms/useFormCreate";
import { useAuthStore } from "~/stores/authStore";

const { $hrLeaveService } = useNuxtApp();
const authStore = useAuthStore();

const detailLoading = ref<Record<string | number, boolean>>({});
const deleteLoading = ref<Record<string | number, boolean>>({});
const actionLoading = ref<Record<string | number, boolean>>({});

const q = ref("");
const statusFilter = ref<string | undefined>(undefined);
const include_deleted = ref(false);
const deleted_only = ref(false);

// Check user role
const isManager = computed(() => {
  const role = authStore.user?.role;
  return role === "manager" || role === "hr_admin" || role === "admin";
});

const isEmployee = computed(() => {
  const role = authStore.user?.role;
  return role === "employee";
});

const {
  data: leaves,
  error: tableError,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = usePaginatedFetch<LeaveDTO, void>(
  async (_unusedFilter, page, size, signal) => {
    const keyword = q.value.trim();
    const res = await $hrLeaveService.getLeaves({
      q: keyword.length ? keyword : undefined,
      page,
      limit: size,
      status: statusFilter.value,
      include_deleted: include_deleted.value,
      deleted_only: deleted_only.value,
      signal,
    });

    return {
      items: (res.items ?? []) as LeaveDTO[],
      total: res.total ?? 0,
    };
  },
  { initialPage: 1 }
);

watch([q, statusFilter, include_deleted, deleted_only], () => {
  fetchPage(1);
});

// Create Leave Form
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
    return await $hrLeaveService.submitLeave(data);
  },
  () => getLeaveFormData(),
  () => leaveFormSchema
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

// Update Leave Form
const updateFormVisible = ref(false);
const updateFormData = ref<any>({});
const updateFormLoading = ref(false);
const currentLeaveId = ref<string>("");

const handleOpenUpdateForm = async (row: LeaveDTO) => {
  if (row.status !== "pending") {
    ElMessageBox.alert(
      "Only pending leave requests can be updated",
      "Cannot Update",
      { type: "warning" }
    );
    return;
  }

  currentLeaveId.value = row.id;
  updateFormData.value = getLeaveUpdateFormData(row);
  updateFormVisible.value = true;
};

const handleUpdateSave = async (form: any) => {
  updateFormLoading.value = true;
  try {
    await $hrLeaveService.updateLeave(currentLeaveId.value, form);
    updateFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    updateFormLoading.value = false;
  }
};

// Review Leave (Approve/Reject)
const reviewFormVisible = ref(false);
const reviewFormData = ref<any>({ comment: "" });
const reviewFormLoading = ref(false);
const reviewAction = ref<"approve" | "reject">("approve");

const handleOpenReviewForm = async (
  row: LeaveDTO,
  action: "approve" | "reject"
) => {
  if (row.status !== "pending") {
    ElMessageBox.alert(
      "Only pending leave requests can be reviewed",
      "Cannot Review",
      { type: "warning" }
    );
    return;
  }

  currentLeaveId.value = row.id;
  reviewAction.value = action;
  reviewFormData.value = { comment: "" };
  reviewFormVisible.value = true;
};

const handleReviewSave = async (form: any) => {
  reviewFormLoading.value = true;
  try {
    if (reviewAction.value === "approve") {
      await $hrLeaveService.approveLeave(currentLeaveId.value, form);
    } else {
      await $hrLeaveService.rejectLeave(currentLeaveId.value, form);
    }
    reviewFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    reviewFormLoading.value = false;
  }
};

// Cancel Leave
const handleCancelLeave = async (row: LeaveDTO) => {
  if (row.status !== "pending") {
    ElMessageBox.alert(
      "Only pending leave requests can be cancelled",
      "Cannot Cancel",
      { type: "warning" }
    );
    return;
  }

  try {
    await ElMessageBox.confirm(
      "Are you sure you want to cancel this leave request?",
      "Confirm Cancel",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "warning" }
    );

    actionLoading.value[row.id] = true;
    await $hrLeaveService.cancelLeave(row.id);
    await fetchPage(currentPage.value || 1);
  } finally {
    actionLoading.value[row.id] = false;
  }
};

// Soft Delete
const handleSoftDeleteLeave = async (row: LeaveDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to delete this leave request?",
      "Warning",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "warning" }
    );

    deleteLoading.value[row.id] = true;
    await $hrLeaveService.softDeleteLeave(row.id);

    const page = currentPage.value || 1;
    await fetchPage(page);

    if (page > 1 && (leaves.value?.length ?? 0) === 0) {
      await fetchPage(page - 1);
    }
  } finally {
    deleteLoading.value[row.id] = false;
  }
};

// Initial load
await fetchPage(1);

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
</script>

<template>
  <OverviewHeader
    :title="'Leave Management'"
    :description="'Manage employee leave requests'"
    :backPath="'/hr'"
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
        Submit Leave Request
      </BaseButton>
    </template>
  </OverviewHeader>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="6">
      <el-input
        v-model="q"
        placeholder="Search by reason..."
        clearable
        @clear="fetchPage(1)"
      />
    </el-col>
    <el-col :span="6">
      <el-select
        v-model="statusFilter"
        placeholder="Filter by status"
        clearable
        @change="fetchPage(1)"
      >
        <el-option label="Pending" value="pending" />
        <el-option label="Approved" value="approved" />
        <el-option label="Rejected" value="rejected" />
        <el-option label="Cancelled" value="cancelled" />
      </el-select>
    </el-col>
  </el-row>

  <SmartTable
    :columns="leaveColumns"
    :data="leaves"
    :loading="initialLoading || fetching"
    :total="totalRows"
    :page="currentPage"
    :page-size="pageSize"
    @page="goPage"
    @page-size="setPageSize"
  >
    <template #status="{ row }">
      <el-tag :type="getStatusTagType(row.status)" size="small">
        {{ row.status.toUpperCase() }}
      </el-tag>
    </template>

    <template #operation="{ row }">
      <el-space>
        <!-- Update (only pending) -->
        <el-button
          v-if="row.status === 'pending'"
          type="primary"
          size="small"
          link
          @click="handleOpenUpdateForm(row as LeaveDTO)"
        >
          Edit
        </el-button>

        <!-- Approve/Reject (Manager only, pending only) -->
        <template v-if="isManager && row.status === 'pending'">
          <el-button
            type="success"
            size="small"
            link
            :loading="actionLoading[row.id]"
            @click="handleOpenReviewForm(row as LeaveDTO, 'approve')"
          >
            Approve
          </el-button>
          <el-button
            type="danger"
            size="small"
            link
            :loading="actionLoading[row.id]"
            @click="handleOpenReviewForm(row as LeaveDTO, 'reject')"
          >
            Reject
          </el-button>
        </template>

        <!-- Cancel (Employee, pending only) -->
        <el-button
          v-if="row.status === 'pending'"
          type="warning"
          size="small"
          link
          :loading="actionLoading[row.id]"
          @click="handleCancelLeave(row as LeaveDTO)"
        >
          Cancel
        </el-button>

        <!-- Delete (Admin only) -->
        <el-button
          v-if="isManager"
          type="danger"
          size="small"
          link
          :loading="deleteLoading[row.id]"
          @click="handleSoftDeleteLeave(row as LeaveDTO)"
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

  <!-- Create Leave Dialog -->
  <SmartFormDialog
    :key="createDialogKey"
    v-model:visible="createFormVisible"
    :model-value="createFormData"
    :fields="createFormSchema"
    :width="'40%'"
    :loading="createFormLoading"
    :disabled="createFormLoading"
    title="Submit Leave Request"
    useElForm
    @save="handleCreateSave"
    @cancel="cancelCreateForm"
  />

  <!-- Update Leave Dialog -->
  <SmartFormDialog
    v-model:visible="updateFormVisible"
    :model-value="updateFormData"
    :fields="leaveFormSchema"
    :width="'40%'"
    :loading="updateFormLoading"
    :disabled="updateFormLoading"
    title="Update Leave Request"
    useElForm
    @save="handleUpdateSave"
    @cancel="updateFormVisible = false"
  />

  <!-- Review Leave Dialog -->
  <SmartFormDialog
    v-model:visible="reviewFormVisible"
    :model-value="reviewFormData"
    :fields="leaveReviewFormSchema"
    :width="'40%'"
    :loading="reviewFormLoading"
    :disabled="reviewFormLoading"
    :title="
      reviewAction === 'approve' ? 'Approve Leave Request' : 'Reject Leave Request'
    "
    useElForm
    @save="handleReviewSave"
    @cancel="reviewFormVisible = false"
  />
</template>

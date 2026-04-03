<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import BaseButton from "~/components/base/BaseButton.vue";
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
  ElEmpty,
} from "element-plus";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import type {
  OvertimeRequestDTO,
  OvertimeRequestReviewDTO,
} from "~/api/hr_admin/overtimeRequest";
import { overtimeColumns } from "~/modules/tables/columns/hr_admin/overtimeColumns";
import {
  overtimeReviewFormSchema,
  getOvertimeReviewFormData,
} from "~/modules/forms/hr_admin/overtime/";
import { useAuthStore } from "~/stores/authStore";

const { $hrmsAdminService } = useNuxtApp();
const authStore = useAuthStore();

const actionLoading = ref<Record<string | number, boolean>>({});

const q = ref("");
const statusFilter = ref<string | undefined>("pending");

const isManager = computed(() => {
  const role = authStore.user?.role;
  return role === "manager" || role === "hr_admin" || role === "admin";
});

if (!isManager.value) {
  throw new Error("Only managers can access this page");
}

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
    const res = await $hrmsAdminService().overtimeRequest.getTeamRequests({
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

watch([q, statusFilter], () => {
  fetchPage(1);
});

// Review Overtime Request (Approve/Reject)
const reviewFormVisible = ref(false);
const reviewFormData = ref<any>(getOvertimeReviewFormData());
const reviewFormLoading = ref(false);
const reviewAction = ref<"approve" | "reject">("approve");
const currentOvertimeId = ref<string>("");

const handleOpenReviewForm = async (
  row: OvertimeRequestDTO,
  action: "approve" | "reject",
) => {
  if (row.status !== "pending") {
    ElMessageBox.alert(
      "Only pending overtime requests can be reviewed",
      "Cannot Review",
      { type: "warning" },
    );
    return;
  }

  currentOvertimeId.value = row.id;
  reviewAction.value = action;
  reviewFormData.value = {
    approved: action === "approve",
    comment: "",
  };
  reviewFormVisible.value = true;
};

const handleReviewSave = async (form: any) => {
  reviewFormLoading.value = true;
  try {
    const payload: OvertimeRequestReviewDTO = {
      approved: reviewAction.value === "approve",
      comment: form.comment || null,
    };
    await $hrmsAdminService().overtimeRequest.reviewRequest(
      currentOvertimeId.value,
      payload,
    );
    reviewFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    reviewFormLoading.value = false;
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
    :title="'Overtime Approvals'"
    :description="'Review and approve team overtime requests'"
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
    </template>
  </OverviewHeader>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="12">
      <el-select
        v-model="statusFilter"
        placeholder="Filter by status"
        clearable
        @change="fetchPage(1)"
      >
        <el-option label="Pending" value="pending" />
        <el-option label="Approved" value="approved" />
        <el-option label="Rejected" value="rejected" />
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
        <!-- Approve/Reject (pending only) -->
        <template v-if="row.status === 'pending'">
          <el-button
            type="success"
            size="small"
            link
            :loading="actionLoading[row.id]"
            @click="handleOpenReviewForm(row as OvertimeRequestDTO, 'approve')"
          >
            Approve
          </el-button>
          <el-button
            type="danger"
            size="small"
            link
            :loading="actionLoading[row.id]"
            @click="handleOpenReviewForm(row as OvertimeRequestDTO, 'reject')"
          >
            Reject
          </el-button>
        </template>

        <!-- View details -->
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

  <!-- Review Overtime Dialog -->
  <SmartFormDialog
    v-model:visible="reviewFormVisible"
    :model-value="reviewFormData"
    :fields="overtimeReviewFormSchema"
    :width="'40%'"
    :loading="reviewFormLoading"
    :disabled="reviewFormLoading"
    :title="
      reviewAction === 'approve'
        ? 'Approve Overtime Request'
        : 'Reject Overtime Request'
    "
    useElForm
    @save="handleReviewSave"
    @cancel="reviewFormVisible = false"
  />
</template>

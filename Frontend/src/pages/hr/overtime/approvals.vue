<script setup lang="ts">
import { computed, ref, watch } from "vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import { ElInput, ElMessage, ElMessageBox, ElTag } from "element-plus";
import type {
  OvertimeApproveDTO,
  OvertimeRejectDTO,
  OvertimeRequestDTO,
} from "~/api/hr_admin/overtime/dto";
import { overtimeColumns } from "~/modules/tables/columns/hr_admin/overtimeColumns";
import {
  getOvertimeReviewFormData,
  overtimeReviewFormSchema,
} from "~/modules/forms/hr_admin/overtime";
import { useAuthStore } from "~/stores/authStore";
import { useOvertimeStore } from "~/stores/overtimeStore";

const authStore = useAuthStore();
const overtimeStore = useOvertimeStore();

const q = ref("");
const statusFilter = ref<string | undefined>("pending");
const isFallbackPendingMode = ref(false);
const isLocalFallbackMode = ref(false);
const reviewFormVisible = ref(false);
const reviewFormData = ref<any>(getOvertimeReviewFormData());
const reviewFormLoading = ref(false);
const reviewAction = ref<"approve" | "reject">("approve");
const currentOvertimeRow = ref<OvertimeRequestDTO | null>(null);

const localFallbackRows = ref<OvertimeRequestDTO[]>([
  {
    id: "LOCAL-OT-001",
    employee_id: "EMP-LOCAL-01",
    request_date: "2026-04-06",
    start_time: "2026-04-06T18:00:00+07:00",
    end_time: "2026-04-06T20:00:00+07:00",
    schedule_end_time: "17:00:00",
    reason: "Fallback OT row while server is unavailable",
    day_type: "working_day",
    basic_salary: 0,
    submitted_at: "2026-04-06T10:00:00+07:00",
    status: "pending",
    manager_id: null,
    manager_comment: null,
    approved_hours: 0,
    calculated_payment: 0,
    lifecycle: {
      created_at: "2026-04-06T10:00:00+07:00",
      updated_at: "2026-04-06T10:00:00+07:00",
      deleted_at: null,
      deleted_by: null,
    },
  },
]);

const canApproveOvertime = computed(() => {
  const role = authStore.user?.role;
  return role === "manager" || role === "hr_admin";
});

if (!canApproveOvertime.value) {
  throw new Error("Only HR Admin and Manager can approve overtime requests");
}

const tableLoading = computed(
  () =>
    !isLocalFallbackMode.value &&
    (overtimeStore.isLoading("getRequests") ||
      overtimeStore.isLoading("getPendingRequests") ||
      overtimeStore.isLoading("approveRequest") ||
      overtimeStore.isLoading("rejectRequest")),
);

const sourceRows = computed(() =>
  isLocalFallbackMode.value
    ? localFallbackRows.value
    : isFallbackPendingMode.value
    ? overtimeStore.pendingApproval
    : overtimeStore.list,
);

const filteredRows = computed(() => {
  const keyword = q.value.trim().toLowerCase();
  return sourceRows.value.filter((row) => {
    if (statusFilter.value && row.status !== statusFilter.value) return false;
    if (!keyword) return true;
    return (
      String(row.id ?? "")
        .toLowerCase()
        .includes(keyword) ||
      String(row.employee_id ?? "")
        .toLowerCase()
        .includes(keyword) ||
      String(row.reason ?? "")
        .toLowerCase()
        .includes(keyword)
    );
  });
});

const tableRows = computed(() => filteredRows.value);

function getDefaultApprovedHours(row: OvertimeRequestDTO): number {
  if (typeof row.approved_hours === "number" && row.approved_hours > 0) {
    return row.approved_hours;
  }

  const start = new Date(row.start_time);
  const end = new Date(row.end_time);
  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) return 1;

  const diffHours = (end.getTime() - start.getTime()) / 3_600_000;
  return diffHours > 0 ? Number(diffHours.toFixed(2)) : 1;
}

function isPendingStatus(status: string | null | undefined): boolean {
  return String(status ?? "").toLowerCase() === "pending";
}

async function fetchRequests(page = 1) {
  overtimeStore.setFilters({ status: statusFilter.value ?? null });

  try {
    await overtimeStore.fetchList(page);
    isFallbackPendingMode.value = false;
    isLocalFallbackMode.value = false;
  } catch (error: any) {
    // Fallback for unstable list endpoint on manager/hr contexts.
    const canFallback = !statusFilter.value || statusFilter.value === "pending";
    if (!canFallback) {
      isFallbackPendingMode.value = false;
      isLocalFallbackMode.value = true;
      ElMessage.error(
        "Overtime list endpoint is unavailable. Using local fallback rows.",
      );
      return;
    }

    try {
      await overtimeStore.fetchPendingApproval(page);
      isFallbackPendingMode.value = true;
      isLocalFallbackMode.value = false;
      ElMessage.warning(
        "Primary OT list failed, showing pending-approval data",
      );
    } catch {
      isFallbackPendingMode.value = false;
      isLocalFallbackMode.value = true;
      ElMessage.error(
        "OT endpoints are unavailable. Using local fallback rows.",
      );
    }
  }
}

const handleOpenReviewForm = (
  row: OvertimeRequestDTO,
  action: "approve" | "reject",
) => {
  if (!isPendingStatus(row.status)) {
    ElMessageBox.alert(
      "Only pending overtime requests can be reviewed",
      "Cannot Review",
      { type: "warning" },
    );
    return;
  }

  currentOvertimeRow.value = row;
  reviewAction.value = action;
  reviewFormData.value = {
    approved: action === "approve",
    approved_hours: getDefaultApprovedHours(row),
    comment: "",
  };
  reviewFormVisible.value = true;
};

const handleViewDetails = async (row: OvertimeRequestDTO) => {
  try {
    const detail = isLocalFallbackMode.value
      ? row
      : await overtimeStore.fetchOne(row.id);
    await ElMessageBox.alert(
      `Employee: ${detail.employee_id}\nDate: ${detail.request_date}\nStart: ${
        detail.start_time
      }\nEnd: ${detail.end_time}\nStatus: ${detail.status}\nReason: ${
        detail.reason
      }\nComment: ${detail.manager_comment || "-"}`,
      `Overtime Detail (${detail.id})`,
      { type: "info" },
    );
  } catch {
    ElMessage.error("Failed to load overtime detail");
  }
};

const handleReviewSave = async (form: any) => {
  if (!currentOvertimeRow.value) return;

  reviewFormLoading.value = true;
  try {
    if (reviewAction.value === "approve") {
      const payload: OvertimeApproveDTO = {
        approved_hours:
          Number(form?.approved_hours) ||
          getDefaultApprovedHours(currentOvertimeRow.value),
        comment: form.comment || null,
      };
      if (isLocalFallbackMode.value) {
        const local = localFallbackRows.value.find(
          (item) => item.id === currentOvertimeRow.value?.id,
        );
        if (local) {
          local.status = "approved";
          local.approved_hours = payload.approved_hours;
          local.manager_comment = payload.comment || "Approved";
        }
      } else {
        await overtimeStore.approveRequest(
          currentOvertimeRow.value.id,
          payload,
        );
      }
      ElMessage.success("Overtime request approved");
    } else {
      const payload: OvertimeRejectDTO = {
        comment: String(form.comment || "Rejected by reviewer"),
      };
      if (isLocalFallbackMode.value) {
        const local = localFallbackRows.value.find(
          (item) => item.id === currentOvertimeRow.value?.id,
        );
        if (local) {
          local.status = "rejected";
          local.approved_hours = 0;
          local.manager_comment = payload.comment;
        }
      } else {
        await overtimeStore.rejectRequest(currentOvertimeRow.value.id, payload);
      }
      ElMessage.success("Overtime request rejected");
    }

    reviewFormVisible.value = false;
    currentOvertimeRow.value = null;
    await fetchRequests(overtimeStore.pagination.page || 1);
  } catch (error) {
    ElMessage.error("Failed to submit review action");
  } finally {
    reviewFormLoading.value = false;
  }
};

const getStatusTagType = (status: string) => {
  const typeMap: Record<string, "warning" | "success" | "danger" | "info"> = {
    pending: "warning",
    approved: "success",
    rejected: "danger",
    cancelled: "info",
  };
  return typeMap[status] || "info";
};

const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    pending: "status-pill status-pill--pending",
    approved: "status-pill status-pill--approved",
    rejected: "status-pill status-pill--rejected",
    cancelled: "status-pill status-pill--cancelled",
  };
  return classMap[status] || "status-pill";
};

watch(statusFilter, async () => {
  await fetchRequests(1);
});

await fetchRequests(1);
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
        :loading="tableLoading"
        class="!border-[color:var(--color-primary)] !text-[color:var(--color-primary)] hover:!bg-[var(--color-primary-light-7)]"
        @click="fetchRequests(overtimeStore.pagination.page || 1)"
      >
        Refresh
      </BaseButton>
    </template>
  </OverviewHeader>

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="8">
      <ElInput
        v-model="q"
        clearable
        placeholder="Search ID, employee, reason"
      />
    </el-col>
    <el-col :span="8">
      <el-select
        v-model="statusFilter"
        placeholder="Filter by status"
        clearable
        @change="fetchRequests(1)"
      >
        <el-option label="Pending" value="pending" />
        <el-option label="Approved" value="approved" />
        <el-option label="Rejected" value="rejected" />
      </el-select>
    </el-col>
  </el-row>

  <SmartTable
    :columns="overtimeColumns"
    :data="tableRows"
    :loading="tableLoading"
    :total="filteredRows.length"
    :page="overtimeStore.pagination.page"
    :page-size="overtimeStore.pagination.limit"
    @page="fetchRequests"
    @page-size="(size: number) => { overtimeStore.setPagination(1, size); fetchRequests(1); }"
  >
    <template #status="{ row }">
      <el-tag
        :type="getStatusTagType(row.status)"
        effect="plain"
        round
        size="small"
        :class="getStatusClass(row.status)"
      >
        {{ row.status.charAt(0).toUpperCase() + row.status.slice(1) }}
      </el-tag>
    </template>

    <template #operation="{ row }">
      <el-space class="review-actions" :size="6">
        <!-- Approve/Reject (pending only) -->
        <template v-if="canApproveOvertime && isPendingStatus(row.status)">
          <el-button
            type="success"
            size="small"
            plain
            class="review-btn review-btn--approve"
            @click.stop="
              handleOpenReviewForm(row as OvertimeRequestDTO, 'approve')
            "
          >
            Approve
          </el-button>
          <el-button
            type="danger"
            size="small"
            plain
            class="review-btn review-btn--reject"
            @click.stop="
              handleOpenReviewForm(row as OvertimeRequestDTO, 'reject')
            "
          >
            Reject
          </el-button>
        </template>

        <!-- View details -->
        <el-button
          type="info"
          size="small"
          plain
          class="review-btn review-btn--view"
          @click.stop="handleViewDetails(row as OvertimeRequestDTO)"
        >
          View
        </el-button>
      </el-space>
    </template>
  </SmartTable>

  <el-row v-if="filteredRows.length > 0" justify="end" class="m-4">
    <el-pagination
      :current-page="overtimeStore.pagination.page"
      :page-size="overtimeStore.pagination.limit"
      :total="filteredRows.length"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      background
      @current-change="fetchRequests"
      @size-change="(size: number) => { overtimeStore.setPagination(1, size); fetchRequests(1); }"
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

<style scoped>
.status-pill {
  font-weight: 600;
  letter-spacing: 0.01em;
}

.status-pill--pending {
  border-color: #e6a23c;
  color: #b88230;
  background: #fff8eb;
}

.status-pill--approved {
  border-color: #67c23a;
  color: #3b8f1d;
  background: #f1faec;
}

.status-pill--rejected {
  border-color: #f56c6c;
  color: #c74141;
  background: #fff2f2;
}

.status-pill--cancelled {
  border-color: #909399;
  color: #61656d;
  background: #f5f6f7;
}

.review-actions {
  display: inline-flex;
  align-items: center;
}

.review-btn {
  min-width: 72px;
  font-weight: 600;
}

.review-btn--approve {
  border-color: #67c23a;
}

.review-btn--reject {
  border-color: #f56c6c;
}

.review-btn--view {
  border-color: #909399;
}
</style>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import {
  ElButton,
  ElCard,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElMessage,
  ElMessageBox,
  ElTable,
  ElTableColumn,
  ElTag,
  ElPagination,
  ElLoading,
  ElEmpty,
  ElInputNumber,
} from "element-plus";
import type { FormInstance } from "element-plus";
import { Check, Close } from "@element-plus/icons-vue";
import { useOvertimeStore } from "~/stores/overtimeStore";
import type {
  OvertimeApproveDTO,
  OvertimeRejectDTO,
} from "~/api/hr_admin/overtime/dto";

definePageMeta({ layout: "default" });

const overtimeStore = useOvertimeStore();

// Dialog states
const detailDialogVisible = ref(false);
const approveDialogVisible = ref(false);
const rejectDialogVisible = ref(false);

// Forms
const approveFormRef = ref<FormInstance>();
const rejectFormRef = ref<FormInstance>();
const approveForm = ref<OvertimeApproveDTO>({
  approved_hours: 0,
  comment: "",
});

const rejectForm = ref<OvertimeRejectDTO>({
  comment: "",
});

let currentActionRequestId: string | null = null;

// Computed properties
const pendingRequests = computed(() => overtimeStore.pendingApproval);
const list = computed(() => overtimeStore.list);
const requestDetail = computed(() => overtimeStore.requestDetail);
const isLoadingPending = computed(() =>
  overtimeStore.isLoading("getPendingRequests"),
);
const isLoadingList = computed(() => overtimeStore.isLoading("getRequests"));
const isLoadingApprove = computed(() =>
  overtimeStore.isLoading("approveRequest"),
);
const isLoadingReject = computed(() =>
  overtimeStore.isLoading("rejectRequest"),
);
const isLoadingDetail = computed(() => overtimeStore.isLoading("getRequest"));

const paginationProps = computed(() => ({
  currentPage: overtimeStore.pagination.page,
  pageSize: overtimeStore.pagination.limit,
  total: overtimeStore.pagination.total,
}));

// Methods
async function viewDetail(id: string) {
  try {
    await overtimeStore.fetchOne(id);
    detailDialogVisible.value = true;
  } catch (error) {
    ElMessage.error("Failed to load request detail");
  }
}

function closeDetailDialog() {
  detailDialogVisible.value = false;
  overtimeStore.clearDetail();
}

function openApproveDialog(id: string) {
  currentActionRequestId = id;
  approveForm.value = {
    approved_hours: requestDetail.value?.schedule_end_time
      ? parseFloat(requestDetail.value.schedule_end_time)
      : 8,
    comment: "",
  };
  approveDialogVisible.value = true;
}

function closeApproveDialog() {
  approveDialogVisible.value = false;
  currentActionRequestId = null;
  approveForm.value = { approved_hours: 0, comment: "" };
}

function openRejectDialog(id: string) {
  currentActionRequestId = id;
  rejectForm.value = { comment: "" };
  rejectDialogVisible.value = true;
}

function closeRejectDialog() {
  rejectDialogVisible.value = false;
  currentActionRequestId = null;
  rejectForm.value = { comment: "" };
}

async function submitApprove() {
  if (!currentActionRequestId) return;

  try {
    await approveFormRef.value?.validate();

    await ElMessageBox.confirm(
      `Approve this overtime request with ${approveForm.value.approved_hours} hours?`,
      "Confirm Approve",
      {
        confirmButtonText: "Approve",
        cancelButtonText: "Cancel",
        type: "success",
      },
    );

    await overtimeStore.approveRequest(
      currentActionRequestId,
      approveForm.value,
    );
    ElMessage.success("Request approved successfully");
    closeApproveDialog();
    await Promise.all([
      overtimeStore.fetchPendingApproval(),
      overtimeStore.fetchList(),
    ]);
  } catch (error: any) {
    if (error !== "cancel") {
      ElMessage.error(
        overtimeStore.getError("approveRequest") || "Failed to approve",
      );
    }
  }
}

async function submitReject() {
  if (!currentActionRequestId) return;

  try {
    await rejectFormRef.value?.validate();

    await ElMessageBox.confirm(
      "Are you sure you want to reject this overtime request?",
      "Confirm Reject",
      {
        confirmButtonText: "Reject",
        cancelButtonText: "Cancel",
        type: "warning",
      },
    );

    await overtimeStore.rejectRequest(currentActionRequestId, rejectForm.value);
    ElMessage.success("Request rejected successfully");
    closeRejectDialog();
    await Promise.all([
      overtimeStore.fetchPendingApproval(),
      overtimeStore.fetchList(),
    ]);
  } catch (error: any) {
    if (error !== "cancel") {
      ElMessage.error(
        overtimeStore.getError("rejectRequest") || "Failed to reject",
      );
    }
  }
}

function formatTime(time: string) {
  if (!time) return "—";
  return time;
}

function formatDate(date: string) {
  if (!date) return "—";
  return new Date(date).toLocaleDateString();
}

function statusTagType(
  status: string,
): "success" | "info" | "warning" | "danger" {
  switch (status?.toLowerCase()) {
    case "approved":
      return "success";
    case "rejected":
      return "danger";
    case "cancelled":
      return "info";
    case "pending":
      return "warning";
    default:
      return "info";
  }
}

// Page initialization
onMounted(async () => {
  try {
    await Promise.all([
      overtimeStore.fetchPendingApproval(),
      overtimeStore.fetchList(),
    ]);
  } catch (error) {
    ElMessage.error("Failed to load overtime information");
  }
});

const handlePageChange = async (page: number) => {
  await overtimeStore.fetchPendingApproval(page);
};
</script>

<template>
  <div class="manager-overtime-page">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1>Overtime Approval</h1>
        <p class="subtitle">Review and approve employee overtime requests</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs-container">
      <ElButton type="primary" class="tab-active">Pending Approval</ElButton>
      <ElButton type="info">All Requests</ElButton>
    </div>

    <!-- Pending Requests Table -->
    <ElCard class="requests-card" v-show="true">
      <template #header>
        <div class="card-title">
          Pending Approval ({{ pendingRequests.length }})
        </div>
      </template>

      <div v-if="isLoadingPending" class="loading">
        <ElLoading fullscreen lock />
      </div>

      <ElEmpty v-else-if="!pendingRequests || pendingRequests.length === 0" />

      <ElTable v-else :data="pendingRequests" stripe>
        <ElTableColumn prop="employee_id" label="Employee" width="120" />
        <ElTableColumn prop="request_date" label="Date" width="120">
          <template #default="{ row }">
            {{ formatDate(row.request_date) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="start_time" label="Start Time" width="100">
          <template #default="{ row }">
            {{ formatTime(row.start_time) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="end_time" label="End Time" width="100">
          <template #default="{ row }">
            {{ formatTime(row.end_time) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="reason" label="Reason" min-width="200" />
        <ElTableColumn prop="status" label="Status" width="100">
          <template #default="{ row }">
            <ElTag :type="statusTagType(row.status)">
              {{ row.status }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn label="Actions" width="200" align="center">
          <template #default="{ row }">
            <ElButton
              link
              type="primary"
              size="small"
              @click="viewDetail(row.id)"
            >
              View
            </ElButton>
            <ElButton
              link
              type="success"
              size="small"
              :icon="Check"
              @click="openApproveDialog(row.id)"
            >
              Approve
            </ElButton>
            <ElButton
              link
              type="danger"
              size="small"
              :icon="Close"
              @click="openRejectDialog(row.id)"
            >
              Reject
            </ElButton>
          </template>
        </ElTableColumn>
      </ElTable>

      <div
        v-if="pendingRequests && pendingRequests.length > 0"
        class="pagination"
      >
        <ElPagination
          :current-page="paginationProps.currentPage"
          :page-size="paginationProps.pageSize"
          :total="paginationProps.total"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </ElCard>

    <!-- Detail Dialog -->
    <ElDialog
      v-model="detailDialogVisible"
      title="Request Details"
      width="700px"
      @close="closeDetailDialog"
    >
      <div v-if="requestDetail" class="detail-content">
        <div class="detail-row">
          <span class="label">Employee ID:</span>
          <span class="value">{{ requestDetail.employee_id }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Date:</span>
          <span class="value">{{
            formatDate(requestDetail.request_date)
          }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Time:</span>
          <span class="value">
            {{ formatTime(requestDetail.start_time) }} -
            {{ formatTime(requestDetail.end_time) }}
          </span>
        </div>
        <div class="detail-row">
          <span class="label">Status:</span>
          <ElTag :type="statusTagType(requestDetail.status)">
            {{ requestDetail.status }}
          </ElTag>
        </div>
        <div class="detail-row">
          <span class="label">Reason:</span>
          <span class="value">{{ requestDetail.reason }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Day Type:</span>
          <span class="value">{{ requestDetail.day_type }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Submitted:</span>
          <span class="value">{{ requestDetail.submitted_at }}</span>
        </div>
      </div>
    </ElDialog>

    <!-- Approve Dialog -->
    <ElDialog
      v-model="approveDialogVisible"
      title="Approve Overtime Request"
      width="500px"
      @close="closeApproveDialog"
    >
      <ElForm ref="approveFormRef" :model="approveForm" label-width="120px">
        <ElFormItem
          label="Approved Hours"
          prop="approved_hours"
          :rules="[
            { required: true, message: 'Please enter approved hours' },
            { type: 'number', min: 0, message: 'Hours must be positive' },
          ]"
        >
          <ElInputNumber
            v-model="approveForm.approved_hours"
            :min="0"
            :max="24"
            style="width: 100%"
          />
        </ElFormItem>
        <ElFormItem label="Comment" prop="comment">
          <ElInput
            v-model="approveForm.comment"
            type="textarea"
            placeholder="Optional comment"
            rows="3"
          />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="closeApproveDialog">Cancel</ElButton>
        <ElButton
          type="success"
          :loading="isLoadingApprove"
          @click="submitApprove"
        >
          Approve
        </ElButton>
      </template>
    </ElDialog>

    <!-- Reject Dialog -->
    <ElDialog
      v-model="rejectDialogVisible"
      title="Reject Overtime Request"
      width="500px"
      @close="closeRejectDialog"
    >
      <ElForm ref="rejectFormRef" :model="rejectForm" label-width="80px">
        <ElFormItem
          label="Comment"
          prop="comment"
          :rules="[{ required: true, message: 'Please provide a reason' }]"
        >
          <ElInput
            v-model="rejectForm.comment"
            type="textarea"
            placeholder="Explain why you're rejecting this request"
            rows="4"
          />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="closeRejectDialog">Cancel</ElButton>
        <ElButton
          type="danger"
          :loading="isLoadingReject"
          @click="submitReject"
        >
          Reject
        </ElButton>
      </template>
    </ElDialog>
  </div>
</template>

<style scoped>
.manager-overtime-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.subtitle {
  margin: 4px 0 0 0;
  color: #606266;
  font-size: 14px;
}

.tabs-container {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.tab-active {
  border-color: #409eff !important;
  background-color: #f0f9ff;
}

.requests-card {
  margin-bottom: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
}

.pagination {
  margin-top: 16px;
  text-align: right;
}

.loading {
  position: relative;
  min-height: 200px;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.detail-row:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: #606266;
}

.value {
  color: #303133;
}
</style>

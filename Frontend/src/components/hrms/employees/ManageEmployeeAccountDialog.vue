<script setup lang="ts">
import {
  ElDialog,
  ElDescriptions,
  ElDescriptionsItem,
  ElEmpty,
  ElButton,
  ElTag,
  ElSkeleton,
} from "element-plus";

import type {
  HrEmployeeDTO,
  HrEmployeeAccountDTO,
} from "~/api/hr_admin/employees/dto";

const props = defineProps<{
  visible: boolean;
  employee: HrEmployeeDTO | null;
  account: HrEmployeeAccountDTO | null;
  loading?: boolean;
  actionLoading?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:visible", value: boolean): void;
  (e: "open-create-account"): void;
  (e: "soft-delete-account"): void;
  (e: "restore-account"): void;
  (e: "close"): void;
}>();

function closeDialog() {
  emit("update:visible", false);
  emit("close");
}

function accountTagType(status?: string | null) {
  if (status === "active") return "success";
  if (status === "inactive") return "warning";
  return "danger";
}
</script>

<template>
  <ElDialog
    :model-value="visible"
    title="Manage Login Account"
    width="640px"
    @close="closeDialog"
  >
    <div v-if="loading">
      <ElSkeleton :rows="6" animated />
    </div>

    <div v-else>
      <ElDescriptions border :column="1">
        <ElDescriptionsItem label="Employee">
          {{ employee?.full_name || "-" }}
        </ElDescriptionsItem>
        <ElDescriptionsItem label="Employee Code">
          {{ employee?.employee_code || "-" }}
        </ElDescriptionsItem>
      </ElDescriptions>

      <div v-if="account" class="section-gap">
        <ElDescriptions border :column="1">
          <ElDescriptionsItem label="Status">
            <ElTag :type="accountTagType(account.status)">
              {{ account.status || "linked" }}
            </ElTag>
          </ElDescriptionsItem>

          <ElDescriptionsItem label="Email">
            {{ account.email || "-" }}
          </ElDescriptionsItem>

          <ElDescriptionsItem label="Username">
            {{ account.username || "-" }}
          </ElDescriptionsItem>

          <ElDescriptionsItem label="Role">
            {{ account.role || "-" }}
          </ElDescriptionsItem>
        </ElDescriptions>

        <div class="dialog-actions">
          <ElButton
            v-if="account.status === 'active'"
            type="danger"
            :loading="actionLoading"
            @click="$emit('soft-delete-account')"
          >
            Soft Delete Account
          </ElButton>

          <ElButton
            v-else
            type="success"
            :loading="actionLoading"
            @click="$emit('restore-account')"
          >
            Restore Account
          </ElButton>
        </div>
      </div>

      <div v-else class="section-gap">
        <ElEmpty description="No linked account yet" />

        <div class="dialog-actions">
          <ElButton
            type="primary"
            :loading="actionLoading"
            @click="$emit('open-create-account')"
          >
            Create Account
          </ElButton>
        </div>
      </div>
    </div>
  </ElDialog>
</template>

<style scoped>
.section-gap {
  margin-top: 16px;
}

.dialog-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>

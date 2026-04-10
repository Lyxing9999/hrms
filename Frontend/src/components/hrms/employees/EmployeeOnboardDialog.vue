<script setup lang="ts">
import { computed, reactive } from "vue";
import { ElDialog, ElMessage } from "element-plus";
import { Role } from "~/api/types/enums/role.enum";
import type { HrCreateEmployeeDTO } from "~/api/hr_admin/employees/dto";
import EmployeeFormFields from "~/components/hrms/employees/EmployeeFormFields.vue";
import BaseButton from "~/components/base/BaseButton.vue";

type HrOnboardRole = Role.EMPLOYEE | Role.MANAGER | Role.PAYROLL_MANAGER;

type EmployeeFormModel = {
  employee_code: string;
  full_name: string;
  department: string;
  position: string;
  employment_type: "permanent" | "contract";
  basic_salary: number | null;
  status: "active" | "inactive";
  email?: string;
  username?: string;
  password?: string;
  role?: HrOnboardRole;
};

const props = defineProps<{
  visible: boolean;
  loading?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:visible", value: boolean): void;
  (
    e: "submitted",
    payload: {
      employee: HrCreateEmployeeDTO;
      account: {
        email: string;
        password: string;
        username?: string;
        role?: HrOnboardRole;
      };
    },
  ): void;
}>();

const form = reactive<EmployeeFormModel>({
  employee_code: "",
  full_name: "",
  department: "",
  position: "",
  employment_type: "permanent",
  basic_salary: null,
  status: "active",
  email: "",
  username: "",
  password: "",
  role: undefined,
});

const canSubmit = computed(() => {
  return (
    form.employee_code.trim().length > 0 &&
    form.full_name.trim().length > 0 &&
    Number(form.basic_salary || 0) >= 0 &&
    (form.email || "").trim().length > 0 &&
    (form.password || "").length >= 6
  );
});

function resetForm() {
  form.employee_code = "";
  form.full_name = "";
  form.department = "";
  form.position = "";
  form.employment_type = "permanent";
  form.basic_salary = null;
  form.status = "active";
  form.email = "";
  form.username = "";
  form.password = "";
  form.role = undefined;
}

function closeDialog() {
  emit("update:visible", false);
}

function handleClosed() {
  resetForm();
}

function submit() {
  if (!canSubmit.value) {
    ElMessage.error("Please complete required onboarding fields");
    return;
  }

  const employee: HrCreateEmployeeDTO = {
    employee_code: form.employee_code.trim(),
    full_name: form.full_name.trim(),
    department: form.department?.trim() || undefined,
    position: form.position?.trim() || undefined,
    employment_type: form.employment_type,
    basic_salary: Number(form.basic_salary || 0),
    status: form.status,
  };

  const account = {
    email: (form.email || "").trim(),
    password: form.password || "",
    username: form.username?.trim() || undefined,
    role: form.role,
  };

  emit("submitted", { employee, account });
}
</script>

<template>
  <ElDialog
    :model-value="visible"
    title="Onboard Employee"
    width="900px"
    destroy-on-close
    @update:model-value="emit('update:visible', $event)"
    @closed="handleClosed"
  >
    <EmployeeFormFields v-model="form" mode="onboard" />

    <template #footer>
      <div class="dialog-actions">
        <BaseButton plain :disabled="loading" @click="closeDialog">
          Cancel
        </BaseButton>
        <BaseButton type="primary" :loading="loading" @click="submit">
          Create Employee + Account
        </BaseButton>
      </div>
    </template>
  </ElDialog>
</template>

<style scoped>
.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>

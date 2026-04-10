<script setup lang="ts">
import { computed } from "vue";
import { Role } from "~/api/types/enums/role.enum";
import type { HrEmploymentType } from "~/api/hr_admin/employees/dto";

type Mode = "employee" | "onboard";

interface EmployeeFormModel {
  employee_code: string;
  full_name: string;
  department: string;
  position: string;
  employment_type: HrEmploymentType;
  basic_salary: number | null;
  status: "active" | "inactive";
  email?: string;
  username?: string;
  password?: string;
  role?: Role.EMPLOYEE | Role.MANAGER | Role.PAYROLL_MANAGER;
}

const props = defineProps<{
  modelValue: EmployeeFormModel;
  mode: Mode;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: EmployeeFormModel): void;
}>();

const form = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

function update<K extends keyof EmployeeFormModel>(
  key: K,
  value: EmployeeFormModel[K],
) {
  form.value = {
    ...form.value,
    [key]: value,
  };
}
</script>

<template>
  <el-form label-position="top" class="dialog-form">
    <div class="form-grid">
      <el-form-item label="Employee Code" required>
        <el-input
          :model-value="form.employee_code"
          placeholder="EMP-001"
          @update:model-value="update('employee_code', $event)"
        />
      </el-form-item>

      <el-form-item label="Full Name" required>
        <el-input
          :model-value="form.full_name"
          placeholder="Employee full name"
          @update:model-value="update('full_name', $event)"
        />
      </el-form-item>

      <el-form-item label="Department">
        <el-input
          :model-value="form.department"
          placeholder="Department"
          @update:model-value="update('department', $event)"
        />
      </el-form-item>

      <el-form-item label="Position">
        <el-input
          :model-value="form.position"
          placeholder="Position"
          @update:model-value="update('position', $event)"
        />
      </el-form-item>

      <el-form-item label="Employment Type">
        <el-select
          :model-value="form.employment_type"
          @update:model-value="update('employment_type', $event)"
        >
          <el-option label="Permanent" value="permanent" />
          <el-option label="Contract" value="contract" />
        </el-select>
      </el-form-item>

      <el-form-item label="Status">
        <el-select
          :model-value="form.status"
          @update:model-value="update('status', $event)"
        >
          <el-option label="Active" value="active" />
          <el-option label="Inactive" value="inactive" />
        </el-select>
      </el-form-item>

      <el-form-item label="Basic Salary" required>
        <el-input-number
          :model-value="form.basic_salary"
          :min="0"
          :step="10"
          :precision="2"
          controls-position="right"
          style="width: 100%"
          @update:model-value="update('basic_salary', $event)"
        />
      </el-form-item>

      <template v-if="mode === 'onboard'">
        <el-form-item label="Email" required>
          <el-input
            :model-value="form.email"
            placeholder="employee@company.com"
            @update:model-value="update('email', $event)"
          />
        </el-form-item>

        <el-form-item label="Username">
          <el-input
            :model-value="form.username"
            placeholder="username (optional)"
            @update:model-value="update('username', $event)"
          />
        </el-form-item>

        <el-form-item label="Password" required>
          <el-input
            :model-value="form.password"
            type="password"
            show-password
            @update:model-value="update('password', $event)"
          />
        </el-form-item>

        <el-form-item label="Role">
          <el-select
            :model-value="form.role"
            @update:model-value="update('role', $event)"
          >
            <el-option label="Employee" :value="Role.EMPLOYEE" />
            <el-option label="Manager" :value="Role.MANAGER" />
            <el-option label="Payroll Manager" :value="Role.PAYROLL_MANAGER" />
          </el-select>
        </el-form-item>
      </template>
    </div>
  </el-form>
</template>

<style scoped>
.dialog-form {
  margin-top: 6px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 14px;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>

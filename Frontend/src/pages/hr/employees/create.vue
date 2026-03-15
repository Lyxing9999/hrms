<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useNuxtApp } from "#app";

import type {
  HrCreateEmployeeDTO,
  HrUpdateEmployeeDTO,
  HrEmployeeDTO,
} from "~/api/hr_admin/employees/dto";

import OverviewHeader from "~/components/overview/OverviewHeader.vue";

import {
  ElCard,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElButton,
  ElInputNumber,
} from "element-plus";

const route = useRoute();
const router = useRouter();
const { $hrEmployeeService } = useNuxtApp();

const employeeId = route.params.id as string | undefined;
const isEdit = computed(() => !!employeeId);

const loading = ref(false);

const form = reactive<HrCreateEmployeeDTO>({
  employee_code: "",
  full_name: "",
  department: "",
  position: "",
  employment_type: "contract",
  basic_salary: 0,
  status: "active",
});

async function loadEmployee() {
  if (!isEdit.value) return;

  loading.value = true;

  try {
    const employee: HrEmployeeDTO = await $hrEmployeeService.getEmployee(
      employeeId!,
    );

    form.employee_code = employee.employee_code;
    form.full_name = employee.full_name;
    form.department = employee.department ?? "";
    form.position = employee.position ?? "";
    form.employment_type = employee.employment_type;
    form.basic_salary = employee.basic_salary;
    form.status = employee.status;
  } finally {
    loading.value = false;
  }
}

async function submit() {
  loading.value = true;

  try {
    if (isEdit.value) {
      const payload: HrUpdateEmployeeDTO = { ...form };

      await $hrEmployeeService.updateEmployee(employeeId!, payload);
    } else {
      await $hrEmployeeService.createEmployee(form);
    }

    router.push("/hr/employees");
  } catch (error) {
    console.error("Failed to save employee", error);
  } finally {
    loading.value = false;
  }
}

onMounted(loadEmployee);
</script>

<template>
  <div class="employee-form-page">
    <OverviewHeader
      :title="isEdit ? 'Edit Employee' : 'Create Employee'"
      description="Manage employee information"
      backPath="/hr/employees"
    />

    <ElCard class="mt-4" v-loading="loading">
      <ElForm label-width="160px">
        <ElFormItem label="Employee Code">
          <ElInput v-model="form.employee_code" />
        </ElFormItem>

        <ElFormItem label="Full Name">
          <ElInput v-model="form.full_name" />
        </ElFormItem>

        <ElFormItem label="Department">
          <ElInput v-model="form.department" />
        </ElFormItem>

        <ElFormItem label="Position">
          <ElInput v-model="form.position" />
        </ElFormItem>

        <ElFormItem label="Employment Type">
          <ElSelect v-model="form.employment_type">
            <ElOption label="Permanent" value="permanent" />
            <ElOption label="Contract" value="contract" />
          </ElSelect>
        </ElFormItem>

        <ElFormItem label="Basic Salary">
          <ElInputNumber
            v-model="form.basic_salary"
            :min="0"
            style="width: 200px"
          />
        </ElFormItem>

        <ElFormItem label="Status">
          <ElSelect v-model="form.status">
            <ElOption label="Active" value="active" />
            <ElOption label="Inactive" value="inactive" />
          </ElSelect>
        </ElFormItem>

        <ElFormItem>
          <ElButton type="primary" :loading="loading" @click="submit">
            {{ isEdit ? "Update Employee" : "Create Employee" }}
          </ElButton>

          <ElButton @click="router.back()">Cancel</ElButton>
        </ElFormItem>
      </ElForm>
    </ElCard>
  </div>
</template>

<style scoped>
.employee-form-page {
  padding: 20px;
}
</style>

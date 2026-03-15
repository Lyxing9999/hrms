<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useNuxtApp } from "nuxt/app";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import { ElCard, ElDescriptions, ElDescriptionsItem, ElAvatar, ElButton, ElTag } from "element-plus";

const route = useRoute();
const { $hrEmployeeService } = useNuxtApp();

const employeeId = route.params.id as string;
const employee = ref<any>(null);
const loading = ref(true);

onMounted(async () => {
  try {
    employee.value = await $hrEmployeeService.getEmployee(employeeId);
  } catch (error) {
    console.error("Failed to load employee:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="employee-detail">
    <OverviewHeader
      :title="employee?.full_name || 'Employee Detail'"
      :description="`Employee ID: ${employee?.employee_code || employeeId}`"
      :backPath="'/hr/employees'"
    >
      <template #actions>
        <ElButton type="primary">Edit Employee</ElButton>
      </template>
    </OverviewHeader>

    <ElCard v-loading="loading" class="mt-4">
      <template #header>
        <div class="flex items-center gap-4">
          <ElAvatar :size="80" :src="employee?.photo_url">
            {{ employee?.full_name?.charAt(0) }}
          </ElAvatar>
          <div>
            <h2 class="text-2xl font-bold">{{ employee?.full_name }}</h2>
            <p class="text-gray-500">{{ employee?.position || "N/A" }}</p>
          </div>
        </div>
      </template>

      <ElDescriptions :column="2" border v-if="employee">
        <ElDescriptionsItem label="Employee Code">
          {{ employee.employee_code }}
        </ElDescriptionsItem>
        <ElDescriptionsItem label="Employment Type">
          <ElTag :type="employee.employment_type === 'permanent' ? 'success' : 'warning'">
            {{ employee.employment_type }}
          </ElTag>
        </ElDescriptionsItem>
        <ElDescriptionsItem label="Department">
          {{ employee.department || "N/A" }}
        </ElDescriptionsItem>
        <ElDescriptionsItem label="Position">
          {{ employee.position || "N/A" }}
        </ElDescriptionsItem>
        <ElDescriptionsItem label="Status">
          <ElTag :type="employee.status === 'active' ? 'success' : 'danger'">
            {{ employee.status }}
          </ElTag>
        </ElDescriptionsItem>
        <ElDescriptionsItem label="User Account">
          {{ employee.user_id ? "Linked" : "Not Linked" }}
        </ElDescriptionsItem>
      </ElDescriptions>
    </ElCard>
  </div>
</template>

<style scoped>
.employee-detail {
  padding: 20px;
}
</style>

<script setup lang="ts">
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import { ElCard, ElEmpty } from "element-plus";
</script>

<template>
  <div class="reports-page">
    <OverviewHeader
      :title="'Reports & Analytics'"
      :description="'Generate and view HRMS reports'"
      :backPath="'/hr'"
    />

    <ElCard class="mt-4">
      <ElEmpty description="Reports & Analytics - Coming Soon">
        <template #image>
          <el-icon :size="100" color="#909399">
            <DataAnalysis />
          </el-icon>
        </template>
        <p class="text-gray-600 mt-4">
          Available reports:
        </p>
        <ul class="text-left mt-2 text-gray-600">
          <li>• Daily/Monthly Attendance Reports</li>
          <li>• Overtime Summary Reports</li>
          <li>• Payroll Reports</li>
          <li>• Deduction Reports</li>
          <li>• Team Performance Reports</li>
          <li>• Export to CSV/PDF</li>
        </ul>
      </ElEmpty>
    </ElCard>
  </div>
</template>

<style scoped>
.reports-page {
  padding: 20px;
}
</style>

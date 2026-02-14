<script setup lang="ts">
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import { ElCard, ElEmpty } from "element-plus";
</script>

<template>
  <div class="payroll-page">
    <OverviewHeader
      :title="'Payroll System'"
      :description="'Automated payroll calculation and payslip generation'"
      :backPath="'/hr'"
    />

    <ElCard class="mt-4">
      <ElEmpty description="Payroll System - Coming Soon">
        <template #image>
          <el-icon :size="100" color="#909399">
            <Money />
          </el-icon>
        </template>
        <p class="text-gray-600 mt-4">
          Features include:
        </p>
        <ul class="text-left mt-2 text-gray-600">
          <li>• Automated salary calculation</li>
          <li>• OT payment integration</li>
          <li>• Late deduction processing</li>
          <li>• Public holiday handling</li>
          <li>• Payslip generation</li>
          <li>• Payroll reports</li>
        </ul>
      </ElEmpty>
    </ElCard>
  </div>
</template>

<style scoped>
.payroll-page {
  padding: 20px;
}
</style>

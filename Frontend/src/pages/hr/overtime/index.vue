<script setup lang="ts">
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import { ElCard, ElEmpty } from "element-plus";
</script>

<template>
  <div class="overtime-page">
    <OverviewHeader
      :title="'Overtime Management'"
      :description="'Request, approve, and track overtime hours'"
      :backPath="'/hr'"
    />

    <ElCard class="mt-4">
      <ElEmpty description="Overtime Management - Coming Soon">
        <template #image>
          <el-icon :size="100" color="#909399">
            <Timer />
          </el-icon>
        </template>
        <p class="text-gray-600 mt-4">
          Features include:
        </p>
        <ul class="text-left mt-2 text-gray-600">
          <li>• OT request submission (3 hours before)</li>
          <li>• Manager approval workflow</li>
          <li>• Automatic rate calculation (150% / 200%)</li>
          <li>• Weekend and holiday OT</li>
          <li>• OT history and reports</li>
        </ul>
      </ElEmpty>
    </ElCard>
  </div>
</template>

<style scoped>
.overtime-page {
  padding: 20px;
}
</style>

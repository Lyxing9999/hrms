<script setup lang="ts">
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
</script>

<template>
  <OverviewHeader
    :title="'Payroll Manager Dashboard'"
    :description="'Manage payroll processing and reports'"
  />

  <el-card class="mt-4">
    <div class="text-center py-12">
      <el-icon :size="64" color="#909399">
        <Money />
      </el-icon>
      <h3 class="mt-4 text-xl font-semibold">Payroll Manager Dashboard</h3>
      <p class="mt-2 text-gray-500">This feature is coming soon</p>
    </div>
  </el-card>
</template>

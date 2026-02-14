<script setup lang="ts">
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
</script>

<template>
  <OverviewHeader
    :title="'Overtime History'"
    :description="'View overtime records and history'"
    :backPath="'/hr/overtime'"
  />

  <el-card class="mt-4">
    <div class="text-center py-12">
      <el-icon :size="64" color="#909399">
        <Calendar />
      </el-icon>
      <h3 class="mt-4 text-xl font-semibold">Overtime History</h3>
      <p class="mt-2 text-gray-500">This feature is coming soon</p>
    </div>
  </el-card>
</template>

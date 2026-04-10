<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import { ElCard, ElRow, ElCol } from "element-plus";
import { Clock, Location, Calendar, Coin } from "@element-plus/icons-vue";
import { ROUTES } from "~/constants/routes";

const router = useRouter();

const configModules = ref([
  {
    title: "Working Schedules",
    description: "Configure working hours and days",
    icon: Clock,
    route: ROUTES.HR_ADMIN.WORKING_SCHEDULES,
    color: "#409EFF",
  },
  {
    title: "Work Locations",
    description: "Manage approved work locations",
    icon: Location,
    route: ROUTES.HR_ADMIN.WORK_LOCATIONS,
    color: "#67C23A",
  },
  {
    title: "Public Holidays",
    description: "Khmer calendar and holidays",
    icon: Calendar,
    route: ROUTES.HR_ADMIN.PUBLIC_HOLIDAYS,
    color: "#E6A23C",
  },
  {
    title: "Deduction Rules",
    description: "Late and absence deduction policies",
    icon: Coin,
    route: ROUTES.HR_ADMIN.DEDUCTION_RULES,
    color: "#F56C6C",
  },
]);
</script>

<template>
  <div class="config-page">
    <OverviewHeader
      :title="'System Configuration'"
      :description="'Configure HRMS system settings'"
      :backPath="'/hr'"
    />

    <el-row :gutter="24" class="mt-6">
      <el-col
        v-for="module in configModules"
        :key="module.route"
        :xs="24"
        :sm="12"
        :md="6"
        class="mb-4"
      >
        <el-card
          shadow="hover"
          class="config-card cursor-pointer"
          @click="router.push(module.route)"
        >
          <div class="flex flex-col items-center text-center">
            <div
              class="icon-wrapper mb-4"
              :style="{ backgroundColor: module.color }"
            >
              <el-icon :size="32" color="#fff">
                <component :is="module.icon" />
              </el-icon>
            </div>
            <h3 class="text-lg font-semibold mb-2">{{ module.title }}</h3>
            <p class="text-sm text-gray-500">{{ module.description }}</p>
            <el-tag type="success" size="small" class="mt-3">Ready</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.config-page {
  padding: 20px;
}

.config-card {
  transition: all 0.3s ease;
}

.config-card:hover {
  transform: translateY(-4px);
}

.icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>

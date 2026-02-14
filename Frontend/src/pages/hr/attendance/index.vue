<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import { ElCard, ElRow, ElCol } from "element-plus";

const router = useRouter();

const modules = ref([
  {
    title: "Check In / Check Out",
    description: "Record your attendance with GPS location verification",
    route: "/hr/attendance/check-in",
    icon: "Clock",
    color: "#409EFF",
    status: "ready",
  },
  {
    title: "Attendance History",
    description: "View your attendance records and check-in history",
    route: "/hr/attendance/history",
    icon: "Calendar",
    color: "#67C23A",
    status: "ready",
  },
  {
    title: "Team Attendance",
    description: "Monitor team attendance and check-in status",
    route: "/hr/attendance/team",
    icon: "User",
    color: "#E6A23C",
    status: "ready",
  },
  {
    title: "Attendance Reports",
    description: "Generate and view attendance reports",
    route: "/hr/attendance/reports",
    icon: "Document",
    color: "#F56C6C",
    status: "coming-soon",
  },
]);
</script>

<template>
  <div class="attendance-page">
    <OverviewHeader
      :title="'Attendance System'"
      :description="'Track employee check-in/check-out and attendance records'"
      :backPath="'/hr'"
    />

    <el-row :gutter="16" class="mt-4">
      <el-col
        v-for="module in modules"
        :key="module.route"
        :xs="24"
        :sm="12"
        :md="6"
        class="mb-4"
      >
        <el-card
          shadow="hover"
          class="module-card"
          :class="{ 'coming-soon': module.status === 'coming-soon' }"
          @click="module.status === 'ready' ? router.push(module.route) : null"
        >
          <div class="card-icon" :style="{ backgroundColor: module.color }">
            <el-icon :size="32" color="#fff">
              <component :is="module.icon" />
            </el-icon>
          </div>
          <h3 class="card-title">{{ module.title }}</h3>
          <p class="card-description">{{ module.description }}</p>
          <el-tag
            v-if="module.status === 'coming-soon'"
            type="warning"
            size="small"
            class="mt-2"
          >
            Coming Soon
          </el-tag>
          <el-tag
            v-else
            type="success"
            size="small"
            class="mt-2"
          >
            Ready
          </el-tag>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.attendance-page {
  padding: 20px;
}

.module-card {
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  padding: 24px;
  min-height: 220px;
}

.module-card:hover {
  transform: translateY(-4px);
}

.module-card.coming-soon {
  opacity: 0.6;
  cursor: not-allowed;
}

.module-card.coming-soon:hover {
  transform: none;
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.card-description {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}
</style>

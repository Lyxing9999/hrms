<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import { ElCard, ElRow, ElCol } from "element-plus";
import { useAuthStore } from "~/stores/authStore";

const router = useRouter();
const authStore = useAuthStore();

const isManager = computed(() => {
  const role = authStore.user?.role;
  return role === "manager" || role === "hr_admin" || role === "admin";
});

const modules = ref([
  {
    title: "New Request",
    description: "Submit a new overtime request",
    route: "/hr/overtime/request",
    icon: "EditPen",
    color: "#409EFF",
    status: "ready",
    roles: ["employee", "manager", "hr_admin", "admin"],
  },
  {
    title: "My History",
    description: "View your overtime request history",
    route: "/hr/overtime/history",
    icon: "Calendar",
    color: "#67C23A",
    status: "ready",
    roles: ["employee", "manager", "hr_admin", "admin"],
  },
  {
    title: "Approvals",
    description: "Review and approve team overtime requests",
    route: "/hr/overtime/approvals",
    icon: "Check",
    color: "#E6A23C",
    status: "ready",
    roles: ["manager", "hr_admin", "admin"],
  },
  {
    title: "Team History",
    description: "View team member overtime records",
    route: "/hr/overtime/history#team",
    icon: "UserFilled",
    color: "#F56C6C",
    status: "ready",
    roles: ["manager", "hr_admin", "admin"],
  },
]);

const availableModules = computed(() => {
  const userRole = authStore.user?.role;
  return modules.value.filter((module) =>
    module.roles.includes(userRole || ""),
  );
});
</script>

<template>
  <div class="overtime-page">
    <OverviewHeader
      :title="'Overtime Management'"
      :description="'Request, approve, and track overtime hours'"
      :backPath="'/hr'"
    />

    <el-row :gutter="16" class="mt-4">
      <el-col
        v-for="module in availableModules"
        :key="module.route"
        :xs="24"
        :sm="12"
        :md="6"
        class="mb-4"
      >
        <el-card
          shadow="hover"
          class="module-card"
          @click="router.push(module.route)"
        >
          <div class="card-icon" :style="{ backgroundColor: module.color }">
            <el-icon :size="32" color="#fff">
              <component :is="module.icon" />
            </el-icon>
          </div>
          <h3 class="card-title">{{ module.title }}</h3>
          <p class="card-description">{{ module.description }}</p>
          <el-tag type="success" size="small" class="mt-2"> Ready </el-tag>
        </el-card>
      </el-col>
    </el-row>

    <!-- Info Section -->
    <el-row :gutter="16" class="mt-8">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span class="title">Overtime Policy</span>
            </div>
          </template>
          <div class="policy-content">
            <div class="policy-item">
              <h4>Request Requirements:</h4>
              <ul>
                <li>
                  Submit overtime requests at least 3 hours before working
                  overtime
                </li>
                <li>Provide a clear reason for the overtime</li>
                <li>Requests must be approved by your manager</li>
                <li>Only edit or cancel requests that are pending approval</li>
              </ul>
            </div>
            <div class="policy-item">
              <h4>Overtime Rates:</h4>
              <ul>
                <li>Weekday overtime: 150% of base salary</li>
                <li>Weekend overtime: 200% of base salary</li>
                <li>Public holiday overtime: 200-250% of base salary</li>
              </ul>
            </div>
            <div class="policy-item" v-if="isManager">
              <h4>Manager Responsibilities:</h4>
              <ul>
                <li>Review team overtime requests within 24 hours</li>
                <li>Approve or reject with relevant comments</li>
                <li>Monitor team overtime hours for compliance</li>
                <li>Ensure overtime is business-critical</li>
              </ul>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.overtime-page {
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
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.policy-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.policy-item h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: var(--el-text-color-primary);
}

.policy-item ul {
  margin: 0;
  padding-left: 20px;
  list-style-type: disc;
}

.policy-item li {
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 1.6;
}
</style>

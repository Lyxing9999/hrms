<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import { ElCard, ElRow, ElCol, ElStatistic } from "element-plus";
import {
  User,
  Calendar,
  Document,
  Clock,
  Money,
  Location,
} from "@element-plus/icons-vue";

const router = useRouter();

const modules = ref([
  {
    title: "Employee Management",
    description: "Manage employee profiles, contracts, and accounts",
    icon: User,
    route: "/hr/employees/employee-profile",
    color: "#409EFF",
    stats: { label: "Total Employees", value: "-" },
  },
  {
    title: "Leave Management",
    description: "Submit, approve, and track leave requests",
    icon: Calendar,
    route: "/hr/leaves",
    color: "#67C23A",
    stats: { label: "Pending Requests", value: "-" },
  },
  {
    title: "Attendance System",
    description: "Check-in/out, location validation, and tracking",
    icon: Clock,
    route: "/hr/attendance",
    color: "#E6A23C",
    stats: { label: "Today's Attendance", value: "-" },
  },
  {
    title: "Overtime Management",
    description: "Request, approve, and calculate overtime hours",
    icon: Document,
    route: "/hr/overtime",
    color: "#F56C6C",
    stats: { label: "Pending OT", value: "-" },
    badge: "Coming Soon",
  },
  {
    title: "Payroll System",
    description: "Automated payroll calculation and payslip generation",
    icon: Money,
    route: "/hr/payroll",
    color: "#909399",
    stats: { label: "This Month", value: "-" },
    badge: "Coming Soon",
  },
  {
    title: "System Configuration",
    description: "Working hours, locations, holidays, and deduction rules",
    icon: Location,
    route: "/hr/config",
    color: "#606266",
    stats: { label: "Active Locations", value: "-" },
  },
]);

const navigateTo = (route: string, badge?: string) => {
  if (badge === "Coming Soon") {
    ElMessage.warning("This module is coming soon!");
    return;
  }
  router.push(route);
};
</script>

<template>
  <div class="hrms-dashboard">
    <OverviewHeader
      :title="'HRMS Dashboard'"
      :description="'Human Resource Management System'"
    />

    <el-row :gutter="24" class="module-grid">
      <el-col
        v-for="module in modules"
        :key="module.route"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="8"
        class="mb-6"
      >
        <el-card
          shadow="hover"
          class="module-card"
          :class="{ 'coming-soon': module.badge === 'Coming Soon' }"
          @click="navigateTo(module.route, module.badge)"
        >
          <div class="card-header">
            <div class="icon-wrapper" :style="{ backgroundColor: module.color }">
              <el-icon :size="32" color="#fff">
                <component :is="module.icon" />
              </el-icon>
            </div>
            <el-tag
              v-if="module.badge"
              type="warning"
              size="small"
              class="badge"
            >
              {{ module.badge }}
            </el-tag>
          </div>

          <div class="card-content">
            <h3 class="module-title">{{ module.title }}</h3>
            <p class="module-description">{{ module.description }}</p>
          </div>

          <div class="card-footer">
            <el-statistic
              :value="module.stats.value"
              :title="module.stats.label"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Quick Stats -->
    <el-row :gutter="24" class="mt-8">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header-title">
              <span>System Overview</span>
            </div>
          </template>

          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="6">
              <el-statistic title="Total Employees" :value="0" />
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <el-statistic title="Active Leaves" :value="0" />
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <el-statistic title="Pending Approvals" :value="0" />
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <el-statistic title="This Month Payroll" value="$0" />
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.hrms-dashboard {
  padding: 20px;
}

.module-grid {
  margin-top: 24px;
}

.module-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
  min-height: 240px;
}

.module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.module-card.coming-soon {
  opacity: 0.7;
  cursor: not-allowed;
}

.module-card.coming-soon:hover {
  transform: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
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

.badge {
  position: absolute;
  top: 16px;
  right: 16px;
}

.card-content {
  margin: 16px 0;
}

.module-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--el-text-color-primary);
}

.module-description {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
  line-height: 1.6;
}

.card-footer {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.card-header-title {
  font-size: 16px;
  font-weight: 600;
}
</style>

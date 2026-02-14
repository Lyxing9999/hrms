<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/authStore";
import {
  Clock,
  Calendar,
  Document,
  User,
  Timer,
  Location,
} from "@element-plus/icons-vue";

const router = useRouter();
const authStore = useAuthStore();

const userName = ref(authStore.user?.username || "Employee");

const quickActions = [
  {
    title: "Check In / Out",
    description: "Record your attendance",
    icon: Clock,
    route: "/employee/check-in",
    color: "#409EFF",
  },
  {
    title: "Attendance History",
    description: "View your attendance records",
    icon: Calendar,
    route: "/employee/attendance-history",
    color: "#67C23A",
  },
  {
    title: "My Leaves",
    description: "View and manage leave requests",
    icon: Document,
    route: "/hr/leaves",
    color: "#E6A23C",
  },
  {
    title: "My Profile",
    description: "View your employee profile",
    icon: User,
    route: "/employee/profile",
    color: "#909399",
  },
];

const navigateTo = (route: string) => {
  router.push(route);
};
</script>

<template>
  <div class="employee-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="welcome-section">
        <h1 class="welcome-title">Welcome back, {{ userName }}!</h1>
        <p class="welcome-subtitle">
          {{ new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" }) }}
        </p>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="content-wrapper">
      <h2 class="section-title">Quick Actions</h2>
      <el-row :gutter="24" class="actions-grid">
        <el-col
          v-for="action in quickActions"
          :key="action.route"
          :xs="24"
          :sm="12"
          :md="6"
          class="action-col"
        >
          <el-card
            shadow="hover"
            class="action-card"
            @click="navigateTo(action.route)"
          >
            <div class="action-content">
              <div
                class="action-icon"
                :style="{ backgroundColor: action.color }"
              >
                <el-icon :size="32" color="#fff">
                  <component :is="action.icon" />
                </el-icon>
              </div>
              <h3 class="action-title">{{ action.title }}</h3>
              <p class="action-description">{{ action.description }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- Info Cards -->
      <el-row :gutter="24" class="mt-6">
        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="info-card" shadow="hover">
            <div class="info-content">
              <el-icon :size="48" class="info-icon" color="#409EFF">
                <Timer />
              </el-icon>
              <div class="info-text">
                <h3 class="info-title">Today's Status</h3>
                <p class="info-value">Not Checked In</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="info-card" shadow="hover">
            <div class="info-content">
              <el-icon :size="48" class="info-icon" color="#67C23A">
                <Calendar />
              </el-icon>
              <div class="info-text">
                <h3 class="info-title">This Month</h3>
                <p class="info-value">0 Days Worked</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="info-card" shadow="hover">
            <div class="info-content">
              <el-icon :size="48" class="info-icon" color="#E6A23C">
                <Document />
              </el-icon>
              <div class="info-text">
                <h3 class="info-title">Leave Balance</h3>
                <p class="info-value">- Days</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped>
.employee-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.dashboard-header {
  margin-bottom: 32px;
  text-align: center;
}

.welcome-section {
  color: white;
}

.welcome-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.welcome-subtitle {
  font-size: 18px;
  opacity: 0.9;
  margin: 0;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: white;
  margin: 0 0 24px 0;
}

.actions-grid {
  margin-bottom: 24px;
}

.action-col {
  margin-bottom: 24px;
}

.action-card {
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 16px;
  height: 100%;
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.action-content {
  text-align: center;
  padding: 24px 16px;
}

.action-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.action-description {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

.info-card {
  border-radius: 16px;
  height: 100%;
}

.info-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px;
}

.info-icon {
  flex-shrink: 0;
}

.info-text {
  flex: 1;
}

.info-title {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0 0 4px 0;
}

.info-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  margin: 0;
}

.mt-6 {
  margin-top: 24px;
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 28px;
  }

  .welcome-subtitle {
    font-size: 16px;
  }

  .section-title {
    font-size: 20px;
  }
}
</style>

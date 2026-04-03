<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import * as Icons from "@element-plus/icons-vue";
import { useAuthStore } from "~/stores/authStore";
import { ROUTES } from "~/constants/routes";

type RoleKey = keyof typeof ROUTES;

interface MenuItem {
  title: string;
  icon?: keyof typeof Icons;
  route?: string;
  children?: MenuItem[];
  badge?: string; // For "Coming Soon" or "New" badges
}

interface MenuNode extends MenuItem {
  index: string;
  iconComponent: any;
  children?: MenuNode[];
}

const props = defineProps<{ logoSrc: string; collapsed?: boolean }>();
const emit = defineEmits<{ (e: "navigate"): void }>();

const authStore = useAuthStore();
const route = useRoute();

/** Role menus */
const menus: Record<RoleKey, MenuItem[]> = {
  ADMIN: [
    { title: "Dashboard", icon: "HomeFilled", route: ROUTES.ADMIN.DASHBOARD },
    {
      title: "Management",
      icon: "Management",
      children: [
        {
          title: "Manage Users",
          icon: "UserFilled",
          route: ROUTES.ADMIN.MANAGE_USERS,
        },
        {
          title: "Manage Classes",
          icon: "Notebook",
          route: ROUTES.ADMIN.MANAGE_CLASSES,
        },
        {
          title: "Manage Subjects",
          icon: "Collection",
          route: ROUTES.ADMIN.MANAGE_SUBJECTS,
        },
        {
          title: "Manage Schedules",
          icon: "Calendar",
          route: ROUTES.ADMIN.MANAGE_SCHEDULES,
        },
      ],
    },
    {
      title: "Teaching",
      icon: "Link",
      children: [
        {
          title: "Teaching Assignments",
          icon: "Link",
          route: ROUTES.ADMIN.TEACHING_ASSIGNMENTS,
        },
      ],
    },
    {
      title: "System",
      icon: "Setting",
      children: [
        {
          title: "Notifications",
          icon: "Bell",
          route: ROUTES.ADMIN.NOTIFICATIONS,
        },
        { title: "Settings", icon: "Setting", route: ROUTES.ADMIN.SETTINGS },
      ],
    },
  ],

  TEACHER: [
    { title: "Dashboard", icon: "HomeFilled", route: ROUTES.TEACHER.DASHBOARD },
    {
      title: "Students",
      icon: "UserFilled",
      children: [
        {
          title: "Manage Students",
          icon: "UserFilled",
          route: ROUTES.TEACHER.MANAGE_STUDENTS,
        },
      ],
    },
    {
      title: "Academics",
      icon: "Notebook",
      children: [
        {
          title: "My Classes",
          icon: "Notebook",
          route: ROUTES.TEACHER.MY_CLASSES,
        },
        { title: "Grades", icon: "TrendCharts", route: ROUTES.TEACHER.GRADES },
        {
          title: "Attendance",
          icon: "Finished",
          route: ROUTES.TEACHER.ATTENDANCE,
        },
        { title: "Schedule", icon: "Timer", route: ROUTES.TEACHER.SCHEDULE },
      ],
    },
    {
      title: "System",
      icon: "Setting",
      children: [
        {
          title: "Notifications",
          icon: "Bell",
          route: ROUTES.TEACHER.NOTIFICATIONS,
        },
        { title: "Calendar", icon: "Calendar", route: ROUTES.TEACHER.CALENDAR },
        { title: "Settings", icon: "Setting", route: ROUTES.TEACHER.SETTINGS },
      ],
    },
  ],

  STUDENT: [
    { title: "Dashboard", icon: "HomeFilled", route: ROUTES.STUDENT.DASHBOARD },
    {
      title: "My Study",
      icon: "Notebook",
      children: [
        {
          title: "My Classes",
          icon: "Notebook",
          route: ROUTES.STUDENT.MY_CLASSES,
        },
        {
          title: "My Grades",
          icon: "TrendCharts",
          route: ROUTES.STUDENT.MY_GRADES,
        },
        {
          title: "My Schedule",
          icon: "Timer",
          route: ROUTES.STUDENT.MY_SCHEDULE,
        },
        {
          title: "Attendance",
          icon: "Finished",
          route: ROUTES.STUDENT.ATTENDANCE,
        },
      ],
    },
    {
      title: "System",
      icon: "Setting",
      children: [
        {
          title: "Notifications",
          icon: "Bell",
          route: ROUTES.STUDENT.NOTIFICATIONS,
        },
        { title: "Calendar", icon: "Calendar", route: ROUTES.STUDENT.CALENDAR },
        { title: "Settings", icon: "Setting", route: ROUTES.STUDENT.SETTINGS },
      ],
    },
  ],

  HR_ADMIN: [
    {
      title: "Dashboard",
      icon: "HomeFilled",
      route: "/hr",
    },
    {
      title: "Employees",
      icon: "UserFilled",
      children: [
        {
          title: "Employee Directory",
          icon: "User",
          route: "/hr/employees",
        },
        {
          title: "Employee Accounts",
          icon: "Avatar",
          route: "/hr/employees/accounts",
        },
        {
          title: "Attendance Log",
          icon: "Finished",
          route: "/hr/employees/attendance",
        },
      ],
    },
    {
      title: "Attendance",
      icon: "Clock",
      children: [
        {
          title: "Overview",
          icon: "List",
          route: "/hr/attendance",
        },
        {
          title: "Check In",
          icon: "Clock",
          route: "/hr/attendance/check-in",
        },
        {
          title: "Attendance History",
          icon: "Document",
          route: "/hr/attendance/history",
        },
        {
          title: "Team Attendance",
          icon: "UserFilled",
          route: "/hr/attendance/team",
        },
        {
          title: "Attendance Reports",
          icon: "Document",
          route: "/hr/attendance/reports",
        },
      ],
    },
    {
      title: "Overtime",
      icon: "Timer",
      children: [
        {
          title: "Overview",
          icon: "Timer",
          route: "/hr/overtime",
        },
        {
          title: "Request Overtime",
          icon: "EditPen",
          route: "/hr/overtime/request",
        },
        {
          title: "Overtime History",
          icon: "List",
          route: "/hr/overtime/history",
        },
        {
          title: "Approvals",
          icon: "CircleCheck",
          route: "/hr/overtime/approvals",
        },
      ],
    },
    {
      title: "Leave",
      icon: "Calendar",
      children: [
        {
          title: "Leave Management",
          icon: "Calendar",
          route: "/hr/leaves",
        },
      ],
    },
    {
      title: "Payroll",
      icon: "Money",
      children: [
        {
          title: "Overview",
          icon: "Money",
          route: "/hr/payroll",
        },
        {
          title: "Process Payroll",
          icon: "Operation",
          route: "/hr/payroll/process",
        },
        {
          title: "Payroll History",
          icon: "List",
          route: "/hr/payroll/history",
        },
        {
          title: "Payslips",
          icon: "Document",
          route: "/hr/payslips",
        },
      ],
    },
    {
      title: "Configuration",
      icon: "Setting",
      children: [
        {
          title: "Overview",
          icon: "Setting",
          route: "/hr/config",
        },
        {
          title: "Working Schedules",
          icon: "Clock",
          route: "/hr/config/schedules",
        },
        {
          title: "Work Locations",
          icon: "Location",
          route: "/hr/config/locations",
        },
        {
          title: "Public Holidays",
          icon: "Calendar",
          route: "/hr/config/public-holidays",
        },
        {
          title: "Deduction Rules",
          icon: "Coin",
          route: "/hr/config/deductions",
        },
      ],
    },
    {
      title: "Reports",
      icon: "DataAnalysis",
      children: [
        {
          title: "Overview",
          icon: "DataAnalysis",
          route: "/hr/reports",
        },
        {
          title: "Attendance",
          icon: "Document",
          route: "/hr/reports/attendance",
        },
        {
          title: "Overtime",
          icon: "Document",
          route: "/hr/reports/overtime",
        },
        {
          title: "Payroll",
          icon: "Document",
          route: "/hr/reports/payroll",
        },
        {
          title: "Deductions",
          icon: "Document",
          route: "/hr/reports/deductions",
        },
      ],
    },
  ],

  EMPLOYEE: [
    {
      title: "Dashboard",
      icon: "HomeFilled",
      route: ROUTES.EMPLOYEE.DASHBOARD,
    },
    {
      title: "Attendance",
      icon: "Clock",
      children: [
        {
          title: "Check In",
          icon: "Clock",
          route: ROUTES.EMPLOYEE.ATTENDANCE_CHECK,
        },
        {
          title: "Attendance History",
          icon: "List",
          route: ROUTES.EMPLOYEE.ATTENDANCE_HISTORY,
        },
      ],
    },
    {
      title: "Overtime",
      icon: "Timer",
      children: [
        {
          title: "Request Overtime",
          icon: "EditPen",
          route: ROUTES.EMPLOYEE.OVERTIME_REQUEST,
        },
        {
          title: "Overtime History",
          icon: "Document",
          route: ROUTES.EMPLOYEE.OVERTIME_HISTORY,
        },
      ],
    },
    {
      title: "Leave",
      icon: "Calendar",
      children: [
        {
          title: "Request Leave",
          icon: "EditPen",
          route: ROUTES.EMPLOYEE.LEAVE_REQUEST,
        },
        {
          title: "Leave History",
          icon: "Document",
          route: ROUTES.EMPLOYEE.LEAVE_HISTORY,
        },
        {
          title: "Leave Balance",
          icon: "Memo",
          route: ROUTES.EMPLOYEE.LEAVE_BALANCE,
        },
      ],
    },
    {
      title: "Payroll",
      icon: "Money",
      children: [
        {
          title: "Payslips",
          icon: "Document",
          route: ROUTES.EMPLOYEE.PAYSLIPS,
        },
      ],
    },
    {
      title: "Profile",
      icon: "User",
      route: ROUTES.EMPLOYEE.PROFILE,
    },
  ],

  MANAGER: [
    {
      title: "Dashboard",
      icon: "HomeFilled",
      route: ROUTES.MANAGER.DASHBOARD,
    },
    {
      title: "Attendance",
      icon: "Clock",
      children: [
        {
          title: "Team Attendance",
          icon: "UserFilled",
          route: ROUTES.MANAGER.ATTENDANCE_TEAM,
        },
        {
          title: "Attendance Reports",
          icon: "Document",
          route: ROUTES.MANAGER.ATTENDANCE_REPORTS,
        },
      ],
    },
    {
      title: "Overtime",
      icon: "Timer",
      children: [
        {
          title: "OT Reviews",
          icon: "CircleCheck",
          route: ROUTES.MANAGER.OVERTIME_REVIEWS,
        },
        {
          title: "OT History",
          icon: "Document",
          route: ROUTES.MANAGER.OVERTIME_HISTORY,
        },
      ],
    },
    {
      title: "Leave",
      icon: "Calendar",
      children: [
        {
          title: "Leave Reviews",
          icon: "CircleCheck",
          route: ROUTES.MANAGER.LEAVE_REVIEWS,
        },
        {
          title: "Leave History",
          icon: "Document",
          route: ROUTES.MANAGER.LEAVE_HISTORY,
        },
      ],
    },
    {
      title: "Reports",
      icon: "DataAnalysis",
      children: [
        {
          title: "Team Reports",
          icon: "Document",
          route: ROUTES.MANAGER.REPORTS_TEAM,
        },
      ],
    },
  ],

  PAYROLL_MANAGER: [
    {
      title: "Dashboard",
      icon: "HomeFilled",
      route: ROUTES.PAYROLL_MANAGER.DASHBOARD,
    },
    {
      title: "Payroll",
      icon: "Money",
      children: [
        {
          title: "Generate Payroll",
          icon: "Operation",
          route: ROUTES.PAYROLL_MANAGER.PAYROLL_PROCESS,
        },
        {
          title: "Payroll Runs",
          icon: "List",
          route: ROUTES.PAYROLL_MANAGER.PAYROLL_RUNS,
        },
        {
          title: "Payslips",
          icon: "Document",
          route: ROUTES.PAYROLL_MANAGER.PAYSLIPS,
        },
      ],
    },
    {
      title: "Attendance",
      icon: "Clock",
      children: [
        {
          title: "Final Attendance",
          icon: "List",
          route: ROUTES.PAYROLL_MANAGER.ATTENDANCE_FINAL,
        },
      ],
    },
    {
      title: "Overtime",
      icon: "Timer",
      children: [
        {
          title: "Approved OT",
          icon: "CircleCheck",
          route: ROUTES.PAYROLL_MANAGER.OVERTIME_APPROVED,
        },
      ],
    },
    {
      title: "Reports",
      icon: "DataAnalysis",
      children: [
        {
          title: "Payroll Reports",
          icon: "Document",
          route: ROUTES.PAYROLL_MANAGER.REPORTS_PAYROLL,
        },
      ],
    },
  ],
};

/** IMPORTANT: don’t default to ADMIN while loading */
const role = computed<RoleKey | null>(() => {
  if (!authStore.isReady) return null;
  const r = authStore.user?.role?.toUpperCase();
  return (r as RoleKey) ?? null;
});

function iconOf(name?: keyof typeof Icons) {
  if (!name) return Icons.Menu;
  return (Icons as any)[name] ?? Icons.Menu;
}

/** stable submenu indexes */
function groupIndex(path: string[], title: string) {
  return `group:${[...path, title].join(" / ")}`;
}

function toNodes(items: MenuItem[], path: string[] = []): MenuNode[] {
  return items.map((it) => {
    const index = it.route || groupIndex(path, it.title);
    return {
      ...it,
      index,
      iconComponent: iconOf(it.icon),
      children: it.children
        ? toNodes(it.children, [...path, it.title])
        : undefined,
    };
  });
}

const menuTree = computed<MenuNode[]>(() => {
  if (!role.value) return [];
  return toNodes(menus[role.value] ?? []);
});

/** active leaf route */
function matchActiveLeaf(items: MenuNode[]): string {
  for (const it of items) {
    if (
      it.route &&
      (route.path === it.route || route.path.startsWith(it.route + "/"))
    )
      return it.route;
    if (it.children?.length) {
      const hit = matchActiveLeaf(it.children);
      if (hit) return hit;
    }
  }
  return "";
}

const activeIndex = computed(() => matchActiveLeaf(menuTree.value));

/** open parent groups */
function findOpenGroups(items: MenuNode[], parents: string[] = []): string[] {
  for (const it of items) {
    if (
      it.route &&
      (route.path === it.route || route.path.startsWith(it.route + "/"))
    )
      return parents;
    if (it.children?.length) {
      const res = findOpenGroups(it.children, [...parents, it.index]);
      if (res.length) return res;
    }
  }
  return [];
}

const openeds = computed(() => findOpenGroups(menuTree.value));

function handleSelect() {
  emit("navigate");
}
</script>

<template>
  <aside class="app-aside" :class="{ 'is-collapsed': !!collapsed }">
    <div class="logo-section">
      <div class="logo-badge" aria-label="App logo">
        <img :src="logoSrc" class="logo-image" alt="Logo" />
      </div>
    </div>

    <div class="menu-scroll">
      <el-menu
        v-if="authStore.isReady && role"
        class="app-menu"
        router
        :collapse="!!collapsed"
        :collapse-transition="false"
        :default-active="activeIndex"
        :default-openeds="openeds"
        @select="handleSelect"
      >
        <template v-for="item in menuTree" :key="item.index">
          <el-sub-menu v-if="item.children?.length" :index="item.index">
            <template #title>
              <el-icon><component :is="item.iconComponent" /></el-icon>
              <span class="menu-title">{{ item.title }}</span>
            </template>

            <el-menu-item
              v-for="child in item.children"
              :key="child.index"
              :index="child.route!"
              :title="child.title"
            >
              <el-icon><component :is="child.iconComponent" /></el-icon>
              <template #title>
                <span class="menu-title">{{ child.title }}</span>
                <el-tag
                  v-if="child.badge"
                  size="small"
                  type="warning"
                  class="menu-badge"
                >
                  {{ child.badge }}
                </el-tag>
              </template>
            </el-menu-item>
          </el-sub-menu>

          <el-menu-item v-else :index="item.route!" :title="item.title">
            <el-icon><component :is="item.iconComponent" /></el-icon>
            <template #title>
              <span class="menu-title">{{ item.title }}</span>
              <el-tag
                v-if="item.badge"
                size="small"
                type="warning"
                class="menu-badge"
              >
                {{ item.badge }}
              </el-tag>
            </template>
          </el-menu-item>
        </template>
      </el-menu>

      <!-- Skeleton while auth loads -->
      <div v-else class="menu-skeleton" aria-busy="true">
        <div class="skeleton-item" v-for="i in 7" :key="i"></div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.app-aside {
  background: var(--app-surface);
  border-right: 1px solid var(--app-border);
  color: var(--app-text);
}

:deep(.el-menu) {
  background: transparent;
  border-right: 0;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  color: var(--app-text);
}

:deep(.el-menu-item.is-active) {
  background: var(--app-active-bg);
  color: var(--app-primary);
  border-radius: 12px;
}

.menu-skeleton .skeleton-item {
  background: color-mix(in srgb, var(--app-muted) 25%, transparent);
}

.menu-badge {
  margin-left: 8px;
  font-size: 10px;
  padding: 0 6px;
  height: 18px;
  line-height: 18px;
}
</style>

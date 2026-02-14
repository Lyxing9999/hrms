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
      route: ROUTES.HR_ADMIN.DASHBOARD,
    },
    {
      title: "Employee Management",
      icon: "UserFilled",
      children: [
        {
          title: "All Employees",
          icon: "User",
          route: ROUTES.HR_ADMIN.EMPLOYEES,
        },
      ],
    },
    {
      title: "Leave Management",
      icon: "Calendar",
      children: [
        {
          title: "All Leaves",
          icon: "Calendar",
          route: ROUTES.HR_ADMIN.LEAVES,
        },
        {
          title: "Leave Approvals",
          icon: "CircleCheck",
          route: ROUTES.HR_ADMIN.LEAVE_APPROVALS,
          badge: "Soon",
        },
        {
          title: "My Leaves",
          icon: "Document",
          route: ROUTES.HR_ADMIN.MY_LEAVES,
          badge: "Soon",
        },
      ],
    },
    {
      title: "Attendance System",
      icon: "Clock",
      children: [
        {
          title: "Check In/Out",
          icon: "Clock",
          route: ROUTES.HR_ADMIN.ATTENDANCE_CHECK_IN,
          badge: "Soon",
        },
        {
          title: "Attendance History",
          icon: "List",
          route: ROUTES.HR_ADMIN.ATTENDANCE_HISTORY,
          badge: "Soon",
        },
        {
          title: "Team Attendance",
          icon: "User",
          route: ROUTES.HR_ADMIN.ATTENDANCE_TEAM,
          badge: "Soon",
        },
        {
          title: "Reports",
          icon: "Document",
          route: ROUTES.HR_ADMIN.ATTENDANCE_REPORTS,
          badge: "Soon",
        },
      ],
    },
    {
      title: "Overtime (OT)",
      icon: "Timer",
      children: [
        {
          title: "OT Requests",
          icon: "Timer",
          route: ROUTES.HR_ADMIN.OVERTIME,
          badge: "Soon",
        },
        {
          title: "OT Approvals",
          icon: "CircleCheck",
          route: ROUTES.HR_ADMIN.OVERTIME_APPROVALS,
          badge: "Soon",
        },
        {
          title: "OT History",
          icon: "List",
          route: ROUTES.HR_ADMIN.OVERTIME_HISTORY,
          badge: "Soon",
        },
      ],
    },
    {
      title: "Payroll System",
      icon: "Money",
      children: [
        {
          title: "Process Payroll",
          icon: "Money",
          route: ROUTES.HR_ADMIN.PAYROLL_PROCESS,
          badge: "Soon",
        },
        {
          title: "Payroll History",
          icon: "List",
          route: ROUTES.HR_ADMIN.PAYROLL_HISTORY,
          badge: "Soon",
        },
        {
          title: "Payslips",
          icon: "Document",
          route: ROUTES.HR_ADMIN.PAYSLIPS,
          badge: "Soon",
        },
      ],
    },
    {
      title: "Configuration",
      icon: "Setting",
      children: [
        {
          title: "Working Schedules",
          icon: "Clock",
          route: ROUTES.HR_ADMIN.WORKING_SCHEDULES,
        },
        {
          title: "Work Locations",
          icon: "Location",
          route: ROUTES.HR_ADMIN.WORK_LOCATIONS,
        },
        {
          title: "Public Holidays",
          icon: "Calendar",
          route: ROUTES.HR_ADMIN.PUBLIC_HOLIDAYS,
        },
        {
          title: "Deduction Rules",
          icon: "Coin",
          route: ROUTES.HR_ADMIN.DEDUCTION_RULES,
        },
      ],
    },
    {
      title: "Reports & Analytics",
      icon: "DataAnalysis",
      children: [
        {
          title: "Attendance Reports",
          icon: "Document",
          route: ROUTES.HR_ADMIN.REPORTS_ATTENDANCE,
          badge: "Soon",
        },
        {
          title: "Overtime Reports",
          icon: "Document",
          route: ROUTES.HR_ADMIN.REPORTS_OVERTIME,
          badge: "Soon",
        },
        {
          title: "Payroll Reports",
          icon: "Document",
          route: ROUTES.HR_ADMIN.REPORTS_PAYROLL,
          badge: "Soon",
        },
        {
          title: "Deduction Reports",
          icon: "Document",
          route: ROUTES.HR_ADMIN.REPORTS_DEDUCTIONS,
          badge: "Soon",
        },
      ],
    },
    {
      title: "System",
      icon: "Tools",
      children: [
        {
          title: "Notifications",
          icon: "Bell",
          route: ROUTES.HR_ADMIN.NOTIFICATIONS,
        },
        {
          title: "Calendar",
          icon: "Calendar",
          route: ROUTES.HR_ADMIN.CALENDAR,
        },
        {
          title: "Settings",
          icon: "Setting",
          route: ROUTES.HR_ADMIN.SETTINGS,
        },
      ],
    },
  ],

  // ============================================
  // EMPLOYEE SELF-SERVICE PORTAL
  // ============================================
  EMPLOYEE: [
    {
      title: "Dashboard",
      icon: "HomeFilled",
      route: ROUTES.EMPLOYEE.DASHBOARD,
    },
    {
      title: "My Profile",
      icon: "UserFilled",
      route: ROUTES.EMPLOYEE.MY_PROFILE,
    },
    {
      title: "Attendance",
      icon: "Clock",
      children: [
        {
          title: "Check In/Out",
          icon: "Clock",
          route: ROUTES.EMPLOYEE.CHECK_IN,
        },
        {
          title: "My Attendance",
          icon: "List",
          route: ROUTES.EMPLOYEE.MY_ATTENDANCE,
        },
      ],
    },
    {
      title: "Leave",
      icon: "Calendar",
      children: [
        {
          title: "My Leaves",
          icon: "Calendar",
          route: ROUTES.EMPLOYEE.MY_LEAVES,
        },
      ],
    },
    {
      title: "Overtime",
      icon: "Timer",
      children: [
        {
          title: "My Overtime",
          icon: "Timer",
          route: ROUTES.EMPLOYEE.MY_OVERTIME,
        },
      ],
    },
    {
      title: "Payroll",
      icon: "Money",
      children: [
        {
          title: "My Payslips",
          icon: "Document",
          route: ROUTES.EMPLOYEE.MY_PAYSLIPS,
        },
        {
          title: "My Schedule",
          icon: "Calendar",
          route: ROUTES.EMPLOYEE.MY_SCHEDULE,
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
          route: ROUTES.EMPLOYEE.NOTIFICATIONS,
        },
        {
          title: "Settings",
          icon: "Setting",
          route: ROUTES.EMPLOYEE.SETTINGS,
        },
      ],
    },
  ],

  // ============================================
  // MANAGER PORTAL
  // ============================================
  MANAGER: [
    {
      title: "Dashboard",
      icon: "HomeFilled",
      route: ROUTES.MANAGER.DASHBOARD,
    },
    {
      title: "My Team",
      icon: "UserFilled",
      children: [
        {
          title: "Team Overview",
          icon: "User",
          route: ROUTES.MANAGER.TEAM,
        },
        {
          title: "Team Attendance",
          icon: "Clock",
          route: ROUTES.MANAGER.TEAM_ATTENDANCE,
        },
      ],
    },
    {
      title: "Approvals",
      icon: "CircleCheck",
      children: [
        {
          title: "Leave Approvals",
          icon: "Calendar",
          route: ROUTES.MANAGER.LEAVE_APPROVALS,
        },
        {
          title: "Overtime Approvals",
          icon: "Timer",
          route: ROUTES.MANAGER.OVERTIME_APPROVALS,
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
          route: ROUTES.MANAGER.TEAM_REPORTS,
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
          route: ROUTES.MANAGER.NOTIFICATIONS,
        },
        {
          title: "Settings",
          icon: "Setting",
          route: ROUTES.MANAGER.SETTINGS,
        },
      ],
    },
  ],

  // ============================================
  // PAYROLL MANAGER PORTAL
  // ============================================
  PAYROLL_MANAGER: [
    {
      title: "Dashboard",
      icon: "HomeFilled",
      route: ROUTES.PAYROLL_MANAGER.DASHBOARD,
    },
    {
      title: "Payroll Processing",
      icon: "Money",
      children: [
        {
          title: "Process Payroll",
          icon: "Money",
          route: ROUTES.PAYROLL_MANAGER.PROCESS_PAYROLL,
        },
        {
          title: "Payroll History",
          icon: "List",
          route: ROUTES.PAYROLL_MANAGER.PAYROLL_HISTORY,
        },
      ],
    },
    {
      title: "Payslips",
      icon: "Document",
      children: [
        {
          title: "All Payslips",
          icon: "Document",
          route: ROUTES.PAYROLL_MANAGER.PAYSLIPS,
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
          route: ROUTES.PAYROLL_MANAGER.REPORTS,
        },
      ],
    },
    {
      title: "System",
      icon: "Setting",
      children: [
        {
          title: "Settings",
          icon: "Setting",
          route: ROUTES.PAYROLL_MANAGER.SETTINGS,
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

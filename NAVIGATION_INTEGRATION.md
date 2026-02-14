# Navigation Integration for Live Tracking Page

## Add to HR Navigation Menu

### Option 1: If you have a menu configuration file

```typescript
// Example: ~/config/menu.ts or ~/constants/navigation.ts

export const hrMenuItems = [
  {
    title: 'Dashboard',
    icon: 'Dashboard',
    path: '/hr/dashboard',
    roles: ['hr_admin', 'manager']
  },
  {
    title: 'Employees',
    icon: 'User',
    path: '/hr/employees',
    roles: ['hr_admin']
  },
  {
    title: 'Attendance',
    icon: 'Clock',
    children: [
      {
        title: 'Attendance Records',
        path: '/hr/attendance',
        roles: ['hr_admin', 'manager']
      },
      {
        title: 'Live Tracking',  // ← NEW
        path: '/hr/attendance/live-tracking',
        roles: ['hr_admin', 'manager'],
        badge: 'Live',
        badgeType: 'success'
      }
    ]
  },
  {
    title: 'Leaves',
    icon: 'Calendar',
    path: '/hr/leaves',
    roles: ['hr_admin', 'manager']
  }
];
```

### Option 2: Direct link in layout

```vue
<!-- Example: ~/layouts/hr.vue or ~/components/navigation/HRSidebar.vue -->

<template>
  <el-menu>
    <!-- Other menu items -->
    
    <el-sub-menu index="attendance">
      <template #title>
        <el-icon><Clock /></el-icon>
        <span>Attendance</span>
      </template>
      
      <el-menu-item index="/hr/attendance">
        Attendance Records
      </el-menu-item>
      
      <!-- NEW: Live Tracking -->
      <el-menu-item index="/hr/attendance/live-tracking">
        <el-icon><MapLocation /></el-icon>
        <span>Live Tracking</span>
        <el-badge value="Live" type="success" class="ml-2" />
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>
```

### Option 3: Dashboard Quick Link

```vue
<!-- Example: ~/pages/hr/dashboard.vue -->

<template>
  <div class="dashboard">
    <!-- Other dashboard content -->
    
    <el-row :gutter="16">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="quick-link-card">
          <div class="quick-link" @click="navigateTo('/hr/attendance/live-tracking')">
            <div class="icon-wrapper">
              <el-icon :size="40" color="#2196F3">
                <MapLocation />
              </el-icon>
            </div>
            <h3>Live Tracking</h3>
            <p>Monitor employee locations in real-time</p>
            <el-badge value="Live" type="success" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.quick-link-card {
  cursor: pointer;
  transition: all 0.3s;
}

.quick-link-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.quick-link {
  text-align: center;
  padding: 20px;
}

.icon-wrapper {
  margin-bottom: 16px;
}
</style>
```

## Route Protection

### Middleware Setup

```typescript
// middleware/auth.ts or middleware/role.ts

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return navigateTo('/login');
  }
  
  // Check role-based access
  if (to.meta.roles) {
    const userRole = authStore.user?.role;
    const allowedRoles = to.meta.roles as string[];
    
    if (!allowedRoles.includes(userRole)) {
      ElMessage.error('You do not have permission to access this page');
      return navigateTo('/dashboard');
    }
  }
});
```

### Page Meta

The live tracking page already includes proper meta (if using Nuxt 3 auto-routing):

```typescript
// This is automatically inferred from the file path
// frontend/src/pages/hr/attendance/live-tracking.vue

definePageMeta({
  layout: 'hr',
  middleware: ['auth', 'role'],
  requiresAuth: true,
  roles: ['hr_admin', 'manager']
});
```

## Breadcrumb Integration

```vue
<!-- Example: Add to page or layout -->

<el-breadcrumb separator="/">
  <el-breadcrumb-item :to="{ path: '/hr/dashboard' }">
    HR Dashboard
  </el-breadcrumb-item>
  <el-breadcrumb-item :to="{ path: '/hr/attendance' }">
    Attendance
  </el-breadcrumb-item>
  <el-breadcrumb-item>
    Live Tracking
  </el-breadcrumb-item>
</el-breadcrumb>
```

## Notification Badge

Show count of active employees in menu:

```vue
<template>
  <el-menu-item index="/hr/attendance/live-tracking">
    <el-icon><MapLocation /></el-icon>
    <span>Live Tracking</span>
    <el-badge 
      v-if="activeEmployeeCount > 0"
      :value="activeEmployeeCount" 
      type="success" 
      class="ml-2" 
    />
  </el-menu-item>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { io } from 'socket.io-client';

const activeEmployeeCount = ref(0);

onMounted(() => {
  // Connect to get live count
  const socket = io('http://localhost:5001');
  
  socket.on('manager:joined', (data) => {
    activeEmployeeCount.value = data.active_employees?.length || 0;
  });
  
  socket.on('employee:location', (data) => {
    // Update count based on status changes
    if (data.status === 'active') {
      activeEmployeeCount.value++;
    } else {
      activeEmployeeCount.value = Math.max(0, activeEmployeeCount.value - 1);
    }
  });
});
</script>
```

## Mobile Navigation

For mobile responsive menu:

```vue
<template>
  <el-drawer v-model="drawerVisible" direction="ltr">
    <template #header>
      <h3>HR Menu</h3>
    </template>
    
    <el-menu>
      <!-- Other items -->
      
      <el-menu-item 
        index="/hr/attendance/live-tracking"
        @click="navigateAndClose('/hr/attendance/live-tracking')"
      >
        <el-icon><MapLocation /></el-icon>
        <span>Live Tracking</span>
        <el-badge value="Live" type="success" />
      </el-menu-item>
    </el-menu>
  </el-drawer>
</template>

<script setup lang="ts">
const drawerVisible = ref(false);
const router = useRouter();

const navigateAndClose = (path: string) => {
  router.push(path);
  drawerVisible.value = false;
};
</script>
```

## Permission Check Component

Create a reusable permission wrapper:

```vue
<!-- components/PermissionGuard.vue -->

<template>
  <slot v-if="hasPermission" />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from '~/stores/authStore';

const props = defineProps<{
  roles: string[];
}>();

const authStore = useAuthStore();

const hasPermission = computed(() => {
  const userRole = authStore.user?.role;
  return props.roles.includes(userRole);
});
</script>
```

Usage:

```vue
<PermissionGuard :roles="['hr_admin', 'manager']">
  <el-menu-item index="/hr/attendance/live-tracking">
    <el-icon><MapLocation /></el-icon>
    <span>Live Tracking</span>
  </el-menu-item>
</PermissionGuard>
```

## Quick Access Button

Add floating action button on attendance pages:

```vue
<!-- Add to ~/pages/hr/attendance/index.vue -->

<template>
  <div class="attendance-page">
    <!-- Existing content -->
    
    <!-- Floating Action Button -->
    <el-button
      type="primary"
      circle
      size="large"
      class="fab-button"
      @click="navigateTo('/hr/attendance/live-tracking')"
    >
      <el-icon :size="24">
        <MapLocation />
      </el-icon>
    </el-button>
  </div>
</template>

<style scoped>
.fab-button {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 64px;
  height: 64px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.fab-button:hover {
  transform: scale(1.1);
}
</style>
```

## Testing Navigation

1. **Check Route Access**
   ```bash
   # Navigate to the page
   http://localhost:3000/hr/attendance/live-tracking
   ```

2. **Test Role Permissions**
   - Login as `hr_admin` → Should access
   - Login as `manager` → Should access
   - Login as `employee` → Should redirect/deny

3. **Test Menu Visibility**
   - Verify menu item appears for authorized roles
   - Verify menu item hidden for unauthorized roles

4. **Test Navigation Flow**
   - Click menu item → Page loads
   - Use breadcrumbs → Navigate back
   - Use browser back button → Works correctly

## Complete Example

Here's a complete navigation component:

```vue
<!-- components/navigation/HRMenu.vue -->

<template>
  <el-menu
    :default-active="activeIndex"
    mode="vertical"
    @select="handleSelect"
  >
    <el-menu-item index="/hr/dashboard">
      <el-icon><Dashboard /></el-icon>
      <span>Dashboard</span>
    </el-menu-item>
    
    <el-sub-menu index="attendance">
      <template #title>
        <el-icon><Clock /></el-icon>
        <span>Attendance</span>
      </template>
      
      <el-menu-item index="/hr/attendance">
        <el-icon><Document /></el-icon>
        <span>Records</span>
      </el-menu-item>
      
      <el-menu-item index="/hr/attendance/live-tracking">
        <el-icon><MapLocation /></el-icon>
        <span>Live Tracking</span>
        <el-badge 
          v-if="activeCount > 0"
          :value="activeCount" 
          type="success"
          class="menu-badge"
        />
      </el-menu-item>
    </el-sub-menu>
    
    <PermissionGuard :roles="['hr_admin']">
      <el-menu-item index="/hr/employees">
        <el-icon><User /></el-icon>
        <span>Employees</span>
      </el-menu-item>
    </PermissionGuard>
  </el-menu>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { io } from 'socket.io-client';

const route = useRoute();
const router = useRouter();
const activeCount = ref(0);

const activeIndex = computed(() => route.path);

const handleSelect = (index: string) => {
  router.push(index);
};

onMounted(() => {
  const socket = io('http://localhost:5001');
  
  socket.on('manager:joined', (data) => {
    activeCount.value = data.active_employees?.length || 0;
  });
});
</script>

<style scoped>
.menu-badge {
  margin-left: 8px;
}
</style>
```

This provides a complete, production-ready navigation integration!

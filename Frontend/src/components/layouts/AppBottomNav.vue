<template>
  <nav class="app-bottom-nav">
    <button
      v-for="item in navItems"
      :key="item.route"
      :class="['nav-btn', { active: isActive(item.route) }]"
      @click="navigate(item.route)"
      aria-label="item.title"
    >
      <el-icon :size="22"><component :is="item.iconComponent" /></el-icon>
      <span class="nav-label">{{ item.title }}</span>
    </button>
  </nav>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";
import * as Icons from "@element-plus/icons-vue";
import { computed } from "vue";

const router = useRouter();
const route = useRoute();

// Minimal example, you can expand with more items or dynamic role-based
const navItems = [
  { title: "Dashboard", icon: "Odometer", route: "/admin/dashboard" },
  { title: "Employees", icon: "User", route: "/admin/employees" },
  { title: "Attendance", icon: "Clock", route: "/admin/attendance" },
  { title: "Payroll", icon: "Money", route: "/admin/payroll" },
  { title: "Settings", icon: "Setting", route: "/admin/settings" },
].map((item) => ({
  ...item,
  iconComponent: (Icons as any)[item.icon] || Icons.Menu,
}));

function isActive(path: string) {
  return route.path.startsWith(path);
}

function navigate(path: string) {
  if (route.path !== path) router.push(path);
}
</script>

<style scoped>
.app-bottom-nav {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 200;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: var(--sidebar-bg, #fff);
  border-top: 1px solid var(--sidebar-border, #eee);
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.04);
  height: 56px;
}
.nav-btn {
  flex: 1 1 0;
  background: none;
  border: none;
  outline: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--app-text, #333);
  font-size: 12px;
  padding: 0 2px;
  height: 100%;
  transition: color 0.18s;
}
.nav-btn.active {
  color: var(--app-primary, #ff52a1);
}
.nav-label {
  font-size: 11px;
  margin-top: 2px;
}
@media (min-width: 769px) {
  .app-bottom-nav {
    display: none;
  }
}
</style>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import AppSidebar from "~/components/layouts/AppSidebar.vue";
import AppHeader from "~/components/layouts/AppHeader.vue";
import AppFooter from "~/components/layouts/AppFooter.vue";
import schoolLogoLight from "~/assets/image/school-logo-light.jpg";

const route = useRoute();
const MOBILE_BREAKPOINT = 768;

/** Mobile drawer state */
const sidebarOpen = ref(false);

/** Desktop sidebar collapse state */
const sidebarCollapsed = ref(false);

function toggleSidebar() {
  // Toggle mobile drawer
  if (window.innerWidth < MOBILE_BREAKPOINT) {
    sidebarOpen.value = !sidebarOpen.value;
  } else {
    // Toggle desktop collapse
    sidebarCollapsed.value = !sidebarCollapsed.value;
  }
}

function closeSidebar() {
  sidebarOpen.value = false;
}

function syncSidebarStateByViewport() {
  const isMobile = window.innerWidth < MOBILE_BREAKPOINT;

  if (isMobile) {
    // Keep desktop sidebar expanded when returning from mobile.
    sidebarCollapsed.value = false;
  } else {
    // Ensure mobile drawer is closed on desktop.
    sidebarOpen.value = false;
  }
}

onMounted(() => {
  syncSidebarStateByViewport();
  window.addEventListener("resize", syncSidebarStateByViewport, {
    passive: true,
  });
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", syncSidebarStateByViewport);
});

/** Close drawer after navigation (mobile) */
watch(
  () => route.fullPath,
  () => closeSidebar(),
);
</script>

<template>
  <el-container class="app-layout">
    <!-- Sidebar: desktop only -->
    <el-aside
      v-if="!sidebarCollapsed"
      width="240px"
      class="layout-aside desktop-only"
      tabindex="0"
    >
      <AppSidebar
        :logoSrc="schoolLogoLight"
        :collapsed="sidebarCollapsed"
        @navigate="closeSidebar"
      />
    </el-aside>

    <!-- Mobile drawer popup -->
    <el-drawer
      v-model="sidebarOpen"
      direction="ltr"
      size="240px"
      :with-header="false"
      class="mobile-sidebar-drawer mobile-only"
      @close="closeSidebar"
    >
      <AppSidebar
        :logoSrc="schoolLogoLight"
        :collapsed="false"
        @navigate="closeSidebar"
      />
    </el-drawer>

    <!-- Main -->
    <el-container
      direction="vertical"
      :class="['layout-main-container', { 'sidebar-hidden': sidebarCollapsed }]"
    >
      <!-- Header can be hidden per-page using route.meta.noHeader -->
      <el-header v-if="!route.meta.noHeader" class="layout-header">
        <AppHeader
          :sidebar-collapsed="sidebarCollapsed"
          @toggle-sidebar="toggleSidebar"
        />
      </el-header>

      <el-main :key="route.fullPath" class="layout-main">
        <NuxtPage />
      </el-main>

      <el-footer v-if="!route.meta.noHeader" class="layout-footer">
        <AppFooter />
      </el-footer>
    </el-container>
  </el-container>
</template>

<style scoped>
/* ── layout.css handles background/border/padding via tokens ──
   This block only owns: positioning, animation, mobile state */

.layout-aside {
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  width: 240px;
  transform: translateX(0);
  opacity: 1;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s;
}

/* Auto-hide on collapse (desktop) */
.layout-aside:not(:hover):not(:focus-within).is-collapsed {
  transform: translateX(-220px);
  opacity: 0.1;
  pointer-events: none;
}

/* Desktop-only / mobile-only utilities */
.desktop-only { display: block; }
.mobile-only  { display: none; }

@media (max-width: 768px) {
  .layout-aside  { display: none !important; }
  .desktop-only  { display: none !important; }
  .mobile-only   { display: block !important; }
}

/* Mobile drawer: theme via real tokens */
:deep(.mobile-sidebar-drawer .el-drawer) {
  background: var(--sidebar-bg);
  border-right: 1px solid var(--sidebar-border);
  box-shadow: 0 18px 42px var(--card-shadow);
}
:deep(.mobile-sidebar-drawer .el-drawer__body) {
  padding: 0;
  background: var(--sidebar-bg);
}
:deep(.mobile-sidebar-drawer .el-overlay) {
  background: rgba(0, 0, 0, 0.35);
}
:deep(html[data-theme="dark"] .mobile-sidebar-drawer .el-overlay) {
  background: rgba(0, 0, 0, 0.55);
}

/* Main container shifts right to clear the fixed sidebar */
.layout-main-container {
  margin-left: 240px;
  transition: margin-left 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.layout-main-container.sidebar-hidden {
  margin-left: 0;
}
@media (max-width: 768px) {
  .layout-main-container {
    margin-left: 0 !important;
  }
}
</style>


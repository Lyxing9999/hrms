<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import {
  ArrowLeft,
  ArrowRight,
  Document,
  InfoFilled,
} from "@element-plus/icons-vue";

interface ShellStat {
  label: string;
  value: string;
  hint?: string;
}

interface ShellAction {
  title: string;
  description: string;
  route: string;
  icon?: any;
  color?: string;
  badge?: string;
}

interface ShellSection {
  title: string;
  items: string[];
  note?: string;
}

const props = withDefaults(
  defineProps<{
    title: string;
    description: string;
    backPath?: string;
    badge?: string;
    accent?: string;
    stats?: ShellStat[];
    actions?: ShellAction[];
    sections?: ShellSection[];
  }>(),
  {
    backPath: "",
    badge: "Prototype",
    accent: "var(--color-primary)",
    stats: () => [],
    actions: () => [],
    sections: () => [],
  },
);

const router = useRouter();

const accentStyle = computed(() => ({
  "--accent": props.accent,
}));

function goBack() {
  if (props.backPath) router.push(props.backPath);
}

function goTo(route: string) {
  router.push(route);
}
</script>

<template>
  <div class="prototype-shell" :style="accentStyle">
    <section class="hero-card">
      <div class="hero-top">
        <div>
          <el-tag type="success" effect="dark" class="hero-badge">
            {{ badge }}
          </el-tag>
          <h1 class="hero-title">{{ title }}</h1>
          <p class="hero-description">{{ description }}</p>
        </div>

        <el-button v-if="backPath" class="back-button" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          Back
        </el-button>
      </div>

      <div class="hero-meta">
        <div class="meta-pill">
          <el-icon><InfoFilled /></el-icon>
          <span>Aligned with the backend HRMS module map</span>
        </div>
        <div class="meta-pill meta-pill-strong">
          <el-icon><Document /></el-icon>
          <span>Demo pages only, wired for navigation</span>
        </div>
      </div>
    </section>

    <el-row :gutter="20" class="stats-grid">
      <el-col v-for="stat in stats" :key="stat.label" :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div v-if="stat.hint" class="stat-hint">{{ stat.hint }}</div>
        </el-card>
      </el-col>
    </el-row>

    <section v-if="actions.length" class="section-block">
      <div class="section-header">
        <h2>Quick Actions</h2>
        <span>Primary demo routes for this role</span>
      </div>

      <el-row :gutter="20">
        <el-col
          v-for="action in actions"
          :key="action.route"
          :xs="24"
          :sm="12"
          :lg="8"
          class="action-col"
        >
          <el-card
            class="action-card"
            shadow="hover"
            @click="goTo(action.route)"
          >
            <div class="action-row">
              <div
                class="action-icon"
                :style="{ backgroundColor: action.color || 'var(--accent)' }"
              >
                <el-icon :size="26" color="var(--color-light)">
                  <component :is="action.icon" />
                </el-icon>
              </div>

              <div class="action-copy">
                <div class="action-head">
                  <h3>{{ action.title }}</h3>
                  <el-tag v-if="action.badge" size="small" type="warning">{{
                    action.badge
                  }}</el-tag>
                </div>
                <p>{{ action.description }}</p>
              </div>

              <el-icon class="action-chevron"><ArrowRight /></el-icon>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </section>

    <section v-if="sections.length" class="section-grid">
      <el-card
        v-for="section in sections"
        :key="section.title"
        class="detail-card"
        shadow="never"
      >
        <div class="section-header compact">
          <h2>{{ section.title }}</h2>
          <span v-if="section.note">{{ section.note }}</span>
        </div>

        <ul class="detail-list">
          <li v-for="item in section.items" :key="item">{{ item }}</li>
        </ul>
      </el-card>
    </section>
  </div>
</template>

<style scoped>
.prototype-shell {
  display: grid;
  gap: 20px;
  padding: 20px;
  background: radial-gradient(
      circle at top right,
      color-mix(in srgb, var(--accent) 18%, transparent),
      transparent 32%
    ),
    linear-gradient(180deg, rgba(255, 255, 255, 0.82), var(--color-light));
}

.hero-card,
.stat-card,
.action-card,
.detail-card {
  border-radius: 20px;
  border: 1px solid
    color-mix(in srgb, var(--accent) 15%, var(--input-border) 85%);
  box-shadow: 0 18px 40px var(--card-shadow);
}

.hero-card {
  padding: 24px;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--accent) 88%, var(--color-bg) 12%),
    var(--color-bg)
  );
  color: var(--color-light);
}

.hero-top {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.hero-badge {
  margin-bottom: 14px;
}

.hero-title {
  margin: 0;
  font-size: clamp(28px, 3vw, 42px);
  line-height: 1.05;
}

.hero-description {
  margin: 10px 0 0;
  max-width: 720px;
  color: rgba(255, 255, 255, 0.82);
  font-size: 15px;
}

.back-button {
  border: 0;
  background: rgba(255, 255, 255, 0.14);
  color: var(--color-light);
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 18px;
}

.meta-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.86);
}

.meta-pill-strong {
  background: rgba(255, 255, 255, 0.2);
}

.stats-grid,
.section-block,
.section-grid {
  width: 100%;
}

.stat-card {
  height: 100%;
  background: rgba(255, 255, 255, 0.95);
}

.stat-value {
  font-size: 30px;
  font-weight: 800;
  color: var(--color-dark);
}

.stat-label {
  margin-top: 4px;
  font-weight: 650;
  color: var(--muted-color);
}

.stat-hint {
  margin-top: 8px;
  color: var(--muted-color);
  font-size: 13px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: baseline;
  margin-bottom: 14px;
}

.section-header h2 {
  margin: 0;
  font-size: 18px;
  color: var(--color-dark);
}

.section-header span {
  color: var(--muted-color);
  font-size: 13px;
}

.compact {
  margin-bottom: 12px;
}

.action-col {
  margin-bottom: 20px;
}

.action-card {
  cursor: pointer;
  min-height: 132px;
  transition: transform 180ms ease, box-shadow 180ms ease;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 44px
    color-mix(in srgb, var(--card-shadow) 1.75, transparent);
}

.action-row {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 14px;
  align-items: center;
}

.action-icon {
  width: 54px;
  height: 54px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.action-copy h3 {
  margin: 0;
  font-size: 16px;
  color: var(--color-dark);
}

.action-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.action-copy p {
  margin: 6px 0 0;
  color: var(--muted-color);
  font-size: 13px;
  line-height: 1.55;
}

.action-chevron {
  color: var(--muted-color);
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.detail-card {
  background: rgba(255, 255, 255, 0.92);
}

.detail-list {
  margin: 0;
  padding-left: 18px;
  display: grid;
  gap: 10px;
  color: var(--color-dark);
}

@media (max-width: 768px) {
  .prototype-shell {
    padding: 16px;
  }

  .hero-top,
  .action-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-row {
    grid-template-columns: auto 1fr;
  }

  .action-chevron {
    display: none;
  }
}
</style>

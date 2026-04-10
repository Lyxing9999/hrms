<script setup lang="ts">
import { computed, useSlots } from "vue";
import BaseInputSearch from "~/components/base/BaseInputSearch.vue";

type OverviewStat = {
  key?: string | number;
  value: number;
  singular?: string;
  plural?: string;
  label?: string;
  suffix?: string;
  prefix?: string;
  variant?: "primary" | "secondary";
  dotClass?: string;
};

const props = withDefaults(
  defineProps<{
    title: string;
    description?: string;

    // Search
    showSearch?: boolean;
    searchModelValue?: string;
    searchPlaceholder?: string;
    searchDisabled?: boolean;

    // Reset
    showReset?: boolean;
    resetLabel?: string;
    resetDisabled?: boolean;

    // Refresh
    showRefresh?: boolean;
    loading?: boolean;
    disabled?: boolean;
    refreshLabel?: string;

    stats?: OverviewStat[];
  }>(),
  {
    description: "",
    showSearch: false,
    searchModelValue: "",
    searchPlaceholder: "Search...",
    searchDisabled: false,
    showReset: false,
    resetLabel: "Reset",
    resetDisabled: false,
    showRefresh: false,
    loading: false,
    disabled: false,
    refreshLabel: "Refresh",
    stats: () => [],
  },
);

const slots = useSlots();

const emit = defineEmits<{
  (e: "refresh"): void;
  (e: "update:searchModelValue", value: string): void;
  (e: "reset"): void;
}>();

const searchValue = computed({
  get: () => props.searchModelValue,
  set: (v: string | number | null) =>
    emit("update:searchModelValue", String(v ?? "")),
});

const hasTopActions = computed(
  () => Boolean(slots.actions) || props.showRefresh,
);

const hasControlSection = computed(
  () => props.showSearch || props.showReset || Boolean(slots.filters),
);

const hasControlRow = computed(() => props.showSearch || props.showReset);

const hasStats = computed(
  () => (props.stats?.length ?? 0) > 0 || Boolean(slots["custom-stats"]),
);

function onReset() {
  emit("update:searchModelValue", "");
  emit("reset");
}

function pluralize(stat: {
  value: number;
  singular?: string;
  plural?: string;
  label?: string;
}) {
  if (stat.label) return stat.label;
  if (!stat.singular) return "";
  if (stat.value === 1) return stat.singular;
  return stat.plural ?? `${stat.singular}s`;
}
</script>

<template>
  <div class="overview-header mb-4 rounded-2xl border p-5 shadow-sm">
    <el-row :gutter="16" align="top" class="overview-top">
      <el-col
        :xs="24"
        :sm="hasTopActions ? 16 : 24"
        :md="hasTopActions ? 18 : 24"
      >
        <h1
          class="flex items-center gap-2 text-2xl font-bold text-[color:var(--color-dark)]"
        >
          {{ title }}
          <slot name="icon" />
        </h1>

        <p
          v-if="description"
          class="mt-1 text-sm text-[color:var(--color-primary-light-1)]"
        >
          {{ description }}
        </p>
      </el-col>

      <el-col v-if="hasTopActions" :xs="24" :sm="8" :md="6">
        <div class="overview-actions mt-3 sm:mt-0">
          <slot name="actions">
            <BaseButton
              v-if="showRefresh"
              plain
              class="w-full sm:w-auto overview-action-btn overview-action-btn--neutral"
              :loading="loading"
              :disabled="disabled"
              @click="emit('refresh')"
              aria-label="Refresh data"
            >
              {{ refreshLabel }}
            </BaseButton>
          </slot>
        </div>
      </el-col>
    </el-row>

    <div
      v-if="hasControlSection"
      class="mt-4 border-t border-[color:var(--color-primary-light-8)] pt-4"
    >
      <el-row v-if="hasControlRow" :gutter="12" align="middle">
        <el-col :xs="24" :sm="16" :md="12">
          <BaseInputSearch
            v-if="showSearch"
            v-model="searchValue"
            :placeholder="searchPlaceholder"
            :disabled="searchDisabled"
            :auto-search="true"
            :debounce="350"
            :ignore-empty="false"
            @search="emit('refresh')"
          />
        </el-col>

        <el-col :xs="24" :sm="8" :md="4">
          <BaseButton
            v-if="showReset"
            plain
            class="w-full sm:w-auto overview-action-btn overview-action-btn--neutral"
            :disabled="disabled || resetDisabled"
            @click="onReset"
            aria-label="Reset filters"
          >
            {{ resetLabel }}
          </BaseButton>
        </el-col>
      </el-row>

      <div v-if="$slots.filters" class="mt-3">
        <slot name="filters" />
      </div>
    </div>

    <div v-if="hasStats" class="mt-4">
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <template
          v-for="(stat, index) in stats"
          :key="stat.key ?? stat.label ?? index"
        >
          <span
            v-if="stat.variant === 'primary'"
            class="inline-flex items-center gap-1 rounded-full bg-[var(--color-primary-light-8)] text-[color:var(--color-primary)] px-3 py-0.5 border border-[var(--color-primary-light-5)]"
          >
            <span class="w-1.5 h-1.5 rounded-full bg-[var(--color-primary)]" />
            {{ stat.value }} {{ pluralize(stat) }}
          </span>

          <span v-else class="stat-pill stat-pill--secondary">
            <span
              class="w-1.5 h-1.5 rounded-full"
              :class="stat.dotClass ?? 'bg-emerald-500'"
            />
            <span v-if="stat.prefix">{{ stat.prefix }}</span>
            <span>{{ stat.value }} {{ pluralize(stat) }}</span>
            <span v-if="stat.suffix">{{ stat.suffix }}</span>
          </span>
        </template>
      </div>

      <div v-if="$slots['custom-stats']" class="mt-2">
        <slot name="custom-stats" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.overview-header {
  background: linear-gradient(
    to right,
    var(--color-primary-light-9),
    var(--color-primary-light-9)
  );
  border-color: var(--color-primary-light-9);
}

.overview-top :deep(.el-col) {
  min-width: 0;
}

.overview-actions {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

@media (min-width: 640px) {
  .overview-actions {
    justify-content: flex-end;
  }
}

.overview-actions :deep(.el-button),
.overview-action-btn {
  min-height: 36px;
  border-radius: 10px;
  font-weight: 650;
}

.overview-action-btn {
  border-radius: 10px;
  font-weight: 650;

  border: 1px solid
    color-mix(in srgb, var(--border-color) 70%, var(--color-primary) 30%) !important;
  color: color-mix(
    in srgb,
    var(--text-color) 78%,
    var(--muted-color) 22%
  ) !important;
  background: color-mix(
    in srgb,
    var(--color-card) 92%,
    var(--color-bg) 8%
  ) !important;

  transition: background-color var(--transition-base),
    border-color var(--transition-base), color var(--transition-base),
    transform var(--transition-base);
}

.overview-action-btn:hover:not(.is-disabled):not([disabled]) {
  background: var(--hover-bg) !important;
  border-color: color-mix(
    in srgb,
    var(--border-color) 55%,
    var(--color-primary) 45%
  ) !important;
  color: var(--text-color) !important;
  transform: translateY(-0.5px);
}

.overview-action-btn:active:not(.is-disabled):not([disabled]) {
  transform: translateY(0);
}

.overview-action-btn.is-disabled,
.overview-action-btn[disabled],
.overview-action-btn:disabled {
  background: color-mix(
    in srgb,
    var(--color-card) 75%,
    var(--color-bg) 25%
  ) !important;
  border-color: color-mix(
    in srgb,
    var(--border-color) 92%,
    transparent
  ) !important;
  color: color-mix(in srgb, var(--muted-color) 85%, transparent) !important;

  opacity: 1 !important;
  cursor: not-allowed !important;
  transform: none !important;
}

html[data-theme="dark"] .overview-action-btn {
  background: color-mix(
    in srgb,
    var(--color-card) 88%,
    var(--color-bg) 12%
  ) !important;
  border-color: color-mix(
    in srgb,
    var(--border-color) 78%,
    var(--color-primary) 22%
  ) !important;
}

html[data-theme="dark"] .overview-action-btn.is-disabled,
html[data-theme="dark"] .overview-action-btn[disabled],
html[data-theme="dark"] .overview-action-btn:disabled {
  background: color-mix(
    in srgb,
    var(--color-card) 92%,
    var(--color-bg) 8%
  ) !important;
  border-color: color-mix(
    in srgb,
    var(--border-color) 92%,
    transparent
  ) !important;
  color: color-mix(in srgb, var(--muted-color) 82%, transparent) !important;
}

.stat-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem; /* gap-1 */
  padding: 0.125rem 0.75rem; /* py-0.5 px-3 */
  border-radius: 999px;
  border: 1px solid transparent;
  min-width: 0;
  white-space: nowrap;
}

.stat-pill--secondary {
  background: color-mix(in srgb, var(--color-card) 92%, var(--color-bg) 8%);
  border-color: color-mix(in srgb, var(--border-color) 70%, transparent);
  color: color-mix(in srgb, var(--text-color) 84%, var(--muted-color) 16%);

  transition: background-color var(--transition-base),
    border-color var(--transition-base), color var(--transition-base);
}

.stat-pill--secondary:hover {
  background: var(--hover-bg);
  border-color: color-mix(
    in srgb,
    var(--border-color) 55%,
    var(--color-primary) 45%
  );
  color: var(--text-color);
}
</style>

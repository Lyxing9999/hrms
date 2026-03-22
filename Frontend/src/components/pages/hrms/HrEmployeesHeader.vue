<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  loading: boolean;
  stats: any;
  isDirty: boolean;
  searchModelValue: string;
  hasAccount: "" | "yes" | "no";
  employeeStatus: "" | "active" | "inactive";
}>();

const emit = defineEmits<{
  (e: "update:searchModelValue", v: string): void;
  (e: "update:hasAccount", v: "" | "yes" | "no"): void;
  (e: "update:employeeStatus", v: "" | "active" | "inactive"): void;
  (e: "refresh"): void;
  (e: "reset"): void;
  (e: "open-create"): void;
}>();

const searchModel = computed({
  get: () => props.searchModelValue,
  set: (v: string) => emit("update:searchModelValue", v),
});

const hasAccountModel = computed({
  get: () => props.hasAccount,
  set: (v: "" | "yes" | "no") => emit("update:hasAccount", v),
});

const employeeStatusModel = computed({
  get: () => props.employeeStatus,
  set: (v: "" | "active" | "inactive") => emit("update:employeeStatus", v),
});
</script>

<template>
  <OverviewHeader
    title="Employees"
    description="Manage employees and linked login accounts."
    :loading="loading"
    :stats="stats"
    :show-refresh="true"
    :show-search="true"
    :show-reset="true"
    :reset-disabled="!isDirty"
    :search-model-value="searchModel"
    @update:searchModelValue="searchModel = $event"
    @refresh="emit('refresh')"
    @reset="emit('reset')"
  >
    <template #filters>
      <el-row :gutter="12" align="middle" class="w-full">
        <el-col :xs="24" :md="12">
          <el-select v-model="hasAccountModel" class="w-full" clearable>
            <el-option label="All accounts" value="" />
            <el-option label="Has account" value="yes" />
            <el-option label="No account" value="no" />
          </el-select>
        </el-col>

        <el-col :xs="24" :md="12">
          <el-select v-model="employeeStatusModel" class="w-full" clearable>
            <el-option label="All statuses" value="" />
            <el-option label="Active" value="active" />
            <el-option label="Inactive" value="inactive" />
          </el-select>
        </el-col>
      </el-row>
    </template>

    <template #actions>
      <BaseButton plain :loading="loading" @click="emit('refresh')">
        Refresh
      </BaseButton>

      <BaseButton
        type="primary"
        :disabled="loading"
        @click="emit('open-create')"
      >
        Add Employee
      </BaseButton>
    </template>
  </OverviewHeader>
</template>

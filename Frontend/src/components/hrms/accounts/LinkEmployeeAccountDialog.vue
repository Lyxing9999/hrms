<script setup lang="ts">
import { computed, ref, watch } from "vue";
import {
  ElAlert,
  ElDialog,
  ElInput,
  ElButton,
  ElTable,
  ElTableColumn,
  ElEmpty,
  ElSkeleton,
  ElTag,
} from "element-plus";
import type { HrEmployeeDTO } from "~/api/hr_admin/employees/dto";

const props = defineProps<{
  visible: boolean;
  loading?: boolean;
  activeEmployeeId?: string | null;
  employees: HrEmployeeDTO[];
  selectedAccountLabel?: string;
  selectedAccountRole?: string;
  canLinkSelectedAccount?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:visible", value: boolean): void;
  (e: "select", employee: HrEmployeeDTO): void;
  (e: "search", keyword: string): void;
  (e: "close"): void;
}>();

const keyword = ref("");

watch(
  () => props.visible,
  (v) => {
    if (!v) keyword.value = "";
  },
);

const filteredEmployees = computed(() => props.employees ?? []);
const accountLabel = computed(() => props.selectedAccountLabel?.trim() || "-");
const accountRole = computed(() => props.selectedAccountRole?.trim() || "-");
const canLinkSelectedAccount = computed(
  () => props.canLinkSelectedAccount ?? true,
);
const roleTagType = computed(() =>
  canLinkSelectedAccount.value ? "success" : "danger",
);
const roleDescription = computed(() => {
  if (canLinkSelectedAccount.value) {
    return "This account role is allowed to be linked to an employee.";
  }

  return "Backend rules allow linking only employee, manager, and payroll manager accounts.";
});

const emptyDescription = computed(() => {
  if (props.loading) return "Loading employees who can be linked...";
  if (keyword.value.trim()) return "No employees matched your search.";
  return "No unlinked employees are available right now.";
});

function closeDialog() {
  emit("update:visible", false);
  emit("close");
}

function handleSearch() {
  emit("search", keyword.value.trim());
}

function resetSearch() {
  keyword.value = "";
  emit("search", "");
}
</script>

<template>
  <ElDialog
    :model-value="visible"
    title="Link Employee Account"
    width="920px"
    destroy-on-close
    @close="closeDialog"
  >
    <div class="space-y-4">
      <ElAlert type="info" show-icon :closable="false">
        <template #title>Link the selected account to an employee</template>
        <template #default>
          <div class="text-sm leading-6">
            <div>
              Selected account:
              <span class="font-semibold text-[var(--text-color)]">
                {{ accountLabel }}
              </span>
            </div>
            <div class="mt-1 flex flex-wrap items-center gap-2">
              <span class="text-[var(--muted-color)]">Role:</span>
              <ElTag :type="roleTagType" effect="plain" size="small">
                {{ accountRole }}
              </ElTag>
            </div>
            <div class="text-[var(--muted-color)]">
              {{ roleDescription }}
            </div>
          </div>
        </template>
      </ElAlert>

      <div class="flex flex-col gap-2 sm:flex-row">
        <ElInput
          v-model="keyword"
          placeholder="Search employee by code, name, department..."
          clearable
          class="flex-1"
          @keyup.enter="handleSearch"
        />
        <div class="flex gap-2">
          <ElButton :disabled="loading" @click="handleSearch">Search</ElButton>
          <ElButton plain :disabled="loading && !keyword" @click="resetSearch">
            Reset
          </ElButton>
        </div>
      </div>

      <div
        v-if="loading"
        class="rounded-lg border border-[var(--border-color)] p-4"
      >
        <ElSkeleton animated :rows="5" />
      </div>

      <template v-else>
        <ElTable
          v-if="filteredEmployees.length > 0"
          :data="filteredEmployees"
          height="420"
        >
          <ElTableColumn
            prop="employee_code"
            label="Employee Code"
            min-width="140"
          />
          <ElTableColumn prop="full_name" label="Full Name" min-width="180" />
          <ElTableColumn prop="department" label="Department" min-width="140" />
          <ElTableColumn prop="position" label="Position" min-width="140" />
          <ElTableColumn label="Status" width="120" align="center">
            <template #default="{ row }">
              <ElTag type="success" effect="plain" size="small">
                Available
              </ElTag>
            </template>
          </ElTableColumn>
          <ElTableColumn label="Operation" width="170" align="center">
            <template #default="{ row }">
              <ElButton
                type="primary"
                size="small"
                :loading="activeEmployeeId === row.id"
                :disabled="!!activeEmployeeId && activeEmployeeId !== row.id"
                @click="emit('select', row)"
              >
                Link to this employee
              </ElButton>
            </template>
          </ElTableColumn>
        </ElTable>

        <ElEmpty v-else :description="emptyDescription" />
      </template>
    </div>
  </ElDialog>
</template>

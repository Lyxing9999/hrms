<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { ElMessageBox } from "element-plus";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { ColumnConfig } from "~/components/types/tableEdit";
import { hrmsAdminService } from "~/api/hr_admin";
import type {
  DeductionRuleCreateDTO,
  DeductionRuleDTO,
  DeductionRuleType,
  DeductionRuleUpdateDTO,
} from "~/api/hr_admin/deduction";
import { useMessage } from "~/composables/common/useMessage";

definePageMeta({ layout: "default" });

type RuleFilter = "active" | "deleted" | "all";
type RuleStatusFilter = "all" | "active" | "inactive";

interface RuleFormModel {
  type: DeductionRuleType;
  min_minutes: number | null;
  max_minutes: number | null;
  deduction_percentage: number | null;
  is_active: boolean;
}

const deductionRuleService = hrmsAdminService().deductionRule;
const { showInfo } = useMessage();

const rules = ref<DeductionRuleDTO[]>([]);
const loading = ref(false);
const saving = ref(false);
const rowLoading = ref<Record<string, boolean>>({});
const statusLoading = ref<Record<string, boolean>>({});

const dialogVisible = ref(false);
const dialogMode = ref<"create" | "edit">("create");
const currentRuleId = ref<string>("");
const initialFormValues = ref<RuleFormModel | null>(null);

const q = ref("");
const typeFilter = ref<"all" | DeductionRuleType>("all");
const statusFilter = ref<RuleStatusFilter>("all");
const lifecycleFilter = ref<RuleFilter>("active");
const page = ref(1);
const pageSize = ref(10);

const checkingApplicable = ref(false);
const applicableType = ref<DeductionRuleType>("late");
const applicableMinutes = ref<number | null>(null);
const applicableResult = ref<DeductionRuleDTO | null>(null);
const applicableChecked = ref(false);
const applicableLastCheckedAt = ref<string | null>(null);

const selectedTypeActiveRules = computed(() => {
  return rules.value
    .filter(
      (item) =>
        !item.lifecycle?.deleted_at &&
        item.is_active &&
        item.type === applicableType.value,
    )
    .sort((a, b) => a.min_minutes - b.min_minutes);
});

const checkerSummaryCards = computed(() => {
  const list = selectedTypeActiveRules.value;
  const openEnded = list.filter((item) => item.max_minutes == null).length;
  const maxDeduction = list.reduce(
    (acc, item) =>
      item.deduction_percentage > acc ? item.deduction_percentage : acc,
    0,
  );
  const firstRangeStart = list.length ? list[0].min_minutes : null;
  const lastRange = list.length ? list[list.length - 1] : null;
  const coverageRange =
    firstRangeStart == null
      ? "-"
      : `${firstRangeStart} - ${
          lastRange?.max_minutes == null ? "infinite" : lastRange.max_minutes
        } mins`;

  return [
    {
      label: "Rules in scope",
      value: String(list.length),
    },
    {
      label: "Coverage",
      value: coverageRange,
    },
    {
      label: "Max deduction",
      value: list.length ? `${maxDeduction}%` : "-",
    },
    {
      label: "Open-ended",
      value: String(openEnded),
    },
    {
      label: "Last check",
      value: applicableLastCheckedAt.value ?? "Not checked",
    },
  ];
});

const nearestApplicableHint = computed(() => {
  if (applicableMinutes.value == null || applicableMinutes.value < 0) {
    return "Enter a minute value to test applicability.";
  }

  const mins = Number(applicableMinutes.value);
  const list = selectedTypeActiveRules.value;

  if (!list.length) {
    return "No active rules exist for the selected type.";
  }

  const hasCoverage = list.some(
    (item) =>
      mins >= item.min_minutes &&
      (item.max_minutes == null || mins <= item.max_minutes),
  );

  if (hasCoverage) {
    return "This minute value is within at least one active range.";
  }

  const nextRange = list.find((item) => mins < item.min_minutes);
  if (nextRange) {
    return `Next configured range starts at ${nextRange.min_minutes} minutes.`;
  }

  const lastRange = list[list.length - 1];
  return `No open-ended range is configured after ${
    lastRange.max_minutes ?? lastRange.min_minutes
  } minutes.`;
});

const form = reactive<RuleFormModel>(getDefaultForm());

const ruleTypeOptions: Array<{ label: string; value: DeductionRuleType }> = [
  { label: "Late", value: "late" },
  { label: "Early Leave", value: "early_leave" },
  { label: "Absent", value: "absent" },
];

const tableColumns: ColumnConfig<DeductionRuleDTO>[] = [
  {
    field: "type",
    label: "Type",
    width: "140px",
    useSlot: true,
    slotName: "type",
  },
  {
    field: "min_minutes",
    label: "Minute Range",
    minWidth: "200px",
    useSlot: true,
    slotName: "range",
  },
  {
    field: "deduction_percentage",
    label: "Deduction",
    width: "170px",
    useSlot: true,
    slotName: "deduction",
  },
  {
    field: "is_active",
    label: "Status",
    width: "170px",
    useSlot: true,
    slotName: "status",
  },
  {
    field: "lifecycle",
    label: "Updated",
    width: "190px",
    useSlot: true,
    slotName: "updated_at",
  },
  {
    field: "id",
    label: "Actions",
    operation: true,
    width: "220px",
    fixed: "right",
    useSlot: true,
    slotName: "operation",
  },
];

const summaryCards = computed(() => {
  const active = rules.value.filter((item) => !item.lifecycle?.deleted_at);
  const inactive = active.filter((item) => !item.is_active);
  const deleted = rules.value.filter((item) => item.lifecycle?.deleted_at);
  const highest = active.reduce(
    (acc, curr) =>
      curr.deduction_percentage > acc.deduction_percentage ? curr : acc,
    active[0] ?? null,
  );

  return [
    { label: "Total rules", value: rules.value.length },
    { label: "Active records", value: active.length },
    { label: "Inactive", value: inactive.length },
    { label: "Deleted", value: deleted.length },
    {
      label: "Highest deduction",
      value: highest ? `${highest.deduction_percentage}%` : "-",
    },
  ];
});

const filteredRules = computed(() => {
  const keyword = q.value.trim().toLowerCase();

  return rules.value
    .filter((item) => {
      const isDeleted = Boolean(item.lifecycle?.deleted_at);

      if (lifecycleFilter.value === "active" && isDeleted) return false;
      if (lifecycleFilter.value === "deleted" && !isDeleted) return false;

      if (typeFilter.value !== "all" && item.type !== typeFilter.value) {
        return false;
      }

      if (statusFilter.value === "active" && !item.is_active) return false;
      if (statusFilter.value === "inactive" && item.is_active) return false;

      if (!keyword) return true;

      const searchableText = [
        formatRuleType(item.type),
        String(item.min_minutes),
        String(item.max_minutes ?? "no-limit"),
        String(item.deduction_percentage),
      ]
        .join(" ")
        .toLowerCase();

      return searchableText.includes(keyword);
    })
    .sort((a, b) => {
      if (a.type !== b.type) return a.type.localeCompare(b.type);
      return a.min_minutes - b.min_minutes;
    });
});

const totalRows = computed(() => filteredRules.value.length);

const pagedRules = computed(() => {
  const start = (page.value - 1) * pageSize.value;
  return filteredRules.value.slice(start, start + pageSize.value);
});

const formError = computed(() => {
  if (!form.type) return "Rule type is required.";

  if (form.min_minutes == null || form.min_minutes < 0) {
    return "Minimum minutes must be 0 or greater.";
  }

  if (form.max_minutes != null && form.max_minutes < form.min_minutes) {
    return "Maximum minutes must be greater than or equal to minimum minutes.";
  }

  if (
    form.deduction_percentage == null ||
    form.deduction_percentage < 0 ||
    form.deduction_percentage > 100
  ) {
    return "Deduction percentage must be between 0 and 100.";
  }

  return "";
});

const hasFormChanged = computed(() => {
  if (!initialFormValues.value) return false;
  return JSON.stringify(form) !== JSON.stringify(initialFormValues.value);
});

const canSubmitForm = computed(() => {
  if (formError.value) return false;
  return dialogMode.value === "create" ? true : hasFormChanged.value;
});

function getDefaultForm(): RuleFormModel {
  return {
    type: "late",
    min_minutes: 0,
    max_minutes: null,
    deduction_percentage: 0,
    is_active: true,
  };
}

function resetForm() {
  Object.assign(form, getDefaultForm());
  initialFormValues.value = null;
}

function fillForm(rule: DeductionRuleDTO) {
  const normalized: RuleFormModel = {
    type: (rule.type as DeductionRuleType) ?? "late",
    min_minutes: rule.min_minutes,
    max_minutes: rule.max_minutes,
    deduction_percentage: rule.deduction_percentage,
    is_active: rule.is_active,
  };
  Object.assign(form, normalized);
  initialFormValues.value = { ...normalized };
}

function formatRuleType(type: string): string {
  const map: Record<string, string> = {
    late: "Late",
    early_leave: "Early Leave",
    absent: "Absent",
  };
  return map[type] ?? type;
}

function formatMinuteRange(rule: DeductionRuleDTO): string {
  if (rule.max_minutes == null) {
    return `${rule.min_minutes}+ minutes`;
  }
  return `${rule.min_minutes} - ${rule.max_minutes} minutes`;
}

function formatDate(value?: string | null): string {
  if (!value) return "-";
  try {
    return new Intl.DateTimeFormat("en-GB", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(value));
  } catch {
    return "-";
  }
}

function formatCheckedAt(date: Date): string {
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(date);
}

async function loadRules() {
  loading.value = true;
  try {
    const response = await deductionRuleService.getRules({
      page: 1,
      limit: 500,
      include_deleted: true,
    });
    rules.value = response.items ?? [];

    if (
      (page.value - 1) * pageSize.value >= totalRows.value &&
      page.value > 1
    ) {
      page.value = Math.max(1, Math.ceil(totalRows.value / pageSize.value));
    }
  } catch {
  } finally {
    loading.value = false;
  }
}

function openCreateDialog() {
  dialogMode.value = "create";
  currentRuleId.value = "";
  resetForm();
  dialogVisible.value = true;
}

async function openEditDialog(rule: DeductionRuleDTO) {
  try {
    rowLoading.value[rule.id] = true;
    const detail = await deductionRuleService.getRule(rule.id);
    dialogMode.value = "edit";
    currentRuleId.value = rule.id;
    fillForm(detail);
    dialogVisible.value = true;
  } catch {
  } finally {
    rowLoading.value[rule.id] = false;
  }
}

function closeDialog() {
  dialogVisible.value = false;
  currentRuleId.value = "";
  resetForm();
}

async function submitForm() {
  if (!canSubmitForm.value) return;

  saving.value = true;
  try {
    if (dialogMode.value === "create") {
      const payload: DeductionRuleCreateDTO = {
        type: form.type,
        min_minutes: Number(form.min_minutes),
        max_minutes: form.max_minutes,
        deduction_percentage: Number(form.deduction_percentage),
        is_active: form.is_active,
      };
      await deductionRuleService.createRule(payload);
    } else {
      const payload: DeductionRuleUpdateDTO = {
        min_minutes: form.min_minutes,
        max_minutes: form.max_minutes,
        deduction_percentage: form.deduction_percentage,
        is_active: form.is_active,
      };
      await deductionRuleService.updateRule(currentRuleId.value, payload);
    }

    closeDialog();
    await loadRules();
  } catch {
  } finally {
    saving.value = false;
  }
}

async function confirmDelete(rule: DeductionRuleDTO) {
  try {
    await ElMessageBox.confirm(
      `Delete ${formatRuleType(rule.type)} rule ${formatMinuteRange(rule)}?`,
      "Delete deduction rule",
      {
        type: "warning",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      },
    );

    rowLoading.value[rule.id] = true;
    await deductionRuleService.deleteRule(rule.id);
    await loadRules();
  } catch (error: any) {
    if (error !== "cancel") {
      // Error notification is already handled by the service layer.
    }
  } finally {
    rowLoading.value[rule.id] = false;
  }
}

async function confirmRestore(rule: DeductionRuleDTO) {
  try {
    await ElMessageBox.confirm(
      `Restore ${formatRuleType(rule.type)} rule ${formatMinuteRange(rule)}?`,
      "Restore deduction rule",
      {
        type: "info",
        confirmButtonText: "Restore",
        cancelButtonText: "Cancel",
      },
    );

    rowLoading.value[rule.id] = true;
    await deductionRuleService.restoreRule(rule.id);
    await loadRules();
  } finally {
    rowLoading.value[rule.id] = false;
  }
}

async function toggleRuleStatus(rule: DeductionRuleDTO) {
  const previousValue = rule.is_active;
  rule.is_active = !previousValue;

  try {
    statusLoading.value[rule.id] = true;
    await deductionRuleService.updateRule(rule.id, {
      is_active: rule.is_active,
    });
  } catch {
    rule.is_active = previousValue;
  } finally {
    statusLoading.value[rule.id] = false;
  }
}

async function checkApplicableRule() {
  if (applicableMinutes.value == null || applicableMinutes.value < 0) {
    showInfo("Enter a valid minute value to test applicability.");
    return;
  }

  checkingApplicable.value = true;
  applicableChecked.value = false;
  applicableResult.value = null;

  try {
    const result = await deductionRuleService.getApplicableRule({
      type: applicableType.value,
      minutes: Number(applicableMinutes.value),
    });

    applicableResult.value = result;
    applicableChecked.value = true;
    applicableLastCheckedAt.value = formatCheckedAt(new Date());
  } catch {
  } finally {
    checkingApplicable.value = false;
  }
}

function onFilterChange() {
  page.value = 1;
}

onMounted(async () => {
  await loadRules();
});
</script>
<template>
  <div class="deduction-rules-page">
    <OverviewHeader
      :title="'Deduction Rules'"
      :description="'Configure deduction rules for lateness, early leave, and absence. Review ranges, activation status, and rule coverage in one place.'"
      :backPath="'/hr/config'"
    >
      <template #actions>
        <div class="header-actions">
          <BaseButton
            plain
            :loading="loading"
            class="!border-[color:var(--color-primary)] !text-[color:var(--color-primary)] hover:!bg-[var(--color-primary-light-7)]"
            @click="loadRules"
          >
            Refresh
          </BaseButton>

          <BaseButton
            type="primary"
            :disabled="loading"
            @click="openCreateDialog"
          >
            Add Rule
          </BaseButton>
        </div>
      </template>
    </OverviewHeader>

    <div class="summary-grid">
      <div v-for="item in summaryCards" :key="item.label" class="summary-card">
        <div class="summary-label">{{ item.label }}</div>
        <div class="summary-value">{{ item.value }}</div>
      </div>
    </div>

    <div class="content-grid">
      <section class="table-section">
        <div class="toolbar">
          <el-input
            v-model="q"
            clearable
            placeholder="Search by type, range, or percentage"
            @input="onFilterChange"
            @clear="onFilterChange"
          />

          <el-select v-model="typeFilter" @change="onFilterChange">
            <el-option label="All Types" value="all" />
            <el-option
              v-for="item in ruleTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>

          <el-select v-model="statusFilter" @change="onFilterChange">
            <el-option label="All Status" value="all" />
            <el-option label="Active" value="active" />
            <el-option label="Inactive" value="inactive" />
          </el-select>

          <div class="lifecycle-filter">
            <el-segmented
              v-model="lifecycleFilter"
              :options="[
                { label: 'Active', value: 'active' },
                { label: 'Deleted', value: 'deleted' },
                { label: 'All', value: 'all' },
              ]"
              @change="onFilterChange"
            />
          </div>
        </div>

        <div class="table-card">
          <SmartTable
            :columns="tableColumns"
            :data="pagedRules"
            :loading="loading"
            :total="totalRows"
            :page="page"
            :page-size="pageSize"
            @page="page = $event"
            @page-size="pageSize = $event"
          >
            <template #type="{ row }">
              <el-tag size="small" type="info">
                {{ formatRuleType((row as DeductionRuleDTO).type) }}
              </el-tag>
            </template>

            <template #range="{ row }">
              {{ formatMinuteRange(row as DeductionRuleDTO) }}
            </template>

            <template #deduction="{ row }">
              <div class="deduction-meter">
                <el-progress
                  :stroke-width="8"
                  :percentage="Number((row as DeductionRuleDTO).deduction_percentage)"
                  :show-text="false"
                />
                <span class="deduction-value">
                  {{ (row as DeductionRuleDTO).deduction_percentage }}%
                </span>
              </div>
            </template>

            <template #status="{ row }">
              <div class="status-wrap">
                <el-switch
                  :model-value="(row as DeductionRuleDTO).is_active"
                  :disabled="Boolean((row as DeductionRuleDTO).lifecycle?.deleted_at)"
                  :loading="statusLoading[(row as DeductionRuleDTO).id]"
                  @change="toggleRuleStatus(row as DeductionRuleDTO)"
                />
                <el-tag
                  :type="(row as DeductionRuleDTO).lifecycle?.deleted_at ? 'danger' : (row as DeductionRuleDTO).is_active ? 'success' : 'warning'"
                  size="small"
                >
                  {{
                    (row as DeductionRuleDTO).lifecycle?.deleted_at
                      ? "Deleted"
                      : (row as DeductionRuleDTO).is_active
                      ? "Active"
                      : "Inactive"
                  }}
                </el-tag>
              </div>
            </template>

            <template #updated_at="{ row }">
              {{ formatDate((row as DeductionRuleDTO).lifecycle?.updated_at) }}
            </template>

            <template #operation="{ row }">
              <el-space wrap>
                <el-button
                  v-if="!(row as DeductionRuleDTO).lifecycle?.deleted_at"
                  type="primary"
                  link
                  size="small"
                  :loading="rowLoading[(row as DeductionRuleDTO).id]"
                  @click="openEditDialog(row as DeductionRuleDTO)"
                >
                  Edit
                </el-button>

                <el-button
                  v-if="(row as DeductionRuleDTO).lifecycle?.deleted_at"
                  type="success"
                  link
                  size="small"
                  :loading="rowLoading[(row as DeductionRuleDTO).id]"
                  @click="confirmRestore(row as DeductionRuleDTO)"
                >
                  Restore
                </el-button>

                <el-button
                  v-else
                  type="danger"
                  link
                  size="small"
                  :loading="rowLoading[(row as DeductionRuleDTO).id]"
                  @click="confirmDelete(row as DeductionRuleDTO)"
                >
                  Delete
                </el-button>
              </el-space>
            </template>
          </SmartTable>

          <div v-if="!loading && totalRows === 0" class="empty-state">
            <div class="empty-title">No deduction rules found</div>
            <div class="empty-text">
              Try adjusting the filters or create a new deduction rule.
            </div>
          </div>
        </div>
      </section>

      <aside class="applicable-panel">
        <div class="panel-header">
          <h3>Applicable Rule Checker</h3>
          <p>
            Check which deduction rule matches a selected type and number of
            minutes.
          </p>
        </div>

        <div class="checker-summary-grid">
          <div
            v-for="item in checkerSummaryCards"
            :key="item.label"
            class="checker-summary-card"
          >
            <div class="checker-summary-label">{{ item.label }}</div>
            <div class="checker-summary-value">{{ item.value }}</div>
          </div>
        </div>

        <el-form label-position="top" class="checker-form">
          <el-form-item label="Rule Type">
            <el-select v-model="applicableType" class="w-full">
              <el-option
                v-for="item in ruleTypeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="Minutes">
            <el-input-number
              v-model="applicableMinutes"
              :min="0"
              :step="1"
              class="w-full"
            />
          </el-form-item>

          <BaseButton
            type="primary"
            :loading="checkingApplicable"
            class="checker-submit"
            @click="checkApplicableRule"
          >
            Check Applicable Rule
          </BaseButton>
        </el-form>

        <el-alert
          :title="nearestApplicableHint"
          type="info"
          :closable="false"
          show-icon
        />

        <div v-if="applicableChecked" class="applicable-result">
          <template v-if="applicableResult">
            <el-alert
              title="Matching rule found"
              type="success"
              :closable="false"
              show-icon
            />
            <div class="result-grid">
              <div class="result-item">
                <span class="result-label">Type</span>
                <strong>{{ formatRuleType(applicableResult.type) }}</strong>
              </div>
              <div class="result-item">
                <span class="result-label">Range</span>
                <strong>{{ formatMinuteRange(applicableResult) }}</strong>
              </div>
              <div class="result-item">
                <span class="result-label">Deduction</span>
                <strong>{{ applicableResult.deduction_percentage }}%</strong>
              </div>
              <div class="result-item">
                <span class="result-label">Status</span>
                <strong>{{
                  applicableResult.is_active ? "Active" : "Inactive"
                }}</strong>
              </div>
            </div>
          </template>

          <template v-else>
            <el-alert
              title="No rule matched"
              type="warning"
              :closable="false"
              show-icon
            />
          </template>
        </div>
      </aside>
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="
        dialogMode === 'create' ? 'Add Deduction Rule' : 'Edit Deduction Rule'
      "
      width="620px"
      destroy-on-close
      @closed="closeDialog"
    >
      <el-form label-position="top">
        <el-form-item label="Rule Type" required>
          <el-select
            v-model="form.type"
            :disabled="dialogMode === 'edit'"
            class="w-full"
          >
            <el-option
              v-for="item in ruleTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <div v-if="dialogMode === 'edit'" class="field-hint">
            Type is fixed after creation. Create a new rule if you need another
            type.
          </div>
        </el-form-item>

        <div class="range-grid">
          <el-form-item label="Minimum Minutes" required>
            <el-input-number
              v-model="form.min_minutes"
              :min="0"
              :step="1"
              class="w-full"
            />
          </el-form-item>

          <el-form-item label="Maximum Minutes">
            <el-input-number
              v-model="form.max_minutes"
              :min="0"
              :step="1"
              :placeholder="'Optional'"
              class="w-full"
            />
            <div class="field-hint">
              Leave empty for an open-ended range, such as 60+ minutes.
            </div>
          </el-form-item>
        </div>

        <el-form-item label="Deduction Percentage" required>
          <div class="percentage-editor">
            <el-slider
              v-model="form.deduction_percentage"
              :min="0"
              :max="100"
              :step="1"
            />
            <el-input-number
              v-model="form.deduction_percentage"
              :min="0"
              :max="100"
              :step="1"
            />
          </div>
        </el-form-item>

        <el-form-item label="Rule Active">
          <el-switch v-model="form.is_active" />
        </el-form-item>

        <el-alert
          v-if="formError"
          :title="formError"
          type="error"
          :closable="false"
          class="mb-2"
        />
      </el-form>

      <template #footer>
        <el-space>
          <BaseButton plain @click="closeDialog">Cancel</BaseButton>
          <BaseButton
            type="primary"
            :loading="saving"
            :disabled="!canSubmitForm"
            @click="submitForm"
          >
            {{ dialogMode === "create" ? "Create Rule" : "Save Changes" }}
          </BaseButton>
        </el-space>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.deduction-rules-page {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
}

.summary-card {
  border: 1px solid var(--el-border-color-light);
  border-radius: 14px;
  padding: 14px;
  min-height: 88px;
  background: var(--color-card);
  box-shadow: 0 2px 10px var(--card-shadow);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.summary-label {
  color: var(--el-text-color-secondary);
  font-size: 12px;
  font-weight: 500;
}

.summary-value {
  margin-top: 6px;
  font-size: 22px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  line-height: 1.2;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 16px;
  align-items: start;
}

.table-section,
.applicable-panel,
.table-card,
.checker-summary-card,
.result-item {
  border: 1px solid var(--el-border-color-light);
  border-radius: 14px;
  background: var(--color-card);
  box-shadow: 0 2px 10px var(--card-shadow);
}

.table-section {
  padding: 14px;
}

.toolbar {
  display: grid;
  grid-template-columns:
    minmax(240px, 1fr)
    minmax(160px, 180px)
    minmax(160px, 180px)
    minmax(240px, 300px);
  gap: 12px;
  margin-bottom: 16px;
  align-items: center;
}

.toolbar > * {
  min-width: 0;
}

.lifecycle-filter {
  min-width: 0;
}

.lifecycle-filter :deep(.el-segmented) {
  width: 100%;
}

.lifecycle-filter :deep(.el-segmented__item) {
  min-width: 0;
}

.table-card {
  padding: 8px;
}

.deduction-meter {
  display: flex;
  align-items: center;
  gap: 10px;
}

.deduction-value {
  min-width: 48px;
  text-align: right;
  font-weight: 600;
}

.status-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.empty-state {
  text-align: center;
  padding: 40px 16px 24px;
}

.empty-title {
  font-size: 15px;
  font-weight: 600;
}

.empty-text {
  margin-top: 6px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.applicable-panel {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: sticky;
  top: 16px;
}

.panel-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.applicable-panel h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
}

.applicable-panel p {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  line-height: 1.5;
}

.checker-form {
  margin-top: 4px;
}

.checker-summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.checker-summary-card {
  padding: 10px;
  background: color-mix(in srgb, var(--el-fill-color-light) 65%, white);
}

.checker-summary-label {
  font-size: 11px;
  color: var(--el-text-color-secondary);
}

.checker-summary-value {
  margin-top: 4px;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.35;
  word-break: break-word;
}

.checker-submit {
  width: 100%;
}

.applicable-result {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.result-item {
  padding: 10px;
}

.result-label {
  display: block;
  font-size: 11px;
  color: var(--el-text-color-secondary);
  margin-bottom: 4px;
}

.range-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.percentage-editor {
  display: grid;
  grid-template-columns: 1fr 110px;
  gap: 12px;
  align-items: center;
}

.field-hint {
  margin-top: 6px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  line-height: 1.4;
}

@media (max-width: 1080px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .applicable-panel {
    position: static;
    top: auto;
  }

  .toolbar {
    grid-template-columns:
      minmax(220px, 1fr)
      minmax(150px, 1fr)
      minmax(150px, 1fr);
  }

  .lifecycle-filter {
    grid-column: 1 / -1;
  }
}

@media (max-width: 720px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }

  .summary-card {
    padding: 12px;
    min-height: 78px;
  }

  .summary-value {
    font-size: 18px;
  }

  .table-section,
  .applicable-panel {
    padding: 12px;
  }

  .applicable-panel p {
    font-size: 11px;
  }

  .checker-form :deep(.el-form-item) {
    margin-bottom: 12px;
  }

  .checker-summary-grid {
    grid-template-columns: 1fr;
  }

  .toolbar {
    grid-template-columns: 1fr;
  }

  .lifecycle-filter :deep(.el-segmented__item-label) {
    font-size: 12px;
  }

  .range-grid,
  .percentage-editor,
  .result-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions > * {
    flex: 1 1 auto;
  }
}
</style>

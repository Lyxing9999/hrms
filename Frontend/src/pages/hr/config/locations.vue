<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import { ElMessage, ElMessageBox } from "element-plus";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import GoogleLocationPicker from "~/components/hrms/location/GoogleLocationPicker.vue";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { useFormCreate } from "~/composables/forms/useFormCreate";
import type { WorkLocationDTO } from "~/api/hr_admin/workLocations/dto";

const { $hrLocationService } = useNuxtApp();

const q = ref("");
const isActiveFilter = ref<boolean | undefined>(undefined);
const deletedMode = ref<"active_only" | "include_deleted" | "deleted_only">("active_only");

const deleteLoading = ref<Record<string, boolean>>({});
const restoreLoading = ref<Record<string, boolean>>({});
const toggleStatusLoading = ref<Record<string, boolean>>({});

const createDialogKey = ref(0);
const currentLocationId = ref("");

const includeDeleted = computed(() => deletedMode.value === "include_deleted");
const deletedOnly = computed(() => deletedMode.value === "deleted_only");

const locationColumns = [
  { prop: "name", label: "Location", minWidth: 180 },
  { prop: "address", label: "Address", minWidth: 260 },
  { prop: "coordinates", label: "Coordinates", minWidth: 200, slot: "coordinates" },
  { prop: "radius_meters", label: "Radius", width: 110, slot: "radius_meters" },
  { prop: "is_active", label: "Status", width: 130, slot: "is_active" },
  { prop: "operation", label: "Actions", width: 260, fixed: "right", slot: "operation" },
];

const {
  data: locations,
  currentPage,
  pageSize,
  totalRows,
  initialLoading,
  fetching,
  fetchPage,
  goPage,
  setPageSize,
} = usePaginatedFetch<WorkLocationDTO, void>(
  async (_unused, page, size, signal) => {
    const res = await $hrLocationService.getWorkLocations(
      {
        q: q.value.trim() || undefined,
        page,
        limit: size,
        is_active: isActiveFilter.value,
        include_deleted: includeDeleted.value,
        deleted_only: deletedOnly.value,
      },
      { signal },
    );

    return {
      items: res.items ?? [],
      total: res.total ?? 0,
    };
  },
  { initialPage: 1 },
);

watch([isActiveFilter, deletedMode], () => {
  fetchPage(1);
});

let searchTimer: ReturnType<typeof setTimeout> | null = null;
watch(q, () => {
  if (searchTimer) clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    fetchPage(1);
  }, 400);
});

const locationFormSchema = [
  {
    prop: "name",
    label: "Location Name",
    type: "input",
    required: true,
    placeholder: "e.g. Main Office",
  },
  {
    prop: "address",
    label: "Address",
    type: "textarea",
    required: true,
    placeholder: "Search or pick from map",
    rows: 3,
  },
  {
    prop: "latitude",
    label: "Latitude",
    type: "number",
    required: true,
    min: -90,
    max: 90,
    step: 0.000001,
    placeholder: "e.g. 11.5564",
  },
  {
    prop: "longitude",
    label: "Longitude",
    type: "number",
    required: true,
    min: -180,
    max: 180,
    step: 0.000001,
    placeholder: "e.g. 104.9282",
  },
  {
    prop: "radius_meters",
    label: "Radius (meters)",
    type: "number",
    required: true,
    min: 10,
    max: 5000,
    step: 1,
    placeholder: "e.g. 100",
  },
  {
    prop: "is_active",
    label: "Active",
    type: "switch",
  },
];

const {
  formDialogVisible: createFormVisible,
  formData: createFormData,
  saveForm: saveCreateForm,
  openForm: openCreateForm,
  loading: createFormLoading,
} = useFormCreate(
  () => async (data: any) => {
    return await $hrLocationService.createWorkLocation(data);
  },
  () => ({
    name: "",
    address: "",
    latitude: 11.5564,
    longitude: 104.9282,
    radius_meters: 100,
    is_active: true,
  }),
  () => locationFormSchema,
);

const updateFormVisible = ref(false);
const updateFormLoading = ref(false);
const updateFormData = ref<any>({
  name: "",
  address: "",
  latitude: 11.5564,
  longitude: 104.9282,
  radius_meters: 100,
  is_active: true,
});

const handleOpenCreateForm = async () => {
  createDialogKey.value += 1;
  await openCreateForm({});
};

const handleCreateSave = async (form: any) => {
  const created = await saveCreateForm(form);
  if (created) {
    await fetchPage(1);
  }
};

const handleOpenUpdateForm = (row: WorkLocationDTO) => {
  currentLocationId.value = row.id;
  updateFormData.value = {
    name: row.name,
    address: row.address,
    latitude: row.latitude,
    longitude: row.longitude,
    radius_meters: row.radius_meters,
    is_active: row.is_active,
  };
  updateFormVisible.value = true;
};

const handleUpdateSave = async (form: any) => {
  updateFormLoading.value = true;
  try {
    await $hrLocationService.updateWorkLocation(currentLocationId.value, form);
    updateFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    updateFormLoading.value = false;
  }
};

const handleToggleActive = async (row: WorkLocationDTO, value: boolean) => {
  toggleStatusLoading.value[row.id] = true;
  try {
    if (value) {
      await $hrLocationService.activateWorkLocation(row.id);
    } else {
      await $hrLocationService.deactivateWorkLocation(row.id);
    }
    await fetchPage(currentPage.value || 1);
  } catch {
    row.is_active = !value;
  } finally {
    toggleStatusLoading.value[row.id] = false;
  }
};

const handleSoftDeleteLocation = async (row: WorkLocationDTO) => {
  try {
    await ElMessageBox.confirm(
      `Delete "${row.name}"? You can restore it later.`,
      "Delete Location",
      {
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
        type: "warning",
      },
    );

    deleteLoading.value[row.id] = true;
    await $hrLocationService.softDeleteWorkLocation(row.id);
    ElMessage.success("Location deleted successfully");
    await fetchPage(currentPage.value || 1);
  } finally {
    deleteLoading.value[row.id] = false;
  }
};

const handleRestoreLocation = async (row: WorkLocationDTO) => {
  try {
    await ElMessageBox.confirm(
      `Restore "${row.name}"?`,
      "Restore Location",
      {
        confirmButtonText: "Restore",
        cancelButtonText: "Cancel",
        type: "info",
      },
    );

    restoreLoading.value[row.id] = true;
    await $hrLocationService.restoreWorkLocation(row.id);
    ElMessage.success("Location restored successfully");
    await fetchPage(currentPage.value || 1);
  } finally {
    restoreLoading.value[row.id] = false;
  }
};

const resetFilters = async () => {
  q.value = "";
  isActiveFilter.value = undefined;
  deletedMode.value = "active_only";
  await fetchPage(1);
};

const openInExternalMap = (row: WorkLocationDTO) => {
  window.open(`https://www.google.com/maps?q=${row.latitude},${row.longitude}`, "_blank");
};

await fetchPage(1);
</script>

<template>
  <div class="space-y-4">
    <OverviewHeader
      title="Work Locations"
      description="Manage work locations and GPS radius for attendance validation"
      backPath="/hr/config"
    >
      <template #actions>
        <BaseButton
          plain
          :loading="initialLoading || fetching"
          @click="fetchPage(currentPage || 1)"
        >
          Refresh
        </BaseButton>

        <BaseButton
          type="primary"
          :disabled="initialLoading || fetching"
          @click="handleOpenCreateForm"
        >
          Add Location
        </BaseButton>
      </template>
    </OverviewHeader>

    <el-card shadow="never">
      <el-row :gutter="12">
        <el-col :xs="24" :sm="24" :md="8">
          <el-input
            v-model="q"
            clearable
            placeholder="Search by name or address"
            @clear="fetchPage(1)"
          />
        </el-col>

        <el-col :xs="24" :sm="12" :md="5">
          <el-select
            v-model="isActiveFilter"
            clearable
            placeholder="Status"
            class="w-full"
          >
            <el-option label="All Status" :value="undefined" />
            <el-option label="Active" :value="true" />
            <el-option label="Inactive" :value="false" />
          </el-select>
        </el-col>

        <el-col :xs="24" :sm="12" :md="7">
          <el-segmented
            v-model="deletedMode"
            :options="[
              { label: 'Normal', value: 'active_only' },
              { label: 'Include Deleted', value: 'include_deleted' },
              { label: 'Deleted Only', value: 'deleted_only' },
            ]"
            class="w-full"
          />
        </el-col>

        <el-col :xs="24" :sm="24" :md="4" class="flex justify-end">
          <BaseButton plain @click="resetFilters">
            Reset
          </BaseButton>
        </el-col>
      </el-row>
    </el-card>

    <SmartTable
      :columns="locationColumns"
      :data="locations"
      :loading="initialLoading || fetching"
      :total="totalRows"
      :page="currentPage"
      :page-size="pageSize"
      @page="goPage"
      @page-size="setPageSize"
    >
      <template #coordinates="{ row }">
        <div class="flex flex-col">
          <span>{{ Number(row.latitude).toFixed(6) }}, {{ Number(row.longitude).toFixed(6) }}</span>
          <el-button
            type="primary"
            link
            size="small"
            @click="openInExternalMap(row as WorkLocationDTO)"
          >
            Open Map
          </el-button>
        </div>
      </template>

      <template #radius_meters="{ row }">
        <span>{{ row.radius_meters }} m</span>
      </template>

      <template #is_active="{ row }">
        <div class="flex items-center gap-2">
          <el-tag
            v-if="row.lifecycle?.deleted_at"
            type="danger"
            size="small"
          >
            Deleted
          </el-tag>

          <el-switch
            v-else
            :model-value="row.is_active"
            :loading="toggleStatusLoading[row.id]"
            inline-prompt
            active-text="Active"
            inactive-text="Inactive"
            @change="(value: boolean) => handleToggleActive(row as WorkLocationDTO, value)"
          />
        </div>
      </template>

      <template #operation="{ row }">
        <el-space wrap>
          <el-button
            type="primary"
            size="small"
            link
            :disabled="!!row.lifecycle?.deleted_at"
            @click="handleOpenUpdateForm(row as WorkLocationDTO)"
          >
            Edit
          </el-button>

          <el-button
            type="primary"
            size="small"
            link
            @click="openInExternalMap(row as WorkLocationDTO)"
          >
            Map
          </el-button>

          <el-button
            v-if="row.lifecycle?.deleted_at"
            type="success"
            size="small"
            link
            :loading="restoreLoading[row.id]"
            @click="handleRestoreLocation(row as WorkLocationDTO)"
          >
            Restore
          </el-button>

          <el-button
            v-else
            type="danger"
            size="small"
            link
            :loading="deleteLoading[row.id]"
            @click="handleSoftDeleteLocation(row as WorkLocationDTO)"
          >
            Delete
          </el-button>
        </el-space>
      </template>
    </SmartTable>

    <el-row v-if="totalRows > 0" justify="end">
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="totalRows"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        background
        @current-change="goPage"
        @size-change="setPageSize"
      />
    </el-row>

    <SmartFormDialog
      :key="createDialogKey"
      v-model:visible="createFormVisible"
      :model-value="createFormData"
      :fields="locationFormSchema"
      :width="'70%'"
      :loading="createFormLoading"
      :disabled="createFormLoading"
      title="Add Work Location"
      useElForm
      @save="handleCreateSave"
    >
      <template #default="{ model }">
        <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <div class="space-y-4">
            <el-form-item label="Location Name" required>
              <el-input v-model="model.name" placeholder="e.g. Main Office" />
            </el-form-item>

            <el-form-item label="Address" required>
              <el-input
                v-model="model.address"
                type="textarea"
                :rows="3"
                placeholder="Search by place or pick from map"
              />
            </el-form-item>

            <el-form-item label="Latitude" required>
              <el-input-number
                v-model="model.latitude"
                :min="-90"
                :max="90"
                :step="0.000001"
                class="!w-full"
              />
            </el-form-item>

            <el-form-item label="Longitude" required>
              <el-input-number
                v-model="model.longitude"
                :min="-180"
                :max="180"
                :step="0.000001"
                class="!w-full"
              />
            </el-form-item>

            <el-form-item label="Radius (meters)" required>
              <el-input-number
                v-model="model.radius_meters"
                :min="10"
                :max="5000"
                :step="1"
                class="!w-full"
              />
            </el-form-item>

            <el-form-item label="Active">
              <el-switch v-model="model.is_active" />
            </el-form-item>
          </div>

          <div>
            <GoogleLocationPicker
              v-model:latitude="model.latitude"
              v-model:longitude="model.longitude"
              v-model:address="model.address"
              :radius-meters="model.radius_meters"
            />
          </div>
        </div>
      </template>
    </SmartFormDialog>

    <SmartFormDialog
      v-model:visible="updateFormVisible"
      :model-value="updateFormData"
      :fields="locationFormSchema"
      :width="'70%'"
      :loading="updateFormLoading"
      :disabled="updateFormLoading"
      title="Update Work Location"
      useElForm
      @save="handleUpdateSave"
      @cancel="updateFormVisible = false"
    >
      <template #default="{ model }">
        <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <div class="space-y-4">
            <el-form-item label="Location Name" required>
              <el-input v-model="model.name" placeholder="e.g. Main Office" />
            </el-form-item>

            <el-form-item label="Address" required>
              <el-input
                v-model="model.address"
                type="textarea"
                :rows="3"
                placeholder="Search by place or pick from map"
              />
            </el-form-item>

            <el-form-item label="Latitude" required>
              <el-input-number
                v-model="model.latitude"
                :min="-90"
                :max="90"
                :step="0.000001"
                class="!w-full"
              />
            </el-form-item>

            <el-form-item label="Longitude" required>
              <el-input-number
                v-model="model.longitude"
                :min="-180"
                :max="180"
                :step="0.000001"
                class="!w-full"
              />
            </el-form-item>

            <el-form-item label="Radius (meters)" required>
              <el-input-number
                v-model="model.radius_meters"
                :min="10"
                :max="5000"
                :step="1"
                class="!w-full"
              />
            </el-form-item>

            <el-form-item label="Active">
              <el-switch v-model="model.is_active" />
            </el-form-item>
          </div>

          <div>
            <GoogleLocationPicker
              v-model:latitude="model.latitude"
              v-model:longitude="model.longitude"
              v-model:address="model.address"
              :radius-meters="model.radius_meters"
            />
          </div>
        </div>
      </template>
    </SmartFormDialog>
  </div>
</template>
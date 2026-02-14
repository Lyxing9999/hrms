<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useNuxtApp } from "nuxt/app";
import SmartTable from "~/components/table-edit/core/table/SmartTable.vue";
import type { WorkLocationDTO } from "~/api/hr_admin/location/location.dto";
import { usePaginatedFetch } from "~/composables/data/usePaginatedFetch";
import { ElMessageBox } from "element-plus";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import SmartFormDialog from "~/components/form/SmartFormDialog.vue";
import { useFormCreate } from "~/composables/forms/useFormCreate";

const { $hrLocationService } = useNuxtApp();

const deleteLoading = ref<Record<string | number, boolean>>({});
const restoreLoading = ref<Record<string | number, boolean>>({});

const q = ref("");
const is_active = ref<boolean | undefined>(undefined);
const include_deleted = ref(false);
const deleted_only = ref(false);

// Table columns
const locationColumns = [
  { prop: "name", label: "Location Name", minWidth: 180 },
  { prop: "address", label: "Address", minWidth: 250 },
  { prop: "latitude", label: "Latitude", width: 120 },
  { prop: "longitude", label: "Longitude", width: 120 },
  { prop: "radius_meters", label: "Radius (m)", width: 100 },
  { prop: "is_active", label: "Status", width: 100, slot: "is_active" },
  { prop: "operation", label: "Actions", width: 200, fixed: "right", slot: "operation" },
];

// Fetch data
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
  async (_unusedFilter, page, size, signal) => {
    const keyword = q.value.trim();
    const res = await $hrLocationService.getLocations({
      q: keyword.length ? keyword : undefined,
      page,
      limit: size,
      is_active: is_active.value,
      include_deleted: include_deleted.value,
      deleted_only: deleted_only.value,
      signal,
    });

    return {
      items: (res.items ?? []) as WorkLocationDTO[],
      total: res.total ?? 0,
    };
  },
  { initialPage: 1 }
);

watch([q, is_active, include_deleted, deleted_only], () => {
  fetchPage(1);
});

// Form schema
const locationFormSchema = [
  {
    prop: "name",
    label: "Location Name",
    type: "input",
    required: true,
    placeholder: "e.g., Main Office",
  },
  {
    prop: "address",
    label: "Address",
    type: "textarea",
    required: true,
    placeholder: "Full address",
    rows: 3,
  },
  {
    prop: "latitude",
    label: "Latitude",
    type: "number",
    required: true,
    placeholder: "e.g., 11.5564",
    min: -90,
    max: 90,
    step: 0.000001,
  },
  {
    prop: "longitude",
    label: "Longitude",
    type: "number",
    required: true,
    placeholder: "e.g., 104.9282",
    min: -180,
    max: 180,
    step: 0.000001,
  },
  {
    prop: "radius_meters",
    label: "Radius (meters)",
    type: "number",
    required: true,
    placeholder: "e.g., 100",
    min: 10,
    max: 1000,
  },
  {
    prop: "is_active",
    label: "Active",
    type: "switch",
  },
];

// Create form
const {
  formDialogVisible: createFormVisible,
  formData: createFormData,
  saveForm: saveCreateForm,
  openForm: openCreateForm,
  loading: createFormLoading,
} = useFormCreate(
  () => async (data: any) => {
    return await $hrLocationService.createLocation(data);
  },
  () => ({
    name: "",
    address: "",
    latitude: 11.5564,
    longitude: 104.9282,
    radius_meters: 100,
    is_active: true,
  }),
  () => locationFormSchema
);

const handleCreateSave = async (form: any) => {
  const created = await saveCreateForm(form);
  if (created) await fetchPage(1);
};

const createDialogKey = ref(0);

const handleOpenCreateForm = async () => {
  createDialogKey.value++;
  await openCreateForm({});
};

// Update form
const updateFormVisible = ref(false);
const updateFormData = ref<any>({});
const updateFormLoading = ref(false);
const currentLocationId = ref<string>("");

const handleOpenUpdateForm = async (row: WorkLocationDTO) => {
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
    await $hrLocationService.updateLocation(currentLocationId.value, form);
    updateFormVisible.value = false;
    await fetchPage(currentPage.value || 1);
  } finally {
    updateFormLoading.value = false;
  }
};

// Delete
const handleSoftDeleteLocation = async (row: WorkLocationDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to delete this location?",
      "Warning",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "warning" }
    );

    deleteLoading.value[row.id] = true;
    await $hrLocationService.softDeleteLocation(row.id);
    await fetchPage(currentPage.value || 1);
  } finally {
    deleteLoading.value[row.id] = false;
  }
};

// Restore
const handleRestoreLocation = async (row: WorkLocationDTO) => {
  try {
    await ElMessageBox.confirm(
      "Are you sure you want to restore this location?",
      "Confirm Restore",
      { confirmButtonText: "Yes", cancelButtonText: "No", type: "info" }
    );

    restoreLoading.value[row.id] = true;
    await $hrLocationService.restoreLocation(row.id);
    await fetchPage(currentPage.value || 1);
  } finally {
    restoreLoading.value[row.id] = false;
  }
};

// Initial load
await fetchPage(1);
</script>

<template>
  <OverviewHeader
    :title="'Work Locations'"
    :description="'Manage work locations with GPS coordinates for check-in validation'"
    :backPath="'/hr/config'"
  >
    <template #actions>
      <BaseButton
        plain
        :loading="initialLoading || fetching"
        class="!border-[color:var(--color-primary)] !text-[color:var(--color-primary)] hover:!bg-[var(--color-primary-light-7)]"
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

  <!-- Filters -->
  <el-row :gutter="16" class="mb-4">
    <el-col :span="6">
      <el-input
        v-model="q"
        placeholder="Search by name or address..."
        clearable
        @clear="fetchPage(1)"
      />
    </el-col>
    <el-col :span="4">
      <el-select
        v-model="is_active"
        placeholder="Filter by status"
        clearable
        @change="fetchPage(1)"
      >
        <el-option label="Active" :value="true" />
        <el-option label="Inactive" :value="false" />
      </el-select>
    </el-col>
    <el-col :span="4">
      <el-checkbox v-model="include_deleted" @change="fetchPage(1)">
        Include Deleted
      </el-checkbox>
    </el-col>
  </el-row>

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
    <template #is_active="{ row }">
      <el-tag v-if="row.is_active" type="success" size="small">Active</el-tag>
      <el-tag v-else type="info" size="small">Inactive</el-tag>
    </template>

    <template #operation="{ row }">
      <el-space>
        <el-button
          type="primary"
          size="small"
          link
          @click="handleOpenUpdateForm(row as WorkLocationDTO)"
        >
          Edit
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

  <el-row v-if="totalRows > 0" justify="end" class="m-4">
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

  <!-- Create Dialog -->
  <SmartFormDialog
    :key="createDialogKey"
    v-model:visible="createFormVisible"
    :model-value="createFormData"
    :fields="locationFormSchema"
    :width="'40%'"
    :loading="createFormLoading"
    :disabled="createFormLoading"
    title="Add Work Location"
    useElForm
    @save="handleCreateSave"
  />

  <!-- Update Dialog -->
  <SmartFormDialog
    v-model:visible="updateFormVisible"
    :model-value="updateFormData"
    :fields="locationFormSchema"
    :width="'40%'"
    :loading="updateFormLoading"
    :disabled="updateFormLoading"
    title="Update Work Location"
    useElForm
    @save="handleUpdateSave"
    @cancel="updateFormVisible = false"
  />
</template>

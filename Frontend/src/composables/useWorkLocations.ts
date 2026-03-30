import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { WorkLocationService } from '~/services/hr/work-location.service';
import type {
  WorkLocationDto,
  WorkLocationFilters,
  WorkLocationListResponse,
} from '~/types/hr/work-location.dto';

export function useWorkLocations() {
  const workLocationService = new WorkLocationService();
  
  // State
  const locations = ref<WorkLocationDto[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  
  // Pagination
  const pagination = reactive({
    page: 1,
    limit: 20,
    total: 0,
  });

  // Filters
  const filters = reactive<WorkLocationFilters>({
    search: '',
    status: 'all',
    deleted_mode: 'normal',
  });

  // Methods
  async function fetchLocations() {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await workLocationService.getWorkLocations(
        filters,
        pagination.page,
        pagination.limit
      );
      
      locations.value = response.data;
      pagination.total = response.total;
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch locations';
      ElMessage.error(error.value);
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function refreshLocations() {
    await fetchLocations();
  }

  function resetFilters() {
    filters.search = '';
    filters.status = 'all';
    filters.deleted_mode = 'normal';
    pagination.page = 1;
  }

  function updatePagination(page?: number, limit?: number) {
    if (page !== undefined) pagination.page = page;
    if (limit !== undefined) {
      pagination.limit = limit;
      pagination.page = 1; // Reset to first page when changing page size
    }
  }

  return {
    // State
    locations,
    isLoading,
    error,
    pagination,
    filters,
    
    // Methods
    fetchLocations,
    refreshLocations,
    resetFilters,
    updatePagination,
    
    // Service instance for direct access
    workLocationService,
  };
}

export function useWorkLocationActions() {
  const isUpdating = ref<Record<string, boolean>>({});
  const isDeleting = ref<Record<string, boolean>>({});
  
  const workLocationService = new WorkLocationService();

  async function toggleLocationStatus(location: WorkLocationDto) {
    const locationId = location.id;
    isUpdating.value[locationId] = true;

    try {
      const updatedLocation = await workLocationService.toggleWorkLocationStatus(
        locationId,
        location.is_active
      );
      
      ElMessage.success(
        `Location ${location.is_active ? 'activated' : 'deactivated'} successfully`
      );
      
      return updatedLocation;
    } catch (error: any) {
      ElMessage.error(error.message || 'Failed to update location status');
      throw error;
    } finally {
      isUpdating.value[locationId] = false;
    }
  }

  async function deleteLocation(locationId: string) {
    isDeleting.value[locationId] = true;

    try {
      await workLocationService.softDeleteWorkLocation(locationId);
      ElMessage.success('Location deleted successfully');
    } catch (error: any) {
      ElMessage.error(error.message || 'Failed to delete location');
      throw error;
    } finally {
      isDeleting.value[locationId] = false;
    }
  }

  async function restoreLocation(locationId: string) {
    isDeleting.value[locationId] = true;

    try {
      const restoredLocation = await workLocationService.restoreWorkLocation(locationId);
      ElMessage.success('Location restored successfully');
      return restoredLocation;
    } catch (error: any) {
      ElMessage.error(error.message || 'Failed to restore location');
      throw error;
    } finally {
      isDeleting.value[locationId] = false;
    }
  }

  function openLocationInMaps(latitude: number, longitude: number) {
    const url = workLocationService.generateGoogleMapsUrl(latitude, longitude);
    window.open(url, '_blank');
  }

  return {
    isUpdating,
    isDeleting,
    toggleLocationStatus,
    deleteLocation,
    restoreLocation,
    openLocationInMaps,
    workLocationService,
  };
}
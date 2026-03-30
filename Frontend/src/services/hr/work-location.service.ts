import { WorkLocationApi } from '~/api/hr/work-location.api';
import type {
  WorkLocationDto,
  CreateWorkLocationDto,
  UpdateWorkLocationDto,
  WorkLocationSelectOption,
  WorkLocationFilters,
  WorkLocationListResponse,
} from '~/types/hr/work-location.dto';

export class WorkLocationService {
  private api: WorkLocationApi;

  constructor() {
    this.api = new WorkLocationApi();
  }

  async getWorkLocations(
    filters: WorkLocationFilters = {},
    page = 1,
    limit = 20
  ): Promise<WorkLocationListResponse> {
    try {
      return await this.api.getWorkLocations(filters, page, limit);
    } catch (error) {
      console.error('Error fetching work locations:', error);
      throw new Error('Failed to fetch work locations');
    }
  }

  async getWorkLocation(id: string): Promise<WorkLocationDto> {
    try {
      return await this.api.getWorkLocation(id);
    } catch (error) {
      console.error('Error fetching work location:', error);
      throw new Error('Failed to fetch work location');
    }
  }

  async getWorkLocationSelectOptions(): Promise<WorkLocationSelectOption[]> {
    try {
      return await this.api.getWorkLocationSelectOptions();
    } catch (error) {
      console.error('Error fetching work location options:', error);
      throw new Error('Failed to fetch work location options');
    }
  }

  async createWorkLocation(payload: CreateWorkLocationDto): Promise<WorkLocationDto> {
    try {
      // Validate required fields
      this.validateWorkLocationData(payload);
      return await this.api.createWorkLocation(payload);
    } catch (error) {
      console.error('Error creating work location:', error);
      throw error instanceof Error ? error : new Error('Failed to create work location');
    }
  }

  async updateWorkLocation(
    id: string,
    payload: UpdateWorkLocationDto
  ): Promise<WorkLocationDto> {
    try {
      // Validate fields if provided
      if (Object.keys(payload).length > 0) {
        this.validateWorkLocationData(payload, false);
      }
      return await this.api.updateWorkLocation(id, payload);
    } catch (error) {
      console.error('Error updating work location:', error);
      throw error instanceof Error ? error : new Error('Failed to update work location');
    }
  }

  async toggleWorkLocationStatus(id: string, isActive: boolean): Promise<WorkLocationDto> {
    try {
      if (isActive) {
        return await this.api.activateWorkLocation(id);
      } else {
        return await this.api.deactivateWorkLocation(id);
      }
    } catch (error) {
      console.error('Error toggling work location status:', error);
      throw new Error('Failed to update work location status');
    }
  }

  async softDeleteWorkLocation(id: string): Promise<void> {
    try {
      await this.api.softDeleteWorkLocation(id);
    } catch (error) {
      console.error('Error deleting work location:', error);
      throw new Error('Failed to delete work location');
    }
  }

  async restoreWorkLocation(id: string): Promise<WorkLocationDto> {
    try {
      return await this.api.restoreWorkLocation(id);
    } catch (error) {
      console.error('Error restoring work location:', error);
      throw new Error('Failed to restore work location');
    }
  }

  generateGoogleMapsUrl(latitude: number, longitude: number): string {
    return `https://www.google.com/maps?q=${latitude},${longitude}`;
  }

  formatCoordinates(latitude: number, longitude: number): string {
    return `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
  }

  formatRadius(radiusMeters: number): string {
    if (radiusMeters >= 1000) {
      return `${(radiusMeters / 1000).toFixed(1)} km`;
    }
    return `${radiusMeters} m`;
  }

  private validateWorkLocationData(
    data: CreateWorkLocationDto | UpdateWorkLocationDto,
    isCreate = true
  ): void {
    if (isCreate) {
      const createData = data as CreateWorkLocationDto;
      if (!createData.name?.trim()) {
        throw new Error('Location name is required');
      }
      if (!createData.address?.trim()) {
        throw new Error('Address is required');
      }
      if (typeof createData.latitude !== 'number' || isNaN(createData.latitude)) {
        throw new Error('Valid latitude is required');
      }
      if (typeof createData.longitude !== 'number' || isNaN(createData.longitude)) {
        throw new Error('Valid longitude is required');
      }
      if (typeof createData.radius_meters !== 'number' || createData.radius_meters <= 0) {
        throw new Error('Valid radius is required');
      }
    } else {
      const updateData = data as UpdateWorkLocationDto;
      if (updateData.name !== undefined && !updateData.name?.trim()) {
        throw new Error('Location name cannot be empty');
      }
      if (updateData.address !== undefined && !updateData.address?.trim()) {
        throw new Error('Address cannot be empty');
      }
      if (updateData.latitude !== undefined && (typeof updateData.latitude !== 'number' || isNaN(updateData.latitude))) {
        throw new Error('Valid latitude is required');
      }
      if (updateData.longitude !== undefined && (typeof updateData.longitude !== 'number' || isNaN(updateData.longitude))) {
        throw new Error('Valid longitude is required');
      }
      if (updateData.radius_meters !== undefined && (typeof updateData.radius_meters !== 'number' || updateData.radius_meters <= 0)) {
        throw new Error('Valid radius is required');
      }
    }

    // Validate coordinate ranges
    if ('latitude' in data && data.latitude !== undefined) {
      if (data.latitude < -90 || data.latitude > 90) {
        throw new Error('Latitude must be between -90 and 90');
      }
    }
    if ('longitude' in data && data.longitude !== undefined) {
      if (data.longitude < -180 || data.longitude > 180) {
        throw new Error('Longitude must be between -180 and 180');
      }
    }
  }
}
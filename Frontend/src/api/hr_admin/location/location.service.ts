// frontend/src/api/hr_admin/location/location.service.ts
import { WorkLocationApi } from "./location.api";
import type {
  WorkLocationDTO,
  WorkLocationPaginatedDTO,
  WorkLocationCreateDTO,
  WorkLocationUpdateDTO,
  WorkLocationListParams,
} from "./location.dto";

export class WorkLocationService {
  private api: WorkLocationApi;

  constructor() {
    this.api = new WorkLocationApi();
  }

  async getLocations(
    params: WorkLocationListParams = {}
  ): Promise<WorkLocationPaginatedDTO> {
    return await this.api.getLocations(params);
  }

  async getLocation(id: string): Promise<WorkLocationDTO> {
    return await this.api.getLocation(id);
  }

  async getActiveLocations(): Promise<{ items: WorkLocationDTO[] }> {
    return await this.api.getActiveLocations();
  }

  async createLocation(
    data: WorkLocationCreateDTO
  ): Promise<WorkLocationDTO> {
    return await this.api.createLocation(data);
  }

  async updateLocation(
    id: string,
    data: WorkLocationUpdateDTO
  ): Promise<WorkLocationDTO> {
    return await this.api.updateLocation(id, data);
  }

  async softDeleteLocation(id: string): Promise<WorkLocationDTO> {
    return await this.api.softDeleteLocation(id);
  }

  async restoreLocation(id: string): Promise<WorkLocationDTO> {
    return await this.api.restoreLocation(id);
  }
}

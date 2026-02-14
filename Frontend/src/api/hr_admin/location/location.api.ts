// frontend/src/api/hr_admin/location/location.api.ts
import type {
  WorkLocationDTO,
  WorkLocationPaginatedDTO,
  WorkLocationCreateDTO,
  WorkLocationUpdateDTO,
  WorkLocationListParams,
} from "./location.dto";

export class WorkLocationApi {
  private baseUrl = "/api/hrms/admin/work-locations";

  async getLocations(
    params: WorkLocationListParams = {}
  ): Promise<WorkLocationPaginatedDTO> {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.append("page", params.page.toString());
    if (params.limit) queryParams.append("limit", params.limit.toString());
    if (params.q) queryParams.append("q", params.q);
    if (params.is_active !== undefined)
      queryParams.append("is_active", params.is_active.toString());
    if (params.include_deleted !== undefined)
      queryParams.append("include_deleted", params.include_deleted.toString());
    if (params.deleted_only !== undefined)
      queryParams.append("deleted_only", params.deleted_only.toString());

    const response = await $fetch<WorkLocationPaginatedDTO>(
      `${this.baseUrl}?${queryParams}`,
      { signal: params.signal }
    );
    return response;
  }

  async getLocation(id: string): Promise<WorkLocationDTO> {
    return await $fetch<WorkLocationDTO>(`${this.baseUrl}/${id}`);
  }

  async getActiveLocations(): Promise<{ items: WorkLocationDTO[] }> {
    return await $fetch<{ items: WorkLocationDTO[] }>(
      `${this.baseUrl}/active`
    );
  }

  async createLocation(
    data: WorkLocationCreateDTO
  ): Promise<WorkLocationDTO> {
    return await $fetch<WorkLocationDTO>(this.baseUrl, {
      method: "POST",
      body: data,
    });
  }

  async updateLocation(
    id: string,
    data: WorkLocationUpdateDTO
  ): Promise<WorkLocationDTO> {
    return await $fetch<WorkLocationDTO>(`${this.baseUrl}/${id}`, {
      method: "PATCH",
      body: data,
    });
  }

  async softDeleteLocation(id: string): Promise<WorkLocationDTO> {
    return await $fetch<WorkLocationDTO>(`${this.baseUrl}/${id}/soft-delete`, {
      method: "DELETE",
    });
  }

  async restoreLocation(id: string): Promise<WorkLocationDTO> {
    return await $fetch<WorkLocationDTO>(`${this.baseUrl}/${id}/restore`, {
      method: "POST",
    });
  }
}

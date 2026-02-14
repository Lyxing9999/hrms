// frontend/src/api/hr_admin/schedule/schedule.api.ts
import type {
  WorkingScheduleDTO,
  WorkingSchedulePaginatedDTO,
  WorkingScheduleCreateDTO,
  WorkingScheduleUpdateDTO,
  WorkingScheduleListParams,
} from "./schedule.dto";

export class WorkingScheduleApi {
  private baseUrl = "/api/hrms/admin/working-schedules";

  async getSchedules(
    params: WorkingScheduleListParams = {}
  ): Promise<WorkingSchedulePaginatedDTO> {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.append("page", params.page.toString());
    if (params.limit) queryParams.append("limit", params.limit.toString());
    if (params.q) queryParams.append("q", params.q);
    if (params.include_deleted !== undefined)
      queryParams.append("include_deleted", params.include_deleted.toString());
    if (params.deleted_only !== undefined)
      queryParams.append("deleted_only", params.deleted_only.toString());

    const response = await $fetch<WorkingSchedulePaginatedDTO>(
      `${this.baseUrl}?${queryParams}`,
      { signal: params.signal }
    );
    return response;
  }

  async getSchedule(id: string): Promise<WorkingScheduleDTO> {
    return await $fetch<WorkingScheduleDTO>(`${this.baseUrl}/${id}`);
  }

  async getDefaultSchedule(): Promise<WorkingScheduleDTO> {
    return await $fetch<WorkingScheduleDTO>(`${this.baseUrl}/default`);
  }

  async createSchedule(
    data: WorkingScheduleCreateDTO
  ): Promise<WorkingScheduleDTO> {
    return await $fetch<WorkingScheduleDTO>(this.baseUrl, {
      method: "POST",
      body: data,
    });
  }

  async updateSchedule(
    id: string,
    data: WorkingScheduleUpdateDTO
  ): Promise<WorkingScheduleDTO> {
    return await $fetch<WorkingScheduleDTO>(`${this.baseUrl}/${id}`, {
      method: "PATCH",
      body: data,
    });
  }

  async softDeleteSchedule(id: string): Promise<WorkingScheduleDTO> {
    return await $fetch<WorkingScheduleDTO>(
      `${this.baseUrl}/${id}/soft-delete`,
      { method: "DELETE" }
    );
  }

  async restoreSchedule(id: string): Promise<WorkingScheduleDTO> {
    return await $fetch<WorkingScheduleDTO>(`${this.baseUrl}/${id}/restore`, {
      method: "POST",
    });
  }
}

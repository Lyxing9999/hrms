import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  WorkingScheduleDTO,
  WorkingScheduleCreateDTO,
  WorkingScheduleUpdateDTO,
  WorkingScheduleListParams,
} from "./dto";

import type { SelectOptionDTO } from "~/api/types/common/select-option.type";

export class WorkingScheduleApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/working-schedules",
  ) {}

  async getSchedules(params?: WorkingScheduleListParams) {
    const res = await this.$api.get<ApiResponse<WorkingScheduleDTO[]>>(
      this.baseURL,
      {
        params,
      },
    );
    return res.data;
  }

  async getSchedule(id: string) {
    const res = await this.$api.get<ApiResponse<WorkingScheduleDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async getDefaultSchedule() {
    const res = await this.$api.get<ApiResponse<WorkingScheduleDTO>>(
      `${this.baseURL}/default`,
    );
    return res.data;
  }

  async createSchedule(payload: WorkingScheduleCreateDTO) {
    const res = await this.$api.post<ApiResponse<WorkingScheduleDTO>>(
      this.baseURL,
      payload,
    );
    return res.data;
  }

  async updateSchedule(id: string, payload: WorkingScheduleUpdateDTO) {
    const res = await this.$api.patch<ApiResponse<WorkingScheduleDTO>>(
      `${this.baseURL}/${id}`,
      payload,
    );
    return res.data;
  }

  async softDeleteSchedule(id: string) {
    const res = await this.$api.delete<ApiResponse<WorkingScheduleDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async restoreSchedule(id: string) {
    const res = await this.$api.post<ApiResponse<WorkingScheduleDTO>>(
      `${this.baseURL}/${id}/restore`,
    );
    return res.data;
  }

  async getScheduleSelectOptions() {
    const res = await this.$api.get<ApiResponse<SelectOptionDTO[]>>(
      `${this.baseURL}/select-options`,
    );
    return res.data;
  }
}

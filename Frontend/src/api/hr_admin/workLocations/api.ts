import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  WorkLocationDTO,
  WorkLocationCreateDTO,
  WorkLocationUpdateDTO,
  WorkLocationListParams,
} from "./dto";

export class WorkLocationApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/work-locations",
  ) {}

  async getWorkLocations(params?: WorkLocationListParams) {
    const res = await this.$api.get<ApiResponse<WorkLocationDTO[]>>(
      this.baseURL,
      {
        params,
      },
    );
    return res.data;
  }

  async getWorkLocation(id: string) {
    const res = await this.$api.get<ApiResponse<WorkLocationDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async getActiveWorkLocation() {
    const res = await this.$api.get<ApiResponse<WorkLocationDTO | null>>(
      `${this.baseURL}/active`,
    );
    return res.data;
  }

  async createWorkLocation(payload: WorkLocationCreateDTO) {
    const res = await this.$api.post<ApiResponse<WorkLocationDTO>>(
      this.baseURL,
      payload,
    );
    return res.data;
  }

  async updateWorkLocation(id: string, payload: WorkLocationUpdateDTO) {
    const res = await this.$api.patch<ApiResponse<WorkLocationDTO>>(
      `${this.baseURL}/${id}`,
      payload,
    );
    return res.data;
  }

  async activateWorkLocation(id: string) {
    const res = await this.$api.post<ApiResponse<WorkLocationDTO>>(
      `${this.baseURL}/${id}/activate`,
    );
    return res.data;
  }

  async deactivateWorkLocation(id: string) {
    const res = await this.$api.post<ApiResponse<WorkLocationDTO>>(
      `${this.baseURL}/${id}/deactivate`,
    );
    return res.data;
  }

  async softDeleteWorkLocation(id: string) {
    const res = await this.$api.delete<ApiResponse<WorkLocationDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async restoreWorkLocation(id: string) {
    const res = await this.$api.post<ApiResponse<WorkLocationDTO>>(
      `${this.baseURL}/${id}/restore`,
    );
    return res.data;
  }

  async getWorkLocationSelectOptions() {
    const res = await this.$api.get<
      ApiResponse<{ value: string; label: string }[]>
    >(`${this.baseURL}/select-options`);
    return res.data;
  }
}

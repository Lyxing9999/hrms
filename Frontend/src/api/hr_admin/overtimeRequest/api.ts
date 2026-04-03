import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  OvertimeRequestDTO,
  OvertimeRequestCreateDTO,
  OvertimeRequestUpdateDTO,
  OvertimeRequestReviewDTO,
  OvertimeRequestListParams,
} from "./dto";

export class OvertimeRequestApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/overtime-requests",
  ) {}

  async getMyRequests(params?: OvertimeRequestListParams) {
    const res = await this.$api.get<ApiResponse<OvertimeRequestDTO[]>>(
      `${this.baseURL}/me`,
      {
        params,
        signal: params?.signal,
      },
    );
    return res.data;
  }

  async getTeamRequests(params?: OvertimeRequestListParams) {
    const res = await this.$api.get<ApiResponse<OvertimeRequestDTO[]>>(
      `${this.baseURL}/team`,
      {
        params,
        signal: params?.signal,
      },
    );
    return res.data;
  }

  async getRequest(id: string) {
    const res = await this.$api.get<ApiResponse<OvertimeRequestDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async createRequest(payload: OvertimeRequestCreateDTO) {
    const res = await this.$api.post<ApiResponse<OvertimeRequestDTO>>(
      this.baseURL,
      payload,
    );
    return res.data;
  }

  async updateRequest(id: string, payload: OvertimeRequestUpdateDTO) {
    const res = await this.$api.patch<ApiResponse<OvertimeRequestDTO>>(
      `${this.baseURL}/${id}`,
      payload,
    );
    return res.data;
  }

  async cancelRequest(id: string) {
    const res = await this.$api.delete<ApiResponse<OvertimeRequestDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async reviewRequest(id: string, payload: OvertimeRequestReviewDTO) {
    const res = await this.$api.post<ApiResponse<OvertimeRequestDTO>>(
      `${this.baseURL}/${id}/review`,
      payload,
    );
    return res.data;
  }
}

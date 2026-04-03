import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

import type {
  OvertimeRequestDTO,
  OvertimeRequestCreateDTO,
  OvertimeRequestUpdateDTO,
  OvertimeRequestReviewDTO,
  OvertimeRequestListParams,
} from "./dto";

import { OvertimeRequestApi } from "./api";

export class OvertimeRequestService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly overtimeRequestApi: OvertimeRequestApi) {}

  async getMyRequests(
    params?: OvertimeRequestListParams,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestDTO[]> {
    const data = await this.callApi<OvertimeRequestDTO[]>(
      () => this.overtimeRequestApi.getMyRequests(params),
      options,
    );
    return data ?? [];
  }

  async getTeamRequests(
    params?: OvertimeRequestListParams,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestDTO[]> {
    const data = await this.callApi<OvertimeRequestDTO[]>(
      () => this.overtimeRequestApi.getTeamRequests(params),
      options,
    );
    return data ?? [];
  }

  async getRequest(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.getRequest(id),
      options,
    );
    return data!;
  }

  async createRequest(
    payload: OvertimeRequestCreateDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.createRequest(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async updateRequest(
    id: string,
    payload: OvertimeRequestUpdateDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.updateRequest(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async cancelRequest(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.cancelRequest(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async reviewRequest(
    id: string,
    payload: OvertimeRequestReviewDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.reviewRequest(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }
}

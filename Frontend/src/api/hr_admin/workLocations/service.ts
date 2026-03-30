import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

import type {
  WorkLocationDTO,
  WorkLocationCreateDTO,
  WorkLocationUpdateDTO,
  WorkLocationListParams,
} from "./dto";
import { WorkLocationApi } from "./api";

export class WorkLocationService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly workLocationApi: WorkLocationApi) {}

  async getWorkLocations(
    params?: WorkLocationListParams,
    options?: ApiCallOptions,
  ): Promise<WorkLocationDTO[]> {
    const data = await this.callApi<WorkLocationDTO[]>(
      () => this.workLocationApi.getWorkLocations(params),
      options,
    );
    return data!;
  }

  async getWorkLocation(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<WorkLocationDTO>(
      () => this.workLocationApi.getWorkLocation(id),
      options,
    );
    return data!;
  }

  async getActiveWorkLocation(options?: ApiCallOptions) {
    const data = await this.callApi<WorkLocationDTO | null>(
      () => this.workLocationApi.getActiveWorkLocation(),
      options,
    );
    return data!;
  }

  async createWorkLocation(
    payload: WorkLocationCreateDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<WorkLocationDTO>(
      () => this.workLocationApi.createWorkLocation(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async updateWorkLocation(
    id: string,
    payload: WorkLocationUpdateDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<WorkLocationDTO>(
      () => this.workLocationApi.updateWorkLocation(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async activateWorkLocation(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<WorkLocationDTO>(
      () => this.workLocationApi.activateWorkLocation(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async deactivateWorkLocation(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<WorkLocationDTO>(
      () => this.workLocationApi.deactivateWorkLocation(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async softDeleteWorkLocation(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<WorkLocationDTO>(
      () => this.workLocationApi.softDeleteWorkLocation(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async restoreWorkLocation(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<WorkLocationDTO>(
      () => this.workLocationApi.restoreWorkLocation(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }
}
import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

import type {
  WorkingScheduleDTO,
  WorkingScheduleCreateDTO,
  WorkingScheduleUpdateDTO,
  WorkingScheduleListParams,
} from "./dto";

import type { SelectOptionDTO } from "~/api/types/common/select-option.type";

import { WorkingScheduleApi } from "./api";

export class WorkingScheduleService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly workingScheduleApi: WorkingScheduleApi) {}

  async getSchedules(
    params?: WorkingScheduleListParams,
    options?: ApiCallOptions,
  ): Promise<WorkingScheduleDTO[]> {
    const data = await this.callApi<WorkingScheduleDTO[]>(
      () => this.workingScheduleApi.getSchedules(params),
      options,
    );
    return data ?? [];
  }

  async getSchedule(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<WorkingScheduleDTO>(
      () => this.workingScheduleApi.getSchedule(id),
      options,
    );
    return data!;
  }

  async getDefaultSchedule(options?: ApiCallOptions) {
    const data = await this.callApi<WorkingScheduleDTO>(
      () => this.workingScheduleApi.getDefaultSchedule(),
      options,
    );
    return data!;
  }

  async createSchedule(
    payload: WorkingScheduleCreateDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<WorkingScheduleDTO>(
      () => this.workingScheduleApi.createSchedule(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async updateSchedule(
    id: string,
    payload: WorkingScheduleUpdateDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<WorkingScheduleDTO>(
      () => this.workingScheduleApi.updateSchedule(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async softDeleteSchedule(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<WorkingScheduleDTO>(
      () => this.workingScheduleApi.softDeleteSchedule(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async restoreSchedule(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<WorkingScheduleDTO>(
      () => this.workingScheduleApi.restoreSchedule(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }
  async getScheduleSelectOptions(options?: ApiCallOptions) {
    const data = await this.callApi<SelectOptionDTO[]>(
      () => this.workingScheduleApi.getScheduleSelectOptions(),
      options,
    );
    return data ?? [];
  }
}

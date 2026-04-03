import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

import type {
  PublicHolidayDTO,
  PublicHolidayCreateDTO,
  PublicHolidayUpdateDTO,
  PublicHolidayImportDefaultsDTO,
  PublicHolidayImportResultDTO,
  PublicHolidayListParams,
} from "./dto";

import { PublicHolidayApi } from "./api";

export class PublicHolidayService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly publicHolidayApi: PublicHolidayApi) {}

  async getPublicHolidays(
    params?: PublicHolidayListParams,
    options?: ApiCallOptions,
  ): Promise<PublicHolidayDTO[]> {
    const data = await this.callApi<PublicHolidayDTO[]>(
      () => this.publicHolidayApi.getPublicHolidays(params),
      options,
    );
    return data ?? [];
  }

  async getPublicHoliday(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<PublicHolidayDTO>(
      () => this.publicHolidayApi.getPublicHoliday(id),
      options,
    );
    return data!;
  }

  async getPublicHolidayByDate(date: string, options?: ApiCallOptions) {
    const data = await this.callApi<PublicHolidayDTO | null>(
      () => this.publicHolidayApi.getPublicHolidayByDate(date),
      options,
    );
    return data ?? null;
  }

  async createPublicHoliday(
    payload: PublicHolidayCreateDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<PublicHolidayDTO>(
      () => this.publicHolidayApi.createPublicHoliday(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async importDefaultPublicHolidays(
    payload: PublicHolidayImportDefaultsDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<PublicHolidayImportResultDTO>(
      () => this.publicHolidayApi.importDefaultPublicHolidays(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async updatePublicHoliday(
    id: string,
    payload: PublicHolidayUpdateDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<PublicHolidayDTO>(
      () => this.publicHolidayApi.updatePublicHoliday(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async softDeletePublicHoliday(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<PublicHolidayDTO>(
      () => this.publicHolidayApi.softDeletePublicHoliday(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async restorePublicHoliday(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<PublicHolidayDTO>(
      () => this.publicHolidayApi.restorePublicHoliday(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }
}

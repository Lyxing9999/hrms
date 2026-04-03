import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  PublicHolidayDTO,
  PublicHolidayCreateDTO,
  PublicHolidayUpdateDTO,
  PublicHolidayImportDefaultsDTO,
  PublicHolidayImportResultDTO,
  PublicHolidayListParams,
} from "./dto";

export class PublicHolidayApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/public-holidays",
  ) {}

  async getPublicHolidays(params?: PublicHolidayListParams) {
    const res = await this.$api.get<ApiResponse<PublicHolidayDTO[]>>(
      this.baseURL,
      { params, signal: params?.signal },
    );
    return res.data;
  }

  async getPublicHoliday(id: string) {
    const res = await this.$api.get<ApiResponse<PublicHolidayDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async getPublicHolidayByDate(date: string) {
    const res = await this.$api.get<ApiResponse<PublicHolidayDTO | null>>(
      `${this.baseURL}/by-date`,
      { params: { date } },
    );
    return res.data;
  }

  async createPublicHoliday(payload: PublicHolidayCreateDTO) {
    const res = await this.$api.post<ApiResponse<PublicHolidayDTO>>(
      this.baseURL,
      payload,
    );
    return res.data;
  }

  async importDefaultPublicHolidays(payload: PublicHolidayImportDefaultsDTO) {
    const res = await this.$api.post<ApiResponse<PublicHolidayImportResultDTO>>(
      `${this.baseURL}/import-defaults`,
      payload,
    );
    return res.data;
  }

  async updatePublicHoliday(id: string, payload: PublicHolidayUpdateDTO) {
    const res = await this.$api.patch<ApiResponse<PublicHolidayDTO>>(
      `${this.baseURL}/${id}`,
      payload,
    );
    return res.data;
  }

  async softDeletePublicHoliday(id: string) {
    const res = await this.$api.delete<ApiResponse<PublicHolidayDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async restorePublicHoliday(id: string) {
    const res = await this.$api.post<ApiResponse<PublicHolidayDTO>>(
      `${this.baseURL}/${id}/restore`,
    );
    return res.data;
  }
}
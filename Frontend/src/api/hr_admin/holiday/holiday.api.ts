// frontend/src/api/hr_admin/holiday/holiday.api.ts
import type {
  PublicHolidayDTO,
  PublicHolidayPaginatedDTO,
  PublicHolidayCreateDTO,
  PublicHolidayUpdateDTO,
  PublicHolidayListParams,
} from "./holiday.dto";

export class PublicHolidayApi {
  private baseUrl = "/api/hrms/admin/public-holidays";

  async getHolidays(
    params: PublicHolidayListParams = {}
  ): Promise<PublicHolidayPaginatedDTO> {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.append("page", params.page.toString());
    if (params.limit) queryParams.append("limit", params.limit.toString());
    if (params.q) queryParams.append("q", params.q);
    if (params.year) queryParams.append("year", params.year.toString());
    if (params.include_deleted !== undefined)
      queryParams.append("include_deleted", params.include_deleted.toString());
    if (params.deleted_only !== undefined)
      queryParams.append("deleted_only", params.deleted_only.toString());

    const response = await $fetch<PublicHolidayPaginatedDTO>(
      `${this.baseUrl}?${queryParams}`,
      { signal: params.signal }
    );
    return response;
  }

  async getHoliday(id: string): Promise<PublicHolidayDTO> {
    return await $fetch<PublicHolidayDTO>(`${this.baseUrl}/${id}`);
  }

  async getHolidaysByYear(
    year: number
  ): Promise<{ items: PublicHolidayDTO[]; year: number }> {
    return await $fetch<{ items: PublicHolidayDTO[]; year: number }>(
      `${this.baseUrl}/year/${year}`
    );
  }

  async createHoliday(data: PublicHolidayCreateDTO): Promise<PublicHolidayDTO> {
    return await $fetch<PublicHolidayDTO>(this.baseUrl, {
      method: "POST",
      body: data,
    });
  }

  async updateHoliday(
    id: string,
    data: PublicHolidayUpdateDTO
  ): Promise<PublicHolidayDTO> {
    return await $fetch<PublicHolidayDTO>(`${this.baseUrl}/${id}`, {
      method: "PATCH",
      body: data,
    });
  }

  async softDeleteHoliday(id: string): Promise<PublicHolidayDTO> {
    return await $fetch<PublicHolidayDTO>(`${this.baseUrl}/${id}/soft-delete`, {
      method: "DELETE",
    });
  }

  async restoreHoliday(id: string): Promise<PublicHolidayDTO> {
    return await $fetch<PublicHolidayDTO>(`${this.baseUrl}/${id}/restore`, {
      method: "POST",
    });
  }
}

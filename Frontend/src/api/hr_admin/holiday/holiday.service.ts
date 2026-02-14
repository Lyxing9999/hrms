// frontend/src/api/hr_admin/holiday/holiday.service.ts
import { PublicHolidayApi } from "./holiday.api";
import type {
  PublicHolidayDTO,
  PublicHolidayPaginatedDTO,
  PublicHolidayCreateDTO,
  PublicHolidayUpdateDTO,
  PublicHolidayListParams,
} from "./holiday.dto";

export class PublicHolidayService {
  private api: PublicHolidayApi;

  constructor() {
    this.api = new PublicHolidayApi();
  }

  async getHolidays(
    params: PublicHolidayListParams = {}
  ): Promise<PublicHolidayPaginatedDTO> {
    return await this.api.getHolidays(params);
  }

  async getHoliday(id: string): Promise<PublicHolidayDTO> {
    return await this.api.getHoliday(id);
  }

  async getHolidaysByYear(
    year: number
  ): Promise<{ items: PublicHolidayDTO[]; year: number }> {
    return await this.api.getHolidaysByYear(year);
  }

  async createHoliday(data: PublicHolidayCreateDTO): Promise<PublicHolidayDTO> {
    return await this.api.createHoliday(data);
  }

  async updateHoliday(
    id: string,
    data: PublicHolidayUpdateDTO
  ): Promise<PublicHolidayDTO> {
    return await this.api.updateHoliday(id, data);
  }

  async softDeleteHoliday(id: string): Promise<PublicHolidayDTO> {
    return await this.api.softDeleteHoliday(id);
  }

  async restoreHoliday(id: string): Promise<PublicHolidayDTO> {
    return await this.api.restoreHoliday(id);
  }
}

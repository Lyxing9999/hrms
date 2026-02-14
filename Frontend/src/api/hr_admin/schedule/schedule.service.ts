// frontend/src/api/hr_admin/schedule/schedule.service.ts
import { WorkingScheduleApi } from "./schedule.api";
import type {
  WorkingScheduleDTO,
  WorkingSchedulePaginatedDTO,
  WorkingScheduleCreateDTO,
  WorkingScheduleUpdateDTO,
  WorkingScheduleListParams,
} from "./schedule.dto";

export class WorkingScheduleService {
  private api: WorkingScheduleApi;

  constructor() {
    this.api = new WorkingScheduleApi();
  }

  async getSchedules(
    params: WorkingScheduleListParams = {}
  ): Promise<WorkingSchedulePaginatedDTO> {
    return await this.api.getSchedules(params);
  }

  async getSchedule(id: string): Promise<WorkingScheduleDTO> {
    return await this.api.getSchedule(id);
  }

  async getDefaultSchedule(): Promise<WorkingScheduleDTO> {
    return await this.api.getDefaultSchedule();
  }

  async createSchedule(
    data: WorkingScheduleCreateDTO
  ): Promise<WorkingScheduleDTO> {
    return await this.api.createSchedule(data);
  }

  async updateSchedule(
    id: string,
    data: WorkingScheduleUpdateDTO
  ): Promise<WorkingScheduleDTO> {
    return await this.api.updateSchedule(id, data);
  }

  async softDeleteSchedule(id: string): Promise<WorkingScheduleDTO> {
    return await this.api.softDeleteSchedule(id);
  }

  async restoreSchedule(id: string): Promise<WorkingScheduleDTO> {
    return await this.api.restoreSchedule(id);
  }
}

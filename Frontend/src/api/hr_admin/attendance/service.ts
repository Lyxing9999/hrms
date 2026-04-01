import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

import type {
  AttendanceApproveWrongLocationDTO,
  AttendanceCheckInDTO,
  AttendanceCheckOutDTO,
  AttendanceDTO,
  AttendanceListParams,
  AttendancePaginatedDTO,
  AttendanceTeamListParams,
  WrongLocationReportParams,
} from "./dto";

import { AttendanceApi } from "./api";

export class AttendanceService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly attendanceApi: AttendanceApi) {}

  async checkIn(payload: AttendanceCheckInDTO, options?: ApiCallOptions) {
    const data = await this.callApi<AttendanceDTO>(
      () => this.attendanceApi.checkIn(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async checkOut(payload: AttendanceCheckOutDTO, options?: ApiCallOptions) {
    const data = await this.callApi<AttendanceDTO>(
      () => this.attendanceApi.checkOut(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async reviewWrongLocation(
    attendanceId: string,
    payload: AttendanceApproveWrongLocationDTO,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<AttendanceDTO>(
      () => this.attendanceApi.reviewWrongLocation(attendanceId, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async getMyAttendance(options?: ApiCallOptions) {
    const data = await this.callApi<AttendancePaginatedDTO>(
      () => this.attendanceApi.getMyAttendance(),
      options,
    );
    // Return the first item (today's attendance) or undefined if no records exist
    return data?.items?.[0] ?? null;
  }

  async getAttendances(
    params?: AttendanceListParams,
    options?: ApiCallOptions,
  ): Promise<AttendancePaginatedDTO> {
    const data = await this.callApi<AttendancePaginatedDTO>(
      () => this.attendanceApi.getAttendances(params),
      options,
    );

    return (
      data ?? {
        items: [],
        total: 0,
        page: 1,
        page_size: 10,
        total_pages: 0,
      }
    );
  }

  async getTeamAttendances(
    params?: AttendanceTeamListParams,
    options?: ApiCallOptions,
  ): Promise<AttendancePaginatedDTO> {
    const data = await this.callApi<AttendancePaginatedDTO>(
      () => this.attendanceApi.getTeamAttendances(params),
      options,
    );

    return (
      data ?? {
        items: [],
        total: 0,
        page: 1,
        page_size: 10,
        total_pages: 0,
      }
    );
  }
  async getWrongLocationReports(
    params?: WrongLocationReportParams,
    options?: ApiCallOptions,
  ): Promise<AttendancePaginatedDTO> {
    const data = await this.callApi<AttendancePaginatedDTO>(
      () => this.attendanceApi.getWrongLocationReports(params),
      options,
    );

    return (
      data ?? {
        items: [],
        total: 0,
        page: 1,
        page_size: 10,
        total_pages: 0,
      }
    );
  }
}

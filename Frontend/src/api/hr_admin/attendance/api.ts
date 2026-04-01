import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";

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

export class AttendanceApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/attendance",
  ) {}

  async checkIn(payload: AttendanceCheckInDTO) {
    const res = await this.$api.post<ApiResponse<AttendanceDTO>>(
      `${this.baseURL}/check-in`,
      payload,
    );
    return res.data;
  }

  async checkOut(payload: AttendanceCheckOutDTO) {
    const res = await this.$api.post<ApiResponse<AttendanceDTO>>(
      `${this.baseURL}/check-out`,
      payload,
    );
    return res.data;
  }

  async reviewWrongLocation(
    attendanceId: string,
    payload: AttendanceApproveWrongLocationDTO,
  ) {
    const res = await this.$api.post<ApiResponse<AttendanceDTO>>(
      `${this.baseURL}/${attendanceId}/wrong-location/review`,
      payload,
    );
    return res.data;
  }

  async getMyAttendance() {
    const res = await this.$api.get<ApiResponse<AttendancePaginatedDTO>>(
      `${this.baseURL}/me`,
    );
    return res.data;
  }

  async getAttendances(params?: AttendanceListParams) {
    const res = await this.$api.get<ApiResponse<AttendancePaginatedDTO>>(
      this.baseURL,
      {
        params,
      },
    );
    return res.data;
  }

  async getTeamAttendances(params?: AttendanceTeamListParams) {
    const res = await this.$api.get<ApiResponse<AttendancePaginatedDTO>>(
      `${this.baseURL}/team`,
      {
        params,
      },
    );
    return res.data;
  }

  async getWrongLocationReports(params?: WrongLocationReportParams) {
    const res = await this.$api.get<ApiResponse<AttendancePaginatedDTO>>(
      `${this.baseURL}/reports/wrong-location`,
      {
        params,
      },
    );
    return res.data;
  }
}

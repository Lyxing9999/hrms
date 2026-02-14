// frontend/src/api/hr_admin/attendance/attendance.api.ts
import type { AxiosInstance } from "axios";
import type {
  AttendanceDTO,
  AttendancePaginatedDTO,
  AttendanceCheckInDTO,
  AttendanceCheckOutDTO,
  AttendanceUpdateDTO,
  AttendanceStatsDTO,
  AttendanceListParams,
  AttendanceStatsParams,
} from "./attendance.dto";

/**
 * Attendance API - Low-level HTTP calls
 * Responsible for building URLs, choosing HTTP methods, passing params/body
 * Returns raw backend response
 */
export class AttendanceAPI {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms"
  ) {}

  // ============
  // EMPLOYEE ENDPOINTS
  // ============

  async checkIn(data: AttendanceCheckInDTO) {
    return this.$api
      .post<AttendanceDTO>(`${this.baseURL}/employee/attendance/check-in`, data)
      .then((res) => res.data);
  }

  async checkOut(attendanceId: string, data: AttendanceCheckOutDTO) {
    return this.$api
      .post<AttendanceDTO>(
        `${this.baseURL}/employee/attendance/${attendanceId}/check-out`,
        data
      )
      .then((res) => res.data);
  }

  async getTodayAttendance(employeeId?: string) {
    return this.$api
      .get<AttendanceDTO | null>(`${this.baseURL}/employee/attendance/today`, {
        params: employeeId ? { employee_id: employeeId } : undefined,
      })
      .then((res) => res.data);
  }

  async getMyAttendanceHistory(params?: Omit<AttendanceListParams, 'employee_id'>) {
    return this.$api
      .get<AttendancePaginatedDTO>(`${this.baseURL}/employee/attendance/history`, {
        params: {
          start_date: params?.start_date ?? undefined,
          end_date: params?.end_date ?? undefined,
          status: params?.status ?? undefined,
          page: params?.page ?? 1,
          limit: params?.limit ?? 10,
        },
        signal: params?.signal,
      })
      .then((res) => res.data);
  }

  async getMyAttendanceStats(params: Omit<AttendanceStatsParams, 'employee_id'>) {
    return this.$api
      .get<AttendanceStatsDTO>(`${this.baseURL}/employee/attendance/stats`, {
        params: {
          start_date: params.start_date,
          end_date: params.end_date,
        },
      })
      .then((res) => res.data);
  }

  // ============
  // EMPLOYEE-SPECIFIC ENDPOINTS (by ID)
  // ============

  async getEmployeeAttendanceHistory(employeeId: string, params?: Omit<AttendanceListParams, 'employee_id'>) {
    return this.$api
      .get<AttendancePaginatedDTO>(`${this.baseURL}/employees/${employeeId}/attendance/history`, {
        params: {
          start_date: params?.start_date ?? undefined,
          end_date: params?.end_date ?? undefined,
          status: params?.status ?? undefined,
          page: params?.page ?? 1,
          limit: params?.limit ?? 10,
        },
        signal: params?.signal,
      })
      .then((res) => res.data);
  }

  async getEmployeeAttendanceStats(employeeId: string, params: Omit<AttendanceStatsParams, 'employee_id'>) {
    return this.$api
      .get<AttendanceStatsDTO>(`${this.baseURL}/employees/${employeeId}/attendance/stats`, {
        params: {
          start_date: params.start_date,
          end_date: params.end_date,
        },
      })
      .then((res) => res.data);
  }

  // ============
  // ADMIN ENDPOINTS
  // ============

  async getAttendances(params?: AttendanceListParams) {
    return this.$api
      .get<AttendancePaginatedDTO>(`${this.baseURL}/admin/attendances`, {
        params: {
          employee_id: params?.employee_id ?? undefined,
          start_date: params?.start_date ?? undefined,
          end_date: params?.end_date ?? undefined,
          status: params?.status ?? undefined,
          include_deleted: params?.include_deleted ?? undefined,
          deleted_only: params?.deleted_only ?? undefined,
          page: params?.page ?? 1,
          limit: params?.limit ?? 10,
        },
        signal: params?.signal,
      })
      .then((res) => res.data);
  }

  async getAttendance(id: string) {
    return this.$api
      .get<AttendanceDTO>(`${this.baseURL}/admin/attendances/${id}`)
      .then((res) => res.data);
  }

  async updateAttendance(id: string, data: AttendanceUpdateDTO) {
    return this.$api
      .patch<AttendanceDTO>(`${this.baseURL}/admin/attendances/${id}`, data)
      .then((res) => res.data);
  }

  async getAttendanceStats(params: AttendanceStatsParams) {
    return this.$api
      .get<AttendanceStatsDTO>(`${this.baseURL}/admin/attendances/stats`, {
        params: {
          employee_id: params.employee_id,
          start_date: params.start_date,
          end_date: params.end_date,
        },
      })
      .then((res) => res.data);
  }

  async softDeleteAttendance(id: string) {
    return this.$api
      .delete<AttendanceDTO>(`${this.baseURL}/admin/attendances/${id}/soft-delete`)
      .then((res) => res.data);
  }

  async restoreAttendance(id: string) {
    return this.$api
      .post<AttendanceDTO>(`${this.baseURL}/admin/attendances/${id}/restore`)
      .then((res) => res.data);
  }
}

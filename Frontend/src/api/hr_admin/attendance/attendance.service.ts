// frontend/src/api/hr_admin/attendance/attendance.service.ts
import type { AttendanceAPI } from "./attendance.api";
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
 * Attendance Service - High-level wrapper
 * Handles app policy & behavior
 * Can add caching, validation, business rules, toast messages, etc.
 */
export class AttendanceService {
  constructor(private readonly attendanceApi: AttendanceAPI) {}

  // ============
  // EMPLOYEE ENDPOINTS
  // ============

  async checkIn(data: AttendanceCheckInDTO): Promise<AttendanceDTO> {
    return await this.attendanceApi.checkIn(data);
  }

  async checkOut(
    attendanceId: string,
    data: AttendanceCheckOutDTO
  ): Promise<AttendanceDTO> {
    return await this.attendanceApi.checkOut(attendanceId, data);
  }

  async getTodayAttendance(employeeId?: string): Promise<AttendanceDTO | null> {
    return await this.attendanceApi.getTodayAttendance(employeeId);
  }

  async getMyAttendanceHistory(
    params?: Omit<AttendanceListParams, 'employee_id'>
  ): Promise<AttendancePaginatedDTO> {
    return await this.attendanceApi.getMyAttendanceHistory(params);
  }

  async getMyAttendanceStats(
    params: Omit<AttendanceStatsParams, 'employee_id'>
  ): Promise<AttendanceStatsDTO> {
    return await this.attendanceApi.getMyAttendanceStats(params);
  }

  // ============
  // EMPLOYEE-SPECIFIC ENDPOINTS (by ID)
  // ============

  async getEmployeeAttendanceHistory(
    employeeId: string,
    params?: Omit<AttendanceListParams, 'employee_id'>
  ): Promise<AttendancePaginatedDTO> {
    return await this.attendanceApi.getEmployeeAttendanceHistory(employeeId, params);
  }

  async getEmployeeAttendanceStats(
    employeeId: string,
    params: Omit<AttendanceStatsParams, 'employee_id'>
  ): Promise<AttendanceStatsDTO> {
    return await this.attendanceApi.getEmployeeAttendanceStats(employeeId, params);
  }

  // ============
  // ADMIN ENDPOINTS
  // ============

  async getAttendances(
    params?: AttendanceListParams
  ): Promise<AttendancePaginatedDTO> {
    return await this.attendanceApi.getAttendances(params);
  }

  async getAttendance(id: string): Promise<AttendanceDTO> {
    return await this.attendanceApi.getAttendance(id);
  }

  async updateAttendance(
    id: string,
    data: AttendanceUpdateDTO
  ): Promise<AttendanceDTO> {
    return await this.attendanceApi.updateAttendance(id, data);
  }

  async getAttendanceStats(params: AttendanceStatsParams): Promise<AttendanceStatsDTO> {
    return await this.attendanceApi.getAttendanceStats(params);
  }

  async softDeleteAttendance(id: string): Promise<AttendanceDTO> {
    return await this.attendanceApi.softDeleteAttendance(id);
  }

  async restoreAttendance(id: string): Promise<AttendanceDTO> {
    return await this.attendanceApi.restoreAttendance(id);
  }
}

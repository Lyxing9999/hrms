// frontend/src/api/hr_admin/attendance/attendance.dto.ts
import type { LifecycleDTO } from "~/api/types/lifecycle.dto";

/**
 * Attendance status types
 */
export type AttendanceStatus = "checked_in" | "checked_out" | "late" | "early_leave";

/**
 * Attendance record DTO
 */
export interface AttendanceDTO {
  id: string;
  employee_id: string;
  check_in_time: string; // ISO datetime
  check_out_time: string | null;
  location_id: string | null;
  check_in_latitude: number | null;
  check_in_longitude: number | null;
  check_out_latitude: number | null;
  check_out_longitude: number | null;
  status: string;
  notes: string | null;
  late_minutes: number;
  early_leave_minutes: number;
  lifecycle: LifecycleDTO;
}

/**
 * Paginated attendance response
 */
export interface AttendancePaginatedDTO {
  items: AttendanceDTO[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/**
 * Check-in request payload
 */
export interface AttendanceCheckInDTO {
  employee_id?: string;
  location_id?: string;
  latitude?: number;
  longitude?: number;
  notes?: string;
}

/**
 * Check-out request payload
 */
export interface AttendanceCheckOutDTO {
  latitude?: number;
  longitude?: number;
  notes?: string;
}

/**
 * Update attendance request payload (admin only)
 */
export interface AttendanceUpdateDTO {
  check_in_time?: string;
  check_out_time?: string;
  location_id?: string;
  notes?: string;
  late_minutes?: number;
  early_leave_minutes?: number;
}

/**
 * Attendance statistics DTO
 */
export interface AttendanceStatsDTO {
  total_days: number;
  present_days: number;
  late_days: number;
  early_leave_days: number;
  total_late_minutes: number;
  total_early_leave_minutes: number;
  attendance_rate: number;
}

/**
 * List attendances query parameters
 */
export interface AttendanceListParams {
  employee_id?: string;
  start_date?: string; // ISO date
  end_date?: string; // ISO date
  status?: string;
  include_deleted?: boolean;
  deleted_only?: boolean;
  page?: number;
  limit?: number;
}

/**
 * Attendance statistics query parameters
 */
export interface AttendanceStatsParams {
  employee_id: string;
  start_date: string; // ISO date
  end_date: string; // ISO date
}

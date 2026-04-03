import type { LifecycleDTO } from "~/api/types/lifecycle.dto";

export type AttendanceStatus =
  | "checked_in"
  | "checked_out"
  | "late"
  | "early_leave"
  | "absent"
  | "holiday_off"
  | "weekend_off"
  | "wrong_location_pending"
  | "wrong_location_approved"
  | "wrong_location_rejected";

export interface AttendanceDTO {
  id: string;
  employee_id?: string | null;
  attendance_date: string;

  check_in_time?: string | null;
  check_out_time?: string | null;

  schedule_id?: string | null;
  location_id?: string | null;

  check_in_latitude?: number | null;
  check_in_longitude?: number | null;
  check_out_latitude?: number | null;
  check_out_longitude?: number | null;

  status: AttendanceStatus | string;
  notes?: string | null;
  late_minutes: number;
  early_leave_minutes: number;

  wrong_location_reason?: string | null;
  admin_comment?: string | null;
  location_reviewed_by?: string | null;

  lifecycle: LifecycleDTO;
}

export interface AttendancePaginatedDTO {
  items: AttendanceDTO[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface AttendanceCheckInDTO {
  check_in_time: string;
  latitude: number;
  longitude: number;
  wrong_location_reason?: string | null;
  late_reason?: string | null;
}

export interface AttendanceCheckOutDTO {
  check_out_time: string;
  latitude?: number | null;
  longitude?: number | null;
  early_leave_reason?: string | null;
}

export interface AttendanceApproveWrongLocationDTO {
  approved: boolean;
  comment?: string | null;
}

export interface AttendanceListParams {
  employee_id?: string;
  status?: string;
  page?: number;
  page_size?: number;
  start_date?: string;
  end_date?: string;
}

export interface AttendanceTeamListParams {
  employee_id?: string;
  status?: string;
  page?: number;
  page_size?: number;
  start_date?: string;
  end_date?: string;
  department_id?: string;
}

export interface WrongLocationReportItemDTO {
  id: string;
  employee_id?: string | null;
  attendance_date: string;
  check_in_time?: string | null;
  check_out_time?: string | null;
  schedule_id?: string | null;
  location_id?: string | null;
  check_in_latitude?: number | null;
  check_in_longitude?: number | null;
  check_out_latitude?: number | null;
  check_out_longitude?: number | null;
  status: string;
  notes?: string | null;
  late_minutes: number;
  early_leave_minutes: number;
  wrong_location_reason?: string | null;
  admin_comment?: string | null;
  location_reviewed_by?: string | null;
  lifecycle: LifecycleDTO;
}

export interface WrongLocationReportParams {
  page?: number;
  page_size?: number;
  start_date?: string;
  end_date?: string;
  employee_id?: string;
  status?: string;
}

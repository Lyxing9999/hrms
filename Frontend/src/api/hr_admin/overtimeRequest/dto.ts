import type { LifecycleDTO } from "~/api/types/lifecycle.dto";

export type OvertimeRequestStatus =
  | "pending"
  | "approved"
  | "rejected"
  | "cancelled";

export interface OvertimeRequestDTO {
  id: string;
  employee_id: string;
  request_date: string; // YYYY-MM-DD
  start_time: string; // ISO or HH:MM:SS based on backend
  end_time: string; // ISO or HH:MM:SS based on backend
  requested_hours: number;
  reason: string;
  status: OvertimeRequestStatus;
  manager_comment: string | null;
  approved_by: string | null;
  approved_at: string | null;
  lifecycle: LifecycleDTO;
}

export interface OvertimeRequestCreateDTO {
  request_date: string; // YYYY-MM-DD
  start_time: string;
  end_time: string;
  reason: string;
}

export interface OvertimeRequestUpdateDTO {
  request_date?: string;
  start_time?: string;
  end_time?: string;
  reason?: string;
}

export interface OvertimeRequestReviewDTO {
  approved: boolean;
  comment?: string | null;
}

export interface OvertimeRequestListParams {
  status?: OvertimeRequestStatus;
  year?: number;
  month?: number;
  signal?: AbortSignal;
}

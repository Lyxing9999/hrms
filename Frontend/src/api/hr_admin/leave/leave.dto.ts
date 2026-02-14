// frontend/src/api/hr_admin/leave/leave.dto.ts

export interface LifecycleDTO {
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
  deleted_by: string | null;
}

export interface LeaveDTO {
  id: string;
  employee_id: string;
  leave_type: "annual" | "sick" | "unpaid" | "other";
  start_date: string; // ISO date
  end_date: string; // ISO date
  reason: string;
  contract_start: string; // ISO date
  contract_end: string; // ISO date
  is_paid: boolean;
  status: "pending" | "approved" | "rejected" | "cancelled";
  manager_user_id: string | null;
  manager_comment: string | null;
  lifecycle: LifecycleDTO;
}

export interface LeavePaginatedDTO {
  items: LeaveDTO[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface LeaveCreateDTO {
  employee_id?: string; // Optional, can be extracted from token
  leave_type: "annual" | "sick" | "unpaid" | "other";
  start_date: string; // YYYY-MM-DD
  end_date: string; // YYYY-MM-DD
  reason: string;
}

export interface LeaveUpdateDTO {
  leave_type?: "annual" | "sick" | "unpaid" | "other";
  start_date?: string;
  end_date?: string;
  reason?: string;
}

export interface LeaveReviewDTO {
  comment?: string;
}

export interface ListLeavesParams {
  q?: string;
  page?: number;
  limit?: number;
  employee_id?: string;
  status?: "pending" | "approved" | "rejected" | "cancelled";
  include_deleted?: boolean;
  deleted_only?: boolean;
  signal?: AbortSignal;
}

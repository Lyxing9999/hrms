import type { ApiResponse } from "~/api/types/common/api-response.type";

export type HrEmployeeDTO = {
  id: string;
  employee_code: string;
  full_name: string;
  department?: string | null;
  position?: string | null;
  employment_type?: "permanent" | "contract";
  status?: "active" | "inactive";
  photo_url?: string | null;
  lifecycle?: { deleted_at?: string | null } | null;
};

export type HrCreateEmployeeDTO = {
  employee_code: string;
  full_name: string;
  department?: string | null;
  position?: string | null;
  employment_type?: "permanent" | "contract";
  contract?: {
    start_date: string;
    end_date: string;
    salary_type: "monthly" | "daily" | "hourly";
    rate: number;
    pay_on_holiday?: boolean;
    pay_on_weekend?: boolean;
  } | null;
  status?: "active" | "inactive";
};

export type HrUpdateEmployeeDTO = Partial<HrCreateEmployeeDTO>;

export type HrEmployeePaginatedDTO = {
  items: HrEmployeeDTO[];
  total: number;
  page?: number;
  page_size?: number;
  total_pages?: number;
};

export type ListEmployeesParams = {
  q?: string;
  page?: number;
  limit?: number;
  include_deleted?: boolean;
  deleted_only?: boolean;
};

// Wrapped responses
export type HrGetEmployeesResponse = ApiResponse<HrEmployeePaginatedDTO>;
export type HrGetEmployeeResponse = ApiResponse<HrEmployeeDTO>;
export type HrCreateEmployeeResponse = ApiResponse<HrEmployeeDTO>;
export type HrUpdateEmployeeResponse = ApiResponse<HrEmployeeDTO>;
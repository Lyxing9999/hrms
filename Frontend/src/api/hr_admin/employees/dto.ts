import type { ApiResponse } from "~/api/types/common/api-response.type";

export type HrEmploymentType = "permanent" | "contract";
export type HrEmployeeStatus = "active" | "inactive";
export type HrSalaryType = "monthly" | "daily" | "hourly";

export type HrContractDTO = {
  start_date: string;
  end_date: string;
  salary_type: HrSalaryType;
  rate: number;
  leave_policy_id?: string | null;
  pay_on_holiday?: boolean;
  pay_on_weekend?: boolean;
};

export type HrEmployeeDTO = {
  id: string;
  user_id?: string | null;

  employee_code: string;
  full_name: string;
  department?: string | null;
  position?: string | null;

  employment_type: HrEmploymentType;

  basic_salary: number;
  contract?: HrContractDTO | null;

  manager_user_id?: string | null;
  schedule_id?: string | null;

  status: HrEmployeeStatus;

  created_by?: string | null;
  photo_url?: string | null;

  lifecycle?: {
    created_at?: string;
    updated_at?: string;
    deleted_at?: string | null;
  } | null;
};

export type HrCreateEmployeeDTO = {
  employee_code: string;
  full_name: string;

  department?: string | null;
  position?: string | null;

  employment_type?: HrEmploymentType;
  basic_salary: number;

  contract?: HrContractDTO | null;

  manager_user_id?: string | null;
  schedule_id?: string | null;

  status?: HrEmployeeStatus;
  photo_url?: string | null;
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

export type HrGetEmployeesResponse = ApiResponse<HrEmployeePaginatedDTO>;
export type HrGetEmployeeResponse = ApiResponse<HrEmployeeDTO>;
export type HrCreateEmployeeResponse = ApiResponse<HrEmployeeDTO>;
export type HrUpdateEmployeeResponse = ApiResponse<HrEmployeeDTO>;

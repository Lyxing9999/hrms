import type { ApiResponse } from "~/api/types/common/api-response.type";
import type { Role } from "~/api/types/enums/role.enum";

export type HrEmploymentType = "permanent" | "contract";
export type HrEmployeeStatus = "active" | "inactive";

export type HrEmployeeDTO = {
  id: string;
  user_id?: string | null;
  employee_code: string;
  full_name: string;
  department?: string | null;
  position?: string | null;
  employment_type: HrEmploymentType;
  basic_salary: number;
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
  status?: HrEmployeeStatus;
};

export type HrUpdateEmployeeDTO = Partial<HrCreateEmployeeDTO>;

export type ListEmployeesParams = {
  q?: string;
  page?: number;
  limit?: number;
  include_deleted?: boolean;
  deleted_only?: boolean;
  with_accounts?: boolean;
};

export interface HrEmployeeAccountDTO {
  id: string;
  email?: string | null;
  username?: string | null;
  role?: string | null;
  status?: string | null;
}

export interface HrCreateEmployeeAccountDTO {
  username?: string;
  email: string;
  password: string;
  role: Role;
}

export interface HrEmployeeWithAccountDTO {
  employee: HrEmployeeDTO;
  user: HrEmployeeAccountDTO | null;
}

export interface HrEmployeeWithAccountSummaryDTO {
  employee: HrEmployeeDTO;
  account?: HrEmployeeAccountDTO | null;
}

export interface HrEmployeeWithAccountSummaryPaginatedDTO {
  items: HrEmployeeWithAccountSummaryDTO[];
  total: number;
  page?: number;
  page_size?: number;
  total_pages?: number;
}

export type HrGetEmployeesWithAccountsResponse =
  ApiResponse<HrEmployeeWithAccountSummaryPaginatedDTO>;
export type HrGetEmployeeResponse = ApiResponse<HrEmployeeDTO>;
export type HrCreateEmployeeResponse = ApiResponse<HrEmployeeDTO>;
export type HrUpdateEmployeeResponse = ApiResponse<HrEmployeeDTO>;
export type HrGetEmployeeAccountResponse =
  ApiResponse<HrEmployeeAccountDTO | null>;
export type HrCreateEmployeeAccountResponse =
  ApiResponse<HrEmployeeWithAccountDTO>;
export type HrSoftDeleteEmployeeAccountResponse =
  ApiResponse<HrEmployeeAccountDTO>;
export type HrRestoreEmployeeAccountResponse =
  ApiResponse<HrEmployeeAccountDTO>;

export type ListEmployeeAccountsParams = {
  q?: string;
  page?: number;
  limit?: number;
  include_deleted?: boolean;
  deleted_only?: boolean;
  status?: string;
};

export interface HrEmployeeAccountListItemDTO {
  id: string;
  email?: string | null;
  username?: string | null;
  role?: string | null;
  status?: string | null;
}

export interface HrEmployeeAccountPaginatedDTO {
  items: HrEmployeeAccountListItemDTO[];
  total: number;
  page?: number;
  page_size?: number;
  total_pages?: number;
}

export interface HrLinkEmployeeAccountDTO {
  user_id: string;
}

export type HrGetEmployeeAccountsResponse =
  ApiResponse<HrEmployeeAccountPaginatedDTO>;

export type HrLinkEmployeeAccountResponse = ApiResponse<HrEmployeeDTO>;

export interface HrUpdateEmployeeAccountDTO {
  email?: string;
  username?: string;
  password?: string;
}

export interface HrPasswordResetResponse {
  message: string;
  reset_link?: string;
}

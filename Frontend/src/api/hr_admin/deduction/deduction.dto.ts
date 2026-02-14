// frontend/src/api/hr_admin/deduction/deduction.dto.ts
import type { LifecycleDTO } from "~/api/types/lifecycle.dto";

export type DeductionType = "late" | "absent" | "early_leave";

export interface DeductionRuleDTO {
  id: string;
  type: DeductionType;
  min_minutes: number;
  max_minutes: number;
  deduction_percentage: number;
  is_active: boolean;
  created_by: string | null;
  lifecycle: LifecycleDTO;
}

export interface DeductionRulePaginatedDTO {
  items: DeductionRuleDTO[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface DeductionRuleCreateDTO {
  type: DeductionType;
  min_minutes: number;
  max_minutes: number;
  deduction_percentage: number;
  is_active?: boolean;
}

export interface DeductionRuleUpdateDTO {
  type?: DeductionType;
  min_minutes?: number;
  max_minutes?: number;
  deduction_percentage?: number;
  is_active?: boolean;
}

export interface DeductionRuleListParams {
  page?: number;
  limit?: number;
  type?: DeductionType;
  is_active?: boolean;
  include_deleted?: boolean;
  deleted_only?: boolean;
  signal?: AbortSignal;
}

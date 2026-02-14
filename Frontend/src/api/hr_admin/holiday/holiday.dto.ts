// frontend/src/api/hr_admin/holiday/holiday.dto.ts
import type { LifecycleDTO } from "~/api/types/lifecycle.dto";

export interface PublicHolidayDTO {
  id: string;
  name: string;
  name_kh: string | null;
  date: string; // YYYY-MM-DD
  is_paid: boolean;
  description: string | null;
  created_by: string | null;
  lifecycle: LifecycleDTO;
}

export interface PublicHolidayPaginatedDTO {
  items: PublicHolidayDTO[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PublicHolidayCreateDTO {
  name: string;
  name_kh?: string;
  date: string;
  is_paid?: boolean;
  description?: string;
}

export interface PublicHolidayUpdateDTO {
  name?: string;
  name_kh?: string;
  date?: string;
  is_paid?: boolean;
  description?: string;
}

export interface PublicHolidayListParams {
  page?: number;
  limit?: number;
  q?: string;
  year?: number;
  include_deleted?: boolean;
  deleted_only?: boolean;
  signal?: AbortSignal;
}

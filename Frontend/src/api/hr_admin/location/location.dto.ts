// frontend/src/api/hr_admin/location/location.dto.ts
import type { LifecycleDTO } from "~/api/types/lifecycle.dto";

export interface WorkLocationDTO {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  radius_meters: number;
  is_active: boolean;
  created_by: string | null;
  lifecycle: LifecycleDTO;
}

export interface WorkLocationPaginatedDTO {
  items: WorkLocationDTO[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface WorkLocationCreateDTO {
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  radius_meters: number;
  is_active?: boolean;
}

export interface WorkLocationUpdateDTO {
  name?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  radius_meters?: number;
  is_active?: boolean;
}

export interface WorkLocationListParams {
  page?: number;
  limit?: number;
  q?: string;
  is_active?: boolean;
  include_deleted?: boolean;
  deleted_only?: boolean;
  signal?: AbortSignal;
}

export interface WorkLocationDto {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  radius_meters: number;
  is_active: boolean;
  lifecycle: {
    created_at: string;
    updated_at: string;
    deleted_at: string | null;
  };
}

export interface CreateWorkLocationDto {
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  radius_meters: number;
  is_active: boolean;
}

export interface UpdateWorkLocationDto {
  name?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  radius_meters?: number;
  is_active?: boolean;
}

export interface WorkLocationSelectOption {
  value: string;
  label: string;
  address: string;
  coordinates: {
    latitude: number;
    longitude: number;
  };
}

export interface WorkLocationFilters {
  search?: string;
  status?: 'all' | 'active' | 'inactive';
  deleted_mode?: 'normal' | 'include_deleted' | 'deleted_only';
}

export interface WorkLocationListResponse {
  data: WorkLocationDto[];
  total: number;
  page: number;
  limit: number;
}

export interface GooglePlaceResult {
  place_id: string;
  formatted_address: string;
  geometry: {
    location: {
      lat: number;
      lng: number;
    };
  };
  name: string;
}
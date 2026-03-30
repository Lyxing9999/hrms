import type {
  WorkLocationDto,
  CreateWorkLocationDto,
  UpdateWorkLocationDto,
  WorkLocationSelectOption,
  WorkLocationFilters,
  WorkLocationListResponse,
} from '~/types/hr/work-location.dto';

export class WorkLocationApi {
  private baseUrl: string;

  constructor() {
    const config = useRuntimeConfig();
    this.baseUrl = config.public.apiBase;
  }

  async getWorkLocations(
    filters: WorkLocationFilters = {},
    page = 1,
    limit = 20
  ): Promise<WorkLocationListResponse> {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
      ...Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value !== undefined && value !== '')
      ),
    });

    const { data } = await $fetch<{ data: WorkLocationListResponse }>(
      `/hr/work-locations?${params}`,
      {
        baseURL: this.baseUrl,
        method: 'GET',
      }
    );

    return data;
  }

  async getWorkLocation(id: string): Promise<WorkLocationDto> {
    const { data } = await $fetch<{ data: WorkLocationDto }>(
      `/hr/work-locations/${id}`,
      {
        baseURL: this.baseUrl,
        method: 'GET',
      }
    );

    return data;
  }

  async getWorkLocationSelectOptions(): Promise<WorkLocationSelectOption[]> {
    const { data } = await $fetch<{ data: WorkLocationSelectOption[] }>(
      '/hr/work-locations/select-options',
      {
        baseURL: this.baseUrl,
        method: 'GET',
      }
    );

    return data;
  }

  async createWorkLocation(payload: CreateWorkLocationDto): Promise<WorkLocationDto> {
    const { data } = await $fetch<{ data: WorkLocationDto }>(
      '/hr/work-locations',
      {
        baseURL: this.baseUrl,
        method: 'POST',
        body: payload,
      }
    );

    return data;
  }

  async updateWorkLocation(
    id: string,
    payload: UpdateWorkLocationDto
  ): Promise<WorkLocationDto> {
    const { data } = await $fetch<{ data: WorkLocationDto }>(
      `/hr/work-locations/${id}`,
      {
        baseURL: this.baseUrl,
        method: 'PUT',
        body: payload,
      }
    );

    return data;
  }

  async activateWorkLocation(id: string): Promise<WorkLocationDto> {
    const { data } = await $fetch<{ data: WorkLocationDto }>(
      `/hr/work-locations/${id}/activate`,
      {
        baseURL: this.baseUrl,
        method: 'POST',
      }
    );

    return data;
  }

  async deactivateWorkLocation(id: string): Promise<WorkLocationDto> {
    const { data } = await $fetch<{ data: WorkLocationDto }>(
      `/hr/work-locations/${id}/deactivate`,
      {
        baseURL: this.baseUrl,
        method: 'POST',
      }
    );

    return data;
  }

  async softDeleteWorkLocation(id: string): Promise<void> {
    await $fetch(`/hr/work-locations/${id}`, {
      baseURL: this.baseUrl,
      method: 'DELETE',
    });
  }

  async restoreWorkLocation(id: string): Promise<WorkLocationDto> {
    const { data } = await $fetch<{ data: WorkLocationDto }>(
      `/hr/work-locations/${id}/restore`,
      {
        baseURL: this.baseUrl,
        method: 'POST',
      }
    );

    return data;
  }
}
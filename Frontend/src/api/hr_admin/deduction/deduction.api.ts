// frontend/src/api/hr_admin/deduction/deduction.api.ts
import type {
  DeductionRuleDTO,
  DeductionRulePaginatedDTO,
  DeductionRuleCreateDTO,
  DeductionRuleUpdateDTO,
  DeductionRuleListParams,
  DeductionType,
} from "./deduction.dto";

export class DeductionRuleApi {
  private baseUrl = "/api/hrms/admin/deduction-rules";

  async getRules(
    params: DeductionRuleListParams = {}
  ): Promise<DeductionRulePaginatedDTO> {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.append("page", params.page.toString());
    if (params.limit) queryParams.append("limit", params.limit.toString());
    if (params.type) queryParams.append("type", params.type);
    if (params.is_active !== undefined)
      queryParams.append("is_active", params.is_active.toString());
    if (params.include_deleted !== undefined)
      queryParams.append("include_deleted", params.include_deleted.toString());
    if (params.deleted_only !== undefined)
      queryParams.append("deleted_only", params.deleted_only.toString());

    const response = await $fetch<DeductionRulePaginatedDTO>(
      `${this.baseUrl}?${queryParams}`,
      { signal: params.signal }
    );
    return response;
  }

  async getRule(id: string): Promise<DeductionRuleDTO> {
    return await $fetch<DeductionRuleDTO>(`${this.baseUrl}/${id}`);
  }

  async getActiveRules(): Promise<{ items: DeductionRuleDTO[] }> {
    return await $fetch<{ items: DeductionRuleDTO[] }>(
      `${this.baseUrl}/active`
    );
  }

  async getRulesByType(
    type: DeductionType
  ): Promise<{ items: DeductionRuleDTO[]; type: DeductionType }> {
    return await $fetch<{ items: DeductionRuleDTO[]; type: DeductionType }>(
      `${this.baseUrl}/type/${type}`
    );
  }

  async createRule(data: DeductionRuleCreateDTO): Promise<DeductionRuleDTO> {
    return await $fetch<DeductionRuleDTO>(this.baseUrl, {
      method: "POST",
      body: data,
    });
  }

  async updateRule(
    id: string,
    data: DeductionRuleUpdateDTO
  ): Promise<DeductionRuleDTO> {
    return await $fetch<DeductionRuleDTO>(`${this.baseUrl}/${id}`, {
      method: "PATCH",
      body: data,
    });
  }

  async softDeleteRule(id: string): Promise<DeductionRuleDTO> {
    return await $fetch<DeductionRuleDTO>(`${this.baseUrl}/${id}/soft-delete`, {
      method: "DELETE",
    });
  }

  async restoreRule(id: string): Promise<DeductionRuleDTO> {
    return await $fetch<DeductionRuleDTO>(`${this.baseUrl}/${id}/restore`, {
      method: "POST",
    });
  }
}

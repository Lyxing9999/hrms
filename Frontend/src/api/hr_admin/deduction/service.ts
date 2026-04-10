import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

import type {
  DeductionRuleDTO,
  DeductionRuleCreateDTO,
  DeductionRuleUpdateDTO,
  DeductionRuleListParams,
  DeductionRuleApplicableParams,
  DeductionRuleListResponseDTO,
} from "./dto";

import { DeductionRuleApi } from "./api";

export class DeductionRuleService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly deductionRuleApi: DeductionRuleApi) {}

  /**
   * Create a new deduction rule
   * POST /api/hrms/deduction-rules
   */
  async createRule(
    payload: DeductionRuleCreateDTO,
    options?: ApiCallOptions,
  ): Promise<DeductionRuleDTO> {
    const data = await this.callApi<DeductionRuleDTO>(
      () => this.deductionRuleApi.createRule(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  /**
   * Get all deduction rules
   * GET /api/hrms/deduction-rules
   */
  async getRules(
    params?: DeductionRuleListParams,
    options?: ApiCallOptions,
  ): Promise<DeductionRuleListResponseDTO> {
    const data = await this.callApi<DeductionRuleListResponseDTO>(
      () => this.deductionRuleApi.getRules(params),
      options,
    );
    return (
      data ?? {
        items: [],
        total: 0,
        page: 1,
        page_size: 10,
        total_pages: 0,
      }
    );
  }

  /**
   * Get a specific deduction rule
   * GET /api/hrms/deduction-rules/<rule_id>
   */
  async getRule(
    id: string,
    options?: ApiCallOptions,
  ): Promise<DeductionRuleDTO> {
    const data = await this.callApi<DeductionRuleDTO>(
      () => this.deductionRuleApi.getRule(id),
      options,
    );
    return data!;
  }

  /**
   * Find applicable deduction rule
   * GET /api/hrms/deduction-rules/applicable
   */
  async getApplicableRule(
    params: DeductionRuleApplicableParams,
    options?: ApiCallOptions,
  ): Promise<DeductionRuleDTO | null> {
    const data = await this.callApi<DeductionRuleDTO | null>(
      () => this.deductionRuleApi.getApplicableRule(params),
      options,
    );
    return data ?? null;
  }

  /**
   * Update a deduction rule
   * PATCH /api/hrms/deduction-rules/<rule_id>
   */
  async updateRule(
    id: string,
    payload: DeductionRuleUpdateDTO,
    options?: ApiCallOptions,
  ): Promise<DeductionRuleDTO> {
    const data = await this.callApi<DeductionRuleDTO>(
      () => this.deductionRuleApi.updateRule(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  /**
   * Soft delete a deduction rule
   * DELETE /api/hrms/deduction-rules/<rule_id>
   */
  async deleteRule(
    id: string,
    options?: ApiCallOptions,
  ): Promise<DeductionRuleDTO> {
    const data = await this.callApi<DeductionRuleDTO>(
      () => this.deductionRuleApi.deleteRule(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  /**
   * Restore a deduction rule
   * POST /api/hrms/deduction-rules/<rule_id>/restore
   */
  async restoreRule(
    id: string,
    options?: ApiCallOptions,
  ): Promise<DeductionRuleDTO> {
    const data = await this.callApi<DeductionRuleDTO>(
      () => this.deductionRuleApi.restoreRule(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }
}

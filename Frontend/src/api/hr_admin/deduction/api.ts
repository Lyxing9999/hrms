import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  DeductionRuleDTO,
  DeductionRuleCreateDTO,
  DeductionRuleUpdateDTO,
  DeductionRuleListParams,
  DeductionRuleApplicableParams,
  DeductionRuleListResponseDTO,
} from "./dto";

export class DeductionRuleApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/deduction-rules",
  ) {}

  /**
   * Create a new deduction rule
   * POST /api/hrms/deduction-rules
   */
  async createRule(payload: DeductionRuleCreateDTO) {
    const res = await this.$api.post<ApiResponse<DeductionRuleDTO>>(
      this.baseURL,
      payload,
    );
    return res.data;
  }

  /**
   * Get all deduction rules with pagination
   * GET /api/hrms/deduction-rules
   */
  async getRules(params?: DeductionRuleListParams) {
    const res = await this.$api.get<ApiResponse<DeductionRuleListResponseDTO>>(
      this.baseURL,
      {
        params: {
          page: params?.page,
          limit: params?.limit,
          type: params?.type,
          is_active: params?.is_active,
          include_deleted: params?.include_deleted,
          deleted_only: params?.deleted_only,
        },
        signal: params?.signal,
      },
    );
    return res.data;
  }

  /**
   * Get a specific deduction rule by ID
   * GET /api/hrms/deduction-rules/<rule_id>
   */
  async getRule(id: string) {
    const res = await this.$api.get<ApiResponse<DeductionRuleDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  /**
   * Find applicable deduction rule
   * GET /api/hrms/deduction-rules/applicable
   */
  async getApplicableRule(params: DeductionRuleApplicableParams) {
    const res = await this.$api.get<ApiResponse<DeductionRuleDTO | null>>(
      `${this.baseURL}/applicable`,
      {
        params: {
          type: params.type,
          minutes: params.minutes,
        },
        signal: params.signal,
      },
    );
    return res.data;
  }

  /**
   * Update a deduction rule
   * PATCH /api/hrms/deduction-rules/<rule_id>
   */
  async updateRule(id: string, payload: DeductionRuleUpdateDTO) {
    const res = await this.$api.patch<ApiResponse<DeductionRuleDTO>>(
      `${this.baseURL}/${id}`,
      payload,
    );
    return res.data;
  }

  /**
   * Soft delete a deduction rule
   * DELETE /api/hrms/deduction-rules/<rule_id>
   */
  async deleteRule(id: string) {
    const res = await this.$api.delete<ApiResponse<DeductionRuleDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  /**
   * Restore a deduction rule
   * POST /api/hrms/deduction-rules/<rule_id>/restore
   */
  async restoreRule(id: string) {
    const res = await this.$api.post<ApiResponse<DeductionRuleDTO>>(
      `${this.baseURL}/${id}/restore`,
      {},
    );
    return res.data;
  }
}

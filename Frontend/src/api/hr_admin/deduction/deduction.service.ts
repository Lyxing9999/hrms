// frontend/src/api/hr_admin/deduction/deduction.service.ts
import { DeductionRuleApi } from "./deduction.api";
import type {
  DeductionRuleDTO,
  DeductionRulePaginatedDTO,
  DeductionRuleCreateDTO,
  DeductionRuleUpdateDTO,
  DeductionRuleListParams,
  DeductionType,
} from "./deduction.dto";

export class DeductionRuleService {
  private api: DeductionRuleApi;

  constructor() {
    this.api = new DeductionRuleApi();
  }

  async getRules(
    params: DeductionRuleListParams = {}
  ): Promise<DeductionRulePaginatedDTO> {
    return await this.api.getRules(params);
  }

  async getRule(id: string): Promise<DeductionRuleDTO> {
    return await this.api.getRule(id);
  }

  async getActiveRules(): Promise<{ items: DeductionRuleDTO[] }> {
    return await this.api.getActiveRules();
  }

  async getRulesByType(
    type: DeductionType
  ): Promise<{ items: DeductionRuleDTO[]; type: DeductionType }> {
    return await this.api.getRulesByType(type);
  }

  async createRule(data: DeductionRuleCreateDTO): Promise<DeductionRuleDTO> {
    return await this.api.createRule(data);
  }

  async updateRule(
    id: string,
    data: DeductionRuleUpdateDTO
  ): Promise<DeductionRuleDTO> {
    return await this.api.updateRule(id, data);
  }

  async softDeleteRule(id: string): Promise<DeductionRuleDTO> {
    return await this.api.softDeleteRule(id);
  }

  async restoreRule(id: string): Promise<DeductionRuleDTO> {
    return await this.api.restoreRule(id);
  }
}

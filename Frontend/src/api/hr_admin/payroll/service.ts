import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

import type {
  PayslipDTO,
  PayslipListParams,
  PayslipPaginatedDTO,
  PayrollRunDTO,
  PayrollRunGenerateDTO,
  PayrollRunGenerateResponseDTO,
  PayrollRunListParams,
  PayrollRunPaginatedDTO,
} from "./dto";
import { PayrollRunApi } from "./api";

export class PayrollRunService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly payrollRunApi: PayrollRunApi) {}

  /**
   * Generate payroll run
   * POST /api/hrms/payroll/runs/generate
   */
  async generateRun(
    payload: PayrollRunGenerateDTO,
    options?: ApiCallOptions,
  ): Promise<PayrollRunGenerateResponseDTO> {
    const data = await this.callApi<PayrollRunGenerateResponseDTO>(
      () => this.payrollRunApi.generateRun(payload),
      { showSuccess: true, ...(options ?? {}) },
    );

    return data ?? {};
  }

  /**
   * List payroll runs
   * GET /api/hrms/payroll/runs
   */
  async listRuns(
    params?: PayrollRunListParams,
    options?: ApiCallOptions,
  ): Promise<PayrollRunPaginatedDTO> {
    const data = await this.callApi<PayrollRunPaginatedDTO>(
      () => this.payrollRunApi.listRuns(params),
      options,
    );

    return (
      data ?? {
        items: [],
        total: 0,
        page: params?.page ?? 1,
        page_size: params?.limit ?? 10,
        total_pages: 0,
      }
    );
  }

  /**
   * Get payroll run detail
   * GET /api/hrms/payroll/runs/<payroll_run_id>
   */
  async getRun(
    payrollRunId: string,
    options?: ApiCallOptions,
  ): Promise<PayrollRunDTO> {
    const data = await this.callApi<PayrollRunDTO>(
      () => this.payrollRunApi.getRun(payrollRunId),
      options,
    );
    return data!;
  }

  /**
   * Finalize payroll run
   * POST /api/hrms/payroll/runs/<payroll_run_id>/finalize
   */
  async finalizeRun(
    payrollRunId: string,
    options?: ApiCallOptions,
  ): Promise<PayrollRunDTO> {
    const data = await this.callApi<PayrollRunDTO>(
      () => this.payrollRunApi.finalizeRun(payrollRunId),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  /**
   * Mark payroll run paid
   * POST /api/hrms/payroll/runs/<payroll_run_id>/mark-paid
   */
  async markRunPaid(
    payrollRunId: string,
    options?: ApiCallOptions,
  ): Promise<PayrollRunDTO> {
    const data = await this.callApi<PayrollRunDTO>(
      () => this.payrollRunApi.markRunPaid(payrollRunId),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  /**
   * List payslips
   * GET /api/hrms/payroll/payslips
   */
  async listPayslips(
    params?: PayslipListParams,
    options?: ApiCallOptions,
  ): Promise<PayslipPaginatedDTO> {
    const data = await this.callApi<PayslipPaginatedDTO>(
      () => this.payrollRunApi.listPayslips(params),
      options,
    );

    return (
      data ?? {
        items: [],
        total: 0,
        page: params?.page ?? 1,
        page_size: params?.limit ?? 10,
        total_pages: 0,
      }
    );
  }

  /**
   * Get payslip detail
   * GET /api/hrms/payroll/payslips/<payslip_id>
   */
  async getPayslip(
    payslipId: string,
    options?: ApiCallOptions,
  ): Promise<PayslipDTO> {
    const data = await this.callApi<PayslipDTO>(
      () => this.payrollRunApi.getPayslip(payslipId),
      options,
    );
    return data!;
  }
}

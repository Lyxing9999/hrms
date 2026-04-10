import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  PayslipDTO,
  PayslipPaginatedDTO,
  PayslipListParams,
  PayrollRunDTO,
  PayrollRunGenerateDTO,
  PayrollRunGenerateResponseDTO,
  PayrollRunListParams,
  PayrollRunPaginatedDTO,
} from "./dto";

export class PayrollRunApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/payroll/runs",
  ) {}

  /**
   * Generate payroll run
   * POST /api/hrms/payroll/runs/generate
   */
  async generateRun(payload: PayrollRunGenerateDTO) {
    const res = await this.$api.post<
      ApiResponse<PayrollRunGenerateResponseDTO>
    >(`${this.baseURL}/generate`, payload);
    return res.data;
  }

  /**
   * List payroll runs
   * GET /api/hrms/payroll/runs
   */
  async listRuns(params?: PayrollRunListParams) {
    const res = await this.$api.get<ApiResponse<PayrollRunPaginatedDTO>>(
      this.baseURL,
      {
        params,
      },
    );
    return res.data;
  }

  /**
   * Get payroll run detail
   * GET /api/hrms/payroll/runs/<payroll_run_id>
   */
  async getRun(payrollRunId: string) {
    const res = await this.$api.get<ApiResponse<PayrollRunDTO>>(
      `${this.baseURL}/${payrollRunId}`,
    );
    return res.data;
  }

  /**
   * Finalize payroll run
   * POST /api/hrms/payroll/runs/<payroll_run_id>/finalize
   */
  async finalizeRun(payrollRunId: string) {
    const res = await this.$api.post<ApiResponse<PayrollRunDTO>>(
      `${this.baseURL}/${payrollRunId}/finalize`,
      {},
    );
    return res.data;
  }

  /**
   * Mark payroll run paid
   * POST /api/hrms/payroll/runs/<payroll_run_id>/mark-paid
   */
  async markRunPaid(payrollRunId: string) {
    const res = await this.$api.post<ApiResponse<PayrollRunDTO>>(
      `${this.baseURL}/${payrollRunId}/mark-paid`,
      {},
    );
    return res.data;
  }

  /**
   * List payslips
   * GET /api/hrms/payroll/payslips
   */
  async listPayslips(params?: PayslipListParams) {
    const res = await this.$api.get<ApiResponse<PayslipPaginatedDTO>>(
      "/api/hrms/payroll/payslips",
      {
        params,
      },
    );
    return res.data;
  }

  /**
   * Get payslip detail
   * GET /api/hrms/payroll/payslips/<payslip_id>
   */
  async getPayslip(payslipId: string) {
    const res = await this.$api.get<ApiResponse<PayslipDTO>>(
      `/api/hrms/payroll/payslips/${payslipId}`,
    );
    return res.data;
  }
}

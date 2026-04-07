import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  OvertimeRequestDTO,
  OvertimeRequestCreateDTO,
  OvertimeApproveDTO,
  OvertimeRejectDTO,
  OvertimeCancelDTO,
  OvertimeRequestListParams,
  OvertimeRequestListResponseDTO,
  MyOvertimeSummaryDTO,
  OvertimePayrollSummaryDTO,
} from "./dto";

export class OvertimeRequestApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/overtime-requests",
  ) {}

  /**
   * Create a new overtime request
   * POST /api/hrms/overtime-requests
   */
  async createRequest(payload: OvertimeRequestCreateDTO) {
    const res = await this.$api.post<ApiResponse<OvertimeRequestDTO>>(
      this.baseURL,
      payload,
    );
    return res.data;
  }

  /**
   * Get all overtime requests with pagination
   * GET /api/hrms/overtime-requests
   */
  async getRequests(params?: OvertimeRequestListParams) {
    const res = await this.$api.get<
      ApiResponse<OvertimeRequestListResponseDTO>
    >(this.baseURL, {
      params: {
        page: params?.page,
        limit: params?.limit,
        employee_id: params?.employee_id,
        status: params?.status,
        start_date: params?.start_date,
        end_date: params?.end_date,
      },
      signal: params?.signal,
    });
    return res.data;
  }

  /**
   * Get my overtime requests
   * GET /api/hrms/overtime-requests/my
   */
  async getMyRequests(params?: OvertimeRequestListParams) {
    const res = await this.$api.get<
      ApiResponse<OvertimeRequestListResponseDTO>
    >(`${this.baseURL}/my`, {
      params: {
        page: params?.page,
        limit: params?.limit,
        status: params?.status,
        start_date: params?.start_date,
        end_date: params?.end_date,
      },
      signal: params?.signal,
    });
    return res.data;
  }

  /**
   * Get a specific overtime request by ID
   * GET /api/hrms/overtime-requests/<overtime_id>
   */
  async getRequest(id: string) {
    const res = await this.$api.get<ApiResponse<OvertimeRequestDTO>>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  /**
   * Get pending overtime requests awaiting approval
   * GET /api/hrms/overtime-requests/pending-approval
   */
  async getPendingRequests(params?: OvertimeRequestListParams) {
    const res = await this.$api.get<
      ApiResponse<OvertimeRequestListResponseDTO>
    >(`${this.baseURL}/pending-approval`, {
      params: {
        page: params?.page,
        limit: params?.limit,
        employee_id: params?.employee_id,
        start_date: params?.start_date,
        end_date: params?.end_date,
      },
      signal: params?.signal,
    });
    return res.data;
  }

  /**
   * Get my overtime summary
   * GET /api/hrms/overtime-requests/my-summary
   */
  async getMyOvertimeSummary() {
    const res = await this.$api.get<ApiResponse<MyOvertimeSummaryDTO>>(
      `${this.baseURL}/my-summary`,
    );
    return res.data;
  }

  /**
   * Get payroll approved overtime requests
   * GET /api/hrms/overtime-requests/payroll-approved
   */
  async getPayrollApprovedRequests(params?: OvertimeRequestListParams) {
    const res = await this.$api.get<
      ApiResponse<OvertimeRequestListResponseDTO>
    >(`${this.baseURL}/payroll-approved`, {
      params: {
        page: params?.page,
        limit: params?.limit,
        employee_id: params?.employee_id,
        start_date: params?.start_date,
        end_date: params?.end_date,
      },
      signal: params?.signal,
    });
    return res.data;
  }

  /**
   * Get payroll overtime summary
   * GET /api/hrms/overtime-requests/payroll-summary
   */
  async getPayrollOvertimeSummary(params?: {
    start_date?: string;
    end_date?: string;
    employee_id?: string;
  }) {
    const res = await this.$api.get<ApiResponse<OvertimePayrollSummaryDTO>>(
      `${this.baseURL}/payroll-summary`,
      {
        params,
      },
    );
    return res.data;
  }

  /**
   * Approve an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/approve
   */
  async approveRequest(id: string, payload: OvertimeApproveDTO) {
    const res = await this.$api.post<ApiResponse<OvertimeRequestDTO>>(
      `${this.baseURL}/${id}/approve`,
      payload,
    );
    return res.data;
  }

  /**
   * Reject an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/reject
   */
  async rejectRequest(id: string, payload: OvertimeRejectDTO) {
    const res = await this.$api.post<ApiResponse<OvertimeRequestDTO>>(
      `${this.baseURL}/${id}/reject`,
      payload,
    );
    return res.data;
  }

  /**
   * Cancel an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/cancel
   */
  async cancelRequest(id: string, payload?: OvertimeCancelDTO) {
    const res = await this.$api.post<ApiResponse<OvertimeRequestDTO>>(
      `${this.baseURL}/${id}/cancel`,
      payload ?? {},
    );
    return res.data;
  }
}

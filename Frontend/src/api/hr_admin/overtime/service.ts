import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

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

import { OvertimeRequestApi } from "./api";

export class OvertimeRequestService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly overtimeRequestApi: OvertimeRequestApi) {}

  /**
   * Create a new overtime request
   * POST /api/hrms/overtime-requests
   */
  async createRequest(
    payload: OvertimeRequestCreateDTO,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestDTO> {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.createRequest(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  /**
   * Get all overtime requests
   * GET /api/hrms/overtime-requests
   */
  async getRequests(
    params?: OvertimeRequestListParams,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestListResponseDTO> {
    const data = await this.callApi<OvertimeRequestListResponseDTO>(
      () => this.overtimeRequestApi.getRequests(params),
      options,
    );
    return (
      data ?? {
        items: [],
        total: 0,
        page: 1,
        limit: 10,
        total_pages: 0,
      }
    );
  }

  /**
   * Get my overtime requests
   * GET /api/hrms/overtime-requests/my
   */
  async getMyRequests(
    params?: OvertimeRequestListParams,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestListResponseDTO> {
    const data = await this.callApi<OvertimeRequestListResponseDTO>(
      () => this.overtimeRequestApi.getMyRequests(params),
      options,
    );
    return (
      data ?? {
        items: [],
        total: 0,
        page: 1,
        limit: 10,
        total_pages: 0,
      }
    );
  }

  /**
   * Get a specific overtime request
   * GET /api/hrms/overtime-requests/<overtime_id>
   */
  async getRequest(
    id: string,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestDTO> {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.getRequest(id),
      options,
    );
    return data!;
  }

  /**
   * Get pending overtime requests
   * GET /api/hrms/overtime-requests/pending-approval
   */
  async getPendingRequests(
    params?: OvertimeRequestListParams,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestListResponseDTO> {
    const data = await this.callApi<OvertimeRequestListResponseDTO>(
      () => this.overtimeRequestApi.getPendingRequests(params),
      options,
    );
    return (
      data ?? {
        items: [],
        total: 0,
        page: 1,
        limit: 10,
        total_pages: 0,
      }
    );
  }

  /**
   * Get my overtime summary
   * GET /api/hrms/overtime-requests/my-summary
   */
  async getMyOvertimeSummary(
    options?: ApiCallOptions,
  ): Promise<MyOvertimeSummaryDTO> {
    const data = await this.callApi<MyOvertimeSummaryDTO>(
      () => this.overtimeRequestApi.getMyOvertimeSummary(),
      options,
    );
    return (
      data ?? {
        total_requests: 0,
        pending_count: 0,
        approved_count: 0,
        rejected_count: 0,
        cancelled_count: 0,
        approved_hours: 0,
        approved_payment: 0,
      }
    );
  }

  /**
   * Get payroll approved overtime requests
   * GET /api/hrms/overtime-requests/payroll-approved
   */
  async getPayrollApprovedRequests(
    params?: OvertimeRequestListParams,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestListResponseDTO> {
    const data = await this.callApi<OvertimeRequestListResponseDTO>(
      () => this.overtimeRequestApi.getPayrollApprovedRequests(params),
      options,
    );
    return (
      data ?? {
        items: [],
        total: 0,
        page: 1,
        limit: 10,
        total_pages: 0,
      }
    );
  }

  /**
   * Get payroll overtime summary
   * GET /api/hrms/overtime-requests/payroll-summary
   */
  async getPayrollOvertimeSummary(
    params?: {
      start_date?: string;
      end_date?: string;
      employee_id?: string;
    },
    options?: ApiCallOptions,
  ): Promise<OvertimePayrollSummaryDTO> {
    const data = await this.callApi<OvertimePayrollSummaryDTO>(
      () => this.overtimeRequestApi.getPayrollOvertimeSummary(params),
      options,
    );
    return (
      data ?? {
        total_approved_requests: 0,
        total_approved_hours: 0,
        total_approved_payment: 0,
      }
    );
  }

  /**
   * Approve an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/approve
   */
  async approveRequest(
    id: string,
    payload: OvertimeApproveDTO,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestDTO> {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.approveRequest(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  /**
   * Reject an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/reject
   */
  async rejectRequest(
    id: string,
    payload: OvertimeRejectDTO,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestDTO> {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.rejectRequest(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  /**
   * Cancel an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/cancel
   */
  async cancelRequest(
    id: string,
    payload?: OvertimeCancelDTO,
    options?: ApiCallOptions,
  ): Promise<OvertimeRequestDTO> {
    const data = await this.callApi<OvertimeRequestDTO>(
      () => this.overtimeRequestApi.cancelRequest(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }
}

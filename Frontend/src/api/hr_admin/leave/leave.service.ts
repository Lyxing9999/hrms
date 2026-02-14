// frontend/src/api/hr_admin/leave/leave.service.ts
import type {
  LeaveDTO,
  LeavePaginatedDTO,
  LeaveCreateDTO,
  LeaveUpdateDTO,
  LeaveReviewDTO,
  ListLeavesParams,
} from "./leave.dto";
import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";
import { LeaveApi } from "./leave.api";

export class LeaveService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly leaveApi: LeaveApi) {}

  // ============
  // QUERY
  // ============
  async getLeaves(params?: ListLeavesParams, options?: ApiCallOptions) {
    const data = await this.callApi<LeavePaginatedDTO>(
      () => this.leaveApi.getLeaves(params),
      options
    );
    return data!;
  }

  async getLeave(leaveId: string, options?: ApiCallOptions) {
    const data = await this.callApi<LeaveDTO>(
      () => this.leaveApi.getLeave(leaveId),
      options
    );
    return data!;
  }

  // Note: Backend doesn't have a separate endpoint for employee's own leaves
  // Use getLeaves() with employee_id filter instead
  // async getMyLeaves(params?: ListLeavesParams, options?: ApiCallOptions) {
  //   const data = await this.callApi<LeavePaginatedDTO>(
  //     () => this.leaveApi.getMyLeaves(params),
  //     options
  //   );
  //   return data!;
  // }

  // ============
  // COMMANDS
  // ============
  async submitLeave(payload: LeaveCreateDTO, options?: ApiCallOptions) {
    const leave = await this.callApi<LeaveDTO>(
      () => this.leaveApi.submitLeave(payload),
      { showSuccess: true, successMessage: "Leave request submitted", ...(options ?? {}) }
    );
    return leave!;
  }

  async updateLeave(
    leaveId: string,
    payload: LeaveUpdateDTO,
    options?: ApiCallOptions
  ) {
    const leave = await this.callApi<LeaveDTO>(
      () => this.leaveApi.updateLeave(leaveId, payload),
      { showSuccess: true, successMessage: "Leave request updated", ...(options ?? {}) }
    );
    return leave!;
  }

  async approveLeave(
    leaveId: string,
    payload: LeaveReviewDTO,
    options?: ApiCallOptions
  ) {
    const leave = await this.callApi<LeaveDTO>(
      () => this.leaveApi.approveLeave(leaveId, payload),
      { showSuccess: true, successMessage: "Leave approved", ...(options ?? {}) }
    );
    return leave!;
  }

  async rejectLeave(
    leaveId: string,
    payload: LeaveReviewDTO,
    options?: ApiCallOptions
  ) {
    const leave = await this.callApi<LeaveDTO>(
      () => this.leaveApi.rejectLeave(leaveId, payload),
      { showSuccess: true, successMessage: "Leave rejected", ...(options ?? {}) }
    );
    return leave!;
  }

  async cancelLeave(leaveId: string, options?: ApiCallOptions) {
    const leave = await this.callApi<LeaveDTO>(
      () => this.leaveApi.cancelLeave(leaveId),
      { showSuccess: true, successMessage: "Leave cancelled", ...(options ?? {}) }
    );
    return leave!;
  }

  async softDeleteLeave(leaveId: string, options?: ApiCallOptions) {
    const leave = await this.callApi<LeaveDTO>(
      () => this.leaveApi.softDeleteLeave(leaveId),
      { showSuccess: true, successMessage: "Leave deleted", ...(options ?? {}) }
    );
    return leave!;
  }

  async restoreLeave(leaveId: string, options?: ApiCallOptions) {
    const leave = await this.callApi<LeaveDTO>(
      () => this.leaveApi.restoreLeave(leaveId),
      { showSuccess: true, successMessage: "Leave restored", ...(options ?? {}) }
    );
    return leave!;
  }
}

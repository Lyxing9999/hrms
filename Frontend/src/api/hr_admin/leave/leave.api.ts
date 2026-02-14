// frontend/src/api/hr_admin/leave/leave.api.ts
import type {
  LeaveDTO,
  LeavePaginatedDTO,
  LeaveCreateDTO,
  LeaveUpdateDTO,
  LeaveReviewDTO,
  ListLeavesParams,
} from "./leave.dto";

export class LeaveApi {
  constructor(private readonly $fetch: typeof $fetch) {}

  // ============
  // QUERY
  // ============
  async getLeaves(params?: ListLeavesParams): Promise<LeavePaginatedDTO> {
    return await this.$fetch("/api/hrms/leaves", {
      method: "GET",
      params: {
        q: params?.q,
        page: params?.page ?? 1,
        limit: params?.limit ?? 10,
        employee_id: params?.employee_id,
        status: params?.status,
        include_deleted: params?.include_deleted ?? false,
        deleted_only: params?.deleted_only ?? false,
      },
      signal: params?.signal,
    });
  }

  async getLeave(leaveId: string): Promise<LeaveDTO> {
    return await this.$fetch(`/api/hrms/leaves/${leaveId}`, {
      method: "GET",
    });
  }

  // Note: Backend doesn't have a separate endpoint for employee's own leaves
  // Use getLeaves() with employee_id filter instead
  // async getMyLeaves(params?: ListLeavesParams): Promise<LeavePaginatedDTO> {
  //   return await this.$fetch("/api/hrms/employee/leaves", {
  //     method: "GET",
  //     params: {
  //       page: params?.page ?? 1,
  //       limit: params?.limit ?? 10,
  //       status: params?.status,
  //     },
  //     signal: params?.signal,
  //   });
  // }

  // ============
  // COMMANDS
  // ============
  async submitLeave(payload: LeaveCreateDTO): Promise<LeaveDTO> {
    return await this.$fetch("/api/hrms/employee/leaves", {
      method: "POST",
      body: payload,
    });
  }

  async updateLeave(
    leaveId: string,
    payload: LeaveUpdateDTO
  ): Promise<LeaveDTO> {
    return await this.$fetch(`/api/hrms/leaves/${leaveId}`, {
      method: "PATCH",
      body: payload,
    });
  }

  async approveLeave(
    leaveId: string,
    payload: LeaveReviewDTO
  ): Promise<LeaveDTO> {
    return await this.$fetch(`/api/hrms/manager/leaves/${leaveId}/approve`, {
      method: "PATCH",
      body: payload,
    });
  }

  async rejectLeave(
    leaveId: string,
    payload: LeaveReviewDTO
  ): Promise<LeaveDTO> {
    return await this.$fetch(`/api/hrms/manager/leaves/${leaveId}/reject`, {
      method: "PATCH",
      body: payload,
    });
  }

  async cancelLeave(leaveId: string): Promise<LeaveDTO> {
    return await this.$fetch(`/api/hrms/leaves/${leaveId}/cancel`, {
      method: "PATCH",
    });
  }

  async softDeleteLeave(leaveId: string): Promise<LeaveDTO> {
    return await this.$fetch(`/api/hrms/leaves/${leaveId}/soft-delete`, {
      method: "DELETE",
    });
  }

  async restoreLeave(leaveId: string): Promise<LeaveDTO> {
    return await this.$fetch(`/api/hrms/leaves/${leaveId}/restore`, {
      method: "POST",
    });
  }
}

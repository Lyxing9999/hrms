import type { AxiosInstance } from "axios";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  HrCreateEmployeeDTO,
  HrUpdateEmployeeDTO,
  HrGetEmployeesWithAccountsResponse,
  HrGetEmployeeResponse,
  HrCreateEmployeeResponse,
  HrUpdateEmployeeResponse,
  HrGetEmployeeAccountResponse,
  HrCreateEmployeeAccountDTO,
  HrCreateEmployeeAccountResponse,
  HrEmployeeOnboardDTO,
  HrEmployeeOnboardResponse,
  HrSoftDeleteEmployeeAccountResponse,
  HrRestoreEmployeeAccountResponse,
  ListEmployeesParams,
  ListEmployeeAccountsParams,
  HrGetEmployeeAccountsResponse,
  HrLinkEmployeeAccountDTO,
  HrLinkEmployeeAccountResponse,
  HrUpdateEmployeeAccountDTO,
  HrEmployeeAccountDTO,
  HrPasswordResetResponse,
} from "./dto";
import { Status } from "../../types/enums/status.enum";
export class EmployeeApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/employees",
  ) {}

  async getEmployeesWithAccounts(params?: ListEmployeesParams) {
    const res = await this.$api.get<HrGetEmployeesWithAccountsResponse>(
      this.baseURL,
      {
        params: {
          ...params,
          with_accounts: true,
        },
      },
    );
    return res.data;
  }

  async getEmployee(id: string) {
    const res = await this.$api.get<HrGetEmployeeResponse>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  async getEmployeeAccount(id: string) {
    const res = await this.$api.get<HrGetEmployeeAccountResponse>(
      `${this.baseURL}/${id}/account`,
    );
    return res.data;
  }

  async createEmployee(payload: HrCreateEmployeeDTO) {
    const res = await this.$api.post<HrCreateEmployeeResponse>(
      this.baseURL,
      payload,
    );
    return res.data;
  }

  async updateEmployee(id: string, payload: HrUpdateEmployeeDTO) {
    const res = await this.$api.patch<HrUpdateEmployeeResponse>(
      `${this.baseURL}/${id}`,
      payload,
    );
    return res.data;
  }

  async softDeleteEmployee(id: string) {
    const res = await this.$api.delete<ApiResponse<void>>(
      `${this.baseURL}/${id}/soft-delete`,
    );
    return res.data;
  }

  async restoreEmployee(id: string) {
    const res = await this.$api.post<ApiResponse<void>>(
      `${this.baseURL}/${id}/restore`,
    );
    return res.data;
  }

  async createAccount(id: string, payload: HrCreateEmployeeAccountDTO) {
    const res = await this.$api.post<HrCreateEmployeeAccountResponse>(
      `${this.baseURL}/${id}/create-account`,
      payload,
    );
    return res.data;
  }

  async onboardEmployee(payload: HrEmployeeOnboardDTO) {
    const res = await this.$api.post<HrEmployeeOnboardResponse>(
      `${this.baseURL}/onboard`,
      payload,
    );
    return res.data;
  }

  async softDeleteEmployeeAccount(id: string) {
    const res = await this.$api.post<HrSoftDeleteEmployeeAccountResponse>(
      `${this.baseURL}/${id}/account/soft-delete`,
    );
    return res.data;
  }

  async restoreEmployeeAccount(id: string) {
    const res = await this.$api.post<HrRestoreEmployeeAccountResponse>(
      `${this.baseURL}/${id}/account/restore`,
    );
    return res.data;
  }

  async getEmployeeAccounts(params?: ListEmployeeAccountsParams) {
    const res = await this.$api.get<HrGetEmployeeAccountsResponse>(
      "/api/hrms/employee-accounts",
      { params },
    );
    return res.data;
  }

  async linkAccount(employeeId: string, payload: HrLinkEmployeeAccountDTO) {
    const res = await this.$api.post<HrLinkEmployeeAccountResponse>(
      `${this.baseURL}/${employeeId}/link-account`,
      payload,
    );
    return res.data;
  }

  async updateEmployeeAccount(id: string, payload: HrUpdateEmployeeAccountDTO) {
    const res = await this.$api.patch<ApiResponse<HrEmployeeAccountDTO>>(
      `${this.baseURL}/${id}/account`,
      payload,
    );
    return res.data;
  }

  async requestEmployeeAccountPasswordReset(id: string) {
    const res = await this.$api.post<ApiResponse<HrPasswordResetResponse>>(
      `${this.baseURL}/${id}/account/password-reset`,
      {},
    );
    return res.data;
  }

  async setEmployeeAccountStatus(
    employeeId: string,
    payload: { status: Status },
  ) {
    console.log("employee api baseURL:", this.$api.defaults.baseURL);
    const res = await this.$api.patch<
      ApiResponse<{ id: string; status: Status }>
    >(`${this.baseURL}/${employeeId}/account/status`, payload);
    return res.data;
  }
}

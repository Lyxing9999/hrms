import type { AxiosInstance } from "axios";
import type { UserRegisterForm } from "../../iam/iam.dto";
import type { ApiResponse } from "~/api/types/common/api-response.type";
import type {
  HrCreateEmployeeDTO,
  HrUpdateEmployeeDTO,
  ListEmployeesParams,
  HrGetEmployeesResponse,
  HrGetEmployeeResponse,
  HrCreateEmployeeResponse,
  HrUpdateEmployeeResponse,
} from "./dto";

export class EmployeeApi {
  constructor(
    private readonly $api: AxiosInstance,
    private readonly baseURL = "/api/hrms/employees",
  ) {}

  // QUERY

  async getEmployees(params?: ListEmployeesParams) {
    const res = await this.$api.get<HrGetEmployeesResponse>(this.baseURL, {
      params,
    });
    return res.data;
  }

  async getEmployee(id: string) {
    const res = await this.$api.get<HrGetEmployeeResponse>(
      `${this.baseURL}/${id}`,
    );
    return res.data;
  }

  // COMMAND

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

  async createAccount(id: string, payload: UserRegisterForm) {
    const res = await this.$api.post<HrCreateEmployeeResponse>(
      `${this.baseURL}/${id}/create-account`,
      payload,
    );
    return res.data;
  }
  // TODO
  // async uploadEmployeePhoto(
  //   employeeId: string,
  //   file: File,
  //   oldPhotoUrl?: string | null,
  // ) {
  //   const form = new FormData();
  //   form.append("photo", file);
  //   if (oldPhotoUrl) form.append("old_photo_url", oldPhotoUrl);

  //   const res = await this.$api.patch<ApiResponse<{ photo_url: string }>>(
  //     `/uploads/employee/${employeeId}`,
  //     form,
  //     { headers: { "Content-Type": "multipart/form-data" } },
  //   );

  //   return res.data;
  // }
}

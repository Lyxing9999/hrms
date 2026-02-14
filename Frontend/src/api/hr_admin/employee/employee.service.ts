import { useApiUtils, type ApiCallOptions } from "~/composables/system/useApiUtils";
import type {
  HrEmployeeDTO,
  HrEmployeePaginatedDTO,
  HrCreateEmployeeDTO,
  HrUpdateEmployeeDTO,
  ListEmployeesParams,

} from "./employee.dto";
import { EmployeeApi } from "./employee.api";

export class EmployeeService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly employeeApi: EmployeeApi) { }

  // ============
  // QUERY
  // ============

  async getEmployees(params?: ListEmployeesParams, options?: ApiCallOptions) {
    const data = await this.callApi<HrEmployeePaginatedDTO>(
      () => this.employeeApi.getEmployees(params),
      options,
    );
    return data!;
  }

  async getEmployee(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<HrEmployeeDTO>(
      () => this.employeeApi.getEmployee(id),
      options,
    );
    return data!;
  }

  // ============
  // COMMANDS
  // ============

  async createEmployee(payload: HrCreateEmployeeDTO, options?: ApiCallOptions) {
    const data = await this.callApi<HrEmployeeDTO>(
      () => this.employeeApi.createEmployee(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async updateEmployee(id: string, payload: HrUpdateEmployeeDTO, options?: ApiCallOptions) {
    const data = await this.callApi<HrEmployeeDTO>(
      () => this.employeeApi.updateEmployee(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async softDeleteEmployee(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<any>(
      () => this.employeeApi.softDeleteEmployee(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async restoreEmployee(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<any>(
      () => this.employeeApi.restoreEmployee(id),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async createAccount(employeeId: string, payload: any, options?: ApiCallOptions) {
    const data = await this.callApi<any>(
      () => this.employeeApi.createAccount(employeeId, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async uploadEmployeePhoto(employeeId: string, file: File, oldPhotoUrl?: string | null, options?: ApiCallOptions) {
    const data = await this.callApi<{ photo_url: string }>(
      () => this.employeeApi.uploadEmployeePhoto(employeeId, file, oldPhotoUrl),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }
}
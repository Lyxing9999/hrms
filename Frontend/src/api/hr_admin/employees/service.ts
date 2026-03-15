import {
  useApiUtils,
  type ApiCallOptions,
} from "~/composables/system/useApiUtils";

import type {
  HrEmployeeDTO,
  HrEmployeePaginatedDTO,
  HrCreateEmployeeDTO,
  HrUpdateEmployeeDTO,
  ListEmployeesParams,
} from "./dto";

import { EmployeeApi } from "./api";

export class EmployeeService {
  private readonly callApi = useApiUtils().callApi;

  constructor(private readonly employeeApi: EmployeeApi) {}

  // QUERY

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

  // COMMAND

  private mapFormToCreateDTO(form: any): HrCreateEmployeeDTO {
    return {
      employee_code: form.employee_code,
      full_name: form.full_name,
      department: form.department,
      position: form.position,
      employment_type: form.employment_type,
      basic_salary: form.basic_salary,
      status: form.status ?? "active",
      contract:
        form.employment_type === "contract"
          ? {
              start_date: form.start_date,
              end_date: form.end_date,
              salary_type: form.salary_type,
              rate: form.rate,
              leave_policy_id: form.leave_policy_id,
              pay_on_holiday: form.pay_on_holiday ?? true,
              pay_on_weekend: form.pay_on_weekend ?? false,
            }
          : undefined,
      manager_user_id: form.manager_user_id,
      schedule_id: form.schedule_id,
      photo_url: form.photo_url,
    };
  }

  // --- Helper: map form data to update DTO ---
  private mapFormToUpdateDTO(form: any): HrUpdateEmployeeDTO {
    const payload: HrUpdateEmployeeDTO = {
      full_name: form.full_name,
      department: form.department,
      position: form.position,
      employment_type: form.employment_type,
      basic_salary: form.basic_salary,
      status: form.status,
      manager_user_id: form.manager_user_id,
      schedule_id: form.schedule_id,
      photo_url: form.photo_url,
    };

    if (form.employment_type === "contract" || form.contract) {
      payload.contract = {
        start_date: form.start_date,
        end_date: form.end_date,
        salary_type: form.salary_type,
        rate: form.rate,
        leave_policy_id: form.leave_policy_id,
        pay_on_holiday: form.pay_on_holiday ?? true,
        pay_on_weekend: form.pay_on_weekend ?? false,
      };
    }

    return payload;
  }

  // --- Create Employee ---
  async createEmployee(
    form: any,
    options?: ApiCallOptions,
  ): Promise<HrEmployeeDTO> {
    const payload = this.mapFormToCreateDTO(form);
    const data = await this.callApi<HrEmployeeDTO>(
      () => this.employeeApi.createEmployee(payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  // --- Update Employee ---
  async updateEmployee(
    id: string,
    form: any,
    options?: ApiCallOptions,
  ): Promise<HrEmployeeDTO> {
    const payload = this.mapFormToUpdateDTO(form);
    const data = await this.callApi<HrEmployeeDTO>(
      () => this.employeeApi.updateEmployee(id, payload),
      { showSuccess: true, ...(options ?? {}) },
    );
    return data!;
  }

  async softDeleteEmployee(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<void>(
      () => this.employeeApi.softDeleteEmployee(id),
      { showSuccess: true, ...(options ?? {}) },
    );

    return data!;
  }

  async restoreEmployee(id: string, options?: ApiCallOptions) {
    const data = await this.callApi<void>(
      () => this.employeeApi.restoreEmployee(id),
      { showSuccess: true, ...(options ?? {}) },
    );

    return data!;
  }

  async createAccount(
    employeeId: string,
    payload: any,
    options?: ApiCallOptions,
  ) {
    const data = await this.callApi<HrEmployeeDTO>(
      () => this.employeeApi.createAccount(employeeId, payload),
      { showSuccess: true, ...(options ?? {}) },
    );

    return data!;
  }
  // TODO
  // async uploadEmployeePhoto(
  //   employeeId: string,
  //   file: File,
  //   oldPhotoUrl?: string | null,
  //   options?: ApiCallOptions,
  // ) {
  //   const data = await this.callApi<{ photo_url: string }>(
  //     () => this.employeeApi.uploadEmployeePhoto(employeeId, file, oldPhotoUrl),
  //     { showSuccess: true, ...(options ?? {}) },
  //   );

  //   return data!;
  // }
}

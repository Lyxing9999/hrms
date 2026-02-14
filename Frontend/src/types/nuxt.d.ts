import type { EmployeeApi } from "~/api/hr_admin/employee/employee.api";
import type { EmployeeService } from "~/api/hr_admin/employee/employee.service";

declare module "#app" {
  interface NuxtApp {
    $hrEmployeeApi: EmployeeApi;
    $hrEmployeeService: EmployeeService;
  }
}

declare module "vue" {
  interface ComponentCustomProperties {
    $hrEmployeeApi: EmployeeApi;
    $hrEmployeeService: EmployeeService;
  }
}

export {};

import type { EmployeeApi } from "~/api/hr_admin/employee/employee.api";
import type { EmployeeService } from "~/api/hr_admin/employees/service";
import type { WorkingScheduleService } from "~/api/hr_admin/schedule";

declare module "#app" {
  interface NuxtApp {
    $hrEmployeeApi: EmployeeApi;
    $hrEmployeeService: EmployeeService;
    $hrScheduleService: WorkingScheduleService;
  }
}

declare module "vue" {
  interface ComponentCustomProperties {
    $hrEmployeeApi: EmployeeApi;
    $hrEmployeeService: EmployeeService;
    $hrScheduleService: WorkingScheduleService;
  }
}

declare module "vue" {
  interface ComponentCustomProperties {
    $hrEmployeeApi: EmployeeApi;
    $hrEmployeeService: EmployeeService;
  }
}

export {};

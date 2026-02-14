// frontend/src/types/nuxt-api.d.ts
import type { EmployeeService } from "~/api/hr_admin/employee/employee.service";
import type { LeaveService } from "~/api/hr_admin/leave/leave.service";

declare module "#app" {
  interface NuxtApp {
    $hrEmployeeService: EmployeeService;
    $hrLeaveService: LeaveService;
  }
}

declare module "vue" {
  interface ComponentCustomProperties {
    $hrEmployeeService: EmployeeService;
    $hrLeaveService: LeaveService;
  }
}

export {};

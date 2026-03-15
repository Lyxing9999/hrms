import type { de } from "element-plus/es/locale/index.mjs";
import type { EmployeeService } from "~/api/hr_admin/employees/service";
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

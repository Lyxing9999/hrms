import { EmployeeApi } from "~/api/hr_admin/employee/employee.api";
import { EmployeeService } from "~/api/hr_admin/employee/employee.service";

export default defineNuxtPlugin((nuxtApp) => {
  const $api = nuxtApp.$api;
  if (!$api) return;


  const employeeApi = new EmployeeApi($api, "/api/hrms/admin/employees");
  const employeeService = new EmployeeService(employeeApi);

  return {
    provide: {
      hrEmployeeService: employeeService,
    },
  };
});
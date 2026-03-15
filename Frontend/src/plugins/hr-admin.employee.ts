import { EmployeeApi } from "~/api/hr_admin/employees/api";
import { EmployeeService } from "~/api/hr_admin/employees/service";

export default defineNuxtPlugin((nuxtApp) => {
  const $api = nuxtApp.$api;
  if (!$api) return;

  const employeeApi = new EmployeeApi($api as any);
  const employeeService = new EmployeeService(employeeApi);

  return {
    provide: {
      hrEmployeeService: employeeService,
    },
  };
});

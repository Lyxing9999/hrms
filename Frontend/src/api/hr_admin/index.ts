import { EmployeeApi } from "~/api/hr_admin/employees/api";
import { EmployeeService } from "~/api/hr_admin/employees/service";

let _hrmsAdminService: ReturnType<typeof createHrmsAdminService> | null = null;

function createHrmsAdminService() {
  const { $api } = useNuxtApp();
  if (!$api) throw new Error("$api is undefined.");

  const hrmsApi = {
    employee: new EmployeeApi($api),
  };

  return {
    employee: new EmployeeService(hrmsApi.employee),
  };
}

export const hrmsAdminService = () =>
  (_hrmsAdminService ??= createHrmsAdminService());

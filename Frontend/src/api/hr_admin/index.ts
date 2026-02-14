import { EmployeeApi } from "~/api/hr_admin/employee/employee.api";
import { EmployeeService } from "~/api/hr_admin/employee/employee.service";

let _hrmsAdminService: ReturnType<typeof createHrmsAdminService> | null = null;

function createHrmsAdminService() {
    const { $api } = useNuxtApp();
    if (!$api) throw new Error("$api is undefined.");

    const hrmsApi = {
        employee: new EmployeeApi($api, "/api/hrms/admin/employees"),
    };

    return {
        employee: new EmployeeService(hrmsApi.employee),
    };
}

export const hrmsAdminService = () => (_hrmsAdminService ??= createHrmsAdminService());
import { EmployeeApi } from "~/api/hr_admin/employees/api";
import { EmployeeService } from "~/api/hr_admin/employees/service";
import { WorkingScheduleApi } from "./schedule";
import { WorkingScheduleService } from "./schedule";
import { WorkLocationApi, WorkLocationService } from "./workLocations";
import { AttendanceApi, AttendanceService } from "./attendance";

let _hrmsAdminService: ReturnType<typeof createHrmsAdminService> | null = null;

function createHrmsAdminService() {
  const { $api } = useNuxtApp();
  if (!$api) throw new Error("$api is undefined.");

  const hrmsApi = {
    employee: new EmployeeApi($api),
    workingSchedule: new WorkingScheduleApi($api),
    workLocation: new WorkLocationApi($api),
    attendance: new AttendanceApi($api),
  };

  return {
    employee: new EmployeeService(hrmsApi.employee),
    workingSchedule: new WorkingScheduleService(hrmsApi.workingSchedule),
    workLocation: new WorkLocationService(hrmsApi.workLocation),
    attendance: new AttendanceService(hrmsApi.attendance),
  };
}

export const hrmsAdminService = () =>
  (_hrmsAdminService ??= createHrmsAdminService());

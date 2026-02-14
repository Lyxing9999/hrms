// frontend/src/plugins/hr-admin.attendance.ts
import { AttendanceAPI } from "~/api/hr_admin/attendance/attendance.api";
import { AttendanceService } from "~/api/hr_admin/attendance/attendance.service";

export default defineNuxtPlugin((nuxtApp) => {
  const $api = nuxtApp.$api;

  const attendanceApi = new AttendanceAPI($api as any, "/api/hrms");
  const attendanceService = new AttendanceService(attendanceApi);

  return {
    provide: {
      hrAttendanceApi: attendanceApi,
      hrAttendanceService: attendanceService,
    },
  };
});

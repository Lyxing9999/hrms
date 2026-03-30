// frontend/src/plugins/hr-admin.schedule.ts
import { WorkingScheduleApi } from "~/api/hr_admin/schedule";
import { WorkingScheduleService } from "~/api/hr_admin/schedule";

export default defineNuxtPlugin((nuxtApp) => {
  const $api = nuxtApp.$api;
  if (!$api) return;

  const scheduleApi = new WorkingScheduleApi($api as any);
  const scheduleService = new WorkingScheduleService(scheduleApi);

  return {
    provide: {
      hrScheduleService: scheduleService,
    },
  };
});

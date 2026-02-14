// frontend/src/plugins/hr-admin.schedule.ts
import { WorkingScheduleService } from "~/api/hr_admin/schedule";

export default defineNuxtPlugin(() => {
  const scheduleService = new WorkingScheduleService();

  return {
    provide: {
      hrScheduleService: scheduleService,
    },
  };
});

// frontend/src/plugins/hr-admin.holiday.ts
import { PublicHolidayService } from "~/api/hr_admin/publicHoliday";

export default defineNuxtPlugin(() => {
  const holidayService = new PublicHolidayService();

  return {
    provide: {
      hrHolidayService: holidayService,
    },
  };
});

import { hrmsAdminService } from "~/api/hr_admin";

export default defineNuxtPlugin(() => {
  const service = hrmsAdminService();

  return {
    provide: {
      hrLocationService: service.workLocation,
    },
  };
});

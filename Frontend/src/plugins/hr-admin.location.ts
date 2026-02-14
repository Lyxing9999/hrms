// frontend/src/plugins/hr-admin.location.ts
import { WorkLocationService } from "~/api/hr_admin/location";

export default defineNuxtPlugin(() => {
  const locationService = new WorkLocationService();

  return {
    provide: {
      hrLocationService: locationService,
    },
  };
});

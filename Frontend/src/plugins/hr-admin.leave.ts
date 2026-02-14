// frontend/src/plugins/hr-admin.leave.ts
import { LeaveApi } from "~/api/hr_admin/leave/leave.api";
import { LeaveService } from "~/api/hr_admin/leave/leave.service";

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase || "http://localhost:5001";

  const customFetch = $fetch.create({
    baseURL: apiBase,
    credentials: "include",
    onRequest({ options }) {
      // Auth headers are handled by 20.api-auth.client.ts
    },
  });

  const leaveApi = new LeaveApi(customFetch);
  const leaveService = new LeaveService(leaveApi);

  return {
    provide: {
      hrLeaveService: leaveService,
    },
  };
});

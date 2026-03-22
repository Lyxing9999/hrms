import { hrmsAdminService } from "~/api/hr_admin";
import { Status } from "~/api/types/enums/status.enum";
import { useInlineStatus } from "~/composables/table-edit/useInlineStatus";
import type { HrEmployeeAccountRow } from "~/modules/tables/columns/hr_admin/employeeAccountColumns";

export function useEmployeeAccountStatusInline() {
  const api = hrmsAdminService();

  return useInlineStatus<HrEmployeeAccountRow, Status>(
    (id, next) => api.employee.setEmployeeAccountStatus(id, { status: next }),
    {
      defaultStatus: Status.ACTIVE,
      isLocked: () => false,

      tagType: (s) => {
        if (s === Status.ACTIVE) return "success";
        if (s === Status.INACTIVE) return "warning";
        if (s === Status.SUSPENDED) return "danger";
        return "info";
      },

      label: (s) => {
        const v = String(s ?? Status.ACTIVE).trim();
        return v ? v.charAt(0).toUpperCase() + v.slice(1) : "—";
      },
    },
  );
}

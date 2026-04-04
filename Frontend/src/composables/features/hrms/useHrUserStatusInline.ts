import { Status } from "~/api/types/enums/status.enum";
import { useInlineStatus } from "~/composables/table-edit/useInlineStatus";
import type { HrEmployeeAccountRow } from "~/modules/tables/columns/hr_admin/employeeAccountColumns";
import { useHrEmployeeState } from "~/composables/features/hrms/useHrEmployeeState";

export function useEmployeeAccountStatusInline() {
  const employeeState = useHrEmployeeState();

  return useInlineStatus<HrEmployeeAccountRow, Status>(
    (id, next) => employeeState.setEmployeeAccountStatus(id, { status: next }),
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

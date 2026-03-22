import type { ColumnConfig } from "~/components/types/tableEdit";
import { ElTag } from "element-plus";
import { h } from "vue";

export type HrEmployeeAccountRow = {
  id: string;
  email?: string | null;
  username?: string | null;
  role?: string | null;
  status?: string | null;
};

export const employeeAccountColumns: ColumnConfig<HrEmployeeAccountRow>[] = [
  {
    field: "username",
    label: "Username",
    minWidth: "180px",
  },
  {
    field: "email",
    label: "Email",
    minWidth: "260px",
  },
  {
    field: "role",
    label: "Role",
    width: "120px",
    align: "center",
    render: (row) =>
      h(
        ElTag,
        { type: "success", effect: "plain", size: "small" },
        { default: () => String(row.role ?? "—") },
      ),
  },
  {
    field: "status",
    label: "Status",
    width: "120px",
    align: "center",
    render: (row) => {
      const status = String(row.status ?? "unknown");
      const type =
        status === "active"
          ? "success"
          : status === "inactive"
          ? "warning"
          : "danger";

      return h(
        ElTag,
        { type, effect: "plain", size: "small" },
        { default: () => status },
      );
    },
  },
  {
    field: "id",
    operation: true,
    label: "Operation",
    align: "center",
    minWidth: "180px",
  },
];

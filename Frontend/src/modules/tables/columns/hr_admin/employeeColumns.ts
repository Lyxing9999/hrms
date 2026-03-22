import type { ColumnConfig } from "~/components/types/tableEdit";
import type {
  HrEmployeeDTO,
  HrEmployeeAccountDTO,
} from "~/api/hr_admin/employees/dto";
import { ElInput, ElTag } from "element-plus";
export type EmployeeTableRow = {
  id: string;
  employee: HrEmployeeDTO;
  account: HrEmployeeAccountDTO | null;
};

export const employeeColumns: ColumnConfig<EmployeeTableRow>[] = [
  {
    field: "username",
    label: "Username",
    sortable: true,
    controls: false,
    autoSave: true,
    revertSlots: true,

    minWidth: "150px",
    rules: [
      { required: true, message: "Please input username", trigger: "blur" },
      { min: 6, message: "At least 6 characters", trigger: "blur" },
      { max: 20, message: "Max 20 characters", trigger: "blur" },
      {
        pattern: /^[A-Za-z]+$/,
        message: "Only letters allowed (no numbers, no spaces)",
      },
    ],
    component: ElInput,
    componentProps: { placeholder: "Enter username" },
  },
  {
    field: "email",
    label: "Email",
    controls: false,
    autoSave: true,
    revertSlots: true,
    minWidth: "300px",

    component: ElInput,
    componentProps: {
      placeholder: "Enter email",
      class: "w-full",
      style: { width: "100%" },
    },
  },
  {
    field: "status",
    label: "Status",
    width: "130px",
    useSlot: true,
    slotName: "status",
  },
  {
    field: "role",
    label: "Role",
    width: "120px",
    align: "center",
    render: (row: EmployeeTableRow, _field: keyof EmployeeTableRow) => {
      const role = String(row.role ?? "");

      let tagType: "success" | "danger" | "warning" = "success";
      if (role === "manager") tagType = "danger";
      else if (role === "employee") tagType = "warning";

      return h(
        ElTag,
        { type: tagType, effect: "plain", size: "small" },
        { default: () => role || "N/A" },
      );
    },
  },
  // {
  //   field: "created_by_name",
  //   label: "Created By",
  //   controls: false,
  //   minWidth: "140px",
  //   align: "center",
  //   render: (row: EmployeeTableRow) =>
  //     h(
  //       "span",
  //       { style: { color: "#999" } },
  //       String(row.created_by_name ?? "—"),
  //     ),
  // },

  {
    field: "id",
    operation: true,
    label: "Operation",
    inlineEditActive: false,
    align: "center",
    minWidth: "300px",
    smartProps: {},
  },
];

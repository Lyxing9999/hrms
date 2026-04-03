// frontend/src/modules/tables/columns/hr_admin/overtimeColumns.ts
import type { ColumnConfig } from "~/components/types/tableEdit";
import type { OvertimeRequestDTO } from "~/api/hr_admin/overtimeRequest";
import dayjs from "dayjs";
import duration from "dayjs/plugin/duration";

dayjs.extend(duration);

export const overtimeColumns: ColumnConfig<OvertimeRequestDTO>[] = [
  {
    prop: "id",
    label: "ID",
    width: 100,
    visible: false,
  },
  {
    prop: "employee_id",
    label: "Employee",
    width: 150,
    visible: true,
    sortable: false,
  },
  {
    prop: "request_date",
    label: "Date",
    width: 130,
    visible: true,
    sortable: true,
    formatter: (row: OvertimeRequestDTO) => {
      return dayjs(row.request_date).format("MMM DD, YYYY");
    },
  },
  {
    prop: "start_time",
    label: "Start Time",
    width: 120,
    visible: true,
    sortable: false,
    formatter: (row: OvertimeRequestDTO) => {
      return dayjs(row.start_time, "HH:mm:ss").format("HH:mm");
    },
  },
  {
    prop: "end_time",
    label: "End Time",
    width: 120,
    visible: true,
    sortable: false,
    formatter: (row: OvertimeRequestDTO) => {
      return dayjs(row.end_time, "HH:mm:ss").format("HH:mm");
    },
  },
  {
    prop: "requested_hours",
    label: "Hours",
    width: 80,
    visible: true,
    sortable: false,
    formatter: (row: OvertimeRequestDTO) => {
      return `${row.requested_hours.toFixed(1)}h`;
    },
  },
  {
    prop: "reason",
    label: "Reason",
    minWidth: 200,
    visible: true,
    sortable: false,
  },
  {
    prop: "status",
    label: "Status",
    width: 120,
    visible: true,
    sortable: true,
    slotName: "status",
  },
  {
    prop: "manager_comment",
    label: "Manager Comment",
    minWidth: 180,
    visible: false,
    sortable: false,
  },
  {
    prop: "lifecycle.created_at",
    label: "Submitted",
    width: 160,
    visible: true,
    sortable: true,
    formatter: (row: OvertimeRequestDTO) => {
      return dayjs(row.lifecycle.created_at).format("MMM DD, HH:mm");
    },
  },
  {
    prop: "operation",
    label: "Actions",
    width: 200,
    fixed: "right",
    visible: true,
    slotName: "operation",
  },
];

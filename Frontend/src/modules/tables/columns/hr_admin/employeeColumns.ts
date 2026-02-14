import { ElInput } from "element-plus";
import type { ColumnConfig } from "~/components/types/tableEdit";
import type { HrEmployeeDTO } from "~/api/hr_admin/employee/employee.dto";


export type HrEmployeeColumnConfig = HrEmployeeDTO & {
    photo_url?: string | null;
};

export const employeeColumns: ColumnConfig<HrEmployeeColumnConfig>[] = [

    {
        field: "photo_url",
        label: "Photo",
        width: "120px",
        align: "center",
        sortable: false,
        controls: false,
        autoSave: false,
        revertSlots: true,
        useSlot: true,
        slotName: "photo",
    },

    {
        field: "employee_code",
        label: "Code",
        minWidth: "120px",
        sortable: true,
        controls: false,
        autoSave: false,
        revertSlots: true,
        component: ElInput,
        componentProps: {
            disabled: true,
            class: "w-full",
        },
    },
    {
        field: "full_name",
        label: "Name",
        minWidth: "180px",
        sortable: true,
        controls: false,
        autoSave: false,
        revertSlots: true,
        component: ElInput,
        componentProps: {
            disabled: true,
            class: "w-full",
        },
    },
    {
        field: "department",
        label: "Dept",
        minWidth: "140px",
        sortable: true,
        controls: false,
        autoSave: false,
        revertSlots: true,
        component: ElInput,
        componentProps: {
            disabled: true,
            class: "w-full",
        },
    },
    {
        field: "position",
        label: "Position",
        minWidth: "160px",
        sortable: true,
        controls: false,
        autoSave: false,
        revertSlots: true,
        component: ElInput,
        componentProps: {
            disabled: true,
            class: "w-full",
        },
    },
    {
        field: "employment_type",
        label: "Type",
        minWidth: "120px",
        sortable: true,
        controls: false,
        autoSave: false,
        revertSlots: true,
        component: ElInput,
        componentProps: {
            disabled: true,
            class: "w-full",
        },
    },
    {
        field: "status",
        label: "Status",
        minWidth: "120px",
        align: "center",
        sortable: true,
        controls: false,
        autoSave: false,
        revertSlots: true,
        component: ElInput,
        componentProps: {
            disabled: true,
            class: "w-full",
        },
    },
    {
        field: "id",
        label: "Operation",
        align: "center",
        width: "220px",
        operation: true,
        inlineEditActive: false,
        useSlot: true,
        slotName: "operation",
    },
];
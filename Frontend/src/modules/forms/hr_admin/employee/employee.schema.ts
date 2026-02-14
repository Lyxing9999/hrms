import type { Field } from "~/components/types/form";
import {
    ElInput,
    ElSelect,
    ElOption,
    ElDatePicker,
    ElInputNumber,
    ElUpload,
    ElSwitch,
} from "element-plus";
import type {
    HrCreateEmployeeFormFlat,
    HrEmploymentType,
    HrEmployeeStatus,
    HrSalaryType,
} from "~/api/hr_admin/employee/employee.dto";

import {
    User,
    OfficeBuilding,
    Briefcase,
    Tickets,
    CircleCheck,
    Calendar,
    Money,
    Coin,
    Picture,
    Sunny,
} from "@element-plus/icons-vue";

const employmentTypeOptions: { label: string; value: HrEmploymentType }[] = [
    { label: "Contract", value: "contract" },
    { label: "Permanent", value: "permanent" },
];

const statusOptions: { label: string; value: HrEmployeeStatus }[] = [
    { label: "Active", value: "active" },
    { label: "Inactive", value: "inactive" },
];

const salaryTypeOptions: { label: string; value: HrSalaryType }[] = [
    { label: "Monthly", value: "monthly" },
    { label: "Daily", value: "daily" },
    { label: "Hourly", value: "hourly" },
];

const col = (span = 12) => ({ colProps: { xs: 24, sm: 24, md: span, lg: span } });

export const employeeFormSchema: Field<HrCreateEmployeeFormFlat>[] = [
    // --- Row 1: Code + Name
    {
        row: [
            {
                key: "employee_code",
                label: "Employee Code",
                iconComponent: Tickets,
                component: ElInput,
                formItemProps: { required: true, prop: "employee_code", label: "Employee Code" },
                componentProps: {
                    placeholder: "E.g. EMP-001",
                    clearable: true,
                    class: "w-full",
                    ...col(12),
                },
            },
            {
                key: "full_name",
                label: "Full Name",
                iconComponent: User,
                component: ElInput,
                formItemProps: { required: true, prop: "full_name", label: "Full Name" },
                componentProps: {
                    placeholder: "Enter full name",
                    clearable: true,
                    class: "w-full",
                    ...col(12),
                },
            },
        ],
    },

    // --- Row 2: Department + Position
    {
        row: [
            {
                key: "department",
                label: "Department",
                iconComponent: OfficeBuilding,
                component: ElInput,
                formItemProps: { required: false, prop: "department", label: "Department" },
                componentProps: {
                    placeholder: "Department (optional)",
                    clearable: true,
                    class: "w-full",
                    ...col(12),
                },
            },
            {
                key: "position",
                label: "Position",
                iconComponent: Briefcase,
                component: ElInput,
                formItemProps: { required: false, prop: "position", label: "Position" },
                componentProps: {
                    placeholder: "Position (optional)",
                    clearable: true,
                    class: "w-full",
                    ...col(12),
                },
            },
        ],
    },

    // --- Row 3: Employment Type + Status
    {
        row: [
            {
                key: "employment_type",
                label: "Employment Type",
                iconComponent: CircleCheck,
                component: ElSelect,
                childComponent: ElOption,
                formItemProps: { required: true, prop: "employment_type", label: "Employment Type" },
                componentProps: { placeholder: "Select type", class: "w-full", ...col(12) },
                childComponentProps: {
                    options: () => employmentTypeOptions,
                    valueKey: "value",
                    labelKey: "label",
                },
            },
            {
                key: "status",
                label: "Status",
                iconComponent: CircleCheck,
                component: ElSelect,
                childComponent: ElOption,
                formItemProps: { required: true, prop: "status", label: "Status" },
                componentProps: { placeholder: "Select status", class: "w-full", ...col(12) },
                childComponentProps: {
                    options: () => statusOptions,
                    valueKey: "value",
                    labelKey: "label",
                },
            },
        ],
    },

    // --- Row 4: Contract dates (only enabled for contract)
    {
        row: [
            {
                key: "contract.start_date",
                label: "Contract Start Date",
                iconComponent: Calendar,
                component: ElDatePicker,
                formItemProps: (m: HrCreateEmployeeFormFlat) => ({
                    required: m.employment_type === "contract",
                    prop: "contract.start_date",
                    label: "Contract Start Date",
                }),
                componentProps: (m: HrCreateEmployeeFormFlat) => ({
                    type: "date",
                    valueFormat: "YYYY-MM-DD",
                    placeholder: "Start date",
                    class: "w-full",
                    disabled: m.employment_type !== "contract",
                    ...col(12),
                }),
            },
            {
                key: "contract.end_date",
                label: "Contract End Date",
                iconComponent: Calendar,
                component: ElDatePicker,
                formItemProps: (m: HrCreateEmployeeFormFlat) => ({
                    required: m.employment_type === "contract",
                    prop: "contract.end_date",
                    label: "Contract End Date",
                }),
                componentProps: (m: HrCreateEmployeeFormFlat) => ({
                    type: "date",
                    valueFormat: "YYYY-MM-DD",
                    placeholder: "End date",
                    class: "w-full",
                    disabled: m.employment_type !== "contract",
                    ...col(12),
                }),
            },
        ],
    },

    // --- Row 5: Salary type + Rate
    {
        row: [
            {
                key: "contract.salary_type",
                label: "Salary Type",
                iconComponent: Money,
                component: ElSelect,
                childComponent: ElOption,
                formItemProps: (m: HrCreateEmployeeFormFlat) => ({
                    required: m.employment_type === "contract",
                    prop: "contract.salary_type",
                    label: "Salary Type",
                }),
                componentProps: (m: HrCreateEmployeeFormFlat) => ({
                    placeholder: "Select salary type",
                    class: "w-full",
                    disabled: m.employment_type !== "contract",
                    ...col(12),
                }),
                childComponentProps: {
                    options: () => salaryTypeOptions,
                    valueKey: "value",
                    labelKey: "label",
                },
            },
            {
                key: "contract.rate",
                label: "Rate",
                iconComponent: Coin,
                component: ElInputNumber,
                formItemProps: (m: HrCreateEmployeeFormFlat) => ({
                    required: m.employment_type === "contract",
                    prop: "contract.rate",
                    label: "Rate",
                }),
                componentProps: (m: HrCreateEmployeeFormFlat) => ({
                    min: 0,
                    step: 1,
                    class: "w-full",
                    controlsPosition: "right",
                    disabled: m.employment_type !== "contract",
                    ...col(12),
                }),
            },
        ],
    },

    // --- Row 6: Contract flags
    {
        row: [
            {
                key: "contract.pay_on_holiday",
                label: "Pay on Holiday",
                iconComponent: Sunny,
                component: ElSwitch,
                formItemProps: {
                    required: false,
                    prop: "contract.pay_on_holiday",
                    label: "Pay on Holiday",
                },
                componentProps: (m: HrCreateEmployeeFormFlat) => ({
                    disabled: m.employment_type !== "contract",
                    ...col(12),
                }),
            },
            {
                key: "contract.pay_on_weekend",
                label: "Pay on Weekend",
                iconComponent: Sunny,
                component: ElSwitch,
                formItemProps: {
                    required: false,
                    prop: "contract.pay_on_weekend",
                    label: "Pay on Weekend",
                },
                componentProps: (m: HrCreateEmployeeFormFlat) => ({
                    disabled: m.employment_type !== "contract",
                    ...col(12),
                }),
            },
        ],
    },

    // --- Row 7: Photo full width
    {
        row: [
            {
                key: "photo",
                label: "Photo",
                iconComponent: Picture,
                component: ElUpload,
                formItemProps: { required: false, prop: "photo", label: "Photo" },
                componentProps: {
                    autoUpload: false,
                    limit: 1,
                    multiple: false,
                    showFileList: true,
                    accept: "image/*",
                    listType: "picture-card",
                    ...col(24),
                },
            },
        ],
    },
];
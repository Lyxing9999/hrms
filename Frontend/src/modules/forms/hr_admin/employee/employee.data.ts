import { reactive } from "vue";
import { unflatten } from "~/utils/data/unflatten";
import type {
    HrCreateEmployeeDTO,
    HrEmployeeContractDTO,
    HrEmploymentType,
    HrEmployeeStatus,
} from "~/api/hr_admin/employee/employee.dto";

export const defaultContract = (): HrEmployeeContractDTO => ({
    start_date: "",
    end_date: "",
    salary_type: "monthly",
    rate: 0,
    leave_policy_id: null,
    pay_on_holiday: true,
    pay_on_weekend: false,
});

// FLAT form model for UI
export type HrCreateEmployeeFormFlat = Omit<HrCreateEmployeeDTO, "contract"> & {
    "contract.start_date": string;
    "contract.end_date": string;
    "contract.salary_type": HrEmployeeContractDTO["salary_type"];
    "contract.rate": number;

    "contract.leave_policy_id"?: string | null;
    "contract.pay_on_holiday"?: boolean;
    "contract.pay_on_weekend"?: boolean;

    photo?: File | string | null;
};

export const getEmployeeFormDataFlat = (): HrCreateEmployeeFormFlat => ({
    employee_code: "",
    full_name: "",
    department: null,
    position: null,
    employment_type: "contract" as HrEmploymentType,
    status: "active" as HrEmployeeStatus,

    "contract.start_date": "",
    "contract.end_date": "",
    "contract.salary_type": "monthly",
    "contract.rate": 0,
    "contract.leave_policy_id": null,
    "contract.pay_on_holiday": true,
    "contract.pay_on_weekend": false,

    manager_user_id: null,
    schedule_id: null,
    photo: null,
});

export const getEmployeeFormDataEditFlat = (data?: Partial<HrCreateEmployeeFormFlat>) =>
    reactive<HrCreateEmployeeFormFlat>({
        ...getEmployeeFormDataFlat(),
        ...(data ?? {}),
    });




export function toCreateEmployeePayload(form: HrCreateEmployeeFormFlat): HrCreateEmployeeDTO {
    const { photo, ...flat } = form;

    const nested = unflatten(flat) as any;

    if (nested.employment_type !== "contract") {
        nested.contract = null;
        return nested as HrCreateEmployeeDTO;
    }

    // contract employee
    const c = { ...defaultContract(), ...(nested.contract ?? {}) };

    c.start_date = String(c.start_date || "").trim();
    c.end_date = String(c.end_date || "").trim();
    c.salary_type = c.salary_type || "monthly";
    c.rate = Number(c.rate || 0);

    // optional frontend validation (avoid backend error)
    if (!c.start_date || !c.end_date) {
        throw new Error("Contract start_date and end_date are required");
    }
    if (c.end_date < c.start_date) {
        throw new Error("Contract end_date must be >= start_date");
    }
    if (c.rate <= 0) {
        throw new Error("Contract rate must be > 0");
    }

    nested.contract = c;
    return nested as HrCreateEmployeeDTO;
}

// Convert employee DTO to flat form format for editing
export function employeeToFormFlat(employee: any): HrCreateEmployeeFormFlat {
    return {
        employee_code: employee.employee_code || "",
        full_name: employee.full_name || "",
        department: employee.department || null,
        position: employee.position || null,
        employment_type: employee.employment_type || "contract",
        status: employee.status || "active",
        "contract.start_date": employee.contract?.start_date || "",
        "contract.end_date": employee.contract?.end_date || "",
        "contract.salary_type": employee.contract?.salary_type || "monthly",
        "contract.rate": employee.contract?.rate || 0,
        "contract.leave_policy_id": employee.contract?.leave_policy_id || null,
        "contract.pay_on_holiday": employee.contract?.pay_on_holiday ?? true,
        "contract.pay_on_weekend": employee.contract?.pay_on_weekend ?? false,
        manager_user_id: employee.manager_user_id || null,
        schedule_id: employee.schedule_id || null,
        photo: employee.photo_url || null,
    };
}
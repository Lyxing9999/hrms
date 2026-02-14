import type { UseFormService } from "~/form-system/types/serviceFormTypes";
import type { HrEmployeeDTO } from "~/api/hr_admin/employee/employee.dto";
import type { EmployeeService } from "~/api/hr_admin/employee/employee.service";
import type { HrCreateEmployeeFormFlat } from "~/modules/forms/hr_admin/employee";
import { toCreateEmployeePayload } from "~/modules/forms/hr_admin/employee";

export function useEmployeeCreateWithPhoto(
    $hrEmployeeService: EmployeeService,
): UseFormService<HrCreateEmployeeFormFlat, Record<string, any>> {
    return {
        create: async (form) => {
            console.log(form)
            const payload = toCreateEmployeePayload(form);

            const created = await $hrEmployeeService.createEmployee(payload);

            // ElementPlus upload => file is often in (form.photo as any).raw
            const file = (form.photo as any)?.raw instanceof File ? (form.photo as any).raw : form.photo;

            if (file instanceof File) {
                await $hrEmployeeService.uploadEmployeePhoto(created.id, file, created.photo_url ?? null);
            }

            return created;
        },
    };
}
// frontend/src/plugins/hr-admin.deduction.ts
import { DeductionRuleService } from "~/api/hr_admin/deduction";

export default defineNuxtPlugin(() => {
  const deductionService = new DeductionRuleService();

  return {
    provide: {
      hrDeductionService: deductionService,
    },
  };
});

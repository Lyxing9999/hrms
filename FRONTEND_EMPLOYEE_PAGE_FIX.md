# Frontend Employee Page Error Fix

## Issue
The employee profile page at `http://localhost:3000/hr/employees/employee-profile` was showing "An unexpected error occurred" even though the backend API was working correctly.

## Root Causes

### 1. Missing Runtime Import
**File**: `frontend/src/pages/hr/employees/employee-profile.vue`

**Problem**: The `employeeToFormFlat` function was imported as a TypeScript type only:
```typescript
import type { employeeToFormFlat} from "~/modules/forms/hr_admin/employee/";
```

But it was being used as a runtime function on line 94:
```typescript
updateFormData.value = employeeToFormFlat(row);
```

**Fix**: Changed to import it as both a runtime function and a type:
```typescript
import { getEmployeeFormDataFlat, getEmployeeFormDataEditFlat, employeeToFormFlat } from "~/modules/forms/hr_admin/employee/";
import type { employeeToFormFlat as EmployeeToFormFlatType } from "~/modules/forms/hr_admin/employee/";
```

### 2. Missing Unflatten Import
**File**: `frontend/src/modules/forms/hr_admin/employee/employee.data.ts`

**Problem**: The `unflatten` function was used in `toCreateEmployeePayload` but not imported:
```typescript
const nested = unflatten(flat) as any;  // unflatten is not defined!
```

**Fix**: Added the import:
```typescript
import { unflatten } from "~/utils/data/unflatten";
```

## Changes Made

### 1. frontend/src/pages/hr/employees/employee-profile.vue
```diff
- import { getEmployeeFormDataFlat, getEmployeeFormDataEditFlat } from "~/modules/forms/hr_admin/employee/";
- import type { employeeToFormFlat} from "~/modules/forms/hr_admin/employee/";
- import { employeeFormSchema } from "~/modules/forms/hr_admin/employee/";
+ import { getEmployeeFormDataFlat, getEmployeeFormDataEditFlat, employeeToFormFlat } from "~/modules/forms/hr_admin/employee/";
+ import type { employeeToFormFlat as EmployeeToFormFlatType } from "~/modules/forms/hr_admin/employee/";
+ import { employeeFormSchema } from "~/modules/forms/hr_admin/employee/";
```

### 2. frontend/src/modules/forms/hr_admin/employee/employee.data.ts
```diff
  import { reactive } from "vue";
+ import { unflatten } from "~/utils/data/unflatten";
  import type {
      HrCreateEmployeeDTO,
      HrEmployeeContractDTO,
      HrEmploymentType,
      HrEmployeeStatus,
  } from "~/api/hr_admin/employee/employee.dto";
```

## Impact

These fixes resolve:
- ✅ Page loading errors
- ✅ Employee list display
- ✅ Edit employee functionality
- ✅ Create employee functionality
- ✅ Form data conversion between flat and nested formats

## Testing

After these fixes, verify:
1. ✅ Page loads without errors at `/hr/employees/employee-profile`
2. ✅ Employee list displays correctly
3. ✅ "Add Employee" button opens the form
4. ✅ "Edit" button opens the form with employee data
5. ✅ Form submission works correctly
6. ✅ No console errors in browser

## Related Files

- `frontend/src/pages/hr/employees/employee-profile.vue` - Main employee management page
- `frontend/src/modules/forms/hr_admin/employee/employee.data.ts` - Form data utilities
- `frontend/src/modules/forms/hr_admin/employee/index.ts` - Module exports
- `frontend/src/utils/data/unflatten.ts` - Utility function for flattening objects

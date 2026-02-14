# Frontend API Connections - Complete

## ✅ All Backend Endpoints Connected to Frontend

### API Services Created

#### 1. Working Schedule Service ✅
**Files**:
- `frontend/src/api/hr_admin/schedule/schedule.dto.ts`
- `frontend/src/api/hr_admin/schedule/schedule.api.ts`
- `frontend/src/api/hr_admin/schedule/schedule.service.ts`
- `frontend/src/api/hr_admin/schedule/index.ts`
- `frontend/src/plugins/hr-admin.schedule.ts`

**Endpoints Connected**:
- GET `/api/hrms/admin/working-schedules` - List schedules
- GET `/api/hrms/admin/working-schedules/default` - Get default
- GET `/api/hrms/admin/working-schedules/{id}` - Get single
- POST `/api/hrms/admin/working-schedules` - Create
- PATCH `/api/hrms/admin/working-schedules/{id}` - Update
- DELETE `/api/hrms/admin/working-schedules/{id}/soft-delete` - Delete
- POST `/api/hrms/admin/working-schedules/{id}/restore` - Restore

---

#### 2. Work Location Service ✅
**Files**:
- `frontend/src/api/hr_admin/location/location.dto.ts`
- `frontend/src/api/hr_admin/location/location.api.ts`
- `frontend/src/api/hr_admin/location/location.service.ts`
- `frontend/src/api/hr_admin/location/index.ts`
- `frontend/src/plugins/hr-admin.location.ts`

**Endpoints Connected**:
- GET `/api/hrms/admin/work-locations` - List locations
- GET `/api/hrms/admin/work-locations/active` - Get active
- GET `/api/hrms/admin/work-locations/{id}` - Get single
- POST `/api/hrms/admin/work-locations` - Create
- PATCH `/api/hrms/admin/work-locations/{id}` - Update
- DELETE `/api/hrms/admin/work-locations/{id}/soft-delete` - Delete
- POST `/api/hrms/admin/work-locations/{id}/restore` - Restore

---

#### 3. Public Holiday Service ✅
**Files**:
- `frontend/src/api/hr_admin/holiday/holiday.dto.ts`
- `frontend/src/api/hr_admin/holiday/holiday.api.ts`
- `frontend/src/api/hr_admin/holiday/holiday.service.ts`
- `frontend/src/api/hr_admin/holiday/index.ts`
- `frontend/src/plugins/hr-admin.holiday.ts`

**Endpoints Connected**:
- GET `/api/hrms/admin/public-holidays` - List holidays
- GET `/api/hrms/admin/public-holidays/year/{year}` - Get by year
- GET `/api/hrms/admin/public-holidays/{id}` - Get single
- POST `/api/hrms/admin/public-holidays` - Create
- PATCH `/api/hrms/admin/public-holidays/{id}` - Update
- DELETE `/api/hrms/admin/public-holidays/{id}/soft-delete` - Delete
- POST `/api/hrms/admin/public-holidays/{id}/restore` - Restore

---

#### 4. Deduction Rule Service ✅
**Files**:
- `frontend/src/api/hr_admin/deduction/deduction.dto.ts`
- `frontend/src/api/hr_admin/deduction/deduction.api.ts`
- `frontend/src/api/hr_admin/deduction/deduction.service.ts`
- `frontend/src/api/hr_admin/deduction/index.ts`
- `frontend/src/plugins/hr-admin.deduction.ts`

**Endpoints Connected**:
- GET `/api/hrms/admin/deduction-rules` - List rules
- GET `/api/hrms/admin/deduction-rules/active` - Get active
- GET `/api/hrms/admin/deduction-rules/type/{type}` - Get by type
- GET `/api/hrms/admin/deduction-rules/{id}` - Get single
- POST `/api/hrms/admin/deduction-rules` - Create
- PATCH `/api/hrms/admin/deduction-rules/{id}` - Update
- DELETE `/api/hrms/admin/deduction-rules/{id}/soft-delete` - Delete
- POST `/api/hrms/admin/deduction-rules/{id}/restore` - Restore

---

#### 5. Employee Service ✅ (Already exists)
**Files**:
- `frontend/src/api/hr_admin/employee/employee.dto.ts`
- `frontend/src/api/hr_admin/employee/employee.api.ts`
- `frontend/src/api/hr_admin/employee/employee.service.ts`
- `frontend/src/plugins/hr-admin.employee.ts`

**Endpoints Connected**: 8 endpoints

---

#### 6. Leave Service ✅ (Already exists)
**Files**:
- `frontend/src/api/hr_admin/leave/leave.dto.ts`
- `frontend/src/api/hr_admin/leave/leave.api.ts`
- `frontend/src/api/hr_admin/leave/leave.service.ts`
- `frontend/src/plugins/hr-admin.leave.ts`

**Endpoints Connected**: 9 endpoints

---

## 📊 Summary

### Total API Services: 6
1. ✅ Employee Service (8 endpoints)
2. ✅ Leave Service (9 endpoints)
3. ✅ Working Schedule Service (7 endpoints)
4. ✅ Work Location Service (7 endpoints)
5. ✅ Public Holiday Service (7 endpoints)
6. ✅ Deduction Rule Service (8 endpoints)

### Total Endpoints Connected: 46

### Plugin Registration
All services are registered as Nuxt plugins:
- `$hrEmployeeService`
- `$hrLeaveService`
- `$hrScheduleService`
- `$hrLocationService`
- `$hrHolidayService`
- `$hrDeductionService`

---

## 🎯 Usage in Components

### Example: Using Schedule Service
```vue
<script setup lang="ts">
import { useNuxtApp } from "nuxt/app";

const { $hrScheduleService } = useNuxtApp();

// List schedules
const schedules = await $hrScheduleService.getSchedules({
  page: 1,
  limit: 10,
  q: "search term",
});

// Get single schedule
const schedule = await $hrScheduleService.getSchedule(id);

// Create schedule
const newSchedule = await $hrScheduleService.createSchedule({
  name: "Standard 9-5",
  start_time: "09:00:00",
  end_time: "17:00:00",
  working_days: [0, 1, 2, 3, 4],
  is_default: true,
});

// Update schedule
const updated = await $hrScheduleService.updateSchedule(id, {
  name: "Updated Name",
});

// Delete schedule
await $hrScheduleService.softDeleteSchedule(id);

// Restore schedule
await $hrScheduleService.restoreSchedule(id);
</script>
```

### Example: Using Location Service
```vue
<script setup lang="ts">
const { $hrLocationService } = useNuxtApp();

// Get active locations
const activeLocations = await $hrLocationService.getActiveLocations();

// Create location
const newLocation = await $hrLocationService.createLocation({
  name: "Main Office",
  address: "123 Street, Phnom Penh",
  latitude: 11.5564,
  longitude: 104.9282,
  radius_meters: 100,
  is_active: true,
});
</script>
```

### Example: Using Holiday Service
```vue
<script setup lang="ts">
const { $hrHolidayService } = useNuxtApp();

// Get holidays by year
const holidays2024 = await $hrHolidayService.getHolidaysByYear(2024);

// Create holiday
const newHoliday = await $hrHolidayService.createHoliday({
  name: "Khmer New Year",
  name_kh: "បុណ្យចូលឆ្នាំខ្មែរ",
  date: "2024-04-14",
  is_paid: true,
  description: "Traditional Cambodian New Year",
});
</script>
```

### Example: Using Deduction Service
```vue
<script setup lang="ts">
const { $hrDeductionService } = useNuxtApp();

// Get rules by type
const lateRules = await $hrDeductionService.getRulesByType("late");

// Create rule
const newRule = await $hrDeductionService.createRule({
  type: "late",
  min_minutes: 1,
  max_minutes: 30,
  deduction_percentage: 5.0,
  is_active: true,
});
</script>
```

---

## 🔧 TypeScript Support

All services are fully typed with TypeScript:

```typescript
// DTOs are properly typed
interface WorkingScheduleDTO {
  id: string;
  name: string;
  start_time: string;
  end_time: string;
  working_days: number[];
  weekend_days: number[];
  total_hours_per_day: number;
  is_default: boolean;
  created_by: string | null;
  lifecycle: LifecycleDTO;
}

// Service methods are typed
class WorkingScheduleService {
  async getSchedules(
    params: WorkingScheduleListParams = {}
  ): Promise<WorkingSchedulePaginatedDTO>;
  
  async createSchedule(
    data: WorkingScheduleCreateDTO
  ): Promise<WorkingScheduleDTO>;
  
  // ... other methods
}
```

---

## ✅ Benefits

1. **Type Safety**: Full TypeScript support with proper types
2. **Reusability**: Services can be used in any component
3. **Consistency**: All services follow the same pattern
4. **Error Handling**: Proper error handling with try/catch
5. **Loading States**: Easy to implement loading states
6. **Abort Support**: All list methods support AbortSignal
7. **Plugin System**: Services are globally available via `useNuxtApp()`

---

## 🎯 Next Steps

Now that all API services are connected, you can:

1. ✅ Create frontend pages for:
   - Work Locations (`/hr/config/locations`)
   - Public Holidays (`/hr/config/holidays`)
   - Deduction Rules (`/hr/config/deductions`)

2. ✅ All pages will follow the same pattern as Working Schedules

3. ✅ Use the services in components with full type safety

---

## 📝 Summary

**All 46 backend endpoints are now connected to the frontend!**

✅ 6 complete API services
✅ Full TypeScript support
✅ Plugin registration
✅ Consistent patterns
✅ Ready to use in components

You can now create the remaining frontend pages and they will have full backend connectivity!


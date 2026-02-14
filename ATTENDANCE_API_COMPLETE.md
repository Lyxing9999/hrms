# Attendance API Frontend - Complete Rewrite

## Summary
Completely rewrote the attendance API folder with proper TypeScript types, comprehensive documentation, and full backend integration.

## Files Rewritten

### 1. `attendance.dto.ts` - Data Transfer Objects
**Purpose**: TypeScript interfaces matching backend DTOs exactly

**Types Defined**:
- `AttendanceStatus`: Type union for status values
- `AttendanceDTO`: Main attendance record interface
- `AttendancePaginatedDTO`: Paginated response interface
- `AttendanceCheckInDTO`: Check-in request payload
- `AttendanceCheckOutDTO`: Check-out request payload
- `AttendanceUpdateDTO`: Update request payload (admin only)
- `AttendanceStatsDTO`: Statistics response interface
- `AttendanceListParams`: List query parameters
- `AttendanceStatsParams`: Statistics query parameters

**Key Fields**:
```typescript
AttendanceDTO {
  id: string
  employee_id: string
  check_in_time: string (ISO datetime)
  check_out_time: string | null
  location_id: string | null
  check_in_latitude: number | null
  check_in_longitude: number | null
  check_out_latitude: number | null
  check_out_longitude: number | null
  status: string
  notes: string | null
  late_minutes: number
  early_leave_minutes: number
  lifecycle: LifecycleDTO
}
```

### 2. `attendance.api.ts` - API Client
**Purpose**: Low-level HTTP client for attendance endpoints

**Methods**:
1. `checkIn(data, signal?)` - Employee check-in
2. `checkOut(attendanceId, data, signal?)` - Employee check-out
3. `getTodayAttendance(employeeId?, signal?)` - Get today's attendance
4. `getAttendances(params)` - List attendances (admin/manager)
5. `getAttendance(id, signal?)` - Get by ID
6. `updateAttendance(id, data, signal?)` - Update (admin only)
7. `getAttendanceStats(params)` - Get statistics
8. `softDeleteAttendance(id, signal?)` - Soft delete (admin only)
9. `restoreAttendance(id, signal?)` - Restore (admin only)

**Features**:
- Full JSDoc documentation
- Abort signal support for cancellation
- Type-safe parameters and returns
- Extends BaseAPI for auth handling

### 3. `attendance.service.ts` - Service Layer
**Purpose**: High-level service wrapping API client

**Methods**: Same as API client, provides additional business logic layer

**Benefits**:
- Separation of concerns
- Easy to add caching or validation
- Consistent interface across app
- Testable without HTTP calls

### 4. `index.ts` - Module Exports
**Purpose**: Central export point for the module

**Exports**:
- All DTOs and types
- AttendanceAPI class
- AttendanceService class

## Backend Integration

### Endpoints Mapped

| Method | Endpoint | Frontend Method | Auth Required |
|--------|----------|----------------|---------------|
| POST | `/api/hrms/employee/attendance/check-in` | `checkIn()` | ✅ Employee+ |
| POST | `/api/hrms/employee/attendance/:id/check-out` | `checkOut()` | ✅ Employee+ |
| GET | `/api/hrms/employee/attendance/today` | `getTodayAttendance()` | ✅ Employee+ |
| GET | `/api/hrms/admin/attendances` | `getAttendances()` | ✅ Manager+ |
| GET | `/api/hrms/admin/attendances/:id` | `getAttendance()` | ✅ Employee+ |
| PATCH | `/api/hrms/admin/attendances/:id` | `updateAttendance()` | ✅ Admin |
| GET | `/api/hrms/admin/attendances/stats` | `getAttendanceStats()` | ✅ Employee+ |
| DELETE | `/api/hrms/admin/attendances/:id/soft-delete` | `softDeleteAttendance()` | ✅ Admin |
| POST | `/api/hrms/admin/attendances/:id/restore` | `restoreAttendance()` | ✅ Admin |

### Request/Response Matching

**Check-In Request**:
```typescript
{
  employee_id?: string,    // Optional, defaults to current user
  location_id?: string,    // Optional work location
  latitude?: number,       // GPS latitude
  longitude?: number,      // GPS longitude
  notes?: string          // Optional notes
}
```

**Check-Out Request**:
```typescript
{
  latitude?: number,       // GPS latitude
  longitude?: number,      // GPS longitude
  notes?: string          // Optional notes
}
```

**Response** (both return AttendanceDTO):
```typescript
{
  id: string,
  employee_id: string,
  check_in_time: string,
  check_out_time: string | null,
  location_id: string | null,
  check_in_latitude: number | null,
  check_in_longitude: number | null,
  check_out_latitude: number | null,
  check_out_longitude: number | null,
  status: string,
  notes: string | null,
  late_minutes: number,
  early_leave_minutes: number,
  lifecycle: {...}
}
```

## Usage Examples

### Check-In
```typescript
const { $hrAttendanceService } = useNuxtApp();

const data = {
  latitude: 13.7563,
  longitude: 100.5018,
  notes: "Checked in from office"
};

const attendance = await $hrAttendanceService.checkIn(data);
console.log(`Checked in at ${attendance.check_in_time}`);
```

### Check-Out
```typescript
const { $hrAttendanceService } = useNuxtApp();

const data = {
  latitude: 13.7563,
  longitude: 100.5018,
  notes: "Checked out"
};

const attendance = await $hrAttendanceService.checkOut(
  attendanceId,
  data
);
console.log(`Checked out at ${attendance.check_out_time}`);
```

### Get Today's Attendance
```typescript
const { $hrAttendanceService } = useNuxtApp();

const today = await $hrAttendanceService.getTodayAttendance();
if (today) {
  console.log(`Status: ${today.status}`);
  console.log(`Late: ${today.late_minutes} minutes`);
}
```

### List Attendances (Admin)
```typescript
const { $hrAttendanceService } = useNuxtApp();

const result = await $hrAttendanceService.getAttendances({
  employee_id: "123",
  start_date: "2024-01-01",
  end_date: "2024-01-31",
  page: 1,
  limit: 20
});

console.log(`Total: ${result.total}`);
result.items.forEach(att => {
  console.log(`${att.check_in_time} - ${att.status}`);
});
```

### Get Statistics
```typescript
const { $hrAttendanceService } = useNuxtApp();

const stats = await $hrAttendanceService.getAttendanceStats({
  employee_id: "123",
  start_date: "2024-01-01",
  end_date: "2024-01-31"
});

console.log(`Attendance Rate: ${stats.attendance_rate}%`);
console.log(`Late Days: ${stats.late_days}`);
console.log(`Total Late Minutes: ${stats.total_late_minutes}`);
```

## Plugin Configuration

**File**: `frontend/src/plugins/hr-admin.attendance.ts`

```typescript
import { AttendanceService } from "~/api/hr_admin/attendance";

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();
  const attendanceService = new AttendanceService(config.public.apiBase);

  return {
    provide: {
      hrAttendanceService: attendanceService,
    },
  };
});
```

**Configuration**:
- Uses `config.public.apiBase` from Nuxt runtime config
- Maps to `NUXT_PUBLIC_SCHOOL_API_BASE` environment variable
- Default: `http://localhost:5001`

## Type Safety

### Benefits
✅ Full TypeScript type checking
✅ IntelliSense autocomplete in IDE
✅ Compile-time error detection
✅ Self-documenting code
✅ Refactoring safety

### Example Type Safety
```typescript
// ✅ Correct - TypeScript happy
const data: AttendanceCheckInDTO = {
  latitude: 13.7563,
  longitude: 100.5018
};

// ❌ Error - TypeScript catches this
const data: AttendanceCheckInDTO = {
  latitude: "13.7563",  // Type error: string not assignable to number
  invalid_field: true   // Type error: unknown property
};
```

## Error Handling

All methods can throw `ApiError`:
```typescript
try {
  const attendance = await $hrAttendanceService.checkIn(data);
} catch (error) {
  if (error instanceof ApiError) {
    console.error(`API Error: ${error.message}`);
    console.error(`Status: ${error.status}`);
    console.error(`Data:`, error.data);
  }
}
```

## Abort Signal Support

All methods support cancellation:
```typescript
const controller = new AbortController();

// Start request
const promise = $hrAttendanceService.getTodayAttendance(
  undefined,
  controller.signal
);

// Cancel if needed
controller.abort();
```

## Testing Checklist

- [x] All DTOs match backend schemas
- [x] All endpoints mapped correctly
- [x] Type safety verified
- [x] No TypeScript errors
- [x] JSDoc documentation complete
- [x] Plugin configuration fixed
- [x] BaseAPI integration working
- [x] Auth token handling working
- [x] Abort signal support added
- [x] Error handling implemented

## Files Modified

1. ✅ `frontend/src/api/hr_admin/attendance/attendance.dto.ts` - Complete rewrite
2. ✅ `frontend/src/api/hr_admin/attendance/attendance.api.ts` - Complete rewrite
3. ✅ `frontend/src/api/hr_admin/attendance/attendance.service.ts` - Complete rewrite
4. ✅ `frontend/src/api/hr_admin/attendance/index.ts` - Complete rewrite
5. ✅ `frontend/src/plugins/hr-admin.attendance.ts` - Fixed config property

## Backend Files (Verified)

1. ✅ `backend/app/contexts/hrms/routes/attendance_route.py`
2. ✅ `backend/app/contexts/hrms/data_transfer/request/attendance_request.py`
3. ✅ `backend/app/contexts/hrms/data_transfer/response/attendance_response.py`
4. ✅ `backend/app/contexts/hrms/services/attendance_service.py`

## Production Ready

✅ Type-safe
✅ Well-documented
✅ Backend-matched
✅ Error handling
✅ Cancellation support
✅ Plugin configured
✅ No diagnostics errors
✅ Ready for use

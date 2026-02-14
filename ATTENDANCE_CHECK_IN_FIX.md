# Attendance Check-In Error Fix

## Issue
Check-in was failing with error:
```
'NoneType' object has no attribute 'schedule_id'
```

## Root Cause
The `AttendanceService` was incorrectly initialized with `AttendanceReadModel` instead of `EmployeeReadModel`:

```python
# WRONG - Line 24
self.employee_read = AttendanceReadModel(db)
```

When `check_in()` was called, it tried to fetch employee data using:
```python
employee = self.employee_read.find_by_id(employee_id)
```

But `AttendanceReadModel` doesn't have a `find_by_id()` method that returns employee data, so it returned `None`. Then when trying to access `employee.schedule_id`, it failed with the NoneType error.

## Solution

### 1. Fixed Import (Line 20)
```python
# BEFORE
from app.contexts.hrms.read_models.attendance_read_model import AttendanceReadModel

# AFTER
from app.contexts.hrms.read_models.employee_read_model import EmployeeReadModel
```

### 2. Fixed Initialization (Line 28)
```python
# BEFORE
self.employee_read = AttendanceReadModel(db)

# AFTER
self.employee_read = EmployeeReadModel(db)
```

### 3. Fixed check_in Method (Lines 115-147)
```python
# BEFORE
employee = self.employee_read.find_by_id(employee_id)
late_minutes = self._calculate_late_minutes(check_in_time, employee.schedule_id)

# AFTER
employee_doc = self.employee_read.get_by_id(employee_id)
if not employee_doc:
    raise EmployeeNotFoundException(employee_id)

schedule_id = employee_doc.get("schedule_id")
late_minutes = self._calculate_late_minutes(check_in_time, schedule_id)
```

### 4. Fixed check_out Method (Lines 149-185)
```python
# BEFORE
employee = self.employee_repo.find_by_id(attendance.employee_id)
early_leave_minutes = self._calculate_early_leave_minutes(
    check_out_time, employee.schedule_id
)

# AFTER
employee_doc = self.employee_read.get_by_id(attendance.employee_id)
if not employee_doc:
    raise EmployeeNotFoundException(attendance.employee_id)

schedule_id = employee_doc.get("schedule_id")
early_leave_minutes = self._calculate_early_leave_minutes(
    check_out_time, schedule_id
)
```

## Key Changes

1. **Correct Read Model**: Now uses `EmployeeReadModel` which has the `get_by_id()` method
2. **Proper Error Handling**: Added check for None employee and raises `EmployeeNotFoundException`
3. **Safe Schedule Access**: Uses `employee_doc.get("schedule_id")` which returns None if not present
4. **Consistent Pattern**: Both `check_in` and `check_out` now use the same pattern

## Benefits

- Check-in/check-out now works even if employee doesn't have a schedule assigned
- Proper error messages when employee is not found
- No more NoneType attribute errors
- Schedule calculations gracefully handle None schedule_id (returns 0 late/early minutes)

## Testing

The fix ensures:
- ✅ Employees without schedules can check in/out (no late/early calculations)
- ✅ Employees with schedules get proper late/early minute calculations
- ✅ Proper error handling when employee doesn't exist
- ✅ No NoneType errors

# HRMS Complete System - Implementation Plan

## 📋 System Requirements Summary

### Core Modules to Implement
1. ✅ **Employee Management** - COMPLETE
2. ✅ **Leave Management** - COMPLETE
3. 🔨 **Attendance System** - NEW
4. 🔨 **Overtime (OT) Management** - NEW
5. 🔨 **Location Check-in** - NEW
6. 🔨 **Public Holidays (Khmer Calendar)** - NEW
7. 🔨 **Payroll System** - NEW
8. 🔨 **Working Schedule** - NEW
9. 🔨 **Deduction Rules** - NEW
10. 🔨 **Reporting System** - NEW

---

## 🏗️ Architecture Design

### New Domain Models

#### 1. Attendance
```python
class AttendanceStatus(Enum):
    PRESENT = "present"
    LATE = "late"
    ABSENT = "absent"
    WRONG_LOCATION = "wrong_location"
    PENDING_APPROVAL = "pending_approval"

class Attendance:
    - id: ObjectId
    - employee_id: ObjectId
    - date: date
    - check_in_time: datetime | None
    - check_out_time: datetime | None
    - check_in_location: dict (lat, lng, address)
    - check_out_location: dict | None
    - status: AttendanceStatus
    - is_valid_location: bool
    - justification: str | None
    - approved_by: ObjectId | None
    - total_hours: float
    - late_minutes: int
    - deduction_amount: float
    - lifecycle: Lifecycle
```

#### 2. OvertimeRequest
```python
class OTStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"

class OvertimeRequest:
    - id: ObjectId
    - employee_id: ObjectId
    - date: date
    - requested_hours: float
    - actual_hours: float | None
    - reason: str
    - status: OTStatus
    - is_weekend: bool
    - is_holiday: bool
    - rate_multiplier: float (1.5 or 2.0)
    - calculated_payment: float
    - requested_at: datetime
    - approved_by: ObjectId | None
    - approved_at: datetime | None
    - lifecycle: Lifecycle
```

#### 3. PublicHoliday
```python
class PublicHoliday:
    - id: ObjectId
    - name: str
    - name_kh: str (Khmer name)
    - date: date
    - is_paid: bool
    - description: str
    - created_by: ObjectId
    - lifecycle: Lifecycle
```

#### 4. WorkingSchedule
```python
class WorkingSchedule:
    - id: ObjectId
    - name: str
    - start_time: time
    - end_time: time
    - working_days: list[int] (0=Monday, 6=Sunday)
    - weekend_days: list[int]
    - total_hours_per_day: float
    - is_default: bool
    - lifecycle: Lifecycle
```

#### 5. WorkLocation
```python
class WorkLocation:
    - id: ObjectId
    - name: str
    - address: str
    - latitude: float
    - longitude: float
    - radius_meters: int (acceptable range)
    - is_active: bool
    - created_by: ObjectId
    - lifecycle: Lifecycle
```

#### 6. DeductionRule
```python
class DeductionType(Enum):
    LATE = "late"
    ABSENT = "absent"
    EARLY_LEAVE = "early_leave"

class DeductionRule:
    - id: ObjectId
    - type: DeductionType
    - min_minutes: int
    - max_minutes: int
    - deduction_percentage: float
    - is_active: bool
    - lifecycle: Lifecycle
```

#### 7. Payroll
```python
class PayrollStatus(Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    PAID = "paid"

class Payroll:
    - id: ObjectId
    - employee_id: ObjectId
    - period_start: date
    - period_end: date
    - basic_salary: float
    - total_working_days: int
    - actual_working_days: int
    - total_ot_hours: float
    - ot_payment: float
    - total_deductions: float
    - gross_salary: float
    - net_salary: float
    - status: PayrollStatus
    - breakdown: dict
    - processed_by: ObjectId
    - processed_at: datetime | None
    - lifecycle: Lifecycle
```

---

## 📁 Directory Structure

```
hrms/
├── domain/
│   ├── employee.py ✅
│   ├── leave.py ✅
│   ├── attendance.py 🔨
│   ├── overtime.py 🔨
│   ├── public_holiday.py 🔨
│   ├── working_schedule.py 🔨
│   ├── work_location.py 🔨
│   ├── deduction_rule.py 🔨
│   └── payroll.py 🔨
│
├── services/
│   ├── employee_service.py ✅
│   ├── leave_service.py ✅
│   ├── attendance_service.py 🔨
│   ├── overtime_service.py 🔨
│   ├── public_holiday_service.py 🔨
│   ├── working_schedule_service.py 🔨
│   ├── work_location_service.py 🔨
│   ├── deduction_service.py 🔨
│   ├── payroll_service.py 🔨
│   └── location_validator_service.py 🔨
│
├── repositories/
│   ├── employee_repository.py ✅
│   ├── leave_repository.py ✅
│   ├── attendance_repository.py 🔨
│   ├── overtime_repository.py 🔨
│   ├── public_holiday_repository.py 🔨
│   ├── working_schedule_repository.py 🔨
│   ├── work_location_repository.py 🔨
│   ├── deduction_rule_repository.py 🔨
│   └── payroll_repository.py 🔨
│
├── read_models/
│   ├── employee_read_model.py ✅
│   ├── leave_read_model.py ✅
│   ├── attendance_read_model.py 🔨
│   ├── overtime_read_model.py 🔨
│   ├── public_holiday_read_model.py 🔨
│   ├── payroll_read_model.py 🔨
│   └── report_read_model.py 🔨
│
├── factories/
│   ├── employee_factory.py ✅
│   ├── leave_factory.py ✅
│   ├── attendance_factory.py 🔨
│   ├── overtime_factory.py 🔨
│   ├── public_holiday_factory.py 🔨
│   ├── working_schedule_factory.py 🔨
│   ├── work_location_factory.py 🔨
│   └── payroll_factory.py 🔨
│
├── mapper/
│   ├── employee_mapper.py ✅
│   ├── leave_mapper.py ✅
│   ├── attendance_mapper.py 🔨
│   ├── overtime_mapper.py 🔨
│   ├── public_holiday_mapper.py 🔨
│   ├── working_schedule_mapper.py 🔨
│   ├── work_location_mapper.py 🔨
│   └── payroll_mapper.py 🔨
│
├── policies/
│   ├── leave_policy.py ✅
│   ├── attendance_policy.py 🔨
│   ├── overtime_policy.py 🔨
│   ├── location_policy.py 🔨
│   └── payroll_policy.py 🔨
│
├── data_transfer/
│   ├── request/
│   │   ├── employee_request.py ✅
│   │   ├── leave_request.py ✅
│   │   ├── attendance_request.py 🔨
│   │   ├── overtime_request.py 🔨
│   │   ├── public_holiday_request.py 🔨
│   │   ├── working_schedule_request.py 🔨
│   │   ├── work_location_request.py 🔨
│   │   └── payroll_request.py 🔨
│   │
│   └── response/
│       ├── employee_response.py ✅
│       ├── leave_response.py ✅
│       ├── attendance_response.py 🔨
│       ├── overtime_response.py 🔨
│       ├── public_holiday_response.py 🔨
│       ├── working_schedule_response.py 🔨
│       ├── work_location_response.py 🔨
│       ├── payroll_response.py 🔨
│       └── report_response.py 🔨
│
├── routes/
│   ├── employee_route.py ✅
│   ├── leave_route.py ✅
│   ├── attendance_route.py 🔨
│   ├── overtime_route.py 🔨
│   ├── public_holiday_route.py 🔨
│   ├── working_schedule_route.py 🔨
│   ├── work_location_route.py 🔨
│   ├── payroll_route.py 🔨
│   └── report_route.py 🔨
│
└── errors/
    ├── employee_exceptions.py ✅
    ├── leave_exceptions.py ✅
    ├── attendance_exceptions.py 🔨
    ├── overtime_exceptions.py 🔨
    ├── location_exceptions.py 🔨
    └── payroll_exceptions.py 🔨
```

---

## 🔄 Implementation Phases

### Phase 1: Foundation (Priority 1)
1. ✅ Working Schedule Management
2. ✅ Work Location Management
3. ✅ Public Holiday Management
4. ✅ Deduction Rules Configuration

### Phase 2: Core Operations (Priority 2)
5. ✅ Attendance System (Check-in/Check-out)
6. ✅ Location Validation
7. ✅ Overtime Request & Approval

### Phase 3: Payroll (Priority 3)
8. ✅ Payroll Calculation Engine
9. ✅ Payslip Generation
10. ✅ Payroll Reports

### Phase 4: Reporting (Priority 4)
11. ✅ Daily/Monthly Attendance Reports
12. ✅ OT Reports
13. ✅ Payroll Reports
14. ✅ Deduction Reports

---

## 🔐 Role-Based Access Control

### Administrator
- Full CRUD on all modules
- Configure system settings
- Approve wrong location check-ins
- Process payroll

### Employee
- Check-in/Check-out
- View own attendance
- Submit OT requests
- View payslips
- Submit location justifications

### Manager
- View team attendance
- Approve/Reject OT requests
- Generate team reports

### Payroll Manager
- View all attendance records
- Process payroll
- Generate payslips
- Generate payroll reports

---

## 📊 Database Collections

### New Collections
1. `attendances` - Daily check-in/check-out records
2. `overtime_requests` - OT requests and approvals
3. `public_holidays` - Khmer calendar holidays
4. `working_schedules` - Working hours configuration
5. `work_locations` - Approved work locations
6. `deduction_rules` - Late/absent deduction policies
7. `payrolls` - Monthly payroll records
8. `payroll_breakdowns` - Detailed payroll calculations

---

## 🔔 Notification Events

### Attendance
- `LATE_CHECK_IN` → Employee, Manager
- `WRONG_LOCATION` → Administrator
- `LOCATION_APPROVED` → Employee
- `LOCATION_REJECTED` → Employee

### Overtime
- `OT_SUBMITTED` → Manager
- `OT_APPROVED` → Employee
- `OT_REJECTED` → Employee
- `OT_DEADLINE_WARNING` → Employee (3 hours before)

### Payroll
- `PAYROLL_PROCESSED` → Employee
- `PAYSLIP_READY` → Employee

---

## 🧮 Business Logic

### Attendance Calculation
```python
def calculate_attendance_status(check_in_time, scheduled_start):
    late_minutes = (check_in_time - scheduled_start).total_seconds() / 60
    
    if late_minutes <= 0:
        return "PRESENT", 0, 0.0
    elif late_minutes <= 60:
        return "LATE", late_minutes, basic_salary * 0.05
    elif late_minutes <= 120:
        return "LATE", late_minutes, basic_salary * 0.10
    elif late_minutes <= 180:
        return "LATE", late_minutes, basic_salary * 0.15
    else:
        return "LATE", late_minutes, basic_salary * 0.20
```

### OT Payment Calculation
```python
def calculate_ot_payment(hours, basic_salary, is_weekend_or_holiday):
    hourly_rate = basic_salary / 22 / 8  # 22 working days, 8 hours/day
    
    if is_weekend_or_holiday:
        return hours * hourly_rate * 2.0  # 200%
    else:
        return hours * hourly_rate * 1.5  # 150%
```

### Location Validation
```python
def validate_location(check_in_lat, check_in_lng, work_location):
    distance = calculate_distance(
        check_in_lat, check_in_lng,
        work_location.latitude, work_location.longitude
    )
    
    return distance <= work_location.radius_meters
```

### Payroll Calculation
```python
def calculate_payroll(employee, period_start, period_end):
    # 1. Get attendance records
    attendances = get_attendances(employee_id, period_start, period_end)
    
    # 2. Calculate working days
    total_working_days = count_working_days(period_start, period_end)
    actual_working_days = count_present_days(attendances)
    
    # 3. Calculate OT payment
    ot_records = get_approved_ot(employee_id, period_start, period_end)
    total_ot_payment = sum(ot.calculated_payment for ot in ot_records)
    
    # 4. Calculate deductions
    total_deductions = sum(att.deduction_amount for att in attendances)
    
    # 5. Calculate salary
    daily_rate = basic_salary / total_working_days
    gross_salary = daily_rate * actual_working_days + total_ot_payment
    net_salary = gross_salary - total_deductions
    
    return Payroll(
        basic_salary=basic_salary,
        total_working_days=total_working_days,
        actual_working_days=actual_working_days,
        total_ot_hours=sum(ot.actual_hours for ot in ot_records),
        ot_payment=total_ot_payment,
        total_deductions=total_deductions,
        gross_salary=gross_salary,
        net_salary=net_salary
    )
```

---

## 📝 API Endpoints Summary

### Attendance (8 endpoints)
- POST `/api/hrms/attendance/check-in`
- POST `/api/hrms/attendance/check-out`
- GET `/api/hrms/attendance/my`
- GET `/api/hrms/attendance/team`
- POST `/api/hrms/attendance/{id}/justify`
- PATCH `/api/hrms/admin/attendance/{id}/approve-location`
- PATCH `/api/hrms/admin/attendance/{id}/reject-location`
- GET `/api/hrms/attendance/wrong-locations`

### Overtime (7 endpoints)
- POST `/api/hrms/overtime/request`
- GET `/api/hrms/overtime/my`
- GET `/api/hrms/overtime/team`
- PATCH `/api/hrms/manager/overtime/{id}/approve`
- PATCH `/api/hrms/manager/overtime/{id}/reject`
- GET `/api/hrms/overtime/pending`
- DELETE `/api/hrms/overtime/{id}`

### Public Holidays (5 endpoints)
- GET `/api/hrms/admin/holidays`
- POST `/api/hrms/admin/holidays`
- PATCH `/api/hrms/admin/holidays/{id}`
- DELETE `/api/hrms/admin/holidays/{id}`
- GET `/api/hrms/holidays/upcoming`

### Working Schedule (5 endpoints)
- GET `/api/hrms/admin/schedules`
- POST `/api/hrms/admin/schedules`
- PATCH `/api/hrms/admin/schedules/{id}`
- DELETE `/api/hrms/admin/schedules/{id}`
- GET `/api/hrms/schedules/my`

### Work Location (5 endpoints)
- GET `/api/hrms/admin/locations`
- POST `/api/hrms/admin/locations`
- PATCH `/api/hrms/admin/locations/{id}`
- DELETE `/api/hrms/admin/locations/{id}`
- GET `/api/hrms/locations/active`

### Deduction Rules (5 endpoints)
- GET `/api/hrms/admin/deduction-rules`
- POST `/api/hrms/admin/deduction-rules`
- PATCH `/api/hrms/admin/deduction-rules/{id}`
- DELETE `/api/hrms/admin/deduction-rules/{id}`
- GET `/api/hrms/deduction-rules/active`

### Payroll (8 endpoints)
- POST `/api/hrms/payroll/process`
- GET `/api/hrms/payroll/my`
- GET `/api/hrms/payroll/employee/{id}`
- GET `/api/hrms/payroll/period`
- GET `/api/hrms/payroll/{id}/payslip`
- GET `/api/hrms/payroll/reports/monthly`
- GET `/api/hrms/payroll/reports/summary`
- PATCH `/api/hrms/payroll/{id}/mark-paid`

### Reports (6 endpoints)
- GET `/api/hrms/reports/attendance/daily`
- GET `/api/hrms/reports/attendance/monthly`
- GET `/api/hrms/reports/overtime/summary`
- GET `/api/hrms/reports/deductions/summary`
- GET `/api/hrms/reports/team/performance`
- GET `/api/hrms/reports/export`

**Total New Endpoints: 54**

---

## 🎯 Success Criteria

1. ✅ All domain models implemented
2. ✅ All services with business logic
3. ✅ All repositories for data persistence
4. ✅ All API endpoints functional
5. ✅ Location validation working
6. ✅ OT calculation accurate
7. ✅ Payroll calculation correct
8. ✅ Notifications integrated
9. ✅ Reports generating correctly
10. ✅ Role-based access enforced

---

## ⏱️ Estimated Timeline

- **Phase 1**: 2-3 hours (Foundation)
- **Phase 2**: 3-4 hours (Core Operations)
- **Phase 3**: 2-3 hours (Payroll)
- **Phase 4**: 1-2 hours (Reporting)

**Total**: 8-12 hours of development

---

## 🚀 Next Steps

1. Start with Phase 1: Foundation modules
2. Implement domain models
3. Create services and repositories
4. Build API routes
5. Add notifications
6. Create reports
7. Test all workflows
8. Document APIs

Ready to begin implementation! 🎉

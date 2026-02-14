# HRMS Module - API Documentation

## Overview

The HRMS (Human Resource Management System) module provides comprehensive employee and leave management following the DDD architecture pattern used throughout the application.

## Architecture

```
hrms/
├── domain/           # Business entities (Employee, Leave, Payroll)
├── services/         # Application logic & orchestration
├── repositories/     # Data persistence layer
├── read_models/      # Optimized query models
├── factories/        # Domain object creation
├── mapper/           # Domain ↔ DTO conversion
├── policies/         # Business rules & authorization
├── data_transfer/    # Request/Response DTOs
│   ├── request/
│   └── response/
├── routes/           # HTTP endpoints
└── errors/           # Domain-specific exceptions
```

## Features

### ✅ Employee Management (CRUD Complete)
- Create employee profiles
- Update employee information
- Soft delete with restore capability
- Link employees to IAM accounts
- Photo upload support
- Manager assignment
- Contract management (permanent/contract)

### ✅ Leave Management (CRUD Complete)
- Submit leave requests
- List leaves with filters
- Update pending requests
- Approve/Reject by manager
- Cancel by employee
- Soft delete with restore
- Automatic notifications

### 🚧 Payroll Management (Domain Ready)
- Domain model defined
- Service implementation pending

---

## API Endpoints

### Employee Endpoints

#### 1. List Employees
```http
GET /api/hrms/admin/employees
Authorization: Bearer <token>
Role: hr_admin

Query Parameters:
- q: string (search query)
- page: number (default: 1)
- limit: number (default: 10, max: 100)
- include_deleted: boolean (default: false)
- deleted_only: boolean (default: false)

Response: EmployeePaginatedDTO
{
  "items": [EmployeeDTO],
  "total": number,
  "page": number,
  "page_size": number,
  "total_pages": number
}
```

#### 2. Get Employee
```http
GET /api/hrms/admin/employees/{employee_id}
Authorization: Bearer <token>
Role: hr_admin

Response: EmployeeDTO
{
  "id": "string",
  "user_id": "string | null",
  "employee_code": "string",
  "full_name": "string",
  "department": "string | null",
  "position": "string | null",
  "employment_type": "permanent | contract",
  "contract": {
    "start_date": "date",
    "end_date": "date",
    "salary_type": "monthly | daily | hourly",
    "rate": number,
    "leave_policy_id": "string | null",
    "pay_on_holiday": boolean,
    "pay_on_weekend": boolean
  } | null,
  "manager_user_id": "string | null",
  "schedule_id": "string | null",
  "status": "active | inactive",
  "created_by": "string | null",
  "photo_url": "string | null",
  "lifecycle": LifecycleDTO
}
```

#### 3. Create Employee
```http
POST /api/hrms/admin/employees
Authorization: Bearer <token>
Role: hr_admin

Request Body: EmployeeCreateSchema
{
  "employee_code": "string (2-30 chars)",
  "full_name": "string (2-120 chars)",
  "department": "string | null",
  "position": "string | null",
  "employment_type": "permanent | contract",
  "contract": ContractSchema | null,
  "manager_user_id": "string | null",
  "schedule_id": "string | null",
  "status": "active"
}

Response: EmployeeDTO
```

**Notifications Triggered:**
- `NEW_TEAM_MEMBER` → Manager (if assigned)

#### 4. Update Employee
```http
PATCH /api/hrms/admin/employees/{employee_id}
Authorization: Bearer <token>
Role: hr_admin

Request Body: EmployeeUpdateSchema (all fields optional)
{
  "full_name": "string",
  "department": "string",
  "position": "string",
  "employment_type": "permanent | contract",
  "contract": ContractSchema,
  "manager_user_id": "string",
  "schedule_id": "string",
  "status": "string"
}

Response: EmployeeDTO
```

#### 5. Create Account for Employee
```http
POST /api/hrms/admin/employees/{employee_id}/create-account
Authorization: Bearer <token>
Role: hr_admin

Request Body: EmployeeCreateAccountSchema
{
  "email": "email",
  "password": "string (min 6 chars)",
  "username": "string | null",
  "role": "employee | manager | payroll_manager | admin"
}

Response: EmployeeWithAccountDTO
{
  "employee": EmployeeDTO,
  "user": IAMBaseDataDTO
}
```

**Notifications Triggered:**
- `ACCOUNT_CREATED` → Employee

#### 6. Upload Employee Photo
```http
PATCH /uploads/employee/{employee_id}
Content-Type: multipart/form-data

Form Data:
- photo: File (png, jpg, jpeg, gif, webp)
- old_photo_url: string (optional)

Response:
{
  "success": boolean,
  "message": "string",
  "photo_url": "string",
  "employee": EmployeeDTO
}
```

#### 7. Soft Delete Employee
```http
DELETE /api/hrms/admin/employees/{employee_id}/soft-delete
Authorization: Bearer <token>
Role: hr_admin

Response: EmployeeDTO (with deleted_at set)
```

#### 8. Restore Employee
```http
POST /api/hrms/admin/employees/{employee_id}/restore
Authorization: Bearer <token>
Role: hr_admin

Response: EmployeeDTO (with deleted_at cleared)
```

---

### Leave Endpoints

#### 1. List Leaves
```http
GET /api/hrms/leaves
Authorization: Bearer <token>
Role: hr_admin, manager

Query Parameters:
- q: string (search in reason)
- page: number (default: 1)
- limit: number (default: 10, max: 100)
- employee_id: string (filter by employee)
- status: string (pending | approved | rejected | cancelled)
- include_deleted: boolean (default: false)
- deleted_only: boolean (default: false)

Response: LeavePaginatedDTO
{
  "items": [LeaveDTO],
  "total": number,
  "page": number,
  "page_size": number,
  "total_pages": number
}
```

#### 2. Get Leave
```http
GET /api/hrms/leaves/{leave_id}
Authorization: Bearer <token>
Role: hr_admin, manager, employee

Response: LeaveDTO
{
  "id": "string",
  "employee_id": "string",
  "leave_type": "annual | sick | unpaid | other",
  "start_date": "date",
  "end_date": "date",
  "reason": "string",
  "contract_start": "date",
  "contract_end": "date",
  "is_paid": boolean,
  "status": "pending | approved | rejected | cancelled",
  "manager_user_id": "string | null",
  "manager_comment": "string | null",
  "lifecycle": LifecycleDTO
}
```

#### 3. Submit Leave Request
```http
POST /api/hrms/employee/leaves
Authorization: Bearer <token>
Role: employee, manager

Request Body: LeaveCreateSchema
{
  "employee_id": "string | null",  // Optional, extracted from token
  "leave_type": "annual | sick | unpaid | other",
  "start_date": "date",
  "end_date": "date",
  "reason": "string (max 500 chars)"
}

Response: LeaveDTO
```

**Notifications Triggered:**
- `LEAVE_SUBMITTED` → Manager

**Business Rules:**
- Leave dates must be within contract period
- End date must be >= start date
- Contract employees must have valid contract

#### 4. Update Leave Request
```http
PATCH /api/hrms/leaves/{leave_id}
Authorization: Bearer <token>
Role: hr_admin, employee

Request Body: LeaveUpdateSchema (all fields optional)
{
  "leave_type": "annual | sick | unpaid | other",
  "start_date": "date",
  "end_date": "date",
  "reason": "string"
}

Response: LeaveDTO
```

**Business Rules:**
- Only pending requests can be updated
- Dates must remain within contract period

#### 5. Approve Leave
```http
PATCH /api/hrms/manager/leaves/{leave_id}/approve
Authorization: Bearer <token>
Role: manager, hr_admin

Request Body: LeaveReviewSchema
{
  "comment": "string (max 500 chars) | null"
}

Response: LeaveDTO
```

**Notifications Triggered:**
- `LEAVE_APPROVED` → Employee

**Business Rules:**
- Only pending requests can be approved
- Manager must have permission (policy check)

#### 6. Reject Leave
```http
PATCH /api/hrms/manager/leaves/{leave_id}/reject
Authorization: Bearer <token>
Role: manager, hr_admin

Request Body: LeaveReviewSchema
{
  "comment": "string (max 500 chars) | null"
}

Response: LeaveDTO
```

**Notifications Triggered:**
- `LEAVE_REJECTED` → Employee

**Business Rules:**
- Only pending requests can be rejected
- Manager must have permission (policy check)

#### 7. Cancel Leave
```http
PATCH /api/hrms/leaves/{leave_id}/cancel
Authorization: Bearer <token>
Role: employee, hr_admin

Response: LeaveDTO
```

**Business Rules:**
- Only pending requests can be cancelled
- Employee can cancel their own requests

#### 8. Soft Delete Leave
```http
DELETE /api/hrms/leaves/{leave_id}/soft-delete
Authorization: Bearer <token>
Role: hr_admin

Response: LeaveDTO (with deleted_at set)
```

#### 9. Restore Leave
```http
POST /api/hrms/leaves/{leave_id}/restore
Authorization: Bearer <token>
Role: hr_admin

Response: LeaveDTO (with deleted_at cleared)
```

---

## Domain Models

### Employee
```python
class EmploymentType(Enum):
    PERMANENT = "permanent"
    CONTRACT = "contract"

class Employee:
    - id: ObjectId
    - user_id: ObjectId | None
    - employee_code: str
    - full_name: str
    - employment_type: EmploymentType
    - department: str | None
    - position: str | None
    - contract: dict | None
    - manager_user_id: ObjectId | None
    - schedule_id: ObjectId | None
    - status: str
    - created_by: ObjectId
    - photo_url: str | None
    - lifecycle: Lifecycle
```

### LeaveRequest
```python
class LeaveType(Enum):
    ANNUAL = "annual"
    SICK = "sick"
    UNPAID = "unpaid"
    OTHER = "other"

class LeaveStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class LeaveRequest:
    - id: ObjectId
    - employee_id: ObjectId
    - leave_type: LeaveType
    - start_date: date
    - end_date: date
    - reason: str
    - contract_start: date
    - contract_end: date
    - is_paid: bool
    - status: LeaveStatus
    - manager_user_id: ObjectId | None
    - manager_comment: str | None
    - lifecycle: Lifecycle
```

---

## Business Rules

### Employee Management
1. **Contract Validation**: Contract employees MUST have valid contract with start/end dates
2. **Manager Notification**: When employee is assigned to manager, manager receives notification
3. **Account Creation**: Employee can only have one linked IAM account
4. **Photo Upload**: Supports png, jpg, jpeg, gif, webp formats
5. **Soft Delete**: Deleted employees can be restored by hr_admin

### Leave Management
1. **Date Validation**: 
   - End date must be >= start date
   - Dates must be within employee's contract period
2. **Status Transitions**:
   - PENDING → APPROVED (by manager)
   - PENDING → REJECTED (by manager)
   - PENDING → CANCELLED (by employee)
3. **Update Restrictions**: Only PENDING requests can be updated
4. **Manager Authorization**: Policy checks ensure manager has permission to review
5. **Notifications**: Automatic notifications for submit, approve, reject actions

---

## Error Handling

### Employee Exceptions
- `EmployeeNotFoundException`: Employee ID not found
- `ContractRequiredException`: Contract employee missing contract data
- `ContractDateInvalidException`: Invalid contract date range
- `EmployeeDeletedException`: Operation on deleted employee

### Leave Exceptions
- `LeaveNotFoundException`: Leave ID not found
- `LeaveDateRangeInvalidException`: Invalid date range
- `LeaveOutsideContractException`: Dates outside contract period
- `LeaveAlreadyReviewedException`: Attempt to modify reviewed request
- `LeaveRequestDeletedException`: Operation on deleted request

---

## Integration Points

### IAM Context
- Employee account creation links to IAM users
- Role-based access control (hr_admin, manager, employee)
- JWT authentication for all endpoints

### Notification Context
- `ACCOUNT_CREATED`: Employee account ready
- `NEW_TEAM_MEMBER`: Manager notified of new hire
- `LEAVE_SUBMITTED`: Manager notified of leave request
- `LEAVE_APPROVED`: Employee notified of approval
- `LEAVE_REJECTED`: Employee notified of rejection

### Shared Context
- Lifecycle management (soft delete, restore)
- Model converters (Pydantic ↔ MongoDB)
- Response decorators
- Authentication utilities

---

## Database Collections

### employees
```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId | null,
  "employee_code": String,
  "full_name": String,
  "department": String | null,
  "position": String | null,
  "employment_type": "permanent" | "contract",
  "contract": {
    "start_date": ISODate,
    "end_date": ISODate,
    "salary_type": "monthly" | "daily" | "hourly",
    "rate": Number,
    "leave_policy_id": ObjectId | null,
    "pay_on_holiday": Boolean,
    "pay_on_weekend": Boolean
  } | null,
  "manager_user_id": ObjectId | null,
  "schedule_id": ObjectId | null,
  "status": "active" | "inactive",
  "created_by": ObjectId,
  "photo_url": String | null,
  "lifecycle": {
    "created_at": ISODate,
    "updated_at": ISODate,
    "deleted_at": ISODate | null,
    "deleted_by": ObjectId | null
  }
}
```

### leave_requests
```javascript
{
  "_id": ObjectId,
  "employee_id": ObjectId,
  "leave_type": "annual" | "sick" | "unpaid" | "other",
  "start_date": ISODate,
  "end_date": ISODate,
  "reason": String,
  "contract_start": ISODate,
  "contract_end": ISODate,
  "is_paid": Boolean,
  "status": "pending" | "approved" | "rejected" | "cancelled",
  "manager_user_id": ObjectId | null,
  "manager_comment": String | null,
  "lifecycle": {
    "created_at": ISODate,
    "updated_at": ISODate,
    "deleted_at": ISODate | null,
    "deleted_by": ObjectId | null
  }
}
```

---

## Testing

### Unit Tests (Recommended)
```python
# Test employee domain
test_employee_contract_validation()
test_employee_soft_delete()
test_employee_link_user()

# Test leave domain
test_leave_date_validation()
test_leave_approve_reject()
test_leave_cancel()
test_leave_outside_contract()
```

### Integration Tests (Recommended)
```python
# Test employee service
test_create_employee_with_notification()
test_update_employee()
test_create_account_for_employee()

# Test leave service
test_submit_leave_with_notification()
test_approve_leave_with_notification()
test_manager_authorization()
```

---

## Future Enhancements

### Payroll Module
- [ ] Salary calculation service
- [ ] Payslip generation
- [ ] Tax calculation
- [ ] Payment history tracking

### Leave Enhancements
- [ ] Leave balance tracking
- [ ] Annual leave accrual
- [ ] Leave policy management
- [ ] Bulk leave approval
- [ ] Leave calendar view

### Employee Enhancements
- [ ] Performance reviews
- [ ] Training records
- [ ] Document management
- [ ] Emergency contacts
- [ ] Onboarding workflow

---

## Version History

- **v1.0.0** (Current): Complete CRUD for Employee and Leave management
- **v0.1.0**: Initial domain models and basic endpoints

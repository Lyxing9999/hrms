# HRMS Module - Quick Start Guide

## 🚀 Getting Started

The HRMS module is now fully operational with complete CRUD operations for Employee and Leave management.

---

## 📍 Base URL
```
http://localhost:5001/api/hrms
```

---

## 🔑 Authentication

All endpoints require JWT authentication:
```http
Authorization: Bearer YOUR_JWT_TOKEN
```

Get token by logging in:
```http
POST http://localhost:5001/api/iam/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "your_password"
}
```

---

## 👥 Employee Management

### Create Employee
```http
POST /api/hrms/admin/employees
Authorization: Bearer {token}

{
  "employee_code": "EMP001",
  "full_name": "John Doe",
  "department": "Engineering",
  "position": "Developer",
  "employment_type": "permanent",
  "status": "active"
}
```

### List Employees
```http
GET /api/hrms/admin/employees?page=1&limit=10
Authorization: Bearer {token}
```

### Update Employee
```http
PATCH /api/hrms/admin/employees/{employee_id}
Authorization: Bearer {token}

{
  "position": "Senior Developer",
  "department": "Engineering"
}
```

### Create Account for Employee
```http
POST /api/hrms/admin/employees/{employee_id}/create-account
Authorization: Bearer {token}

{
  "email": "john@company.com",
  "password": "SecurePass123",
  "role": "employee"
}
```

---

## 📅 Leave Management

### Submit Leave Request
```http
POST /api/hrms/employee/leaves
Authorization: Bearer {token}

{
  "employee_id": "EMPLOYEE_ID",
  "leave_type": "annual",
  "start_date": "2026-03-01",
  "end_date": "2026-03-05",
  "reason": "Family vacation"
}
```

### List Leaves
```http
GET /api/hrms/leaves?page=1&limit=10
Authorization: Bearer {token}
```

### Approve Leave (Manager)
```http
PATCH /api/hrms/manager/leaves/{leave_id}/approve
Authorization: Bearer {token}

{
  "comment": "Approved!"
}
```

### Reject Leave (Manager)
```http
PATCH /api/hrms/manager/leaves/{leave_id}/reject
Authorization: Bearer {token}

{
  "comment": "Sorry, we need you during this period."
}
```

---

## 🔍 Search & Filter

### Search Employees
```http
GET /api/hrms/admin/employees?q=john&page=1&limit=10
```

### Filter Leaves by Status
```http
GET /api/hrms/leaves?status=pending
```

### Filter Leaves by Employee
```http
GET /api/hrms/leaves?employee_id=EMPLOYEE_ID
```

### Include Deleted Records
```http
GET /api/hrms/admin/employees?include_deleted=true
```

---

## 🗑️ Soft Delete & Restore

### Soft Delete Employee
```http
DELETE /api/hrms/admin/employees/{employee_id}/soft-delete
Authorization: Bearer {token}
```

### Restore Employee
```http
POST /api/hrms/admin/employees/{employee_id}/restore
Authorization: Bearer {token}
```

### Soft Delete Leave
```http
DELETE /api/hrms/leaves/{leave_id}/soft-delete
Authorization: Bearer {token}
```

### Restore Leave
```http
POST /api/hrms/leaves/{leave_id}/restore
Authorization: Bearer {token}
```

---

## 📋 Common Workflows

### 1. Onboard New Employee
```bash
# Step 1: Create employee profile
POST /api/hrms/admin/employees
{
  "employee_code": "EMP001",
  "full_name": "John Doe",
  "employment_type": "permanent",
  ...
}

# Step 2: Create system account
POST /api/hrms/admin/employees/{id}/create-account
{
  "email": "john@company.com",
  "password": "SecurePass123",
  "role": "employee"
}

# Step 3: Upload photo (optional)
PATCH /uploads/employee/{id}
[multipart/form-data with photo file]
```

### 2. Leave Request Flow
```bash
# Step 1: Employee submits leave
POST /api/hrms/employee/leaves
{
  "leave_type": "annual",
  "start_date": "2026-03-01",
  "end_date": "2026-03-05",
  "reason": "Vacation"
}

# Step 2: Manager reviews
GET /api/hrms/leaves?status=pending

# Step 3: Manager approves/rejects
PATCH /api/hrms/manager/leaves/{id}/approve
{
  "comment": "Approved!"
}
```

---

## 🎭 Roles & Permissions

| Role | Permissions |
|------|-------------|
| **hr_admin** | Full access to all HRMS operations |
| **manager** | Review leaves, view employees |
| **employee** | Submit/update/cancel own leaves |

---

## 🔔 Automatic Notifications

The system automatically sends notifications for:

### Employee Events
- ✅ Account created → Employee
- ✅ New team member → Manager

### Leave Events
- ✅ Leave submitted → Manager
- ✅ Leave approved → Employee
- ✅ Leave rejected → Employee

---

## 📚 Full Documentation

For complete API documentation, see:
- **API Reference**: `backend/app/contexts/hrms/HRMS_API.md`
- **Test Endpoints**: `backend/HRMS_TEST_ENDPOINTS.http`
- **Technical Details**: `backend/app/contexts/hrms/COMPLETION_SUMMARY.md`

---

## 🐛 Troubleshooting

### "Missing or invalid token"
- Ensure you're logged in and using a valid JWT token
- Token format: `Authorization: Bearer YOUR_TOKEN`

### "Employee not found"
- Verify the employee_id exists
- Check if employee is soft-deleted (use `include_deleted=true`)

### "Cannot update leave request"
- Only PENDING requests can be updated
- Approved/Rejected/Cancelled requests are immutable

### "Permission denied"
- Check your role has access to the endpoint
- Managers can only review leaves, not create employees

---

## ✅ Quick Health Check

Test if HRMS is running:
```bash
# Should return 401 (authentication required)
curl http://localhost:5001/api/hrms/admin/employees

# Should return 200 with token
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5001/api/hrms/admin/employees
```

---

## 🎯 Next Steps

1. **Test the APIs** using `backend/HRMS_TEST_ENDPOINTS.http`
2. **Add database indexes** for better performance
3. **Integrate with frontend** (Nuxt 3 components)
4. **Add unit tests** for domain logic
5. **Configure notifications** (email/SMS)

---

**Status**: ✅ Fully Operational  
**Version**: 1.0.0  
**Last Updated**: February 9, 2026

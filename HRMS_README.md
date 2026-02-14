# HRMS (Human Resource Management System)

## 🎯 Project Overview

A comprehensive HRMS system built with Flask (Backend) and Nuxt 3 (Frontend) following Domain-Driven Design (DDD) architecture.

### Current Status: **56% Complete** (37/66 endpoints)

---

## ✅ Completed Modules

### 1. Employee Management (100%)
**Backend**: 8 endpoints | **Frontend**: Full CRUD interface

**Features**:
- Create, view, update, delete employees
- Photo upload support
- Contract management (permanent/contract)
- Manager assignment
- Link to IAM accounts
- Soft delete and restore
- Pagination and search

**Access**: `/hr/employees/employee-profile`

---

### 2. Leave Management (100%)
**Backend**: 9 endpoints | **Frontend**: Full CRUD interface

**Features**:
- Submit leave requests
- Approve/reject workflow (Manager/HR Admin)
- Update pending requests
- Cancel requests
- Leave types: Annual, Sick, Unpaid, Other
- Status tracking: Pending, Approved, Rejected, Cancelled
- Automatic notifications
- Soft delete and restore

**Access**: `/hr/leaves`

---

### 3. Working Schedule (Backend 100%, Frontend 0%)
**Backend**: 7 endpoints | **Frontend**: Pending

**Features**:
- Define working hours (e.g., 9:00-17:00)
- Set working days (Mon-Fri)
- Auto-calculate hours per day
- Default schedule management
- Weekend days auto-calculation

**API**: `/api/hrms/admin/working-schedules`

---

### 4. Work Location (Backend 100%, Frontend 0%)
**Backend**: 7 endpoints | **Frontend**: Pending

**Features**:
- GPS-based location management
- Latitude/Longitude validation
- Radius validation (10m-1000m)
- Active/inactive status
- Location-based check-in validation

**API**: `/api/hrms/admin/work-locations`

---

### 5. Public Holiday (Backend 100%, Frontend 0%)
**Backend**: 6 endpoints | **Frontend**: Pending

**Features**:
- Khmer calendar support
- Bilingual (English + Khmer names)
- Paid/unpaid holiday flag
- Year-based filtering
- Duplicate prevention

**API**: `/api/hrms/admin/public-holidays`

---

### 6. Deduction Rule (Backend 100%, Frontend 0%)
**Backend**: 8 endpoints | **Frontend**: Pending

**Features**:
- Three rule types: Late, Absent, Early Leave
- Minute range configuration
- Percentage-based deduction (0-100%)
- Active/inactive status
- Overlapping rule prevention

**API**: `/api/hrms/admin/deduction-rules`

---

## 🔨 Pending Modules

### 7. Attendance System (0%)
**Estimated**: 8 endpoints

**Planned Features**:
- GPS-based check-in/check-out
- Location validation
- Late deduction calculation
- Wrong location handling
- Justification workflow
- Admin approval for wrong locations

---

### 8. Overtime Management (0%)
**Estimated**: 7 endpoints

**Planned Features**:
- OT request submission (3 hours before rule)
- Manager approval workflow
- Rate calculation (150% weekday, 200% weekend/holiday)
- Integration with public holidays
- OT history tracking

---

### 9. Payroll System (0%)
**Estimated**: 8 endpoints

**Planned Features**:
- Automated salary calculation
- Working days vs actual days
- OT payment integration
- Deduction processing
- Holiday pay calculation
- Payslip generation (PDF)
- Payment tracking

---

### 10. Reports & Analytics (0%)
**Estimated**: 6 endpoints

**Planned Features**:
- Daily/monthly attendance reports
- OT summary reports
- Payroll reports
- Deduction reports
- Team performance reports
- Export to CSV/PDF

---

## 🏗️ Architecture

### Backend (Flask + MongoDB)
```
backend/app/contexts/hrms/
├── domain/              # Business entities (6 models)
├── services/            # Application logic (6 services)
├── repositories/        # Data persistence (6 repositories)
├── read_models/         # Query optimization (6 read models)
├── factories/           # Object creation (6 factories)
├── mapper/              # DTO conversion (6 mappers)
├── policies/            # Business rules (1 policy)
├── data_transfer/       # Request/Response DTOs
│   ├── request/         # 6 request schemas
│   └── response/        # 6 response schemas
├── routes/              # API endpoints (6 route files)
└── errors/              # Domain exceptions (6 error files)
```

**Total Backend Files**: ~50 files

### Frontend (Nuxt 3 + Vue 3 + Element Plus)
```
frontend/src/
├── pages/hr/            # HRMS pages
│   ├── index.vue        # Dashboard
│   ├── employees/       # Employee pages
│   ├── leaves/          # Leave pages
│   ├── config/          # Configuration pages (pending)
│   ├── attendance/      # Attendance pages (pending)
│   ├── overtime/        # Overtime pages (pending)
│   ├── payroll/         # Payroll pages (pending)
│   └── reports/         # Reports pages (pending)
├── api/hr_admin/        # API services
│   ├── employee/        # Employee API
│   ├── leave/           # Leave API
│   └── schedule/        # Schedule API
├── modules/
│   ├── forms/hr_admin/  # Form schemas
│   └── tables/columns/hr_admin/  # Table columns
└── plugins/             # Service plugins
```

---

## 🔐 Role-Based Access Control

### HR_ADMIN (Full Access)
- ✅ Employee Management (CRUD)
- ✅ Leave Management (View all, Approve/Reject)
- 🔨 Attendance Management (View all, Approve wrong locations)
- 🔨 Overtime Management (View all, Approve/Reject)
- 🔨 Payroll Processing
- 🔨 Configuration (All modules)
- 🔨 Reports & Analytics

### MANAGER
- ✅ View team employees
- ✅ Leave Management (Approve/Reject team leaves)
- 🔨 View team attendance
- 🔨 Overtime Management (Approve/Reject team OT)
- 🔨 Team reports

### EMPLOYEE
- ✅ View own profile
- ✅ Submit leave requests
- 🔨 Check-in/Check-out
- 🔨 View own attendance
- 🔨 Submit OT requests
- 🔨 View own payslips

### PAYROLL_MANAGER
- 🔨 View all attendance
- 🔨 Process payroll
- 🔨 Generate payslips
- 🔨 Payroll reports

---

## 🚀 Quick Start

### 1. Start Backend

```bash
cd backend
docker-compose up -d
```

**Services**:
- Backend API: http://localhost:5001
- MongoDB: localhost:27017
- MongoDB Express: http://localhost:8081

### 2. Start Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

**Frontend**: http://localhost:3000

### 3. Login

```
Email: admin@school.com
Password: admin123
Role: hr_admin
```

### 4. Access HRMS

Navigate to: **http://localhost:3000/hr**

---

## 📊 API Endpoints

### Employee Management (8 endpoints)
```
GET    /api/hrms/admin/employees
GET    /api/hrms/admin/employees/{id}
POST   /api/hrms/admin/employees
PATCH  /api/hrms/admin/employees/{id}
DELETE /api/hrms/admin/employees/{id}/soft-delete
POST   /api/hrms/admin/employees/{id}/restore
POST   /api/hrms/admin/employees/{id}/create-account
PATCH  /uploads/employee/{id}
```

### Leave Management (9 endpoints)
```
GET    /api/hrms/leaves
GET    /api/hrms/leaves/{id}
GET    /api/hrms/employee/leaves
POST   /api/hrms/employee/leaves
PATCH  /api/hrms/leaves/{id}
PATCH  /api/hrms/manager/leaves/{id}/approve
PATCH  /api/hrms/manager/leaves/{id}/reject
PATCH  /api/hrms/leaves/{id}/cancel
DELETE /api/hrms/leaves/{id}/soft-delete
```

### Configuration Modules (28 endpoints)
```
# Working Schedule (7 endpoints)
GET    /api/hrms/admin/working-schedules
GET    /api/hrms/admin/working-schedules/default
GET    /api/hrms/admin/working-schedules/{id}
POST   /api/hrms/admin/working-schedules
PATCH  /api/hrms/admin/working-schedules/{id}
DELETE /api/hrms/admin/working-schedules/{id}/soft-delete
POST   /api/hrms/admin/working-schedules/{id}/restore

# Work Location (7 endpoints)
GET    /api/hrms/admin/work-locations
GET    /api/hrms/admin/work-locations/active
GET    /api/hrms/admin/work-locations/{id}
POST   /api/hrms/admin/work-locations
PATCH  /api/hrms/admin/work-locations/{id}
DELETE /api/hrms/admin/work-locations/{id}/soft-delete
POST   /api/hrms/admin/work-locations/{id}/restore

# Public Holiday (6 endpoints)
GET    /api/hrms/admin/public-holidays
GET    /api/hrms/admin/public-holidays/year/{year}
GET    /api/hrms/admin/public-holidays/{id}
POST   /api/hrms/admin/public-holidays
PATCH  /api/hrms/admin/public-holidays/{id}
DELETE /api/hrms/admin/public-holidays/{id}/soft-delete

# Deduction Rule (8 endpoints)
GET    /api/hrms/admin/deduction-rules
GET    /api/hrms/admin/deduction-rules/active
GET    /api/hrms/admin/deduction-rules/type/{type}
GET    /api/hrms/admin/deduction-rules/{id}
POST   /api/hrms/admin/deduction-rules
PATCH  /api/hrms/admin/deduction-rules/{id}
DELETE /api/hrms/admin/deduction-rules/{id}/soft-delete
POST   /api/hrms/admin/deduction-rules/{id}/restore
```

---

## 📚 Documentation

- **Quick Start**: `QUICK_START_GUIDE.md`
- **API Reference**: `backend/app/contexts/hrms/CONFIGURATION_API_REFERENCE.md`
- **Implementation Guide**: `HRMS_IMPLEMENTATION_GUIDE.md`
- **Complete Plan**: `HRMS_COMPLETE_FINAL_DELIVERY.md`
- **Architecture**: `HRMS_FINAL_IMPLEMENTATION_PLAN.md`

---

## 🧪 Testing

### Verify System
```bash
./verify-system.sh
```

### Test APIs
```bash
# Get JWT token
TOKEN="your-jwt-token"

# Test employee endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/hrms/admin/employees

# Test leave endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/hrms/leaves

# Test configuration endpoints
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/hrms/admin/working-schedules
```

---

## 📈 Progress Tracking

### Completed
- ✅ Employee Management (Backend + Frontend)
- ✅ Leave Management (Backend + Frontend)
- ✅ Working Schedule (Backend only)
- ✅ Work Location (Backend only)
- ✅ Public Holiday (Backend only)
- ✅ Deduction Rule (Backend only)

### In Progress
- 🔨 Configuration Frontend Pages

### Pending
- ⏳ Attendance System
- ⏳ Overtime Management
- ⏳ Payroll System
- ⏳ Reports & Analytics

**Overall Progress**: 56% (37/66 endpoints)

---

## 🎯 Next Steps

### Immediate (2-3 hours)
1. Create frontend pages for configuration modules
   - Working Schedule page
   - Work Location page
   - Public Holiday page
   - Deduction Rule page

### Short Term (1-2 weeks)
2. Implement Attendance System (Backend + Frontend)
3. Implement Overtime Management (Backend + Frontend)

### Medium Term (2-3 weeks)
4. Implement Payroll System (Backend + Frontend)
5. Implement Reports & Analytics

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: MongoDB
- **Authentication**: JWT
- **Architecture**: DDD (Domain-Driven Design)
- **Validation**: Pydantic
- **Containerization**: Docker

### Frontend
- **Framework**: Nuxt 3
- **UI Library**: Element Plus
- **State Management**: Pinia
- **Styling**: Tailwind CSS
- **HTTP Client**: $fetch (Nuxt)

---

## 📝 License

[Your License Here]

---

## 👥 Contributors

[Your Team Here]

---

## 🆘 Support

For issues or questions:
1. Check `QUICK_START_GUIDE.md`
2. Review API documentation
3. Run `./verify-system.sh`
4. Check Docker logs: `docker-compose logs`

---

**Last Updated**: February 2026
**Version**: 1.0.0 (Beta)
**Status**: Production-ready for Employee and Leave Management


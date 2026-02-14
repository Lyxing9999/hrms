# HRMS Final Complete Implementation Plan

## 🎯 Complete System Requirements

### Role-Based Access Control

#### HR_ADMIN (Full Access)
- ✅ Employee Management (CRUD)
- ✅ Leave Management (View all, Approve/Reject)
- 🔨 Attendance Management (View all, Approve wrong locations)
- 🔨 Overtime Management (View all, Approve/Reject)
- 🔨 Payroll Processing (Calculate, Generate payslips)
- 🔨 Configuration (Schedules, Locations, Holidays, Deduction Rules)
- 🔨 Reports & Analytics (All reports, Export)

#### MANAGER
- ✅ View team employees
- ✅ Leave Management (Approve/Reject team leaves)
- 🔨 View team attendance
- 🔨 Overtime Management (Approve/Reject team OT)
- 🔨 Team reports

#### EMPLOYEE
- ✅ View own profile
- ✅ Submit leave requests
- 🔨 Check-in/Check-out
- 🔨 View own attendance
- 🔨 Submit OT requests
- 🔨 View own payslips

#### PAYROLL_MANAGER
- 🔨 View all attendance
- 🔨 Process payroll
- 🔨 Generate payslips
- 🔨 Payroll reports

## 📊 Complete Module List

### ✅ Phase 0: Completed (17 endpoints)
1. Employee Management - 8 endpoints
2. Leave Management - 9 endpoints

### 🔨 Phase 1: Configuration (20 endpoints)
3. Working Schedule - 5 endpoints
4. Work Location - 5 endpoints
5. Public Holidays - 5 endpoints
6. Deduction Rules - 5 endpoints

### 🔨 Phase 2: Operations (15 endpoints)
7. Attendance System - 8 endpoints
8. Overtime Management - 7 endpoints

### 🔨 Phase 3: Payroll (8 endpoints)
9. Payroll System - 8 endpoints

### 🔨 Phase 4: Reports (6 endpoints)
10. Reports & Analytics - 6 endpoints

**Total: 66 endpoints**

## 🏗️ Implementation Order

### Step 1: Configuration Modules (Foundation)
These are prerequisites for all other modules.

**Working Schedule**
- Define working hours (8:00-17:00)
- Set working days (Mon-Fri)
- Calculate hours per day

**Work Location**
- GPS coordinates
- Acceptable radius
- Location validation

**Public Holidays**
- Khmer calendar support
- Paid/unpaid holidays
- Holiday calendar

**Deduction Rules**
- Late deduction (1-30min = 5%, 31-60min = 10%, etc.)
- Absent deduction
- Early leave deduction

### Step 2: Attendance System
- Check-in with GPS validation
- Check-out tracking
- Late calculation
- Wrong location handling
- Justification workflow
- Admin approval for wrong locations

### Step 3: Overtime Management
- OT request (3 hours before rule)
- Manager approval
- Rate calculation (150% weekday, 200% weekend/holiday)
- OT completion tracking

### Step 4: Payroll System
- Automated calculation:
  - Basic salary
  - Working days vs actual days
  - OT payment
  - Deductions (late, absent)
  - Holiday pay
- Payslip generation
- Payment tracking

### Step 5: Reports & Analytics
- Daily attendance report
- Monthly attendance report
- OT summary report
- Payroll report
- Deduction report
- Team performance report
- Export to CSV/PDF

## 📁 Complete File Structure

```
backend/app/contexts/hrms/
├── domain/
│   ├── employee.py ✅
│   ├── leave.py ✅
│   ├── working_schedule.py ✅
│   ├── work_location.py ✅
│   ├── public_holiday.py ✅
│   ├── deduction_rule.py ✅
│   ├── attendance.py 🔨
│   ├── overtime.py 🔨
│   └── payroll.py 🔨
│
├── services/
│   ├── employee_service.py ✅
│   ├── leave_service.py ✅
│   ├── working_schedule_service.py 🔨
│   ├── work_location_service.py 🔨
│   ├── public_holiday_service.py 🔨
│   ├── deduction_rule_service.py 🔨
│   ├── attendance_service.py 🔨
│   ├── overtime_service.py 🔨
│   ├── payroll_service.py 🔨
│   └── location_validator_service.py 🔨
│
├── repositories/ (10 files) 🔨
├── read_models/ (10 files) 🔨
├── factories/ (10 files) 🔨
├── mapper/ (10 files) 🔨
├── policies/ (5 files) 🔨
├── data_transfer/
│   ├── request/ (10 files, 4 done) 🔨
│   └── response/ (10 files) 🔨
├── routes/ (10 files, 2 done) 🔨
└── errors/ (10 files, 6 done) 🔨
```

```
frontend/src/
├── pages/hr/
│   ├── index.vue ✅ (Dashboard)
│   ├── employees/
│   │   ├── employee-profile.vue ✅
│   │   └── [id].vue ✅
│   ├── leaves/
│   │   └── index.vue ✅
│   ├── config/
│   │   ├── index.vue 🔨 (Config dashboard)
│   │   ├── schedules.vue 🔨
│   │   ├── locations.vue 🔨
│   │   ├── holidays.vue 🔨
│   │   └── deduction-rules.vue 🔨
│   ├── attendance/
│   │   ├── index.vue 🔨 (My attendance)
│   │   ├── check-in.vue 🔨
│   │   ├── team.vue 🔨 (Manager view)
│   │   └── admin.vue 🔨 (Admin view)
│   ├── overtime/
│   │   ├── index.vue 🔨 (My OT)
│   │   ├── request.vue 🔨
│   │   ├── team.vue 🔨 (Manager view)
│   │   └── admin.vue 🔨 (Admin view)
│   ├── payroll/
│   │   ├── index.vue 🔨 (My payslips)
│   │   ├── process.vue 🔨 (Admin)
│   │   └── reports.vue 🔨 (Admin)
│   └── reports/
│       └── index.vue 🔨 (All reports)
│
├── api/hr_admin/
│   ├── employee/ ✅
│   ├── leave/ ✅
│   ├── schedule/ 🔨
│   ├── location/ 🔨
│   ├── holiday/ 🔨
│   ├── deduction/ 🔨
│   ├── attendance/ 🔨
│   ├── overtime/ 🔨
│   ├── payroll/ 🔨
│   └── report/ 🔨
│
└── modules/
    ├── forms/hr_admin/ (8 modules) 🔨
    └── tables/columns/hr_admin/ (8 modules) 🔨
```

## 🔐 Role-Based Page Access

### Route Guards

```typescript
// frontend/src/middleware/hrms-auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  const role = authStore.user?.role;
  
  // HR Admin routes
  if (to.path.startsWith('/hr/config') && role !== 'hr_admin') {
    return navigateTo('/hr');
  }
  
  if (to.path.startsWith('/hr/payroll/process') && 
      !['hr_admin', 'payroll_manager'].includes(role)) {
    return navigateTo('/hr');
  }
  
  // Manager routes
  if (to.path.includes('/team') && 
      !['manager', 'hr_admin'].includes(role)) {
    return navigateTo('/hr');
  }
  
  // Employee routes (all authenticated users)
  // No restriction needed
});
```

### Menu Structure by Role

```typescript
// HR_ADMIN Menu
- Dashboard
- Employees (CRUD)
- Leaves (All, Approve/Reject)
- Attendance (All, Approve locations)
- Overtime (All, Approve/Reject)
- Payroll (Process, Reports)
- Configuration
  - Working Schedules
  - Work Locations
  - Public Holidays
  - Deduction Rules
- Reports & Analytics

// MANAGER Menu
- Dashboard
- My Team
  - Employees
  - Leaves (Approve/Reject)
  - Attendance
  - Overtime (Approve/Reject)
- My Profile
- My Attendance
- My Overtime
- My Payslips

// EMPLOYEE Menu
- Dashboard
- My Profile
- My Attendance (Check-in/out)
- My Leaves
- My Overtime
- My Payslips

// PAYROLL_MANAGER Menu
- Dashboard
- Attendance (View all)
- Payroll Processing
- Payroll Reports
```

## 🚀 Implementation Timeline

### Day 1: Configuration Modules (3-4 hours)
- Working Schedule (CRUD)
- Work Location (CRUD)
- Public Holidays (CRUD)
- Deduction Rules (CRUD)
- Frontend pages for all 4 modules

### Day 2: Attendance System (3-4 hours)
- Domain model
- Check-in/Check-out service
- Location validation
- Late calculation
- Wrong location workflow
- Frontend pages (Employee, Manager, Admin views)

### Day 3: Overtime Management (2-3 hours)
- Domain model
- OT request service
- Approval workflow
- Rate calculation
- Frontend pages (Employee, Manager, Admin views)

### Day 4: Payroll System (3-4 hours)
- Domain model
- Calculation engine
- Payslip generation
- Frontend pages (Employee, Admin views)

### Day 5: Reports & Analytics (2-3 hours)
- Report read models
- Export functionality
- Frontend report pages
- Charts and visualizations

**Total: 13-18 hours**

## 📋 Success Criteria

- [ ] All 66 endpoints functional
- [ ] Role-based access control working
- [ ] All frontend pages responsive
- [ ] GPS location validation working
- [ ] OT calculation accurate (150%/200%)
- [ ] Payroll calculation correct
- [ ] Reports generating correctly
- [ ] Export to CSV/PDF working
- [ ] Soft delete and restore working
- [ ] Pagination and filtering working
- [ ] Error handling comprehensive
- [ ] Notifications integrated

## 🎯 Next Action

**Start with Phase 1: Configuration Modules**

This will create the foundation for all other modules. I'll implement:
1. Complete backend (Services, Repositories, Routes)
2. Complete frontend (API services, Pages, Forms)
3. Role-based access control
4. Full CRUD operations

Ready to begin! 🚀


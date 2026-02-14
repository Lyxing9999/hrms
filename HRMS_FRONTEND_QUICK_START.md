# HRMS Frontend - Quick Start Guide

## 🚀 Getting Started

Your HRMS frontend is now ready! Here's how to use it.

---

## 📍 URLs

### Development
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5001
- **HRMS Dashboard**: http://localhost:3000/hr
- **Leave Management**: http://localhost:3000/hr/leaves
- **Employee Management**: http://localhost:3000/hr/employees

---

## 🎯 Features Available

### ✅ HRMS Dashboard (`/hr`)
Main hub for all HRMS modules with:
- Module cards with icons
- Quick navigation
- System statistics
- "Coming Soon" indicators

### ✅ Employee Management (`/hr/employees`)
Already implemented:
- List all employees
- Create new employee
- Upload employee photo
- Create employee account
- Soft delete employee
- Search and filter

### ✅ Leave Management (`/hr/leaves`)
**NEW - Fully functional:**
- Submit leave requests
- View all leaves (paginated)
- Update pending requests
- Approve/Reject (managers)
- Cancel requests
- Delete requests (admin)
- Search by reason
- Filter by status

---

## 👥 User Roles & Permissions

### Employee
```
Can:
- Submit leave requests
- Update own pending requests
- Cancel own pending requests
- View own leave history

Cannot:
- Approve/reject leaves
- Delete leaves
- View other employees' leaves
```

### Manager
```
Can:
- All employee permissions
- View team leaves
- Approve pending requests
- Reject pending requests
- Add review comments

Cannot:
- Delete leaves (admin only)
```

### HR Admin
```
Can:
- All manager permissions
- Delete leave requests
- Restore deleted requests
- View all employees' leaves
- Manage all employees
```

---

## 🎨 UI Walkthrough

### 1. HRMS Dashboard
```
┌──────────────────────────────────────────────┐
│  HRMS Dashboard                              │
│  Human Resource Management System            │
├──────────────────────────────────────────────┤
│                                              │
│  [👤 Employee]  [📅 Leave]  [⏰ Attendance] │
│   Management     Management    System        │
│                                              │
│  [📄 Overtime]  [💰 Payroll]  [⚙️ Config]   │
│   Management     System        Settings      │
│                                              │
├──────────────────────────────────────────────┤
│  System Overview                             │
│  Total: 0  Active: 0  Pending: 0  $0        │
└──────────────────────────────────────────────┘
```

### 2. Leave Management
```
┌──────────────────────────────────────────────┐
│  Leave Management                            │
│  Manage employee leave requests              │
│                      [Refresh] [Submit Leave]│
├──────────────────────────────────────────────┤
│  [Search...] [Status: All ▼]                │
├──────────────────────────────────────────────┤
│  Type    │ Start   │ End     │ Days │ Status│
│  Annual  │ Mar 01  │ Mar 05  │ 6    │🟡PENDING│
│  Sick    │ Mar 10  │ Mar 11  │ 2    │🟢APPROVED│
│  Unpaid  │ Mar 15  │ Mar 20  │ 6    │🔴REJECTED│
│                                              │
│  Actions: [Edit] [Approve] [Reject] [Cancel]│
└──────────────────────────────────────────────┘
```

---

## 🔄 Workflows

### Submit Leave Request (Employee)
1. Go to `/hr/leaves`
2. Click **"Submit Leave Request"**
3. Fill form:
   - Leave Type: Annual/Sick/Unpaid/Other
   - Start Date
   - End Date
   - Reason (max 500 chars)
4. Click **"Save"**
5. ✅ Leave submitted → Manager notified

### Approve Leave (Manager)
1. Go to `/hr/leaves`
2. Find pending request
3. Click **"Approve"**
4. Add comment (optional)
5. Click **"Save"**
6. ✅ Leave approved → Employee notified

### Update Leave (Employee)
1. Go to `/hr/leaves`
2. Find your pending request
3. Click **"Edit"**
4. Update dates/reason
5. Click **"Save"**
6. ✅ Leave updated

### Cancel Leave (Employee)
1. Go to `/hr/leaves`
2. Find your pending request
3. Click **"Cancel"**
4. Confirm
5. ✅ Leave cancelled

---

## 🎨 Status Colors

| Status | Color | Icon |
|--------|-------|------|
| Pending | 🟡 Yellow | Warning |
| Approved | 🟢 Green | Success |
| Rejected | 🔴 Red | Danger |
| Cancelled | ⚪ Gray | Info |

---

## 🔍 Search & Filter

### Search
- Type in search box
- Searches in "reason" field
- Real-time filtering

### Status Filter
- All (default)
- Pending
- Approved
- Rejected
- Cancelled

### Pagination
- 10, 20, 50, 100 items per page
- Total count displayed
- Jump to page

---

## 🐛 Troubleshooting

### "Cannot connect to backend"
```bash
# Check backend is running
docker ps | grep flask-backend

# Restart backend
docker restart flask-backend-lite-DDD-clean

# Check logs
docker logs flask-backend-lite-DDD-clean --tail 50
```

### "Missing or invalid token"
```bash
# Login again
# Go to http://localhost:3000/auth/login
# Use your credentials
```

### "Leave service not found"
```bash
# Check plugin is loaded
# File: frontend/src/plugins/hr-admin.leave.ts
# Should be auto-loaded by Nuxt

# Restart frontend
cd frontend
pnpm dev
```

### "Cannot submit leave"
```bash
# Check form validation
# All fields are required
# End date must be after start date
# Reason max 500 characters
```

---

## 📱 Responsive Design

### Desktop (>1200px)
- 3 columns for module cards
- Full table with all columns
- Side-by-side forms

### Tablet (768px - 1200px)
- 2 columns for module cards
- Scrollable table
- Stacked forms

### Mobile (<768px)
- 1 column for module cards
- Card-based table view
- Full-width forms

---

## 🎯 Testing Checklist

### Employee Flow
- [ ] Login as employee
- [ ] Navigate to `/hr/leaves`
- [ ] Submit new leave request
- [ ] See "Pending" status
- [ ] Update pending request
- [ ] Cancel pending request

### Manager Flow
- [ ] Login as manager
- [ ] Navigate to `/hr/leaves`
- [ ] See team's leave requests
- [ ] Approve a pending request
- [ ] Reject a pending request
- [ ] Add review comments

### Admin Flow
- [ ] Login as hr_admin
- [ ] Navigate to `/hr/leaves`
- [ ] See all leave requests
- [ ] Delete a leave request
- [ ] Search and filter
- [ ] Export data (TODO)

---

## 🚀 Next Steps

### Immediate
1. Test all workflows
2. Check notifications
3. Verify role-based access
4. Test on mobile devices

### Enhancements
1. Add leave balance display
2. Add calendar view
3. Add export to PDF
4. Add email notifications
5. Add leave history chart

### New Modules
1. Attendance System
2. Overtime Management
3. Payroll System
4. Configuration Pages
5. Reports & Analytics

---

## 📞 Support

### Documentation
- Backend API: `backend/app/contexts/hrms/HRMS_API.md`
- Frontend Guide: `FRONTEND_HRMS_COMPLETION.md`
- Test Endpoints: `backend/HRMS_TEST_ENDPOINTS.http`

### Quick Links
- Dashboard: http://localhost:3000/hr
- Leaves: http://localhost:3000/hr/leaves
- Employees: http://localhost:3000/hr/employees

---

## ✅ Status

**Frontend HRMS**: ✅ Operational  
**Employee Module**: ✅ Complete  
**Leave Module**: ✅ Complete  
**Backend Integration**: ✅ Connected  

Ready to use! 🎉

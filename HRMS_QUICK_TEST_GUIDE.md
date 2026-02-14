# HRMS System - Quick Test Guide

## 🚀 Quick Start

### 1. Start the System

```bash
# Terminal 1 - Backend
cd backend
docker-compose up

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

### 2. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

## ✅ Testing Checklist

### Phase 1: Configuration Setup (5 minutes)

#### Test Working Schedules
1. Navigate to: http://localhost:3000/hr/config/schedules
2. Click "Add Schedule"
3. Fill in:
   - Name: "Standard 9-5"
   - Start Time: 09:00:00
   - End Time: 17:00:00
   - Working Days: Mon-Fri
   - Set as Default: Yes
4. Click Save
5. ✅ Verify schedule appears in list
6. ✅ Test Edit, Delete, Restore

#### Test Work Locations
1. Navigate to: http://localhost:3000/hr/config/locations
2. Click "Add Location"
3. Fill in:
   - Name: "Main Office"
   - Address: "123 Main St, City"
   - Latitude: 11.5564
   - Longitude: 104.9282
   - Radius: 100 meters
   - Active: Yes
4. Click Save
5. ✅ Verify location appears in list

#### Test Public Holidays
1. Navigate to: http://localhost:3000/hr/config/holidays
2. Click "Add Holiday"
3. Fill in:
   - Name: "New Year's Day"
   - Khmer Name: "ថ្ងៃចូលឆ្នាំថ្មី"
   - Date: 2026-01-01
   - Paid: Yes
4. Click Save
5. ✅ Verify holiday appears in list

#### Test Deduction Rules
1. Navigate to: http://localhost:3000/hr/config/deductions
2. Click "Add Rule"
3. Fill in:
   - Type: Late
   - Min Minutes: 0
   - Max Minutes: 30
   - Deduction %: 10
   - Active: Yes
4. Click Save
5. ✅ Verify rule appears in list

### Phase 2: Employee Management (10 minutes)

#### Create Employee
1. Navigate to: http://localhost:3000/hr/employees/employee-profile
2. Click "Add Employee"
3. Fill in:
   - Employee Code: "EMP001"
   - Full Name: "John Doe"
   - Department: "Engineering"
   - Position: "Software Developer"
   - Employment Type: Contract
   - Contract Start: 2026-01-01
   - Contract End: 2026-12-31
   - Salary Type: Monthly
   - Rate: 1000
   - Schedule: Select "Standard 9-5"
   - Status: Active
4. Click Save
5. ✅ Verify employee appears in list

#### Upload Photo
1. Click on employee name
2. Click "Upload Photo"
3. Select an image file
4. ✅ Verify photo appears

#### Create User Account
1. On employee detail page
2. Click "Create Account"
3. Fill in:
   - Email: john.doe@company.com
   - Password: password123
   - Role: employee
4. Click Save
5. ✅ Verify account created message

### Phase 3: Leave Management (10 minutes)

#### Submit Leave Request
1. Navigate to: http://localhost:3000/hr/leaves
2. Click "Submit Leave"
3. Fill in:
   - Employee: Select "John Doe"
   - Leave Type: Annual
   - Start Date: 2026-03-01
   - End Date: 2026-03-03
   - Reason: "Family vacation"
4. Click Submit
5. ✅ Verify leave appears with "Pending" status

#### Approve Leave (as Manager/HR Admin)
1. Navigate to: http://localhost:3000/hr/leave-approvals
2. Find the pending leave
3. Click "Approve"
4. Add comment (optional)
5. Click Confirm
6. ✅ Verify status changed to "Approved"

#### Test Reject and Cancel
1. Submit another leave request
2. Click "Reject" and add comment
3. ✅ Verify status changed to "Rejected"
4. Submit another leave
5. Click "Cancel"
6. ✅ Verify status changed to "Cancelled"

### Phase 4: Attendance System (15 minutes)

#### Test Check-In
1. Navigate to: http://localhost:3000/hr/attendance/check-in
2. ✅ Verify "Not Checked In" status
3. Select work location
4. Add notes (optional)
5. Click "Check In Now"
6. ✅ Allow browser to access location (or continue without)
7. ✅ Verify success message
8. ✅ Verify status changed to "Checked In"
9. ✅ Check if late minutes calculated correctly

#### Test Check-Out
1. On same page
2. Add notes (optional)
3. Click "Check Out Now"
4. ✅ Verify success message
5. ✅ Verify status changed to "Checked Out"
6. ✅ Check if early leave minutes calculated

#### View Attendance History
1. Navigate to: http://localhost:3000/hr/attendance/history
2. ✅ Verify today's attendance appears
3. Test filters:
   - Select date range
   - Filter by status
   - Include deleted checkbox
4. ✅ Verify filtering works

#### View Team Attendance
1. Navigate to: http://localhost:3000/hr/attendance/team
2. ✅ Verify stats cards show correct numbers
3. ✅ Verify attendance list shows team members
4. Change date to today
5. ✅ Verify data updates

### Phase 5: Advanced Features (10 minutes)

#### Test Soft Delete & Restore
1. Go to any module (e.g., employees)
2. Click "Delete" on an item
3. ✅ Verify item marked as deleted
4. Check "Include Deleted"
5. ✅ Verify deleted item appears
6. Click "Restore"
7. ✅ Verify item restored

#### Test Search & Filters
1. Go to employees list
2. Type in search box
3. ✅ Verify results filter
4. Test pagination
5. ✅ Verify page navigation works
6. Change page size
7. ✅ Verify items per page changes

#### Test GPS Location Validation
1. Go to check-in page
2. Open browser console
3. Check in with location
4. ✅ Verify GPS coordinates captured
5. Check backend logs
6. ✅ Verify distance calculation logged

## 🐛 Common Issues & Solutions

### Issue: GPS Location Not Working
**Solution:** 
- Ensure HTTPS or localhost
- Allow location permission in browser
- Check browser console for errors

### Issue: Late Minutes Not Calculating
**Solution:**
- Verify employee has schedule assigned
- Check schedule working days include today
- Verify schedule start time is set correctly

### Issue: Cannot Create Employee Account
**Solution:**
- Verify email is unique
- Check IAM service is running
- Verify user has hr_admin role

### Issue: Leave Request Fails
**Solution:**
- Verify employee has contract
- Check dates are within contract period
- Verify end date >= start date

### Issue: API Errors
**Solution:**
- Check backend is running
- Verify MongoDB is connected
- Check backend logs for errors
- Verify JWT token is valid

## 📊 Expected Results

### After Complete Testing

**Configuration:**
- ✅ 1 Working Schedule
- ✅ 1 Work Location
- ✅ 1 Public Holiday
- ✅ 1 Deduction Rule

**HR Data:**
- ✅ 1 Employee with photo
- ✅ 1 User account linked
- ✅ 3-4 Leave requests (various statuses)
- ✅ 1-2 Attendance records

**System Status:**
- ✅ All modules accessible
- ✅ All CRUD operations working
- ✅ GPS validation working
- ✅ Late/early calculations working
- ✅ Soft delete/restore working
- ✅ Search and filters working

## 🔍 Verification Commands

### Check Backend Health
```bash
curl http://localhost:5001/health
```

### Check Database
```bash
# Connect to MongoDB
docker exec -it <mongo-container> mongosh

# Check collections
use hrms_db
show collections
db.employees.countDocuments()
db.attendances.countDocuments()
db.leave_requests.countDocuments()
```

### Check API Endpoints
```bash
# Get employees (requires auth token)
curl -H "Authorization: Bearer <token>" \
  http://localhost:5001/api/hrms/admin/employees

# Get attendances
curl -H "Authorization: Bearer <token>" \
  http://localhost:5001/api/hrms/admin/attendances
```

## 📝 Test Data Templates

### Employee Test Data
```json
{
  "employee_code": "EMP001",
  "full_name": "John Doe",
  "department": "Engineering",
  "position": "Developer",
  "employment_type": "contract",
  "contract": {
    "start_date": "2026-01-01",
    "end_date": "2026-12-31",
    "salary_type": "monthly",
    "rate": 1000
  },
  "status": "active"
}
```

### Leave Request Test Data
```json
{
  "leave_type": "annual",
  "start_date": "2026-03-01",
  "end_date": "2026-03-03",
  "reason": "Family vacation"
}
```

### Check-In Test Data
```json
{
  "location_id": "<location-id>",
  "latitude": 11.5564,
  "longitude": 104.9282,
  "notes": "On time"
}
```

## ✅ Success Criteria

### All Tests Pass When:
- ✅ All configuration modules working
- ✅ Employee CRUD operations successful
- ✅ Leave workflow complete (submit → approve/reject)
- ✅ Attendance check-in/out working
- ✅ GPS validation functioning
- ✅ Late/early calculations accurate
- ✅ Soft delete/restore working
- ✅ Search and filters responsive
- ✅ No console errors
- ✅ No API errors

## 🎯 Performance Benchmarks

### Expected Response Times:
- List operations: < 500ms
- Create operations: < 300ms
- Update operations: < 300ms
- Delete operations: < 200ms
- GPS validation: < 1000ms

### Expected Load:
- 100+ employees: Smooth
- 1000+ attendance records: Paginated
- 500+ leave requests: Filtered

---

**Testing Time:** ~50 minutes for complete test
**Recommended:** Test in order (Phase 1 → Phase 5)
**Status:** Ready for Testing

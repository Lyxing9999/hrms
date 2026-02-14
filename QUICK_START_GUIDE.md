# Employee Check-In - Quick Start Guide

## 🚀 Start the System

### 1. Backend (Terminal 1)
```bash
cd backend
python run.py
```
✅ Backend running on: `http://localhost:5001`

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
✅ Frontend running on: `http://localhost:3000`

---

## 🧪 Test the Check-In Page

### Access the Page
```
http://localhost:3000/employee/check-in
```

### Test Flow
1. **Allow Location** - Browser will ask for permission
2. **Click "Check In Now"** - Watch progress bar
3. **Verify Status** - Check-in time should appear
4. **Click "Check Out Now"** - Watch progress bar
5. **Verify Complete** - Work duration should show

---

## 🔧 If Something Goes Wrong

### Backend Not Working?
```bash
# Check if backend is running
curl http://localhost:5001/api/hrms/employee/attendance/today
# Should return 401 or data
```

### Frontend Not Connecting?
```bash
# Check .env file
cat frontend/.env
# Should show: NUXT_PUBLIC_SCHOOL_API_BASE=http://localhost:5001
```

### Location Permission Denied?
- Click "Try Again" button
- Or check browser settings
- Or try incognito mode

---

## 📁 Key Files

### Frontend
- Page: `frontend/src/pages/employee/check-in.vue`
- API: `frontend/src/api/hr_admin/attendance/`
- Plugin: `frontend/src/plugins/hr-admin.attendance.ts`
- Config: `frontend/.env`

### Backend
- Routes: `backend/app/contexts/hrms/routes/attendance_route.py`
- Service: `backend/app/contexts/hrms/services/attendance_service.py`
- DTOs: `backend/app/contexts/hrms/data_transfer/`

---

## ✅ System Status

**All Systems**: ✅ GO
**Errors**: ❌ None
**Status**: 🟢 Production Ready

---

## 🎯 What Works

✅ Check-in with GPS location
✅ Check-out with GPS location
✅ Progress bars
✅ Location permission handling
✅ Late/early warnings
✅ Work duration calculation
✅ Notes field
✅ Error handling
✅ Responsive design
✅ Theme support

---

## 📞 Need Help?

Check these files:
1. `EMPLOYEE_CHECK_IN_FINAL_STATUS.md` - Complete status report
2. `ATTENDANCE_API_COMPLETE.md` - API documentation
3. `EMPLOYEE_CHECK_IN_FINAL.md` - Implementation details

**Everything is ready to go! 🎉**

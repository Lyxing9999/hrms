# System Status and Critical Fixes

## 🔴 Critical Issues Found

### 1. MongoDB Not Running
**Error:** `localhost:27017: [Errno 111] ECONNREFUSED`

**Impact:** 
- All database operations fail
- Check-in/check-out cannot work
- Attendance history cannot be retrieved
- Employee data cannot be accessed

**Solution:**
```bash
# Start MongoDB
brew services start mongodb-community

# OR if using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verify MongoDB is running
mongo --eval "db.version()"
# OR
mongosh --eval "db.version()"
```

### 2. HRMS Context Not Initialized (FIXED)
**Error:** `AttributeError: 'Flask' object has no attribute 'hrms'`

**Fix Applied:** Added `load_hrms_context` hook to `backend/app/__init__.py`

```python
# Added these lines:
from app.contexts.hrms.routes import load_hrms_context, remove_hrms_context

app.before_request(load_hrms_context)
app.teardown_request(remove_hrms_context)
```

### 3. Mobile App API Field Mismatch (FIXED)
**Error:** Backend expected `latitude`/`longitude`, mobile sent `lat`/`lng`

**Fix Applied:** Updated `mobile_flutter/lib/services/api_service.dart` to use correct field names

## ✅ Fixes Applied

1. **Backend HRMS Context**: Added before_request hook to initialize `g.hrms`
2. **Mobile App API**: Fixed field names (`lat` → `latitude`, `lng` → `longitude`)
3. **Check-Out Endpoint**: Updated to fetch today's attendance ID first

## 📋 Required Actions

### Immediate (Critical)

1. **Start MongoDB**
   ```bash
   # Check if MongoDB is installed
   which mongod
   
   # If installed, start it
   brew services start mongodb-community
   
   # If not installed
   brew tap mongodb/brew
   brew install mongodb-community
   brew services start mongodb-community
   ```

2. **Restart Backend Server**
   ```bash
   cd backend
   ./venv/bin/python run.py
   ```

3. **Verify Database Connection**
   ```bash
   # Test connection
   mongosh
   > show dbs
   > use school_management
   > show collections
   ```

### Setup (If Fresh Install)

4. **Create Employee Record for User**
   ```bash
   # Connect to MongoDB
   mongosh school_management
   
   # Find your user ID
   db.users.find({email: "your_email@example.com"})
   
   # Create employee record
   db.employees.insertOne({
     user_id: ObjectId("YOUR_USER_ID_HERE"),
     employee_code: "EMP001",
     full_name: "Your Name",
     department: "IT",
     position: "Developer",
     employment_type: "permanent",
     status: "active",
     created_by: ObjectId("YOUR_USER_ID_HERE"),
     lifecycle: {
       created_at: new Date(),
       updated_at: new Date(),
       deleted_at: null,
       deleted_by: null
     }
   })
   ```

## 🧪 Testing Checklist

After starting MongoDB:

- [ ] Backend starts without errors
- [ ] Can login to web/mobile app
- [ ] User has employee_id linked
- [ ] Can access attendance history endpoint
- [ ] Can check-in with location and photo
- [ ] Can check-out
- [ ] Attendance records are saved to database

## 🔍 Verification Commands

### Check MongoDB Status
```bash
# macOS
brew services list | grep mongodb

# Check if port 27017 is listening
lsof -i :27017

# OR
netstat -an | grep 27017
```

### Check Backend Status
```bash
# Check if backend is running
curl http://localhost:5000/api/iam/login

# Check attendance endpoint (with auth token)
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/hrms/employee/attendance/today
```

### Check Database Collections
```bash
mongosh school_management

# List collections
show collections

# Check employees
db.employees.find().pretty()

# Check attendance records
db.attendance.find().pretty()

# Check users
db.users.find({}, {email: 1, roles: 1}).pretty()
```

## 📊 System Architecture

```
Mobile App (Flutter)
    ↓ HTTP/HTTPS
Backend API (Flask) :5000
    ↓ PyMongo
MongoDB :27017
    ↓ Collections
    - users
    - employees
    - attendance
    - leave_requests
```

## 🐛 Common Errors and Solutions

### Error: "ECONNREFUSED localhost:27017"
**Solution:** Start MongoDB service

### Error: "employee_id is required"
**Solution:** Link user account to employee record in database

### Error: "401 Unauthorized"
**Solution:** 
1. Check JWT token is valid
2. Ensure user is logged in
3. Verify token is sent in Authorization header

### Error: "No active check-in found"
**Solution:** User must check-in before checking out

### Error: "Already checked in today"
**Solution:** User can only check-in once per day

### Error: "You are Xm away from work location"
**Solution:** User must be within geofence radius (150m for PPIU)

## 📝 Next Steps

1. ✅ Start MongoDB
2. ✅ Restart backend server
3. ✅ Verify database connection
4. ✅ Create employee records for test users
5. ✅ Test check-in flow from mobile app
6. ✅ Test check-out flow
7. ✅ Verify attendance records in database

## 🎯 Production Deployment Checklist

- [ ] MongoDB running with authentication enabled
- [ ] Backend environment variables configured
- [ ] CORS origins properly set
- [ ] JWT secret key is secure
- [ ] Database backups configured
- [ ] SSL/TLS certificates installed
- [ ] Mobile app points to production URL
- [ ] Geofence coordinates verified for office location
- [ ] Photo upload storage configured
- [ ] Error logging and monitoring setup

## 📞 Support

If issues persist:
1. Check backend logs: `tail -f backend/logs/app.log`
2. Check MongoDB logs: `tail -f /usr/local/var/log/mongodb/mongo.log`
3. Verify all services are running
4. Check firewall settings
5. Verify network connectivity

## 🔄 Quick Restart Commands

```bash
# Stop all services
brew services stop mongodb-community
# Kill backend if running
pkill -f "python run.py"

# Start all services
brew services start mongodb-community
cd backend && ./venv/bin/python run.py &

# Verify
curl http://localhost:5000/api/iam/login
mongosh --eval "db.version()"
```

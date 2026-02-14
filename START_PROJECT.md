# 🚀 Start HRMS Project - Quick Guide

## ✅ All Import Errors Fixed!

The project is now ready to run without errors.

---

## 📋 Prerequisites Check

Before starting, ensure you have:
- ✅ Docker & Docker Compose installed
- ✅ Node.js 18+ installed
- ✅ pnpm or npm installed

---

## 🎯 Step-by-Step Startup

### Step 1: Start Backend

```bash
cd backend
docker-compose up -d
```

**Wait for services to start** (about 30 seconds)

**Expected output**:
```
✔ Container mongo                    Started
✔ Container mongo-express            Started  
✔ Container flask-backend-lite-DDD-clean  Started
```

**Verify backend is running**:
```bash
# Check logs
docker-compose logs -f backend

# Should see:
# * Running on http://0.0.0.0:5001
# * Running on http://127.0.0.1:5001
```

**Test backend health**:
```bash
curl http://localhost:5001/health
# Should return: {"status": "healthy"}
```

---

### Step 2: Start Frontend

Open a **new terminal** window:

```bash
cd frontend
pnpm install
pnpm dev
```

**Expected output**:
```
✔ Nuxt 3.x.x
✔ Local:    http://localhost:3000/
✔ Network:  http://192.168.x.x:3000/
```

---

### Step 3: Access the System

Open your browser and go to:
**http://localhost:3000/hr**

**Login credentials**:
```
Email: admin@school.com
Password: admin123
Role: hr_admin
```

---

## 🧪 Test the System

### Test 1: Employee Management
1. Navigate to: http://localhost:3000/hr/employees/employee-profile
2. Click "Add Employee"
3. Fill in employee details
4. Upload a photo (optional)
5. Click "Save"
6. Verify employee appears in the list

### Test 2: Leave Management
1. Navigate to: http://localhost:3000/hr/leaves
2. Click "Submit Leave Request"
3. Select leave type and dates
4. Enter reason
5. Click "Submit"
6. Verify leave appears with "Pending" status

### Test 3: Configuration APIs
```bash
# Get JWT token first (login via frontend, check browser DevTools > Application > Local Storage)
TOKEN="your-jwt-token-here"

# Test working schedules
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/hrms/admin/working-schedules

# Test work locations
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/hrms/admin/work-locations

# Test public holidays
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/hrms/admin/public-holidays

# Test deduction rules
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/hrms/admin/deduction-rules
```

---

## 🔍 Troubleshooting

### Backend won't start

**Check Docker logs**:
```bash
cd backend
docker-compose logs backend
```

**Common issues**:
1. **Port 5001 already in use**:
   ```bash
   # Find and kill the process
   lsof -ti:5001 | xargs kill -9
   ```

2. **MongoDB connection error**:
   ```bash
   # Restart MongoDB
   docker-compose restart mongo
   ```

3. **Import errors**:
   ```bash
   # Rebuild the container
   docker-compose up --build
   ```

### Frontend won't start

**Clear cache and reinstall**:
```bash
cd frontend
rm -rf node_modules .nuxt
pnpm install
pnpm dev
```

**Common issues**:
1. **Port 3000 already in use**:
   ```bash
   # Kill the process
   lsof -ti:3000 | xargs kill -9
   ```

2. **Module not found errors**:
   ```bash
   # Clear Nuxt cache
   rm -rf .nuxt
   pnpm dev
   ```

### API calls failing

1. **Check backend is running**:
   ```bash
   curl http://localhost:5001/health
   ```

2. **Check CORS settings** in browser console

3. **Verify JWT token** is valid (login again if expired)

---

## 📊 Available Services

Once started, you'll have access to:

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main application |
| Backend API | http://localhost:5001 | REST API |
| MongoDB | localhost:27017 | Database |
| MongoDB Express | http://localhost:8081 | Database admin UI |
| API Docs | http://localhost:5001/api/docs | Swagger UI |

---

## 🎯 What's Working

### ✅ Fully Functional (Backend + Frontend)
1. **Employee Management** - `/hr/employees/employee-profile`
   - Create, view, update, delete employees
   - Photo upload
   - Account creation
   - Soft delete and restore

2. **Leave Management** - `/hr/leaves`
   - Submit leave requests
   - Approve/reject workflow
   - Status tracking
   - Notifications

3. **HRMS Dashboard** - `/hr`
   - Module overview
   - Navigation

### ✅ Backend Ready (API Available)
4. **Working Schedule** - API: `/api/hrms/admin/working-schedules`
5. **Work Location** - API: `/api/hrms/admin/work-locations`
6. **Public Holiday** - API: `/api/hrms/admin/public-holidays`
7. **Deduction Rule** - API: `/api/hrms/admin/deduction-rules`

---

## 🛑 Stop the System

### Stop Backend
```bash
cd backend
docker-compose down
```

### Stop Frontend
Press `Ctrl+C` in the terminal running the frontend

---

## 🔄 Restart the System

### Restart Backend
```bash
cd backend
docker-compose restart
```

### Restart Frontend
```bash
cd frontend
pnpm dev
```

---

## 📝 Quick Commands Reference

```bash
# Backend
cd backend
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose restart        # Restart
docker-compose logs -f        # View logs
docker-compose ps             # Check status

# Frontend
cd frontend
pnpm install                  # Install dependencies
pnpm dev                      # Start dev server
pnpm build                    # Build for production
pnpm preview                  # Preview production build

# Database
docker exec -it mongo mongosh # Access MongoDB shell
```

---

## ✅ Success Checklist

- [ ] Backend started successfully (port 5001)
- [ ] Frontend started successfully (port 3000)
- [ ] Can access http://localhost:3000/hr
- [ ] Can login with admin credentials
- [ ] Employee Management page loads
- [ ] Leave Management page loads
- [ ] Can create a test employee
- [ ] Can submit a test leave request

---

## 🎉 You're All Set!

The HRMS system is now running successfully!

**Next steps**:
1. Explore Employee Management
2. Test Leave Management workflow
3. Try the configuration APIs
4. Review the documentation in `QUICK_START_GUIDE.md`

**Need help?**
- Check `QUICK_START_GUIDE.md` for detailed instructions
- Review `PROJECT_STATUS.md` for current status
- Run `./verify-system.sh` to check system health

---

**Happy coding! 🚀**


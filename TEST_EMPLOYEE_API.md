# Employee API Troubleshooting

## Issue
The API endpoint `http://localhost:5001/api/hrms/admin/employees?page=1&limit=10&include_deleted=false&deleted_only=false` works but the frontend page doesn't show any data.

## Possible Causes

### 1. Empty Database
The API might be returning an empty list because there are no employees in the database yet.

**Solution**: Create test employees using the "Add Employee" button on the frontend.

### 2. Frontend Port Mismatch
The API is running on port 5000, but the frontend might be trying to connect to port 5001.

**Check**: 
- Backend runs on: `http://localhost:5000`
- Frontend API calls should go to: `http://localhost:5000/api/hrms/admin/employees`

**Fix**: Update frontend API base URL if needed in `frontend/nuxt.config.ts` or environment variables.

### 3. CORS Issues
If the frontend and backend are on different ports, CORS might be blocking the requests.

**Check**: Browser console for CORS errors.

### 4. Response Format Mismatch
The backend might be returning data in a different format than the frontend expects.

**Expected Format**:
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 0,
    "page": 1,
    "page_size": 10,
    "total_pages": 0
  }
}
```

## Testing Steps

### 1. Test API Directly
```bash
curl http://localhost:5000/api/hrms/admin/employees?page=1&limit=10
```

### 2. Check Database
```bash
# Connect to MongoDB
mongosh

# Switch to your database
use your_database_name

# Count employees
db.employees.countDocuments()

# List employees
db.employees.find().limit(5)
```

### 3. Create Test Employee
Use the frontend "Add Employee" button or create via API:
```bash
curl -X POST http://localhost:5000/api/hrms/admin/employees \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "employee_code": "EMP001",
    "full_name": "Test Employee",
    "department": "IT",
    "position": "Developer",
    "employment_type": "full_time",
    "status": "active"
  }'
```

### 4. Check Frontend API Configuration
Look for API base URL configuration in:
- `frontend/nuxt.config.ts`
- `frontend/.env`
- `frontend/src/composables/system/useApiUtils.ts`

The base URL should be `http://localhost:5000` not `http://localhost:5001`.

## Quick Fix

If the issue is port mismatch, update the frontend API configuration:

1. Check `frontend/nuxt.config.ts`:
```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:5000'  // Should be 5000, not 5001
    }
  }
})
```

2. Or update environment variable:
```bash
# frontend/.env
NUXT_PUBLIC_API_BASE=http://localhost:5000
```

## Verification

After fixing, verify:
1. ✅ API returns data: `curl http://localhost:5000/api/hrms/admin/employees?page=1&limit=10`
2. ✅ Frontend shows data in the table
3. ✅ No console errors in browser
4. ✅ Network tab shows successful API calls to port 5000

# Live Tracking Page - Debug Guide

## Issue: Page Stuck in Loading State

The page shows a loading spinner and never completes. Here's how to debug:

## Step 1: Check Browser Console

Open browser DevTools (F12) and check the Console tab for errors:

### Expected Console Messages (Success):
```
✅ Map initialized successfully
✅ Socket connected
✅ Joined managers room: { manager_id: "...", room: "managers", ... }
```

### Common Error Messages:

#### 1. Socket Connection Error
```
❌ Socket connection error: Error: ...
```
**Cause:** Backend Socket.IO server not running or wrong URL

**Fix:**
- Verify backend is running: `http://localhost:5001`
- Check if Socket.IO handlers are registered
- Verify CORS settings allow frontend origin

#### 2. Map Loading Error
```
❌ Failed to initialize map: Error: Leaflet loading timeout
```
**Cause:** Cannot load Leaflet.js from CDN

**Fix:**
- Check internet connection
- Try different CDN: `https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js`
- Install Leaflet locally: `npm install leaflet`

#### 3. Auth Store Error
```
Cannot read properties of undefined (reading 'user')
```
**Cause:** Auth store not initialized

**Fix:**
- Verify user is logged in
- Check auth store setup
- Add null check: `authStore?.user?.id`

## Step 2: Check Network Tab

Open DevTools → Network tab:

### Check Socket.IO Connection:
1. Look for `socket.io` requests
2. Status should be `101 Switching Protocols` (WebSocket)
3. If status is `404` or `502`, backend is not running

### Check Leaflet Loading:
1. Look for `leaflet.js` and `leaflet.css`
2. Status should be `200 OK`
3. If failed, check internet connection

## Step 3: Verify Backend

### Check if Socket.IO server is running:
```bash
curl http://localhost:5001/socket.io/
```

Expected response: Socket.IO server info

### Check if handlers are registered:
```python
# In backend/app/__init__.py
from app.contexts.hrms.realtime import handlers  # Should be imported
```

### Test Socket.IO connection manually:
```html
<!-- test-socket.html -->
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
</head>
<body>
    <h1>Socket.IO Test</h1>
    <div id="status">Connecting...</div>
    
    <script>
        const socket = io('http://localhost:5001');
        
        socket.on('connect', () => {
            document.getElementById('status').textContent = 'Connected!';
            console.log('✅ Connected');
            
            socket.emit('manager:join', { manager_id: 'test_manager' });
        });
        
        socket.on('manager:joined', (data) => {
            console.log('✅ Joined:', data);
            document.getElementById('status').textContent = 'Joined managers room!';
        });
        
        socket.on('connect_error', (error) => {
            console.error('❌ Error:', error);
            document.getElementById('status').textContent = 'Connection failed!';
        });
    </script>
</body>
</html>
```

## Step 4: Quick Fixes

### Fix 1: Add Fallback Loading State

If Socket.IO fails, show the page anyway:

```typescript
// In initSocket(), after socket.value.on("connect_error", ...)
socket.value.on("connect_error", (error) => {
  console.error("❌ Socket connection error:", error);
  loading.value = false; // ← Stop loading
  connected.value = false;
  ElMessage.error("Cannot connect to live tracking server");
});
```

### Fix 2: Skip Socket.IO for Testing

Temporarily disable Socket.IO to test map:

```typescript
onMounted(async () => {
  await initMap();
  loading.value = false; // ← Stop loading immediately
  // initSocket(); // ← Comment out temporarily
});
```

### Fix 3: Use Mock Data

Test with fake employee data:

```typescript
onMounted(async () => {
  await initMap();
  
  // Add mock employee
  const mockEmployee: EmployeeLocation = {
    employee_id: "mock_1",
    employee_name: "John Doe",
    employee_code: "EMP001",
    department: "IT",
    position: "Developer",
    lat: 11.5565,
    lng: 104.9283,
    accuracy: 15,
    distance_from_office_m: 50,
    status: "active",
    photo_url: "",
    shift_started_at: new Date().toISOString(),
    last_seen_at: new Date().toISOString()
  };
  
  updateEmployee(mockEmployee);
  loading.value = false;
  
  // initSocket(); // ← Comment out
});
```

## Step 5: Check Backend Logs

Start backend with verbose logging:

```bash
# In backend directory
python run.py
```

Look for:
```
✅ Socket.IO initialized
✅ Realtime handlers registered
✅ Client connected: <socket_id>
✅ Manager joined: manager_id=...
```

If you see errors:
```
❌ ImportError: cannot import name 'handlers'
❌ AttributeError: module has no attribute 'socketio'
```

Then handlers are not properly registered.

## Step 6: Verify File Structure

Ensure all files exist:

```
backend/
├── app/
│   ├── __init__.py (imports handlers)
│   └── contexts/
│       ├── infra/
│       │   └── realtime/
│       │       └── socketio_ext.py
│       └── hrms/
│           └── realtime/
│               ├── __init__.py
│               ├── handlers.py
│               └── attendance_realtime_service.py

frontend/
└── src/
    └── pages/
        └── hr/
            └── attendance/
                └── live-tracking.vue
```

## Step 7: Common Solutions

### Solution 1: Backend Not Running
```bash
cd backend
python run.py
```

### Solution 2: Handlers Not Registered

In `backend/app/__init__.py`, add:
```python
# After registering blueprints
from app.contexts.hrms.realtime import handlers  # noqa: F401
```

### Solution 3: CORS Issue

In `backend/app/contexts/infra/realtime/socketio_ext.py`:
```python
socketio = SocketIO(
    cors_allowed_origins=["http://localhost:3000", "http://localhost:3001"],
    async_mode="eventlet",
    ping_timeout=20,
    ping_interval=25,
)
```

### Solution 4: Port Conflict

Check if port 5001 is in use:
```bash
lsof -i :5001
```

If occupied, kill the process or change port.

## Step 8: Enable Debug Mode

Add debug logging to the page:

```typescript
const initSocket = () => {
  console.log("🔍 Initializing socket...");
  const socketUrl = "http://localhost:5001";
  console.log("🔍 Socket URL:", socketUrl);
  
  socket.value = io(socketUrl, {
    transports: ["websocket", "polling"],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5,
  });
  
  console.log("🔍 Socket instance created");
  
  socket.value.on("connect", () => {
    console.log("✅ Socket connected, ID:", socket.value?.id);
    // ... rest of code
  });
  
  socket.value.on("connect_error", (error) => {
    console.error("❌ Connection error:", error.message);
    console.error("❌ Error details:", error);
  });
  
  socket.value.on("disconnect", (reason) => {
    console.log("⚠️ Disconnected, reason:", reason);
  });
};
```

## Step 9: Test Checklist

- [ ] Backend server is running on port 5001
- [ ] Can access `http://localhost:5001` in browser
- [ ] Socket.IO handlers are imported in `app/__init__.py`
- [ ] Frontend can access `http://localhost:3000`
- [ ] User is logged in with `hr_admin` or `manager` role
- [ ] Browser console shows no errors
- [ ] Network tab shows Socket.IO connection
- [ ] Leaflet.js loads successfully

## Step 10: Emergency Fallback

If nothing works, use this simplified version:

```vue
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";

const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  try {
    // Test backend connection
    const response = await fetch("http://localhost:5001/api/health");
    if (!response.ok) {
      throw new Error("Backend not responding");
    }
    
    loading.value = false;
    ElMessage.success("Backend is running!");
  } catch (err: any) {
    error.value = err.message;
    loading.value = false;
    ElMessage.error("Cannot connect to backend: " + err.message);
  }
});
</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error }}</div>
  <div v-else>Backend is connected! Now add Socket.IO...</div>
</template>
```

## Need More Help?

1. Share browser console output
2. Share backend logs
3. Share network tab screenshot
4. Confirm backend is running: `curl http://localhost:5001`

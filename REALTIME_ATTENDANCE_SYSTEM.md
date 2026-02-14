# Realtime Employee Attendance System with Photo & GPS Tracking

## Overview
Complete implementation of a realtime employee check-in/location tracking system with photo verification for managers. Built with Flask-SocketIO (eventlet), MongoDB, and vanilla JavaScript.

## Architecture

### Backend Components

1. **SocketIO Handlers** (`backend/app/contexts/hrms/realtime/handlers.py`)
   - `employee:join` - Employee joins their personal room
   - `manager:join` - Manager joins shared "managers" room
   - `shift:start` - Employee starts shift with photo and location
   - `location:update` - Periodic location updates (every 5 seconds)
   - `shift:stop` - Employee stops shift with final location

2. **Realtime Service** (`backend/app/contexts/hrms/realtime/attendance_realtime_service.py`)
   - GPS validation (accuracy < 200m)
   - Geofencing (Haversine distance calculation)
   - MongoDB operations for events and live locations
   - Business logic for shift management

3. **Photo Upload Route** (`backend/app/contexts/hrms/routes/photo_upload_route.py`)
   - REST endpoint: `POST /api/uploads/photo`
   - Accepts multipart/form-data
   - Validates file type and size
   - Stores locally and returns photo_url

### Frontend Components

1. **Employee Client** (`frontend/realtime-attendance-client.js`)
   - Photo capture and upload
   - GPS location tracking
   - Socket.IO connection management
   - Shift start/stop workflow

2. **Manager Dashboard** (`frontend/manager-dashboard-client.js`)
   - Realtime map display (Leaflet.js)
   - Employee location markers with photos
   - Live updates via Socket.IO
   - Employee list and filtering

## Room Design Decision

**Chosen: Single "managers" room**

```
Employees: room="employee:<employee_id>"
Managers:  room="managers" (shared)
```

### Why Single "managers" Room?

1. **Simplicity**: Broadcast once to all managers vs. iterating manager IDs
2. **Scalability**: No need to track online managers or manager-employee relationships
3. **Frontend Filtering**: Managers filter by team on client side
4. **Reduced Complexity**: No realtime manager-employee mapping required
5. **Consistency**: Matches notification broadcast patterns

### Alternative (Not Chosen)
```
room="manager:<manager_id>"
```
Would require:
- Tracking which managers are online
- Maintaining manager-employee relationships in realtime
- Multiple emit calls per location update
- More complex room management

## Data Flow

### Shift Start Flow
```
1. Employee captures photo (camera/file input)
2. Employee gets GPS location
3. Upload photo → POST /api/uploads/photo → photo_url
4. Emit "shift:start" with {employee_id, lat, lng, accuracy, photo_url, started_at}
5. Backend validates:
   - Accuracy < 200m
   - Distance from office < 150m (geofence)
   - Employee exists and not already active
6. Store in attendance_events collection
7. Update live_locations collection
8. Broadcast to "managers" room → "employee:location" event
9. Confirm to employee → "shift:started" event
```

### Location Update Flow (Every 5 seconds)
```
1. watchPosition updates current location
2. Emit "location:update" with {employee_id, lat, lng, accuracy, ts}
3. Backend validates accuracy and geofence
4. Update live_locations collection
5. Broadcast to "managers" room → "employee:location" event
```

### Shift Stop Flow
```
1. Employee gets final GPS location
2. Emit "shift:stop" with {employee_id, lat, lng, accuracy, stopped_at}
3. Backend validates location
4. Calculate shift duration
5. Store in attendance_events collection
6. Update live_locations status to "inactive"
7. Broadcast to "managers" room → "employee:location" event
8. Confirm to employee → "shift:stopped" event with duration
9. Stop watchPosition and update timer
```

## MongoDB Collections

### 1. `attendance_events`
Stores all check-in/out events (immutable audit trail).

```javascript
{
  _id: ObjectId,
  employee_id: String,
  type: "shift_start" | "shift_stop",
  lat: Number,
  lng: Number,
  accuracy: Number,
  distance_from_office_m: Number,
  photo_url: String,
  created_at: ISODate,
  metadata: {
    employee_name: String,
    employee_code: String,
    duration_minutes: Number  // only for shift_stop
  }
}
```

### 2. `live_locations`
Stores current/latest state per employee (mutable, frequently updated).

```javascript
{
  _id: ObjectId,
  employee_id: String,  // unique
  lat: Number,
  lng: Number,
  accuracy: Number,
  distance_from_office_m: Number,
  status: "active" | "inactive",
  photo_url: String,
  shift_started_at: ISODate,
  shift_stopped_at: ISODate,
  last_seen_at: ISODate,
  updated_at: ISODate,
  metadata: {
    employee_name: String,
    employee_code: String,
    department: String,
    position: String
  }
}
```

## Validation Rules

### GPS Accuracy
- **Requirement**: accuracy < 200 meters
- **Rejection**: "GPS accuracy too low. Please wait for better signal"

### Geofencing
- **Office Location**: Configurable (default: 11.5564, 104.9282)
- **Radius**: 150 meters
- **Calculation**: Haversine formula
- **Rejection**: "You are Xm from office. Please be within 150m to check in"

### Photo Upload
- **Allowed Types**: jpg, jpeg, png, webp
- **Max Size**: 5MB
- **Validation**: File type and size checked before upload

## API Endpoints

### REST Endpoints

#### POST /api/uploads/photo
Upload employee shift photo.

**Request:**
```
Content-Type: multipart/form-data
Authorization: Bearer <token>

photo: <file>
employee_id: <string> (optional)
```

**Response:**
```json
{
  "success": true,
  "photo_url": "/uploads/attendance_photos/2026-02-13_abc123.jpg",
  "filename": "2026-02-13_abc123.jpg",
  "size_bytes": 245678
}
```

#### GET /uploads/attendance_photos/<filename>
Serve uploaded photos.

### Socket.IO Events

#### Client → Server

**employee:join**
```json
{ "employee_id": "507f1f77bcf86cd799439011" }
```

**manager:join**
```json
{ "manager_id": "507f1f77bcf86cd799439012" }
```

**shift:start**
```json
{
  "employee_id": "507f1f77bcf86cd799439011",
  "lat": 11.5564,
  "lng": 104.9282,
  "accuracy": 15.5,
  "photo_url": "/uploads/attendance_photos/2026-02-13_abc123.jpg",
  "started_at": "2026-02-13T08:00:00Z"
}
```

**location:update**
```json
{
  "employee_id": "507f1f77bcf86cd799439011",
  "lat": 11.5565,
  "lng": 104.9283,
  "accuracy": 12.3,
  "ts": "2026-02-13T08:05:00Z"
}
```

**shift:stop**
```json
{
  "employee_id": "507f1f77bcf86cd799439011",
  "lat": 11.5564,
  "lng": 104.9282,
  "accuracy": 18.2,
  "stopped_at": "2026-02-13T17:00:00Z"
}
```

#### Server → Client

**employee:joined**
```json
{
  "employee_id": "507f1f77bcf86cd799439011",
  "room": "employee:507f1f77bcf86cd799439011",
  "timestamp": "2026-02-13T08:00:00Z"
}
```

**manager:joined**
```json
{
  "manager_id": "507f1f77bcf86cd799439012",
  "room": "managers",
  "active_employees": [...],
  "timestamp": "2026-02-13T08:00:00Z"
}
```

**shift:started** (to employee room)
```json
{
  "employee_id": "507f1f77bcf86cd799439011",
  "started_at": "2026-02-13T08:00:00Z",
  "location": { "lat": 11.5564, "lng": 104.9282, "accuracy": 15.5 }
}
```

**shift:stopped** (to employee room)
```json
{
  "employee_id": "507f1f77bcf86cd799439011",
  "stopped_at": "2026-02-13T17:00:00Z",
  "duration_minutes": 540,
  "location": { "lat": 11.5564, "lng": 104.9282, "accuracy": 18.2 }
}
```

**employee:location** (to managers room)
```json
{
  "employee_id": "507f1f77bcf86cd799439011",
  "lat": 11.5565,
  "lng": 104.9283,
  "accuracy": 12.3,
  "status": "active",
  "photo_url": "/uploads/attendance_photos/2026-02-13_abc123.jpg",
  "last_seen_at": "2026-02-13T08:05:00Z"
}
```

**error**
```json
{
  "message": "GPS accuracy too low (250m). Please wait for better signal (required: <200m)"
}
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install flask-socketio eventlet pymongo
```

### 2. Create MongoDB Indexes
```python
from pymongo import ASCENDING, DESCENDING
from app.contexts.infra.database.mongodb import get_db

db = get_db()

# attendance_events indexes
db.attendance_events.create_index([("employee_id", ASCENDING), ("created_at", DESCENDING)])
db.attendance_events.create_index([("type", ASCENDING), ("created_at", DESCENDING)])

# live_locations indexes
db.live_locations.create_index([("employee_id", ASCENDING)], unique=True)
db.live_locations.create_index([("status", ASCENDING), ("last_seen_at", DESCENDING)])
```

### 3. Configure Geofence
Edit `attendance_realtime_service.py`:
```python
OFFICE_LAT = 11.5564  # Your office latitude
OFFICE_LNG = 104.9282  # Your office longitude
GEOFENCE_RADIUS_M = 150  # Radius in meters
MAX_ACCURACY_M = 200  # Maximum GPS accuracy
```

### 4. Run Server
```bash
python run.py
```

## Frontend Integration

### Employee Page
```html
<!DOCTYPE html>
<html>
<head>
    <title>Employee Check-In</title>
</head>
<body>
    <div id="attendance-app">
        <input type="file" id="photo-input" accept="image/*" capture="user">
        <button id="start-shift-btn">Start Shift</button>
        <button id="stop-shift-btn" disabled>Stop Shift</button>
        <div id="status"></div>
        <div id="location"></div>
    </div>
    
    <script src="/realtime-attendance-client.js"></script>
    <script>
        const client = new RealtimeAttendanceClient({
            socketUrl: 'http://localhost:5001',
            apiUrl: 'http://localhost:5001',
            onShiftStarted: (data) => {
                document.getElementById('status').textContent = 'Shift Active';
            },
            onShiftStopped: (data) => {
                document.getElementById('status').textContent = 
                    `Shift Ended (${data.duration_minutes} minutes)`;
            }
        });
        
        client.connect('YOUR_EMPLOYEE_ID');
        
        document.getElementById('start-shift-btn').onclick = async () => {
            await client.startShift(document.getElementById('photo-input'));
        };
        
        document.getElementById('stop-shift-btn').onclick = async () => {
            await client.stopShift();
        };
    </script>
</body>
</html>
```

### Manager Dashboard
```html
<!DOCTYPE html>
<html>
<head>
    <title>Manager Dashboard</title>
</head>
<body>
    <div id="map" style="height: 600px;"></div>
    <div id="employee-list"></div>
    
    <script src="/manager-dashboard-client.js"></script>
    <script>
        const dashboard = new ManagerDashboardClient({
            socketUrl: 'http://localhost:5001',
            mapElementId: 'map'
        });
        
        dashboard.connect('YOUR_MANAGER_ID');
    </script>
</body>
</html>
```

## Security Considerations

1. **Authentication**: All endpoints require JWT token
2. **Authorization**: Role-based access (employee, manager, hr_admin)
3. **File Upload**: Validate file type, size, and sanitize filenames
4. **GPS Validation**: Prevent fake locations with accuracy and geofence checks
5. **Rate Limiting**: Consider adding rate limits for location updates
6. **Photo Storage**: In production, use S3/CDN instead of local storage

## Performance Optimization

1. **Location Updates**: 5-second interval balances accuracy and server load
2. **MongoDB Indexes**: Critical for query performance
3. **Room Broadcasting**: Single "managers" room reduces emit overhead
4. **Photo Compression**: Consider client-side compression before upload
5. **CDN**: Serve photos from CDN in production

## Monitoring & Debugging

### Check Active Connections
```python
from app.contexts.infra.realtime.socketio_ext import socketio

# Get connected clients
print(socketio.server.manager.rooms)
```

### Monitor Location Updates
```python
# Query recent updates
db.live_locations.find({"status": "active"}).sort("last_seen_at", -1)
```

### Check Stale Locations
```python
from datetime import datetime, timedelta

stale_threshold = datetime.utcnow() - timedelta(minutes=5)
stale = db.live_locations.find({
    "status": "active",
    "last_seen_at": {"$lt": stale_threshold}
})
```

## Troubleshooting

### Location Permission Denied
- Check browser settings
- Ensure HTTPS in production (required for geolocation)
- Provide clear user instructions

### High GPS Accuracy (>200m)
- Wait for better signal
- Move to open area
- Check device GPS settings

### Photo Upload Fails
- Check file size (<5MB)
- Verify file type (jpg, png, webp)
- Ensure upload directory exists and is writable

### Socket Connection Issues
- Verify eventlet is installed
- Check CORS settings
- Ensure Socket.IO versions match (client/server)

## Future Enhancements

1. **Offline Support**: Queue location updates when offline
2. **Battery Optimization**: Adaptive update intervals based on movement
3. **Route Tracking**: Store location history for route visualization
4. **Geofence Alerts**: Notify managers when employees leave geofence
5. **Analytics**: Dashboard with attendance statistics and heatmaps
6. **Multi-Office**: Support multiple office locations
7. **Photo Verification**: Face recognition for enhanced security

## License
Proprietary - Internal Use Only

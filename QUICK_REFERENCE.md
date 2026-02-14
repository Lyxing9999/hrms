# Live Tracking - Quick Reference Card

## 🚀 Quick Start

```bash
# 1. Start Backend
cd backend && python run.py

# 2. Start Frontend  
cd frontend && npm run dev

# 3. Run Tests
python test_live_tracking.py

# 4. Access Page
http://localhost:3000/hr/attendance/live-tracking
```

## 📍 Key URLs

| Service | URL |
|---------|-----|
| Backend | http://localhost:5001 |
| Frontend | http://localhost:3000 |
| Live Tracking | http://localhost:3000/hr/attendance/live-tracking |
| Socket.IO | http://localhost:5001/socket.io/ |

## 🎯 Color Indicators

### GPS Accuracy
- 🟢 Green (< 50m) = Excellent
- 🟠 Orange (50-100m) = Good  
- 🔴 Red (> 100m) = Poor

### Distance from Office
- 🟢 Green (< 50m) = Very close
- 🟠 Orange (50-100m) = Close
- 🔴 Red (> 100m) = Far

## 🔧 Configuration

```typescript
// Office Location
OFFICE_LAT = 11.5564
OFFICE_LNG = 104.9282
GEOFENCE_RADIUS = 150m

// Validation
MAX_ACCURACY = 200m
UPDATE_INTERVAL = 5 seconds
```

## 📡 Socket.IO Events

### Client → Server
- `employee:join` - Join employee room
- `manager:join` - Join managers room
- `shift:start` - Start shift with location
- `location:update` - Update location
- `shift:stop` - Stop shift

### Server → Client
- `employee:joined` - Confirmation
- `manager:joined` - Confirmation + active employees
- `shift:started` - Shift confirmed
- `shift:stopped` - Shift ended
- `employee:location` - Location update (to managers)
- `error` - Error message

## 🗂️ MongoDB Collections

```javascript
// attendance_events - Immutable log
{
  employee_id, type, lat, lng, accuracy,
  distance_from_office_m, photo_url, created_at
}

// live_locations - Current state
{
  employee_id, lat, lng, accuracy, status,
  photo_url, shift_started_at, last_seen_at
}
```

## 🎨 UI Components

```
Header
├── Title + Active Count
└── User Tag + Refresh Button

Content
├── Map Card (16/24 cols)
│   ├── Office Marker (🏢)
│   ├── Geofence Circle
│   └── Employee Markers
└── Employee List (8/24 cols)
    ├── Search Box
    ├── Status Filter
    ├── Department Filter
    └── Employee Cards
```

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Page loading | Check backend running, see DEBUG.md |
| No employees | Verify active shifts in MongoDB |
| Photos missing | Check employees.photo_url field |
| Map not loading | Check internet (Leaflet CDN) |
| Socket error | Verify handlers registered |

## 📊 Performance Targets

- Page Load: < 2s
- Socket Connect: < 1s
- Update Latency: < 500ms
- Memory: < 100MB
- CPU: < 10%

## ✅ Test Checklist

- [ ] Backend running
- [ ] Frontend running
- [ ] Socket.IO connected
- [ ] Employee appears on map
- [ ] Location updates work
- [ ] Photos display
- [ ] Filters work
- [ ] Responsive design
- [ ] No console errors

## 📞 Support Files

- `LIVE_TRACKING_COMPLETE.md` - Full documentation
- `MANUAL_TEST_GUIDE.md` - Testing steps
- `LIVE_TRACKING_DEBUG.md` - Debug help
- `test_live_tracking.py` - Automated tests

## 🎯 Success Criteria

✅ Real-time updates (< 5s delay)
✅ Photos from database
✅ Color-coded indicators
✅ Responsive layout
✅ No layout breaking
✅ All tests passing

---

**Status:** ✅ COMPLETE & TESTED
**Version:** 1.0.0
**Last Updated:** 2026-02-13

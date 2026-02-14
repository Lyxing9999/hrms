# Live Tracking - Manual Test Guide

## Prerequisites

1. **Backend Running**
   ```bash
   cd backend
   python run.py
   ```
   Should see: `Running on http://localhost:5001`

2. **Frontend Running**
   ```bash
   cd frontend
   npm run dev
   ```
   Should see: `http://localhost:3000`

3. **User Accounts**
   - Manager/HR account with role: `hr_admin` or `manager`
   - Employee account with role: `employee`

## Automated Test

Run the comprehensive test script:

```bash
# Install dependencies
pip install python-socketio requests

# Run tests
python test_live_tracking.py
```

Expected output:
```
✓ Backend server is running
✓ Socket.IO server is available
✓ Employee socket connected
✓ Manager socket connected
✓ Shift started
✓ Location updates received
✓ Shift stopped
✓ Geofencing validation working
✓ Photo upload endpoint exists
✓ Frontend page is accessible

ALL TESTS PASSED!
```

## Manual Testing Steps

### Test 1: Manager Dashboard Access

1. Login as manager/HR admin
2. Navigate to: `http://localhost:3000/hr/attendance/live-tracking`
3. **Expected:**
   - Page loads without errors
   - Map displays with office marker
   - Green geofence circle visible
   - User tag shows your username in header
   - "Live" badge shows connection status

### Test 2: Employee Shift Start

1. Open new browser tab/window
2. Login as employee
3. Navigate to: `http://localhost:3000/employee/check-in`
4. Click "Start Shift"
5. Allow location permission
6. Take/upload photo
7. Click confirm

**Expected:**
- Success message
- Shift status shows "Active"

### Test 3: Manager Sees Employee

1. Switch to manager dashboard tab
2. **Expected:**
   - Employee appears in list (right panel)
   - Employee marker appears on map
   - Marker shows employee initial
   - Green pulse animation on marker
   - Click marker shows popup with:
     - Employee photo
     - Name, code, department
     - Shift start time
     - Duration (updating)
     - GPS accuracy (with color indicator)
     - Distance from office (with color indicator)
     - Status: "CURRENTLY ACTIVE"

### Test 4: Location Updates

1. Keep manager dashboard open
2. Wait 5-10 seconds
3. **Expected:**
   - "Last Seen" time updates
   - Duration increases
   - Marker position may update slightly
   - No page refresh needed

### Test 5: Search and Filters

1. In employee list, type employee name in search
2. **Expected:**
   - List filters to matching employees
   - Map still shows all employees

3. Select "Active" in status filter
4. **Expected:**
   - Only active employees shown

5. Select department in department filter
6. **Expected:**
   - Only employees from that department shown

### Test 6: Employee Details

1. Click employee card in list
2. **Expected:**
   - Map zooms to employee location
   - Popup opens automatically
   - Employee details displayed

### Test 7: Location Accuracy Indicators

Check the popup and list for color indicators:

**GPS Accuracy:**
- Green (●) = < 50m (Excellent)
- Orange (●) = 50-100m (Good)
- Red (●) = > 100m (Poor)

**Distance from Office:**
- Green = < 50m (Very close)
- Orange = 50-100m (Close)
- Red = > 100m (Far)

### Test 8: Employee Shift Stop

1. Switch to employee tab
2. Click "Stop Shift"
3. **Expected:**
   - Success message
   - Duration displayed

4. Switch to manager dashboard
5. **Expected:**
   - Employee marker becomes gray
   - Status changes to "INACTIVE"
   - Popup shows "Shift Ended"
   - After 30 seconds, employee removed from list

### Test 9: Multiple Employees

1. Start shifts for 2-3 employees
2. **Expected:**
   - All appear on map
   - All in employee list
   - Each has unique marker
   - Can click each to view details

### Test 10: Responsive Design

1. Resize browser window
2. **Expected:**
   - Layout adapts to screen size
   - Mobile: Map and list stack vertically
   - Desktop: Side-by-side layout
   - No horizontal scrollbar
   - All elements visible

### Test 11: Connection Loss

1. Stop backend server
2. **Expected:**
   - Warning alert appears: "Disconnected from live tracking server"
   - "Attempting to reconnect..." message
   - Refresh button shows loading state

3. Restart backend
4. **Expected:**
   - Auto-reconnects
   - Alert disappears
   - Data refreshes

### Test 12: Photo Display

1. Ensure employee has photo in database
2. Start shift
3. Check manager dashboard
4. **Expected:**
   - Employee photo shows in list (avatar)
   - Photo shows in map popup
   - If no photo: Shows initial letter

### Test 13: Real-time Updates

1. Have 2 browser windows open:
   - Window A: Manager dashboard
   - Window B: Employee check-in

2. In Window B, start shift
3. In Window A, watch for updates
4. **Expected:**
   - Employee appears immediately (< 2 seconds)
   - No page refresh needed
   - Smooth animation

### Test 14: Geofencing

1. Modify office location in code temporarily:
   ```typescript
   const OFFICE_LAT = 0.0;  // Far away
   const OFFICE_LNG = 0.0;
   ```

2. Try to start shift
3. **Expected:**
   - Error: "You are Xm from office. Please be within 150m"
   - Shift not started

4. Restore correct coordinates

### Test 15: Performance

1. Open browser DevTools (F12)
2. Go to Performance tab
3. Record for 30 seconds
4. **Expected:**
   - No memory leaks
   - Smooth 60fps
   - No layout thrashing
   - Network requests every 5 seconds (location updates)

## Common Issues & Solutions

### Issue: Page stuck loading

**Solution:**
1. Check browser console for errors
2. Verify backend is running
3. Check Socket.IO connection
4. See `LIVE_TRACKING_DEBUG.md`

### Issue: No employees showing

**Solution:**
1. Verify employees have active shifts
2. Check MongoDB `live_locations` collection
3. Verify Socket.IO handlers registered
4. Check backend logs

### Issue: Photos not showing

**Solution:**
1. Verify `photo_url` exists in employees collection
2. Check photo file exists at path
3. Verify photo URL is accessible
4. Check browser console for 404 errors

### Issue: Map not loading

**Solution:**
1. Check internet connection (Leaflet CDN)
2. Check browser console for errors
3. Verify `mapContainer` ref is attached
4. Try refreshing page

### Issue: Location not updating

**Solution:**
1. Verify employee shift is active
2. Check browser console for Socket.IO events
3. Verify backend is receiving updates
4. Check MongoDB `live_locations` collection

## Success Criteria

✅ All automated tests pass
✅ Manager can see active employees
✅ Real-time updates work (< 5 second delay)
✅ Photos display correctly
✅ Geofencing validates locations
✅ Search and filters work
✅ Map interactions smooth
✅ No console errors
✅ Responsive on mobile
✅ Connection recovery works

## Performance Benchmarks

- **Page Load:** < 2 seconds
- **Socket Connection:** < 1 second
- **Location Update Latency:** < 500ms
- **Map Render:** < 1 second
- **Search Filter:** < 100ms
- **Memory Usage:** < 100MB
- **CPU Usage:** < 10% idle

## Browser Compatibility

Tested on:
- ✅ Chrome 120+
- ✅ Firefox 120+
- ✅ Safari 17+
- ✅ Edge 120+
- ✅ Mobile Safari (iOS 16+)
- ✅ Chrome Mobile (Android 12+)

## Next Steps

After successful testing:

1. **Production Deployment**
   - Update Socket.IO URL to production
   - Configure office coordinates
   - Set up CDN for photos
   - Enable SSL/TLS

2. **Monitoring**
   - Set up error tracking
   - Monitor Socket.IO connections
   - Track location update frequency
   - Monitor database performance

3. **Optimization**
   - Enable photo compression
   - Implement marker clustering (100+ employees)
   - Add virtual scrolling for large lists
   - Cache employee data

4. **Enhancements**
   - Add route history
   - Implement heatmaps
   - Add geofence alerts
   - Export location reports

## Support

If tests fail:
1. Check `LIVE_TRACKING_DEBUG.md`
2. Review browser console
3. Check backend logs
4. Verify MongoDB collections
5. Test Socket.IO separately

Happy Testing! 🚀

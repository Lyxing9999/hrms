# Attendance System Issues and Fixes

## Issues Found

### 1. API Field Name Mismatch
**Problem:** Mobile app sends `lat`/`lng`, but backend expects `latitude`/`longitude`

**Mobile App (Flutter):**
```dart
body: jsonEncode({
  'lat': lat,
  'lng': lng,
  'accuracy': accuracy,
  'photo_url': photoUrl,
  'check_in_time': DateTime.now().toIso8601String(),
}),
```

**Backend Expects:**
```python
class AttendanceCheckInSchema(BaseModel):
    latitude: float | None
    longitude: float | None
    notes: str | None
```

### 2. Missing Photo URL Support
**Problem:** Backend attendance system doesn't have fields for:
- `photo_url` (check-in photo)
- `check_out_photo_url` (check-out photo)
- `accuracy` (GPS accuracy)

### 3. Check-Out Endpoint Mismatch
**Problem:** Mobile app calls `/check-out` but backend expects `/attendance/<id>/check-out`

**Mobile App:**
```dart
POST /api/hrms/employee/attendance/check-out
```

**Backend:**
```python
POST /api/hrms/employee/attendance/<attendance_id>/check-out
```

### 4. Missing Employee Linking
**Problem:** Users may not have `employee_id` linked to their account

## Solutions

### Solution 1: Update Mobile App API Service (Quick Fix)

Update `mobile_flutter/lib/services/api_service.dart`:

```dart
// Check In
Future<Map<String, dynamic>> checkIn({
  required double lat,
  required double lng,
  required double accuracy,
  required String photoUrl,
}) async {
  try {
    final response = await http
        .post(
          Uri.parse(AppConfig.checkInEndpoint),
          headers: await _getHeaders(),
          body: jsonEncode({
            'latitude': lat,  // Changed from 'lat'
            'longitude': lng,  // Changed from 'lng'
            'notes': 'Photo: $photoUrl, Accuracy: ${accuracy}m',  // Store in notes
          }),
        )
        .timeout(AppConfig.requestTimeout);

    final data = jsonDecode(response.body);

    if (response.statusCode == 200 || response.statusCode == 201) {
      return {'success': true, 'data': data};
    } else {
      return {
        'success': false,
        'error': data['message'] ?? 'Check-in failed'
      };
    }
  } catch (e) {
    return {'success': false, 'error': 'Network error: ${e.toString()}'};
  }
}

// Check Out - Need to get attendance_id first
Future<Map<String, dynamic>> checkOut({
  required double lat,
  required double lng,
  required double accuracy,
  String? photoUrl,
}) async {
  try {
    // First, get today's attendance to get the ID
    final todayResponse = await http
        .get(
          Uri.parse('${AppConfig.apiBaseUrl}/hrms/employee/attendance/today'),
          headers: await _getHeaders(),
        )
        .timeout(AppConfig.requestTimeout);

    if (todayResponse.statusCode != 200) {
      return {'success': false, 'error': 'No active check-in found'};
    }

    final todayData = jsonDecode(todayResponse.body);
    final attendanceId = todayData['data']['id'];

    // Now check out
    final response = await http
        .post(
          Uri.parse('${AppConfig.apiBaseUrl}/hrms/employee/attendance/$attendanceId/check-out'),
          headers: await _getHeaders(),
          body: jsonEncode({
            'latitude': lat,  // Changed from 'lat'
            'longitude': lng,  // Changed from 'lng'
            'notes': photoUrl != null ? 'Photo: $photoUrl, Accuracy: ${accuracy}m' : 'Accuracy: ${accuracy}m',
          }),
        )
        .timeout(AppConfig.requestTimeout);

    final data = jsonDecode(response.body);

    if (response.statusCode == 200) {
      return {'success': true, 'data': data};
    } else {
      return {
        'success': false,
        'error': data['message'] ?? 'Check-out failed'
      };
    }
  } catch (e) {
    return {'success': false, 'error': 'Network error: ${e.toString()}'};
  }
}
```

### Solution 2: Update Backend to Support Photos (Better Solution)

#### Step 1: Update Attendance Domain Model

`backend/app/contexts/hrms/domain/attendance.py`:
```python
class Attendance:
    def __init__(
        self,
        *,
        employee_id: ObjectId,
        check_in_time: datetime,
        check_in_photo_url: str | None = None,  # ADD THIS
        check_in_latitude: float | None = None,
        check_in_longitude: float | None = None,
        check_in_accuracy: float | None = None,  # ADD THIS
        check_out_time: datetime | None = None,
        check_out_photo_url: str | None = None,  # ADD THIS
        check_out_latitude: float | None = None,
        check_out_longitude: float | None = None,
        check_out_accuracy: float | None = None,  # ADD THIS
        # ... rest of fields
    ):
        self.check_in_photo_url = check_in_photo_url
        self.check_in_accuracy = check_in_accuracy
        self.check_out_photo_url = check_out_photo_url
        self.check_out_accuracy = check_out_accuracy
        # ... rest of initialization
```

#### Step 2: Update Request Schema

`backend/app/contexts/hrms/data_transfer/request/attendance_request.py`:
```python
class AttendanceCheckInSchema(BaseModel):
    employee_id: str | None = None
    location_id: str | None = None
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    accuracy: float | None = Field(None, ge=0)  # ADD THIS
    photo_url: str | None = None  # ADD THIS
    notes: str | None = Field(None, max_length=500)


class AttendanceCheckOutSchema(BaseModel):
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    accuracy: float | None = Field(None, ge=0)  # ADD THIS
    photo_url: str | None = None  # ADD THIS
    notes: str | None = Field(None, max_length=500)
```

#### Step 3: Update Service

`backend/app/contexts/hrms/services/attendance_service.py`:
```python
def check_in(
    self,
    *,
    employee_id: ObjectId,
    location_id: ObjectId | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    accuracy: float | None = None,  # ADD THIS
    photo_url: str | None = None,  # ADD THIS
    notes: str | None = None,
    actor_id: ObjectId,
) -> Attendance:
    # ... existing validation code ...

    attendance = Attendance(
        employee_id=employee_id,
        check_in_time=check_in_time,
        check_in_photo_url=photo_url,  # ADD THIS
        check_in_latitude=latitude,
        check_in_longitude=longitude,
        check_in_accuracy=accuracy,  # ADD THIS
        location_id=location_id,
        notes=notes,
        late_minutes=late_minutes,
        status=AttendanceStatus.LATE if late_minutes > 0 else AttendanceStatus.CHECKED_IN,
    )

    return self.repo.save(attendance)
```

#### Step 4: Update Route

`backend/app/contexts/hrms/routes/attendance_route.py`:
```python
@attendance_bp.route("/employee/attendance/check-in", methods=["POST"])
@require_auth
@require_role("employee", "manager", "hr_admin")
@success_response
def check_in():
    """Employee check-in"""
    data = AttendanceCheckInSchema(**request.get_json())
    db = get_db()
    service = AttendanceService(db)
    mapper = AttendanceMapper()

    current_user_id = ObjectId(g.user["id"])
    
    if data.employee_id:
        employee_id = ObjectId(data.employee_id)
    else:
        employee_id = get_current_employee_id()

    attendance = service.check_in(
        employee_id=employee_id,
        location_id=ObjectId(data.location_id) if data.location_id else None,
        latitude=data.latitude,
        longitude=data.longitude,
        accuracy=data.accuracy,  # ADD THIS
        photo_url=data.photo_url,  # ADD THIS
        notes=data.notes,
        actor_id=current_user_id,
    )

    return AttendanceDTO(**mapper.to_dto(attendance))
```

### Solution 3: Add Simple Check-Out Endpoint

Add this to `backend/app/contexts/hrms/routes/attendance_route.py`:

```python
@attendance_bp.route("/employee/attendance/check-out", methods=["POST"])
@require_auth
@require_role("employee", "manager", "hr_admin")
@success_response
def simple_check_out():
    """Employee check-out (finds today's attendance automatically)"""
    data = AttendanceCheckOutSchema(**request.get_json())
    db = get_db()
    service = AttendanceService(db)
    mapper = AttendanceMapper()

    current_user_id = ObjectId(g.user["id"])
    employee_id = get_current_employee_id()
    
    # Find today's attendance
    today = date.today()
    attendance = service.repo.find_by_employee_and_date(employee_id, today)
    
    if not attendance:
        return {"error": "No active check-in found for today"}, 404
    
    if attendance.check_out_time:
        return {"error": "Already checked out"}, 400

    attendance = service.check_out(
        attendance_id=attendance.id,
        latitude=data.latitude,
        longitude=data.longitude,
        accuracy=data.accuracy,  # ADD THIS
        photo_url=data.photo_url,  # ADD THIS
        notes=data.notes,
        actor_id=current_user_id,
    )

    return AttendanceDTO(**mapper.to_dto(attendance))
```

## Recommended Implementation Order

1. **Quick Fix (5 minutes):** Update mobile app to use `latitude`/`longitude` and store photo in `notes`
2. **Backend Enhancement (30 minutes):** Add photo_url and accuracy fields to backend
3. **Add Simple Check-Out (10 minutes):** Add endpoint that auto-finds today's attendance
4. **Test End-to-End (15 minutes):** Test full flow from mobile app

## Testing Checklist

- [ ] User can login from mobile app
- [ ] User has employee_id linked to account
- [ ] Check-in with photo succeeds
- [ ] Location validation works (within geofence)
- [ ] Check-out succeeds
- [ ] Attendance history displays correctly
- [ ] Photos are stored and retrievable

## Common Errors and Solutions

### Error: "employee_id is required"
**Solution:** Ensure user account is linked to an employee record

### Error: "No active check-in found"
**Solution:** User must check-in before checking out

### Error: "Already checked in today"
**Solution:** User can only check-in once per day

### Error: "You are Xm away from work location"
**Solution:** User must be within geofence radius (150m for PPIU)

### Error: "Network error"
**Solution:** Check backend is running and mobile app has correct base URL

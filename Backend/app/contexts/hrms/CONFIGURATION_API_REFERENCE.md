# HRMS Configuration Modules - API Reference

## Base URL
All endpoints are prefixed with: `/api/hrms/admin`

## Authentication
All endpoints require JWT authentication with `hr_admin` role (unless specified otherwise).

---

## 1. Working Schedule API

### List Working Schedules
```http
GET /api/hrms/admin/working-schedules
```

**Query Parameters:**
- `page` (int, default: 1) - Page number
- `limit` (int, default: 10, max: 100) - Items per page
- `q` (string) - Search by name
- `include_deleted` (boolean) - Include soft-deleted items
- `deleted_only` (boolean) - Show only deleted items

**Response:**
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Standard 9-5",
      "start_time": "09:00:00",
      "end_time": "17:00:00",
      "working_days": [0, 1, 2, 3, 4],
      "weekend_days": [5, 6],
      "total_hours_per_day": 8.0,
      "is_default": true,
      "created_by": "507f1f77bcf86cd799439012",
      "lifecycle": {
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "deleted_at": null,
        "deleted_by": null
      }
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Get Default Schedule
```http
GET /api/hrms/admin/working-schedules/default
```
**Roles:** `hr_admin`, `manager`, `employee`

### Get Single Schedule
```http
GET /api/hrms/admin/working-schedules/{schedule_id}
```

### Create Schedule
```http
POST /api/hrms/admin/working-schedules
```

**Request Body:**
```json
{
  "name": "Standard 9-5",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "working_days": [0, 1, 2, 3, 4],
  "is_default": false
}
```

### Update Schedule
```http
PATCH /api/hrms/admin/working-schedules/{schedule_id}
```

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Schedule",
  "start_time": "08:00:00",
  "end_time": "16:00:00",
  "working_days": [0, 1, 2, 3, 4],
  "is_default": true
}
```

### Soft Delete Schedule
```http
DELETE /api/hrms/admin/working-schedules/{schedule_id}/soft-delete
```

### Restore Schedule
```http
POST /api/hrms/admin/working-schedules/{schedule_id}/restore
```

---

## 2. Work Location API

### List Work Locations
```http
GET /api/hrms/admin/work-locations
```

**Query Parameters:**
- `page` (int, default: 1)
- `limit` (int, default: 10, max: 100)
- `q` (string) - Search by name or address
- `is_active` (boolean) - Filter by active status
- `include_deleted` (boolean)
- `deleted_only` (boolean)

**Response:**
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Main Office",
      "address": "123 Street, Phnom Penh",
      "latitude": 11.5564,
      "longitude": 104.9282,
      "radius_meters": 100,
      "is_active": true,
      "created_by": "507f1f77bcf86cd799439012",
      "lifecycle": { ... }
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Get Active Locations
```http
GET /api/hrms/admin/work-locations/active
```
**Roles:** `hr_admin`, `manager`, `employee`

**Response:**
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Main Office",
      "latitude": 11.5564,
      "longitude": 104.9282,
      "radius_meters": 100,
      ...
    }
  ]
}
```

### Get Single Location
```http
GET /api/hrms/admin/work-locations/{location_id}
```

### Create Location
```http
POST /api/hrms/admin/work-locations
```

**Request Body:**
```json
{
  "name": "Main Office",
  "address": "123 Street, Phnom Penh",
  "latitude": 11.5564,
  "longitude": 104.9282,
  "radius_meters": 100,
  "is_active": true
}
```

**Validation:**
- `latitude`: -90 to 90
- `longitude`: -180 to 180
- `radius_meters`: 10 to 1000

### Update Location
```http
PATCH /api/hrms/admin/work-locations/{location_id}
```

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Office",
  "address": "456 New Street",
  "latitude": 11.5565,
  "longitude": 104.9283,
  "radius_meters": 150,
  "is_active": false
}
```

### Soft Delete Location
```http
DELETE /api/hrms/admin/work-locations/{location_id}/soft-delete
```

### Restore Location
```http
POST /api/hrms/admin/work-locations/{location_id}/restore
```

---

## 3. Public Holiday API

### List Public Holidays
```http
GET /api/hrms/admin/public-holidays
```

**Query Parameters:**
- `page` (int, default: 1)
- `limit` (int, default: 10, max: 100)
- `q` (string) - Search by name (English or Khmer) or description
- `year` (int) - Filter by year
- `include_deleted` (boolean)
- `deleted_only` (boolean)

**Response:**
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Khmer New Year",
      "name_kh": "បុណ្យចូលឆ្នាំខ្មែរ",
      "date": "2024-04-14",
      "is_paid": true,
      "description": "Traditional Cambodian New Year",
      "created_by": "507f1f77bcf86cd799439012",
      "lifecycle": { ... }
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Get Holidays by Year
```http
GET /api/hrms/admin/public-holidays/year/{year}
```
**Roles:** `hr_admin`, `manager`, `employee`

**Response:**
```json
{
  "items": [ ... ],
  "year": 2024
}
```

### Get Single Holiday
```http
GET /api/hrms/admin/public-holidays/{holiday_id}
```

### Create Holiday
```http
POST /api/hrms/admin/public-holidays
```

**Request Body:**
```json
{
  "name": "Khmer New Year",
  "name_kh": "បុណ្យចូលឆ្នាំខ្មែរ",
  "date": "2024-04-14",
  "is_paid": true,
  "description": "Traditional Cambodian New Year"
}
```

**Validation:**
- Prevents duplicate holidays on the same date

### Update Holiday
```http
PATCH /api/hrms/admin/public-holidays/{holiday_id}
```

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Holiday Name",
  "name_kh": "ឈ្មោះថ្មី",
  "date": "2024-04-15",
  "is_paid": false,
  "description": "Updated description"
}
```

### Soft Delete Holiday
```http
DELETE /api/hrms/admin/public-holidays/{holiday_id}/soft-delete
```

### Restore Holiday
```http
POST /api/hrms/admin/public-holidays/{holiday_id}/restore
```

---

## 4. Deduction Rule API

### List Deduction Rules
```http
GET /api/hrms/admin/deduction-rules
```

**Query Parameters:**
- `page` (int, default: 1)
- `limit` (int, default: 10, max: 100)
- `type` (string) - Filter by type: `late`, `absent`, `early_leave`
- `is_active` (boolean) - Filter by active status
- `include_deleted` (boolean)
- `deleted_only` (boolean)

**Response:**
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "type": "late",
      "min_minutes": 1,
      "max_minutes": 30,
      "deduction_percentage": 5.0,
      "is_active": true,
      "created_by": "507f1f77bcf86cd799439012",
      "lifecycle": { ... }
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Get Active Rules
```http
GET /api/hrms/admin/deduction-rules/active
```
**Roles:** `hr_admin`, `manager`

**Response:**
```json
{
  "items": [ ... ]
}
```

### Get Rules by Type
```http
GET /api/hrms/admin/deduction-rules/type/{rule_type}
```
**Roles:** `hr_admin`, `manager`

**Path Parameters:**
- `rule_type`: `late`, `absent`, or `early_leave`

**Response:**
```json
{
  "items": [ ... ],
  "type": "late"
}
```

### Get Single Rule
```http
GET /api/hrms/admin/deduction-rules/{rule_id}
```

### Create Rule
```http
POST /api/hrms/admin/deduction-rules
```

**Request Body:**
```json
{
  "type": "late",
  "min_minutes": 1,
  "max_minutes": 30,
  "deduction_percentage": 5.0,
  "is_active": true
}
```

**Validation:**
- `type`: Must be `late`, `absent`, or `early_leave`
- `min_minutes`: >= 0
- `max_minutes`: >= min_minutes
- `deduction_percentage`: 0 to 100
- Prevents overlapping rules for the same type

**Example Rules:**
```json
// Late 1-30 minutes: 5% deduction
{ "type": "late", "min_minutes": 1, "max_minutes": 30, "deduction_percentage": 5.0 }

// Late 31-60 minutes: 10% deduction
{ "type": "late", "min_minutes": 31, "max_minutes": 60, "deduction_percentage": 10.0 }

// Absent: 100% deduction
{ "type": "absent", "min_minutes": 0, "max_minutes": 1440, "deduction_percentage": 100.0 }
```

### Update Rule
```http
PATCH /api/hrms/admin/deduction-rules/{rule_id}
```

**Request Body:** (all fields optional)
```json
{
  "type": "late",
  "min_minutes": 1,
  "max_minutes": 45,
  "deduction_percentage": 7.5,
  "is_active": false
}
```

### Soft Delete Rule
```http
DELETE /api/hrms/admin/deduction-rules/{rule_id}/soft-delete
```

### Restore Rule
```http
POST /api/hrms/admin/deduction-rules/{rule_id}/restore
```

---

## Common Response Codes

### Success Codes
- `200 OK` - Request successful
- `201 Created` - Resource created successfully

### Error Codes
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate resource or constraint violation
- `500 Internal Server Error` - Server error

### Error Response Format
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Working schedule not found: 507f1f77bcf86cd799439011",
    "details": {}
  }
}
```

---

## Common Patterns

### Pagination
All list endpoints support pagination with consistent parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

Response includes:
- `items`: Array of resources
- `total`: Total count
- `page`: Current page
- `page_size`: Items per page
- `total_pages`: Total pages

### Soft Delete
All resources support soft delete:
- Soft deleted items have `lifecycle.deleted_at` timestamp
- Use `include_deleted=true` to include deleted items
- Use `deleted_only=true` to show only deleted items
- Use `/restore` endpoint to restore deleted items

### Lifecycle Tracking
All resources include lifecycle information:
```json
{
  "lifecycle": {
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-02T00:00:00Z",
    "deleted_at": null,
    "deleted_by": null
  }
}
```

---

## Integration Examples

### Check-in Validation Flow
```javascript
// 1. Get active work locations
GET /api/hrms/admin/work-locations/active

// 2. Validate employee GPS coordinates against locations
// Calculate distance and check if within radius

// 3. If valid, allow check-in
```

### Payroll Calculation Flow
```javascript
// 1. Get public holidays for the month
GET /api/hrms/admin/public-holidays/year/2024

// 2. Get employee's working schedule
GET /api/hrms/admin/working-schedules/{schedule_id}

// 3. Get active deduction rules
GET /api/hrms/admin/deduction-rules/active

// 4. Calculate:
// - Working days (excluding holidays and weekends)
// - Deductions (based on late/absent/early_leave rules)
// - Overtime (work on holidays/weekends)
```

### Attendance Deduction Flow
```javascript
// 1. Employee is late by 25 minutes
const lateMinutes = 25;

// 2. Get applicable deduction rule
GET /api/hrms/admin/deduction-rules/type/late
// Find rule where min_minutes <= 25 <= max_minutes

// 3. Calculate deduction
// If rule: 1-30 minutes = 5%
// Daily salary: $20
// Deduction: $20 * 0.05 = $1
```

---

## Notes

1. All timestamps are in ISO 8601 format (UTC)
2. All IDs are MongoDB ObjectId strings
3. Time fields use HH:MM:SS format
4. Date fields use YYYY-MM-DD format
5. All endpoints require authentication unless specified
6. Role-based access control is enforced
7. Validation errors return 400 with detailed messages
8. Duplicate prevention is enforced at domain level

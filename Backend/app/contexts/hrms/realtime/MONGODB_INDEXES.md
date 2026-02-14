# MongoDB Indexes for Realtime Attendance System

## Collections and Recommended Indexes

### 1. `attendance_events` Collection
Stores all check-in/out events with location and photo data.

```javascript
// Create indexes
db.attendance_events.createIndex({ "employee_id": 1, "created_at": -1 });
db.attendance_events.createIndex({ "type": 1, "created_at": -1 });
db.attendance_events.createIndex({ "created_at": -1 });

// Compound index for employee history queries
db.attendance_events.createIndex({ 
    "employee_id": 1, 
    "type": 1, 
    "created_at": -1 
});
```

**Purpose:**
- Fast lookup of employee attendance history
- Efficient filtering by event type (shift_start, shift_stop)
- Time-based queries for reports

### 2. `live_locations` Collection
Stores current/latest location state for each employee.

```javascript
// Create indexes
db.live_locations.createIndex({ "employee_id": 1 }, { unique: true });
db.live_locations.createIndex({ "status": 1, "last_seen_at": -1 });
db.live_locations.createIndex({ "status": 1, "updated_at": -1 });

// Geospatial index for location-based queries (optional, for future features)
db.live_locations.createIndex({ 
    "location": "2dsphere" 
});
```

**Purpose:**
- Unique constraint on employee_id (one live location per employee)
- Fast filtering of active employees for manager dashboard
- Efficient queries for stale location detection
- Optional: Geospatial queries for proximity features

### 3. TTL Index for Cleanup (Optional)
Auto-delete old attendance events after retention period.

```javascript
// Delete events older than 90 days
db.attendance_events.createIndex(
    { "created_at": 1 }, 
    { expireAfterSeconds: 7776000 }  // 90 days
);
```

## Index Creation Script

Run this in MongoDB shell or via Python:

```python
from pymongo import ASCENDING, DESCENDING, GEO2D
from app.contexts.infra.database.mongodb import get_db

def create_attendance_indexes():
    db = get_db()
    
    # attendance_events indexes
    db.attendance_events.create_index([("employee_id", ASCENDING), ("created_at", DESCENDING)])
    db.attendance_events.create_index([("type", ASCENDING), ("created_at", DESCENDING)])
    db.attendance_events.create_index([("created_at", DESCENDING)])
    db.attendance_events.create_index([
        ("employee_id", ASCENDING),
        ("type", ASCENDING),
        ("created_at", DESCENDING)
    ])
    
    # live_locations indexes
    db.live_locations.create_index([("employee_id", ASCENDING)], unique=True)
    db.live_locations.create_index([("status", ASCENDING), ("last_seen_at", DESCENDING)])
    db.live_locations.create_index([("status", ASCENDING), ("updated_at", DESCENDING)])
    
    print("✅ Attendance indexes created successfully")

if __name__ == "__main__":
    create_attendance_indexes()
```

## Performance Considerations

1. **Write Performance**: Indexes add overhead to writes. The `live_locations` collection has frequent updates (every 5 seconds per active employee), so keep indexes minimal.

2. **Read Performance**: The `status + last_seen_at` index is critical for manager dashboard queries to fetch all active employees efficiently.

3. **Storage**: Each index consumes disk space. Monitor index size with:
   ```javascript
   db.live_locations.stats()
   db.attendance_events.stats()
   ```

4. **Index Usage**: Monitor index usage with:
   ```javascript
   db.live_locations.aggregate([{ $indexStats: {} }])
   ```

## Data Retention Strategy

Consider implementing data archival:
- Keep `live_locations` current (delete inactive > 24 hours)
- Archive `attendance_events` older than 90 days to separate collection
- Use MongoDB TTL indexes or scheduled cleanup jobs

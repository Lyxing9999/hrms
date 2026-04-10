# app/contexts/hrms/repositories/attendance_repository.py
from bson import ObjectId
from datetime import datetime, date, timezone
from pymongo.database import Database
from app.contexts.hrms.domain.attendance import Attendance
from app.contexts.hrms.mapper.attendance_mapper import AttendanceMapper
from app.contexts.hrms.errors.attendance_exceptions import AttendanceNotFoundException
from app.contexts.shared.time_utils import ensure_utc
from datetime import datetime
from bson import ObjectId
from datetime import date
from calendar import monthrange

class MongoAttendanceRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_attendances"]
        self.mapper = AttendanceMapper()
    
    def _oid(self, v) -> ObjectId | None:
        if v is None:
            return None
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and v.strip().lower() in {"", "null", "none", "undefined"}:
            return None
        return ObjectId(v)
    def save(self, attendance: Attendance) -> Attendance:
        doc = self.mapper.to_persistence(attendance)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return attendance

    def find_by_id(self, attendance_id: ObjectId) -> Attendance:
        doc = self.collection.find_one({"_id": self._oid(attendance_id)})
        if not doc:
            raise AttendanceNotFoundException(attendance_id)
        return self.mapper.to_domain(doc)


    def find_by_employee_and_date(self, employee_id: ObjectId, attendance_date: datetime) -> Attendance | None:
        doc = self.collection.find_one({
            "employee_id": self._oid(employee_id),
            "attendance_date": attendance_date,
            "lifecycle.deleted_at": None,
        })

        return self.mapper.to_domain(doc) if doc else None

    def list_attendances(
        self,
        *,
        employee_id: ObjectId | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        status: str | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[Attendance], int]:
        query = {}

        if employee_id:
            query["employee_id"] = self._oid(employee_id)

        if start_date or end_date:
            query["check_in_time"] = {}
            if start_date:
                # Ensure timezone-aware
                query["check_in_time"]["$gte"] = ensure_utc(start_date)
            if end_date:
                # Ensure timezone-aware
                query["check_in_time"]["$lte"] = ensure_utc(end_date)

        if status:
            query["status"] = status

        # Handle soft delete filters
        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        total = self.collection.count_documents(query)
        skip = (page - 1) * limit

        docs = self.collection.find(query).sort("check_in_time", -1).skip(skip).limit(limit)
        attendances = [self.mapper.to_domain(doc) for doc in docs]

        return attendances, total

    def get_attendance_stats(
        self,
        employee_id: ObjectId,
        start_date: datetime,
        end_date: datetime,
    ) -> dict:
        """Calculate attendance statistics for an employee in a date range"""
        # Ensure timezone-aware datetimes
        start_date = ensure_utc(start_date)
        end_date = ensure_utc(end_date)
        
        pipeline = [
            {
                "$match": {
                    "employee_id": self._oid(employee_id),
                    "check_in_time": {"$gte": start_date, "$lte": end_date},
                    "lifecycle.deleted_at": None,
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_days": {"$sum": 1},
                    "late_days": {
                        "$sum": {"$cond": [{"$gt": ["$late_minutes", 0]}, 1, 0]}
                    },
                    "early_leave_days": {
                        "$sum": {"$cond": [{"$gt": ["$early_leave_minutes", 0]}, 1, 0]}
                    },
                    "total_late_minutes": {"$sum": "$late_minutes"},
                    "total_early_leave_minutes": {"$sum": "$early_leave_minutes"},
                }
            },
        ]

        result = list(self.collection.aggregate(pipeline))
        
        if not result:
            return {
                "total_days": 0,
                "present_days": 0,
                "late_days": 0,
                "early_leave_days": 0,
                "total_late_minutes": 0,
                "total_early_leave_minutes": 0,
                "attendance_rate": 0.0,
            }

        stats = result[0]
        total_days = stats["total_days"]
        
        # Calculate expected working days (simplified - could be enhanced with schedule)
        days_diff = (end_date - start_date).days + 1
        expected_days = days_diff  # Simplified, should consider weekends/holidays
        
        return {
            "total_days": total_days,
            "present_days": total_days,
            "late_days": stats["late_days"],
            "early_leave_days": stats["early_leave_days"],
            "total_late_minutes": stats["total_late_minutes"],
            "total_early_leave_minutes": stats["total_early_leave_minutes"],
            "attendance_rate": (total_days / expected_days * 100) if expected_days > 0 else 0.0,
        }
    def list_open_attendances(self) -> list[Attendance]:
        docs = self.collection.find({
            "check_in_time": {"$ne": None},
            "check_out_time": None,
            "lifecycle.deleted_at": None,
        })
        return [self.mapper.to_domain(doc) for doc in docs]
    def list_by_employee_and_month(self, *, employee_id, month: str):
        year, month_num = map(int, month.split("-"))
        month_start = date(year, month_num, 1)
        month_end = date(year, month_num, monthrange(year, month_num)[1])

        start_key = month_start.isoformat()
        end_key = month_end.isoformat()

        docs = list(
            self.collection.find({
                "employee_id": self._oid(employee_id),
                "lifecycle.deleted_at": None,
                "attendance_date_local": {
                    "$gte": start_key,
                    "$lte": end_key,
                },
            }).sort("attendance_date_local", 1)
        )
        return [self.mapper.to_domain(x) for x in docs]
    
    def delete(self, attendance_id: ObjectId) -> None:
        self.collection.delete_one({"_id": self._oid(attendance_id)})
# app/contexts/hrms/read_models/attendance_read_model.py
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime


class AttendanceReadModel:
    def __init__(self, db: Database):
        self.collection = db["attendances"]

    def find_by_id(self, attendance_id: ObjectId) -> dict | None:
        """Find attendance by ID"""
        return self.collection.find_one({"_id": attendance_id})

    def find_by_employee_today(self, employee_id: ObjectId) -> dict | None:
        """Find today's attendance for an employee"""
        from datetime import date
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        return self.collection.find_one({
            "employee_id": employee_id,
            "check_in_time": {"$gte": start_of_day, "$lte": end_of_day},
            "lifecycle.deleted_at": None,
        })


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
    ) -> tuple[list[dict], int]:
        """List attendances with filters"""
        query = {}

        if employee_id:
            query["employee_id"] = employee_id

        if start_date or end_date:
            query["check_in_time"] = {}
            if start_date:
                query["check_in_time"]["$gte"] = start_date
            if end_date:
                query["check_in_time"]["$lte"] = end_date

        if status:
            query["status"] = status

        # Handle soft delete filters
        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        total = self.collection.count_documents(query)
        skip = (page - 1) * limit

        docs = list(
            self.collection.find(query)
            .sort("check_in_time", -1)
            .skip(skip)
            .limit(limit)
        )

        return docs, total

    def get_employee_stats(
        self, employee_id: ObjectId, start_date: datetime, end_date: datetime
    ) -> dict:
        """Get attendance statistics for an employee"""
        pipeline = [
            {
                "$match": {
                    "employee_id": employee_id,
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
        
        # Calculate expected working days
        days_diff = (end_date - start_date).days + 1
        expected_days = days_diff
        
        return {
            "total_days": total_days,
            "present_days": total_days,
            "late_days": stats["late_days"],
            "early_leave_days": stats["early_leave_days"],
            "total_late_minutes": stats["total_late_minutes"],
            "total_early_leave_minutes": stats["total_early_leave_minutes"],
            "attendance_rate": (total_days / expected_days * 100) if expected_days > 0 else 0.0,
        }

# app/contexts/hrms/services/attendance_service.py
from bson import ObjectId
from datetime import datetime, date
from math import radians, cos, sin, asin, sqrt
from pymongo.database import Database

from app.contexts.hrms.domain.attendance import Attendance, AttendanceStatus
from app.contexts.hrms.repositories.attendance_repository import MongoAttendanceRepository
from app.contexts.hrms.repositories.work_location_repository import MongoWorkLocationRepository
from app.contexts.hrms.repositories.working_schedule_repository import MongoWorkingScheduleRepository
from app.contexts.hrms.repositories.employee_repository import MongoEmployeeRepository
from app.contexts.hrms.errors.attendance_exceptions import (
    AlreadyCheckedInTodayException,
    LocationValidationException,
    AttendanceNotFoundException,
)
from app.contexts.hrms.errors.employee_exceptions import EmployeeNotFoundException
from app.contexts.shared.lifecycle.domain import now_utc
from app.contexts.hrms.read_models.employee_read_model import EmployeeReadModel

class AttendanceService:
    def __init__(self, db: Database):
        self.repo = MongoAttendanceRepository(db)
        self.location_repo = MongoWorkLocationRepository(db)
        self.schedule_repo = MongoWorkingScheduleRepository(db)
        self.employee_repo = MongoEmployeeRepository(db)
        self.employee_read = EmployeeReadModel(db)
    def _calculate_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Calculate distance between two GPS coordinates in meters using Haversine formula"""
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        
        # Radius of earth in meters
        r = 6371000
        return c * r

    def _validate_location(
        self, latitude: float, longitude: float, location_id: ObjectId
    ) -> None:
        """Validate if check-in location is within allowed radius"""
        location = self.location_repo.find_by_id(location_id)
        
        if not location.is_active:
            raise LocationValidationException("Work location is not active")

        distance = self._calculate_distance(
            latitude, longitude, location.latitude, location.longitude
        )

        if distance > location.radius_meters:
            raise LocationValidationException(
                f"You are {int(distance)}m away from the work location. "
                f"Maximum allowed distance is {location.radius_meters}m"
            )

    def _calculate_late_minutes(
        self, check_in_time: datetime, schedule_id: ObjectId | None
    ) -> int:
        """Calculate how many minutes late the employee is"""
        if not schedule_id:
            return 0

        try:
            schedule = self.schedule_repo.find_by_id(schedule_id)
            
            # Get the day of week (0 = Monday, 6 = Sunday)
            day_of_week = check_in_time.weekday()
            
            # Check if it's a working day
            if day_of_week not in schedule.working_days:
                return 0

            # Parse schedule start time
            schedule_start = datetime.strptime(schedule.start_time, "%H:%M:%S").time()
            check_in_time_only = check_in_time.time()

            # Calculate difference in minutes
            if check_in_time_only > schedule_start:
                delta = datetime.combine(date.today(), check_in_time_only) - datetime.combine(
                    date.today(), schedule_start
                )
                return int(delta.total_seconds() / 60)

            return 0
        except Exception:
            return 0

    def _calculate_early_leave_minutes(
        self, check_out_time: datetime, schedule_id: ObjectId | None
    ) -> int:
        """Calculate how many minutes early the employee left"""
        if not schedule_id:
            return 0

        try:
            schedule = self.schedule_repo.find_by_id(schedule_id)
            
            # Get the day of week
            day_of_week = check_out_time.weekday()
            
            # Check if it's a working day
            if day_of_week not in schedule.working_days:
                return 0

            # Parse schedule end time
            schedule_end = datetime.strptime(schedule.end_time, "%H:%M:%S").time()
            check_out_time_only = check_out_time.time()

            # Calculate difference in minutes
            if check_out_time_only < schedule_end:
                delta = datetime.combine(date.today(), schedule_end) - datetime.combine(
                    date.today(), check_out_time_only
                )
                return int(delta.total_seconds() / 60)

            return 0
        except Exception:
            return 0

    def check_in(
        self,
        *,
        employee_id: ObjectId,
        location_id: ObjectId | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        notes: str | None = None,
        actor_id: ObjectId,
    ) -> Attendance:
        """Record employee check-in"""
        # Verify employee exists and get employee data
        employee_doc = self.employee_read.get_by_id(employee_id)
        if not employee_doc:
            raise EmployeeNotFoundException(employee_id)
        
        # Check if already checked in today
        today = date.today()
        existing = self.repo.find_by_employee_and_date(employee_id, today)
        if existing:
            raise AlreadyCheckedInTodayException(employee_id)

        # Validate location if provided
        if location_id and latitude is not None and longitude is not None:
            self._validate_location(latitude, longitude, location_id)

        check_in_time = now_utc()
        
        # Get schedule_id from employee document (might be None)
        schedule_id = employee_doc.get("schedule_id")
        
        # Calculate late minutes
        late_minutes = self._calculate_late_minutes(check_in_time, schedule_id)

        # Create attendance record
        attendance = Attendance(
            employee_id=employee_id,
            check_in_time=check_in_time,
            location_id=location_id,
            check_in_latitude=latitude,
            check_in_longitude=longitude,
            notes=notes,
            late_minutes=late_minutes,
            status=AttendanceStatus.LATE if late_minutes > 0 else AttendanceStatus.CHECKED_IN,
        )

        return self.repo.save(attendance)

    def check_out(
        self,
        *,
        attendance_id: ObjectId,
        latitude: float | None = None,
        longitude: float | None = None,
        notes: str | None = None,
        actor_id: ObjectId,
    ) -> Attendance:
        """Record employee check-out"""
        attendance = self.repo.find_by_id(attendance_id)
        
        # Get employee document to check schedule
        employee_doc = self.employee_read.get_by_id(attendance.employee_id)
        if not employee_doc:
            raise EmployeeNotFoundException(attendance.employee_id)
        
        check_out_time = now_utc()
        
        # Get schedule_id from employee document (might be None)
        schedule_id = employee_doc.get("schedule_id")
        
        # Calculate early leave minutes
        early_leave_minutes = self._calculate_early_leave_minutes(
            check_out_time, schedule_id
        )

        # Validate location if provided
        if attendance.location_id and latitude is not None and longitude is not None:
            self._validate_location(latitude, longitude, attendance.location_id)

        # Update notes if provided
        if notes:
            attendance.notes = notes

        attendance.check_out(
            check_out_time=check_out_time,
            latitude=latitude,
            longitude=longitude,
            early_leave_minutes=early_leave_minutes,
        )

        return self.repo.save(attendance)

    def get_attendance(self, attendance_id: ObjectId) -> Attendance:
        return self.repo.find_by_id(attendance_id)

    def get_today_attendance(self, employee_id: ObjectId) -> Attendance | None:
        """Get today's attendance record for an employee"""
        return self.repo.find_by_employee_and_date(employee_id, date.today())

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
        return self.repo.list_attendances(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            status=status,
            include_deleted=include_deleted,
            deleted_only=deleted_only,
            page=page,
            limit=limit,
        )

    def get_attendance_stats(
        self, employee_id: ObjectId, start_date: datetime, end_date: datetime
    ) -> dict:
        """Get attendance statistics for an employee"""
        return self.repo.get_attendance_stats(employee_id, start_date, end_date)

    def update_attendance(
        self, attendance_id: ObjectId, updates: dict, actor_id: ObjectId
    ) -> Attendance:
        """Update attendance record (admin only)"""
        attendance = self.repo.find_by_id(attendance_id)

        if "check_in_time" in updates:
            attendance.check_in_time = updates["check_in_time"]
        if "check_out_time" in updates:
            attendance.check_out_time = updates["check_out_time"]
        if "location_id" in updates:
            attendance.location_id = ObjectId(updates["location_id"]) if updates["location_id"] else None
        if "notes" in updates:
            attendance.notes = updates["notes"]
        if "late_minutes" in updates:
            attendance.late_minutes = updates["late_minutes"]
        if "early_leave_minutes" in updates:
            attendance.early_leave_minutes = updates["early_leave_minutes"]

        attendance.lifecycle.touch(now_utc())
        return self.repo.save(attendance)

    def soft_delete_attendance(
        self, attendance_id: ObjectId, actor_id: ObjectId
    ) -> Attendance:
        attendance = self.repo.find_by_id(attendance_id)
        attendance.soft_delete(actor_id=actor_id)
        return self.repo.save(attendance)

    def restore_attendance(self, attendance_id: ObjectId) -> Attendance:
        attendance = self.repo.find_by_id(attendance_id)
        attendance.restore()
        return self.repo.save(attendance)

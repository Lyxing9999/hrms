from __future__ import annotations

from datetime import datetime, timezone


class CheckInEmployeeUseCase:
    def __init__(
        self,
        *,
        employee_repository,
        working_schedule_repository,
        work_location_repository,
        attendance_repository,
        audit_log_repository=None,
    ) -> None:
        self.employee_repository = employee_repository
        self.working_schedule_repository = working_schedule_repository
        self.work_location_repository = work_location_repository
        self.attendance_repository = attendance_repository
        self.audit_log_repository = audit_log_repository

    def execute(
        self,
        *,
        employee_id,
        check_in_time: datetime,
        latitude: float,
        longitude: float,
        wrong_location_reason: str | None = None,
    ) -> dict:
        employee = self._get_employee(employee_id)
        schedule = self._get_schedule(employee)
        location = self._get_default_location()

        attendance_date = check_in_time.date()
        self._ensure_not_checked_in(employee_id=employee["_id"], attendance_date=attendance_date)

        is_valid_location = self._is_valid_location(
            location=location,
            latitude=latitude,
            longitude=longitude,
        )

        if not is_valid_location and not wrong_location_reason:
            raise ValueError("wrong_location_reason is required when check-in location is invalid")

        late_minutes = self._calculate_late_minutes(
            schedule=schedule,
            check_in_time=check_in_time,
        )

        status = "checked_in"
        if late_minutes > 0:
            status = "late"

        if not is_valid_location:
            status = "wrong_location_pending"

        now = datetime.now(timezone.utc)

        attendance_doc = {
            "employee_id": employee["_id"],
            "attendance_date": attendance_date,
            "check_in_time": check_in_time,
            "check_out_time": None,
            "schedule_id": schedule["_id"] if schedule else None,
            "location_id": location["_id"] if location else None,
            "check_in_latitude": latitude,
            "check_in_longitude": longitude,
            "check_out_latitude": None,
            "check_out_longitude": None,
            "status": status,
            "notes": None,
            "late_minutes": late_minutes,
            "early_leave_minutes": 0,
            "wrong_location_reason": wrong_location_reason,
            "admin_comment": None,
            "location_reviewed_by": None,
            "lifecycle": {
                "created_at": now,
                "updated_at": now,
                "deleted_at": None,
                "deleted_by": None,
            },
        }

        attendance = self.attendance_repository.create(attendance_doc)

        self._write_audit_log(
            action="attendance_check_in",
            actor_id=employee["_id"],
            entity_id=attendance["_id"],
            details={
                "status": attendance["status"],
                "late_minutes": attendance["late_minutes"],
                "attendance_date": str(attendance["attendance_date"]),
            },
        )

        return attendance

    def _get_employee(self, employee_id):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        if employee.get("status") != "active":
            raise ValueError("Employee is not active")
        return employee

    def _get_schedule(self, employee: dict) -> dict:
        schedule_id = employee.get("schedule_id")
        if not schedule_id:
            raise ValueError("Employee has no assigned schedule")
        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise ValueError("Working schedule not found")
        return schedule

    def _get_default_location(self) -> dict | None:
        # Replace with your real method if different
        if hasattr(self.work_location_repository, "find_active_default"):
            return self.work_location_repository.find_active_default()
        if hasattr(self.work_location_repository, "find_default"):
            return self.work_location_repository.find_default()
        if hasattr(self.work_location_repository, "list_locations"):
            items = self.work_location_repository.list_locations(is_active=True)
            return items[0] if items else None
        return None

    def _ensure_not_checked_in(self, *, employee_id, attendance_date) -> None:
        existing = self.attendance_repository.find_by_employee_and_date(employee_id, attendance_date)
        if existing:
            raise ValueError("Attendance already exists for this date")

    def _is_valid_location(self, *, location: dict | None, latitude: float, longitude: float) -> bool:
        if not location:
            return True

        office_lat = float(location["latitude"])
        office_lng = float(location["longitude"])
        radius_meters = int(location["radius_meters"])

        distance = self._distance_meters(office_lat, office_lng, latitude, longitude)
        return distance <= radius_meters

    def _distance_meters(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        from math import radians, sin, cos, sqrt, atan2

        r = 6371000.0
        dlat = radians(lat2 - lat1)
        dlng = radians(lng2 - lng1)

        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return r * c

    def _calculate_late_minutes(self, *, schedule: dict, check_in_time: datetime) -> int:
        start_time = schedule.get("start_time")
        if not start_time:
            return 0

        # supports "08:00:00" or time object
        if hasattr(start_time, "hour"):
            schedule_start = check_in_time.replace(
                hour=start_time.hour,
                minute=start_time.minute,
                second=getattr(start_time, "second", 0),
                microsecond=0,
            )
        else:
            hh, mm, *rest = str(start_time).split(":")
            ss = int(rest[0]) if rest else 0
            schedule_start = check_in_time.replace(
                hour=int(hh),
                minute=int(mm),
                second=ss,
                microsecond=0,
            )

        if check_in_time <= schedule_start:
            return 0

        return int((check_in_time - schedule_start).total_seconds() // 60)

    def _write_audit_log(self, *, action: str, actor_id, entity_id, details: dict) -> None:
        if not self.audit_log_repository:
            return

        self.audit_log_repository.save(
            {
                "entity_type": "attendance",
                "entity_id": entity_id,
                "action": action,
                "actor_id": actor_id,
                "action_at": datetime.now(timezone.utc),
                "details": details,
            }
        )
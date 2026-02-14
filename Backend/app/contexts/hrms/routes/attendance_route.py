# app/contexts/hrms/routes/attendance_route.py
from flask import Blueprint, request, g
from bson import ObjectId
from datetime import datetime

from app.contexts.core.security.decorators import require_auth, require_role
from app.contexts.core.security.auth_utils import get_current_employee_id
from app.contexts.shared.decorators.response_decorator import success_response
from app.contexts.hrms.mapper.attendance_mapper import AttendanceMapper
from app.contexts.hrms.data_transfer.request.attendance_request import (
    AttendanceCheckInSchema,
    AttendanceCheckOutSchema,
    AttendanceUpdateSchema,
)
from app.contexts.hrms.data_transfer.response.attendance_response import (
    AttendanceDTO,
    AttendancePaginatedDTO,
    AttendanceStatsDTO,
)
from app.contexts.shared.time_utils import ensure_utc

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.route("/employee/attendance/check-in", methods=["POST"])
@require_auth
@require_role("employee", "manager", "hr_admin")
@success_response
def check_in():
    """Employee check-in"""
    data = AttendanceCheckInSchema(**request.get_json())
    mapper = AttendanceMapper()
    current_user_id = ObjectId(g.user["id"])
    
    if data.employee_id:
        employee_id = ObjectId(data.employee_id)
    else:
        employee_id = get_current_employee_id()

    attendance = g.hrms.attendance_service.check_in(
        employee_id=employee_id,
        location_id=ObjectId(data.location_id) if data.location_id else None,
        latitude=data.latitude,
        longitude=data.longitude,
        notes=data.notes,
        actor_id=current_user_id,
    )

    return AttendanceDTO(**mapper.to_dto(attendance))


@attendance_bp.route("/employee/attendance/<attendance_id>/check-out", methods=["POST"])
@require_auth
@require_role("employee", "manager", "hr_admin")
@success_response
def check_out(attendance_id: str):
    """Employee check-out"""
    data = AttendanceCheckOutSchema(**request.get_json())
    mapper = AttendanceMapper()
    current_user_id = ObjectId(g.user["id"])

    attendance = g.hrms.attendance_service.check_out(
        attendance_id=ObjectId(attendance_id),
        latitude=data.latitude,
        longitude=data.longitude,
        notes=data.notes,
        actor_id=current_user_id,
    )

    return AttendanceDTO(**mapper.to_dto(attendance))


@attendance_bp.route("/employee/attendance/today", methods=["GET"])
@require_auth
@require_role("employee", "manager", "hr_admin")
@success_response
def get_today_attendance():
    """Get today's attendance for current user"""
    mapper = AttendanceMapper()
    
    employee_id_str = request.args.get("employee_id")
    if employee_id_str:
        employee_id = ObjectId(employee_id_str)
    else:
        employee_id = get_current_employee_id()

    attendance = g.hrms.attendance_service.get_today_attendance(employee_id)
    
    if not attendance:
        return None

    return AttendanceDTO(**mapper.to_dto(attendance))


@attendance_bp.route("/employee/attendance/history", methods=["GET"])
@require_auth
@require_role("employee", "manager", "hr_admin")
@success_response
def get_employee_attendance_history():
    """Get attendance history for current employee"""
    mapper = AttendanceMapper()

    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    status = request.args.get("status")
    page = int(request.args.get("page", 1))
    limit = min(int(request.args.get("limit", 10)), 100)

    employee_id = get_current_employee_id()

    start_date = ensure_utc(datetime.fromisoformat(start_date_str)) if start_date_str else None
    end_date = ensure_utc(datetime.fromisoformat(end_date_str)) if end_date_str else None

    attendances, total = g.hrms.attendance_service.list_attendances(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
        include_deleted=False,
        deleted_only=False,
        page=page,
        limit=limit,
    )

    items = [AttendanceDTO(**mapper.to_dto(a)) for a in attendances]
    total_pages = (total + limit - 1) // limit

    return AttendancePaginatedDTO(
        items=items,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages,
    )


@attendance_bp.route("/employee/attendance/stats", methods=["GET"])
@require_auth
@require_role("employee", "manager", "hr_admin")
@success_response
def get_employee_attendance_stats():
    """Get attendance statistics for current employee"""
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    if not all([start_date_str, end_date_str]):
        return {"error": "start_date and end_date are required"}, 400

    employee_id = get_current_employee_id()
    start_date = ensure_utc(datetime.fromisoformat(start_date_str))
    end_date = ensure_utc(datetime.fromisoformat(end_date_str))

    stats = g.hrms.attendance_service.get_attendance_stats(employee_id, start_date, end_date)
    return AttendanceStatsDTO(**stats)


@attendance_bp.route("/employees/<employee_id>/attendance/history", methods=["GET"])
@require_auth
@require_role("hr_admin", "manager", "employee")
@success_response
def get_employee_attendance_history_by_id(employee_id: str):
    """Get attendance history for a specific employee by ID"""
    mapper = AttendanceMapper()

    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    status = request.args.get("status")
    page = int(request.args.get("page", 1))
    limit = min(int(request.args.get("limit", 10)), 100)

    start_date = ensure_utc(datetime.fromisoformat(start_date_str)) if start_date_str else None
    end_date = ensure_utc(datetime.fromisoformat(end_date_str)) if end_date_str else None

    attendances, total = g.hrms.attendance_service.list_attendances(
        employee_id=ObjectId(employee_id),
        start_date=start_date,
        end_date=end_date,
        status=status,
        include_deleted=False,
        deleted_only=False,
        page=page,
        limit=limit,
    )

    items = [AttendanceDTO(**mapper.to_dto(a)) for a in attendances]
    total_pages = (total + limit - 1) // limit

    return AttendancePaginatedDTO(
        items=items,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages,
    )


@attendance_bp.route("/employees/<employee_id>/attendance/stats", methods=["GET"])
@require_auth
@require_role("hr_admin", "manager", "employee")
@success_response
def get_employee_attendance_stats_by_id(employee_id: str):
    """Get attendance statistics for a specific employee by ID"""
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    if not all([start_date_str, end_date_str]):
        return {"error": "start_date and end_date are required"}, 400

    start_date = ensure_utc(datetime.fromisoformat(start_date_str))
    end_date = ensure_utc(datetime.fromisoformat(end_date_str))

    stats = g.hrms.attendance_service.get_attendance_stats(ObjectId(employee_id), start_date, end_date)
    return AttendanceStatsDTO(**stats)


@attendance_bp.route("/admin/attendances", methods=["GET"])
@require_auth
@require_role("hr_admin", "manager")
@success_response
def list_attendances():
    """List attendance records with filters"""
    mapper = AttendanceMapper()

    employee_id_str = request.args.get("employee_id")
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    status = request.args.get("status")
    include_deleted = request.args.get("include_deleted", "false").lower() == "true"
    deleted_only = request.args.get("deleted_only", "false").lower() == "true"
    page = int(request.args.get("page", 1))
    limit = min(int(request.args.get("limit", 10)), 100)

    start_date = ensure_utc(datetime.fromisoformat(start_date_str)) if start_date_str else None
    end_date = ensure_utc(datetime.fromisoformat(end_date_str)) if end_date_str else None
    employee_id = ObjectId(employee_id_str) if employee_id_str else None

    attendances, total = g.hrms.attendance_service.list_attendances(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
        include_deleted=include_deleted,
        deleted_only=deleted_only,
        page=page,
        limit=limit,
    )

    items = [AttendanceDTO(**mapper.to_dto(a)) for a in attendances]
    total_pages = (total + limit - 1) // limit

    return AttendancePaginatedDTO(
        items=items,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages,
    )


@attendance_bp.route("/admin/attendances/<attendance_id>", methods=["GET"])
@require_auth
@require_role("hr_admin", "manager", "employee")
@success_response
def get_attendance(attendance_id: str):
    """Get attendance by ID"""
    mapper = AttendanceMapper()

    attendance = g.hrms.attendance_service.get_attendance(ObjectId(attendance_id))
    return AttendanceDTO(**mapper.to_dto(attendance))


@attendance_bp.route("/admin/attendances/<attendance_id>", methods=["PATCH"])
@require_auth
@require_role("hr_admin")
@success_response
def update_attendance(attendance_id: str):
    """Update attendance record (admin only)"""
    data = AttendanceUpdateSchema(**request.get_json())
    mapper = AttendanceMapper()
    current_user_id = ObjectId(g.user["id"])
    
    updates = data.model_dump(exclude_unset=True)
    attendance = g.hrms.attendance_service.update_attendance(
        ObjectId(attendance_id), updates, current_user_id
    )

    return AttendanceDTO(**mapper.to_dto(attendance))


@attendance_bp.route("/admin/attendances/stats", methods=["GET"])
@require_auth
@require_role("hr_admin", "manager", "employee")
@success_response
def get_attendance_stats():
    """Get attendance statistics for an employee"""
    employee_id_str = request.args.get("employee_id")
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    if not all([employee_id_str, start_date_str, end_date_str]):
        return {"error": "employee_id, start_date, and end_date are required"}, 400

    employee_id = ObjectId(employee_id_str)
    start_date = ensure_utc(datetime.fromisoformat(start_date_str))
    end_date = ensure_utc(datetime.fromisoformat(end_date_str))

    stats = g.hrms.attendance_service.get_attendance_stats(employee_id, start_date, end_date)
    return AttendanceStatsDTO(**stats)


@attendance_bp.route("/admin/attendances/<attendance_id>/soft-delete", methods=["DELETE"])
@require_auth
@require_role("hr_admin")
@success_response
def soft_delete_attendance(attendance_id: str):
    """Soft delete attendance"""
    mapper = AttendanceMapper()
    current_user_id = ObjectId(g.user["id"])

    attendance = g.hrms.attendance_service.soft_delete_attendance(ObjectId(attendance_id), current_user_id)
    return AttendanceDTO(**mapper.to_dto(attendance))


@attendance_bp.route("/admin/attendances/<attendance_id>/restore", methods=["POST"])
@require_auth
@require_role("hr_admin")
@success_response
def restore_attendance(attendance_id: str):
    """Restore soft-deleted attendance"""
    mapper = AttendanceMapper()

    attendance = g.hrms.attendance_service.restore_attendance(ObjectId(attendance_id))
    return AttendanceDTO(**mapper.to_dto(attendance))

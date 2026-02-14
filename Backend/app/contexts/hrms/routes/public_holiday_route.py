# app/contexts/hrms/routes/public_holiday_route.py
from flask import Blueprint, request, g
from app.contexts.shared.model_converter import pydantic_converter, mongo_converter
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.core.security.auth_utils import get_current_staff_id
import math

from app.contexts.hrms.data_transfer.request.public_holiday_request import (
    PublicHolidayCreateSchema,
    PublicHolidayUpdateSchema,
)
from app.contexts.hrms.data_transfer.response.public_holiday_response import (
    PublicHolidayDTO,
    PublicHolidayPaginatedDTO,
)

public_holiday_bp = Blueprint("public_holiday_bp", __name__)


# -------------------------
# LIST HOLIDAYS
# -------------------------
@public_holiday_bp.route("/public-holidays", methods=["GET"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def list_holidays():
    q = (request.args.get("q") or "").strip()
    page = max(int(request.args.get("page") or 1), 1)
    page_size = min(max(int(request.args.get("limit") or 10), 1), 100)
    
    year_str = request.args.get("year")
    year = int(year_str) if year_str else None
    
    include_deleted = (request.args.get("include_deleted") or "false").lower() == "true"
    deleted_only = (request.args.get("deleted_only") or "false").lower() == "true"
    show_deleted = "all" if include_deleted else ("deleted_only" if deleted_only else "active")
    
    items, total = g.hrms.public_holiday_service.list_holidays(
        q=q,
        page=page,
        page_size=page_size,
        year=year,
        show_deleted=show_deleted,
    )
    
    items_dto = [mongo_converter.doc_to_dto(g.hrms.public_holiday_service._mapper.to_persistence(item), PublicHolidayDTO) for item in items]
    total_pages = max(1, math.ceil(int(total) / page_size))
    
    return PublicHolidayPaginatedDTO(
        items=items_dto,
        total=int(total),
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


# -------------------------
# GET HOLIDAYS BY YEAR
# -------------------------
@public_holiday_bp.route("/public-holidays/year/<int:year>", methods=["GET"])
@login_required(allowed_roles=["hr_admin", "manager", "employee"])
@wrap_response
def get_holidays_by_year(year: int):
    holidays = g.hrms.public_holiday_service.get_holidays_by_year(year)
    items_dto = [mongo_converter.doc_to_dto(g.hrms.public_holiday_service._mapper.to_persistence(h), PublicHolidayDTO) for h in holidays]
    
    return {"items": items_dto, "year": year}


# -------------------------
# GET SINGLE HOLIDAY
# -------------------------
@public_holiday_bp.route("/public-holidays/<holiday_id>", methods=["GET"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def get_holiday(holiday_id: str):
    holiday = g.hrms.public_holiday_service.get_holiday(holiday_id)
    return mongo_converter.doc_to_dto(g.hrms.public_holiday_service._mapper.to_persistence(holiday), PublicHolidayDTO)


# -------------------------
# CREATE HOLIDAY
# -------------------------
@public_holiday_bp.route("/public-holidays", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_holiday():
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, PublicHolidayCreateSchema)
    holiday = g.hrms.public_holiday_service.create_holiday(payload, created_by_user_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.public_holiday_service._mapper.to_persistence(holiday), PublicHolidayDTO)


# -------------------------
# UPDATE HOLIDAY
# -------------------------
@public_holiday_bp.route("/public-holidays/<holiday_id>", methods=["PATCH"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_holiday(holiday_id: str):
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, PublicHolidayUpdateSchema)
    holiday = g.hrms.public_holiday_service.update_holiday(holiday_id, payload, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.public_holiday_service._mapper.to_persistence(holiday), PublicHolidayDTO)


# -------------------------
# SOFT DELETE HOLIDAY
# -------------------------
@public_holiday_bp.route("/public-holidays/<holiday_id>/soft-delete", methods=["DELETE"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_holiday(holiday_id: str):
    staff_id = get_current_staff_id()
    
    holiday = g.hrms.public_holiday_service.soft_delete_holiday(holiday_id, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.public_holiday_service._mapper.to_persistence(holiday), PublicHolidayDTO)


# -------------------------
# RESTORE HOLIDAY
# -------------------------
@public_holiday_bp.route("/public-holidays/<holiday_id>/restore", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_holiday(holiday_id: str):
    holiday = g.hrms.public_holiday_service.restore_holiday(holiday_id)
    return mongo_converter.doc_to_dto(g.hrms.public_holiday_service._mapper.to_persistence(holiday), PublicHolidayDTO)

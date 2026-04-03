from __future__ import annotations

from app.contexts.hrms.data_transfer.response.public_holiday_response import PublicHolidayImportResultDTO
from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_staff_id
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.shared.model_converter import pydantic_converter
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.hrms.data_transfer.request.public_holiday_request import (
    PublicHolidayCreateSchema,
    PublicHolidayImportDefaultsSchema,
    PublicHolidayUpdateSchema,
)
from app.contexts.hrms.mapper.public_holiday_mapper import PublicHolidayMapper


public_holiday_command_bp = Blueprint("public_holiday_command_bp", __name__)
mapper = PublicHolidayMapper()


@public_holiday_command_bp.route("/public-holidays", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_public_holiday():
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, PublicHolidayCreateSchema)

    holiday = g.hrms.public_holiday.create(
        payload=payload,
        created_by_user_id=staff_id,
    )
    return mapper.to_dto(holiday).model_dump(mode="json")


@public_holiday_command_bp.route("/public-holidays/<holiday_id>", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_public_holiday(holiday_id: str):
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, PublicHolidayUpdateSchema)

    holiday = g.hrms.public_holiday.update(
        holiday_id=holiday_id,
        payload=payload,
        actor_id=staff_id,
    )
    return mapper.to_dto(holiday).model_dump(mode="json")


@public_holiday_command_bp.route("/public-holidays/<holiday_id>", methods=["DELETE"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_public_holiday(holiday_id: str):
    staff_id = get_current_staff_id()

    holiday = g.hrms.public_holiday.soft_delete(
        holiday_id=holiday_id,
        actor_id=staff_id,
    )
    return mapper.to_dto(holiday).model_dump(mode="json")


@public_holiday_command_bp.route("/public-holidays/<holiday_id>/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_public_holiday(holiday_id: str):
    holiday = g.hrms.public_holiday.restore(
        holiday_id=holiday_id,
    )
    return mapper.to_dto(holiday).model_dump(mode="json")




@public_holiday_command_bp.route("/public-holidays/import-defaults", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def import_default_public_holidays():
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, PublicHolidayImportDefaultsSchema)

    result = g.hrms.public_holiday.import_defaults(
        year=payload.year,
        created_by_user_id=staff_id,
    )

    dto = PublicHolidayImportResultDTO(
        year=result["year"],
        imported_count=result["imported_count"],
        skipped_count=result["skipped_count"],
        imported=[mapper.to_dto(item) for item in result["imported"]],
        skipped_dates=result["skipped_dates"],
    )
    return dto.model_dump(mode="json")
    
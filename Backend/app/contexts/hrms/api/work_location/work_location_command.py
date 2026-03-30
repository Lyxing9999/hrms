
from __future__ import annotations

from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_staff_id
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.shared.model_converter import pydantic_converter
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.hrms.data_transfer.request.work_location_request import (
    WorkLocationCreateSchema,
    WorkLocationUpdateSchema,
)
from app.contexts.hrms.mapper.work_location_mapper import WorkLocationMapper


work_location_command_bp = Blueprint("work_location_command_bp", __name__)
mapper = WorkLocationMapper()


@work_location_command_bp.route("/work-locations", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_work_location():
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, WorkLocationCreateSchema)

    location = g.hrms.work_location.create(
        payload=payload,
        created_by_user_id=staff_id,
    )
    return mapper.to_dto(location).model_dump(mode="json")


@work_location_command_bp.route("/work-locations/<location_id>", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_work_location(location_id: str):
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, WorkLocationUpdateSchema)

    location = g.hrms.work_location.update(
        location_id=location_id,
        payload=payload,
        actor_id=staff_id,
    )
    return mapper.to_dto(location).model_dump(mode="json")


@work_location_command_bp.route("/work-locations/<location_id>/activate", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def activate_work_location(location_id: str):
    staff_id = get_current_staff_id()
    location = g.hrms.work_location.activate(
        location_id=location_id,
        actor_id=staff_id,
    )
    return mapper.to_dto(location).model_dump(mode="json")


@work_location_command_bp.route("/work-locations/<location_id>/deactivate", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def deactivate_work_location(location_id: str):
    staff_id = get_current_staff_id()
    location = g.hrms.work_location.deactivate(
        location_id=location_id,
        actor_id=staff_id,
    )
    return mapper.to_dto(location).model_dump(mode="json")


@work_location_command_bp.route("/work-locations/<location_id>", methods=["DELETE"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_work_location(location_id: str):
    staff_id = get_current_staff_id()
    location = g.hrms.work_location.soft_delete(
        location_id=location_id,
        actor_id=staff_id,
    )
    return mapper.to_dto(location).model_dump(mode="json")


@work_location_command_bp.route("/work-locations/<location_id>/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_work_location(location_id: str):
    location = g.hrms.work_location.restore(location_id=location_id)
    return mapper.to_dto(location).model_dump(mode="json")
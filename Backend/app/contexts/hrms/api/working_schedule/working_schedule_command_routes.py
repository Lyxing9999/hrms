from __future__ import annotations
from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_staff_id
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.shared.model_converter import pydantic_converter
from app.contexts.hrms.data_transfer.request.working_schedule_request import (
    WorkingScheduleCreateSchema,
    WorkingScheduleUpdateSchema,
)
from app.contexts.hrms.mapper.working_schedule_mapper import WorkingScheduleMapper
from app.contexts.iam.auth.jwt_utils import login_required

working_schedule_command_bp = Blueprint("working_schedule_command_bp", __name__)
mapper = WorkingScheduleMapper()


@working_schedule_command_bp.route("/working-schedules", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_working_schedule():
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, WorkingScheduleCreateSchema)
    schedule = g.hrms.working_schedule.create(payload=payload, created_by=staff_id)
    return mapper.to_dto(schedule)


@working_schedule_command_bp.route("/working-schedules/<schedule_id>", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_working_schedule(schedule_id: str):
    payload = pydantic_converter.convert_to_model(request.json, WorkingScheduleUpdateSchema)
    schedule = g.hrms.working_schedule.update(schedule_id=schedule_id, payload=payload)
    return mapper.to_dto(schedule)


@working_schedule_command_bp.route("/working-schedules/<schedule_id>", methods=["DELETE"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_working_schedule(schedule_id: str):
    staff_id = get_current_staff_id()
    schedule = g.hrms.working_schedule.soft_delete(schedule_id=schedule_id, actor_id=staff_id)
    return mapper.to_dto(schedule)


@working_schedule_command_bp.route("/working-schedules/<schedule_id>/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_working_schedule(schedule_id: str):
    schedule = g.hrms.working_schedule.restore(schedule_id=schedule_id)
    return mapper.to_dto(schedule)


@working_schedule_command_bp.route("/working-schedules/default", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def set_default_working_schedule():
    schedule_id = request.json.get("schedule_id")
    schedule = g.hrms.working_schedule.set_default(schedule_id=schedule_id)
    return mapper.to_dto(schedule)

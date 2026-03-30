from __future__ import annotations
from flask import Blueprint, g
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.hrms.mapper.working_schedule_mapper import WorkingScheduleMapper
from app.contexts.iam.auth.jwt_utils import login_required

working_schedule_query_bp = Blueprint("working_schedule_query_bp", __name__)
mapper = WorkingScheduleMapper()


@working_schedule_query_bp.route("/working-schedules", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin", "employee"])
@wrap_response
def list_working_schedules():
    schedules = g.hrms.working_schedule.list()
    return [mapper.to_dto(schedule).model_dump(mode="json") for schedule in schedules]


@working_schedule_query_bp.route("/working-schedules/<schedule_id>", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin", "employee"])
@wrap_response
def get_working_schedule(schedule_id: str):
    schedule = g.hrms.working_schedule.get(schedule_id=schedule_id)
    return mapper.to_dto(schedule).model_dump(mode="json")


@working_schedule_query_bp.route("/working-schedules/default", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin", "employee"])
@wrap_response
def get_default_working_schedule():
    schedule = g.hrms.working_schedule.get_default()
    return mapper.to_dto(schedule).model_dump(mode="json")




@working_schedule_query_bp.route("/working-schedules/select-options", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin", "employee"])
@wrap_response
def list_working_schedule_select_options():
    schedules = g.hrms.working_schedule.list()
    return [
        {
            "value": schedule.id,
            "label": schedule.name,
        }
        for schedule in schedules
    ]
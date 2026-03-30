from __future__ import annotations

from app.contexts.hrms.api.working_schedule.working_schedule_command_routes import working_schedule_command_bp
from app.contexts.hrms.api.working_schedule.working_schedule_query_routes import working_schedule_query_bp


def register_working_schedule_routes(app) -> None:
    """
    Register both command and query blueprints for working schedules.
    """
    app.register_blueprint(working_schedule_command_bp, url_prefix="/api/hrms")
    app.register_blueprint(working_schedule_query_bp, url_prefix="/api/hrms")
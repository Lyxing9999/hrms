from __future__ import annotations

from app.contexts.hrms.api.employee.employee_command_routes import employee_command_bp
from app.contexts.hrms.api.employee.employee_query_routes import employee_query_bp


def register_employee_routes(app) -> None:
    app.register_blueprint(employee_command_bp, url_prefix="/api/hrms")
    app.register_blueprint(employee_query_bp, url_prefix="/api/hrms")
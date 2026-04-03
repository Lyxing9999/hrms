

from app.contexts.hrms.api.overtime.overtime_command_routes import (
    overtime_command_bp,
)
from app.contexts.hrms.api.overtime.overtime_query_routes import (
    overtime_query_bp,
)

def register_overtime_routes(app) -> None:
    app.register_blueprint(overtime_command_bp, url_prefix="/api/hrms")
    app.register_blueprint(overtime_query_bp, url_prefix="/api/hrms")
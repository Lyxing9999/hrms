from app.contexts.hrms.api.attendance.attendance_command_routes import attendance_command_bp
from app.contexts.hrms.api.attendance.attendance_query_routes import attendance_query_bp


def register_attendance_routes(app) -> None:
    app.register_blueprint(attendance_command_bp, url_prefix="/api/hrms")
    app.register_blueprint(attendance_query_bp, url_prefix="/api/hrms")
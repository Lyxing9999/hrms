
from app.contexts.hrms.api.leave.leave_command_routes import leave_command_bp
from app.contexts.hrms.api.leave.leave_query_routes import leave_query_bp



def register_leave_routes(app) -> None:
    app.register_blueprint(leave_command_bp, url_prefix="/api/hrms")
    app.register_blueprint(leave_query_bp, url_prefix="/api/hrms")
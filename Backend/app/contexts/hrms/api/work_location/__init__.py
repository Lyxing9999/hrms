from app.contexts.hrms.api.work_location.work_location_command import work_location_command_bp
from app.contexts.hrms.api.work_location.work_location_query import work_location_query_bp




def register_work_location_routes(app) -> None:
    app.register_blueprint(work_location_command_bp, url_prefix="/api/hrms")
    app.register_blueprint(work_location_query_bp, url_prefix="/api/hrms")
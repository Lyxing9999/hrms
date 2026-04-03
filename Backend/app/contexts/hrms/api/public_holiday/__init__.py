
from app.contexts.hrms.api.public_holiday.public_holiday_command_routes import (
    public_holiday_command_bp,
)
from app.contexts.hrms.api.public_holiday.public_holiday_query_routes import (
    public_holiday_query_bp,
)

def register_public_holiday_routes(app) -> None:
    app.register_blueprint(public_holiday_command_bp, url_prefix="/api/hrms")
    app.register_blueprint(public_holiday_query_bp, url_prefix="/api/hrms")
from flask import g, Blueprint
from pymongo.database import Database

from app.contexts.infra.database.db import get_db

from .employee_route import employee_bp
from .leave_route import leave_bp
from .employee_upload_route import employee_upload_bp
from .working_schedule_route import working_schedule_bp
from .work_location_route import work_location_bp
from .public_holiday_route import public_holiday_bp
from .deduction_rule_route import deduction_rule_bp
from .attendance_route import attendance_bp
from .photo_upload_route import photo_upload_bp

from app.contexts.hrms.read_models.employee_read_model import EmployeeReadModel
from app.contexts.hrms.read_models.attendance_read_model import AttendanceReadModel
from app.contexts.hrms.services.employee_service import EmployeeService
from app.contexts.hrms.services.leave_service import LeaveService
from app.contexts.hrms.services.attendance_service import AttendanceService
from app.contexts.hrms.services.working_schedule_service import WorkingScheduleService
from app.contexts.hrms.services.work_location_service import WorkLocationService
from app.contexts.hrms.services.public_holiday_service import PublicHolidayService
from app.contexts.hrms.services.deduction_rule_service import DeductionRuleService

import traceback
from flask import current_app

# Create a single HRMS blueprint for context management
hrms_context_bp = Blueprint("hrms_context", __name__)


class HrmsContext:
    """
    All HRMS-related services and read models for the current request.
    Similar to AdminContext pattern.
    """

    def __init__(self, db: Database) -> None:
        # Read models
        self.employee_read_model = EmployeeReadModel(db)
        self.attendance_read_model = AttendanceReadModel(db)
        
        # Services
        self.employee_service = EmployeeService(db)
        self.leave_service = LeaveService(db)
        self.attendance_service = AttendanceService(db)
        self.working_schedule_service = WorkingScheduleService(db)
        self.work_location_service = WorkLocationService(db)
        self.public_holiday_service = PublicHolidayService(db)
        self.deduction_rule_service = DeductionRuleService(db)


@hrms_context_bp.before_app_request
def load_hrms_context():
    """
    Attach a single HrmsContext to g for this request.
    """
    try:
        if not hasattr(g, "hrms"):
            db = get_db()
            g.hrms = HrmsContext(db)
    except Exception as e:
        current_app.logger.exception("HRMS context init failed")
        raise


@hrms_context_bp.teardown_app_request
def remove_hrms_context(exc=None) -> None:
    if hasattr(g, "hrms"):
        del g.hrms


def register_hrms_routes(app) -> None:
    """
    Call this from create_app() to register all HRMS blueprints with context.
    """
    # Register the context blueprint first (for before_app_request hook)
    app.register_blueprint(hrms_context_bp)
    
    # Register all HRMS blueprints
    app.register_blueprint(employee_bp, url_prefix="/api/hrms/admin")
    app.register_blueprint(employee_upload_bp, url_prefix="/uploads")
    app.register_blueprint(leave_bp, url_prefix="/api/hrms")
    app.register_blueprint(working_schedule_bp, url_prefix="/api/hrms/admin")
    app.register_blueprint(work_location_bp, url_prefix="/api/hrms/admin")
    app.register_blueprint(public_holiday_bp, url_prefix="/api/hrms/admin")
    app.register_blueprint(deduction_rule_bp, url_prefix="/api/hrms/admin")
    app.register_blueprint(attendance_bp, url_prefix="/api/hrms")
    app.register_blueprint(photo_upload_bp)


__all__ = [
    "employee_bp",
    "leave_bp",
    "employee_upload_bp",
    "working_schedule_bp",
    "work_location_bp",
    "public_holiday_bp",
    "deduction_rule_bp",
    "attendance_bp",
    "photo_upload_bp",
    "HrmsContext",
    "load_hrms_context",
    "register_hrms_routes",
]

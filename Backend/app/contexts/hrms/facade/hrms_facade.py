from __future__ import annotations

from app.contexts.hrms.facade.employee_facade import EmployeeFacade
from app.contexts.hrms.facade.attendance_facade import AttendanceFacade
from app.contexts.hrms.facade.public_holiday_facade import PublicHolidayFacade
from app.contexts.hrms.facade.work_location_facade import WorkLocationFacade
from app.contexts.hrms.facade.working_schedule_facade import WorkingScheduleFacade
from app.contexts.hrms.facade.overtime_facade import OvertimeFacade
from app.contexts.hrms.facade.leave_facade import LeaveFacade
from app.contexts.hrms.facade.payroll_facade import PayrollFacade


class HrmsFacade:
    def __init__(
        self,
        *,
        employee: EmployeeFacade,
        attendance: AttendanceFacade,
        working_schedule: WorkingScheduleFacade,
        overtime: OvertimeFacade,
        leave: LeaveFacade,
        payroll: PayrollFacade,
        work_location: WorkLocationFacade,
        public_holiday: PublicHolidayFacade,
    ) -> None:
        self.employee = employee
        self.attendance = attendance
        self.working_schedule = working_schedule
        self.overtime = overtime
        self.leave = leave
        self.payroll = payroll
        self.work_location = work_location
        self.public_holiday = public_holiday
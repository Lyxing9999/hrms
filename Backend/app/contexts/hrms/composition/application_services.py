from __future__ import annotations

from types import SimpleNamespace

from app.contexts.hrms.composition import repositories
from app.contexts.hrms.composition.repositories import HrmsRepositories
from app.contexts.hrms.domain.payroll import PayrollCalculator

from app.contexts.hrms.use_cases.attendance.check_in_employee import CheckInEmployeeUseCase
from app.contexts.hrms.use_cases.attendance.check_out_employee import CheckOutEmployeeUseCase
from app.contexts.hrms.use_cases.attendance.approve_wrong_location import ApproveWrongLocationUseCase

from app.contexts.hrms.queries.attendance.get_my_attendance import GetMyAttendanceQuery
from app.contexts.hrms.queries.attendance.list_attendance import ListAttendanceQuery
from app.contexts.hrms.queries.attendance.get_team_attendance import GetTeamAttendanceQuery
from app.contexts.hrms.queries.attendance.get_wrong_location_report import GetWrongLocationReportQuery
from app.contexts.hrms.use_cases.employee.onboard_employee_with_account import OnboardEmployeeWithAccountUseCase
from app.contexts.hrms.use_cases.employee.create_employee import CreateEmployeeUseCase
from app.contexts.hrms.use_cases.employee.update_employee import UpdateEmployeeUseCase
from app.contexts.hrms.use_cases.employee.create_employee_account import CreateEmployeeAccountUseCase
from app.contexts.hrms.use_cases.employee.soft_delete_employee import SoftDeleteEmployeeUseCase
from app.contexts.hrms.use_cases.employee.restore_employee import RestoreEmployeeUseCase
from app.contexts.hrms.use_cases.employee.update_employee_account import UpdateEmployeeAccountUseCase
from app.contexts.hrms.use_cases.employee.assign_employee_schedule import AssignEmployeeScheduleUseCase
from app.contexts.hrms.use_cases.employee.request_employee_account_password_reset import (
    RequestEmployeeAccountPasswordResetUseCase,
)
from app.contexts.hrms.use_cases.employee.set_account_status import SetAccountStatusUseCase
from app.contexts.hrms.use_cases.employee.link_employee_account import LinkEmployeeAccountUseCase
from app.contexts.hrms.use_cases.employee.change_employee_account_password import ChangeEmployeeAccountPasswordUseCase
from app.contexts.hrms.use_cases.employee.request_employee_account_password_reset import RequestEmployeeAccountPasswordResetUseCase
from app.contexts.hrms.use_cases.employee.change_my_employee_password import ChangeMyEmployeePasswordUseCase
from app.contexts.hrms.queries.employee.list_employees import ListEmployeesQuery
from app.contexts.hrms.queries.employee.get_employee import GetEmployeeQuery
from app.contexts.hrms.queries.employee.get_my_employee_profile import GetMyEmployeeProfileQuery
from app.contexts.hrms.queries.employee.list_employees_with_accounts import ListEmployeesWithAccountsQuery
from app.contexts.hrms.queries.employee.get_employee_account import GetEmployeeAccountQuery
from app.contexts.hrms.queries.employee.list_employee_accounts import ListEmployeeAccountsQuery
from app.contexts.hrms.queries.employee.find_employee_by_user_id import FindEmployeeByUserIdQuery

from app.contexts.hrms.use_cases.working_schedule.create_working_schedule import CreateWorkingScheduleUseCase
from app.contexts.hrms.use_cases.working_schedule.update_working_schedule import UpdateWorkingScheduleUseCase
from app.contexts.hrms.use_cases.working_schedule.set_default_working_schedule import SetDefaultWorkingScheduleUseCase
from app.contexts.hrms.use_cases.working_schedule.soft_delete_working_schedule import SoftDeleteWorkingScheduleUseCase
from app.contexts.hrms.use_cases.working_schedule.restore_working_schedule import RestoreWorkingScheduleUseCase
from app.contexts.hrms.queries.working_schedule.list_working_schedules import ListWorkingSchedulesQuery
from app.contexts.hrms.queries.working_schedule.get_working_schedule import GetWorkingScheduleQuery
from app.contexts.hrms.queries.working_schedule.get_default_working_schedule import GetDefaultWorkingScheduleQuery

from app.contexts.hrms.use_cases.overtime.create_overtime_request import CreateOvertimeRequestUseCase
from app.contexts.hrms.use_cases.overtime.approve_overtime_request import ApproveOvertimeRequestUseCase
from app.contexts.hrms.use_cases.overtime.reject_overtime_request import RejectOvertimeRequestUseCase
from app.contexts.hrms.use_cases.overtime.cancel_overtime_request import CancelOvertimeRequestUseCase
from app.contexts.hrms.queries.overtime.list_my_overtime_requests import ListMyOvertimeRequestsQuery
from app.contexts.hrms.queries.overtime.list_overtime_requests import ListOvertimeRequestsQuery
from app.contexts.hrms.queries.overtime.get_overtime_request import GetOvertimeRequestQuery
from app.contexts.hrms.queries.overtime.list_approved_overtime_for_payroll import ListApprovedOvertimeForPayrollQuery

from app.contexts.hrms.use_cases.leave.submit_leave_request import SubmitLeaveRequestUseCase
from app.contexts.hrms.use_cases.leave.approve_leave_request import ApproveLeaveRequestUseCase

from app.contexts.hrms.use_cases.payroll.generate_monthly_payroll import GenerateMonthlyPayrollUseCase

from app.contexts.hrms.use_cases.work_location.create_work_location import CreateWorkLocationUseCase
from app.contexts.hrms.use_cases.work_location.update_work_location import UpdateWorkLocationUseCase
from app.contexts.hrms.use_cases.work_location.activate_work_location import ActivateWorkLocationUseCase
from app.contexts.hrms.use_cases.work_location.deactivate_work_location import DeactivateWorkLocationUseCase
from app.contexts.hrms.use_cases.work_location.soft_delete_work_location import SoftDeleteWorkLocationUseCase
from app.contexts.hrms.use_cases.work_location.restore_work_location import RestoreWorkLocationUseCase
from app.contexts.hrms.queries.work_location.list_work_locations import ListWorkLocationsQuery
from app.contexts.hrms.queries.work_location.get_work_location import GetWorkLocationQuery
from app.contexts.hrms.queries.work_location.get_active_work_location import GetActiveWorkLocationQuery

from app.contexts.hrms.use_cases.public_holiday.create_public_holiday import CreatePublicHolidayUseCase
from app.contexts.hrms.use_cases.public_holiday.update_public_holiday import UpdatePublicHolidayUseCase
from app.contexts.hrms.use_cases.public_holiday.soft_delete_public_holiday import SoftDeletePublicHolidayUseCase
from app.contexts.hrms.use_cases.public_holiday.restore_public_holiday import RestorePublicHolidayUseCase
from app.contexts.hrms.queries.public_holiday.list_public_holidays import ListPublicHolidaysQuery
from app.contexts.hrms.queries.public_holiday.get_public_holiday import GetPublicHolidayQuery
from app.contexts.hrms.queries.public_holiday.check_public_holiday_by_date import CheckPublicHolidayByDateQuery
from app.contexts.hrms.use_cases.public_holiday.import_default_public_holidays import ImportDefaultPublicHolidaysUseCase


class HrmsApplicationServices:
    def __init__(self, *, repositories: HrmsRepositories) -> None:
        self.repositories = repositories

        # employee account / employee
        self.get_account = GetEmployeeAccountQuery(
            employee_repository=repositories.employee_repository,
            iam_gateway=repositories.iam_gateway,
        )
        self.find_employee_by_user_id = FindEmployeeByUserIdQuery(
            employee_repository=repositories.employee_repository,
        )
        self.set_account_status = SetAccountStatusUseCase(
            iam_gateway=repositories.iam_gateway,
        )
        self.update_employee_account = UpdateEmployeeAccountUseCase(
            employee_repository=repositories.employee_repository,
            iam_gateway=repositories.iam_gateway,
        )
        self.request_employee_account_password_reset = RequestEmployeeAccountPasswordResetUseCase(
            employee_repository=repositories.employee_repository,
            iam_gateway=repositories.iam_gateway,
        )
        self.list_employee_accounts = ListEmployeeAccountsQuery(
            iam_gateway=repositories.iam_gateway,
        )
        self.link_employee_account = LinkEmployeeAccountUseCase(
            employee_repository=repositories.employee_repository,
            iam_gateway=repositories.iam_gateway,
        )

        self.change_employee_account_password = ChangeEmployeeAccountPasswordUseCase(
            employee_repository=repositories.employee_repository,
            user_management_service=repositories.iam_gateway,
        )
        self.create_employee = CreateEmployeeUseCase(
            employee_repository=repositories.employee_repository,
        )
        self.update_employee = UpdateEmployeeUseCase(
            employee_repository=repositories.employee_repository,
        )
        self.create_employee_account = CreateEmployeeAccountUseCase(
            employee_repository=repositories.employee_repository,
            iam_gateway=repositories.iam_gateway,
        )
        self.soft_delete_employee = SoftDeleteEmployeeUseCase(
            employee_repository=repositories.employee_repository,
        )
        self.restore_employee = RestoreEmployeeUseCase(
            employee_repository=repositories.employee_repository,
        )
        self.list_employees = ListEmployeesQuery(
            employee_repository=repositories.employee_repository,
        )
        self.list_employees_with_accounts = ListEmployeesWithAccountsQuery(
            employee_repository=repositories.employee_repository,
            iam_gateway=repositories.iam_gateway,
        )
        self.get_employee = GetEmployeeQuery(
            employee_repository=repositories.employee_repository,
        )
        self.get_my_employee_profile = GetMyEmployeeProfileQuery(
            employee_repository=repositories.employee_repository,
        )
        self.assign_employee_schedule = AssignEmployeeScheduleUseCase(
            employee_repository=repositories.employee_repository,
            working_schedule_repository=repositories.working_schedule_repository,
        )

        # attendance
        self.check_in_employee = CheckInEmployeeUseCase(
            employee_repository=repositories.employee_repository,
            working_schedule_repository=repositories.working_schedule_repository,
            work_location_repository=repositories.work_location_repository,
            public_holiday_repository=repositories.public_holiday_repository,
            attendance_repository=repositories.attendance_repository,
            audit_log_repository=repositories.audit_log_repository,
        )
        self.check_out_employee = CheckOutEmployeeUseCase(
            employee_repository=repositories.employee_repository,
            working_schedule_repository=repositories.working_schedule_repository,
            attendance_repository=repositories.attendance_repository,
            audit_log_repository=repositories.audit_log_repository,
        )
        self.approve_wrong_location = ApproveWrongLocationUseCase(
            attendance_repository=repositories.attendance_repository,
            audit_log_repository=repositories.audit_log_repository,
        )
        self.get_my_attendance = GetMyAttendanceQuery(
            attendance_repository=repositories.attendance_repository,
        )
        self.list_attendance = ListAttendanceQuery(
            attendance_repository=repositories.attendance_repository,
        )
        self.get_team_attendance = GetTeamAttendanceQuery(
            employee_repository=repositories.employee_repository,
            attendance_repository=repositories.attendance_repository,
        )
        self.get_wrong_location_report = GetWrongLocationReportQuery(
            attendance_repository=repositories.attendance_repository,
        )
        self.onboard_employee_with_account = OnboardEmployeeWithAccountUseCase(
            db=repositories.db,
            employee_repository=repositories.employee_repository,
            iam_gateway=repositories.iam_gateway,
        )
        # working schedule
        self.create_working_schedule = CreateWorkingScheduleUseCase(
            working_schedule_repository=repositories.working_schedule_repository,
        )
        self.update_working_schedule = UpdateWorkingScheduleUseCase(
            working_schedule_repository=repositories.working_schedule_repository,
        )
        self.set_default_working_schedule = SetDefaultWorkingScheduleUseCase(
            working_schedule_repository=repositories.working_schedule_repository,
        )
        self.soft_delete_working_schedule = SoftDeleteWorkingScheduleUseCase(
            working_schedule_repository=repositories.working_schedule_repository,
        )
        self.restore_working_schedule = RestoreWorkingScheduleUseCase(
            working_schedule_repository=repositories.working_schedule_repository,
        )
        self.list_working_schedules = ListWorkingSchedulesQuery(
            working_schedule_repository=repositories.working_schedule_repository,
        )
        self.get_working_schedule = GetWorkingScheduleQuery(
            working_schedule_repository=repositories.working_schedule_repository,
        )
        self.get_default_working_schedule = GetDefaultWorkingScheduleQuery(
            working_schedule_repository=repositories.working_schedule_repository,
        )

        # overtime
        self.create_overtime_request = CreateOvertimeRequestUseCase(
            employee_repository=repositories.employee_repository,
            working_schedule_repository=repositories.working_schedule_repository,
            public_holiday_repository=repositories.public_holiday_repository,
            overtime_repository=repositories.overtime_repository,
        )
        self.approve_overtime_request = ApproveOvertimeRequestUseCase(
            overtime_repository=repositories.overtime_repository,
        )
        self.reject_overtime_request = RejectOvertimeRequestUseCase(
            overtime_repository=repositories.overtime_repository,
        )
        self.cancel_overtime_request = CancelOvertimeRequestUseCase(
            overtime_repository=repositories.overtime_repository,
        )
        self.list_overtime_requests = ListOvertimeRequestsQuery(
            overtime_repository=repositories.overtime_repository,
        )
        self.get_overtime_request = GetOvertimeRequestQuery(
            overtime_repository=repositories.overtime_repository,
        )
        self.list_my_overtime_requests = ListMyOvertimeRequestsQuery(
            employee_repository=repositories.employee_repository,
            overtime_repository=repositories.overtime_repository,
        )
        self.list_approved_overtime_for_payroll = ListApprovedOvertimeForPayrollQuery(
            overtime_repository=repositories.overtime_repository,
        )

        # leave
        self.submit_leave_request = SubmitLeaveRequestUseCase(
            employee_repository=repositories.employee_repository,
            leave_repository=repositories.leave_repository,
            audit_log_repository=repositories.audit_log_repository,
        )
        self.approve_leave_request = ApproveLeaveRequestUseCase(
            leave_repository=repositories.leave_repository,
            audit_log_repository=repositories.audit_log_repository,
        )

        # payroll
        self.generate_monthly_payroll = GenerateMonthlyPayrollUseCase(
            employee_repository=repositories.employee_repository,
            attendance_repository=repositories.attendance_repository,
            overtime_repository=repositories.overtime_repository,
            deduction_rule_repository=repositories.deduction_rule_repository,
            payroll_run_repository=repositories.payroll_run_repository,
            payslip_repository=repositories.payslip_repository,
            audit_log_repository=repositories.audit_log_repository,
            payroll_calculator=PayrollCalculator,
        )

        # work location
        self.create_work_location = CreateWorkLocationUseCase(
            work_location_repository=repositories.work_location_repository,
        )
        self.update_work_location = UpdateWorkLocationUseCase(
            work_location_repository=repositories.work_location_repository,
        )
        self.activate_work_location = ActivateWorkLocationUseCase(
            work_location_repository=repositories.work_location_repository,
        )
        self.deactivate_work_location = DeactivateWorkLocationUseCase(
            work_location_repository=repositories.work_location_repository,
        )
        self.soft_delete_work_location = SoftDeleteWorkLocationUseCase(
            work_location_repository=repositories.work_location_repository,
        )
        self.restore_work_location = RestoreWorkLocationUseCase(
            work_location_repository=repositories.work_location_repository,
        )
        self.list_work_locations = ListWorkLocationsQuery(
            work_location_repository=repositories.work_location_repository,
        )
        self.get_work_location = GetWorkLocationQuery(
            work_location_repository=repositories.work_location_repository,
        )
        self.get_active_work_location = GetActiveWorkLocationQuery(
            work_location_repository=repositories.work_location_repository,
        )

        # public holiday
        self.create_public_holiday = CreatePublicHolidayUseCase(
            public_holiday_repository=repositories.public_holiday_repository,
        )
        self.update_public_holiday = UpdatePublicHolidayUseCase(
            public_holiday_repository=repositories.public_holiday_repository,
        )
        self.soft_delete_public_holiday = SoftDeletePublicHolidayUseCase(
            public_holiday_repository=repositories.public_holiday_repository,
        )
        self.restore_public_holiday = RestorePublicHolidayUseCase(
            public_holiday_repository=repositories.public_holiday_repository,
        )
        self.list_public_holidays = ListPublicHolidaysQuery(
            public_holiday_repository=repositories.public_holiday_repository,
        )
        self.get_public_holiday = GetPublicHolidayQuery(
            public_holiday_repository=repositories.public_holiday_repository,
        )
        self.check_public_holiday_by_date = CheckPublicHolidayByDateQuery(
            public_holiday_repository=repositories.public_holiday_repository,
        )
        self.import_default_public_holidays = ImportDefaultPublicHolidaysUseCase(
            public_holiday_repository=repositories.public_holiday_repository,
            cambodia_public_holiday_provider=repositories.cambodia_public_holiday_provider,
        )

        # grouped namespaces
        self.employee = SimpleNamespace(
            get_account=self.get_account.execute,
            create=self.create_employee.execute,
            update=self.update_employee.execute,
            create_account=self.create_employee_account.execute,
            update_account=self.update_employee_account.execute,
            change_account_password=self.change_employee_account_password.execute,
            request_account_password_reset=self.request_employee_account_password_reset.execute,
            set_account_status=self.set_account_status.execute,
            soft_delete=self.soft_delete_employee.execute,
            restore=self.restore_employee.execute,
            list=self.list_employees.execute,
            list_with_accounts=self.list_employees_with_accounts.execute,
            get=self.get_employee.execute,
            get_my_profile=self.get_my_employee_profile.execute,
            link_account=self.link_employee_account.execute,
            list_accounts=self.list_employee_accounts.execute,
            find_by_user_id=self.find_employee_by_user_id.execute,
            assign_schedule=self.assign_employee_schedule.execute,
            onboard_with_account=self.onboard_employee_with_account.execute,    
        )

        self.attendance = SimpleNamespace(
            check_in=self.check_in_employee.execute,
            check_out=self.check_out_employee.execute,
            approve_wrong_location=self.approve_wrong_location.execute,
            get_my_attendance=self.get_my_attendance.execute,
            list_attendance=self.list_attendance.execute,
            get_team_attendance=self.get_team_attendance.execute,
            get_wrong_location_report=self.get_wrong_location_report.execute,
        )

        self.working_schedule = SimpleNamespace(
            create=self.create_working_schedule.execute,
            update=self.update_working_schedule.execute,
            set_default=self.set_default_working_schedule.execute,
            soft_delete=self.soft_delete_working_schedule.execute,
            restore=self.restore_working_schedule.execute,
            list=self.list_working_schedules.execute,
            get=self.get_working_schedule.execute,
            get_default=self.get_default_working_schedule.execute,
        )

        self.overtime = SimpleNamespace(
            create=self.create_overtime_request.execute,
            approve=self.approve_overtime_request.execute,
            reject=self.reject_overtime_request.execute,
            cancel=self.cancel_overtime_request.execute,
            list=self.list_overtime_requests.execute,
            get=self.get_overtime_request.execute,
            list_my=self.list_my_overtime_requests.execute,
            list_approved_for_payroll=self.list_approved_overtime_for_payroll.execute,
        )

        self.leave = SimpleNamespace(
            submit=self.submit_leave_request.execute,
            approve=self.approve_leave_request.execute,
        )

        self.payroll = SimpleNamespace(
            generate_monthly=self.generate_monthly_payroll.execute,
        )

        self.work_location = SimpleNamespace(
            create=self.create_work_location.execute,
            update=self.update_work_location.execute,
            activate=self.activate_work_location.execute,
            deactivate=self.deactivate_work_location.execute,
            soft_delete=self.soft_delete_work_location.execute,
            restore=self.restore_work_location.execute,
            list=self.list_work_locations.execute,
            get=self.get_work_location.execute,
            get_active=self.get_active_work_location.execute,
        )

        self.public_holiday = SimpleNamespace(
            create=self.create_public_holiday.execute,
            update=self.update_public_holiday.execute,
            soft_delete=self.soft_delete_public_holiday.execute,
            restore=self.restore_public_holiday.execute,
            list=self.list_public_holidays.execute,
            get=self.get_public_holiday.execute,
            check_by_date=self.check_public_holiday_by_date.execute,
            import_defaults=self.import_default_public_holidays.execute,
        )
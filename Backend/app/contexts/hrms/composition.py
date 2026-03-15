from __future__ import annotations

from pymongo.database import Database

from app.contexts.hrms.facade import (
    EmployeeFacade,
    AttendanceFacade,
    OvertimeFacade,
    LeaveFacade,
    PayrollFacade,
    HrmsFacade,
)

# repositories
from app.contexts.hrms.repositories.employee_repository import MongoEmployeeRepository
from app.contexts.hrms.repositories.attendance_repository import MongoAttendanceRepository
from app.contexts.hrms.repositories.working_schedule_repository import MongoWorkingScheduleRepository
from app.contexts.hrms.repositories.work_location_repository import MongoWorkLocationRepository
from app.contexts.hrms.repositories.overtime_repository import MongoOvertimeRepository
from app.contexts.hrms.repositories.leave_repository import MongoLeaveRepository
from app.contexts.hrms.repositories.public_holiday_repository import MongoPublicHolidayRepository
from app.contexts.hrms.repositories.deduction_rule_repository import MongoDeductionRuleRepository
from app.contexts.hrms.repositories.payroll_repository import (
    MongoPayrollRunRepository,
    MongoPayslipRepository,
)
from app.contexts.hrms.repositories.audit_log_repository import MongoAuditLogRepository

# domain services
from app.contexts.hrms.domain.payroll import PayrollCalculator

# use cases - attendance
from app.contexts.hrms.use_cases.attendance.check_in_employee import CheckInEmployeeUseCase
from app.contexts.hrms.use_cases.attendance.check_out_employee import CheckOutEmployeeUseCase
from app.contexts.hrms.use_cases.attendance.approve_wrong_location import ApproveWrongLocationUseCase

# use cases - overtime
from app.contexts.hrms.use_cases.overtime.submit_ot_request import SubmitOtRequestUseCase
from app.contexts.hrms.use_cases.overtime.approve_ot_request import ApproveOtRequestUseCase
from app.contexts.hrms.use_cases.overtime.reject_ot_request import RejectOtRequestUseCase

# use cases - leave
from app.contexts.hrms.use_cases.leave.submit_leave_request import SubmitLeaveRequestUseCase
from app.contexts.hrms.use_cases.leave.approve_leave_request import ApproveLeaveRequestUseCase

# use cases - payroll
from app.contexts.hrms.use_cases.payroll.generate_monthly_payroll import GenerateMonthlyPayrollUseCase

#use cases - master data employee
from app.contexts.hrms.use_cases.employee.create_employee import CreateEmployeeUseCase
from app.contexts.hrms.use_cases.employee.update_employee import UpdateEmployeeUseCase
from app.contexts.hrms.use_cases.employee.create_employee_account import CreateEmployeeAccountUseCase
from app.contexts.hrms.use_cases.employee.soft_delete_employee import SoftDeleteEmployeeUseCase
from app.contexts.hrms.use_cases.employee.restore_employee import RestoreEmployeeUseCase

from app.contexts.hrms.queries.employee.list_employees import ListEmployeesQuery
from app.contexts.hrms.queries.employee.get_employee import GetEmployeeQuery
from app.contexts.hrms.queries.employee.get_my_employee_profile import GetMyEmployeeProfileQuery

# external - service 
from app.contexts.iam.services.iam_service import IAMService

class HrmsRepositories:
    def __init__(self, *, db: Database) -> None:
        self.employee_repository = MongoEmployeeRepository(db)
        self.attendance_repository = MongoAttendanceRepository(db)
        self.working_schedule_repository = MongoWorkingScheduleRepository(db)
        self.work_location_repository = MongoWorkLocationRepository(db)
        self.overtime_repository = MongoOvertimeRepository(db)
        self.leave_repository = MongoLeaveRepository(db)
        self.public_holiday_repository = MongoPublicHolidayRepository(db)
        self.deduction_rule_repository = MongoDeductionRuleRepository(db)
        self.payroll_run_repository = MongoPayrollRunRepository(db)
        self.payslip_repository = MongoPayslipRepository(db)
        self.audit_log_repository = MongoAuditLogRepository(db)
        self.iam_service = IAMService(db)


class HrmsUseCases:
    def __init__(self, *, repositories: HrmsRepositories) -> None:
        self.repositories = repositories

        # employee
        self.create_employee = CreateEmployeeUseCase(
            employee_repository=repositories.employee_repository,
        )

        self.update_employee = UpdateEmployeeUseCase(
            employee_repository=repositories.employee_repository,
        )

        self.create_employee_account = CreateEmployeeAccountUseCase(
            employee_repository=repositories.employee_repository,
            iam_service=repositories.iam_service, 
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

        self.get_employee = GetEmployeeQuery(
            employee_repository=repositories.employee_repository,
        )

        self.get_my_employee_profile = GetMyEmployeeProfileQuery(
            employee_repository=repositories.employee_repository,
        )
        # attendance
        self.check_in_employee = CheckInEmployeeUseCase(
            employee_repository=repositories.employee_repository,
            working_schedule_repository=repositories.working_schedule_repository,
            work_location_repository=repositories.work_location_repository,
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

        # overtime
        self.submit_ot_request = SubmitOtRequestUseCase(
            employee_repository=repositories.employee_repository,
            working_schedule_repository=repositories.working_schedule_repository,
            public_holiday_repository=repositories.public_holiday_repository,
            overtime_repository=repositories.overtime_repository,
            audit_log_repository=repositories.audit_log_repository,
        )

        self.approve_ot_request = ApproveOtRequestUseCase(
            overtime_repository=repositories.overtime_repository,
            audit_log_repository=repositories.audit_log_repository,
        )

        self.reject_ot_request = RejectOtRequestUseCase(
            overtime_repository=repositories.overtime_repository,
            audit_log_repository=repositories.audit_log_repository,
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
            payroll_calculator=PayrollCalculator,  # or injected instance later
        )


def build_hrms_repositories(db: Database) -> HrmsRepositories:
    return HrmsRepositories(db=db)


def build_hrms_use_cases(db: Database) -> HrmsUseCases:
    repositories = build_hrms_repositories(db)
    return HrmsUseCases(repositories=repositories)


def build_hrms_facade(db: Database) -> HrmsFacade:
    use_cases = build_hrms_use_cases(db)

    employee = EmployeeFacade(
        create_employee=use_cases.create_employee,
        update_employee=use_cases.update_employee,
        create_employee_account=use_cases.create_employee_account,
        soft_delete_employee=use_cases.soft_delete_employee,
        restore_employee=use_cases.restore_employee,
        list_employees=use_cases.list_employees,
        get_employee=use_cases.get_employee,
        get_my_employee_profile=use_cases.get_my_employee_profile,
    )

    attendance = AttendanceFacade(
        check_in_employee=use_cases.check_in_employee,
        check_out_employee=use_cases.check_out_employee,
        approve_wrong_location=use_cases.approve_wrong_location,
    )

    overtime = OvertimeFacade(
        submit_ot_request=use_cases.submit_ot_request,
        approve_ot_request=use_cases.approve_ot_request,
        reject_ot_request=use_cases.reject_ot_request,
    )

    leave = LeaveFacade(
        submit_leave_request=use_cases.submit_leave_request,
        approve_leave_request=use_cases.approve_leave_request,
    )

    payroll = PayrollFacade(
        generate_monthly_payroll=use_cases.generate_monthly_payroll,
    )

    return HrmsFacade(
        employee=employee,
        attendance=attendance,
        overtime=overtime,
        leave=leave,
        payroll=payroll,
    )
from __future__ import annotations

from pymongo.database import Database

from app.contexts.hrms.api.work_location.work_location_command import create_work_location
from app.contexts.hrms.composition.repositories import HrmsRepositories
from app.contexts.hrms.composition.application_services import HrmsApplicationServices
from app.contexts.hrms.facade import (
    EmployeeFacade,
    AttendanceFacade,
    WorkingScheduleFacade,
    OvertimeFacade,
    LeaveFacade,
    PayrollFacade,
    HrmsFacade,
    WorkLocationFacade
)

def build_hrms_repositories(db: Database) -> HrmsRepositories:
    return HrmsRepositories(db=db)


def build_hrms_application_services(db: Database) -> HrmsApplicationServices:
    repositories = build_hrms_repositories(db)
    return HrmsApplicationServices(repositories=repositories)


def build_hrms_facade(db: Database) -> HrmsFacade:
    services = build_hrms_application_services(db)

    employee = EmployeeFacade(
        get_account=services.get_account,
        create_employee=services.create_employee,
        update_employee=services.update_employee,
        create_employee_account=services.create_employee_account,
        update_employee_account=services.update_employee_account,
        request_employee_account_password_reset=services.request_employee_account_password_reset,
        set_account_status=services.set_account_status,
        soft_delete_employee=services.soft_delete_employee,
        restore_employee=services.restore_employee,
        list_employees=services.list_employees,
        list_employees_with_accounts=services.list_employees_with_accounts,
        get_employee=services.get_employee,
        get_my_employee_profile=services.get_my_employee_profile,
        link_employee_account=services.link_employee_account,
        list_employee_accounts=services.list_employee_accounts,
        find_employee_by_user_id=services.find_employee_by_user_id,
        assign_employee_schedule=services.assign_employee_schedule,
    )

    attendance = AttendanceFacade(
        check_in_employee=services.check_in_employee,
        check_out_employee=services.check_out_employee,
        approve_wrong_location=services.approve_wrong_location,
        get_my_attendance=services.get_my_attendance,
        list_attendance=services.list_attendance,
        get_team_attendance=services.get_team_attendance,
        get_wrong_location_report=services.get_wrong_location_report,
    )

    working_schedule = WorkingScheduleFacade(
        create_working_schedule=services.create_working_schedule,
        update_working_schedule=services.update_working_schedule,
        set_default_working_schedule=services.set_default_working_schedule,
        soft_delete_working_schedule=services.soft_delete_working_schedule,
        restore_working_schedule=services.restore_working_schedule,
        list_working_schedules=services.list_working_schedules,
        get_working_schedule=services.get_working_schedule,
        get_default_working_schedule=services.get_default_working_schedule,
    )

    overtime = OvertimeFacade(
        submit_ot_request=services.submit_ot_request,
        approve_ot_request=services.approve_ot_request,
        reject_ot_request=services.reject_ot_request,
    )

    leave = LeaveFacade(
        submit_leave_request=services.submit_leave_request,
        approve_leave_request=services.approve_leave_request,
    )

    payroll = PayrollFacade(
        generate_monthly_payroll=services.generate_monthly_payroll,
    )

    work_location = WorkLocationFacade(
        create_work_location=services.create_work_location,
        update_work_location=services.update_work_location,
        activate_work_location=services.activate_work_location,
        deactivate_work_location=services.deactivate_work_location,
        soft_delete_work_location=services.soft_delete_work_location,
        restore_work_location=services.restore_work_location,
        list_work_locations=services.list_work_locations,
        get_work_location=services.get_work_location,
        get_active_work_location=services.get_active_work_location,
    )

    return HrmsFacade(
        employee=employee,
        attendance=attendance,
        working_schedule=working_schedule,
        overtime=overtime,
        leave=leave,
        payroll=payroll,
        work_location=work_location,
    )

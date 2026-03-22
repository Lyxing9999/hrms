from __future__ import annotations


class EmployeeFacade:
    def __init__(
        self,
        *,
        get_account,
        create_employee,
        update_employee,
        create_employee_account,
        update_employee_account,
        request_employee_account_password_reset,
        set_account_status,
        soft_delete_employee,
        restore_employee,
        list_employees,
        list_employees_with_accounts,
        get_employee,
        get_my_employee_profile,
        link_employee_account,
        find_employee_by_user_id,
        list_employee_accounts=None,
    ) -> None:
        self._get_account = get_account
        self._create_employee = create_employee
        self._update_employee = update_employee
        self._create_employee_account = create_employee_account
        self._update_employee_account = update_employee_account
        self._request_employee_account_password_reset = request_employee_account_password_reset
        self._set_account_status = set_account_status
        self._soft_delete_employee = soft_delete_employee
        self._restore_employee = restore_employee
        self._list_employees = list_employees
        self._list_employees_with_accounts = list_employees_with_accounts
        self._get_employee = get_employee
        self._get_my_employee_profile = get_my_employee_profile
        self._link_employee_account = link_employee_account
        self._list_employee_accounts = list_employee_accounts
        self._find_employee_by_user_id = find_employee_by_user_id
    def create(self, **kwargs):
        return self._create_employee.execute(**kwargs)

    def update(self, **kwargs):
        return self._update_employee.execute(**kwargs)

    def create_account(self, **kwargs):
        return self._create_employee_account.execute(**kwargs)

    def update_account(self, **kwargs):
        return self._update_employee_account.execute(**kwargs)

    def request_account_password_reset(self, **kwargs):
        return self._request_employee_account_password_reset.execute(**kwargs)

    def get_account(self, **kwargs):
        return self._get_account.execute(**kwargs)

    def set_account_status(self, **kwargs):
        return self._set_account_status.execute(**kwargs)

    def soft_delete(self, **kwargs):
        return self._soft_delete_employee.execute(**kwargs)

    def restore(self, **kwargs):
        return self._restore_employee.execute(**kwargs)

    def link_account(self, **kwargs):
        return self._link_employee_account.execute(**kwargs)

    def list(self, **kwargs):
        return self._list_employees.execute(**kwargs)

    def list_with_accounts(self, **kwargs):
        return self._list_employees_with_accounts.execute(**kwargs)

    def list_accounts(self, **kwargs):
        if not self._list_employee_accounts:
            raise ValueError("Employee account listing is not configured")
        return self._list_employee_accounts.execute(**kwargs)

    def get(self, **kwargs):
        return self._get_employee.execute(**kwargs)

    def me(self, **kwargs):
        return self._get_my_employee_profile.execute(**kwargs)
    
    def find_by_user_id(self, **kwargs):
        return self._find_employee_by_user_id.execute(**kwargs)

class AttendanceFacade:
    def __init__(
        self,
        *,
        check_in_employee,
        check_out_employee,
        approve_wrong_location,
        get_my_attendance,
        list_attendance,
        get_team_attendance,
        get_wrong_location_report,
    ) -> None:
        self._check_in_employee = check_in_employee
        self._check_out_employee = check_out_employee
        self._approve_wrong_location = approve_wrong_location
        self._get_my_attendance = get_my_attendance
        self._list_attendance = list_attendance
        self._get_team_attendance = get_team_attendance
        self._get_wrong_location_report = get_wrong_location_report

    def check_in(self, **kwargs):
        return self._check_in_employee.execute(**kwargs)

    def check_out(self, **kwargs):
        return self._check_out_employee.execute(**kwargs)

    def approve_wrong_location(self, **kwargs):
        return self._approve_wrong_location.execute(**kwargs)

    def get_my_attendance(self, **kwargs):
        return self._get_my_attendance.execute(**kwargs)

    def list_attendance(self, **kwargs):
        return self._list_attendance.execute(**kwargs)

    def get_team_attendance(self, **kwargs):
        return self._get_team_attendance.execute(**kwargs)

    def get_wrong_location_report(self, **kwargs):
        return self._get_wrong_location_report.execute(**kwargs)

class WorkingScheduleFacade:
    def __init__(
        self,
        *,
        create_working_schedule,
        update_working_schedule,
        set_default_working_schedule,
        soft_delete_working_schedule,
        list_working_schedules,
        get_working_schedule,
        get_default_working_schedule,
    ) -> None:
        self._create_working_schedule = create_working_schedule
        self._update_working_schedule = update_working_schedule
        self._set_default_working_schedule = set_default_working_schedule
        self._soft_delete_working_schedule = soft_delete_working_schedule
        self._list_working_schedules = list_working_schedules
        self._get_working_schedule = get_working_schedule
        self._get_default_working_schedule = get_default_working_schedule

    def create(self, **kwargs):
        return self._create_working_schedule.execute(**kwargs)

    def update(self, **kwargs):
        return self._update_working_schedule.execute(**kwargs)

    def set_default(self, **kwargs):
        return self._set_default_working_schedule.execute(**kwargs)

    def soft_delete(self, **kwargs):
        return self._soft_delete_working_schedule.execute(**kwargs)

    def list(self, **kwargs):
        return self._list_working_schedules.execute(**kwargs)

    def get(self, **kwargs):
        return self._get_working_schedule.execute(**kwargs)

    def get_default(self, **kwargs):
        return self._get_default_working_schedule.execute(**kwargs)
    
class OvertimeFacade:
    def __init__(
        self,
        *,
        submit_ot_request,
        approve_ot_request,
        reject_ot_request,
    ) -> None:
        self._submit_ot_request = submit_ot_request
        self._approve_ot_request = approve_ot_request
        self._reject_ot_request = reject_ot_request

    def submit(self, **kwargs):
        return self._submit_ot_request.execute(**kwargs)

    def approve(self, **kwargs):
        return self._approve_ot_request.execute(**kwargs)

    def reject(self, **kwargs):
        return self._reject_ot_request.execute(**kwargs)


class LeaveFacade:
    def __init__(
        self,
        *,
        submit_leave_request,
        approve_leave_request,
    ) -> None:
        self._submit_leave_request = submit_leave_request
        self._approve_leave_request = approve_leave_request

    def submit(self, **kwargs):
        return self._submit_leave_request.execute(**kwargs)

    def approve(self, **kwargs):
        return self._approve_leave_request.execute(**kwargs)


class PayrollFacade:
    def __init__(
        self,
        *,
        generate_monthly_payroll,
    ) -> None:
        self._generate_monthly_payroll = generate_monthly_payroll

    def generate(self, **kwargs):
        return self._generate_monthly_payroll.execute(**kwargs)


class HrmsFacade:
    def __init__(
        self,
        *,
        employee: EmployeeFacade,
        attendance: AttendanceFacade,
        overtime: OvertimeFacade,
        leave: LeaveFacade,
        payroll: PayrollFacade,
        working_Schedule: WorkingScheduleFacade,
    ) -> None:
        self.employee = employee
        self.attendance = attendance
        self.overtime = overtime
        self.leave = leave
        self.payroll = payroll
        self.working_Schedule = working_Schedule
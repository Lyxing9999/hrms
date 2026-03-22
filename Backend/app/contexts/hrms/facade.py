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
        list_employee_accounts=None,
    ) -> None:
        self._get_account = get_account
        self._create_employee = create_employee
        self._update_employee = update_employee
        self._create_employee_account = create_employee_account
        self._update_employee_account = update_employee_account
        self._request_employee_account_password_reset = request_employee_account_password_reset
        self._soft_delete_employee = soft_delete_employee
        self._restore_employee = restore_employee
        self._list_employees = list_employees
        self._list_employees_with_accounts = list_employees_with_accounts
        self._get_employee = get_employee
        self._get_my_employee_profile = get_my_employee_profile
        self._list_employee_accounts = list_employee_accounts
        self._set_account_status = set_account_status
        self._link_employee_account = link_employee_account

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
    
    def set_account_status(self, **kwargs):
        return self._set_account_status.execute(**kwargs)
    def get(self, **kwargs):
        return self._get_employee.execute(**kwargs)

    def me(self, **kwargs):
        return self._get_my_employee_profile.execute(**kwargs)
    
class AttendanceFacade:
    def __init__(
        self,
        *,
        check_in_employee,
        check_out_employee,
        approve_wrong_location,
    ) -> None:
        self.check_in_employee = check_in_employee
        self.check_out_employee = check_out_employee
        self.approve_wrong_location = approve_wrong_location


class OvertimeFacade:
    def __init__(
        self,
        *,
        submit_ot_request,
        approve_ot_request,
        reject_ot_request,
    ) -> None:
        self.submit_ot_request = submit_ot_request
        self.approve_ot_request = approve_ot_request
        self.reject_ot_request = reject_ot_request


class LeaveFacade:
    def __init__(
        self,
        *,
        submit_leave_request,
        approve_leave_request,
    ) -> None:
        self.submit_leave_request = submit_leave_request
        self.approve_leave_request = approve_leave_request


class PayrollFacade:
    def __init__(
        self,
        *,
        generate_monthly_payroll,
    ) -> None:
        self.generate_monthly_payroll = generate_monthly_payroll




class HrmsFacade:
    def __init__(
        self,
        *,
        employee: EmployeeFacade,
        attendance: AttendanceFacade,
        overtime: OvertimeFacade,
        leave: LeaveFacade,
        payroll: PayrollFacade,
    ) -> None:
        self.employee = employee
        self.attendance = attendance
        self.overtime = overtime
        self.leave = leave
        self.payroll = payroll
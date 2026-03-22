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
from app.contexts.hrms.domain.employee import Employee, EmploymentType
from app.contexts.hrms.errors.employee_exceptions import EmployeeCodeAlreadyExistsException


class EmployeeFactory:
    def __init__(self, employee_read_model):
        self._read = employee_read_model

    def create_employee(self, *, payload: dict, created_by: str | None) -> Employee:
        code = (payload.get("employee_code") or "").strip()
        if self._read.get_by_employee_code(code):
            raise EmployeeCodeAlreadyExistsException(code)

        return Employee(
            # domain id generated in domain or left None (depending on your Employee init)
            employee_code=code,
            full_name=(payload.get("full_name") or "").strip(),
            department=payload.get("department"),
            position=payload.get("position"),
            employment_type=payload.get("employment_type") or EmploymentType.CONTRACT.value,
            contract=payload.get("contract"),
            manager_user_id=(payload.get("manager_user_id") or None),
            schedule_id=(payload.get("schedule_id") or None),
            status=payload.get("status") or "active",
            created_by=created_by,
        )
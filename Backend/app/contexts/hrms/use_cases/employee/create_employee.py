from __future__ import annotations

from app.contexts.hrms.errors.employee_exceptions import EmployeeCodeAlreadyExistsException
from app.contexts.shared.time_utils import utc_now


class CreateEmployeeUseCase:
    def __init__(self, *, employee_repository) -> None:
        self.employee_repository = employee_repository

    def execute(self, *, payload, created_by_user_id):
        existing = self.employee_repository.find_by_employee_code(payload.employee_code)
        if existing:
            raise EmployeeCodeAlreadyExistsException(payload.employee_code)
        now = utc_now()
        doc = {
            "employee_code": payload.employee_code,
            "full_name": payload.full_name,
            "department": payload.department,
            "position": payload.position,
            "employment_type": payload.employment_type,
            "basic_salary": payload.basic_salary,
            # Use JSON mode so date fields are serialized to ISO strings.
            "contract": payload.contract.model_dump(mode="json") if payload.contract else None,
            "manager_user_id": payload.manager_user_id,
            "schedule_id": payload.schedule_id,
            "work_location_id": payload.work_location_id,          
            "status": payload.status,
            "photo_url": payload.photo_url,
            "user_id": None,
            "created_by": created_by_user_id,
            "lifecycle": {
                "created_at": now,
                "updated_at": now,
                "deleted_at": None,
                "deleted_by": None,
            },
        }



        return self.employee_repository.create(doc)
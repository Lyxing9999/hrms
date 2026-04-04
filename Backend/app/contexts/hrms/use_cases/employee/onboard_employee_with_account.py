from __future__ import annotations

from pymongo.errors import DuplicateKeyError

from app.contexts.shared.model_converter import mongo_converter
from app.contexts.hrms.errors.employee_exceptions import (
    EmployeeAccountAlreadyLinkedException,
)
from app.contexts.core.errors import AppBaseException, ErrorSeverity, ErrorCategory
from datetime import datetime, time

class OnboardEmployeeWithAccountUseCase:
    def __init__(
        self,
        *,
        db,
        employee_repository,
        iam_gateway,
    ) -> None:
        self.db = db
        self.employee_repository = employee_repository
        self.iam_gateway = iam_gateway
    def _build_employee_doc(self, employee_payload, created_by_user_id: str) -> dict:
        data = employee_payload.model_dump()

        contract = data.get("contract")
        if contract:
            if contract.get("start_date"):
                contract["start_date"] = datetime.combine(contract["start_date"], time.min)
            if contract.get("end_date"):
                contract["end_date"] = datetime.combine(contract["end_date"], time.min)

        if data.get("schedule_id"):
            data["schedule_id"] = mongo_converter.convert_to_object_id(data["schedule_id"])

        if data.get("work_location_id"):
            data["work_location_id"] = mongo_converter.convert_to_object_id(data["work_location_id"])

        if data.get("manager_user_id"):
            data["manager_user_id"] = mongo_converter.convert_to_object_id(data["manager_user_id"])

        data["user_id"] = None
        data["created_by"] = mongo_converter.convert_to_object_id(created_by_user_id)

        return data
    def execute(
        self,
        *,
        employee_payload,
        email: str,
        password: str,
        username: str | None,
        role: str,
        created_by_user_id: str,
    ):
        client = self.db.client

        with client.start_session() as session:
            with session.start_transaction():
                try:
                    # 1. create employee first
                    employee_doc = self.employee_repository.create_with_session(
                        self._build_employee_doc(employee_payload, created_by_user_id),
                        session=session,
                    )

                    if employee_doc.get("user_id"):
                        raise EmployeeAccountAlreadyLinkedException(
                            user_id=str(employee_doc.get("user_id")),
                            linked_employee_id=str(employee_doc.get("_id")),
                        )

                    # 2. create IAM account
                    iam_user = self.iam_gateway.create_user_for_employee(
                        email=email,
                        password=password,
                        username=username,
                        role=role,
                        created_by=created_by_user_id,
                    )

                    user_id = getattr(iam_user, "id", None)
                    if not user_id:
                        raise AppBaseException(
                            message="Failed to create IAM user",
                            user_message="Unable to create account for employee.",
                            severity=ErrorSeverity.MEDIUM,
                            category=ErrorCategory.SYSTEM,
                            recoverable=True,
                            status_code=500,
                        )

                    # 3. atomic conditional link
                    linked_employee = self.employee_repository.link_user_if_empty_with_session(
                        employee_id=employee_doc["_id"],
                        user_id=user_id,
                        session=session,
                    )

                    if not linked_employee:
                        raise AppBaseException(
                            message="Employee account link failed because employee was already linked",
                            user_message="This employee already has an account linked.",
                            severity=ErrorSeverity.MEDIUM,
                            category=ErrorCategory.BUSINESS_RULE,
                            recoverable=True,
                            status_code=409,
                        )

                    return iam_user, linked_employee

                except DuplicateKeyError as e:
                    msg = str(e)

                    if "uq_employee_user_id" in msg:
                        raise AppBaseException(
                            message="User account already linked to another employee",
                            user_message="This account is already linked to another employee.",
                            severity=ErrorSeverity.MEDIUM,
                            category=ErrorCategory.BUSINESS_RULE,
                            recoverable=True,
                            status_code=409,
                        )

                    if "uq_iam_username" in msg:
                        raise AppBaseException(
                            message="Username already exists",
                            user_message="This username is already taken.",
                            severity=ErrorSeverity.LOW,
                            category=ErrorCategory.VALIDATION,
                            recoverable=True,
                            status_code=409,
                        )

                    if "uq_iam_email" in msg:
                        raise AppBaseException(
                            message="Email already exists",
                            user_message="This email is already in use.",
                            severity=ErrorSeverity.LOW,
                            category=ErrorCategory.VALIDATION,
                            recoverable=True,
                            status_code=409,
                        )

                    raise
# app/contexts/hrms/services/employee_service.py
from __future__ import annotations

from typing import Optional, List, Union
from bson import ObjectId
from pymongo.database import Database

# HRMS Context Imports
from app.contexts.hrms.read_models.employee_read_model import EmployeeReadModel
from app.contexts.hrms.repositories.employee_repository import MongoEmployeeRepository
from app.contexts.hrms.factories.employee_factory import EmployeeFactory
from app.contexts.hrms.mapper.employee_mapper import EmployeeMapper
from app.contexts.hrms.errors.employee_exceptions import EmployeeNotFoundException
from app.contexts.hrms.domain.employee import Employee

# IAM Context Imports
from app.contexts.iam.domain.iam import IAM
from app.contexts.iam.factory.iam_factory import IAMFactory
from app.contexts.iam.repositories.iam_repositorie import MongoIAMRepository
from app.contexts.iam.read_models.iam_read_model import IAMReadModel
from app.contexts.iam.mapper.iam_mapper import IAMMapper
from app.contexts.shared.enum.roles import SystemRole
from app.contexts.iam.data_transfer.response import IAMBaseDataDTO

# Notification Context Imports (New Integration)
from app.contexts.notifications.services.notification_service import NotificationService
from app.contexts.notifications.utils.recipient_resolver import NotificationRecipientResolver
from app.contexts.notifications.types import NotifType 

# Shared Imports
from app.contexts.shared.lifecycle.filters import ShowDeleted
from app.contexts.shared.model_converter import mongo_converter
from app.contexts.shared.lifecycle.domain import now_utc


class EmployeeService:
    def __init__(self, db: Database):
        self.db = db
        
        # Domain Services & Repositories
        self._read = EmployeeReadModel(db)
        self._repo = MongoEmployeeRepository(db["employees"])
        self._mapper = EmployeeMapper()
        self._factory = EmployeeFactory(self._read)

        # IAM Integration
        self._iam_read = IAMReadModel(db)
        self._iam_repo = MongoIAMRepository(db["iam"])
        self._iam_factory = IAMFactory(self._iam_read)
        self._iam_mapper = IAMMapper()

        # Notification Integration
        self._notification_service = NotificationService(db)
        self._notif_resolver = NotificationRecipientResolver(db)

    def _oid(self, v: str | ObjectId | None) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    # -------------------------
    # NOTIFICATION HELPERS (Private)
    # -------------------------
    def _notify_account_created(self, user_id: str, username: str, role: str, employee_name: str):
        """
        Notify the employee that their system account is ready.
        """
        self._notification_service.create_for_user(
            user_id=user_id,
            role=role,
            type="ACCOUNT_CREATED", # Add to NotifType Enum ideally
            title="System Account Created",
            message=f"Hello {employee_name}, your account ({username}) has been created successfully.",
            entity_type="employee",
            entity_id=None, # Or link to their profile
            data={
                "username": username,
                "role": role
            }
        )

    def _notify_manager_of_new_hire(self, manager_user_id: str, new_employee_name: str, employee_id: str):
        """
        Notify the manager when a new employee is added to their team.
        """
        if not manager_user_id:
            return

        # Ensure we have a valid user_id for the manager
        # If manager_user_id is already an IAM ID, use it directly.
        # If it might be an Employee ID, use resolver.
        target_id = self._notif_resolver.best_effort_user_id(manager_user_id)
        if not target_id:
            return

        self._notification_service.create_for_user(
            user_id=target_id,
            role="manager", # Assuming manager role
            type="NEW_TEAM_MEMBER", # Add to NotifType Enum
            title="New Team Member",
            message=f"{new_employee_name} has been added to your team.",
            entity_type="employee",
            entity_id=str(employee_id),
            data={
                "employee_id": str(employee_id),
                "name": new_employee_name
            }
        )

    # -------------------------
    # LIST (read model -> domain list + total)
    # -------------------------
    def list_employees(
        self,
        *,
        q: str = "",
        page: int = 1,
        page_size: int = 10,
        show_deleted: ShowDeleted = "active",
    ) -> tuple[list[Employee], int]:
        items, total = self._read.get_page(
            page=page,
            page_size=page_size,
            q=q,
            show_deleted=show_deleted,
        )
        domains = [self._mapper.to_domain(x) for x in items]
        return domains, int(total)

    # -------------------------
    # GET ONE
    # -------------------------
    def get_employee(self, employee_id: str | ObjectId, *, show_deleted: ShowDeleted = "active") -> Employee:
        raw = self._read.get_by_id(self._oid(employee_id), show_deleted=show_deleted)
        if not raw:
            raise EmployeeNotFoundException(str(employee_id))
        return self._mapper.to_domain(raw)

    # -------------------------
    # CREATE
    # -------------------------
    def create_employee(self, payload, *, created_by_user_id: str | ObjectId) -> Employee:
        actor_oid = self._oid(created_by_user_id)

        p = payload.model_dump()
        # Convert IDs
        if p.get("manager_user_id"):
            p["manager_user_id"] = self._oid(p["manager_user_id"])
        if p.get("schedule_id"):
            p["schedule_id"] = self._oid(p["schedule_id"])

        # 1. Create Domain Entity
        emp = self._factory.create_employee(payload=p, created_by=actor_oid)
        saved = self._repo.save(self._mapper.to_persistence(emp))
        
        # 2. Notify Manager (if assigned)
        if saved.manager_user_id:
            self._notify_manager_of_new_hire(
                manager_user_id=str(saved.manager_user_id),
                new_employee_name=saved.full_name, # Assuming full_name property exists
                employee_id=str(saved.id)
            )

        return saved

    # -------------------------
    # CREATE IAM + LINK
    # -------------------------
    def create_account_for_employee(self, employee_id: str | ObjectId, payload, *, created_by_user_id: str | ObjectId) -> Union[IAMBaseDataDTO, Employee ]:
        emp = self.get_employee(employee_id, show_deleted="active")
        if emp.user_id:
            raise ValueError("Employee already has an account linked")

        actor_oid = self._oid(created_by_user_id)

        # 1. Validate Role using Enum (Clean Way)
        try:
            role_enum = SystemRole(str(payload.role or "employee").strip().lower())
        except ValueError:
            raise ValueError(f"Invalid employee account role: {payload.role}")

        # 2. Create IAM User
        iam_domain = self._iam_factory.create_user(
            email=str(payload.email).strip().lower(),
            password=str(payload.password),
            username=payload.username,
            role=role_enum,
            created_by=str(actor_oid),
        )
        iam_saved = self._iam_repo.save(self._iam_mapper.to_persistence(iam_domain))

        # 3. Link User to Employee
        emp.link_user(iam_saved.id)
        updated = self._repo.update(self._oid(emp.id), self._mapper.to_persistence(emp))
        if not updated:
            raise EmployeeNotFoundException(str(employee_id))

        # 4. Notify the Employee (Account Created)
        self._notify_account_created(
            user_id=str(iam_saved.id),
            username=iam_saved.username,
            role=iam_saved.role.value,
            employee_name=emp.full_name 
        )

        return self._iam_mapper.to_dto(iam_domain), emp 

    # -------------------------
    # SOFT DELETE
    # -------------------------
    # -------------------------
    # UPDATE
    # -------------------------
    def update_employee(self, employee_id: str | ObjectId, payload, *, actor_id: str | ObjectId) -> Employee:
        emp = self.get_employee(employee_id, show_deleted="active")
        
        p = payload.model_dump(exclude_unset=True)
        
        # Update fields
        if "full_name" in p and p["full_name"]:
            emp.full_name = str(p["full_name"]).strip()
        if "department" in p:
            emp.department = p["department"]
        if "position" in p:
            emp.position = p["position"]
        if "employment_type" in p and p["employment_type"]:
            emp.employment_type = p["employment_type"]
        if "contract" in p:
            emp.contract = p["contract"]
        if "manager_user_id" in p:
            emp.manager_user_id = self._oid(p["manager_user_id"]) if p["manager_user_id"] else None
        if "schedule_id" in p:
            emp.schedule_id = self._oid(p["schedule_id"]) if p["schedule_id"] else None
        if "status" in p:
            emp.status = p["status"]
        
        # Validate contract rules after update
        emp._validate_contract_rules()
        emp.lifecycle.touch(now_utc())
        
        updated = self._repo.update(self._oid(emp.id), self._mapper.to_persistence(emp))
        if not updated:
            raise EmployeeNotFoundException(str(employee_id))
        
        return updated

    # -------------------------
    # SOFT DELETE
    # -------------------------
    def soft_delete_employee(self, employee_id, *, actor_id):
        emp = self.get_employee(employee_id, show_deleted="active")

        emp.soft_delete(str(actor_id))  # domain string

        payload = self._mapper.to_persistence(emp)  # dict
        updated = self._repo.update(self._oid(emp.id), payload)

        if not updated:
            raise EmployeeNotFoundException(str(employee_id))

        if isinstance(updated, Employee):
            return updated  # ✅ already domain, do not map again

        return EmployeeMapper.to_domain(updated)

    # -------------------------
    # RESTORE
    # -------------------------
    def restore_employee(self, employee_id: str | ObjectId) -> Employee:
        emp = self.get_employee(employee_id, show_deleted="deleted_only")
        
        emp.lifecycle.restore()
        
        updated = self._repo.update(self._oid(emp.id), self._mapper.to_persistence(emp))
        if not updated:
            raise EmployeeNotFoundException(str(employee_id))
        
        return updated 


    def set_employee_photo(self, employee_id: str, *, photo_url: str) -> Employee:
        emp = self.get_employee(employee_id, show_deleted="active")
        emp.photo_url = str(photo_url)

        payload = EmployeeMapper.to_persistence(emp)  
        updated = self._repo.update(self._oid(emp.id), payload)

        if not updated:
            raise EmployeeNotFoundException(str(employee_id))

        if isinstance(updated, dict):
            return EmployeeMapper.to_domain(updated)  
        if isinstance(updated, Employee):
            return updated

        raise TypeError(f"Unexpected update() return type: {type(updated)}")
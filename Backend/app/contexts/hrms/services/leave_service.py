# app/contexts/hrms/services/leave_service.py
from __future__ import annotations
from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.read_models.employee_read_model import EmployeeReadModel
from app.contexts.hrms.read_models.leave_read_model import LeaveReadModel
from app.contexts.hrms.repositories.leave_repository import MongoLeaveRepository
from app.contexts.hrms.mapper.leave_mapper import LeaveMapper
from app.contexts.hrms.factories.leave_factory import LeaveFactory
from app.contexts.hrms.errors.leave_exceptions import LeaveNotFoundException
from app.contexts.hrms.policies.leave_policy import LeavePolicy
from app.contexts.hrms.domain.leave import LeaveRequest
from app.contexts.shared.lifecycle.filters import ShowDeleted
from app.contexts.shared.lifecycle.domain import now_utc

# Notification Integration
from app.contexts.notifications.services.notification_service import NotificationService
from app.contexts.notifications.utils.recipient_resolver import NotificationRecipientResolver

class LeaveService:
    def __init__(self, db: Database):
        self.db = db
        self._employee_read = EmployeeReadModel(db)
        self._leave_read = LeaveReadModel(db)
        self._repo = MongoLeaveRepository(db["leave_requests"])
        self._mapper = LeaveMapper()
        self._policy = LeavePolicy(db)

        # if you store leave_policies in db:
        self._leave_policy_read = db["leave_policies"]
        self._factory = LeaveFactory(self._employee_read, leave_policy_read_model=_LeavePolicyReadModelAdapter(self._leave_policy_read))
        
        # Notification Integration
        self._notification_service = NotificationService(db)
        self._notif_resolver = NotificationRecipientResolver(db)

    def _oid(self, v: str | ObjectId | None) -> ObjectId | None:
        if v is None:
            return None
        return v if isinstance(v, ObjectId) else ObjectId(str(v))

    # -------------------------
    # NOTIFICATION HELPERS
    # -------------------------
    def _notify_leave_submitted(self, leave: LeaveRequest, employee_name: str):
        """Notify manager when employee submits leave request"""
        if not leave.manager_user_id:
            return
        
        self._notification_service.create_for_user(
            user_id=str(leave.manager_user_id),
            role="manager",
            type="LEAVE_SUBMITTED",
            title="New Leave Request",
            message=f"{employee_name} has submitted a leave request for {leave.total_days()} days.",
            entity_type="leave",
            entity_id=str(leave.id),
            data={
                "leave_id": str(leave.id),
                "employee_name": employee_name,
                "start_date": leave.start_date.isoformat(),
                "end_date": leave.end_date.isoformat(),
                "total_days": leave.total_days()
            }
        )

    def _notify_leave_reviewed(self, leave: LeaveRequest, employee_user_id: str, status: str):
        """Notify employee when their leave is approved/rejected"""
        self._notification_service.create_for_user(
            user_id=employee_user_id,
            role="employee",
            type=f"LEAVE_{status.upper()}",
            title=f"Leave Request {status.title()}",
            message=f"Your leave request has been {status}.",
            entity_type="leave",
            entity_id=str(leave.id),
            data={
                "leave_id": str(leave.id),
                "status": status,
                "manager_comment": leave.manager_comment
            }
        )

    # -------------------------
    # LIST
    # -------------------------
    def list_leaves(
        self,
        *,
        q: str = "",
        page: int = 1,
        page_size: int = 10,
        employee_id: str | None = None,
        status: str | None = None,
        show_deleted: ShowDeleted = "active",
    ) -> tuple[list[LeaveRequest], int]:
        items, total = self._leave_read.get_page(
            page=page,
            page_size=page_size,
            q=q,
            employee_id=employee_id,
            status=status,
            show_deleted=show_deleted,
        )
        domains = [self._mapper.to_domain(x) for x in items]
        return domains, int(total)

    # -------------------------
    # GET ONE
    # -------------------------
    def get_leave(self, leave_id: str | ObjectId, *, show_deleted: ShowDeleted = "active") -> LeaveRequest:
        raw = self._leave_read.get_by_id(self._oid(leave_id), show_deleted=show_deleted)
        if not raw:
            raise LeaveNotFoundException(str(leave_id))
        return self._mapper.to_domain(raw)

    # -------------------------
    # CREATE (Employee submits contract leave)
    # -------------------------
    def submit_contract_leave(self, employee_id: str, payload):
        leave = self._factory.create_contract_leave(
            employee_id=employee_id,
            leave_type=payload.leave_type,
            start_date=payload.start_date,
            end_date=payload.end_date,
            reason=payload.reason,
        )
        saved = self._repo.save(self._mapper.to_persistence(leave))
        
        # Notify manager
        emp_raw = self._employee_read.get_by_id(self._oid(employee_id))
        if emp_raw:
            self._notify_leave_submitted(saved, emp_raw.get("full_name", "Employee"))
        
        return self._mapper.to_dto(saved)

    # -------------------------
    # UPDATE (before review)
    # -------------------------
    def update_leave(self, leave_id: str | ObjectId, payload, *, actor_id: str | ObjectId) -> LeaveRequest:
        leave = self.get_leave(leave_id, show_deleted="active")
        
        # Only allow updates if still pending
        if leave.status.value != "pending":
            raise ValueError(f"Cannot update leave request with status: {leave.status.value}")
        
        p = payload.model_dump(exclude_unset=True)
        
        if "start_date" in p:
            leave.start_date = p["start_date"]
        if "end_date" in p:
            leave.end_date = p["end_date"]
        if "reason" in p:
            leave.reason = str(p["reason"]).strip()
        if "leave_type" in p:
            from app.contexts.hrms.domain.leave import LeaveType
            leave.leave_type = LeaveType(str(p["leave_type"]).strip().lower())
        
        # Validate dates
        if leave.end_date < leave.start_date:
            from app.contexts.hrms.errors.leave_exceptions import LeaveDateRangeInvalidException
            raise LeaveDateRangeInvalidException(leave.start_date, leave.end_date)
        
        leave.lifecycle.touch(now_utc())
        
        updated = self._repo.update(leave.id, self._mapper.to_persistence(leave))
        if not updated:
            raise LeaveNotFoundException(str(leave_id))
        
        return updated

    # -------------------------
    # APPROVE
    # -------------------------
    def approve_leave(self, leave_id: str, manager_user_id: str, comment: str | None = None):
        leave_oid = self._oid(leave_id)
        mgr_oid = self._oid(manager_user_id)

        can = self._policy.can_manager_review(mgr_oid, leave_oid)
        if not can.allowed:
            raise PermissionError(can.reasons)

        raw = self._leave_read.get_by_id(leave_oid)
        if not raw:
            raise LeaveNotFoundException(leave_id)

        domain = self._mapper.to_domain(raw)
        domain.approve(manager_id=mgr_oid, comment=comment)

        updated = self._repo.update(domain.id, self._mapper.to_persistence(domain))
        if not updated:
            raise LeaveNotFoundException(leave_id)

        # Notify employee
        emp_raw = self._employee_read.get_by_id(domain.employee_id)
        if emp_raw and emp_raw.get("user_id"):
            self._notify_leave_reviewed(updated, str(emp_raw["user_id"]), "approved")

        return self._mapper.to_dto(updated)

    # -------------------------
    # REJECT
    # -------------------------
    def reject_leave(self, leave_id: str, manager_user_id: str, comment: str | None = None):
        leave_oid = self._oid(leave_id)
        mgr_oid = self._oid(manager_user_id)

        can = self._policy.can_manager_review(mgr_oid, leave_oid)
        if not can.allowed:
            raise PermissionError(can.reasons)

        raw = self._leave_read.get_by_id(leave_oid)
        if not raw:
            raise LeaveNotFoundException(leave_id)

        domain = self._mapper.to_domain(raw)
        domain.reject(manager_id=mgr_oid, comment=comment)

        updated = self._repo.update(domain.id, self._mapper.to_persistence(domain))
        if not updated:
            raise LeaveNotFoundException(leave_id)

        # Notify employee
        emp_raw = self._employee_read.get_by_id(domain.employee_id)
        if emp_raw and emp_raw.get("user_id"):
            self._notify_leave_reviewed(updated, str(emp_raw["user_id"]), "rejected")

        return self._mapper.to_dto(updated)

    # -------------------------
    # CANCEL (by employee)
    # -------------------------
    def cancel_leave(self, leave_id: str | ObjectId, *, actor_id: str | ObjectId) -> LeaveRequest:
        leave = self.get_leave(leave_id, show_deleted="active")
        
        leave.cancel(actor_id=self._oid(actor_id))
        
        updated = self._repo.update(leave.id, self._mapper.to_persistence(leave))
        if not updated:
            raise LeaveNotFoundException(str(leave_id))
        
        return updated

    # -------------------------
    # SOFT DELETE
    # -------------------------
    def soft_delete_leave(self, leave_id: str | ObjectId, *, actor_id: str | ObjectId) -> LeaveRequest:
        leave = self.get_leave(leave_id, show_deleted="active")
        
        leave.lifecycle.soft_delete(actor_id=str(actor_id))
        
        updated = self._repo.update(leave.id, self._mapper.to_persistence(leave))
        if not updated:
            raise LeaveNotFoundException(str(leave_id))
        
        return updated

    # -------------------------
    # RESTORE
    # -------------------------
    def restore_leave(self, leave_id: str | ObjectId) -> LeaveRequest:
        leave = self.get_leave(leave_id, show_deleted="deleted_only")
        
        leave.lifecycle.restore()
        
        updated = self._repo.update(leave.id, self._mapper.to_persistence(leave))
        if not updated:
            raise LeaveNotFoundException(str(leave_id))
        
        return updated


class _LeavePolicyReadModelAdapter:
    def __init__(self, collection):
        self.collection = collection

    def get_by_id(self, oid):
        return self.collection.find_one({"_id": oid, "lifecycle.deleted_at": None})
# app/contexts/hrms/services/leave_lifecycle_service.py
from bson import ObjectId
from pymongo.database import Database
from pymongo.results import UpdateResult, DeleteResult

from app.contexts.shared.lifecycle.types import apply_soft_delete_update, apply_restore_update
from app.contexts.hrms.errors.leave_exceptions import LeaveNotFoundException

LIFECYCLE_NOT_DELETED = {"lifecycle.deleted_at": None}
LIFECYCLE_DELETED = {"lifecycle.deleted_at": {"$ne": None}}

class LeaveLifecycleService:
    def __init__(self, db: Database):
        self.collection = db["leave_requests"]

    def soft_delete(self, leave_id: ObjectId, actor_id: ObjectId) -> UpdateResult:
        res = self.collection.update_one(
            {"_id": leave_id, **LIFECYCLE_NOT_DELETED},
            apply_soft_delete_update(actor_id),
        )
        if res.matched_count == 0:
            raise LeaveNotFoundException(str(leave_id))
        return res

    def restore(self, leave_id: ObjectId, actor_id: ObjectId) -> UpdateResult:
        res = self.collection.update_one(
            {"_id": leave_id, **LIFECYCLE_DELETED},
            apply_restore_update(actor_id),
        )
        if res.matched_count == 0:
            raise LeaveNotFoundException(str(leave_id))
        return res

    def hard_delete(self, leave_id: ObjectId) -> DeleteResult:
        res = self.collection.delete_one({"_id": leave_id, **LIFECYCLE_DELETED})
        if res.deleted_count == 0:
            raise LeaveNotFoundException(str(leave_id))
        return res
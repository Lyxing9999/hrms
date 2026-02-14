from bson import ObjectId
from pymongo.database import Database
from app.contexts.shared.lifecycle.policy_result import PolicyResult

class LeavePolicy:
    """
    Example rules:
      - employee can only cancel own pending leave
      - manager can only approve team (employee.manager_user_id == manager_user_id)
    """

    def __init__(self, db: Database):
        self.employees = db["employees"]
        self.leaves = db["leave_requests"]

    def can_manager_review(self, manager_user_id: ObjectId, leave_id: ObjectId) -> PolicyResult:
        leave = self.leaves.find_one({"_id": leave_id, "lifecycle.deleted_at": None}, {"employee_id": 1})
        if not leave:
            return PolicyResult.deny("review", {"leave": "not_found_or_deleted"})

        emp = self.employees.find_one({"_id": leave["employee_id"]}, {"manager_user_id": 1})
        if not emp or emp.get("manager_user_id") != manager_user_id:
            return PolicyResult.deny("review", {"manager": "not_owner"})

        return PolicyResult.ok("review")
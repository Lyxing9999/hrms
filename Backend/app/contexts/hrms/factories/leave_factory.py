# app/contexts/hrms/factories/leave_factory.py
from datetime import date as date_type
from bson import ObjectId
from app.contexts.hrms.domain.leave import LeaveRequest, LeaveType
from app.contexts.shared.model_converter import mongo_converter

class LeaveFactory:
    def __init__(self, employee_read_model, leave_policy_read_model):
        self.employee_read_model = employee_read_model
        self.leave_policy_read_model = leave_policy_read_model

    def _oid(self, v):
        return mongo_converter.convert_to_object_id(v)

    def create_contract_leave(
        self,
        *,
        employee_id: str | ObjectId,
        leave_type: str,
        start_date: date_type,
        end_date: date_type,
        reason: str,
    ) -> LeaveRequest:
        emp_oid = self._oid(employee_id)
        emp = self.employee_read_model.get_by_id(emp_oid)
        if not emp:
            raise ValueError(f"Employee not found: {emp_oid}")

        contract = emp.get("contract") or {}
        cstart = date_type.fromisoformat(contract["start_date"])
        cend = date_type.fromisoformat(contract["end_date"])

        policy_id = contract.get("leave_policy_id")
        policy = self.leave_policy_read_model.get_by_id(self._oid(policy_id)) if policy_id else None
        rules = (policy or {}).get("rules", {})

        lt = LeaveType(str(leave_type).strip().lower())
        is_paid = False
        if lt == LeaveType.ANNUAL:
            is_paid = bool(rules.get("annual_leave_paid", False))
        elif lt == LeaveType.SICK:
            is_paid = bool(rules.get("sick_leave_paid", False))
        elif lt == LeaveType.UNPAID:
            is_paid = False

        return LeaveRequest(
            employee_id=emp_oid,
            leave_type=lt,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            contract_start=cstart,
            contract_end=cend,
            is_paid=is_paid,
        )
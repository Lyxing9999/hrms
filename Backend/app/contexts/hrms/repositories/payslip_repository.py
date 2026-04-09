from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.payroll import Payslip
from app.contexts.hrms.mapper.payroll_mapper import PayrollMapper


class MongoPayslipRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_payslips"]
        self.mapper = PayrollMapper()

    @staticmethod
    def _oid(v):
        if isinstance(v, ObjectId):
            return v
        return ObjectId(v)

    def save(self, payslip: Payslip) -> Payslip:
        doc = self.mapper.payslip_to_persistence(payslip)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return self.find_by_id(doc["_id"])

    def find_by_id(self, payslip_id) -> Payslip:
        doc = self.collection.find_one({"_id": self._oid(payslip_id)})
        if not doc:
            raise ValueError("Payslip not found")
        return self.mapper.payslip_to_domain(doc)

    def find_by_run_and_employee(self, *, payroll_run_id, employee_id) -> Payslip | None:
        doc = self.collection.find_one({
            "payroll_run_id": self._oid(payroll_run_id),
            "employee_id": self._oid(employee_id),
            "lifecycle.deleted_at": None,
        })
        return self.mapper.payslip_to_domain(doc) if doc else None

    def list_payslips(
        self,
        *,
        payroll_run_id=None,
        employee_id=None,
        month: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):
        query = {"lifecycle.deleted_at": None}
        if payroll_run_id:
            query["payroll_run_id"] = self._oid(payroll_run_id)
        if employee_id:
            query["employee_id"] = self._oid(employee_id)
        if month:
            query["month"] = month

        total = self.collection.count_documents(query)
        skip = (page - 1) * page_size

        docs = list(
            self.collection.find(query)
            .sort([("month", -1), ("employee_id", 1)])
            .skip(skip)
            .limit(page_size)
        )
        return [self.mapper.payslip_to_domain(x) for x in docs], total
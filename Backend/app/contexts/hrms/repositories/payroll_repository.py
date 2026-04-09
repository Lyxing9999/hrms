from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.payroll import PayrollRun
from app.contexts.hrms.mapper.payroll_mapper import PayrollMapper


class MongoPayrollRunRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_payroll_runs"]
        self.mapper = PayrollMapper()

    @staticmethod
    def _oid(v):
        if isinstance(v, ObjectId):
            return v
        return ObjectId(v)

    def save(self, run: PayrollRun) -> PayrollRun:
        doc = self.mapper.payroll_run_to_persistence(run)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return self.find_by_id(doc["_id"])

    def find_by_id(self, run_id) -> PayrollRun:
        doc = self.collection.find_one({"_id": self._oid(run_id)})
        if not doc:
            raise ValueError("Payroll run not found")
        return self.mapper.payroll_run_to_domain(doc)

    def find_by_month(self, month: str) -> PayrollRun | None:
        doc = self.collection.find_one({
            "month": month,
            "lifecycle.deleted_at": None,
        })
        return self.mapper.payroll_run_to_domain(doc) if doc else None

    def list_runs(self, *, page: int = 1, page_size: int = 10):
        query = {"lifecycle.deleted_at": None}
        total = self.collection.count_documents(query)
        skip = (page - 1) * page_size
        docs = list(
            self.collection.find(query)
            .sort("month", -1)
            .skip(skip)
            .limit(page_size)
        )
        return [self.mapper.payroll_run_to_domain(x) for x in docs], total
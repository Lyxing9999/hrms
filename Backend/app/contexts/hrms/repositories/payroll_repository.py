from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.payroll import PayrollRun, Payslip
from app.contexts.hrms.mapper.payroll_mapper import PayrollRunMapper, PayslipMapper
from app.contexts.hrms.errors.payroll_exceptions import (
    PayrollRunNotFoundException,
    PayslipNotFoundException,
)


class MongoPayrollRunRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_payroll_runs"]
        self.mapper = PayrollRunMapper()

    def save(self, payroll_run: PayrollRun) -> PayrollRun:
        doc = self.mapper.to_persistence(payroll_run)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return payroll_run

    def find_by_id(self, payroll_run_id: ObjectId) -> PayrollRun:
        doc = self.collection.find_one({"_id": payroll_run_id})
        if not doc:
            raise PayrollRunNotFoundException(payroll_run_id)
        return self.mapper.to_domain(doc)

    def find_by_month(self, month: str) -> PayrollRun | None:
        doc = self.collection.find_one({
            "month": month,
            "lifecycle.deleted_at": None,
        })
        return self.mapper.to_domain(doc) if doc else None

    def list_runs(
        self,
        *,
        status: str | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[PayrollRun], int]:
        query = {"lifecycle.deleted_at": None}
        if status:
            query["status"] = status

        total = self.collection.count_documents(query)
        skip = (page - 1) * limit

        docs = (
            self.collection.find(query)
            .sort("month", -1)
            .skip(skip)
            .limit(limit)
        )

        return [self.mapper.to_domain(doc) for doc in docs], total

    def delete(self, payroll_run_id: ObjectId) -> None:
        self.collection.delete_one({"_id": payroll_run_id})


class MongoPayslipRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_payslips"]
        self.mapper = PayslipMapper()

    def save(self, payslip: Payslip) -> Payslip:
        doc = self.mapper.to_persistence(payslip)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return payslip

    def find_by_id(self, payslip_id: ObjectId) -> Payslip:
        doc = self.collection.find_one({"_id": payslip_id})
        if not doc:
            raise PayslipNotFoundException(payslip_id)
        return self.mapper.to_domain(doc)

    def list_payslips(
        self,
        *,
        employee_id: ObjectId | None = None,
        payroll_run_id: ObjectId | None = None,
        month: str | None = None,
        status: str | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[Payslip], int]:
        query = {"lifecycle.deleted_at": None}

        if employee_id:
            query["employee_id"] = employee_id
        if payroll_run_id:
            query["payroll_run_id"] = payroll_run_id
        if month:
            query["month"] = month
        if status:
            query["status"] = status

        total = self.collection.count_documents(query)
        skip = (page - 1) * limit

        docs = (
            self.collection.find(query)
            .sort("month", -1)
            .skip(skip)
            .limit(limit)
        )

        return [self.mapper.to_domain(doc) for doc in docs], total

    def find_by_employee_and_month(self, *, employee_id: ObjectId, month: str) -> Payslip | None:
        doc = self.collection.find_one({
            "employee_id": employee_id,
            "month": month,
            "lifecycle.deleted_at": None,
        })
        return self.mapper.to_domain(doc) if doc else None

    def delete(self, payslip_id: ObjectId) -> None:
        self.collection.delete_one({"_id": payslip_id})
from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.payroll import PayrollRun, Payslip
from app.contexts.hrms.data_transfer.response.payroll_response import PayrollRunDTO, PayslipDTO
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.shared.model_converter import mongo_converter


class PayrollMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        if v is None:
            return None
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and v.strip().lower() in {"", "null", "none", "undefined"}:
            return None
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def _lifecycle(data: dict) -> Lifecycle:
        lc_src = data.get("lifecycle") or {}
        return Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

    @staticmethod
    def payroll_run_to_domain(data: dict | PayrollRun) -> PayrollRun:
        if isinstance(data, PayrollRun):
            return data

        return PayrollRun(
            id=PayrollMapper._oid(data.get("_id") or data.get("id")),
            month=data.get("month"),
            generated_by=PayrollMapper._oid(data.get("generated_by")),
            status=data.get("status"),
            lifecycle=PayrollMapper._lifecycle(data),
        )

    @staticmethod
    def payroll_run_to_persistence(run: PayrollRun) -> dict:
        lc = run.lifecycle
        doc = {
            "month": run.month,
            "generated_by": PayrollMapper._oid(run.generated_by),
            "status": run.status.value if hasattr(run.status, "value") else str(run.status),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": PayrollMapper._oid(lc.deleted_by),
            },
        }
        if run.id:
            doc["_id"] = PayrollMapper._oid(run.id)
        return doc

    @staticmethod
    def payroll_run_to_dto(data: PayrollRun | dict) -> PayrollRunDTO:
        run = PayrollMapper.payroll_run_to_domain(data)
        lc = run.lifecycle
        return PayrollRunDTO(
            id=str(run.id),
            month=run.month,
            generated_by=PayrollMapper._sid(run.generated_by),
            status=run.status.value if hasattr(run.status, "value") else str(run.status),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=PayrollMapper._sid(lc.deleted_by),
            ),
        )

    @staticmethod
    def payslip_to_domain(data: dict | Payslip) -> Payslip:
        if isinstance(data, Payslip):
            return data

        return Payslip(
            id=PayrollMapper._oid(data.get("_id") or data.get("id")),
            payroll_run_id=PayrollMapper._oid(data.get("payroll_run_id")),
            employee_id=PayrollMapper._oid(data.get("employee_id")),
            month=data.get("month"),
            base_salary=float(data.get("base_salary", 0)),
            payable_working_days=int(data.get("payable_working_days", 0)),
            paid_holiday_days=int(data.get("paid_holiday_days", 0)),
            unpaid_leave_days=int(data.get("unpaid_leave_days", 0)),
            total_ot_hours=float(data.get("total_ot_hours", 0)),
            ot_payment=float(data.get("ot_payment", 0)),
            total_deductions=float(data.get("total_deductions", 0)),
            net_salary=float(data.get("net_salary", 0)),
            status=data.get("status"),
            lifecycle=PayrollMapper._lifecycle(data),
        )

    @staticmethod
    def payslip_to_persistence(payslip: Payslip) -> dict:
        lc = payslip.lifecycle
        doc = {
            "payroll_run_id": PayrollMapper._oid(payslip.payroll_run_id),
            "employee_id": PayrollMapper._oid(payslip.employee_id),
            "month": payslip.month,
            "base_salary": payslip.base_salary,
            "payable_working_days": payslip.payable_working_days,
            "paid_holiday_days": payslip.paid_holiday_days,
            "unpaid_leave_days": payslip.unpaid_leave_days,
            "total_ot_hours": payslip.total_ot_hours,
            "ot_payment": payslip.ot_payment,
            "total_deductions": payslip.total_deductions,
            "net_salary": payslip.net_salary,
            "status": payslip.status.value if hasattr(payslip.status, "value") else str(payslip.status),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": PayrollMapper._oid(lc.deleted_by),
            },
        }
        if payslip.id:
            doc["_id"] = PayrollMapper._oid(payslip.id)
        return doc

    @staticmethod
    def payslip_to_dto(data: Payslip | dict) -> PayslipDTO:
        payslip = PayrollMapper.payslip_to_domain(data)
        lc = payslip.lifecycle
        return PayslipDTO(
            id=str(payslip.id),
            payroll_run_id=PayrollMapper._sid(payslip.payroll_run_id),
            employee_id=PayrollMapper._sid(payslip.employee_id),
            month=payslip.month,
            base_salary=payslip.base_salary,
            payable_working_days=payslip.payable_working_days,
            paid_holiday_days=payslip.paid_holiday_days,
            unpaid_leave_days=payslip.unpaid_leave_days,
            total_ot_hours=payslip.total_ot_hours,
            ot_payment=payslip.ot_payment,
            total_deductions=payslip.total_deductions,
            net_salary=payslip.net_salary,
            status=payslip.status.value if hasattr(payslip.status, "value") else str(payslip.status),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=PayrollMapper._sid(lc.deleted_by),
            ),
        )
from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.payroll import PayrollRun, Payslip
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.payroll_response import PayrollRunDTO, PayslipDTO
from app.contexts.shared.model_converter import mongo_converter


class PayrollRunMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def to_domain(data: dict) -> PayrollRun:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return PayrollRun(
            id=PayrollRunMapper._oid(data.get("_id") or data.get("id")),
            month=data.get("month") or "",
            generated_by=PayrollRunMapper._oid(data.get("generated_by")),
            status=data.get("status", "draft"),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(payroll_run: PayrollRun) -> dict:
        if not isinstance(payroll_run, PayrollRun):
            raise TypeError(f"to_persistence expected PayrollRun, got {type(payroll_run)}")

        lc = payroll_run.lifecycle
        doc = {
            "month": payroll_run.month,
            "generated_by": PayrollRunMapper._oid(payroll_run.generated_by),
            "status": payroll_run.status.value if hasattr(payroll_run.status, "value") else str(payroll_run.status),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": PayrollRunMapper._oid(lc.deleted_by),
            },
        }

        if payroll_run.id:
            doc["_id"] = PayrollRunMapper._oid(payroll_run.id)

        return doc

    @staticmethod
    def to_dto(payroll_run: PayrollRun) -> PayrollRunDTO:
        lc = payroll_run.lifecycle
        return PayrollRunDTO(
            id=str(payroll_run.id),
            month=payroll_run.month,
            generated_by=PayrollRunMapper._sid(payroll_run.generated_by),
            status=payroll_run.status.value if hasattr(payroll_run.status, "value") else str(payroll_run.status),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=lc.deleted_by,
            ),
        )


class PayslipMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def to_domain(data: dict) -> Payslip:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return Payslip(
            id=PayslipMapper._oid(data.get("_id") or data.get("id")),
            payroll_run_id=PayslipMapper._oid(data.get("payroll_run_id")),
            employee_id=PayslipMapper._oid(data.get("employee_id")),
            month=data.get("month") or "",
            base_salary=float(data.get("base_salary", 0)),
            payable_working_days=int(data.get("payable_working_days", 0)),
            paid_holiday_days=int(data.get("paid_holiday_days", 0)),
            unpaid_leave_days=int(data.get("unpaid_leave_days", 0)),
            total_ot_hours=float(data.get("total_ot_hours", 0)),
            ot_payment=float(data.get("ot_payment", 0)),
            total_deductions=float(data.get("total_deductions", 0)),
            net_salary=float(data.get("net_salary", 0)),
            status=data.get("status", "generated"),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(payslip: Payslip) -> dict:
        if not isinstance(payslip, Payslip):
            raise TypeError(f"to_persistence expected Payslip, got {type(payslip)}")

        lc = payslip.lifecycle
        doc = {
            "payroll_run_id": PayslipMapper._oid(payslip.payroll_run_id),
            "employee_id": PayslipMapper._oid(payslip.employee_id),
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
                "deleted_by": PayslipMapper._oid(lc.deleted_by),
            },
        }

        if payslip.id:
            doc["_id"] = PayslipMapper._oid(payslip.id)

        return doc

    @staticmethod
    def to_dto(payslip: Payslip) -> PayslipDTO:
        lc = payslip.lifecycle
        return PayslipDTO(
            id=str(payslip.id),
            payroll_run_id=PayslipMapper._sid(payslip.payroll_run_id),
            employee_id=PayslipMapper._sid(payslip.employee_id),
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
                deleted_by=lc.deleted_by,
            ),
        )
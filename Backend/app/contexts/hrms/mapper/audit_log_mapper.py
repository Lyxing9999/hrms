from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.audit_log import AuditLog
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.audit_log_response import AuditLogDTO
from app.contexts.shared.model_converter import mongo_converter


class AuditLogMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def to_domain(data: dict) -> AuditLog:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return AuditLog(
            id=AuditLogMapper._oid(data.get("_id") or data.get("id")),
            entity_type=data.get("entity_type") or "",
            entity_id=AuditLogMapper._oid(data.get("entity_id")),
            action=data.get("action"),
            actor_id=AuditLogMapper._oid(data.get("actor_id")),
            action_at=data.get("action_at"),
            details=data.get("details") or {},
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(audit_log: AuditLog) -> dict:
        if not isinstance(audit_log, AuditLog):
            raise TypeError(f"to_persistence expected AuditLog, got {type(audit_log)}")

        lc = audit_log.lifecycle
        doc = {
            "entity_type": audit_log.entity_type,
            "entity_id": AuditLogMapper._oid(audit_log.entity_id),
            "action": audit_log.action.value if hasattr(audit_log.action, "value") else str(audit_log.action),
            "actor_id": AuditLogMapper._oid(audit_log.actor_id),
            "action_at": audit_log.action_at,
            "details": audit_log.details,
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": AuditLogMapper._oid(lc.deleted_by),
            },
        }

        if audit_log.id:
            doc["_id"] = AuditLogMapper._oid(audit_log.id)

        return doc

    @staticmethod
    def to_dto(audit_log: AuditLog) -> AuditLogDTO:
        lc = audit_log.lifecycle
        return AuditLogDTO(
            id=str(audit_log.id),
            entity_type=audit_log.entity_type,
            entity_id=AuditLogMapper._sid(audit_log.entity_id),
            action=audit_log.action.value if hasattr(audit_log.action, "value") else str(audit_log.action),
            actor_id=AuditLogMapper._sid(audit_log.actor_id),
            action_at=audit_log.action_at,
            details=audit_log.details,
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=lc.deleted_by,
            ),
        )
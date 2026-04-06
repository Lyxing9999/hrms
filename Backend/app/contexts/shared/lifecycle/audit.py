from __future__ import annotations
from typing import Any, Dict, Optional
from bson import ObjectId
from pymongo.collection import Collection

from app.contexts.shared.time_utils import utc_now


def append_history(
    collection: Collection,
    entity_id: ObjectId,
    event: str,
    actor_id: ObjectId,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    collection.update_one(
        {"_id": entity_id},
        {"$push": {"history": {
            "event": event,
            "at": utc_now().isoformat(),
            "meta": {"actor_id": str(actor_id), **(meta or {})},
        }}}
    )


def write_audit_log(
    audit_collection: Collection,
    *,
    actor_id: ObjectId,
    entity: str,
    entity_id: ObjectId,
    action: str,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    audit_collection.insert_one({
        "actor_id": actor_id,
        "entity": entity,
        "entity_id": entity_id,
        "action": action,
        "meta": meta or {},
        "created_at": utc_now(),
    })
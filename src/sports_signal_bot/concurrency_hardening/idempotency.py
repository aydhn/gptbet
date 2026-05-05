import uuid
import datetime
from typing import Dict, Any, List

from .contracts import (
    IdempotencyRecord, IdempotencyKeyRecord, SideEffectRecord,
    SideEffectReplayRecord, DuplicateExecutionRecord, IdempotencyHealthRecord,
    IdempotencyManifestRecord, IdempotencyWarningRecord
)

def build_idempotency_contract(target_ref: str, key_value: str) -> IdempotencyRecord:
    """Builds an idempotency contract for a target surface."""
    record_id = f"idem_{uuid.uuid4().hex[:8]}"
    key_id = f"idk_{uuid.uuid4().hex[:8]}"

    return IdempotencyRecord(
        idempotency_id=record_id,
        target_ref=target_ref,
        key_ref=key_id,
        status="protected",
        warnings=[]
    )

def build_idempotency_key(base_data: str) -> IdempotencyKeyRecord:
    """Generates an idempotency key."""
    # Simplified hashing
    import hashlib
    key_val = hashlib.sha256(base_data.encode()).hexdigest()[:16]

    return IdempotencyKeyRecord(
        key_id=f"idk_{uuid.uuid4().hex[:8]}",
        value=key_val
    )

def detect_duplicate_execution(executed_keys: List[str], new_key: str) -> bool:
    """Detects if an execution is a duplicate based on its key."""
    return new_key in executed_keys

def summarize_idempotency_health(records: List[IdempotencyRecord], duplicates: List[DuplicateExecutionRecord]) -> IdempotencyManifestRecord:
    """Summarizes idempotency health."""
    health = IdempotencyHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=len(duplicates) == 0,
        status_summary=f"Found {len(duplicates)} duplicate execution attempts."
    )

    return IdempotencyManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        records=records,
        health=health
    )

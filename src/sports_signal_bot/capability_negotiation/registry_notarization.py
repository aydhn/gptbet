import uuid
import hashlib
from datetime import datetime
from typing import Dict, Any

from sports_signal_bot.capability_negotiation.contracts import (
    RegistrySnapshotNotarizationRecord,
    RegistrySnapshotDigestRecord,
    NotarizedRegistryViewRecord,
    RegistryNotaryReceiptRecord
)

def build_registry_snapshot_digest(snapshot_data: Dict[str, Any]) -> RegistrySnapshotDigestRecord:
    # Deterministic serialization simulation
    data_str = str(snapshot_data).encode('utf-8')
    digest = hashlib.sha256(data_str).hexdigest()
    return RegistrySnapshotDigestRecord(
        snapshot_id=str(uuid.uuid4()),
        digest=digest
    )

def request_registry_notarization(registry_ref: str, snapshot_data: Dict[str, Any]) -> RegistrySnapshotNotarizationRecord:
    digest_rec = build_registry_snapshot_digest(snapshot_data)

    # Simulate a notary signing the digest
    receipt = RegistryNotaryReceiptRecord(
        receipt_id=str(uuid.uuid4()),
        signature=f"sig_{digest_rec.digest[:8]}"
    )

    view = NotarizedRegistryViewRecord(
        view_id=str(uuid.uuid4()),
        snapshot_digest=digest_rec,
        receipt=receipt
    )

    return RegistrySnapshotNotarizationRecord(
        notarization_id=str(uuid.uuid4()),
        registry_ref=registry_ref,
        view=view,
        created_at=datetime.utcnow().isoformat()
    )

def verify_registry_notarization(notarization: RegistrySnapshotNotarizationRecord, current_snapshot_data: Dict[str, Any]) -> bool:
    current_digest = build_registry_snapshot_digest(current_snapshot_data)
    if current_digest.digest != notarization.view.snapshot_digest.digest:
        return False
    return True

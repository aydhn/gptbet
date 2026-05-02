from datetime import datetime
import hashlib
import json
from typing import Dict, Any, List

from src.sports_signal_bot.resilience_fabric.contracts import (
    RelayEnvelopeRecord,
    RelayHealthRecord,
    ExternalEventRelayRecord
)

def build_relay_envelope(relay_id: str, event_family: str, source_identity: str, payload: Dict[str, Any]) -> RelayEnvelopeRecord:
    payload_str = json.dumps(payload, sort_keys=True)
    event_hash = hashlib.sha256(payload_str.encode()).hexdigest()

    return RelayEnvelopeRecord(
        sequence_hint=None,
        freshness_hint=None,
        integrity_hint=None,
        envelope_id=f"env_{event_hash[:8]}",
        relay_id=relay_id,
        event_family=event_family,
        source_identity=source_identity,
        event_hash=event_hash,
        payload=payload
    )

def verify_relay_envelope(envelope: RelayEnvelopeRecord) -> bool:
    payload_str = json.dumps(envelope.payload, sort_keys=True)
    expected_hash = hashlib.sha256(payload_str.encode()).hexdigest()
    return expected_hash == envelope.event_hash

def decide_relay_lane(envelope: RelayEnvelopeRecord, relay: ExternalEventRelayRecord) -> str:
    if relay.review_policy == "review_quarantine_bridge":
        return "quarantine"
    if not verify_relay_envelope(envelope):
        return "quarantine"
    return "verified_signal"

def compute_relay_health(relay_id: str, continuity: float, freshness: float, integrity: float, quarantine_ratio: float) -> RelayHealthRecord:
    status = "healthy"
    warnings = []

    if quarantine_ratio > 0.3:
        status = "degraded"
        warnings.append("High quarantine ratio")
    elif integrity < 0.9:
        status = "caution"
        warnings.append("Integrity failures detected")

    return RelayHealthRecord(
        relay_id=relay_id,
        status=status,
        delivery_continuity_score=continuity,
        freshness_adherence_score=freshness,
        integrity_verification_success_rate=integrity,
        quarantine_ratio=quarantine_ratio,
        warnings=warnings
    )

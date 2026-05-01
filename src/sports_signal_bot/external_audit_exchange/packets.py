from typing import Dict, Any, List
from .contracts import ExternalAuditRequestRecord, ChallengeExchangePacketRecord
import datetime
import uuid

def redact_exchange_payload(payload: Dict[str, Any], profile: str) -> Dict[str, Any]:
    redacted = payload.copy()
    if profile == "strict":
        if "sensitive_data" in redacted:
            redacted["sensitive_data"] = "[REDACTED]"
    return redacted

def attach_required_proofs(packet: Dict[str, Any], proofs: List[str]) -> Dict[str, Any]:
    packet["proofs"] = proofs
    return packet

def validate_packet_safety(packet: Dict[str, Any]) -> bool:
    if "sensitive_data" in packet and packet["sensitive_data"] != "[REDACTED]":
        return False
    return True

def render_packet_summary(packet: Dict[str, Any]) -> str:
    return f"Packet target: {packet.get('target_ref', 'unknown')}"

def build_safe_exchange_packet(
    target_ref: str,
    payload: Dict[str, Any],
    profile: str = "strict",
    proofs: List[str] = None
) -> ChallengeExchangePacketRecord:
    redacted_payload = redact_exchange_payload(payload, profile)
    if proofs:
        redacted_payload = attach_required_proofs(redacted_payload, proofs)

    if not validate_packet_safety(redacted_payload):
        raise ValueError("Packet safety validation failed.")

    return ChallengeExchangePacketRecord(
        packet_id=str(uuid.uuid4()),
        challenge_ref=f"chal_{target_ref}",
        severity="medium",
        target_ref=target_ref,
        safe_payload=redacted_payload
    )

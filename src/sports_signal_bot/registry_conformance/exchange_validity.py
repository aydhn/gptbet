from datetime import datetime, timezone
from typing import List, Tuple
from .contracts import AttestationExchangePacketRecord


def watch_attestation_exchange_validity(
    packet: AttestationExchangePacketRecord,
) -> Tuple[str, List[str]]:
    now = datetime.now(timezone.utc)
    reasons = []

    if packet.validity_window.valid_until < now:
        reasons.append("Exchange packet validity window expired.")
        return "exchange_expired", reasons

    if packet.exchange_status in [
        "exchanged_blocked",
        "exchanged_expired",
        "exchanged_superseded",
    ]:
        reasons.append(f"Packet already in terminal state: {packet.exchange_status}")
        return packet.exchange_status, reasons

    if len(packet.caveat_refs) > 0:
        return "exchange_caveated", ["Packet contains caveats."]

    return "exchange_remains_valid", []


def invalidate_exchange_on_dependency_change(
    packet: AttestationExchangePacketRecord, reason: str
) -> AttestationExchangePacketRecord:
    packet.exchange_status = "exchanged_invalidated"
    packet.warnings.append(f"Invalidated due to dependency change: {reason}")
    return packet


def explain_exchange_watcher_decision(status: str, reasons: List[str]) -> str:
    if reasons:
        reasons_str = ", ".join(reasons)
        return f"Exchange status is {status} because: {reasons_str}"
    return f"Exchange status is {status}."

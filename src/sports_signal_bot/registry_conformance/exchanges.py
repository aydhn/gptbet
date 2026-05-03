from datetime import datetime, timezone
import uuid
from typing import List, Optional
from .contracts import (
    AttestationExchangePacketRecord,
    AttestationExchangeScopeRecord,
    RegistryFreshnessRecord,
    ExchangeCaveatRecord,
    AttestationExchangeDecisionRecord,
)


def build_attestation_exchange_packet(
    source_registry_ref: str,
    attestation_refs: List[str],
    corridor_refs: List[str],
    treaty_refs: List[str],
    scope: str,
    valid_until: datetime,
) -> AttestationExchangePacketRecord:
    now = datetime.now(timezone.utc)

    exchange_scope = AttestationExchangeScopeRecord(scope=scope)

    freshness = RegistryFreshnessRecord(
        last_verified_at=now, valid_until=valid_until, is_stale=False
    )

    return AttestationExchangePacketRecord(
        exchange_packet_id=f"packet_{uuid.uuid4().hex[:8]}",
        source_registry_ref=source_registry_ref,
        attestation_refs=attestation_refs,
        corridor_refs=corridor_refs,
        treaty_refs=treaty_refs,
        exchange_scope=exchange_scope,
        validity_window=freshness,
        exchange_status="prepared",
    )


def validate_attestation_for_exchange(
    packet: AttestationExchangePacketRecord,
) -> AttestationExchangeDecisionRecord:
    now = datetime.now(timezone.utc)
    if packet.validity_window.valid_until < now:
        packet.exchange_status = "exchanged_blocked"
        return AttestationExchangeDecisionRecord(
            decision="blocked",
            reason="Attestation exchange packet has expired validity window.",
        )

    if not packet.attestation_refs:
        packet.exchange_status = "exchanged_blocked"
        return AttestationExchangeDecisionRecord(
            decision="blocked",
            reason="No attestations provided in the exchange packet.",
        )

    packet.exchange_status = "validated"
    return AttestationExchangeDecisionRecord(
        decision="validated", reason="Packet passed validation."
    )


def apply_exchange_constraints(
    packet: AttestationExchangePacketRecord, caveats: List[ExchangeCaveatRecord]
) -> AttestationExchangePacketRecord:
    packet.caveat_refs.extend(caveats)
    if caveats:
        packet.exchange_status = "exchanged_caveated"
    return packet


def summarize_attestation_exchange(packet: AttestationExchangePacketRecord) -> dict:
    return {
        "packet_id": packet.exchange_packet_id,
        "scope": packet.exchange_scope.scope,
        "status": packet.exchange_status,
        "caveat_count": len(packet.caveat_refs),
        "attestation_count": len(packet.attestation_refs),
    }

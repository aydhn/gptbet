from typing import List, Optional
from datetime import datetime
from .contracts import AssuranceExchangePacketRecord
from sports_signal_bot.assurance.contracts import ClaimValidityWindowRecord

def build_exchange_packet(
    exchange_packet_id: str,
    packet_family: str,
    source_registry_ref: str,
    carried_bundle_refs: List[str],
    claim_refs: List[str],
    attestation_refs: List[str],
    proof_refs: List[str],
    target_registry_ref: Optional[str] = None,
    translation_refs: Optional[List[str]] = None,
    notarization_refs: Optional[List[str]] = None,
    valid_from: Optional[datetime] = None,
    valid_until: Optional[datetime] = None
) -> AssuranceExchangePacketRecord:
    """Builds a new assurance exchange packet."""
    validity = ClaimValidityWindowRecord(
        valid_from=valid_from or datetime.utcnow(),
        valid_until=valid_until
    )
    return AssuranceExchangePacketRecord(
        exchange_packet_id=exchange_packet_id,
        packet_family=packet_family,
        source_registry_ref=source_registry_ref,
        target_registry_ref=target_registry_ref,
        carried_bundle_refs=carried_bundle_refs,
        claim_refs=claim_refs,
        attestation_refs=attestation_refs,
        proof_refs=proof_refs,
        translation_refs=translation_refs or [],
        notarization_refs=notarization_refs or [],
        validity_window=validity,
        warnings=[]
    )

def verify_exchange_packet_integrity(packet: AssuranceExchangePacketRecord) -> bool:
    """Verifies the structural integrity of an exchange packet."""
    if not packet.carried_bundle_refs and not packet.claim_refs:
        packet.warnings.append("Packet carries no bundles or claims")
        return False
    if packet.validity_window.valid_until and packet.validity_window.valid_until < datetime.utcnow():
        packet.warnings.append("Packet validity window has expired")
        return False
    return True

from typing import Dict, List, Any
from datetime import datetime
from .contracts import (
    PublicPacketRecord,
    ExternalVerifierPacketRecord,
    DisclosureBundleRecord,
    PublicationProfileRecord
)

def attach_disclosure_caveats(bundle: DisclosureBundleRecord) -> List[str]:
    return [w.description for w in bundle.warnings]

def build_public_packet(
    bundle: DisclosureBundleRecord,
    redacted_payload: Dict[str, Any],
    profile: PublicationProfileRecord,
    supersession_marker: str = None
) -> PublicPacketRecord:

    challenge_instructions = None
    if profile.challenge_intake_allowed:
        challenge_instructions = "Submit challenges via /api/v1/gateway/intake. Requires signed envelope for verification."

    return PublicPacketRecord(
        packet_id=f"pkt_pub_{bundle.disclosure_bundle_id}",
        bundle_id=bundle.disclosure_bundle_id,
        metadata={
            "profile": profile.profile_id,
            "family": bundle.bundle_family
        },
        claimed_content=redacted_payload,
        independently_checkable=bundle.verification_refs,
        proof_refs=bundle.verification_refs,
        redaction_notice=f"This packet has been redacted according to profile: {profile.profile_id}",
        caveats=attach_disclosure_caveats(bundle),
        publication_time=datetime.utcnow(),
        supersession_marker=supersession_marker,
        challenge_instructions=challenge_instructions
    )

def build_external_verifier_packet(
    base_packet: PublicPacketRecord,
    deeper_refs: List[str],
    witness_summary: str,
    audit_trail: List[str],
    correlation_ids: List[str],
    anomaly_context: str = None
) -> ExternalVerifierPacketRecord:
    return ExternalVerifierPacketRecord(
        packet_id=f"pkt_ver_{base_packet.bundle_id}",
        base_packet=base_packet,
        deeper_inclusion_refs=deeper_refs,
        broader_witness_summary=witness_summary,
        richer_anomaly_context=anomaly_context,
        audit_trail_linkage=audit_trail,
        exchange_request_correlation_ids=correlation_ids
    )

def validate_packet_profile_conformance(packet: PublicPacketRecord, profile: PublicationProfileRecord) -> bool:
    # A sanity check that could run before publishing
    # if profile does not allow challenge, packet should not have instructions
    if not profile.challenge_intake_allowed and packet.challenge_instructions:
        return False
    return True

def summarize_packet_verifiability(packet: PublicPacketRecord) -> Dict[str, Any]:
    return {
        "packet_id": packet.packet_id,
        "proof_count": len(packet.proof_refs),
        "checkable_items": len(packet.independently_checkable),
        "has_challenge_instructions": packet.challenge_instructions is not None
    }

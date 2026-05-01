from typing import Dict, Any, List
import uuid
from .contracts import VerificationViewPacketRecord
from .profiles import get_profile

def build_profile_specific_packet(profile_id: str, view_name: str, source_data: Dict[str, Any]) -> VerificationViewPacketRecord:
    profile = get_profile(profile_id)

    if view_name not in profile.visible_view_families:
        raise ValueError(f"View {view_name} not allowed for profile {profile_id}")

    packet = VerificationViewPacketRecord(
        packet_id=str(uuid.uuid4()),
        packet_family="verification_view",
        audience_profile=profile_id,
        view_name=view_name,
        redaction_profile=profile.signer_metadata_masking_level,
        freshness="current",
        supersession_status="active",
        content=source_data
    )

    if profile.proof_depth == "minimal":
        packet.proof_refs = ["basic_proof_ref"]
    elif profile.proof_depth == "standard":
        packet.proof_refs = ["basic_proof_ref", "standard_proof_ref"]
    else:
        packet.proof_refs = ["basic_proof_ref", "standard_proof_ref", "deep_proof_ref"]

    return packet

def compare_packet_depths(packet1: VerificationViewPacketRecord, packet2: VerificationViewPacketRecord) -> Dict[str, Any]:
    return {
        "packet1_profile": packet1.audience_profile,
        "packet2_profile": packet2.audience_profile,
        "packet1_proofs": len(packet1.proof_refs),
        "packet2_proofs": len(packet2.proof_refs)
    }

def validate_no_cross_profile_leakage(packet: VerificationViewPacketRecord, intended_profile: str) -> bool:
    return packet.audience_profile == intended_profile

def summarize_packet_differences(packets: List[VerificationViewPacketRecord]) -> Dict[str, Any]:
    return {p.audience_profile: len(p.proof_refs) for p in packets}

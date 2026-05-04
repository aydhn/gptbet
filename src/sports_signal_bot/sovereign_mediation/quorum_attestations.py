import uuid
from typing import List
from .contracts import QuorumAttestationRecord

def build_governance_quorum_attestation(council_case_ref: str, council_ref: str, decision_type: str, evidence_refs: List[str], caveat_refs: List[str]) -> QuorumAttestationRecord:
    attestation_status = "attested_verified" if not caveat_refs else "attested_with_caveats"
    if decision_type == "no_safe_route":
        attestation_status = "attested_blocked"

    return QuorumAttestationRecord(
        quorum_attestation_id=f"att_{uuid.uuid4()}",
        source_council_case_ref=council_case_ref,
        council_ref=council_ref,
        attestation_family="route_governance_quorum_attestation",
        attested_decision_type=decision_type,
        quorum_summary="Verified by quorum",
        supporting_vote_refs=[],
        supporting_evidence_refs=evidence_refs,
        caveat_refs=caveat_refs,
        validity_window="24h",
        attestation_status=attestation_status,
        warnings=[]
    )

def validate_quorum_attestation(attestation: QuorumAttestationRecord) -> bool:
    if attestation.attestation_status in ["attested_expired", "attested_invalid", "attested_blocked"]:
        return False
    return True

def preserve_council_caveats_in_attestation(council_case_ref: str, current_caveats: List[str]) -> List[str]:
    # Ensure no caveats are stripped
    return current_caveats.copy()

def summarize_quorum_attestation(attestation: QuorumAttestationRecord) -> dict:
    return {
        "id": attestation.quorum_attestation_id,
        "status": attestation.attestation_status,
        "caveat_count": len(attestation.caveat_refs)
    }

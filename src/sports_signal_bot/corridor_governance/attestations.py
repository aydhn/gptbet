from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sports_signal_bot.corridor_governance.contracts import (
    ContinuityAttestationRecord,
    AttestationValidityRecord
)

def build_continuity_attestation(
    attestation_id: str,
    continuity_session_ref: str,
    corridor_ref: str,
    treaty_ref: str,
    source_region_ref: str,
    target_region_ref: str,
    attestation_family: str,
    attested_dimensions: List[str],
    attestation_status: str,
    validity_window: Dict[str, str],
    caveat_refs: List[str],
    evidence_refs: List[str],
    warnings: List[str]
) -> ContinuityAttestationRecord:
    return ContinuityAttestationRecord(
        continuity_attestation_id=attestation_id,
        continuity_session_ref=continuity_session_ref,
        corridor_ref=corridor_ref,
        treaty_ref=treaty_ref,
        source_region_ref=source_region_ref,
        target_region_ref=target_region_ref,
        attestation_family=attestation_family,
        attested_dimensions=attested_dimensions,
        attestation_status=attestation_status,
        validity_window=validity_window,
        caveat_refs=caveat_refs,
        evidence_refs=evidence_refs,
        warnings=warnings
    )

def validate_attestation_against_continuity(attestation: ContinuityAttestationRecord) -> bool:
    if not attestation.continuity_session_ref:
        return False
    return True

def classify_attestation_strength(attestation: ContinuityAttestationRecord) -> str:
    if attestation.attestation_status == "attested_verified" and not attestation.caveat_refs:
        return "strong"
    elif attestation.attestation_status == "attested_with_caveats":
        return "workable"
    return "weak"

def summarize_attestation_state(attestations: List[ContinuityAttestationRecord]) -> Dict[str, int]:
    summary = {}
    for att in attestations:
        summary[att.attestation_status] = summary.get(att.attestation_status, 0) + 1
    return summary

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sports_signal_bot.corridor_governance.contracts import (
    ContinuityAttestationRecord,
    ContinuityAttestationInputRecord,
    AttestationValidityRecord
)

def build_continuity_attestation(
    input_record: ContinuityAttestationInputRecord
) -> ContinuityAttestationRecord:
    return ContinuityAttestationRecord(
        continuity_attestation_id=input_record.attestation_id,
        continuity_session_ref=input_record.continuity_session_ref,
        corridor_ref=input_record.corridor_ref,
        treaty_ref=input_record.treaty_ref,
        source_region_ref=input_record.source_region_ref,
        target_region_ref=input_record.target_region_ref,
        attestation_family=input_record.attestation_family,
        attested_dimensions=input_record.attested_dimensions,
        attestation_status=input_record.attestation_status,
        validity_window=input_record.validity_window,
        caveat_refs=input_record.caveat_refs,
        evidence_refs=input_record.evidence_refs,
        warnings=input_record.warnings
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

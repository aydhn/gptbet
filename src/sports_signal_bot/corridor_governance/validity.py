from datetime import datetime
from sports_signal_bot.corridor_governance.contracts import (
    ContinuityAttestationRecord,
    AttestationValidityRecord
)

def verify_attestation_validity_window(attestation: ContinuityAttestationRecord, current_time: datetime) -> AttestationValidityRecord:
    valid_from = attestation.validity_window.get("effective_from")
    valid_until = attestation.validity_window.get("effective_until")

    is_valid = True
    reason = "Valid within window"

    if valid_until:
        try:
            until_dt = datetime.fromisoformat(valid_until)
            if current_time > until_dt:
                is_valid = False
                reason = "Attestation expired"
        except ValueError:
            is_valid = False
            reason = "Invalid date format in validity window"

    return AttestationValidityRecord(
        attestation_id=attestation.continuity_attestation_id,
        is_valid=is_valid,
        reason=reason
    )

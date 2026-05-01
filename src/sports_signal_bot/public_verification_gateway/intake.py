from typing import Dict, List, Any, Optional
from datetime import datetime
from .contracts import (
    PublicChallengeEnvelopeRecord,
    PublicChallengeIntakeRecord,
    IntakeSanitizationRecord,
    ChallengeIntakeSchemaRecord,
    IntakeDedupRecord,
    ChallengeIntakeQuarantineRecord,
    IntakeQuarantineReasonRecord,
    ChallengeIntakeDecisionRecord
)

def validate_public_challenge_intake(
    envelope: PublicChallengeEnvelopeRecord,
    schema: ChallengeIntakeSchemaRecord
) -> tuple[bool, List[str]]:
    missing_fields = []
    for field in schema.required_fields:
        if field not in envelope.payload:
            missing_fields.append(field)

    if missing_fields:
        return False, [f"Missing required fields: {missing_fields}"]

    # We could also validate signature here if present
    if not envelope.signature:
        # A warning, not strictly invalid unless policy says so
        pass

    return True, []

def sanitize_intake_payload(
    intake_id: str,
    payload: Dict[str, Any],
    allowed_fields: List[str]
) -> tuple[Dict[str, Any], IntakeSanitizationRecord]:
    cleaned = {}
    rejected = []

    for k, v in payload.items():
        # Prevent very large strings
        if isinstance(v, str) and len(v) > 5000:
            rejected.append(f"{k}: Payload too large")
            continue

        if k in allowed_fields:
            cleaned[k] = v
        else:
            rejected.append(k)

    sanitization = IntakeSanitizationRecord(
        sanitization_id=f"san_{intake_id}",
        intake_id=intake_id,
        cleaned_fields=list(cleaned.keys()),
        rejected_fields=rejected
    )
    return cleaned, sanitization

def deduplicate_intake(
    intake: PublicChallengeIntakeRecord,
    payload: Dict[str, Any],
    recent_intakes: List[Dict[str, Any]]
) -> IntakeDedupRecord:
    # Extremely simplified dedup: check if claim description matches recently
    claim_desc = payload.get("claim", "")

    for recent in recent_intakes:
        if claim_desc and claim_desc == recent.get("payload", {}).get("claim", ""):
            return IntakeDedupRecord(
                dedup_id=f"dup_{intake.intake_id}",
                intake_id=intake.intake_id,
                duplicate_of=recent.get("intake_id")
            )

    return IntakeDedupRecord(
        dedup_id=f"dup_{intake.intake_id}",
        intake_id=intake.intake_id,
        duplicate_of=None
    )

def summarize_intake_outcome(
    intake: PublicChallengeIntakeRecord,
    decision: ChallengeIntakeDecisionRecord
) -> Dict[str, Any]:
    return {
        "intake_id": intake.intake_id,
        "trust_class": intake.trust_class,
        "action": decision.action,
        "reason": decision.reason
    }

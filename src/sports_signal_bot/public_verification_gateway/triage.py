from typing import Dict, List, Any
from datetime import datetime
from .contracts import (
    PublicChallengeIntakeRecord,
    ChallengeIntakeDecisionRecord,
    IntakeDedupRecord
)

def route_intake_to_review(
    intake: PublicChallengeIntakeRecord,
    dedup: IntakeDedupRecord,
    severity: str
) -> ChallengeIntakeDecisionRecord:

    if dedup.duplicate_of:
        return ChallengeIntakeDecisionRecord(
            decision_id=f"dec_{intake.intake_id}",
            intake_id=intake.intake_id,
            action="linked_to_existing_case",
            reason=f"Duplicate of {dedup.duplicate_of}"
        )

    if intake.trust_class == "anonymous_low_trust" and severity == "low":
        return ChallengeIntakeDecisionRecord(
            decision_id=f"dec_{intake.intake_id}",
            intake_id=intake.intake_id,
            action="review_required",
            reason="Low priority queue"
        )

    if intake.trust_class in ["trusted_exchange_partner", "known_responder_supported"]:
        return ChallengeIntakeDecisionRecord(
            decision_id=f"dec_{intake.intake_id}",
            intake_id=intake.intake_id,
            action="escalated_to_anomaly_case",
            reason=f"High trust ({intake.trust_class}), escalate immediately"
        )

    return ChallengeIntakeDecisionRecord(
        decision_id=f"dec_{intake.intake_id}",
        intake_id=intake.intake_id,
        action="review_required",
        reason="Standard triage queue"
    )

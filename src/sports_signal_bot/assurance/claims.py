from datetime import datetime
from .contracts import (
    AssuranceClaimRecord,
    ClaimType,
    ClaimInputRecord
)


def create_claim(input_record: ClaimInputRecord) -> AssuranceClaimRecord:
    return AssuranceClaimRecord(
        claim_id=input_record.claim_id,
        claim_family=input_record.family,
        claim_type=ClaimType.satisfied,
        target_family="promotion_candidate",
        target_ref=input_record.target_ref,
        claim_statement=input_record.statement,
        machine_checkable_status=True,
        support_strength=input_record.strength,
        dependency_refs=input_record.dependencies or [],
        evidence_refs=[f"ev_{input_record.claim_id}_01"],
        proof_refs=[f"proof_{input_record.claim_id}_01"]
    )


def evaluate_claim_freshness(
    claim: AssuranceClaimRecord
) -> AssuranceClaimRecord:
    delta = datetime.utcnow() - claim.freshness.evaluated_at
    if delta.total_seconds() > 86400:
        claim.freshness.is_stale = True
        claim.claim_type = ClaimType.stale
    return claim

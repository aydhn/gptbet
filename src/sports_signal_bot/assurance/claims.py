from datetime import datetime
from typing import List, Optional
from .contracts import (AssuranceClaimRecord, ClaimFamily, ClaimType,
                        SupportStrength, ClaimFreshnessRecord, ClaimValidityWindowRecord)

def create_claim(
    claim_id: str,
    family: ClaimFamily,
    target_ref: str,
    statement: str,
    strength: SupportStrength,
    dependencies: Optional[List[str]] = None
) -> AssuranceClaimRecord:
    return AssuranceClaimRecord(
        claim_id=claim_id,
        claim_family=family,
        claim_type=ClaimType.satisfied,
        target_family="promotion_candidate",
        target_ref=target_ref,
        claim_statement=statement,
        machine_checkable_status=True,
        support_strength=strength,
        dependency_refs=dependencies or [],
        evidence_refs=[f"ev_{claim_id}_01"],
        proof_refs=[f"proof_{claim_id}_01"]
    )

def evaluate_claim_freshness(claim: AssuranceClaimRecord) -> AssuranceClaimRecord:
    delta = datetime.utcnow() - claim.freshness.evaluated_at
    if delta.total_seconds() > 86400:
        claim.freshness.is_stale = True
        claim.claim_type = ClaimType.stale
    return claim

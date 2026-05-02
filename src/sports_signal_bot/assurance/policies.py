from typing import List, Optional
from .contracts import ClaimFamily, ClaimFreshnessRecord, AttestationIssuerFamily

def evaluate_claim_acceptance(
    claim_family: ClaimFamily,
    support_strength: str,
    freshness: ClaimFreshnessRecord
) -> bool:
    if freshness.is_stale:
        return False
    if support_strength in ["speculative", "none"]:
        return False
    return True

def determine_required_claims(target_family: str) -> List[ClaimFamily]:
    if target_family == "promotion_candidate":
        return [
            ClaimFamily.policy_conformance_claim,
            ClaimFamily.integrity_chain_claim,
            ClaimFamily.transparency_publication_claim,
            ClaimFamily.e2e_promotion_claim
        ]
    return [ClaimFamily.policy_conformance_claim]

from typing import List, Tuple
from .base import BaseAssuranceStrategy
from ..contracts import ClaimFamily, PromotionEnvelopeRecord, AssuranceClaimRecord, EnvelopeStatus

class BalancedProofCarryingStrategy(BaseAssuranceStrategy):
    name: str = "balanced_proof_carrying_strategy"

    def get_required_claim_families(self) -> List[ClaimFamily]:
        return [
            ClaimFamily.policy_conformance_claim,
            ClaimFamily.integrity_chain_claim,
            ClaimFamily.transparency_publication_claim,
            ClaimFamily.e2e_promotion_claim
        ]

    def evaluate_envelope(self, envelope: PromotionEnvelopeRecord, claims: List[AssuranceClaimRecord]) -> Tuple[bool, str]:
        if envelope.final_assurance_decision == EnvelopeStatus.assurance_blocked:
            return False, "Envelope blocked due to stale or invalid claims."

        satisfied_fams = [c.claim_family for c in claims if c.claim_id in envelope.satisfied_claims]
        missing = [f for f in self.get_required_claim_families() if f not in satisfied_fams]

        if missing:
            return False, f"Missing required claim families: {[m.value for m in missing]}"

        return True, "Balanced assurance criteria met."

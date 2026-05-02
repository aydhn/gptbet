from typing import List, Tuple
from .base import BaseAssuranceStrategy
from ..contracts import ClaimFamily, PromotionEnvelopeRecord, AssuranceClaimRecord

class ConservativeAssuranceEnvelopeStrategy(BaseAssuranceStrategy):
    name: str = "conservative_assurance_strategy"

    def get_required_claim_families(self) -> List[ClaimFamily]:
        return list(ClaimFamily)

    def evaluate_envelope(self, envelope: PromotionEnvelopeRecord, claims: List[AssuranceClaimRecord]) -> Tuple[bool, str]:
        if envelope.blocked_claims:
            return False, "Conservative strategy prohibits any blocked claims."
        return True, "Passed."

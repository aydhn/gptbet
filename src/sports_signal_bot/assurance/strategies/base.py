from typing import List, Tuple
from ..contracts import ClaimFamily, PromotionEnvelopeRecord, AssuranceClaimRecord

class BaseAssuranceStrategy:
    name: str = "base_strategy"

    def get_required_claim_families(self) -> List[ClaimFamily]:
        raise NotImplementedError

    def evaluate_envelope(self, envelope: PromotionEnvelopeRecord, claims: List[AssuranceClaimRecord]) -> Tuple[bool, str]:
        raise NotImplementedError
